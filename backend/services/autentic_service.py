from config.firebase_config import db
from google.cloud.firestore_v1.base_query import FieldFilter
import uuid

class AuthService:
    """ 
    Servicio encargado de la lógica de autenticación consultando y escribiendo en Firestore.
    """
    
    # --- MÉTODO PARA LOGIN (TU CÓDIGO ORIGINAL) ---
    def verificar_credenciales(self, correo, contrasena):
        try:
            print("\n  [SERVICE] -> 1. Entrando a verificar_credenciales()")
            cuentas_ref = db.collection('cuenta')
            
            print(f"  [SERVICE] -> 2. Buscando en 'cuenta' donde correo='{correo}' y clave='{contrasena}'")
            query = cuentas_ref.where(
                filter=FieldFilter('correo', '==', correo)
            ).where(
                filter=FieldFilter('clave', '==', contrasena)
            ).limit(1).get()
            
            print(f"  [SERVICE] -> 3. Tamaño de la respuesta de Firestore: {len(query)}")
            
            if not query:
                print("  [SERVICE] -> X. Error: No se encontró la cuenta (Lista vacía).")
                return {"exito": False, "mensaje": "Correo o contraseña incorrectos."}

            datos_cuenta = query[0].to_dict()
            id_usuario = datos_cuenta.get("id_usuario")
            print(f"  [SERVICE] -> 4. Cuenta hallada. id_usuario extraído: '{id_usuario}'")

            print(f"  [SERVICE] -> 5. Buscando en 'usuario' el documento ID: '{id_usuario}'")
            usuario_ref = db.collection('usuario').document(id_usuario).get()
            
            if usuario_ref.exists:
                perfil = usuario_ref.to_dict()
                print(f"  [SERVICE] -> 6. Perfil encontrado con éxito: {perfil.get('nombre')}")
                return {
                    "exito": True,
                    "id_usuario": id_usuario,
                    "nombre": perfil.get("nombre"),
                    "rango_academico": perfil.get("rango_academico"),
                    "proposito": perfil.get("proposito", "")
                }
            
            print(f"  [SERVICE] -> X. Error: El documento '{id_usuario}' no existe en la colección 'usuario'.")
            return {"exito": False, "mensaje": "Perfil de usuario no encontrado."}

        except Exception as e:
            print(f"  [SERVICE] -> EXCEPCIÓN INTERNA: {str(e)}")
            return {"exito": False, "mensaje": f"Error en AuthService: {str(e)}"}

    # --- MÉTODO NUEVO PARA REGISTRO ---
    def registrar_usuario(self, nombre, correo, contrasena, rango_academico):
        try:
            # Generamos un ID único para vincular ambas colecciones
            nuevo_id = str(uuid.uuid4())
            
            # Guardamos en 'usuario'
            db.collection('usuario').document(nuevo_id).set({
                "nombre": nombre,
                "rango_academico": rango_academico,
                "correo":correo,
            })
            
            # Guardamos en 'cuenta'
            db.collection('cuenta').add({
                "id_usuario": nuevo_id,
                "correo": correo,
                "clave": contrasena,
            })
            
            return {"exito": True}
        
        except Exception as e:
            print(f"Error crítico al registrar: {str(e)}")
            return {"exito": False, "mensaje": str(e)}