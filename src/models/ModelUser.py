from .entities.User import User
from bson.objectid import ObjectId

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
                        result.get('rol', 'usuario')  # Manejo del nuevo atributo de rol
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
                    result.get('rol', 'usuario')  # Manejo del nuevo atributo de rol
                )
            return None
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def get_by_username(cls, db, username):
        # Buscar usuario por nombre de usuario en MongoDB
        return db.usuarios.find_one({"username": username})
    
        
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
