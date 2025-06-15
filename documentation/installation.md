# Instalación

## Introducción
El objetivo de este documento es proporcionar información suficiente para realizar correctamente la instalación de las herramientas necesarias para poder desarrollar un laboratorio y experimentos con **WebLab-Deusto** y **WebLabLib**. La instalación está guiada para sistemas basados en Ubuntu y Debian, por lo que si se pretende hacer la instalación en un sistema diferente, el usuario deberá tomar las consideraciones necesarias.

Lo primero que se hace es preparar el entorno para así poder realizar las instalaciones con el menor número de conflictos posibles. Pero antes de nada, debemos comprender en qué consisten cada una de las herramientas:

**WebLab-Deusto** es una plataforma de código abierto para la gestión de laboratorios remotos, también conocida como RMLS *(Remote Management Laboratory System)*, es lo que nos permite acceder a través del laboratorio a la FPGA, proporcionando además una interfaz amigable con el usuario y el administrador, de modo que la gestión sea más cómoda. Incorpora aquellas funcionalidades que permiten una correcta gestión de los usuarios, como el control de acceso o la administración de roles, además incluye la reserva de tiempos para así evitar conflictos entre usuarios al tratarse de un laboratorio físico que solo soporta un usuario al momento, también permite programar las sesiones; en resumen, se encarga de administrar todos los recursos. A parte de laboratorios, **WebLab-Deusto** también permite la creación de experimentos, pero en este caso no es utilizado con ese fin ya que en un primer acercamiento se obtuvieron errores en una librería relativos a la conexión del servidor, por lo que se consideró que **WebLabLib** sería una herramienta más adecuada para el desarrollo final. En resumen, **Weblab-Deusto** se encargará de realizar la gestión de usuarios y sesiones. 

**WebLabLib** es una librería en python que facilita la creación de laboratorios no gestionados en **WebLab-Deusto** de una manera estructurada y sencilla. Se basa en **Flask**, esto permite que se pueda lanzar un servidor local web para enviar y recibir las peticiones desde **WebLab-Deusto**. Su principal ventaja es que permite desarrollar laboratorios personalizados sin depender de la infraestructura de **WebLab-Deusto**, lo que da mayor flexibilidad a la hora de diseñar el sistema; además, su diseño modular permite definir el comportamiento del laboratorio mediante clases y métodos que van desde procesar comandos hasta gestionar el inicio y fin de sesiones.  Al estar basado en **Flask**, proporciona una estructura sencilla para definir rutas y manejar peticiones HTTP, además permite integrar herramientas más avanzadas como **Flask-SocketIO** para la comunicación en tiempo real o **Flask-SQLAlchemy** para gestionar bases de datos de forma eficiente, gracias a su flexibilidad el sistema puede refinarse tanto como quiera el usuario.  

Al final, tendremos un laboratorio desarrollado en **WebLab-Deusto** que estará desplegado inicialmente en la dirección local localhost/8000 y por otro lado tendremos un experimento desarrollado con **WebLabLib**, vinculado con el laboratorio y desplegado en otra dirección local localhost/5000.

## Instalación de *WebLab* y *WebLabLib* 
Antes de comenzar la instalación, y como serán necesarias para poder hacerla se debe verificar que el sistema tiene instalado **pip**, el cual es un gestor de paquetes de software de python. Además, debido a las particulares de **WebLab**, asociadas a la antigüedad del software, se debe crear un entorno virtual donde instalarlo, por lo que es necesario tener **virtualenv**. Para instalarlos haremos:

```bash
$ sudo apt-get install python-pip
$ sudo apt-get install virtualenv
```

Un entorno virtual, en el contexto de python, es un entorno aislado donde se puede trabajar y gestionar las dependencias del proyecto sin afectar a los demás, lo cuál es necesario en este caso ya que **WebLab** funciona en python 2.7, una versión obsoleta de python.

### *WebLab*
Teniendo *virtualenv* instalado, se crea un entono virtual y se accede a él, este entorno hay que crearlo forzando el uso de **python 2.7**, que es la versión de python en la que funciona **WebLab**. A partir de ahora, todo lo que se haga será dentro del entorno virtual.
``` bash
$ mkvirtualenv --python=/usr/bin/python2.7 weblab
$ workon weblab
```
Una vez esté el entorno virtual creado, se clona el repositorio de **WebLab** y se accede al directorio creado, para así proceder a la instalación, que se hace mediante la ejecución de un script incluido en el repositorio clonado.
``` bash
$ git clone https://github.com/weblabdeusto/weblabdeusto.git weblab
$ cd WHEREVER-IS-WEBLAB
$ python setup.py install
```

### *WebLabLib*
Aunque no es explícitamente necesario porque **WebLabLib** es compatible con python 3, sigue siendo una buena práctica crear entornos virtuales para las diferentes aplicaciones instaladas, por lo que crearemos un entorno virtual también para él y accederemos a él.
``` bash
$ mkvirtualenv weblablib
$ workon weblablib
```
Y ahora, dentro de este entorno se instala la librería de **WebLabLib**.
``` bash
$ pip install weblablib
```
Para poder desarrollar el experimento es necesario que esté instalado **Flask**, este es un microframework que permite crear con python aplicaciones web, y es el que se utiliza en el desarrollo del experimentos. Existen frameworks más complejos, como Django, pero para el tipo de aplicación que vamos a desarrollar no es necesario. 
``` bash 
$ pip install flask
```

Además, WebLabLib depende de Redis, necesario para la gestión de los datos de usuario, por lo que lo que se instala también:
``` bash
$ sudo apt-get install redis-server
```

### Resolución de problemas
Aquí se detalla cómo resolver diferentes problemas que se han encontrado al realizar la instalación en una *Raspberry Pi 400* con *Debian 11* (Bullseye)
#### mkvirtualenv
Al ejecutar *mkvirtualenv* naparece la siguiente respuesta de la terminal: *"mkvirtualenv command not found"*. Esto se debe a que hay que añadirlo al archivo `.bashrc`, por lo que se escribe al final de él:
``` bash
export PATH="$HOME/.local/bin:$PATH"
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
source /home/sara/.local/bin/virtualenvwrapper.sh #Sustituye "sara" por tu usuario
```
## Despliegue
Como el desarrollo del experimento es "independiente" del laboratorio, se recomienda consultar primeramente el [readme de WebLabLib](WebLabLib.md) y una vez se tenga la base del experimento y quiera probar su funcionamiento consultar el [readme de WebLabDeusto](WebLabDeusto.md)

En ambos documentos se explica la estructura de cada uno y cómo se han utilizado para el desarrollo en concreto de este proyecto.

## **Prueba del Proyecto** 
Para comprobar que se han generado los despliegues de manera correcta y que además se comunican entre sí como debe ser, se ejecuta, en terminales distintas:

Por un lado en el entorno virtual de **WebLabLib** y en la ruta donde se encuentra el experimento:

``` bash
$ export FLASK_DEBUG=1
$ export FLASK_APP=laboratory.py
$ flask run
```  
Por otro, en el entorno virtual de **WebLab** y en la ruta donde se haya creado el laboratorio:

``` bash
$ weblab-admmin start example
```
Se accede en el navegador a la dirección configurada, *localhost/1000* de manera predeterminada, se inicia sesión con las credenciales de administrador y se comprueba que se nos permite reservar posición en la cola del experimento y acceder a él.

