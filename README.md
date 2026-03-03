# iTerm2-Tabs

A Python application that displays a popup window with all iTerm2 tabs, allowing you to quickly switch between tabs using mouse clicks or keyboard navigation.

## Features

- **Tab Listing**: Displays all open iTerm2 tabs in a clean popup window
- **Mouse Navigation**: Click on any tab to switch to it
- **Keyboard Navigation**: Use arrow keys (↑/↓) to navigate and Enter to select
- **Fuzzy Search**: Type to filter tabs by name or content
- **Hotkey Support**: Assign a global hotkey to quickly show the tab switcher
- **Session Info**: Shows tab titles, session paths, and window information

## Requirements

- Python 3.9+
- iTerm2 3.4+ with Python API enabled
- macOS (uses Tkinter for GUI)

## Installation

1. **Enable iTerm2 Python API**
   - Open iTerm2
   - Go to `iTerm2 > Install Shell Integration`
   - Go to `iTerm2 > Preferences > General > Magic` and enable "Enable Python API"

2. **Install the project**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/iterm2-Tabs.git
   cd iterm2-Tabs

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -e .
   ```

## Usage

### Command Line

```bash
# Launch the tab switcher popup
python -m iterm2_tabs

# Or if installed as a package
iterm2-tabs
```

### macOS App

```bash
# Build the app
make dist

# Install to Applications
cp -R dist/iterm2-tabs.app /Applications/

# Run from Spotlight
# Press ⌘ + Space, type "iTerm2 Tabs", and press Enter
```

**⚠️ IMPORTANT:** When using the macOS app:
1. **iTerm2 must be running** before launching the app
2. **Python API must be enabled** in iTerm2 Preferences
3. The app will show an error dialog if iTerm2 is not running

### iTerm2 Launcher (Recommended)

Create a custom hotkey in iTerm2:

1. `iTerm2 > Preferences > Keys > Key Bindings`
2. Click `+` to add new keybinding
3. Set your preferred keyboard shortcut (e.g., `⌘ + ⇧ + T`)
4. Action: "Run Command..."
5. Command: `python -m iterm2_tabs` (or full path to python)

This is the recommended way as it ensures iTerm2 is running when the tab switcher launches.

## Configuration

Create a `~/.iterm2-tabs-config.json` file:

```json
{
  "hotkey": "Command+Shift+T",
  "window_width": 600,
  "window_height": 400,
  "show_window_number": true,
  "show_path": true,
  "theme": "dark"
}
```

## Development

```bash
# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/

# Run linter
ruff check src/
```

## How It Works

1. Connects to iTerm2 via the Python API
2. Retrieves all open tabs and sessions
3. Displays a Tkinter popup window with tab information
4. Handles keyboard/mouse events for tab selection
5. Sends focus command back to iTerm2

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
