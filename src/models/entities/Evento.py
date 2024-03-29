from bson.objectid import ObjectId
from datetime import datetime

class Evento:
    def __init__(self,id=None, nombre=None, resumen=None, fecha=None, fecha_hora_inicio=None, fecha_hora_fin=None, lugar=None, referencias=None, aforo=None, duracion_estimada=None, descripcion=None, imagen=None, usuarios_registrados=None):
        self.id = id
        self.nombre = nombre
        self.resumen = resumen
        self.fecha = fecha
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.lugar = lugar
        self.referencias = referencias
        self.aforo = aforo
        self.duracion_estimada = duracion_estimada
        self.descripcion = descripcion
        self.imagen = imagen
        self.usuarios_registrados = usuarios_registrados or []  # Inicializa usuarios_registrados como una lista vacía

    def registrar_usuario(self, user_id):
        self.usuarios_registrados.append(user_id)

    def __str__(self):
        return f"Evento: {self.nombre}, Fecha y hora de inicio: {self.fecha_hora_inicio}, Lugar: {self.lugar}"

