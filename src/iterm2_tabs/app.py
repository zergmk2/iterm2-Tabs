"""Main application logic."""

from typing import Optional

from iterm2_tabs.config import Config, TabInfo
from iterm2_tabs.gui import TabSwitcherWindow
from iterm2_tabs.iterm2_connection import ITerm2Connection, create_connection


class TabSwitcher:
    """Main application class for the iTerm2 tab switcher."""

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the tab switcher.

        Args:
            config: Application configuration. Defaults to loading from file.
        """
        self.config = config or Config.load()
        self.tabs: list[TabInfo] = []
        self.selected_tab: Optional[TabInfo] = None

    async def collect_tabs(self, connection: ITerm2Connection) -> list[TabInfo]:
        """Collect tab information from iTerm2.

        Args:
            connection: Active iTerm2 connection

        Returns:
            List of TabInfo objects
        """
        tabs_data = await connection.get_all_tabs()
        return [self._create_tab_info(data) for data in tabs_data]

    def run(self, tabs: list[TabInfo]) -> Optional[TabInfo]:
        """Run the GUI with the collected tabs.

        Args:
            tabs: List of tabs to display

        Returns:
            The selected tab, or None if no tab was selected
        """
        if not tabs:
            print("No tabs found in iTerm2.")
            return None

        self.tabs = tabs
        self._run_gui()
        return self.selected_tab

    def _run_gui(self) -> None:
        """Create and run the GUI."""
        window = TabSwitcherWindow(
            tabs=self.tabs,
            config=self.config,
            on_select=self._on_tab_selected,
        )
        window.run()

    def _on_tab_selected(self, tab_id: str) -> None:
        """Handle tab selection - save it for later focusing.

        Args:
            tab_id: ID of the selected tab
        """
        tab = next((t for t in self.tabs if t.tab_id == tab_id), None)
        if tab:
            self.selected_tab = tab

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
    import iterm2

    async def main_loop(connection: iterm2.connection.Connection) -> None:
        iterm2_conn = await create_connection(connection)
        switcher = TabSwitcher()
        tabs = await switcher.collect_tabs(iterm2_conn)

        # Return tabs to be used outside the async context
        return tabs

    # Run the async connection to collect tabs
    tabs = iterm2.run_until_complete(main_loop)

    # Now run the GUI with the collected tabs
    if tabs:
        switcher = TabSwitcher()
        selected_tab = switcher.run(tabs)

        # Focus the selected tab after GUI closes
        if selected_tab:
            iterm2.run_until_complete(
                lambda conn: create_connection(conn).focus_tab(
                    selected_tab.tab_id, selected_tab.window_id
                )
            )


async def focus_tab(tab_id: str, window_id: str) -> None:
    """Focus a specific tab in iTerm2.

    This is a standalone function that can be called from the command line
    to focus a tab without showing the GUI.

    Args:
        tab_id: ID of the tab to focus
        window_id: ID of the window containing the tab
    """
    import iterm2

    async def focus_connection(connection: iterm2.connection.Connection) -> None:
        iterm2_conn = await create_connection(connection)
        await iterm2_conn.focus_tab(tab_id, window_id)

    await iterm2.run_until_complete(focus_connection)


if __name__ == "__main__":
    main()
