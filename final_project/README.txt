README.txt - Instructions

Names: Matillda Awad (4518997700) and Jessica Awad (2939433007)

Python scripts in zip file:
server.py
sound_capture.py (created manually on Raspberry Pi using nano)
detect_bird.py
templates/index.html
static/captures/

External Libraries Used:
- flask
- birdnetlib
- librosa
- resampy
- soundfile
- audioread
- tensorflow
- numpy
- scipy
- matplotlib
- requests
- Adafruit_MCP3008
- Adafruit_GPIO


Hardware Setup:
STEP 0: Connect to raspberry pi
Camera module v2
USB-A microphone
Grove Pi Sound Sensor connect to Channel 1 on PCB from lab 10

On Virtual Machine:

STEP 1: Download final_project.zip and extract it into your Downloads folder (no extra folders). Then run:
cd ~/Downloads/final_project

STEP 2:
sudo apt update
sudo apt install python3.12-venv

STEP 3: create virtual environment
python3 -m venv .venv
source .venv/bin/activate

STEP 4: install python packages
pip install flask birdnetlib librosa resampy soundfile audioread tensorflow numpy scipy matplotlib

STEP 5: install system dependency 
sudo apt update
sudo apt install ffmpeg -y

On Raspberry Pi:
STEP 6: install python packages
pip3 install requests Adafruit_MCP3008 Adafruit_GPIO

STEP 7: install audio tools
sudo apt update
sudo apt install alsa-utils -y

STEP 8: install camera tools (for older pi OS ONLY)
sudo apt install libraspberrypi-bin -y

STEP 9: Enable SPI for ADC
sudo raspi-config
*** it will pop up a window, follow these actions: 
Interface Options → SPI → Enable

STEP 10: Enable camera (for older pi OS ONLY)
On same window, also follow these actions:
Interface Options → Camera → Enable
*Now click Finish and yes to reboot

STEP 11: Reboot
sudo reboot
* go back into RPi

STEP 12: verify USB mic works
arecord -l
*You should see USB audio device like: 

“**** List of CAPTURE Hardware Devices ****
card 1: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0”

STEP 13: Create sound_capture.py on Raspberry Pi (in home directory)
cd ~
nano sound_capture.py

STEP 14: You can either copy and paste the capture_sound.py that lives on your VM (Downloads/final_project/pi directory) or copy and paste the code below into the file:

# start of code

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

# end of code

~Run the System~

STEP 15: On Virtual Machine:
* make sure you are in final_project folder
cd vm

source .venv/bin/activate
python3 server.py

STEP 16: On RPi:
cd ~
python3 sound_capture.py

STEP 17: open dashboard on VM browser
http://<VM_IP_ADDRESS>:8000


Now the Bird Wildlife IoT system is complete!! Once a sound is detected, the system will record the audio in real time and identify if the noise came from a bird (sound has to be longer than ~4 seconds), and if so, the ML classifier from birdnetlib will run the audio and reveal what type of bird it is. Once a bird's presence is confirmed, the system will capture a picture of the bird indicated by the LED on the PCB as well as text confirmation on the pi terminal. On the VM web browser, you should see what bird the ML detected along with its confidence of prediction. In addition, you should see the spectrogram (specifically, the one we generated with our python script) of the bird call and the picture capture. The system runs continuously until force quit with Ctrl + C. Have fun with it!!


