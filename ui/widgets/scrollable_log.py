import tkinter as tk

class ScrollableLog(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # --- Canvas and Scrollbar ---
        self.canvas = tk.Canvas(self, bg=self.cget("bg"), highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # --- Inner Frame (where messages go) ---
        self.log_frame = tk.Frame(self.canvas, bg=self.cget("bg"))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.log_frame, anchor="nw")

        # --- Grid layout for log + scrollbar ---
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Bind events for resizing & scrolling ---
        self.log_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # Auto-adjust scroll region when new items are added
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Make log_frame width match the canvas width
    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    # Smooth scrolling with mouse wheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_message(self, text, sender="user"):
    # Colors & alignment based on sender
        if sender == "bot":
            bubble_bg = "#005A8A"   # bluish
            text_fg = "white"
            anchor = "e"            # right-aligned
            padx = (100, 10)        # left padding, right spacing
        else:
            bubble_bg = "#77d0ff"   # grayish
            text_fg = "white"
            anchor = "w"            # left-aligned
            padx = (10, 100)

    # Bubble container frame
        bubble_frame = tk.Frame(self.log_frame, bg=self.log_frame.cget("bg"))
        bubble_frame.pack(fill="x", pady=3, padx=10, anchor=anchor)

    # The bubble itself (label)
        bubble = tk.Label(
            bubble_frame,
            text=text,
            bg=bubble_bg,
            fg=text_fg,
            padx=10,
            pady=6,
            wraplength=500,
            justify="left",
            anchor="w",
            font=("Segoe UI", 10)
        )

    # Give the illusion of rounded corners (padding + color contrast)
        bubble.pack(anchor=anchor, ipadx=5, ipady=3, padx=padx)

    # Scroll to bottom automatically
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

