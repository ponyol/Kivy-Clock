### Technical Specification: Configurable Kivy Clock

### 1. Project Overview

**Description:**
A simple, minimal "Fullscreen Clock" desktop application. The application's primary goal is to display the current system time in a large, highly-readable format, suitable for use as a desk clock or focus timer.

The application must be configurable, allowing the user to select the launch mode (fullscreen or windowed) and customize core aesthetics (font and color) via a built-in settings panel.

### 2. Core Functional Requirements

1.  **Primary Display (Time):** The main view will display the current system time in `HH:MM:SS` format.
2.  **Secondary Display (Date):** **[NEW]** Above the time, the current date and day of the week (e.g., "Monday, November 17") will be displayed.
3.  **Layout:** The entire block (Date + Time) must be perfectly centered vertically and horizontally. The text within the block must also be center-aligned.
4.  **Relative Sizing:** **[NEW]** The font size of the Date display will be **50%** of the font size of the Time display.
5.  **Update Frequency:** The time (and date, if it changes) must update every second.
6.  **Exit:** The application must close gracefully when the `Esc` key is pressed.
7.  **Settings Panel:** The application must provide a settings panel, accessible via the `F1` key.
8.  **Configurable Launch Mode:** The user must be able to choose via the settings panel whether the app launches in fullscreen or a large windowed mode.
9.  **Configurable Aesthetics:** The user must be able to change the following via the settings panel, and **[UPDATED]** the changes must apply to *both* the time and date labels:
      * **Font:** A selection of pre-packaged fonts.
      * **Color:** The text color (e.g., via a hex code input).

### 3. Technical Stack

  * **Language:** Python 3.9+
  * **GUI Framework:** Kivy (v2.3.0 or newer)
  * **Dependencies:** `kivy`

### 4. Application Architecture and Structure

**[UPDATED]** The UI structure is modified to accommodate two labels instead of one. The `FloatLayout` will now center a vertical `BoxLayout` which contains the two labels.

  * **`main.py` (Application Logic):**

      * **`ClockApp(App)`:** No major change. Logic for `on_config_change` will now update two labels instead of one.
      * **`ClockLayout(FloatLayout)`:** The root widget.
          * Will contain a `BoxLayout` (which in turn holds the labels).
          * The `update_time(self, dt)` method will now be responsible for updating the text of *both* labels (`time_label` and `date_label`).

  * **`clock.kv` (UI Presentation):** **[UPDATED]**

      * The root widget `ClockLayout` (a `FloatLayout`) remains.
      * Inside it, a `BoxLayout` will be added to group the labels vertically.
      * **Structure:**

    <!-- end list -->

    ```kv
    <ClockLayout>:
        BoxLayout:
            id: info_container
            orientation: 'vertical'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (None, None) // Size will be based on children
            size: self.texture_size  // Wrap content
            spacing: root.height * 0.02 // Small dynamic spacing

            Label:
                id: date_label
                text: "Monday, November 17" // Placeholder
                font_size: root.height / 10 // 50% of time_label
                halign: 'center'
                // font_name and color will be set from Python

            Label:
                id: time_label
                text: "13:35:27" // Placeholder
                font_size: root.height / 5 // Main size
                halign: 'center'
                // font_name and color will be set from Python
    ```

  * **`settings.json` (Configuration Definition):**

      * No changes required to this file. The existing settings for `font` and `color` will be programmatically applied to both labels.

### 5. Key Implementation Details

  * **Config & Settings Panel:** **[UPDATED]**

      * The `on_config_change` method will be updated to apply changes to both labels.

    <!-- end list -->

    ```python
    # In ClockApp(App)
    def on_config_change(self, config, section, key, value):
        if section == 'Aesthetics':
            if key == 'font':
                font_file = f'fonts/{value}.ttf'
                self.root.ids.time_label.font_name = font_file
                self.root.ids.date_label.font_name = font_file
            if key == 'color':
                color_val = get_color_from_hex(value) # Helper function
                self.root.ids.time_label.color = color_val
                self.root.ids.date_label.color = color_val
    ```

  * **Time Update Logic:** **[UPDATED]**

      * The `update_time` method in `ClockLayout` will be expanded.

    <!-- end list -->

    ```python
    # In ClockLayout(FloatLayout)
    def update_time(self, dt):
        now = datetime.now()
        # Set main time
        self.ids.time_label.text = now.strftime('%H:%M:%S')

        # Set date string
        # We check the current text to avoid re-rendering the same string
        # 60 times a minute (minor optimization)
        new_date_text = now.strftime('%A, %B %d')
        if self.ids.date_label.text != new_date_text:
            self.ids.date_label.text = new_date_text
    ```

  * **Keyboard Bindings:**

      * No changes. `Esc` and `F1` remain the same.

### 6. Potential Issues and Enhancements

  * **OOP vs FP Paradigm:** As noted before, Kivy is a heavily OOP/event-driven framework. This design adheres to Kivy's native patterns (subclassing `App`, using `SettingsPanel`), which is not a functional approach. This is a deliberate choice to use the framework correctly.
  * **Font Management:** All fonts listed in `settings.json` *must* be bundled in a `fonts/` directory and correctly referenced.
  * **Color Input:** The `[string]` setting for color requires the user to know hex codes. A custom `SettingItem` with a color wheel would be a major enhancement but is outside the scope of this initial "simple" build. We will rely on simple string input.
  * **Live Launch Mode Change:** Changing the `launch_mode` setting will require the user to restart the app for it to take effect. This should be noted in the setting's description in `settings.json`.

### 7. Deliverables

1.  **`main.py`**: Main application file (Python).
2.  **`clock.kv`**: Kivy language file (UI).
3.  **`settings.json`**: Settings panel definition.
4.  **`requirements.txt`**: Project dependencies (`kivy>=2.3.0`).
5.  **`fonts/` (Directory)**:
      * `fonts/Roboto-Thin.ttf`
      * `fonts/DSEG7Classic-Regular.ttf` (or similar digital font)
