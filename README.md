Requisitos:

Python 3.7 o superior
Pipenv (opcional, pero recomendado)
Git (opcional, para clonar proyectos existentes)
Pasos:

Crear un directorio para su proyecto:
mkdir mi_proyecto_flask
cd mi_proyecto_flask
(Opcional) Crear un entorno virtual con Pipenv:
pipenv install
Instalar Flask y otras dependencias:
pipenv install flask
Crear un archivo app.py con el siguiente código:
Python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hola, mundo!"

if __name__ == "__main__":
    app.run(debug=True)
Usa el código con precaución.
Ejecutar la aplicación:
pipenv run flask run
Abrir un navegador web y acceder a la dirección http://localhost:5000/.
Recursos adicionales:

Documentación oficial de Flask: https://flask.palletsprojects.com/en/2.2.x/
Tutorial de Flask: https://j2logo.com/tutorial-flask-espanol/
Repositorio con ejemplos de proyectos Flask: [se quitó una URL no válida]
Consejos:

Utilice Pipenv para gestionar las dependencias de su proyecto.
Cree un archivo requirements.txt para listar las dependencias de su proyecto.
Use un editor de código con resaltado de sintaxis y detección de errores para escribir su código.
Pruebe su código con frecuencia para detectar errores.
Depure su código utilizando el modo debug de Flask.
Despliegue su aplicación en un servidor web para que otros puedan acceder a ella.
