from flask import Flask, request, render_template, jsonify, url_for

from weblablib import WebLab, weblab_user
from weblablib import requires_active, requires_login
from weblablib import poll

#For the pulse
import time  

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'something-random',
    'WEBLAB_CALLBACK_URL': '/mycallback',
    'WEBLAB_USERNAME': 'weblabdeusto',
    'WEBLAB_PASSWORD': 'secret',
    'WEBLAB_AUTOPOLL': 'False',
})

weblab = WebLab(app)

@weblab.initial_url
def initial_url():
    return url_for('index')

@app.route('/')
@requires_login
def index():
    return render_template("lab.html")

@app.route('/status')
@requires_active
def status():
    return jsonify(lights=get_light_status(),
                   time_left=weblab_user.time_left,
                   error=False)

@app.route('/poll')
@requires_active
def poll():
    poll()
    return jsonify(result='ok')

@app.route('/lights/<int:number>/')
@requires_active
def light(number):
    state = request.args.get('state') == 'true'
    hardware.switch_light(number, state)
    return jsonify(lights=get_light_status(), error=False)

def get_light_status():
    lights = {}
    for light in range(0, 16):
        lights['light-{}'.format(light)] = hardware.is_light_on(light)
    return lights

# Buttons
@app.route('/pulse/<int:pin_id>')
@requires_active
def pulse(pin_id):
    print("[DEBUG] Received petition in /pulse/")
    hardware.send_pulse(pin_id)
    return jsonify(result="Pulse sent", error=False)
#
import hardware
@app.cli.command('clean-resources')
def clean_resources_command():
    hardware.clean_resources()