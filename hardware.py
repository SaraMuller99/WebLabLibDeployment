import os
import json
import RPi.GPIO as GPIO  # Libreria para GPIO
from laboratory import weblab
from weblablib import weblab_user
import time

#Switches map
mapa = {
    0: 2, 1: 3, 2: 4, 3: 17, 4: 27, 5: 22, 6: 10, 7: 9,
    8: 14, 9: 15, 10: 18, 11: 23, 12: 24, 13: 25, 14: 8, 15: 7
}
#buttons map
botones = {
    0: 5, 1: 6, 2: 13, 3: 19, 4: 26 
} # BTNC, BTNU, BTNL, BTNR, BTND

# All GPIO configuration
GPIO.setmode(GPIO.BCM) 

for pin in mapa.values():
    GPIO.setup(pin, GPIO.OUT)

for pin in botones.values():
    GPIO.setup(pin, GPIO.OUT)



@weblab.on_start
def start(client_data, server_data):
    print("Initializing session for {}".format(weblab_user))

    #Again for avoid inheritance
    GPIO.setmode(GPIO.BCM)
        
    for pin in mapa.values():
        GPIO.setup(pin, GPIO.OUT)
    
    for pin in botones.values():
        GPIO.setup(pin, GPIO.OUT)

    #GPIO to 0 at the beggining
    for pin in mapa.values():
        GPIO.setup(pin, GPIO.LOW)

    for pin in botones.values():
        GPIO.setup(pin, GPIO.LOW)  


@weblab.on_dispose
def dispose():
    print("Disposing session for {}".format(weblab_user))
    clean_resources()
    
    #Clean GPIO at the end
    GPIO.cleanup()

def clean_resources():
    print("Cleaning up resources")
    
    #Turn off switches
    for n in range(0, 16):
        switch_light(n, False)

    #Reboot json
    if os.path.exists('lights.json'):
        os.remove('lights.json')

def switch_light(number, state):
    """Turns a specific light on or off and updates the hardware state"""

    #Read json
    if not os.path.exists('lights.json'):
        lights = { 'light-{}'.format(n): False for n in range(0, 16) }
    else:
        lights = json.load(open('lights.json'))

    #Update json
    lights['light-{}'.format(number)] = state
    json.dump(lights, open('lights.json', 'w'), indent=4)

    #Find in map the correct GPIO
    gpio_number = mapa.get(number, "invalid")
    if (gpio_number != "invalid"):
        GPIO.output(gpio_number, GPIO.HIGH if state else GPIO.LOW)
    else: 
        print("Light " + str(number) +" not GPIO mapped")

#Buttons
def send_pulse(button_id):
    gpio_number = botones.get(button_id)
    if gpio_number is not None:
        print("Sending pulse to GPIO", gpio_number)
        GPIO.output(gpio_number, GPIO.HIGH)
        time.sleep(0.2)  #200ms pulse
        GPIO.output(gpio_number, GPIO.LOW)
        print("Pulse sent to GPIO", gpio_number)
    else:
        print("Invalid button_id:", button_id)
#

def is_light_on(number):
    """Checks whether a light is on or off"""
    if not os.path.exists('lights.json'):
        return False
    with open('lights.json', 'r') as file:
        return json.load(file).get("light-{}".format(number), False)
