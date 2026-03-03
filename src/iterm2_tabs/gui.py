"""GUI implementation using Tkinter."""

import tkinter as tk
from tkinter import ttk
from typing import Any

from iterm2_tabs.config import Config, TabInfo


class TabSwitcherWindow:
    """Main window for the tab switcher."""

    def __init__(self, tabs: list[TabInfo], config: Config, on_select: Any) -> None:
        """Initialize the tab switcher window.

        Args:
            tabs: List of tab information to display
            config: Application configuration
            on_select: Callback function when a tab is selected
        """
        self.tabs = tabs
        self.config = config
        self.on_select = on_select
        self.selected_index = 0
        self.filter_text = ""

        self._setup_window()
        self._setup_widgets()
        self._bind_events()
        self._update_list()

    def _setup_window(self) -> None:
        """Set up the main window properties."""
        self.root = tk.Tk()
        self.root.title("iTerm2 Tab Switcher")

        width = self.config.window_width
        height = self.config.window_height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.grab_set()  # Make window modal

        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply the configured theme to the window."""
        if self.config.theme == "dark":
            bg = "#1e1e1e"
            fg = "#ffffff"
            select_bg = "#0078d4"
            select_fg = "#ffffff"
        else:
            bg = "#ffffff"
            fg = "#000000"
            select_bg = "#0078d4"
            select_fg = "#ffffff"

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("", self.config.font_size))
        style.configure("TEntry", fieldbackground=bg, foreground=fg)
        style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg)
        style.configure(
            "Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            font=("", self.config.font_size),
        )
        style.map(
            "Treeview", background=[("selected", select_bg)], foreground=[("selected", select_fg)]
        )

        self.root.configure(bg=bg)

    def _setup_widgets(self) -> None:
        """Set up all widgets in the window."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Search/filter entry
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, expand=True)

        # Tab list
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("title", "path") if self.config.show_path else ("title",)
        self.tab_list = ttk.Treeview(
            list_frame, columns=columns, show="tree headings", selectmode="browse"
        )

        self.tab_list.heading("#0", text="Tab")
        if self.config.show_path:
            self.tab_list.heading("path", text="Path")

        self.tab_list.column("#0", width=200)
        if self.config.show_path:
            self.tab_list.column("path", width=300)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tab_list.yview)
        self.tab_list.configure(yscrollcommand=scrollbar.set)

        self.tab_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Instructions label
        instructions = "↑↓ Navigate | Enter Select | Esc Close | Type to filter"
        ttk.Label(main_frame, text=instructions).pack(pady=(10, 0))

    def _bind_events(self) -> None:
        """Bind keyboard and mouse events."""
        self.root.bind("<Escape>", lambda e: self.close())
        self.root.bind("<Up>", lambda e: self._navigate(-1))
        self.root.bind("<Down>", lambda e: self._navigate(1))
        self.root.bind("<Return>", lambda e: self._select_current())
        self.root.bind("<Key>", self._on_key_press)

        self.tab_list.bind("<Button-1>", self._on_click)
        self.tab_list.bind("<Double-Button-1>", lambda e: self._select_current())

        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        self.search_entry.focus_set()

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle key press events."""
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        # Redirect other input to search box
        if event.char:
            self.search_entry.focus_set()

    def _on_search_change(self, event: tk.Event) -> None:
        """Handle search text changes."""
        self.filter_text = self.search_entry.get().lower()
        self._update_list()

    def _on_click(self, event: tk.Event) -> None:
        """Handle mouse click on tab list."""
        item = self.tab_list.identify("item", event.x, event.y)
        if item:
            self.selected_index = int(self.tab_list.index(item))
            self.tab_list.selection_set(item)

    def _navigate(self, direction: int) -> None:
        """Navigate up/down in the list."""
        items = self.tab_list.get_children()
        if not items:
            return

        new_index = self.selected_index + direction
        new_index = max(0, min(new_index, len(items) - 1))

        if 0 <= new_index < len(items):
            self.selected_index = new_index
            self.tab_list.selection_set(items[new_index])
            self.tab_list.see(items[new_index])

    def _select_current(self, event: tk.Event | None = None) -> None:
        """Select the currently highlighted tab."""
        items = self.tab_list.get_children()
        if items and 0 <= self.selected_index < len(items):
            item = items[self.selected_index]
            tab_id = self.tab_list.item(item, "tags")[0]
            self.on_select(tab_id)
            self.close()

    def _update_list(self) -> None:
        """Update the tab list based on current filter."""
        self.tab_list.delete(*self.tab_list.get_children())

        filtered_tabs = [
            tab
            for tab in self.tabs
            if not self.filter_text
            or self.filter_text in tab.title.lower()
            or (tab.path and self.filter_text in tab.path.lower())
        ]

        for tab in filtered_tabs:
            values = (tab.path,) if self.config.show_path else ()
            self.tab_list.insert("", "end", text=str(tab), values=values, tags=(tab.tab_id,))

        # Select first item if available
        items = self.tab_list.get_children()
        if items:
            self.selected_index = 0
            self.tab_list.selection_set(items[0])

    def run(self) -> None:
        """Run the main window loop."""
        self.root.mainloop()

    def close(self) -> None:
        """Close the window."""
        self.root.destroy()
