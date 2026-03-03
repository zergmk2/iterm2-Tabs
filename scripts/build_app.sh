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
    <key>NSSupportsAutomaticTermination</key>
    <false/>
    <key>NSSupportsSuddenTermination</key>
    <false/>
</dict>
</plist>
EOF

# Create the launcher script
cat > "${MACOS_DIR}/iterm2-tabs" << 'EOF'
#!/bin/bash
# iTerm2 Tabs Launcher

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENTS_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Set up Python path
export PYTHONPATH="${RESOURCES_DIR}/site-packages:${PYTHONPATH}"

# Run the application
exec python3 -m iterm2_tabs
EOF

# Make the launcher executable
chmod +x "${MACOS_DIR}/iterm2-tabs"

# Copy source code and dependencies to Resources
mkdir -p "${RESOURCES_DIR}/site-packages"

# Copy the source package
rsync -av --exclude='__pycache__' --exclude='*.pyc' \
    src/iterm2_tabs/ "${RESOURCES_DIR}/site-packages/iterm2_tabs/"

# Install dependencies to Resources
pip3 install --target="${RESOURCES_DIR}/site-packages" --no-cache iterm2

# Create PTH file to ensure the package is importable
echo "import site; site.addsitedir('${RESOURCES_DIR}/site-packages')" > "${RESOURCES_DIR}/site-packages/iterm2_tabs.pth"

echo "Built ${APP_DIR}"
echo "You can now run: open ${APP_DIR}"
