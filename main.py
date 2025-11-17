#!/usr/bin/env python3
"""
Configurable Kivy Clock Application

A fullscreen/windowed clock application with customizable fonts and colors.
Displays current time and date with support for multiple monospace and digital fonts.
"""

from datetime import datetime
from pathlib import Path
from typing import Tuple

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex as kivy_get_color_from_hex


# NOTE: Pre-configure window before any other imports
# This ensures settings are applied before window creation
def _preconfigure_window():
    """
    Pre-configure window settings before Kivy initializes.
    This function must be called before any widget imports.
    """
    # Read config early to determine window mode
    from kivy.config import ConfigParser
    config = ConfigParser()
    config.read('clock.ini')

    launch_mode = config.getdefault('Display', 'launch_mode', 'windowed')

    if launch_mode == 'fullscreen':
        Config.set('graphics', 'fullscreen', 'auto')
    else:
        Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '1024')
        Config.set('graphics', 'height', '768')

    Config.write()


# Pre-configure before continuing
_preconfigure_window()


# Background color presets
# NOTE: These are inspired by macOS dark mode aesthetics
BACKGROUND_PRESETS = {
    'Dark Gray': '#2B2B2B',      # Current default
    'Pure Black': '#000000',      # Perfect for OLED screens
    'Graphite': '#3C3C3C',       # macOS Graphite appearance
    'Midnight Blue': '#0F1419',  # Deep blue-black
    'Dark Navy': '#1A1F3A',      # Navy blue dark mode
    'Forest Green': '#0F1F0F',   # Dark forest green
    'Charcoal': '#222222',       # Charcoal gray
}


def get_background_color(preset: str, custom_color: str = '') -> Tuple[float, float, float, float]:
    """
    Returns background color based on preset name or custom hex.

    Args:
        preset: Name of the background preset
        custom_color: Custom hex color (used only if preset is 'Custom')

    Returns:
        RGBA tuple with values between 0 and 1

    NOTE: If preset is 'Custom', uses custom_color, otherwise uses preset from BACKGROUND_PRESETS
    """
    if preset == 'Custom':
        if custom_color:
            return get_color_from_hex(custom_color)
        else:
            # Fallback to Dark Gray if Custom selected but no color provided
            print("WARNING: 'Custom' background selected but no color provided, using Dark Gray")
            return get_color_from_hex(BACKGROUND_PRESETS['Dark Gray'])

    # Get color from presets
    hex_color = BACKGROUND_PRESETS.get(preset, BACKGROUND_PRESETS['Dark Gray'])
    return get_color_from_hex(hex_color)


def get_color_from_hex(hex_color: str) -> Tuple[float, float, float, float]:
    """
    Converts a hex color string to RGBA tuple.

    Args:
        hex_color: Hex color code (e.g., '#FF0000' or 'FF0000')

    Returns:
        RGBA tuple with values between 0 and 1

    NOTE: Kivy uses 0-1 range for colors, not 0-255
    """
    try:
        # Remove '#' if present and ensure proper format
        hex_color = hex_color.strip().lstrip('#')

        # Validate hex format
        if len(hex_color) not in (3, 6):
            raise ValueError(f"Invalid hex color length: {hex_color}")

        # Expand shorthand (e.g., 'F00' -> 'FF0000')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)

        return kivy_get_color_from_hex(f'#{hex_color}')

    except (ValueError, AttributeError) as e:
        # Fallback to red if parsing fails
        print(f"WARNING: Invalid color '{hex_color}', using red as fallback: {e}")
        return (1.0, 0.0, 0.0, 1.0)


