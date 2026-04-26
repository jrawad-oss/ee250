# Note: parts of this code were developed with the help of llms (chatgpt),
# but we reviewed, tested, and modified everything ourselves to understand how it works

from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

def detect_bird(audio_file, min_conf=0.5):
    analyzer = Analyzer()  # initializes the birdnet model used to analyze audio

    # creates a recording object that links the audio file with the analyzer
    recording = Recording(
        analyzer,
        audio_file,
        min_conf=min_conf  # filters out detections below this confidence
    )

    recording.analyze()  # runs the model on the audio file

    # if nothing was detected, return nothing
    if not recording.detections:
        return None

    # picks the detection with the highest confidence score
    best = max(recording.detections, key=lambda d: d["confidence"])

    # return relevant info about the detected bird
    return {
        "common_name": best["common_name"],
        "scientific_name": best["scientific_name"],
        "confidence": best["confidence"],
        "label": best["label"],
    }
