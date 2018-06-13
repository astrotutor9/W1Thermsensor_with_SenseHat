# Ensure /boot/config.txt has added GPIO14 instead of default Pin 4
# dtoverlay=w1-gpio,gpio=14

from time import sleep
from w1thermsensor import W1ThermSensor

# set up the thermometer
thermometer = W1ThermSensor()

temperature = thermometer.get_temperature(W1ThermSensor.DEGREES_C)
	
print("Temperature is ", temperature, " Celsius")

    
