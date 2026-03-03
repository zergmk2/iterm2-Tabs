"""Tests for configuration management."""


from iterm2_tabs.config import Config, TabInfo


class TestConfig:
    """Test Config class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.window_width == 600
        assert config.window_height == 400
        assert config.show_window_number is True
        assert config.show_path is True
        assert config.theme == "dark"
        assert config.font_size == 12

    def test_config_with_custom_values(self):
        """Test configuration with custom values."""
        config = Config(
            window_width=800,
            window_height=600,
            theme="light",
            font_size=14,
        )
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.theme == "light"
        assert config.font_size == 14

    def test_load_from_nonexistent_file(self, tmp_path):
        """Test loading config from nonexistent file returns defaults."""
        config = Config.load(tmp_path / "nonexistent.json")
        assert isinstance(config, Config)
        assert config.window_width == 600

    def test_load_and_save_config(self, tmp_path, sample_config):
        """Test saving and loading configuration."""
        config_file = tmp_path / "test-config.json"
        sample_config.save(config_file)

        loaded_config = Config.load(config_file)
        assert loaded_config.window_width == sample_config.window_width
        assert loaded_config.window_height == sample_config.window_height
        assert loaded_config.theme == sample_config.theme

    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON returns defaults."""
        invalid_file = tmp_path / "invalid.json"
        with invalid_file.open("w") as f:
            f.write("{ invalid json }")

        config = Config.load(invalid_file)
        assert isinstance(config, Config)
        assert config.window_width == 600

    def test_load_partial_config(self, tmp_path):
        """Test loading config with partial values."""
        partial_file = tmp_path / "partial.json"
        with partial_file.open("w") as f:
            f.write('{"window_width": 1000}')

        config = Config.load(partial_file)
        assert config.window_width == 1000
        assert config.window_height == 400  # Default


class TestTabInfo:
    """Test TabInfo class."""

    def test_tab_info_creation(self):
        """Test creating a TabInfo object."""
        tab = TabInfo(
            tab_id="test-tab",
            window_id="test-window",
            title="Test Session",
            path="/home/user",
            session_id="test-session",
            window_number=1,
        )
        assert tab.tab_id == "test-tab"
        assert tab.window_id == "test-window"
        assert tab.title == "Test Session"
        assert tab.path == "/home/user"
        assert tab.session_id == "test-session"
        assert tab.window_number == 1

    def test_tab_info_str_with_path(self):
        """Test string representation with path."""
        tab = TabInfo(
            tab_id="tab1",
            window_id="win1",
            title="Session",
            path="/home/user",
            window_number=1,
        )
        result = str(tab)
        assert "[1]" in result
        assert "Session" in result
        assert "(/home/user)" in result

    def test_tab_info_str_without_path(self):
        """Test string representation without path."""
        tab = TabInfo(
            tab_id="tab1",
            window_id="win1",
            title="Remote",
            window_number=2,
        )
        result = str(tab)
        assert "[2]" in result
        assert "Remote" in result
        assert "(" not in result

    def test_tab_info_str_without_window_number(self):
        """Test string representation without window number."""
        tab = TabInfo(
            tab_id="tab1",
            window_id="win1",
            title="Session",
            path="/tmp",
        )
        result = str(tab)
        assert "[" not in result
        assert "Session" in result
