import os
import json
import RPi.GPIO as GPIO  # Importing the library to control GPIO
from laboratory import weblab
from weblablib import weblab_user

# Set up GPIO for Raspberry Pi
GPIO.setmode(GPIO.BCM)  # Using BCM numbering
GPIO.setup(17, GPIO.OUT)  # Set GPIO17 as an output

@weblab.on_start
def start(client_data, server_data):
    print("Initializing {}".format(weblab_user))

@weblab.on_dispose
def dispose():
    print("Disposing {}".format(weblab_user))
    clean_resources()

def clean_resources():
    """Turns off all lights and cleans up GPIO resources"""
    for n in range(1, 11):
        switch_light(n, False)
    GPIO.cleanup()  # Release GPIO pins

def switch_light(number, state):
    """Turns a specific light on or off and controls GPIO17 if it's light 1"""
    if not os.path.exists('lights.json'):
        lights = {"light-{}".format(n): False for n in range(1, 11)}
    else:
        with open('lights.json', 'r') as file:
            lights = json.load(file)
    
    lights["light-{}".format(number)] = state
    
    with open('lights.json', 'w') as file:
        json.dump(lights, file, indent=4)
    
    # Control GPIO17 if light 1 is toggled
    if number == 1:
        GPIO.output(17, state)

def is_light_on(number):
    """Checks whether a light is on or off"""
    if not os.path.exists('lights.json'):
        return False
    with open('lights.json', 'r') as file:
        return json.load(file).get("light-{}".format(number), False)
