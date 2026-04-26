# Note: parts of this code were developed with the help of LLMs (chatgpt),
# but we reviewed, tested, and modified everything ourselves to understand how it works
import os
import time
import requests
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# using physical pin numbering on the pi
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# setting up the led pin as an output so we can turn it on/off
LED_PIN = 11
GPIO.setup(LED_PIN, GPIO.OUT)

SPI_PORT = 0
SPI_DEVICE = 0
# setting up spi communication so we can talk to the mcp3008 adc (reads analog signals)
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

SOUND_CHANNEL = 1  # the channel on the adc where the sound sensor is connected
SOUND_THRESHOLD = 350  # value above this means "loud enough" to trigger recording

# endpoints on the vm where we send data (audio + images)
VM_URL = "http://172.20.10.4:8000/analyze"
UPLOAD_URL = "http://172.20.10.4:8000/upload_capture"

AUDIO_FILE = "audio.wav" 
CAPTURE_DIR = "captures" # where images will be saved (relative path)
os.makedirs(CAPTURE_DIR, exist_ok=True) # for captures,  creates folder if it doesn’t already exist

CONFIDENCE_THRESHOLD = 0.50 # only accept bird predictions above this confidence
COOLDOWN_SECONDS = 5  # prevents triggering too frequently

def record_audio():
    print("Recording audio...")
    # uses arecord to capture 3 seconds of audio from usb mic
    os.system(f"arecord -D plughw:1,0 -f S16_LE -r 44100 -d 3 {AUDIO_FILE}")
    return AUDIO_FILE

def take_picture(label):
    timestamp = time.strftime("%Y%m%d_%H%M%S") # timestamp so filenames are unique
    safe_label = label.replace(" ", "_").replace("/", "_")  # clean label for filename
    filename = f"{CAPTURE_DIR}/{timestamp}_{safe_label}.jpg"

    print("LED ON")
    GPIO.output(LED_PIN, GPIO.HIGH) # turn led on to indicate capture
    time.sleep(1)

    print("Taking picture now:", filename)
    os.system(f"raspistill -o {filename}")  # captures image using pi camera

    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW) # turn led off after capture
    print("LED OFF")
    print("Saved:", filename)

    return filename

def upload_capture_to_vm(image_path, bird, confidence):
    try:
        # sending the captured image + metadata to the vm for display
        with open(image_path, "rb") as f:
            response = requests.post(
                UPLOAD_URL,
                files={"file": f},
                data={
                    "bird": bird,
                    "confidence": str(confidence)
                },
                timeout=60
            )
        print("Upload status:", response.status_code)
        print("Upload response:", response.text)
    except Exception as e:
        print("Error uploading image to VM:", e)

print("Listening...")

last_trigger_time = 0 # keeps track of last time we triggered to enforce cooldown

try:
    while True:
        sound_value = mcp.read_adc(SOUND_CHANNEL) # read analog value from sound sensor
        print("Sound:", sound_value)

        now = time.time()
        # trigger only if sound is loud enough AND cooldown has passed
        if sound_value >= SOUND_THRESHOLD and (now - last_trigger_time) >= COOLDOWN_SECONDS:
            last_trigger_time = now
            print("Sound detected → processing")

            audio_file = record_audio()

            try:
                print("Sending to VM for BirdNET...")
                # send audio file to vm for ml classification
                with open(audio_file, "rb") as f:
                    response = requests.post(VM_URL, files={"file": f}, timeout=60)

                print("VM status code:", response.status_code)

                try:
                    result = response.json() # expecting json response with bird + confidence
                except Exception:
                    print("VM returned non-JSON response:")
                    print(response.text)
                    time.sleep(2)
                    continue

                print("VM result:", result)

                bird = result.get("bird", "unknown")
                confidence = float(result.get("confidence", 0))

                # only take picture if model is confident enough
                if confidence >= CONFIDENCE_THRESHOLD:
                    image_path = take_picture(bird)
                    upload_capture_to_vm(image_path, bird, confidence)
                else:
                    print("Confidence too low, skipping capture.")

            except Exception as e:
                print("Error talking to VM:", e)

            time.sleep(2)

        time.sleep(0.1)  # small delay so we’re not constantly hammering the cpu

except KeyboardInterrupt:
    print("Stopping...")

finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup() # clean up gpio so pins don’t stay in weird states
