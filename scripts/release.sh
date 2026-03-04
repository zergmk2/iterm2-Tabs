#!/bin/bash
# Create a new GitHub release

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) not installed${NC}"
    echo "Please install from: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

# Get version from argument or prompt
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: ./scripts/release.sh <version>${NC}"
    echo "Example: ./scripts/release.sh v0.1.0"
    read -p "Enter version (e.g., v0.1.0): " VERSION
    if [ -z "$VERSION" ]; then
        echo -e "${RED}Error: Version is required${NC}"
        exit 1
    fi
else
    VERSION="$1"
fi

# Validate version format
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid version format. Use format: v0.1.0${NC}"
    exit 1
fi

echo -e "${GREEN}Creating release for ${VERSION}...${NC}"

# Clean previous build
echo "Cleaning previous build..."
rm -rf dist

# Build the app
echo "Building app..."
make dist

# Create release archive
echo "Creating release archive..."
cd dist
zip -qr "iTerm2 Tabs.app.zip" "iTerm2 Tabs.app"
ARCHIVE_SIZE=$(du -h "iTerm2 Tabs.app.zip" | cut -f1)
echo "Archive size: $ARCHIVE_SIZE"

# Generate checksums
echo "Generating checksums..."
shasum -a 256 "iTerm2 Tabs.app.zip" > checksums.txt
shasum -a 512 "iTerm2 Tabs.app.zip" >> checksums.txt
cd ..

# Create release notes
NOTES_FILE="dist/release_notes.md"
cat > "$NOTES_FILE" << EOF
## iTerm2 Tabs ${VERSION}

### 下载方式
- **macOS App**: 下载 \`iTerm2 Tabs.app.zip\` 并解压到 \`/Applications/\` 目录

### 使用要求
1. macOS 10.15+
2. iTerm2 正在运行
3. 已启用 iTerm2 Python API: \`iTerm2 > Preferences > General > Magic > Enable Python API\`

### 安装步骤
\`\`\`bash
# 1. 下载并解压
unzip "iTerm2 Tabs.app.zip"
# 2. 移动到 Applications 目录
cp -R "iTerm2 Tabs.app" /Applications/
# 3. 首次运行需要授权
open "/Applications/iTerm2 Tabs.app"
\`\`\`

### 校验和
请使用以下命令校验下载文件的完整性：
\`\`\`bash
shasum -a 256 -c checksums.txt
shasum -a 512 -c checksums.txt
\`\`\`

### 功能特性
- 🎯 快速切换 iTerm2 tabs
- ⌨️ 键盘快捷键导航（↑↓）
- 🔍 实时搜索过滤
- 🎨 现代化 GUI 界面
- 🌓 支持深色/浅色主题

### 更新日志
查看 [CHANGELOG.md](https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/blob/main/CHANGELOG.md) 了解详细更新内容。
EOF

# Ask for confirmation
echo -e "${YELLOW}About to create release ${VERSION}${NC}"
echo "Files to upload:"
echo "  - dist/iTerm2 Tabs.app.zip"
echo "  - dist/checksums.txt"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Release cancelled${NC}"
    exit 0
fi

# Create git tag if it doesn't exist
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo -e "${YELLOW}Tag ${VERSION} already exists${NC}"
else
    echo "Creating git tag ${VERSION}..."
    git tag -a "$VERSION" -m "Release ${VERSION}"
    echo -e "${GREEN}Tag created. Run 'git push origin ${VERSION}' to push the tag${NC}"
fi

# Create GitHub release
echo "Creating GitHub release..."
gh release create "$VERSION" \
    --title "iTerm2 Tabs ${VERSION}" \
    --notes-file "$NOTES_FILE" \
    "dist/iTerm2 Tabs.app.zip" \
    dist/checksums.txt

echo -e "${GREEN}Release ${VERSION} created successfully!${NC}"
echo "View at: $(git remote get-url origin | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')/releases/tag/${VERSION}"
