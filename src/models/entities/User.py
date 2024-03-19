from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):

    def __init__(self, id=None, username=None, password=None, nombre="", matricula=None, telefono=None, correo_electronico=None, eventos_asistidos=None, motivo_prof=""):
        self.id = id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.matricula = matricula
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.eventos_asistidos = eventos_asistidos or []
        self.motivo_prof = motivo_prof

    @classmethod
    def hash_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
