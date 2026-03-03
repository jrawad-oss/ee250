import sys
import os
sys.path.append(os.path.expanduser('~/Dexter/GrovePi/Software/Python'))
import time
import grovepi
from grove_rgb_lcd import *

# Grove Ultrasonic Ranger connectd to digital port 2
ultrasonic_ranger = 2
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen before starting main loop
setText("")

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    distance = grovepi.ultrasonicRead(ultrasonic_ranger)
    if distance is None or distance <= 0:
      distance = 0

    # TODO: read threshold from potentiometer
    threshold = grovepi.analogRead(potentiometer)
    if threshold is None:
      threshold = 0

    threshold_in_cm = float(threshold) * 517.0 / 1023.0

    # TODO: format LCD text according to threshhold
    if float(distance) < threshold_in_cm:
      present = "OBJ PRES"
    else:
      present = ""

    top = (str(int(threshold)) + " " + present).ljust(16)
    bottom = str(int(distance)) + " cm"

    setText_norefresh(top + "\n" + bottom)
    time.sleep(0.18)

  except IOError:
    print("Error")
