"""Main application logic."""

import asyncio
import sys

from iterm2_tabs.config import Config, TabInfo
from iterm2_tabs.gui import TabSwitcherWindow
from iterm2_tabs.iterm2_connection import ITerm2Connection, connect_to_iterm2


class TabSwitcher:
    """Main application class for the iTerm2 tab switcher."""

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the tab switcher.

        Args:
            config: Application configuration. Defaults to loading from file.
        """
        self.config = config or Config.load()
        self.connection: ITerm2Connection | None = None
        self.tabs: list[TabInfo] = []

    async def run(self) -> None:
        """Run the tab switcher application."""
        try:
            # Connect to iTerm2
            self.connection = await connect_to_iterm2()

            # Retrieve all tabs
            tabs_data = await self.connection.get_all_tabs()
            self.tabs = [self._create_tab_info(data) for data in tabs_data]

            if not self.tabs:
                print("No tabs found in iTerm2.")
                return

            # Create and run GUI
            self._run_gui()

        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def _run_gui(self) -> None:
        """Create and run the GUI in the main thread."""
        window = TabSwitcherWindow(
            tabs=self.tabs,
            config=self.config,
            on_select=self._on_tab_selected,
        )
        window.run()

    def _on_tab_selected(self, tab_id: str) -> None:
        """Handle tab selection.

        Args:
            tab_id: ID of the selected tab
        """
        if self.connection and self.tabs:
            tab = next((t for t in self.tabs if t.tab_id == tab_id), None)
            if tab:
                # Schedule the focus operation on the iTerm2 connection's event loop
                asyncio.create_task(self.connection.focus_tab(tab.tab_id, tab.window_id))

    @staticmethod
    def _create_tab_info(data: dict) -> TabInfo:
        """Create a TabInfo object from raw data.

        Args:
            data: Raw tab data dictionary

        Returns:
            TabInfo instance
        """
        return TabInfo(
            tab_id=data["tab_id"],
            window_id=data["window_id"],
            title=data["title"],
            path=data.get("path"),
            session_id=data.get("session_id"),
            window_number=data.get("window_number", 0),
        )


def main() -> None:
    """Entry point for the application."""
    switcher = TabSwitcher()
    asyncio.run(switcher.run())


if __name__ == "__main__":
    main()
