import flet as ft
import subprocess
import sys
import os

def main(page: ft.Page):
    page.title = "VyleyBot Launcher"
    page.window_width = 600
    page.window_height = 400
    page.theme_mode = ft.ThemeMode.DARK

    # Use ListView for logs (scrolls automatically)
    log_view = ft.ListView(expand=True, spacing=5, auto_scroll=True)

    status = ft.Text("Ready.", size=14)
    processes = {}

    def append_log(message: str):
        try:
            log_view.controls.append(ft.Text(message))
        except UnicodeEncodeError:
            log_view.controls.append(ft.Text(message.encode("utf-8", "replace").decode("utf-8")))
        page.update()


    def stream_output(process):
        for line in process.stdout:
            append_log(line.strip())

    def run_bot(e):
        if "bot" in processes and processes["bot"].poll() is None:
            status.value = "⚠️ VyleyBot is already running."
        else:
            status.value = "🚀 Starting VyleyBot..."

        # Detect if running frozen (.exe) or in dev mode
        if getattr(sys, "frozen", False):
            # Running from frozen exe → call the frozen bot exe
            bot_cmd = [os.path.join(os.getcwd(), "VyleyBot.exe")]
        else:
            # Running from source → call Python to run the script
            bot_cmd = [sys.executable, "-u", "VyleyBot.py"]

        processes["bot"] = subprocess.Popen(
            bot_cmd,
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        page.run_thread(stream_output, processes["bot"])

    page.update()


    def stop_bot(e):
        if "bot" in processes and processes["bot"].poll() is None:
            processes["bot"].terminate()
            status.value = "🛑 VyleyBot stopped."
            append_log("[Launcher] Bot stopped.")
        else:
            status.value = "VyleyBot is not running."
        page.update()

    page.add(
        status,
        ft.Row([
            ft.ElevatedButton("Start VyleyBot", on_click=run_bot),
            ft.ElevatedButton("Stop VyleyBot", on_click=stop_bot),
        ]),
        ft.Text("Console Output:", size=12, weight=ft.FontWeight.BOLD),
        log_view,
    )

ft.app(target=main)
