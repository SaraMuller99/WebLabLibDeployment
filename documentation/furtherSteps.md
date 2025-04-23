## **Desarrollo del esperimento **
Al tener ya configurado el entorno de manera correcta y teniendo los archivos base estructurados, iremos añadiendo y/o elimienando en cada uno de ellos aquellas funciones que sean necesarias para nuestro propósito específico o bien lo cumplan con nuestros requisitos.

### **Implementación de los switches**
Inicialmente se configuran únicamente los switches de la FPGA, para ello se reutilizan las funciones utilizadas en el ejemplo inicial para encender las luces, así como también el archivo *.json*, estos se ajustan ara que sean 16 interruptores, que son los que tiene la Nexys 4 DDR, modelo que estamos utilizando para este experimento.
Además, se implementa el envío de impulsos a través de los GPIO de la Raspberry Pi en la que se ejecuta el servidor. Para poder hace uso de los GPIO se importa la librería *RPi.GPIO* en *hardware.py* y se modifican las funciones necesarias para hacer uso de estos; por ejemplo, en *switch_light* se añade la conmutación del estado del GPIO en función de la lectura del json y también se crea la función *start* donde se procede a la incialización de los GPIO como salida y a nivel bajo.
Adicionalmente se modifica el *.html* para implementar los switches en la web y se modifica la función *parseStatus* del jacaScrip para contemplar todos los switches y se añade la cuenta regresiva del temporizador.

### **Implementación de los botones**
Al contrario que con los switches, los botones no necesitan conocer su estado anterior ya que simplemente pueden modelarse como un impulso con una duración en milisegundos (se ha ajustado a 200ms pero se podría variar la duración). Por lo que su implementación es más sencilla y no es necesario que se actualice el *.json*. Para su funcionamiento se ha optado por la creación de la función *send_pulse* en *hardware.py* que como su nombre indica se encarga de envíar un pulso de 200ms a través del GPIO deseado, que funciona conjuntamente con la función *pulse* en *laboratory.py*, la función *sendPulse* de *lab.js* y la implementación de los botones en la web en *lab.html*

### **Implementación de la carga del bitstream**

### **Implementación de la cámara en directo**
Para poder hacer uso de la cámara en Flask es necesario instalar *fswebcam* en el lugar donde alojemos el laboratorio, en este caso, la Raspberry Pi. La instalación no es necesaria hacerla dentro de ninguno de nuestros entornos virtuales ya que en estos solo instalaremos las librerías Python y esta es una herramienta del sistema.

*fswebcam* es un programa que nos permite tomar imágenes utilizando una webcam usb conectada a la máquina donde estamos corrienod nuestro laboraotorio. Para instalarlo simplemente haremos esto en nuestro sistema:
   ```sh
   $ sudo apt install fswebcam
   ```
