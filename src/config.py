from pymongo import MongoClient

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://valdo_asistencia:asistencia2024@valdodev.iaxsmpm.mongodb.net/asistenciaWeb_2024'
    }

config = {
    'development': DevelopmentConfig
}
