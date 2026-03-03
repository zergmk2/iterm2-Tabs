"""Tests for the main application."""

from iterm2_tabs.app import TabSwitcher
from iterm2_tabs.config import Config


class TestTabSwitcher:
    """Test TabSwitcher class."""

    def test_initialization(self, sample_config):
        """Test TabSwitcher initialization."""
        switcher = TabSwitcher(config=sample_config)
        assert switcher.config == sample_config
        assert switcher.connection is None
        assert switcher.tabs == []

    def test_initialization_without_config(self):
        """Test TabSwitcher initialization with default config."""
        switcher = TabSwitcher()
        assert isinstance(switcher.config, type(Config()))
        assert switcher.config.window_width == 600

    def test_create_tab_info(self):
        """Test TabInfo creation from raw data."""
        switcher = TabSwitcher()
        data = {
            "tab_id": "test-tab",
            "window_id": "test-window",
            "title": "Test",
            "path": "/test/path",
            "session_id": "test-session",
            "window_number": 1,
        }
        tab = switcher._create_tab_info(data)
        assert tab.tab_id == "test-tab"
        assert tab.window_id == "test-window"
        assert tab.title == "Test"
        assert tab.path == "/test/path"
        assert tab.session_id == "test-session"
        assert tab.window_number == 1

    def test_create_tab_info_with_missing_optional_fields(self):
        """Test TabInfo creation with missing optional fields."""
        switcher = TabSwitcher()
        data = {
            "tab_id": "test-tab",
            "window_id": "test-window",
            "title": "Test",
        }
        tab = switcher._create_tab_info(data)
        assert tab.tab_id == "test-tab"
        assert tab.path is None
        assert tab.session_id is None
        assert tab.window_number == 0
