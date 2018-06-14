# Ensure /boot/config.txt has added GPIO14 instead of default Pin 4
# dtoverlay=w1-gpio,gpio=14

from sense_hat import SenseHat
from time import sleep
from w1thermsensor import W1ThermSensor

# set up the thermometer
thermometer = W1ThermSensor()

#set up SenseHat
sense = SenseHat()

# set up some colour variables to use
red = (100, 0, 0)
green = (0, 100, 0)
blue = (0, 0, 100)

# clear the screen
sense.clear()

while True:
    temperature = round(thermometer.get_temperature(W1ThermSensor.DEGREES_C), 1)
	
    print("Temperature is ", temperature, " Celsius")

    sense.show_message("Temperature is " + str(temperature) + " Celsius", text_colour=red)
    
    sleep(5)
