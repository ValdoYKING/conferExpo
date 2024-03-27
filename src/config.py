from pymongo import MongoClient
import os

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'
    UPLOAD_FOLDER = 'public/imgEvent'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://valdo_asistencia:asistencia2024@valdodev.iaxsmpm.mongodb.net/asistenciaWeb_2024'
    }

    # Define la carpeta de carga de archivos
    # UPLOAD_FOLDER = os.path.join(os.getcwd(), 'public/imgEvent')
    UPLOAD_FOLDER = 'public/imgEvent'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

config = {
    'development': DevelopmentConfig
}
