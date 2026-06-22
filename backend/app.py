from flask import Flask, jsonify, request
from flask_cors import CORS
from config.firebase_config import db
from firebase_admin import firestore
from orchestration import orquestar_peticion 
from services.autentic_service import AuthService  
from services.db_service import obtener_ejercicios_por_categoria, insertar_ejercicio # <-- NUEVA IMPORTACIÓN
import datetime

app = Flask(__name__)
CORS(app)

autentic_service = AuthService()

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Servidor backend de ApoyoEstudiantil funcionando perfectamente."
    })

@app.route('/test-db')
def test_db():
    try:
        doc_ref = db.collection('test_logs').document('conexion')
        doc_ref.set({
            'mensaje': '¡Conexión exitosa desde el backend de Python!',
            'timestamp': firestore.SERVER_TIMESTAMP 
        })
        return jsonify({"status": "success", "message": "Documento creado en Firebase Firestore correctamente."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        correo = data.get("correo")
        password = data.get("password")
        nivel_academico = data.get("nivel_academico", "Pregrado")

        if not correo or not password or not nombre:
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        # GENERACIÓN DEL ID ÚNICO: Usamos el correo limpio (sin puntos ni arrobas) o un ID auto-generado
        # En este caso, usaremos un ID limpio basado en el correo para que sea fácil de rastrear
        usuario_id = correo.replace(".", "_").replace("@", "_")

        # 1. Guardar en la colección 'cuentas' (para autenticación)
        db.collection('cuentas').document(usuario_id).set({
            "correo": correo,
            "password": password, # Recuerda encriptar esto más adelante por seguridad
            "fecha_creacion": datetime.datetime.now()
        })

        # 2. Guardar en la colección 'usuarios' (para el perfil y datos personales)
        db.collection('usuarios').document(usuario_id).set({
            "nombre": nombre,
            "correo": correo,
            "nivel_academico": nivel_academico,
            "fecha_registro": datetime.datetime.now()
        })

        # IMPORTANTE: Devolvemos el usuario_id al frontend para que lo guarde en el navegador
        return jsonify({
            "status": "success", 
            "message": "Usuario registrado exitosamente",
            "usuario_id": usuario_id,
            "nombre": nombre
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        correo = data.get("correo")
        password = data.get("password")

        usuario_id = correo.replace(".", "_").replace("@", "_")
        
        # Buscar la cuenta por el ID unificado
        cuenta_doc = db.collection('cuentas').document(usuario_id).get()

        if cuenta_doc.exists and cuenta_doc.to_dict().get("password") == password:
            # Buscamos su perfil para enviar también el nombre actualizado
            user_doc = db.collection('usuarios').document(usuario_id).get()
            nombre = user_doc.to_dict().get("nombre", "Estudiante") if user_doc.exists else "Estudiante"

            return jsonify({
                "status": "success",
                "usuario_id": usuario_id,
                "nombre": nombre
            }), 200
        else:
            return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        texto_usuario = data.get("mensaje")
        usuario_id = data.get("usuario_id", "estudiante_luz_123") 
        
        if not texto_usuario:
            return jsonify({"status": "error", "message": "Falta el campo 'mensaje' en la petición"}), 400
            
        resultado = orquestar_peticion(texto_usuario, usuario_id)
        
        return jsonify({
            "status": "success",
            "analisis_orquestador": resultado
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error interno en el servidor: {str(e)}"}), 500

# =========================================================
# MÓDULO COGNITIVO (Evaluación e Interpretación)
# =========================================================
@app.route('/api/cognitivo/evaluar', methods=['POST'])
def evaluar_test_cognitivo():
    try:
        datos = request.get_json()
        usuario_id = datos.get("usuario_id")
        respuestas_texto = datos.get("respuestas") 
        bloqueo_selec = datos.get("bloqueo", "No especificado") 
        nivel_selec = datos.get("nivel", "No especificado")
        
        # El propósito se integra directamente como parte de la clase de datos personales
        proposito = datos.get("proposito", "Optimización académica")
        
        if not usuario_id or not respuestas_texto:
            return jsonify({"status": "error", "message": "Datos incompletos."}), 400

        # --- DICCIONARIO DE CONVERSIÓN ---
        mapeo = {
            "Nunca": 1, "Raramente": 2, "A veces": 3, "Frecuentemente": 4, "Siempre": 5
        }

        def get_valor(key):
            texto = respuestas_texto.get(key, "Nunca")
            return mapeo.get(texto, 1) 

        atencion = (get_valor('p1') + get_valor('p2')) / 2
        ejecutivas = (get_valor('p3') + get_valor('p4') + get_valor('p5')) / 3
        memoria = (get_valor('p6') + get_valor('p7')) / 2
        orientacion = (get_valor('p8') + get_valor('p9')) / 2

        def obtener_estado(promedio):
            return "Fortaleza" if promedio >= 3.5 else "Oportunidad"

        resultados_enriquecidos = {
            "Atención": {"puntuacion": round(atencion, 2), "estado": obtener_estado(atencion)},
            "Funciones Ejecutivas": {"puntuacion": round(ejecutivas, 2), "estado": obtener_estado(ejecutivas)},
            "Memoria": {"puntuacion": round(memoria, 2), "estado": obtener_estado(memoria)},
            "Orientación": {"puntuacion": round(orientacion, 2), "estado": obtener_estado(orientacion)}
        }

        # --- NUEVO: CONSTRUCCIÓN DEL DIAGNÓSTICO PERSONALIZADO ---
        diagnostico_personalizado = (
            f"Perfil configurado para el nivel académico '{nivel_selec}'. "
            f"El plan de entrenamiento está orientado a su propósito de datos personales ('{proposito}'), "
            f"priorizando ejercicios que mitiguen el bloqueo principal detectado: '{bloqueo_selec}'."
        )

        # Guardar en Firestore
        db.collection('test_cognitivo').add({
            "id_usuario": usuario_id,
            "fecha": datetime.datetime.utcnow().isoformat(),
            "resultados": resultados_enriquecidos,
            "dimension_bloqueo": bloqueo_selec,
            "nivel_academico": nivel_selec,
            "proposito_usuario": proposito,
            "diagnostico": diagnostico_personalizado # Se guarda el registro histórico
        })

        # Devolvemos el diagnóstico al frontend
        return jsonify({
            "status": "success", 
            "resultados": resultados_enriquecidos,
            "diagnostico": diagnostico_personalizado
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================================================
# MÓDULO DE ENTRENAMIENTO COGNITIVO (Ejercicios)
# =========================================================
@app.route('/api/ejercicios/<categoria>', methods=['GET'])
def get_ejercicios(categoria):
    """
    Ruta para que el frontend pida ejercicios de una categoría.
    Ejemplo: GET /api/ejercicios/atencion
    """
    try:
        ejercicios = obtener_ejercicios_por_categoria(categoria)
        if ejercicios:
            return jsonify({"status": "success", "data": ejercicios}), 200
        else:
            return jsonify({"status": "error", "message": "No se encontraron ejercicios"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ejercicios/nuevo', methods=['POST'])
def add_ejercicio():
    """
    Ruta para insertar un nuevo ejercicio en la base de datos.
    Ideal para poblar Firestore mediante Postman o scripts internos.
    """
    try:
        datos = request.get_json()
        id_generado = insertar_ejercicio(datos)
        
        if id_generado:
            return jsonify({"status": "success", "id": id_generado, "message": "Ejercicio creado exitosamente."}), 201
        return jsonify({"status": "error", "message": "No se pudo insertar el ejercicio en la base de datos."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================================================
# GESTIÓN DE PERFIL DE USUARIO Y DATOS PERSONALES
# =========================================================

@app.route('/api/usuario/<usuario_id>', methods=['GET'])
def obtener_perfil(usuario_id):
    try:
        # 1. Obtener datos de registro del usuario
        user_ref = db.collection('usuarios').document(usuario_id).get()
        if not user_ref.exists:
            datos_usuario = {
                "nombre": "Estudiante",
                "correo": "usuario@luz.edu.ve",
                "nivel_academico": "Pregrado"
            }
        else:
            datos_usuario = user_ref.to_dict()

        # 2. Obtener datos del test (Ordenamos en memoria de Python para evitar exigir índices compuestos)
        test_docs = db.collection('test_cognitivo').where('id_usuario', '==', usuario_id).get()
        
        proposito = "No definido"
        plan_cognitivo = []

        if test_docs and len(test_docs) > 0:
            # Convertimos los documentos a una lista de diccionarios
            lista_tests = [doc.to_dict() for doc in test_docs]
            # Ordenamos por el campo 'fecha' de forma descendente (el más reciente primero)
            lista_tests.sort(key=lambda x: x.get("fecha", ""), reverse=True)
            
            ultimo_test = lista_tests[0]
            proposito = ultimo_test.get("proposito_usuario", "General")
            
            resultados = ultimo_test.get("resultados", {})
            for area, info in resultados.items():
                if info.get("estado") == "Oportunidad":
                    plan_cognitivo.append(area)

        return jsonify({
            "status": "success",
            "nombre": datos_usuario.get("nombre"),
            "correo": datos_usuario.get("correo"), 
            "nivel_academico": datos_usuario.get("nivel_academico"),
            "proposito": proposito,
            "plan_cognitivo": plan_cognitivo
        }), 200

    except Exception as e:
        print("Error en backend obtener_perfil:", str(e)) # Imprime el error real en tu consola de Python
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/usuario/<usuario_id>', methods=['PUT'])
def actualizar_perfil(usuario_id):
    try:
        datos = request.get_json()
        nuevo_nombre = datos.get("nombre")
        nuevo_nivel = datos.get("nivel_academico")

        if not nuevo_nombre or not nuevo_nivel:
            return jsonify({"status": "error", "message": "Datos incompletos."}), 400

        # Actualizar en la colección de usuarios
        db.collection('usuarios').document(usuario_id).set({
            "nombre": nuevo_nombre,
            "nivel_academico": nuevo_nivel
        }, merge=True)

        return jsonify({"status": "success", "message": "Perfil actualizado correctamente."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)