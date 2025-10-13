import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess, threading, sys, os, io


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8", errors="replace")


class VyleyControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VyleyBot Control Center 💜")
        self.geometry("800x500")
        self.configure(bg="#1a1a1a")

        # --- UI ---
        tk.Label(self, text="VyleyBot Console", fg="#bb86fc", bg="#1a1a1a", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.console = ScrolledText(self, bg="#000", fg="#0f0", insertbackground="#0f0",
                                    wrap="word", font=("Consolas", 10))
        self.console.pack(fill="both", expand=True, padx=10, pady=10)

        frame = tk.Frame(self, bg="#1a1a1a")
        frame.pack(pady=5)

        self.status_label = tk.Label(frame, text="🔴 Offline", fg="#ff5555", bg="#1a1a1a", font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side="left", padx=10)

        tk.Button(frame, text="Start Bot", command=self.start_bot, bg="#2b2b2b", fg="white").pack(side="left", padx=5)
        tk.Button(frame, text="Stop Bot", command=self.stop_bot, bg="#2b2b2b", fg="white").pack(side="left", padx=5)

        # --- Vars ---
        self.bot_proc = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- Bot Controls ---
    def start_bot(self):
        if not self.bot_proc or self.bot_proc.poll() is not None:
            self.console.insert(tk.END, "🚀 Starting VyleyBot...\n")
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            self.bot_proc = subprocess.Popen(
                [sys.executable, "-u", "VyleyBot.py"],  # <- the -u flag forces unbuffered I/O
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1
            )

            self.status_label.config(text="🟢 Online", fg="#00ff88")
            threading.Thread(target=self.read_output, daemon=True).start()
        else:
            self.console.insert(tk.END, "⚠️ Bot already running.\n")

    def stop_bot(self):
        if self.bot_proc and self.bot_proc.poll() is None:
            self.console.insert(tk.END, "🛑 Stopping VyleyBot...\n")
            self.bot_proc.terminate()
            self.bot_proc = None
            self.status_label.config(text="🔴 Offline", fg="#ff5555")
        else:
            self.console.insert(tk.END, "⚠️ Bot not running.\n")

    def read_output(self):
        for line in self.bot_proc.stdout:
            self.console.insert(tk.END, line)
            self.console.see(tk.END)

    def on_close(self):
        self.stop_bot()
        self.destroy()


if __name__ == "__main__":
    VyleyControl().mainloop()
