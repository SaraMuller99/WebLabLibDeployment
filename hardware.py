import os
import json
import RPi.GPIO as GPIO  # Librería para GPIO
from laboratory import weblab
from weblablib import weblab_user

# Configuración de los GPIO
GPIO.setmode(GPIO.BCM)  # numeracion BCM
GPIO.setup(17, GPIO.OUT)  # GPIO17 como salida

@weblab.on_start
def start(client_data, server_data):
    print("Initializing session for {}".format(weblab_user))

    # Se repite para evitar que un usuario herede el estado de otro
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    
    # Pin a 0 al inicio de la sesión
    GPIO.output(17, GPIO.LOW)


@weblab.on_dispose
def dispose():
    print("Disposing session for {}".format(weblab_user))
    clean_resources()
    
    # Limpiamos los GPIO cuando Flask se cierra
    GPIO.cleanup()

def clean_resources():
    print("Cleaning up resources and turning off all lights")
    
    # Apagar las luces 
    for n in range(1, 11):
        switch_light(n, False)

    # Reiniciar el lights.json
    if os.path.exists('lights.json'):
        os.remove('lights.json')

def switch_light(number, state):
    """Turns a specific light on or off and updates the hardware state"""

    # Leer estado actual de las luces
    if not os.path.exists('lights.json'):
        lights = { 'light-{}'.format(n): False for n in range(1, 11) }
    else:
        lights = json.load(open('lights.json'))

    # Actualizar estado de las luces
    lights['light-{}'.format(number)] = state
    json.dump(lights, open('lights.json', 'w'), indent=4)

    # Si la luz 1 es la que cambia, actualizar GPIO17
    if number == 1:
        GPIO.output(17, GPIO.HIGH if state else GPIO.LOW)

def is_light_on(number):
    """Checks whether a light is on or off"""
    if not os.path.exists('lights.json'):
        return False
    with open('lights.json', 'r') as file:
        return json.load(file).get("light-{}".format(number), False)
