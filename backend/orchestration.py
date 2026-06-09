from services.ai_service import procesar_lenguaje_natural
from services.db_service import guardar_registro_emocional 

def orquestar_peticion(texto_usuario, usuario_id):
    """
    EL NÚCLEO: Media entre la interpretación de la IA (Gemini) 
    y las acciones reales del sistema.
    """
    print(f"\n[ORQUESTADOR] -> Procesando mensaje para el ID de Firestore: '{usuario_id}'")
    
    # 1. Pasar el texto por el Procesamiento de Lenguaje Natural (Gemini)
    analisis = procesar_lenguaje_natural(texto_usuario)
    
    intencion = analisis.get("intencion")
    emocion = analisis.get("emocion_detectada")
    intensidad = analisis.get("intensidad")
    nota = analisis.get("nota")
    # mas adelante agregar respuesta_para_usuario = analisis.get("respuesta_ia")
    
    # 2. Capa de Orquestación: Toma de decisiones basada en la intención extraída
    if intencion == "REGISTRAR_EMOCION":
        print(f"[LÓGICA]: Intención válida detectada. Conectando con db_service...")
        print(f"[DATOS EXTRAÍDOS]: Emoción: {emocion} | Intensidad: {intensidad} | Nota: {nota}")
        
        # 2. Llamamos a la función para persistir los datos en Firestore
        exito_guardado = guardar_registro_emocional(usuario_id, analisis)
        
        if exito_guardado:
            analisis["accion_ejecutada"] = "Registro emocional guardado con éxito en Firebase Firestore."
        else:
            analisis["accion_ejecutada"] = "Error al intentar escribir en la base de datos."
        
    elif intencion == "DESCONOCIDO":
        print("[LÓGICA]: El usuario habló de un tema fuera del alcance emocional.")
        analisis["accion_ejecutada"] = "Ninguna. Se mantiene la conversación fluida."
        
    elif intencion == "ERROR":
        print("[LÓGICA]: El servicio de IA reportó un error (posible límite de cuota).")
        analisis["accion_ejecutada"] = "Error de proveedor externo (Gemini API)."

    else:
        print("[LÓGICA]: Error en el flujo de análisis.")
        analisis["accion_ejecutada"] = "Error procesando la intención."

    return analisis