#!/bin/bash
# Build macOS .app bundle for iTerm2 Tabs using PyInstaller

set -e

# Configuration
APP_NAME="iTerm2 Tabs"
SPEC_FILE="iterm2_tabs.spec"
VERSION=${VERSION:-"0.1.1"}

echo "=========================================="
echo "Building ${APP_NAME} v${VERSION}"
echo "=========================================="

# Clean previous build
echo "Cleaning previous build..."
rm -rf build/ dist/

# Get version from pyproject.toml if not specified
if [ "$VERSION" = "0.1.1" ] && [ -f "pyproject.toml" ]; then
    VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
    echo "Version from pyproject.toml: ${VERSION}"
fi

# Update version in spec file
echo "Updating version in spec file..."
sed -i.bak "s/CFBundleVersion: '.*'/CFBundleVersion: '${VERSION}'/" ${SPEC_FILE}
sed -i.bak "s/CFBundleShortVersionString: '.*'/CFBundleShortVersionString: '${VERSION}'/" ${SPEC_FILE}
rm -f ${SPEC_FILE}.bak

# Build with PyInstaller
echo "Building with PyInstaller..."
# Use uv run to ensure we're using the project's Python environment
uv run pyinstaller --clean ${SPEC_FILE}

# The output should be in dist/iTerm2 Tabs.app
if [ -d "dist/${APP_NAME}.app" ]; then
    echo "✓ Built dist/${APP_NAME}.app"

    # Show app size
    APP_SIZE=$(du -sh "dist/${APP_NAME}.app" | cut -f1)
    echo "  Size: ${APP_SIZE}"

    echo ""
    echo "To test:"
    echo "  open 'dist/${APP_NAME}.app'"
    echo ""
    echo "To install:"
    echo "  cp -R 'dist/${APP_NAME}.app' /Applications/"
    echo ""
    echo "⚠️  IMPORTANT:"
    echo "    1. Make sure iTerm2 is running"
    echo "    2. Enable Python API: iTerm2 > Preferences > General > Magic > Enable Python API"
    echo "    3. Log file: ~/Library/Logs/iterm2-tabs.log"
else
    echo "❌ Build failed!"
    echo "dist contents:"
    ls -la dist/ 2>/dev/null || echo "dist directory not found"
    exit 1
fi
