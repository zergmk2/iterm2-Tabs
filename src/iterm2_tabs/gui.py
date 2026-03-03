"""GUI implementation using Tkinter."""

import contextlib
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional

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
        self.root.title("Tabs")

        width = self.config.window_width
        height = self.config.window_height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.minsize(400, 300)

        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply the configured theme to the window."""
        if self.config.theme == "dark":
            # Modern dark theme with better colors
            bg = "#2b2b2b"
            fg = "#e0e0e0"
            select_bg = "#007acc"
            select_fg = "#ffffff"
            focus_color = "#005a9e"
        else:
            # Modern light theme
            bg = "#f5f5f5"
            fg = "#333333"
            select_bg = "#007acc"
            select_fg = "#ffffff"
            focus_color = "#005a9e"

        style = ttk.Style()
        style.theme_use("clam")

        # Configure frame with background color
        style.configure("TFrame", background=bg, borderwidth=0)

        # Configure labels with modern font
        style.configure(
            "TLabel",
            background=bg,
            foreground=fg,
            font=("SF Pro Display", self.config.font_size)
            if self.config.theme == "dark"
            else ("SF Pro Text", self.config.font_size),
        )

        # Configure entry with modern styling
        style.configure(
            "TEntry",
            fieldbackground="#3c3c3c" if self.config.theme == "dark" else "#ffffff",
            foreground=fg,
            borderwidth=1,
            relief="solid",
            padding=(8, 8),
        )
        style.map("TEntry", bordercolor=[("focus", focus_color)])

        # Configure Treeview with modern styling
        style.configure(
            "Treeview",
            background="#3c3c3c" if self.config.theme == "dark" else "#ffffff",
            foreground=fg,
            fieldbackground="#3c3c3c" if self.config.theme == "dark" else "#ffffff",
            borderwidth=0,
            font=("SF Pro Display", self.config.font_size)
            if self.config.theme == "dark"
            else ("SF Pro Text", self.config.font_size),
            rowheight=28,
        )

        # Configure selection colors
        style.map(
            "Treeview",
            background=[("selected", select_bg)],
            foreground=[("selected", select_fg)],
        )

        # Configure scrollbar
        style.configure(
            "Vertical.TScrollbar",
            background=bg,
            troughcolor=bg,
            bordercolor=bg,
            arrowcolor=fg,
            darkcolor=select_bg,
            lightcolor=select_bg,
        )

        self.root.configure(bg=bg)

    def _setup_widgets(self) -> None:
        """Set up all widgets in the window."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title/header
        title_label = ttk.Label(
            main_frame,
            text="iTerm2 Tabs",
            font=("SF Pro Display", 16, "bold")
            if self.config.theme == "dark"
            else ("SF Pro Text", 16, "bold"),
        )
        title_label.pack(pady=(0, 12))

        # Search/filter entry with better styling
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 12))

        search_label = ttk.Label(search_frame, text="🔍", font=("", 14))
        search_label.pack(side=tk.LEFT, padx=(0, 8))

        self.search_entry = ttk.Entry(
            search_frame,
            font=("SF Pro Display", 13) if self.config.theme == "dark" else ("SF Pro Text", 13),
        )
        self.search_entry.pack(fill=tk.X, expand=True)

        # Tab list with better spacing
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.tab_list = ttk.Treeview(list_frame, show="tree", selectmode="browse")
        self.tab_list.column("#0", width=600)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar", command=self.tab_list.yview
        )
        self.tab_list.configure(yscrollcommand=scrollbar.set)

        self.tab_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Instructions label with better styling
        instructions = "↑↓ Navigate | Enter: Select | Esc: Close | Type: Filter"
        instructions_label = ttk.Label(
            main_frame,
            text=instructions,
            font=("SF Pro Display", 10) if self.config.theme == "dark" else ("SF Pro Text", 10),
            foreground="#888888" if self.config.theme == "dark" else "#666666",
        )
        instructions_label.pack(pady=(12, 0))

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

    def _select_current(self, event: Optional[tk.Event] = None) -> None:
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
            self.tab_list.insert("", "end", text=str(tab), tags=(tab.tab_id,))

        # Select first item if available
        items = self.tab_list.get_children()
        if items:
            self.selected_index = 0
            self.tab_list.selection_set(items[0])

    def run(self) -> None:
        """Run the main window loop."""
        # Ensure window is visible and on top
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)  # Bring to front
        self.root.focus_force()
        self.root.update_idletasks()
        self.root.after(
            100, lambda: self.root.attributes("-topmost", False)
        )  # Remove topmost after 100ms

        # Process any pending events
        self.root.update_idletasks()

        # Make window modal if window still exists
        if self.root.winfo_exists():
            with contextlib.suppress(Exception):
                self.root.grab_set()

        # Activate the application (macOS specific)
        with contextlib.suppress(Exception):
            self.root.tk.call("::tk::mac::BringToFront", self.root._w)

        self.root.mainloop()

    def close(self) -> None:
        """Close the window."""
        self.root.destroy()
