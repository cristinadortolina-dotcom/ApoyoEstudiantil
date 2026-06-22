import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 1. Inicializar Firebase Admin SDK
try:
    cred = credentials.Certificate('config/firebase-key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("[Firebase]: Conexión establecida con éxito para inicialización.")
except Exception as e:
    print(f"[Error Firebase]: No se pudo conectar. Verifica tus credenciales. Detalle: {e}")
    exit()

# 2. Estructura de ejercicios basados en los cuadernos de estimulación
ejercicios_iniciales = [
    # ---- ATENCIÓN ----
    {
        "categoria": "atencion",
        "nombre": "Secuencias de Números Ausentes",
        "nivel": "Medio",
        "descripcion": "Identifica y completa los números que faltan en una secuencia lógica para entrenar tu capacidad de concentración.",
        "instruccion": "En una secuencia numérica del 1 al 100 distribuidos de forma aleatoria, encuentra los cuatro números específicos que faltan para completar la serie completa."
    },
    {
        "categoria": "atencion",
        "nombre": "Cancelación Visual y Sostenida",
        "nivel": "Alto",
        "descripcion": "Encuentra y filtra elementos específicos en una matriz densa de caracteres parecidos.",
        "instruccion": "Examina la lista de caracteres matemáticos provista y tacha únicamente todos los símbolos de pertenencia matemática (∈) en el menor tiempo posible sin saltarte ninguno."
    },
    
    # ---- FUNCIONES EJECUTIVAS ----
    {
        "categoria": "ejecutivas",
        "nombre": "Planificación de Metas Complejas",
        "nivel": "Alto",
        "descripcion": "Descomponer un objetivo masivo en pasos lógicos ordenados secuencialmente.",
        "instruccion": "Imagina que tienes que planificar cómo conseguir un título universitario. Escribe una lista de exactamente 15 pasos ordenados de forma cronológica con las acciones y decisiones que se deben tomar desde el día uno hasta la graduación."
    },
    {
        "categoria": "ejecutivas",
        "nombre": "Flexibilidad Mental y Clasificación",
        "nivel": "Medio",
        "descripcion": "Adaptación a reglas de ordenación abstractas basadas en múltiples variables.",
        "instruccion": "Empareja una tarjeta objetivo con una de las cuatro opciones disponibles bajo la siguiente regla: Si existe una idéntica en color, forma y número, únelas. Si no existe, debes clasificarla con aquella que NO coincida en absolutamente ninguna de las tres variables."
    },

    # ---- MEMORIA ----
    {
        "categoria": "memoria",
        "nombre": "Memoria de Trabajo Inversa",
        "nivel": "Alto",
        "descripcion": "Retención y manipulación mental de secuencias de información en sentido cronológico inverso.",
        "instruccion": "Escribe de memoria y en orden estrictamente inverso (de atrás hacia adelante) los días de la semana y, posteriormente, las cuatro estaciones del año sin apoyos visuales."
    },
    {
        "categoria": "memoria",
        "nombre": "Asociación Semántica Geográfica",
        "nivel": "Medio",
        "descripcion": "Recuperación de información de almacenamiento a largo plazo mediante redes conceptuales.",
        "instruccion": "Une mediante líneas cada río principal listado en la columna A con la localidad o ciudad correspondiente de la columna B por la cual fluye su cauce."
    },

    # ---- ORIENTACIÓN ----
    {
        "categoria": "orientacion",
        "nombre": "Orientación Temporal de Precisión",
        "nivel": "General",
        "descripcion": "Anclaje consciente y diario de las coordenadas cronológicas actuales.",
        "instruccion": "Escribe en la parte superior de tu espacio de trabajo el día exacto de la semana, la fecha numérica, el mes corriente y la hora exacta de inicio de la actividad."
    }
]

def poblar_base_de_datos():
    print("\n[Proceso]: Iniciando la carga de ejercicios en Firestore...")
    coleccion_ref = db.collection("ejercicios")
    
    contador = 0
    for ejercicio in ejercicios_iniciales:
        try:
            # Añadir documento con ID auto-generado por Firestore
            doc_ref = coleccion_ref.add(ejercicio)
            print(f" -> Guardado exitosamente: '{ejercicio['nombre']}' en la categoría '{ejercicio['categoria']}'")
            contador += 1
        except Exception as err:
            print(f" [Error] No se pudo guardar el ejercicio {ejercicio['nombre']}: {err}")
            
    print(f"\n[Éxito]: Proceso completado. Se insertaron {contador} ejercicios en la colección 'ejercicios'.")

if __name__ == "__main__":
    poblar_base_de_datos()