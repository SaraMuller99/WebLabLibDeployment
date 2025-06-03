#-----------------------------------Backend----------------------------------- 

#CONFIGURATION FILE
import ConfigParser as configparser
import os

CONFIG_PATH= os.path.expanduser('~/shared-config/config.ini')
config = configparser.ConfigParser()
config.read(CONFIG_PATH)


from flask import Flask, request, render_template, jsonify, url_for, Response

from weblablib import WebLab, weblab_user
from weblablib import requires_active, requires_login
from weblablib import poll

#Initialize Flask and configure WebLab Parameters
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'something-random',
    'WEBLAB_CALLBACK_URL': '/mycallback',
    'WEBLAB_USERNAME': config.get('WEBLAB', 'username'),
    'WEBLAB_PASSWORD': config.get('WEBLAB', 'password'),
    'WEBLAB_AUTOPOLL': 'False',
})
#WebLab object instance
weblab = WebLab(app)

@weblab.initial_url
def initial_url():
    return url_for('index')

#Load html web template
@app.route('/')
@requires_login
def index():
    return render_template(config.get('TEMPLATE', 'html'),)

#Shows status: Switches and time left
@app.route('/status')
@requires_active
def status():
    return jsonify(sw=get_switch_status(),
                   time_left=weblab_user.time_left,
                   error=False)

#Keeps sesion open
@app.route('/poll')
@requires_active
def poll():
    poll()
    return jsonify(result='ok')

#TURN ON AND OFF SWITCHES
#Change switch status using hardware.py
@app.route('/sw/<int:number>/')
@requires_active
def switch(number):
    state = request.args.get('state') == 'true'
    hardware.switch_switches(number, state)
    return jsonify(sw=get_switch_status(), error=False)

#Get switch state using hardware.py
def get_switch_status():
    sw = {}
    for switch in range(0, 16):
        sw['switch-{}'.format(switch)] = hardware.is_switch_on(switch)
    return sw

#BUTTONS
#Send the pulse using hardware.py
@app.route('/pulse/<int:pin_id>')
@requires_active
def pulse(pin_id):
    print("[DEBUG] Received petition in /pulse/")
    hardware.send_pulse(pin_id)
    return jsonify(result="Pulse sent", error=False)

#CLEANING
#Defines CLI comand to use the function from hardware.py in console
import hardware
@app.cli.command('clean-resources')
def clean_resources_command():
    hardware.clean_resources()

#UPLOAD BITSTREAM
@app.route('/upload-bitstream', methods=['POST'])
@requires_active
def upload_bitstream():
    #Receive the bitstream file
    bitstream = request.files.get('bitstream')
    if not bitstream:
        return jsonify(ok=False, mensaje="No se ha enviado un archivo .bit.")

    #Use the content (in bytes) of the file as parameter to the hardware.py function
    from hardware import upload_bitstream  #Import function from hardware.py
    resultado = upload_bitstream(bitstream.read())

    #Send from hardware.py if the result was success
    return jsonify(ok=resultado["exito"], mensaje=resultado["mensaje"])
