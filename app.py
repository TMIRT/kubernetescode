import os
import platform
import socket
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template

app = Flask(__name__)

START_TIME = datetime.now(timezone.utc)

def uptime():
    delta = datetime.now(timezone.utc) - START_TIME
    h, rem = divmod(int(delta.total_seconds()), 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s"

@app.route("/")
def index():
    info = {
        "hostname": socket.gethostname(),
        "python":   platform.python_version(),
        "platform": platform.system(),
        "uptime":   uptime(),
        "env":      os.environ.get("APP_ENV", "production"),
    }
    return render_template("index.html", info=info)

@app.route("/health")
def health():
    return jsonify(status="ok", uptime=uptime()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
