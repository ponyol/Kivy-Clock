# Configurable Kivy Clock

A simple, minimal fullscreen/windowed clock application built with Kivy. Displays the current system time in a large, highly-readable format with customizable fonts and colors.

## Features

- **Dual Display**: Shows both date (day of week, month, day) and time (HH:MM:SS)
- **Configurable Launch Mode**: Choose between fullscreen or windowed mode (1024x768)
- **Multiple Fonts**: 6 professional fonts included:
  - Roboto Thin (modern, thin)
  - DSEG7 Classic (digital 7-segment display)
  - Ubuntu Mono (console font)
  - DejaVu Sans Mono (console font)
  - Source Code Pro (Adobe console font)
  - Fira Mono (Mozilla console font)
- **Customizable Colors**: Set text color via hex code
- **Clean UI**: Dark gray background with centered, perfectly aligned text
- **Keyboard Shortcuts**:
  - `F1` - Open settings panel
  - `Esc` - Exit application

## Installation

### Prerequisites

- Python 3.9 or newer
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Download fonts if not already present:

```bash
python3 download_fonts.py
```

## Usage

### Running the Application

```bash
python3 main.py
```

### Configuration

Press `F1` while the application is running to open the settings panel.

**Available Settings:**

1. **Launch Mode** (requires restart)
   - `windowed` - Opens in a 1024x768 window (default)
   - `fullscreen` - Opens in fullscreen mode

2. **Font**
   - Select from 6 pre-installed fonts
   - Default: Roboto Thin

3. **Text Color**
   - Enter hex color code (e.g., `#FF0000` for red, `#00FF00` for green)
   - Default: Red (`#FF0000`)

**NOTE:** Changes to Launch Mode require restarting the application to take effect. Font and color changes apply immediately.

## Project Structure

```
Kivy-Clock/
├── main.py                    # Main application logic
├── clock.kv                   # Kivy UI definition
├── settings.json              # Settings panel configuration
├── requirements.txt           # Python dependencies
├── download_fonts.py          # Font downloader utility
├── fonts/                     # Font files directory
│   ├── Roboto-Thin.ttf
│   ├── DSEG7Classic-Regular.ttf
│   ├── UbuntuMono-Regular.ttf
│   ├── DejaVuSansMono.ttf
│   ├── SourceCodePro-Regular.ttf
│   └── FiraMono-Regular.ttf
└── clock.ini                  # Generated config file (created on first run)
```

## Technical Details

- **Framework**: Kivy 2.3.1
- **Language**: Python 3.11+
- **Update Frequency**: 1 second (time updates every second, date updates when it changes)
- **Default Window Size**: 1024x768 (windowed mode)
- **Default Colors**: Dark gray background (#2B2B2B), red text (#FF0000)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Esc` | Exit application |
| `F1` | Open settings panel |

## License

See [LICENSE](LICENSE) file for details.

## Development

This project follows functional programming principles where practical within the constraints of Kivy's object-oriented framework.

Key architectural decisions:
- Pure functions for color conversion and data transformation
- Immutable configuration handling
- Clear separation of concerns (UI, logic, configuration)
- Comprehensive documentation and type hints

For development guidelines, see [CLAUDE.md](CLAUDE.md).
