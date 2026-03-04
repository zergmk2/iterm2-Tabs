#!/bin/bash
# Bump version number in the project

set -e

VERSION="${1}"

# Validate version format
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version format. Use format: 0.1.0"
    exit 1
fi

echo "Updating version to ${VERSION}..."

# Update version in src/iterm2_tabs/__init__.py
sed -i '' "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/" src/iterm2_tabs/__init__.py

# Update version in scripts/build_app.sh
sed -i '' "s/APP_VERSION=\".*\"/APP_VERSION=\"${VERSION}\"/" scripts/build_app.sh

echo "Version updated to ${VERSION}"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Commit changes: git commit -am \"Bump version to ${VERSION}\""
echo "3. Create release: ./scripts/release.sh v${VERSION}"
