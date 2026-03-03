"""iTerm2 connection and tab retrieval."""

from typing import Any

import iterm2


class ITerm2Connection:
    """Manage connection to iTerm2 and retrieve tab information."""

    def __init__(self, connection: iterm2.connection.Connection) -> None:
        """Initialize with an iTerm2 connection.

        Args:
            connection: Active iTerm2 connection
        """
        self.connection = connection

    async def get_all_tabs(self) -> list[dict[str, Any]]:
        """Retrieve all tabs from iTerm2.

        Returns:
            List of tab information dictionaries
        """
        app = await iterm2.async_get_app(self.connection)
        tabs_info = []

        async with iterm2.VariableMonitor(self.connection, [iterm2.VariableScopes.APP], []) as mon:
            for window in app.windows:
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
                                "window_number": window.number,
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
        app = await iterm2.async_get_app(self.connection)

        for window in app.windows:
            if str(window.window_id) == window_id:
                await window.async_activate()
                for tab in window.tabs:
                    if str(tab.tab_id) == tab_id:
                        await tab.async_activate()
                        return


async def connect_to_iterm2() -> ITerm2Connection:
    """Establish connection to iTerm2.

    Returns:
        ITerm2Connection instance

    Raises:
        RuntimeError: If connection fails
    """
    try:
        connection = await iterm2.Connection().async_connect()
        if connection is None:
            raise RuntimeError("Failed to connect to iTerm2. Make sure Python API is enabled.")
        return ITerm2Connection(connection)
    except Exception as e:
        raise RuntimeError(f"Failed to connect to iTerm2: {e}") from e
