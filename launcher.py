from flask import Flask, render_template, jsonify, request
import subprocess, sys, os

app = Flask(__name__)

# Track your running bot process (optional)
bot_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_bot():
    global bot_process
    if bot_process is None or bot_process.poll() is not None:
        # Start VyleyBot in background
        bot_process = subprocess.Popen([sys.executable, "VyleyBot.py"])
        return jsonify({"status": "running"})
    else:
        return jsonify({"status": "already_running"})

@app.route("/stop", methods=["POST"])
def stop_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        bot_process.terminate()
        bot_process = None
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not_running"})

@app.route("/logs")
def get_logs():
    log_file = "vyleybot.log"
    if not os.path.exists(log_file):
        return jsonify([])
    with open(log_file, "r") as f:
        return jsonify(f.readlines()[-50:])

if __name__ == "__main__":
    app.run(debug=True)