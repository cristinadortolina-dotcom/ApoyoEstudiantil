from config.firebase_config import db
from firebase_admin import firestore

def guardar_registro_emocional(usuario_id, datos_emocion):
    """
    Guarda los datos extraídos por la IA directamente en la 
    colección 'registro_emociones' vinculados al ID del usuario.
    """
    try:
        # De acuerdo con tu diseño de base de datos, vinculamos el id_usuario
        # directamente con la entidad del registro emocional
        registro_data = {
            "id_usuario": usuario_id,
            "emocion_detectada": datos_emocion.get("emocion_detectada"),
            "intensidad": datos_emocion.get("intensidad"),
            "nota": datos_emocion.get("nota"),
            "timestamp": firestore.SERVER_TIMESTAMP  # Hora exacta del servidor en la nube
        }
        
        # Insertar un nuevo documento con un ID automático en Firestore
        doc_ref = db.collection("registro_emociones").document()
        doc_ref.set(registro_data)
        
        print(f"✅ [Firestore]: Datos guardados con éxito bajo el ID de documento: {doc_ref.id}")
        return True
    except Exception as e:
        print(f"❌ [Firestore Error]: No se pudo guardar el registro: {e}")
        return False