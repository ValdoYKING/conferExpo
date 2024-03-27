from .entities.Evento import Evento
from bson.objectid import ObjectId

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
    def obtener_evento_por_id(cls, db, evento_id):
        try:
            # Convertir la cadena de ID en un ObjectId de MongoDB
            object_id = ObjectId(evento_id)
            # Buscar evento por ID en MongoDB
            result = db.eventos.find_one({"_id": object_id})
            if result:
                # Si se encuentra el evento, se crea un objeto Evento y se devuelve
                return Evento(
                    str(result['_id']),
                    result['nombre'],
                    result['resumen'],
                    result['fecha'],
                    result['fecha_hora_inicio'],
                    result['fecha_hora_fin'],
                    result['lugar'],
                    result['referencias'],
                    result['aforo'],
                    result['duracion_estimada'],
                    result['descripcion'],
                    result['imagen']
                )
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_eventos(cls, db):
        try:
            # Obtener todos los eventos de la base de datos
            eventos = db.eventos.find()
            lista_eventos = []
            for evento in eventos:
                lista_eventos.append(Evento(
                    str(evento['_id']),
                    evento['nombre'],
                    evento['resumen'],
                    result['fecha'],
                    evento['fecha_hora_inicio'],
                    evento['fecha_hora_fin'],
                    evento['lugar'],
                    evento['referencias'],
                    evento['aforo'],
                    evento['duracion_estimada'],
                    evento['descripcion'],
                    evento['imagen']
                ))
            return lista_eventos
        except Exception as ex:
            raise Exception(ex)
