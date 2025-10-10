import tkinter as tk
import tkinter.font as tkFont

def get_title_font(root):
    return tkFont.Font(root=root, family="Courier", size=16, weight="bold")

def get_special_font(root):
    return tkFont.Font(root=root, family="Courier", size=12, weight="bold", slant="italic")

def get_normal_font(root):
    return tkFont.Font(root=root, family="Courier", size=12)
    

class StandardLabel(tk.Frame):
    def __init__(self, parent, text="", font=None, **kwargs):
        # Extract visual settings safely
        bg_color = kwargs.pop("bg", parent.cget("bg"))
        fg_color = kwargs.pop("fg", "white")

        # Initialize the frame (no 'fg' sent to Frame)
        super().__init__(parent, bg=bg_color, **kwargs)

        # Create the label inside with matching colors
        self.label = tk.Label(self, text=text, font=font, bg=bg_color, fg=fg_color)
        self.label.pack()


class TitleLabel(tk.Frame):
    def __init__(self, parent, text="", font=None, **kwargs):
        # Extract visual settings safely
        bg_color = kwargs.pop("bg", parent.cget("bg"))
        fg_color = kwargs.pop("fg", "white")

        # Initialize the frame (no 'fg' sent to Frame)
        super().__init__(parent, bg=bg_color, **kwargs)

        # Create the label inside with matching colors
        self.label = tk.Label(self, text=text, font=font, bg=bg_color, fg=fg_color)
        self.label.pack()


class StartButton(tk.Button):
    def __init__(self, parent, text="Start", command=None, **kwargs):
        kwargs.setdefault("bg", "#0daaff")
        kwargs.setdefault("activebackground", "#005a8a")
        kwargs.setdefault("fg", "white")
        kwargs.setdefault("font", ("Segoe UI", 10, "bold"))
        super().__init__(parent, text=text, command=command, **kwargs)

        # store normal color for reverting
        self.default_bg = kwargs["bg"]
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg="#77d0ff")  # lighter hover

    def _on_leave(self, event):
        self.config(bg=self.default_bg)

