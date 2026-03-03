#!/bin/bash
# Build macOS .app bundle for iTerm2 Tabs

set -e

# Configuration
APP_NAME="iterm2-tabs"
APP_VERSION="0.1.0"
APP_DIR="dist/${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Use system Python for the app (works on all macOS systems)
SYSTEM_PYTHON="/usr/bin/python3"

# Check if system Python exists
if [ ! -f "$SYSTEM_PYTHON" ]; then
    echo "Error: System Python not found at $SYSTEM_PYTHON"
    echo "Please install Python 3 from python.org or Homebrew"
    exit 1
fi

# Clean previous build
rm -rf "${APP_DIR}"

# Create .app structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>iterm2-tabs</string>
    <key>CFBundleIdentifier</key>
    <string>com.iterm2-tabs.app</string>
    <key>CFBundleName</key>
    <string>iTerm2 Tabs</string>
    <key>CFBundleVersion</key>
    <string>${APP_VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>${APP_VERSION}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
    <key>LSBackgroundOnly</key>
    <false/>
    <key>LSForegroundOnly</key>
    <true/>
    <key>NSSupportsAutomaticTermination</key>
    <false/>
    <key>NSSupportsSuddenTermination</key>
    <false/>
</dict>
</plist>
EOF

# Create the launcher script with error logging
cat > "${MACOS_DIR}/iterm2-tabs" << 'LAUNCHER_EOF'
#!/bin/bash
# iTerm2 Tabs Launcher

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENTS_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Log file for debugging
LOG_FILE="${HOME}/Library/Logs/iterm2-tabs.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Set up Python path
export PYTHONPATH="${RESOURCES_DIR}/site-packages:${PYTHONPATH}"

# Activate this application to bring it to front
osascript -e 'tell application "System Events" to set frontmost of first process whose unix id is '"$$"'' 2>/dev/null || true

# Run the application with error logging
echo "========================================" >> "$LOG_FILE"
echo "Starting iTerm2 Tabs at $(date)" >> "$LOG_FILE"
echo "Resources dir: ${RESOURCES_DIR}" >> "$LOG_FILE"
echo "System Python: /usr/bin/python3" >> "$LOG_FILE"
echo "Process ID: $$" >> "$LOG_FILE"

# Check if iTerm2 is running
if ! ps aux | grep -q "[i]Term2"; then
    echo "ERROR: iTerm2 is not running!" >> "$LOG_FILE"
    osascript -e 'display dialog "iTerm2 is not running!\n\nPlease start iTerm2 first and make sure the Python API is enabled:\n\niTerm2 > Preferences > General > Magic > Enable Python API" buttons {"OK"} default button 1 with title "iTerm2 Tabs" with icon caution' 2>/dev/null
    exit 1
fi

# Run and log any errors
echo "About to start Python app..." >> "$LOG_FILE"
/usr/bin/python3 -u -m iterm2_tabs 2>&1 | while IFS= read -r line; do
    echo "$line" >> "$LOG_FILE"
    echo "$line"  # Also output to console for debugging
done
EXIT_CODE=${PIPESTATUS[0]}

echo "App exited with code: $EXIT_CODE" >> "$LOG_FILE"

if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: iTerm2 Tabs failed with exit code $EXIT_CODE" >> "$LOG_FILE"
    osascript -e 'display dialog "iTerm2 Tabs failed to start.\n\nCheck the log file for details:\n~/Library/Logs/iterm2-tabs.log\n\nCommon issues:\n• iTerm2 not running\n• Python API not enabled\n• No tabs open\n\nLast 10 lines from log:"' 2>/dev/null &
    sleep 1
    osascript -e "display dialog \"$(tail -10 \"$LOG_FILE\")\"" 2>/dev/null || true
    exit 1
fi
LAUNCHER_EOF

# Make the launcher executable
chmod +x "${MACOS_DIR}/iterm2-tabs"

# Copy source code and dependencies to Resources
mkdir -p "${RESOURCES_DIR}/site-packages"

# Copy the source package
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    src/iterm2_tabs/ "${RESOURCES_DIR}/site-packages/iterm2_tabs/"

# Install dependencies to Resources using system Python
$SYSTEM_PYTHON -m pip install --target="${RESOURCES_DIR}/site-packages" --no-cache --upgrade iterm2 2>&1 | grep -v "already satisfied" || true

# Create __init__.py for site-packages
touch "${RESOURCES_DIR}/site-packages/__init__.py"

echo "Built ${APP_DIR}"
echo ""
echo "To test:"
echo "  ${APP_DIR}/Contents/MacOS/iterm2-tabs"
echo ""
echo "To install:"
echo "  cp -R ${APP_DIR} /Applications/"
echo ""
echo "⚠️  IMPORTANT:"
echo "    1. Make sure iTerm2 is running"
echo "    2. Enable Python API: iTerm2 > Preferences > General > Magic > Enable Python API"
echo "    3. Log file: ~/Library/Logs/iterm2-tabs.log"
EOF
