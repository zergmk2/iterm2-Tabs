# Release Guide

This guide explains how to create releases for iTerm2 Tabs.

## Prerequisites

1. **GitHub CLI** installed and authenticated:
   ```bash
   brew install gh
   gh auth login
   ```

2. **uv** installed for Python environment management:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Release Process

### Option 1: Using Make (Recommended)

```bash
# 1. Bump version
make bump-version VERSION=0.2.0

# 2. Review changes
git diff

# 3. Commit version bump
git commit -am "Bump version to 0.2.0"

# 4. Create release
make release VERSION=0.2.0
```

### Option 2: Using Scripts Directly

```bash
# 1. Bump version
./scripts/bump-version.sh 0.2.0

# 2. Review and commit
git diff
git commit -am "Bump version to 0.2.0"

# 3. Create release
./scripts/release.sh v0.2.0
```

### Option 3: Automated via GitHub Actions

```bash
# 1. Bump version
make bump-version VERSION=0.2.0

# 2. Commit and push
git commit -am "Bump version to 0.2.0"
git push

# 3. Create and push tag
git tag v0.2.0
git push origin v0.2.0
```

GitHub Actions will automatically build and create the release.

## What the Release Script Does

1. **Builds the macOS app**:
   - Uses uv Python 3.12 environment
   - Runs `make dist`
   - Creates `iterm2-tabs.app.zip`

2. **Generates checksums**:
   - SHA-256 checksum
   - SHA-512 checksum

3. **Creates git tag** (if not exists)

4. **Creates GitHub release** with:
   - Release notes with installation instructions
   - App bundle (`iterm2-tabs.app.zip`)
   - Checksums file (`checksums.txt`)

## Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

Examples:
- `0.1.0` - Initial release
- `0.1.1` - Bug fix
- `0.2.0` - New features
- `1.0.0` - Stable release

## Post-Release

After creating a release:

1. **Update CHANGELOG.md** with detailed release notes

2. **Announce the release** (if applicable)

3. **Monitor issues** for the new release

## Testing Before Release

Before creating a release, test the built app:

```bash
# Build the app
make dist

# Test locally
open dist/iterm2-tabs.app

# Verify all features work:
# - Tab listing
# - Keyboard navigation
# - Search/filter
# - Tab selection
# - Theme switching
```

## Troubleshooting

### GitHub CLI not authenticated
```bash
gh auth login
```

### Tag already exists
```bash
# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0
```

### Release already exists
```bash
# Delete release via GitHub CLI
gh release delete v0.1.0

# Or delete via GitHub web interface
```

## Files Updated by Bump Version

- `src/iterm2_tabs/__init__.py` - `__version__`
- `scripts/build_app.sh` - `APP_VERSION`

Make sure to commit these changes before creating the release.
