from .entities.Evento import Evento
from bson.objectid import ObjectId
from datetime import datetime

class ModelEvento:

    
    @classmethod
    def crear_evento(cls, db, evento):
        try:
            # Insertar el nuevo evento en la base de datos
            db.eventos.insert_one(evento.__dict__)
            return True, "¡Evento creado exitosamente!"
        except Exception as ex:
            return False, str(ex)
        
    @classmethod
    def get_all_eventos(cls, db):
        try:
            # Obtener todos los eventos de la base de datos
            eventos = list(db.eventos.find({}))
            return eventos, "¡Eventos encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)
        
    @classmethod
    def get_all_eventos_by_user(cls, db, user_id):
        try:
            # Buscar todos los eventos que contienen el ID de usuario en el arreglo de usuarios registrados
            eventos = list(db.eventos.find({"usuarios_registrados": user_id}))
            return eventos, "¡Eventos encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)

        
    @classmethod
    def get_evento_by_id(cls, db, id):
        try:
            # Buscar el evento por su ID
            evento = db.eventos.find_one({"_id": ObjectId(id)})
            if evento:
                return Evento(
                    str(evento['_id']),
                    evento.get('nombre', ''),
                    evento.get('resumen', ''),
                    evento.get('fecha', ''),
                    evento.get('fecha_hora_inicio', ''),
                    evento.get('fecha_hora_fin', ''),
                    evento.get('lugar', ''),
                    evento.get('referencias', []),
                    evento.get('aforo', ''),
                    evento.get('duracion_estimada', ''),
                    evento.get('descripcion', ''),
                    evento.get('imagen', ''),
                    evento.get('usuarios_registrados', []),
                    evento.get('estatus_evento', '')
                )
            return None
        except Exception as ex:
            raise Exception(ex)

    #update_evento
    @classmethod
    def update_evento(cls, db, id, evento):
        try:
            # Actualizar el evento en la base de datos
            db.eventos.update_one({"_id": ObjectId(id)}, {"$set": evento.__dict__})
            return True, "¡Evento actualizado exitosamente!"
        except Exception as ex:
            return False, str(ex)
    

    
    @classmethod
    def delete_evento(cls, db, id):
        try:
            # Eliminar el evento de la base de datos
            db.eventos.delete_one({"_id": ObjectId(id)})
            return True, "¡Evento eliminado exitosamente!"
        except Exception as ex:
            return False, str(ex)
    
    @classmethod
    def get_evento_by_id_user(cls, db, id):
        try:
            # Buscar el evento por su ID
            evento = db.eventos.find_one({"_id": ObjectId(id)})
            if evento:
                return Evento(
                    str(evento['_id']),
                    evento.get('nombre', ''),
                    evento.get('resumen', ''),
                    evento.get('fecha', ''),
                    evento.get('fecha_hora_inicio', ''),
                    evento.get('fecha_hora_fin', ''),
                    evento.get('lugar', ''),
                    evento.get('referencias', []),
                    evento.get('aforo', ''),
                    evento.get('duracion_estimada', ''),
                    evento.get('descripcion', ''),
                    evento.get('imagen', ''),
                    evento.get('usuarios_registrados', []),
                    evento.get('estatus_evento', '')
                )
            return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_evento_assist(cls, db, id, evento):
        try:
            # Obtener el evento existente de la base de datos
            evento_existente = db.eventos.find_one({"_id": ObjectId(id)})
            if not evento_existente:
                raise Exception("El evento no existe")

            # Agregar el usuario al arreglo de usuarios registrados
            if evento.usuarios_registrados:
                if 'usuarios_registrados' not in evento_existente:
                    evento_existente['usuarios_registrados'] = []
                evento_existente['usuarios_registrados'].extend(evento.usuarios_registrados)

            # Actualizar el evento en la base de datos
            db.eventos.update_one({"_id": ObjectId(id)}, {"$set": evento_existente})
            return True, "¡Evento actualizado exitosamente!"
        except Exception as ex:
            return False, str(ex)
        
    @classmethod
    def update_cancel_event(cls, db, id):
        try:
            # Actualizar el evento en la base de datos
            db.eventos.update_one({"_id": ObjectId(id)}, {"$set": {"estatus_evento": 1}})
            return True, "¡Evento cancelado exitosamente!"
        except Exception as ex:
            return False, str(ex)
        
    @classmethod
    def get_all_eventos_activos(cls, db):
        try:
            # Obtener todos los eventos activos (estatus_evento = 0) de la base de datos
            eventos_activos = list(db.eventos.find({"estatus_evento": 0}))
            return eventos_activos, "¡Eventos activos encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)
        
    @classmethod
    def get_all_eventos_cancelados(cls, db):
        try:
            # Obtener todos los eventos activos (estatus_evento = 0) de la base de datos
            eventos_activos = list(db.eventos.find({"estatus_evento": 1}))
            return eventos_activos, "¡Eventos activos encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)
        
    @classmethod
    def get_all_eventos_proximos(cls, db):
        try:
            fecha_actual_mexico = datetime.now()
            fecha_formateada = fecha_actual_mexico.strftime("%Y-%m-%d")
            
            eventos_proximos = list(db.eventos.find({"fecha": {"$gte": fecha_formateada}}))
            return eventos_proximos, "¡Eventos próximos encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)
    
