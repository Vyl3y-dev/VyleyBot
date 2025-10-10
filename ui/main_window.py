import tkinter as tk
from widgets.common_widgets import TitleLabel, StartButton
from widgets.common_widgets import get_title_font, get_normal_font, get_special_font
#from tkinter import messagebox
from widgets.scrollable_log import ScrollableLog


root = tk.Tk()
root.title("VyleyBot Console")
root.geometry("1024x768")
root.resizable(True, True)
root.config(bg="#042d42")
TitleFont = get_title_font(root)
SpecialFont = get_special_font(root)
NormalFont = get_normal_font(root)

#my grid should look like this:
#  ┌───────────────topbar───────────────┐
#  │      leftbox    |      rightbox    │
#  └───────────────bottombar────────────┘

root.grid_rowconfigure(0, weight=1)   # topbar
root.grid_rowconfigure(1, weight=0)   # headers
root.grid_rowconfigure(2, weight=8)   # boxes
root.grid_rowconfigure(3, weight=1)   # bottombar

root.grid_columnconfigure(0, weight=3)  # leftbox
root.grid_columnconfigure(1, weight=17) # rightbox

# topbar
topbar = tk.Frame(root, bg=root.cget("bg"))
topbar.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=5)
topbar_title = TitleLabel(topbar, "TOPBAR", TitleFont).pack()

# leftbox_header
leftbox_header = tk.Frame(root, bg="#0DAAFF")
leftbox_header.grid(row=1, column=0, sticky="nsew", padx=5)
leftbox_title = TitleLabel(leftbox_header, "LEFTBOX", TitleFont).pack()

#rightbox_header
rightbox_header = tk.Frame(root, bg="#0DAAFF")
rightbox_header.grid(row=1, column=1, sticky="nsew", padx=5)
rightbox_title = TitleLabel(rightbox_header, "RIGHTBOX", TitleFont).pack()
# log = ScrollableLog(rightbox, bg=rightbox.cget("bg"))
# log.pack(fill="both", expand=True)

#leftbox
leftbox = tk.Frame(root, bg="#0DAAFF")
leftbox.grid(row=2, column=0, sticky="nsew", padx=5)

#rightbox
rightbox = tk.Frame(root, bg="#0DAAFF")
rightbox.grid(row=2, column=1, sticky="nsew", padx=5)

#bottombar
bottombar = tk.Frame(root, bg=root.cget("bg"), height=40)
bottombar.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
bottombar_title = TitleLabel(bottombar, "BOTTOMBAR", TitleFont).pack()
start_button = StartButton(bottombar, text="Start Bot", command=None).pack()

# for i in range(30):
#     log.add_message(f"Message number {i+1}", "user")
#     log.add_message(f"Message number {i+1}", "bot")

root.mainloop()