class ClockLayout(FloatLayout):
    """
    Main layout containing the clock display.

    Handles time updates and keyboard input for the application.
    """

    # Background color property (RGBA tuple)
    bg_color = ListProperty([0.169, 0.169, 0.169, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Schedule time updates every second
        # NOTE: Keep reference to prevent garbage collection
        self._update_event = Clock.schedule_interval(self.update_time, 1)

        # Setup keyboard bindings
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # Initial time update (don't wait 1 second)
        Clock.schedule_once(lambda dt: self.update_time(0), 0)

    def update_time(self, dt: float) -> None:
        """
        Updates the time and date labels.

        Args:
            dt: Delta time since last call (provided by Clock)

        NOTE: We check if date text changed to avoid unnecessary re-renders
        (minor optimization - date only changes once per day)
        """
        now = datetime.now()

        # Update time label (always changes every second)
        self.ids.time_label.text = now.strftime('%H:%M:%S')

        # Update date label (only if it changed)
        new_date_text = now.strftime('%A, %B %d')
        if self.ids.date_label.text != new_date_text:
            self.ids.date_label.text = new_date_text

    def _keyboard_closed(self) -> None:
        """
        Callback when keyboard is released.
        Unbinds the keyboard to prevent memory leaks.
        """
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(
        self,
        keyboard,
        keycode: Tuple[int, str],
        text: str,
        modifiers: list
    ) -> bool:
        """
        Handles keyboard input.

        Args:
            keyboard: Keyboard instance
            keycode: Tuple of (key_code, key_name)
            text: Text representation of the key
            modifiers: List of active modifiers (shift, ctrl, etc.)

        Returns:
            True if the key was handled, False otherwise
        """
        key_name = keycode[1]

        # ESC: Close application
        if key_name == 'escape':
            App.get_running_app().stop()
            return True

        # F1: Open settings panel
        elif key_name == 'f1':
            App.get_running_app().open_settings()
            return True

        return False


class ClockApp(App):
    """
    Main application class for the Configurable Kivy Clock.

    Manages application lifecycle, configuration, and settings panel.
    """

    def build(self) -> ClockLayout:
        """
        Builds and returns the root widget.

        Returns:
            ClockLayout instance as the root widget
        """
        self.title = 'Configurable Clock'
        return ClockLayout()

    def build_config(self, config) -> None:
        """
        Sets default configuration values.

        Args:
            config: ConfigParser instance

        NOTE: These values are used if no config file exists
        """
        config.setdefaults('Display', {
            'launch_mode': 'windowed'
        })

        config.setdefaults('Aesthetics', {
            'background': 'Dark Gray',
            'custom_background': '#2B2B2B',
            'font': 'Roboto-Thin',
            'color': '#FF0000'
        })

    def build_settings(self, settings) -> None:
        """
        Loads the settings panel from JSON definition.

        Args:
            settings: Settings instance
        """
        settings_path = Path(__file__).parent / 'settings.json'
        settings.add_json_panel(
            'Clock Settings',
            self.config,
            str(settings_path)
        )

    def on_start(self) -> None:
        """
        Called when the application starts.
        Applies initial configuration to the UI.
        """
        super().on_start()

        # Apply initial background, font and color settings
        self._apply_background()
        self._apply_aesthetics()

    def on_config_change(
        self,
        config,
        section: str,
        key: str,
        value: str
    ) -> None:
        """
        Callback fired when settings are changed.

        Args:
            config: ConfigParser instance
            section: Section name that changed
            key: Key name that changed
            value: New value

        NOTE: Launch mode changes require app restart to take effect
        """
        if config is not self.config:
            return

        if section == 'Aesthetics':
            # Background changes
            if key in ('background', 'custom_background'):
                self._apply_background()
            # Font and color changes
            else:
                self._apply_aesthetics()

        elif section == 'Display' and key == 'launch_mode':
            print(
                f"INFO: Launch mode changed to '{value}'. "
                "Please restart the application for this change to take effect."
            )

    def _apply_background(self) -> None:
        """
        Applies background color to the root layout.

        Uses the background preset or custom color from settings.
        """
        if not self.root:
            return

        # Get current settings
        background_preset = self.config.get('Aesthetics', 'background')
        custom_bg = self.config.get('Aesthetics', 'custom_background')

        # Get background color
        bg_rgba = get_background_color(background_preset, custom_bg)

        # Apply to root layout
        self.root.bg_color = bg_rgba

    def _apply_aesthetics(self) -> None:
        """
        Applies font and color settings to both labels.

        This is a helper method to avoid code duplication.
        Font and color settings apply to both date_label and time_label.
        """
        if not self.root:
            return

        # Get current settings
        font_name = self.config.get('Aesthetics', 'font')
        color_hex = self.config.get('Aesthetics', 'color')

        # Construct font path
        font_path = Path(__file__).parent / 'fonts' / f'{font_name}.ttf'

        # Validate font file exists
        if not font_path.exists():
            print(f"WARNING: Font file not found: {font_path}")
            print("Using default Kivy font")
            font_path = None

        # Convert color
        color_rgba = get_color_from_hex(color_hex)

        # Apply to both labels
        if font_path:
            self.root.ids.time_label.font_name = str(font_path)
            self.root.ids.date_label.font_name = str(font_path)

        self.root.ids.time_label.color = color_rgba
        self.root.ids.date_label.color = color_rgba


def main():
    """Application entry point."""
    ClockApp().run()


if __name__ == '__main__':
    main()
