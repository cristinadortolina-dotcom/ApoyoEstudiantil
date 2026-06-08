from config.firebase_config import db

class AuthService:
    """
    Servicio encargado de la lógica de autenticación consultando Firestore.
    """
    def verificar_credenciales(self, correo, contrasena):
        try:
            # 1. Buscar en la colección 'cuenta' el documento que coincida con correo y contraseña
            cuentas_ref = db.collection('cuenta')
            query = cuentas_ref.where('correo', '==', correo).where('contraseña', '==', contrasena).limit(1).stream()
            
            datos_cuenta = None
            for doc in query:
                datos_cuenta = doc.to_dict()
            
            if not datos_cuenta:
                return {"exito": False, "mensaje": "Correo o contraseña incorrectos."}

            id_usuario = datos_cuenta.get("id_usuario")

            # 2. Con el id_usuario, buscar su perfil en la colección 'usuario'
            usuario_ref = db.collection('usuario').document(id_usuario).get()
            
            if usuario_ref.exists:
                perfil = usuario_ref.to_dict()
                return {
                    "exito": True,
                    "id_usuario": id_usuario,
                    "nombre": perfil.get("nombre"),
                    "rango_academico": perfil.get("rango_academico"),
                    "proposito": perfil.get("proposito", "")
                }
            
            return {"exito": False, "mensaje": "Perfil de usuario no encontrado."}

        except Exception as e:
            return {"exito": False, "mensaje": f"Error en AuthService: {str(e)}"}