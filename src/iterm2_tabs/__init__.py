"""iTerm2-Tabs: A popup window for iTerm2 tab switching."""

__version__ = "0.1.0"

from iterm2_tabs.app import TabSwitcher, focus_tab
from iterm2_tabs.config import Config

__all__ = ["TabSwitcher", "Config", "focus_tab", "__version__"]
