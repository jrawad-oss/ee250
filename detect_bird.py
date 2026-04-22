from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

def detect_bird(audio_file, min_conf=0.5):
    analyzer = Analyzer()

    recording = Recording(
        analyzer,
        audio_file,
        min_conf=min_conf
    )

    recording.analyze()

    if not recording.detections:
        return None

    best = max(recording.detections, key=lambda d: d["confidence"])

    return {
        "common_name": best["common_name"],
        "scientific_name": best["scientific_name"],
        "confidence": best["confidence"],
        "label": best["label"],
    }

