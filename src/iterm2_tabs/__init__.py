"""iTerm2-Tabs: A popup window for iTerm2 tab switching."""

__version__ = "0.1.0"

from iterm2_tabs.app import TabSwitcher
from iterm2_tabs.config import Config

__all__ = ["TabSwitcher", "Config", "__version__"]
