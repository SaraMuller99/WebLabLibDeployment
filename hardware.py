import os
import json
import RPi.GPIO as GPIO  # Libreria para GPIO
from laboratory import weblab
from weblablib import weblab_user

#Mapa de los GPIO
mapa = {
    1: 2,
    2: 3,
    3: 4,
    4: 17,
    5: 27,
    6: 22,
    7: 10,
    8: 9,
    9: 14,
    10: 15,
    11: 18,
    12: 23,
    13: 24,
    14: 25,
    15: 8,
    16: 7
}

# Configuracion de los GPIO
GPIO.setmode(GPIO.BCM)  # numeracion BCM
#Establecer pines como salida
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

@weblab.on_start
def start(client_data, server_data):
    print("Initializing session for {}".format(weblab_user))

    # Se repite para evitar que un usuario herede el estado de otro
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(14, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    
    # Pin a 0 al inicio de la sesion
    GPIO.setup(2, GPIO.LOW)
    GPIO.setup(3, GPIO.LOW)
    GPIO.setup(4, GPIO.LOW)
    GPIO.setup(17, GPIO.LOW)
    GPIO.setup(27, GPIO.LOW)
    GPIO.setup(22, GPIO.LOW)
    GPIO.setup(10, GPIO.LOW)
    GPIO.setup(9, GPIO.LOW)
    GPIO.setup(14, GPIO.LOW)
    GPIO.setup(15, GPIO.LOW)
    GPIO.setup(18, GPIO.LOW)
    GPIO.setup(23, GPIO.LOW)
    GPIO.setup(24, GPIO.LOW)
    GPIO.setup(25, GPIO.LOW)
    GPIO.setup(8, GPIO.LOW)
    GPIO.setup(7, GPIO.LOW)


@weblab.on_dispose
def dispose():
    print("Disposing session for {}".format(weblab_user))
    clean_resources()
    
    # Limpiamos los GPIO cuando Flask se cierra
    GPIO.cleanup()

def clean_resources():
    print("Cleaning up resources and turning off all lights")
    
    # Apagar las luces 
    for n in range(1, 17):
        switch_light(n, False)

    # Reiniciar el lights.json
    if os.path.exists('lights.json'):
        os.remove('lights.json')

def switch_light(number, state):
    """Turns a specific light on or off and updates the hardware state"""

    # Leer estado actual de las luces
    if not os.path.exists('lights.json'):
        lights = { 'light-{}'.format(n): False for n in range(1, 17) }
    else:
        lights = json.load(open('lights.json'))

    # Actualizar estado de las luces
    lights['light-{}'.format(number)] = state
    json.dump(lights, open('lights.json', 'w'), indent=4)

    # Buscar en el mapa el GPIO correspondiente
    gpio_number = mapa.get(number, "invalid")
    if (gpio_number != "invalid"):
        GPIO.output(gpio_number, GPIO.HIGH if state else GPIO.LOW)
    else: 
        print("Light " + str(number) +" not GPIO mapped")

def is_light_on(number):
    """Checks whether a light is on or off"""
    if not os.path.exists('lights.json'):
        return False
    with open('lights.json', 'r') as file:
        return json.load(file).get("light-{}".format(number), False)
