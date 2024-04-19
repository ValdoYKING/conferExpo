from .entities.User import User
from bson.objectid import ObjectId
from .ModelEvento import ModelEvento

class ModelUser():

    @classmethod
    def login(cls, db, user):
        try:
            # Buscar usuario por nombre de usuario en MongoDB
            result = db.usuarios.find_one({"username": user.username})
            if result:
                # Si se encuentra el usuario, se verifica la contraseña
                if User.check_password(result['password'], user.password):
                    # Si la contraseña es correcta, se crea un objeto User y se devuelve
                    return User(
                        str(result['_id']),
                        result['username'],
                        None,  # Se debe cambiar este valor para manejar correctamente la contraseña
                        result.get('nombre', ''),  # Manejo de nuevo atributo
                        result.get('matricula', ''),  # Manejo de nuevo atributo
                        result.get('telefono', ''),  # Manejo de nuevo atributo
                        result.get('correo_electronico', ''),  # Manejo de nuevo atributo
                        result.get('eventos_asistidos', []),  # Manejo de nuevo atributo
                        result.get('motivo_prof', ''),  # Manejo de nuevo atributo
                        result.get('rol', 'usuario'),  # Manejo del nuevo atributo de rol
                        result.get('eventos_por_assistir', []),  # Manejo del nuevo atributo de eventos_por_assistir
                    )
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, db, id):
        try:
            # Convertir la cadena de ID en un ObjectId de MongoDB
            object_id = ObjectId(id)
            # Buscar usuario por ID en MongoDB
            result = db.usuarios.find_one({"_id": object_id})
            if result:
                # Si se encuentra el usuario, se crea un objeto User y se devuelve
                return User(
                    str(result['_id']),
                    result['username'],
                    None,  # Se debe cambiar este valor para manejar correctamente la contraseña
                    result.get('nombre', ''),  # Manejo de nuevo atributo
                    result.get('matricula', ''),  # Manejo de nuevo atributo
                    result.get('telefono', ''),  # Manejo de nuevo atributo
                    result.get('correo_electronico', ''),  # Manejo de nuevo atributo
                    result.get('eventos_asistidos', []),  # Manejo de nuevo atributo
                    result.get('motivo_prof', ''),  # Manejo de nuevo atributo
                    result.get('rol', 'usuario'),  # Manejo del nuevo atributo de rol
                    result.get('eventos_por_assistir', [])  # Manejo del nuevo atributo de eventos_por_assistir
                )
            return None
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def get_by_username(cls, db, username):
        # Buscar usuario por nombre de usuario en MongoDB
        return db.usuarios.find_one({"username": username})

    @classmethod
    def get_by_email(cls, db, correo_electronico):
        # Buscar usuario por correo electrónico en MongoDB
        return db.usuarios.find_one({"correo_electronico": correo_electronico})    
        
    @classmethod
    def register(cls, db, user):
        try:
            # Verificar si el nombre de usuario ya está en uso
            existing_user = db.usuarios.find_one({"username": user.username})
            if existing_user:
                return False, "El nombre de usuario ya está en uso. Por favor, elige otro."

            # Encriptar la contraseña antes de guardarla
            hashed_password = User.hash_password(user.password)
            user.password = hashed_password

            # Insertar el nuevo usuario en la base de datos
            db.usuarios.insert_one(user.__dict__)

            return True, "¡Registro exitoso! Por favor, inicia sesión."
        except Exception as ex:
            return False, str(ex)
    
    @classmethod
    def update_eventos_asistidos(cls, db, user_id, event_id):
        try:
            # Convertir el user_id en ObjectId de MongoDB
            user_object_id = ObjectId(user_id)

            # Actualizar el arreglo eventos_asistidos del usuario
            result = db.usuarios.update_one(
                {'_id': user_object_id},
                {'$addToSet': {'eventos_asistidos': event_id}}
            )

            return result.modified_count == 1
        except Exception as ex:
            print("Error al actualizar eventos asistidos:", ex)
            return False
    
    @classmethod
    def busca_evento_usuario(cls, db, user_id, event_id):
        try:
            # Convertir el user_id en ObjectId de MongoDB
            user_object_id = ObjectId(user_id)
    
            # Realizar una consulta para encontrar al usuario por su ID
            user = db.usuarios.find_one({'_id': user_object_id})
    
            # Verificar si el usuario existe
            if user:
                # Verificar si el evento ya está en la lista de eventos asistidos del usuario
                if event_id in user.get('eventos_asistidos', []):
                    return True  # El evento ya está en la lista de eventos asistidos del usuario
                else:
                    return False  # El evento no está en la lista de eventos asistidos del usuario
            else:
                return False  # El usuario no existe en la base de datos
    
        except Exception as ex:
            print("Error al buscar evento para usuario:", ex)
            return False
        
    @classmethod
    def update_usuario_assist(cls, db, user_id, event_id):
        try:
            # Obtener al usuario por su ID
            user = cls.get_by_id(db, user_id)
            if not user:
                raise Exception("El usuario no existe")

            # Agregar el ID del evento a la lista de eventos por asistir del usuario
            if event_id not in user.eventos_por_assistir:
                user.eventos_por_assistir.append(event_id)

            # Actualizar el usuario en la base de datos
            db.usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": {"eventos_por_assistir": user.eventos_por_assistir}})

            return True, "¡Usuario actualizado exitosamente!"
        except Exception as ex:
            return False, str(ex)
    
    @classmethod
    def get_all_eventos_por_assistir_by_user(cls, db, user_id):
        try:
            # Obtener al usuario por su ID
            user = cls.get_by_id(db, user_id)
            if not user:
                raise Exception("El usuario no existe")

            # Obtener todos los IDs de eventos por asistir del usuario
            eventos_por_assistir_ids = user.eventos_por_assistir

            # Inicializar una lista para almacenar la información de todos los eventos por asistir
            eventos_por_assistir_info = []

            # Obtener la información de cada evento por asistir usando el método get_evento_by_id del modelo de eventos
            for evento_id in eventos_por_assistir_ids:
                evento_info = ModelEvento.get_evento_by_id(db, evento_id)
                if evento_info:
                    eventos_por_assistir_info.append(evento_info)

            return eventos_por_assistir_info

        except Exception as ex:
            print("Error al obtener eventos por asistir del usuario:", ex)
            return None
        
    @classmethod
    def delete_evento_asistido_by_user(cls, db, user_id, event_id):
        try:
            # Obtener al usuario por su ID
            user = cls.get_by_id(db, user_id)
            if not user:
                raise Exception("El usuario no existe")

            # Verificar si el evento está en la lista de eventos por asistir del usuario
            if event_id in user.eventos_por_assistir:
                # Eliminar el evento de la lista de eventos por asistir
                user.eventos_por_assistir.remove(event_id)

                # Actualizar el usuario en la base de datos
                db.usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": {"eventos_por_assistir": user.eventos_por_assistir}})

                return True, "El evento ha sido eliminado de la lista de eventos por asistir."
            else:
                return False, "El evento no está en la lista de eventos por asistir del usuario."

        except Exception as ex:
            print("Error al eliminar evento asistido por usuario:", ex)
            return False, "Error al eliminar evento asistido por usuario."

   
    @classmethod
    def get_all_user(cls, db):
        try:
            # Obtener todos los usuarios de la base de datos
            users = list(db.usuarios.find({}))
            return users, "¡Usuarios encontrados exitosamente!"
        except Exception as ex:
            return None, str(ex)