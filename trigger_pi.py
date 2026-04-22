import sys
import requests

PI_URL = "http://172.20.10.3:5000/capture"

def send_trigger(bird_name, confidence):
    payload = {
        "bird": bird_name,
        "confidence": confidence
    }

    response = requests.post(PI_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 trigger_pi.py <bird_name> <confidence>")
        raise SystemExit(1)

    bird = sys.argv[1]
    confidence = float(sys.argv[2])

    result = send_trigger(bird, confidence)
    print(result)
