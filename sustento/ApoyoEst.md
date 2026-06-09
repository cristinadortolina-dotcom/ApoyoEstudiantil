# Resumen Técnico: Sistema de Apoyo Estudiantil con IA y Orquestación

Este documento detalla la arquitectura, el stack tecnológico y el flujo de datos del proyecto "Apoyo Estudiantil", desarrollado para la gestión y seguimiento emocional de alumnos mediante Inteligencia Artificial.

## 1. Arquitectura del Sistema
La aplicación sigue un modelo **Cliente-Servidor** con una **Capa de Orquestación Lógica** en el backend. Esta arquitectura separa la interpretación del lenguaje natural de la ejecución de acciones en la base de datos.

### Capas Principales:
1. **Frontend (Capa de Presentación):** Interfaz web construida con HTML, CSS y JavaScript (Vanilla JS). Utiliza el API `fetch` para comunicación asíncrona y `localStorage` para la persistencia de sesión.
2. **Backend (Capa de Lógica y Orquestación):** Servidor basado en **Flask** (Python) que actúa como mediador.
3. **Capa de Inteligencia Artificial:** Integración con **Google Gemini 2.5 Flash** para procesamiento de lenguaje natural (PLN).
4. **Capa de Persistencia:** Base de Datos NoSQL con **Firebase Firestore**.

## 2. Stack Tecnológico y Cumplimiento de Requerimientos
- **Lenguaje:** Python 3.10+
- **Framework Web:** Flask (con Flask-CORS para seguridad).
- **IA:** Google GenAI SDK (Gemini 2.5 Flash).
- **Validación de Datos:** Pydantic (Garantiza que la IA siempre responda en el formato JSON esperado).
- **Base de Datos:** Google Firebase Firestore.
- **Entorno:** python-dotenv (Gestión de variables de entorno).

## 3. El Orquestador: Lógica Intermediaria y Toma de Decisiones
El componente más innovador es el **Orquestador**. 
A diferencia de un chatbot tradicional que solo responde texto, este módulo:
1. Recibe el texto del usuario.
2. Solicita a la IA un análisis a traves de un **Orquestador de Código Propio** en Python (`orchestration.py`). Este componente actúa como un controlador inteligente que separa el *entendimiento* de la *ejecución*.
3. **Toma decisiones:** Si la intención detectada es `REGISTRAR_EMOCION`, el orquestador dispara automáticamente el guardado en la base de datos. Si la intención es `DESCONOCIDO`, prioriza la fluidez conversacional.

### Diferenciación Técnica:
1. **No es un Proxy:** El orquestador no devuelve lo que la IA dice de forma directa; primero analiza la "intención" (intent) devuelta por el modelo.
2. **Motor de Decisiones:** Implementa lógica condicional basada en estados. Si la IA clasifica el mensaje como `REGISTRAR_EMOCION`, el orquestador dispara la persistencia en Firebase Firestore. Si la intención es `DESCONOCIDO`, el orquestador decide omitir la base de datos para optimizar recursos.
3. **Validación por Esquema (Pydantic):** Se utiliza `AnalisisEmocional` como un contrato de datos. Esto transforma una respuesta de lenguaje natural ambigua en un objeto de datos tipado y seguro para el backend.

## 4. Procesamiento de Lenguaje Natural (PLN) con Salida Estructurada
Se implementó una técnica de **Prompt Engineering** avanzada conocida como **Structured Output**.
- **Modelo:** `gemini-2.5-flash`
- **Extracción de Entidades:** El sistema no recibe texto plano, sino que obliga a la IA a extraer 5 variables clave: `intencion`, `emocion_detectada`, `intensidad`, `nota` y `respuesta_ia`.
- **Robustez:** Al definir un `response_schema`, el orquestador garantiza que el flujo de control nunca se rompa por respuestas inesperadas del modelo de lenguaje.

## 5. Flujo de Datos y Orquestación (End-to-End)
1. **Captura:** El usuario ingresa un sentimiento en el chat.
2. **Transmisión:** El frontend envía el mensaje junto con el `usuario_id` al endpoint `/api/chat`.
3. **Análisis:** El backend llama a `ai_service.py`, donde Gemini interpreta la carga emocional.
4. **Decisión del Orquestador:** El código Python evalúa la intención. Si cumple los criterios, invoca a `db_service.py` para persistir el registro.
5. **Feedback:** El sistema devuelve una respuesta empática generada por la IA al frontend en tiempo real.

## 6. Puntos Clave para la Defensa Académica
- **Arquitectura No Acoplada:** La lógica de negocio reside en Python, no en la IA. La IA es reemplazable (podría usarse GPT-4 o Llama-3) sin cambiar la lógica de guardado en Firebase.
- **Integridad de Datos:** El uso de Pydantic asegura que solo datos válidos lleguen a la capa de persistencia.
- **Escalabilidad:** Al usar Firestore, el sistema soporta grandes volúmenes de datos sin pérdida de rendimiento.
