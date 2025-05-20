# Instalación

## Introducción
El objetivo de este documento es proporcionar información suficiente para realizar correctamente la instalación de las herramientas necesarias para poder desarrollar un laboratorio y experimentos con **WebLab-Deusto** y **WebLabLib**. La instalación está guiada para sistemas basados en Ubuntu y Debian, por lo que si se pretende hacer la instalación en un sistema diferente, el usuario deberá tomar las consideraciones necesarias.

Lo primero que vamos a hacer es preparar el entorno para así poder realizar las instalaciones con el menor número de conflictos posibles. Pero antes de nada, debemos comprender en qué consisten cada una de las herramientas:

**WebLab-Deusto** es una plataforma de código abierto para la gestión de laboratorios remotos, es quien nos permitirá acceder a través del laboratorio a la FPGA. Incorpora funcionalidades como autenticación, control de acceso, programación de sesiones y administración de recursos. A parte de laboratorios, **WebLab-Deusto** también permite la creación de experimentos, pero en este caso no será utilizado con ese fin ya que en un primer acercamiento se obtuvieron errores relativos a la conexión del servidor en una librería por lo que se consideró que **WebLabLib** sería una herramienta más adecuada para el desarrollo final. En resumen, **Weblab-Deusto** se encargará de realizar la gestión de usuarios y sesiones. 

**WebLabLib** es una biblioteca en python que facilita la creación de laboratorios no gestionados en **WebLab-Deusto**. Se basa en **Flask** y ofrece herramientas para manejar la autenticación, la comunicación con el servidor y la gestión de sesiones de los usuarios. Su principal ventaja es que permite desarrollar laboratorios personalizados sin depender de la infraestructura de **WebLab-Deusto**, lo que da mayor flexibilidad a la hora de diseñar el sistema. Al estar basado en **Flask**, proporciona una estructura sencilla para definir rutas y manejar peticiones HTTP, además de integrar **Flask-SocketIO** para la comunicación en tiempo real y **Flask-SQLAlchemy** para gestionar bases de datos de forma eficiente.  

Al final, tendremos un laboratorio desarrollado en **WebLab-Deusto** que estará desplegado inicialmente en la dirección local localhost/8000 y por otro lado tendremos un experimento desarrollado con **WebLabLib**, vinculado con el laboratorio y desplegado en otra dirección local localhost/5000.

## Instalación de *WebLab* y *WebLabLib* 
Antes de comenzar la instalación, y como seran necesarias para poder hacerla debemos verificar que nuestro sistema tiene instalado **pip**, el cual es un gestor de paquetes de sowtware de python. Además, debido a las particulares de **WebLab**, asociadas a la antiguedad del software, debemos de crear un entorno virtual donde lo instalaremos, por lo que es necesario que tengamos instalado **virtualenv**. Para instalarlos haremos:

```bash
$ sudo apt-get install python-pip
$ sudo apt-get install virtualenv
```

Un entorno virtual, en el contexto de python, es un entorno aislado donde podemos trabajar y gestionar las dependencias del proyecto sin afectar a los demás, lo cuál es necesario en este caso ya que **WebLab** funciona en python 2.7, una versión obsoleta de python.

### *WebLab*
Como ya tenemos *virtualenv* instalado, crearemos un entono virtual y accederemos a él, este entorno debemos asegurarnos de crearlo forzando el uso de **python 2.7**, que es la versión de python en la que funciona **WebLab**. A partir de ahora, todo lo que hagamos será dentro del entorno virtual.
``` bash
$ mkvirtualenv --python=/usr/bin/python2.7 weblab
$ workon weblab
```
Una vez tengamos el entorno virtual creado, haremos el clonado del repositorio de **WebLab** y nos desplazaremos a la carpeta que se ha creado, para así proceder a la instalación, que la haremos mediante la ejecución de un script incluido en el repositorio clonado.
``` bash
$ git clone https://github.com/weblabdeusto/weblabdeusto.git weblab
$ cd WHEREVER-IS-WEBLAB
$ python setup.py install
```

### *WebLabLib*
Aunque no es explícitamente necesario porque **WebLabLib** es compatible con python 3, sigue siendo una buena práctica crear entornos virtuales para las diferentes cosas que instalemos, por lo que crearemos un entorno virtual también para él y accederemos a él.
``` bash
$ mkvirtualenv weblablib
$ workon weblablib
```
Y ahora, dentro de este entorno instalamos la librería de **WebLabLib**.
``` bash
$ pip install weblablib
```
Para poder desarrollar nuestro experimento es necesario que tengamos instalado **Flask**, este es un microframework que permite crear con python aplicaciones web, y es el que se utilizará en el desarrollo de nuestros experimentos. Existen frameworks más complejos, como Django, pero para el tipo de aplicación que vamos a desarrollar no es necesario. 
Como nota informativa, y en caso de que el ussuario que esté leyendo esto no lo sepa, u
``` bash 
$ pip install flask
```

Además, WebLabLib depende de Redis, necesario para la gestión de los datos de usuario, por lo que lo instalaremos también:
``` bash
$ sudo apt-get install redis-server
```

### Resolución de problemas
Aquí se detalla como resolver diferentes problemas que se han encontrado al realizar la instalación en una *Raspberry Pi 400* con *Debian 11* (Bullseye)
#### mkvirtualenv
Al ejecutar *mkvirtualenv* nos encontramos con que la respuesta de la terminal es *"mkvirtualenv command not found"*. Esto se debe a que tenemos que añadirlo al archivo `.bashrc`, por lo que escribiremos al final de él:
``` bash
export PATH="$HOME/.local/bin:$PATH"
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
source /home/sara/.local/bin/virtualenvwrapper.sh #Sustituye "sara" por tu usuario
```
## Despliegue
Como el desarrollo del experimento es "independiente" del laboratorio, se recomienda consultar primeramente el documento WebLabLib.md y una vez se tenga la base del experimento y quiera probar su funcionamiento consultar WebLabDeusto.md

En ambos documentos se explica la estructura de cada uno y cómo se han utilizado para el desarrollo en concreto de este proyecto.

### **Prueba del Proyecto** 
Para comprobar que se han generado los despliegues de manera correcta y que además se comunican entre sí como debe ser, haremos, en terminales distintas:

Por un lado en el entorno virtual de **WebLabLib** y en la ruta donde se encuentra el experimento:

``` bash
$ export FLASK_DEBUG=1
$ export FLASK_APP=laboratory.py
$ flask run
```  
Por otro, en el entorno virtual de **WebLab** y en la ruta donde se haya creado nuestro laboratorio:

``` bash
$ weblab-admmin start example
```
Accederemos en el navegador a la dirección que hayamos configurado, *localhost/1000* de manera predeterminada, inicicamos sesión con las credenciales de administrador y comprobamos que se nos permite reservar posición en la cola del experimento.

