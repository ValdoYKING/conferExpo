from pymongo import MongoClient
import os

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'
    # Modificar la ruta de la carpeta de carga para que sea absoluta
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'public/imgEvent'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://valdo_asistencia:asistencia2024@valdodev.iaxsmpm.mongodb.net/asistenciaWeb_2024'
    }

config = {
    'development': DevelopmentConfig
}
