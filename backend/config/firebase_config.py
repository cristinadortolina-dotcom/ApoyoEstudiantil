import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

def db_init():
    """Inicializa la app de Firebase y retorna el cliente de Firestore"""
    # 1. Obtenemos lo que dice el archivo .env (ej: "backend/config/firebase-key.json" o "firebase-key.json")
    env_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    if not env_path:
        raise ValueError("Error: No se encontró la ruta de las credenciales de Firebase en el archivo .env")

    # 2. MAGIA DE INGENIERÍA: Sacamos solo el nombre del archivo (ej: "firebase-key.json")
    #    sin importar cuántas carpetas le hayas puesto por delante en el .env
    file_name = os.path.basename(env_path)

    # 3. Construimos la ruta absoluta real basada en donde vive este archivo config.py
    #    __file__ es la ubicación actual de 'firebase_config.py' (dentro de backend/config)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Unimos la carpeta actual directamente con el nombre del JSON de credenciales
    absolute_cred_path = os.path.join(current_dir, file_name)
    
    # Doble verificación por si el archivo realmente no está ahí metido
    if not os.path.exists(absolute_cred_path):
        raise FileNotFoundError(f"Error crítico: No se encontró el archivo de llaves en la ruta calculada: {absolute_cred_path}")

    # Evita inicializar la app más de una vez si el servidor se recarga
    if not firebase_admin._apps:
        cred = credentials.Certificate(absolute_cred_path) # Usamos la ruta absoluta calculada
        firebase_admin.initialize_app(cred)
        
    print("Conexión exitosa con Firebase Firestore")
    return firestore.client()

# Instancia global de la base de datos para usarla en los servicios
db = db_init()