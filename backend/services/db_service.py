from config.firebase_config import db
from firebase_admin import firestore

# Asegúrate de que tu config/firebase_config.py ya tenga inicializada la app.
# Si db no viene de config, entonces descomenta la siguiente línea:
db = firestore.client() 

def guardar_registro_emocional(usuario_id, datos_emocion):
    """Guarda los datos de la IA en la colección 'registro_emociones'."""
    try:
        registro_data = {
            "id_usuario": usuario_id,
            "emocion_detectada": datos_emocion.get("emocion_detectada"),
            "intensidad": datos_emocion.get("intensidad"),
            "nota": datos_emocion.get("nota"),
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        
        # Guardamos en la colección
        doc_ref = db.collection("registro_emociones").document()
        doc_ref.set(registro_data)
        
        print(f"[Firestore]: Registro guardado con ID: {doc_ref.id}")
        return True
    except Exception as e:
        print(f"[Firestore Error]: {e}")
        return False

def insertar_ejercicio(datos_ejercicio):
    """Inserta un nuevo ejercicio en la colección 'ejercicios'."""
    try:
        # .add() es perfecto aquí para generar un ID automático
        ref = db.collection('ejercicios').add(datos_ejercicio)
        print(f"¡Éxito! Ejercicio creado con ID: {ref[1].id}")
        return ref[1].id
    except Exception as e:
        print(f"Error al insertar ejercicio: {e}")
        return None

def obtener_ejercicios_por_categoria(categoria):
    """
    Consulta la colección 'ejercicios' y filtra por categoría.
    Ejemplo: categoria = 'atencion'
    """
    try:
        # Creamos una referencia a la colección
        coleccion_ejercicios = db.collection('ejercicios')
        
        # Filtramos donde el campo 'categoria' sea igual al parámetro
        query = coleccion_ejercicios.where('categoria', '==', categoria).stream()
        
        ejercicios = []
        for doc in query:
            # Convertimos el documento a un diccionario y añadimos su ID
            datos = doc.to_dict()
            datos['id'] = doc.id
            ejercicios.append(datos)
            
        print(f"[Firestore]: Se encontraron {len(ejercicios)} ejercicios para '{categoria}'.")
        return ejercicios
    except Exception as e:
        print(f"[Firestore Error]: Error al consultar ejercicios: {e}")
        return []

# Ejemplo de cómo lo llamarías desde tu lógica principal:
# lista_atencion = obtener_ejercicios_por_categoria("atencion")