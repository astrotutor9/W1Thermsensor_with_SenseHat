# Ensure /boot/config.txt has added GPIO14 instead of default Pin 4
# dtoverlay=w1-gpio,gpio=14

# Run using Python not Python3 as Adafruit libraries are not written in Python3
# Ensure to install W1Thermsensor Python version too! (sudo apt-get install python-w1thermsensor
# Install Adafruit-IO with
# sudo pip install adafruit-io
# sudo pip install requests

import sys
import requests
# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
from sense_hat import SenseHat
import picamera
import datetime
from time import sleep
from w1thermsensor import W1ThermSensor

# set up the thermometer
thermometer = W1ThermSensor()
temperature = 0  # initial reading set up

#set up SenseHat
sense = SenseHat()

# set up some colour variables to use
red = (100, 0, 0)
green = (0, 100, 0)
blue = (0, 0, 100)

# clear the screen
sense.clear()

# set up PiCamera
camera = picamera.PiCamera()

######################################################
# Set up all the things for logging data to Adafruit #
######################################################

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = 'a1c387cb72384d48891e6913521368a6'
ADAFRUIT_IO_USERNAME = 'SoftwareCornwall'  # See https://accounts.adafruit.com
                                                    # to find your username.


# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'Temperature'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for Command changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()

###########################################################
# End of Adafruit set up                                  #
###########################################################


def get_temperature():
    temperature = round(thermometer.get_temperature(W1ThermSensor.DEGREES_C), 1)
    print"Temperature is ", temperature, " Celsius"
    return temperature

def time_now():
    timeNow = datetime.datetime.now().strftime('%H:%M:%S')
    return timeNow

def annotated_image():
    temperature = get_temperature()
    timeNow = time_now()
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = "Temperature reading " + str(temperature) + " deg C"
    camera.capture('/home/pi/W1Thermsensor_with_SenseHat/TemperaturePicture_' + timeNow + '.jpg')

# start loop to continuously check for button presses
while True:    
    for event in sense.stick.get_events():        
        # Check if the joystick was pressed
        if event.action == "pressed":
            # Check which direction
            if event.direction == "up":
                temperature = get_temperature()
                sense.show_message("Temperature is " + str(temperature) + " C", text_colour=green)
                sleep(0.5)
            if event.direction == "down":
                temperature = get_temperature()
                print'Publishing to Adafruit {0}'.format(temperature)
                client.publish(FEED_ID, temperature)
                sense.show_message("Adafruit logged " + str(temperature) + " C", text_colour=red, scroll_speed=0.05)
                sleep(0.5)
            if event.direction == "left":
                annotated_image()
                sense.show_message("Picture taken", text_colour=blue, scroll_speed=0.05)
                sleep(0.5)
            sense.clear()
