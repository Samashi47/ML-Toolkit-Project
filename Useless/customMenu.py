import customtkinter as ctk
import tkinter as tk
from typing import Literal


class Menu:
    """
    Custom Menu Class.
    When initializing the menu, make sure there's upper window space for the menu bar,
    menu is packed like so: `pack(side="top", fill="x")`
    """

    def __init__(self, root: ctk.CTk) -> None:
        self._root = root
        self._menu_bar = ctk.CTkFrame(self._root, cursor="hand2")
        self._menu_bar.pack(side="top", fill="x")
        self._menu_widgets: list[tk.Menubutton] = []
        ctk.AppearanceModeTracker.add(self.set_appearance_mode)

    def menu_bar(self, text: str, **kwargs) -> tk.Menu:
        menu = tk.Menubutton(self._menu_bar, text=text,font=('Arial',13))
        menu.menu = tk.Menu(menu, **kwargs,font=('Arial',13))
        menu["menu"] = menu.menu
        menu.pack(side="left")
        self._menu_widgets.append(menu)
        self.set_appearance_mode()
        return menu.menu

    def set_appearance_mode(self, theme_mode: Literal["Light", "Dark"] = None):
        theme = (
            "#252526"
            if (theme_mode or ctk.get_appearance_mode()) == "Dark"
            else "#E9E9E9"
        )
        text_color = "white" if theme == "#252526" else "black"

        self._menu_bar.configure(fg_color=theme)
        for menu in self._menu_widgets:
            menu.configure(
                bg=theme,
                fg=text_color,
                activebackground=theme,
                activeforeground=text_color,
            )
            menu.menu.configure(bg=theme, fg=text_color)