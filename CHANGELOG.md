# Changelog

All notable changes to iTerm2 Tabs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-03-05

### Changed
- 🔧 Migrated build system to PyInstaller
- 📉 Reduced app size from 50MB+ to 28MB
- 🚀 Improved build process and dependency management
- 📦 Standardized macOS app bundle structure

## [0.1.1] - 2026-03-05

### Fixed
- 🐛 Fixed Python 3.9 compatibility issue with websockets library
- 📦 Downgraded websockets to 12.x for better system Python support

## [0.1.0] - 2026-03-04

### Added
- Initial release with iTerm2 tab switching functionality
- Modern GUI with dark/light theme support
- Keyboard navigation (↑↓ arrows) and mouse click selection
- Real-time search/filter functionality
- macOS .app bundle for easy installation
- Support for Python 3.12 with uv environment

### Features
- 🎯 Fast tab switching across multiple iTerm2 windows
- ⌨️ Keyboard shortcuts for efficient navigation
- 🔍 Search tabs by title or path
- 🎨 Clean, modern interface
- 🌓 Theme support (dark/light)
- 📦 Standalone macOS app bundle

### Technical
- Built with Python 3.12 and iTerm2 Python API
- Uses uv for fast dependency management
- Tkinter-based GUI with custom styling
