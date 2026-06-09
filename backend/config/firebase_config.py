import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env (Local)
load_dotenv()

def db_init():
    """esto inicializa la app de Firebase y retorna el cliente de Firestore"""
    
    # 1. se optiene el valor de la variable de entorno
    cred_env_value = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    if not cred_env_value:
        raise ValueError("Error: No se encontró la variable FIREBASE_CREDENTIALS_PATH en el entorno o archivo .env")

    # 2. identificacion y detencion de si el contenido del JSON (Render)
    # o si es una ruta de archivo (Local)
    cred_env_value = cred_env_value.strip()
    
    if cred_env_value.startswith("{"):
        # --- MODO RENDER / NUBE ---
        # Si el valor empieza con llave '{', significa que el contenido del JSON va directo a Render
        try:
            print("[FIREBASE] Detectado texto JSON directo. Cargando desde variable de entorno...")
            cred_dict = json.loads(cred_env_value)
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            raise ValueError(f"Error crítico al procesar el texto JSON de Firebase desde el entorno: {str(e)}")
            
    else:
        # --- MODO LOCAL / MI COMPUTADORA ---
        # Si no empieza con '{', puede ser una ruta física de archivo (ej: "config/firebase-key.json")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) # Sube a la carpeta 'backend'
        
        # Construimos la ruta absoluta usando la definición de tu .env
        absolute_cred_path = os.path.abspath(os.path.join(project_root, cred_env_value))
        
        print(f"[FIREBASE] Detectada ruta física. Buscando archivo en: {absolute_cred_path}")
        if not os.path.exists(absolute_cred_path):
            raise FileNotFoundError(f"Error crítico: No se encontró el archivo de llaves en la ruta calculada: {absolute_cred_path}")
            
        cred = credentials.Certificate(absolute_cred_path)

    # 3. Inicializar la aplicación de Firebase de forma segura
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    print("Conexión exitosa con Firebase Firestore")
    return firestore.client()

# Instancia global de la base de datos para usarla en los servicios
db = db_init()