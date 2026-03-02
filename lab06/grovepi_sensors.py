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

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    distance = grovepi.ultrasonicRead(ultrasonic_ranger)

    # TODO: read threshold from potentiometer
    threshold = grovepi.analogRead(potentiometer)

    # clear present for every iteration
    present = ""
    # TODO: format LCD text according to threshhold
    if distance < threshold:
      present = "OBJ PRES"
    else:
      present = ""
    setText_norefresh(str(threshold) + " cm " + present + "\n" + str(distance) + " cm") # norefresh ensures the LCD not to be blinking as it will not refresh each time new text is displayed
  except IOError:
    print("Error")
