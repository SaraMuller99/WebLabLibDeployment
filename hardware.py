#--------------------------Interaction with the FPGA--------------------------

import os
import json
import RPi.GPIO as GPIO
from laboratory import weblab
from weblablib import weblab_user
import time

#Stuff for upload bitstream
import subprocess
import tempfile

#MAPS: Define the GPIO port
#Switches map
switches = {
    0: 2, 1: 3, 2: 4, 3: 17, 4: 27, 5: 22, 6: 10, 7: 9,
    8: 14, 9: 15, 10: 18, 11: 23, 12: 24, 13: 25, 14: 8, 15: 7
}
#Buttons map
buttons = {
    0: 5, 1: 6, 2: 13, 3: 19, 4: 26 
#   BTNC  BTNU  BTNL   BTNR   BTND
} 

#GPIO CONFIGURATION
#GPIO numeration not pin numeration
GPIO.setmode(GPIO.BCM) 
#Establish gpio's as output 
for pin in switches.values():
    GPIO.setup(pin, GPIO.OUT)
for pin in buttons.values():
    GPIO.setup(pin, GPIO.OUT)

#START CONFIGURATION
@weblab.on_start #Decorator that makes the function to be execute at the begining of execution
def start(client_data, server_data):
    print("Initializing session for {}".format(weblab_user))

    #Again for avoid inheritance
    GPIO.setmode(GPIO.BCM)  
    for pin in switches.values():
        GPIO.setup(pin, GPIO.OUT)
    for pin in buttons.values():
        GPIO.setup(pin, GPIO.OUT)

    #GPIO to 0 at the beggining
    for pin in switches.values():
        GPIO.setup(pin, GPIO.LOW)
    for pin in buttons.values():
        GPIO.setup(pin, GPIO.LOW)  

#END CONFIGURATION
@weblab.on_dispose #Decorator that makes the function to be execute at the end of execution or reload
def dispose():
    print("Disposing session for {}".format(weblab_user))
    clean_resources()
    
    #Clean GPIO at the end
    GPIO.cleanup()

def clean_resources():
    print("Cleaning up resources")
    
    #Turn off switches
    for n in range(0, 16):
        switch_switches(n, False)

    #Reboot json
    if os.path.exists('switches.json'):
        os.remove('switches.json')

#TURN ON AND OFF SWITCHES
#Use a json file to know the state of the switch and turn it on or off
def switch_switches(number, state):

    #Read json
    if not os.path.exists('switches.json'):
        sw = { 'switch-{}'.format(n): False for n in range(0, 16) }
    else:
        sw = json.load(open('switches.json'))

    #Update json
    sw['switch-{}'.format(number)] = state
    json.dump(sw, open('switches.json', 'w'), indent=4)

    #Find in map the correct GPIO
    gpio_number = switches.get(number, "invalid")
    if (gpio_number != "invalid"):
        GPIO.output(gpio_number, GPIO.HIGH if state else GPIO.LOW)
    else: 
        print("switch " + str(number) +" not GPIO mapped")
#Get the switch state
def is_switch_on(number):
    
    if not os.path.exists('switches.json'):
        return False
    with open('switches.json', 'r') as file:
        return json.load(file).get("switch-{}".format(number), False)

#BUTTONS
#Simulate the button by sending a limited pulse
def send_pulse(button_id):

    gpio_number = buttons.get(button_id)
    if gpio_number is not None:
        print("Sending pulse to GPIO", gpio_number)
        GPIO.output(gpio_number, GPIO.HIGH)
        time.sleep(0.2)  #200ms pulse
        GPIO.output(gpio_number, GPIO.LOW)
        print("Pulse sent to GPIO", gpio_number)
    else:
        print("Invalid button_id:", button_id)


#UPLOAD BITSTREAM
#Use https://trabucayre.github.io/openFPGALoader/ to uplode the bitstream faster without vivado
def upload_bitstream(bitstream_bytes):
    try:
        #Save .bit as temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bit") as temp_file:
            temp_file.write(bitstream_bytes)
            ruta_bitstream = temp_file.name

        #OpenFPGALoader command
        comando = [
            "/usr/local/bin/openFPGALoader",
            "-b", "nexys_a7_100",
            ruta_bitstream
        ]

        #Popen allows to execute commands as the OS
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proceso.communicate()
        returncode = proceso.returncode

        #Delete .bit to save space
        os.remove(ruta_bitstream)

        if returncode == 0:
            return {"exito": True, "mensaje": "Bitstream cargado correctamente."}
        else:
            return {"exito": False, "mensaje": err}

    except OSError:
        return {"exito": False, "mensaje": "openFPGALoader no encontrado."}
    except Exception as e:
        return {"exito": False, "mensaje": "Error inesperado: {0}".format(e)}
