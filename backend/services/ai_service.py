import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el cliente oficial de Gemini
# Automáticamente tomará la variable de entorno GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Definimos el esquema estricto que queremos que devuelva la IA usando Pydantic
class AnalisisEmocional(BaseModel):
    intencion: str = Field(description="Debe ser estrictamente 'REGISTRAR_EMOCION' si expresa su estado de ánimo, o 'DESCONOCIDO' si habla de otra cosa.")
    emocion_detectada: str = Field(description="La emoción principal identificada (ej. tristeza, alegría, frustración) o null.")
    intensidad: int = Field(description="Un número entero del 1 al 5 estimado según el mensaje, o null.")
    nota: str = Field(description="Un breve resumen o contexto de por qué se siente así, o null.")
    respuesta_ia: str = Field(description="Un mensaje empático, breve y de apoyo directo para el usuario.")

def procesar_lenguaje_natural(texto_usuario):
    """
    Analiza el texto del usuario usando Google Gemini y obliga al modelo
    a retornar un objeto JSON alineado al esquema estructurado.
    """
    prompt_sistema = (
        "Eres el motor de análisis de una aplicación de gestión emocional de formacion secundaria y universitaria "
        "Tu trabajo es clasificar el texto del usuario y extraer las variables emocionales."
    )

    try:
        # Usamos el modelo gemini-1.5-flash (el estándar actual y más rápido para tareas de texto)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=texto_usuario,
            config=types.GenerateContentConfig(
                system_instruction=prompt_sistema,
                temperature=0.2,
                # Forzamos la salida JSON estructurada basada en nuestra clase Pydantic
                response_mime_type="application/json",
                response_schema=AnalisisEmocional,
            ),
        )
        
        # El SDK moderno ya parsea el JSON y nos permite usar la respuesta directo como texto plano estructurado
        return json.loads(response.text)
        
    except Exception as e:
        # Analizamos si el error contiene la palabra clave de cuota
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("\n⚠️ [ALERTA DE CUOTA]: Se ha agotado el límite de peticiones de Gemini 1.5 Flash.")
            print(f"Detalle técnico: {error_msg}")
        else:
            print(f"❌ Error inesperado en el servicio de Gemini: {error_msg}")
            
        return {
            "intencion": "ERROR",
            "emocion_detectada": None,
            "intensidad": None,
            "nota": None,
            "respuesta_ia": "Lo siento, experimenté un inconveniente al procesar tu estado de ánimo en este momento."
        }