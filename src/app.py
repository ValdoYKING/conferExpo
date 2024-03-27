from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelEvento import ModelEvento

# Entities:
from models.entities.User import User
from models.entities.Evento import Evento

app = Flask(__name__)

csrf = CSRFProtect()
login_manager_app = LoginManager(app)

# Configuración de MongoDB
client = MongoClient('mongodb+srv://valdo_asistencia:asistencia2024@valdodev.iaxsmpm.mongodb.net/asistenciaWeb_2024')
db = client.asistenciaWeb_2024


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario de registro
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        matricula = request.form['matricula']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        motivo_prof = request.form['motivo_prof']
        # Otros campos...

        # Verificar si el nombre de usuario ya está en uso
        if ModelUser.get_by_username(db, username):
            flash('El nombre de usuario ya está en uso. Por favor, elige otro.')
            return redirect(url_for('register'))

        # Crear un nuevo usuario
        new_user = User(username=username, password=password, nombre=nombre, matricula=matricula, telefono=telefono, correo_electronico=correo_electronico, motivo_prof=motivo_prof, rol='usuario')
        # Otros campos...

        # Guardar el nuevo usuario en la base de datos
        ModelUser.register(db, new_user)

        flash('¡Registro exitoso! Por favor, inicia sesión.')
        return redirect(url_for('login'))
    else:
        return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user:
            login_user(logged_user)
            if logged_user.rol == 'administrador': 
                return redirect(url_for('homeAdmin'))
            elif logged_user.rol == 'usuario':
                return redirect(url_for('homeUser'))
            else:
                flash("Usuario o contraseña no válidos")
                return render_template('auth/login.html')
        else:
            flash("Usuario o contraseña no válidos")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/homeUser')
@login_required
def homeUser():
    return render_template('userConferExpo/homeUser.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# Rutas para administrador 
@app.route('/homeAdmin')
@login_required
def homeAdmin():
    return render_template('adminUser/homeAdmin.html')

@app.route('/newEvent')
@login_required
def newEvent():
    return render_template('adminUser/newEvent.html')

def allowed_file(filename):
    allowed_extensions = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/registerEvent', methods=['GET', 'POST'])
@login_required
def registerEvent():
    if request.method == 'POST':
        # Obtener los datos del formulario de registro
        nombre = request.form['eventName']
        resumen = request.form['resumeEvent']
        fecha = request.form['dateEvent']
        fecha_hora_inicio = request.form['starHour']
        fecha_hora_fin = request.form['finishHour']
        lugar = request.form['addressEvent']
        referencias = request.form['referencesAddress']
        aforo = request.form['aforo']
        duracion_estimada = request.form['duracion_estimada']
        descripcion = request.form['descriptionEvent']
        
        # Verificar si se ha proporcionado una imagen
        if 'imagen' not in request.files:
            flash('No se ha proporcionado ninguna imagen')
            return redirect(request.url)
        
        imagen = request.files['imagen']

        
        # Verificar si la imagen tiene un nombre de archivo válido
        if imagen.filename == '':
            flash('No se ha seleccionado ningún archivo')
            return redirect(request.url)
        
        if imagen and allowed_file(imagen.filename):
            # Se asegura que el nombre del archivo sea seguro
            filename = secure_filename(imagen.filename)
            # Se guarda la imagen en la carpeta deseada
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('El formato de archivo de imagen no es válido')
            return redirect(request.url)
        
        # Crear un nuevo evento
        new_event = Evento(
            nombre=nombre,
            resumen=resumen,
            fecha = fecha,
            fecha_hora_inicio=fecha_hora_inicio,
            fecha_hora_fin=fecha_hora_fin,
            lugar=lugar,
            referencias=referencias,
            aforo=aforo,
            duracion_estimada=duracion_estimada,
            descripcion=descripcion,
            imagen=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )

        # Guardar el nuevo evento en la base de datos
        success, message = ModelEvento.crear_evento(db, new_event)

        if success:
            flash(message)
            return redirect(url_for('homeAdmin'))
        else:
            flash(message, 'error')
            return redirect(url_for('registerEvent'))
    else:
        return render_template('adminUser/newEvent.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>This is a protected view, only for authenticated users.</h1>"

@app.route('/test')
def test():
    return render_template('error/404.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return render_template('error/404.html'),404

def status_500(error):
    return render_template('error/500.html'),500

def status_503(error):
    return render_template('error/503.html'),503


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
