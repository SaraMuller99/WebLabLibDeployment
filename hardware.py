import os
import json
import RPi.GPIO as GPIO  # Libreria para GPIO
from laboratory import weblab
from weblablib import weblab_user
import time

#Mapa de los GPIO
mapa = {
    0: 2, 1: 3, 2: 4, 3: 17, 4: 27, 5: 22, 6: 10, 7: 9,
    8: 14, 9: 15, 10: 18, 11: 23, 12: 24, 13: 25, 14: 8, 15: 7
}
botones = {
    0: 5, 1: 6, 2: 13, 3: 19, 4: 26 
} # BTNC, BTNU, BTNL, BTNR, BTND
# Configuracion de los GPIO
GPIO.setmode(GPIO.BCM)  # numeracion BCM
#Establecer pines como salida
for pin in mapa.values():
    GPIO.setup(pin, GPIO.OUT)

#BOTONES
for pin in botones.values():
    GPIO.setup(pin, GPIO.OUT)



@weblab.on_start
def start(client_data, server_data):
    print("Initializing session for {}".format(weblab_user))

    # Se repite para evitar que un usuario herede el estado de otro
    GPIO.setmode(GPIO.BCM)
        
    for pin in mapa.values():
        GPIO.setup(pin, GPIO.OUT)
    #BOTONES
    for pin in botones.values():
        GPIO.setup(pin, GPIO.OUT)

    # Pin a 0 al inicio de la sesion
    for pin in mapa.values():
        GPIO.setup(pin, GPIO.LOW)
    #BOTONES
    for pin in botones.values():
        GPIO.setup(pin, GPIO.LOW)  


@weblab.on_dispose
def dispose():
    print("Disposing session for {}".format(weblab_user))
    clean_resources()
    
    # Limpiamos los GPIO cuando Flask se cierra
    GPIO.cleanup()

def clean_resources():
    print("Cleaning up resources and turning off all lights")
    
    # Apagar las luces 
    for n in range(0, 16):
        switch_light(n, False)

    # Reiniciar el lights.json
    if os.path.exists('lights.json'):
        os.remove('lights.json')

def switch_light(number, state):
    """Turns a specific light on or off and updates the hardware state"""

    # Leer estado actual de las luces
    if not os.path.exists('lights.json'):
        lights = { 'light-{}'.format(n): False for n in range(0, 16) }
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

#BOTONES
def send_pulse():
    """Envia un pulso al GPIO seleccionado"""
    gpio_number = botones.get(0)  # BTNC
    if gpio_number:
        print("Sending pulse to GPIO", gpio_number)
        GPIO.output(gpio_number, GPIO.HIGH)
        time.sleep(0.2)  # Mantiene el pulso por 200 ms
        GPIO.output(gpio_number, GPIO.LOW)
        print("Pulse sent to GPIO", gpio_number)
    else:
        print("Invalid GPIO for pulse")
#

def is_light_on(number):
    """Checks whether a light is on or off"""
    if not os.path.exists('lights.json'):
        return False
    with open('lights.json', 'r') as file:
        return json.load(file).get("light-{}".format(number), False)
