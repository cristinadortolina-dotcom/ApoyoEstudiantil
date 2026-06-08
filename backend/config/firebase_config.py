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

    # 2. Calculamos la ruta absoluta basada en la raíz del proyecto (un nivel arriba de config)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # Sube a la carpeta 'backend'
    
    # 3. Construimos la ruta absoluta usando la definición del .env
    absolute_cred_path = os.path.abspath(os.path.join(project_root, env_path))
    
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