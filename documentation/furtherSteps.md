## **Desarrollo del esperimento**
Al tener ya configurado el entorno de manera correcta y teniendo los archivos base estructurados, iremos añadiendo y/o elimienando en cada uno de ellos aquellas funciones que sean necesarias para nuestro propósito específico o bien lo cumplan con nuestros requisitos.

### **Implementación de los switches**
Inicialmente se configuran únicamente los switches de la FPGA, para ello se reutilizan las funciones utilizadas en el ejemplo inicial para encender las luces, así como también el archivo *.json*, estos se ajustan ara que sean 16 interruptores, que son los que tiene la Nexys 4 DDR, modelo que estamos utilizando para este experimento.
Además, se implementa el envío de impulsos a través de los GPIO de la Raspberry Pi en la que se ejecuta el servidor. Para poder hace uso de los GPIO se importa la librería `RPi.GPIO` en `hardware.py` y se modifican las funciones necesarias para hacer uso de estos; por ejemplo, en `switch_light` se añade la conmutación del estado del GPIO en función de la lectura del json y también se crea la función `start` donde se procede a la incialización de los GPIO como salida y a nivel bajo.
Adicionalmente se modifica `lab.html` para implementar los switches en la web y se modifica la función `parseStatus` del jacaScrip para contemplar todos los switches y se añade la cuenta regresiva del temporizador.

### **Implementación de los botones**
Al contrario que con los switches, los botones no necesitan conocer su estado anterior ya que simplemente pueden modelarse como un impulso con una duración en milisegundos (se ha ajustado a 200ms pero se podría variar la duración). Por lo que su implementación es más sencilla y no es necesario que se actualice el `.json`. Para su funcionamiento se ha optado por la creación de la función `send_pulse` en `hardware.py` que como su nombre indica se encarga de envíar un pulso de 200ms a través del GPIO deseado, que funciona conjuntamente con la función `pulse` en `laboratory.py`, la función `sendPulse` de `lab.js` y la implementación de los botones en la web en `lab.html`

### **Implementación de la carga del bitstream**
Como trabajo previo al desarrollo de este laboratorio se experimentaron diferentes maneras de cargar el bitstream a la FPGA sin necesidad de grandes interacciones. Inicialmente se probó a cargarlo haciendo uso de un script Batch Tcl pero esto era demasiado lento para implementarlo en un laboratorio por turnos ya que la velocidad del ***Vivado*** a la hora de realizar tareas depende mucho de la potencia de la máquina en la que esté instalado, por otro lado, tampoco es la mejor opción ya que para utilizar este tipo de script es necesario instalar el ***Vivado***y es un programa que ocupa mucho espacio. Finalmente se optó por hacer uso de una herramienta de software libre llamada ***Open FPGA Loader***, esta aplicación es universal ya que es compatible con numerosas placas y cables de transmisión de datos y puede instalarse desde su perfil de github [trabucayre/openFPGALoader](https://github.com/trabucayre/openFPGALoader).
Lo que se ha hecho finalmente ha sido implementar dentro de nuestro laboratorio el script externo que teníamos dentro de una nueva función, `cargar_bitstream_en_fpga`, en `hardware.py`. Para cargar el bitstream lo que se hace es almacenar temporalmente el archivo subido por el usuario y posteriormente elimnarlo una vez se ha completado la carga, de esta manera se evita que se consuman recursos en exceso. Además, para que el usuario pueda interaccionar correctamente con esta carga, en el laboratorio se implementa un botón para subir los archvios, esta interacción se encuentra definida en `lab.html`. Por otro lado, en `laboratory.py` la función `upload_bitstream` se encarga de recibir el `.bit` y enviarlo a través de la función de `hardware.py` a la **FPGA**, a su vez en `lab.js` hay una parte del códig destinada a la carga del bitstream que permite subir el archivo al servidor sin necesidad de recargar la página.

### **Implementación de la cámara en directo**
#### Primer planteamiento (fswebam)
Para poder retrasmitir un vídeo en directo existen múltiples posibilidades, para este laboratorio se ha optado por usar la app open source de `fswebcam` ya que es bastante ligera y aunque no nos permite tener una imagen 100% fluida como sería un streaming, nos ofrece una tasa de refresco de imágenes muy alta teniendo en cuenta que la cámara se encontrará estática y los cambios que queremos ver en la raspberry son "discretos"; deseamos ver cómo cambian los leds y los displays y esto no va a ocurrir en menos de 0.2 segundos, que es la tasa de refresco que configuraremos
Necesitamos instalar `fswebcam` en el lugar donde alojemos el laboratorio, en este caso, la Raspberry Pi. La instalación no es necesaria hacerla dentro de ninguno de nuestros entornos virtuales ya que en estos solo instalaremos las librerías Python y esta es una herramienta del sistema. Para instalarlo simplemente haremos esto en nuestro sistema:
   ```sh
   $ sudo apt install fswebcam
   ```
Luego crearemos una función dentro de `laboratory.py` en la que hacemos una llamada continua a `fswebcam` y con `yield` construimos el vídeo con la secuencia de imágenes capturadas.
##### Conclusiones del primer planteamiento
A pesar de lo ofertado por esta aplicación, se implementó y se comprobó que no era factible su uso, la tasa de refresco es tan baja que no se puede ver ningún cambio en la FPGA ya que pasan varios segundos entre imagen e imagen, por lo que se buscarán alternativas que permitan observar en tiempo real lo que ocurre en la FPGA.
#### Segundo plantemiento (OpenCV)
Como el uso de fswebcam no arrojó los resultados esperados, investigando se encuentran diferentes opciones posibles, la más recomendada en foros es hacer uso de OpenCV, el problema es que OpenCV no funciona en python 2 por lo que hay que hay que hacer uso de la aplicación en un script fuera del entorno virtual del laboratorio,ejecutar el servicio desde fuera también y luego insertar una etiqueta dentro de nuestro laboratorio. El código que hay en el script `camera.py` se adjunto aquí, pero hay que tener en cuenta, como se comentaba antes, que es un archivo que debe de ir fuera del entorno virtual en el que está `Weblablib` o en el que esta `WebLabDeusto`
```py
from flask import Flask, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0) #Select the first camera conected

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

#### Problemas asociados
En un futuro, cuando el laboratorio sea subido a la web habrá que hacer acesible el vídeo y para ello se tendrá que decidir si se sigue haciendo uso de OpenCv combinado con otras herramientas, como por ejemplo una VPN entre servidor y Raspberry Pi o un túnel SSH. También se podría plantear enviar el vídeo en streaming a través de YouTube, esta opción no es muy privada, aunque no debería de ser un problema ya que la imagen que se retransmite no da ningún tipo de información comprometida. 

