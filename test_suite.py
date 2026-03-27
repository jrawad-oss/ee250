import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# by taking readings and printing them out, find
# appropriate threshold levels and set them
# accordingly. Then, use them to determine
# when it is light or dark, quiet or loud.
lux_treshold = 100
sound_treshold = 350

while True:
    time.sleep(0.5)

    # blink LED 5 times with a delay of 500 ms in between
    for _ in range(5):
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.5)

    # read the light value from sensor for 5 sec with a delay of 100 ms
    start_time = time.time()
    while time.time() - start_time < 5:
        light_value = mcp.read_adc(0)

        # if the light value is equal to or greater than our set threshold, display the value and "bright"
        if light_value >= lux_treshold:
            print("Light Raw Value:", light_value, "bright")
        else:
            print("Light Raw Value:", light_value, "dark") # did not meet the threshold so --> dark

        time.sleep(0.1) # delay 100 ms

    # blink LED 4 times with 200 ms on/off in between
    for _ in range(4):
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.2)

    # read sound sensor value with the mcp3008 adc for about 5 seconds, every 100 ms
    start_time = time.time()
    while time.time() - start_time < 5:
        sound_value = mcp.read_adc(1)
        print("Sound Raw Value:", sound_value)

        # if the sound value is equal to or greater than our set threshold, light the LED
        if sound_value >= sound_treshold:
            GPIO.output(11, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(11, GPIO.LOW)

        time.sleep(0.1) # delay 100 ms
