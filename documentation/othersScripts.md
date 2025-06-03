# Creación de un archivo de configuración y scripts adicionales
Se ha creado un archivo de configuración `config.ini` para no tener que modificar el código cada vez que se quieran cambiar parámetros que son susceptibles de ser modificados con más frecuencia. Este se encuentra localizado en la carpeta `shared-config` al mismo nivel que las carpetas del despliegue de WeblabDeusto y WebLabLib:

```
/project-root
├── 📁 `deployments/`
│   └── 📁 sample/              → Weblab-Deusto
├── 📁 `weblablib-stuff/`       → Weblablib
│   └── 📁 ...            
├── `shared-config`/
│   └── 📄 config.ini           → Archivo de configuración que contiene los parámetros
│   └── 📄 update_yml.py.md     → scrit en python auxiliar para modificar configuration.yml
├── 📄 `run_all.sh/`
```
El otro archivo que encontramos es un script en python auxiliar necesario para poder modificar los parámetros de configuration.yml ya que no es posible importar un módulo en este tipo de archivos, el formato YAML es una estructura de datos estática que no tiene capacidad para ejecutar python, importar o leer otros archivos por sí mismo.

También se ha readcreado el bash script `run_all.sh`, este se encarga de ejecutar una serie de comandos por consola que permiten poder realizar las ejecuciones de los despliegues de WeblabDeusto y WebLabLib en cada uno de sus entornos virtuales y de la cámara del laboratorio por separado, en una terminal distinta cada uno, pero sin necesidad de ir manualmente uno por uno. También se encarga de ejecutar el scrit en Python responsable de actualizar `configuration.yml`, acción que evidentementerealiza previamente a lanzar los despliegues.

A continuación se adjuntan los códigos de estos nuevos archivos:

## confing.ini
``` ini
[WEBLAB]
username = weblabdeusto
password = secret

[EXPERIMENT]
url = http://localhost:5000

[TEMPLATE]
html = lab.html
```
## update_yml.py
``` py
import ConfigParser
import yaml
import os

#Read config.ini
ini_path = os.path.expanduser('~/shared-config/config.ini')
config = ConfigParser.ConfigParser()
config.read(ini_path)

username = config.get('WEBLAB', 'username')
password = config.get('WEBLAB', 'password')
url = config.get('EXPERIMENT', 'url')

#Read configuration.yml
yml_path = os.path.expanduser('~/deployments/sample/configuration.yml')
with open(yml_path, 'r') as f:
    data = yaml.safe_load(f)

#Change fields
electronics = data['hosts']['core_host']['processes']['laboratory1']['components']['electronics']['config']
electronics['http_experiment_username'] = username
electronics['http_experiment_password'] = password
electronics['http_experiment_url'] = url

#Save changes
with open(yml_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

print("configuration.yml update from  config.ini.")
```
## run_all.sh
``` sh
#!/bin/bash

# --- Update configuration.yml ---
bash -c "source /home/sara/.virtualenvs/weblab_env/bin/activate && python /home/sara/shared-config/update_yml.py"

# --- WebLab-Deusto ---
lxterminal --title="WebLab-Deusto" --working-directory=/home/sara/deployments \
  --command="bash -c 'source /home/sara/.virtualenvs/weblab_env/bin/activate && weblab-admin start sample; exec bash'" &

# --- Weblab Camera ---
lxterminal --title="WeblabCamera" --working-directory=/home/sara/WeblabCamera \
  --command="bash -c 'python3 camera.py; exec bash'" &

# --- WebLabLib app ---
lxterminal --title="WebLabLib" --working-directory=/home/sara/weblablib-stuff \
  --command="bash -c 'source /home/sara/.virtualenvs/weblablib/bin/activate && export FLASK_DEBUG=1 && export FLASK_APP=laboratory.py && flask run; exec bash'" &

echo "Todas las 'aplicaciones' lanzadas"

```