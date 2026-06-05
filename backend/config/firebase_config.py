import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

def db_init():
    """Inicializa la app de Firebase y retorna el cliente de Firestore"""
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    if not cred_path:
        raise ValueError("Error: No se encontró la ruta de las credenciales de Firebase en el archivo .env")

    # Evita inicializar la app más de una vez si el servidor se recarga
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        
    print("🚀 Conexión exitosa con Firebase Firestore")
    return firestore.client()

# Instancia global de la base de datos para usarla en los servicios
db = db_init()