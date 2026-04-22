from flask import Flask, request, jsonify, render_template
import os
import tempfile
import time
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from detect_bird import detect_bird

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
CAPTURE_DIR = os.path.join(STATIC_DIR, "captures")
os.makedirs(CAPTURE_DIR, exist_ok=True)

LATEST = {
    "bird": "None",
    "confidence": 0,
    "spectrogram": None,
    "capture": None,
    "timestamp": None,
}

def make_spectrogram(wav_path, out_path):
    sample_rate, audio = wavfile.read(wav_path)

    if len(audio.shape) > 1:
        audio = audio[:, 0]

    if audio.dtype.kind in ("i", "u"):
        audio = audio.astype(np.float32) / np.iinfo(audio.dtype).max
    else:
        audio = audio.astype(np.float32)

    frequencies, times, spectrogram = signal.spectrogram(audio, fs=sample_rate)

    plt.figure(figsize=(10, 4))
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram + 1e-10), shading="gouraud")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.title("Spectrogram")
    plt.colorbar(label="Intensity [dB]")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

@app.route("/")
def index():
    return render_template("index.html", latest=LATEST)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"bird": "none", "confidence": 0, "error": "missing file"}), 400

    uploaded = request.files["file"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        uploaded.save(tmp.name)
        wav_path = tmp.name

    spec_name = f"latest_spectrogram_{int(time.time())}.png"
    spec_path = os.path.join(STATIC_DIR, spec_name)
    make_spectrogram(wav_path, spec_path)

    result = detect_bird(wav_path)

    if result is None:
        LATEST["bird"] = "none"
        LATEST["confidence"] = 0
    else:
        LATEST["bird"] = result["common_name"]
        LATEST["confidence"] = float(result["confidence"])

    LATEST["spectrogram"] = f"static/{spec_name}"
    LATEST["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "bird": LATEST["bird"],
        "confidence": LATEST["confidence"]
    })

@app.route("/upload_capture", methods=["POST"])
def upload_capture():
    if "file" not in request.files:
        return jsonify({"status": "error", "error": "missing file"}), 400

    uploaded = request.files["file"]
    bird = request.form.get("bird", "unknown").replace(" ", "_")
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{bird}.jpg"
    save_path = os.path.join(CAPTURE_DIR, filename)
    uploaded.save(save_path)

    LATEST["capture"] = f"static/captures/{filename}"
    LATEST["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "status": "ok",
        "file": filename
    })

if __name__ == "__main__":
    print("VM server running on port 8000")
    app.run(host="0.0.0.0", port=8000)
