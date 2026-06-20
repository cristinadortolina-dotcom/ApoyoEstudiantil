import os
import json
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el cliente. Si la librería está bien instalada, esto funcionará.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class AnalisisEmocional(BaseModel):
    intencion: str = Field(description="REGISTRAR_EMOCION o DESCONOCIDO")
    emocion_detectada: str
    intensidad: int
    nota: str
    respuesta_ia: str

def procesar_lenguaje_natural(texto_usuario):
    try:
        # Usamos la estructura de diccionario para evitar importar 'types'
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=texto_usuario,
            config={
                "system_instruction": "Eres un asistente de gestión emocional.",
                "temperature": 0.2,
                "response_mime_type": "application/json",
                "response_schema": AnalisisEmocional,
            }
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error crítico en IA: {e}")
        return {"intencion": "ERROR", "respuesta_ia": "Error en el servicio."}