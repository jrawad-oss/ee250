import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import time
import grovepi
from grove_rgb_lcd import *

# Grove Ultrasonic Ranger connectd to digital port 3 
ultrasonic_ranger = 3
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen  before starting main loop
setText("")
present = ""

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    distance = grovepi.ultrasonicRead(ultrasonic_ranger)

    # TODO: read threshold from potentiometer
    raw_threshold = grovepi.analogRead(potentiometer)
    threshold = int(raw_threshold / 10.23)

     
    # TODO: format LCD text according to threshhold
    if distance < threshold:
      present = "OBJ PRES"
    setText(str(threshold) + " cm " + present +"\n" + str(distance) + " cm ")

  except IOError:
    print("Error")
