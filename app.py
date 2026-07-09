import os
import platform
import socket
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template

app = Flask(__name__)

START_TIME = datetime.now(timezone.utc)
VERSION = "1.1.0"

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
        "version":  VERSION,
    }
    return render_template("index.html", info=info)

@app.route("/health")
def health():
    return jsonify(status="ok", uptime=uptime(), version=VERSION), 200

@app.route("/version")
def version():
    return jsonify(version=VERSION, built_with="python:3.14-alpine"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
