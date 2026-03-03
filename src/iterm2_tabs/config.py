"""Configuration management for iTerm2-Tabs."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Configuration for the tab switcher application."""

    window_width: int = 600
    window_height: int = 400
    show_window_number: bool = True
    show_path: bool = True
    theme: str = "dark"
    font_size: int = 12
    hotkey: str | None = None

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        """Load configuration from file.

        Args:
            path: Path to config file. Defaults to ~/.iterm2-tabs-config.json

        Returns:
            Config instance with loaded values or defaults
        """
        if path is None:
            path = Path.home() / ".iterm2-tabs-config.json"

        if not path.exists():
            return cls()

        try:
            with path.open() as f:
                data = json.load(f)
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        except (json.JSONDecodeError, TypeError):
            return cls()

    def save(self, path: Path | None = None) -> None:
        """Save configuration to file.

        Args:
            path: Path to config file. Defaults to ~/.iterm2-tabs-config.json
        """
        if path is None:
            path = Path.home() / ".iterm2-tabs-config.json"

        data = {k: getattr(self, k) for k in self.__dataclass_fields__}
        with path.open("w") as f:
            json.dump(data, f, indent=2)


@dataclass
class TabInfo:
    """Information about an iTerm2 tab."""

    tab_id: str
    window_id: str
    title: str
    path: str | None = None
    session_id: str | None = None
    window_number: int = 0

    def __str__(self) -> str:
        """Return string representation for display."""
        parts = []
        if self.window_number > 0:
            parts.append(f"[{self.window_number}]")
        parts.append(self.title)
        if self.path:
            parts.append(f"({self.path})")
        return " ".join(parts)
