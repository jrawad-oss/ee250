4.1) 
git clone git@github.com:my-name/my-imaginary-repo.git
cd my-imaginary-repo
touch my_second_file.py
nano my_second_file.py
git status
git add my_second_file.py
git commit -m "add my_second_file.py with Hello World"
git push

4.2) For this lab, we 
First, we modified the files on our RPi directly through the command-line text editor ‘nano’
Then, we tested the functionality of the our code with the GrovePi sensors and hardware
Then, we pushed our modified files to our Github repository (ee250) using the appropriate linux shell commands: i.e. git status, git add, git commit -m, git push
Then, we pulled those files on our VM: i.e. git pull
In the future , we could be more efficient by becoming more familiar with linux shell commands for shortcuts and testing smaller chunks of code for each hardware’s functionality so as to clearly identify the location of the issue, if it arises.

4.3) The ultrasonic read function includes a small delay to allow the sensor enough time to send/receive the sound pulse. The delay amount is ~ 50 ms. The raspberry pi uses the Inter-integrated Circuit (I2C) communication protocol to communicate with the Atmega328P on the GrovePi when it tries to read the ultrasonic ranger output using the `grovepi` python library.

4.4) The GrovePi reports values between 0 and 1023 from analog voltages 0V to 5V by utilizing a 10-bit Analog-to-Digital Converter (ADC) on the Atmega328P microcontroller. This is because 10 bits can produce 2^10 = 1024 combinations, which is sufficient for values 0-1023. The raspberry pi cannot perform this directly because it only reads digital signals (0 and 1) and does not have built-in analog input pins. This is why the Atmega328P on the GrovePi is necessary as it does the conversion first, then sens the digital value to the Pi over the I2C communication protocol.

4.5) If our LCD RGB Backlight screen was not displaying any text even though our code
executed without errors, then I would run:
- sudo raspi-config <<< to check if I2C is enabled
- I2cdetect -y 1 <<< to check if LCD is a connected I2C device
- cd GrovePi/Software/Python
  python grove_firmware_version_check.py << to check firmware version and if properly installed

