# Note: parts of this code were developed with the help of llms (chatgpt),
# but we reviewed, tested, and modified everything ourselves to understand how it works

from flask import Flask, request, jsonify, render_template
import os
import tempfile
import time
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib
matplotlib.use("Agg")  # allows plotting without a display (needed on vm)
import matplotlib.pyplot as plt

from detect_bird import detect_bird

# sets up flask app and tells it where templates + static files are
app = Flask(__name__, template_folder="templates", static_folder="static")

# defines important directories for saving files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
CAPTURE_DIR = os.path.join(STATIC_DIR, "captures")
os.makedirs(CAPTURE_DIR, exist_ok=True)  # create folder if it doesn’t exist

# stores the most recent detection to display on dashboard
LATEST = {
    "bird": "None",
    "confidence": 0,
    "spectrogram": None,
    "capture": None,
    "timestamp": None,
}

def make_spectrogram(wav_path, out_path):
    # reads the audio file
    sample_rate, audio = wavfile.read(wav_path)

    # if stereo, just use one channel
    if len(audio.shape) > 1:
        audio = audio[:, 0]

    # normalize audio depending on type
    if audio.dtype.kind in ("i", "u"):
        audio = audio.astype(np.float32) / np.iinfo(audio.dtype).max
    else:
        audio = audio.astype(np.float32)

    # generates spectrogram data (frequency vs time)
    frequencies, times, spectrogram = signal.spectrogram(audio, fs=sample_rate)

    # plots and saves spectrogram image
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
    # renders dashboard and passes latest detection data
    return render_template("index.html", latest=LATEST)

@app.route("/analyze", methods=["POST"])
def analyze():
    # checks if audio file was sent from pi
    if "file" not in request.files:
        return jsonify({"bird": "none", "confidence": 0, "error": "missing file"}), 400

    uploaded = request.files["file"]

    # saves uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        uploaded.save(tmp.name)
        wav_path = tmp.name

    # creates and saves spectrogram image
    spec_name = f"latest_spectrogram_{int(time.time())}.png"
    spec_path = os.path.join(STATIC_DIR, spec_name)
    make_spectrogram(wav_path, spec_path)

    # runs bird detection model
    result = detect_bird(wav_path)

    if result is None:
        LATEST["bird"] = "none"
        LATEST["confidence"] = 0
    else:
        LATEST["bird"] = result["common_name"]
        LATEST["confidence"] = float(result["confidence"])

    # update latest data for dashboard
    LATEST["spectrogram"] = f"static/{spec_name}"
    LATEST["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # send result back to pi
    return jsonify({
        "bird": LATEST["bird"],
        "confidence": LATEST["confidence"]
    })

@app.route("/upload_capture", methods=["POST"])
def upload_capture():
    # receives image from raspberry pi
    if "file" not in request.files:
        return jsonify({"status": "error", "error": "missing file"}), 400

    uploaded = request.files["file"]
    bird = request.form.get("bird", "unknown").replace(" ", "_")
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{bird}.jpg"
    save_path = os.path.join(CAPTURE_DIR, filename)
    uploaded.save(save_path)

    # update latest image shown on dashboard
    LATEST["capture"] = f"static/captures/{filename}"
    LATEST["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "status": "ok",
        "file": filename
    })

if __name__ == "__main__":
    print("vm server running on port 8000")
    # host=0.0.0.0 allows other devices (like the pi) to connect
    app.run(host="0.0.0.0", port=8000)
