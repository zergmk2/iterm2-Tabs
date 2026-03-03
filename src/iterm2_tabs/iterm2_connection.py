"""iTerm2 connection and tab retrieval."""

from typing import Any

import iterm2


class ITerm2Connection:
    """Manage connection to iTerm2 and retrieve tab information."""

    def __init__(self, connection: iterm2.connection.Connection, app: iterm2.App) -> None:
        """Initialize with an iTerm2 connection and app.

        Args:
            connection: Active iTerm2 connection
            app: iTerm2 app instance
        """
        self.connection = connection
        self.app = app

    async def get_all_tabs(self) -> list[dict[str, Any]]:
        """Retrieve all tabs from iTerm2.

        Returns:
            List of tab information dictionaries
        """
        tabs_info = []

        for window_idx, window in enumerate(self.app.windows, start=1):
            for tab in window.tabs:
                for session in tab.sessions:
                    title = await session.async_get_variable("name")
                    path = await self._get_session_path(session)

                    tabs_info.append(
                        {
                            "tab_id": str(tab.tab_id),
                            "window_id": str(window.window_id),
                            "session_id": str(session.session_id),
                            "title": title,
                            "path": path,
                            "window_number": window_idx,
                        }
                    )

        return tabs_info

    async def _get_session_path(self, session: iterm2.Session) -> str | None:
        """Get the current working directory of a session.

        Args:
            session: iTerm2 session

        Returns:
            Current working directory or None
        """
        try:
            path = await session.async_get_variable("path")
            return str(path) if path else None
        except Exception:
            return None

    async def focus_tab(self, tab_id: str, window_id: str) -> None:
        """Focus a specific tab in iTerm2.

        Args:
            tab_id: ID of the tab to focus
            window_id: ID of the window containing the tab
        """
        for window in self.app.windows:
            if str(window.window_id) == window_id:
                await window.async_activate()
                for tab in window.tabs:
                    if str(tab.tab_id) == tab_id:
                        await tab.async_activate()
                        return


async def create_connection(connection: iterm2.connection.Connection) -> ITerm2Connection:
    """Create an ITerm2Connection from a raw iTerm2 connection.

    Args:
        connection: Raw iTerm2 connection

    Returns:
        ITerm2Connection instance
    """
    app = await iterm2.async_get_app(connection)
    return ITerm2Connection(connection, app)
