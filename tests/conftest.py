"""Pytest configuration and fixtures."""

import pytest

from iterm2_tabs.config import Config, TabInfo


@pytest.fixture
def sample_config():
    """Return a sample configuration."""
    return Config(
        window_width=800,
        window_height=500,
        show_window_number=True,
        show_path=True,
        theme="dark",
    )


@pytest.fixture
def sample_tabs():
    """Return sample tab data."""
    return [
        TabInfo(
            tab_id="tab1",
            window_id="win1",
            title="Session 1",
            path="/home/user/project1",
            session_id="sess1",
            window_number=1,
        ),
        TabInfo(
            tab_id="tab2",
            window_id="win1",
            title="Session 2",
            path="/home/user/project2",
            session_id="sess2",
            window_number=1,
        ),
        TabInfo(
            tab_id="tab3",
            window_id="win2",
            title="Server Connection",
            path=None,
            session_id="sess3",
            window_number=2,
        ),
    ]


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    import json

    config_data = {
        "window_width": 700,
        "window_height": 450,
        "theme": "light",
    }
    config_file = tmp_path / "config.json"
    with config_file.open("w") as f:
        json.dump(config_data, f)
    return config_file
