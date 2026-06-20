from flask import Flask, jsonify, request
from flask_cors import CORS
from config.firebase_config import db
from firebase_admin import firestore
from orchestration import orquestar_peticion 
from services.autentic_service import AuthService  
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
        contrasena = data.get("contraseña")
        rango = data.get("rango_academico")

        resultado = autentic_service.registrar_usuario(nombre, correo, contrasena, rango)
        
        if resultado.get("exito"):
            return jsonify({"status": "success", "message": "Usuario registrado"}), 201
        else:
            return jsonify({"status": "error", "error": resultado.get("mensaje")}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        correo = data.get("correo")
        contrasena = data.get("contraseña") 
        
        if not correo or not contrasena:
            return jsonify({"status": "error", "message": "Campos obligatorios vacíos."}), 400
            
        resultado = autentic_service.verificar_credenciales(correo, contrasena)
        
        if resultado["exito"]:
            return jsonify({
                "status": "success",
                "message": "Autenticación exitosa.",
                "id_usuario": resultado["id_usuario"],
                "nombre": resultado["nombre"],
                "rango_academico": resultado["rango_academico"],
                "proposito": resultado["proposito"]
            }), 200
        else:
            return jsonify({"status": "error", "message": resultado["mensaje"]}), 401
            
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
# MÓDULO COGNITIVO MODIFICADO (Evaluación e Interpretación)
# =========================================================
@app.route('/api/cognitivo/evaluar', methods=['POST'])
def evaluar_test_cognitivo():
    try:
        datos = request.get_json()
        usuario_id = datos.get("usuario_id")
        respuestas_texto = datos.get("respuestas") # Recibe {"p1": "Siempre", ...}
        bloqueo_selec = datos.get("bloqueo") 
        nivel_selec = datos.get("nivel")
        proposito = datos.get("proposito")
        
        if not usuario_id or not respuestas_texto:
            return jsonify({"status": "error", "message": "Datos incompletos."}), 400

        # --- DICCIONARIO DE CONVERSIÓN ---
        mapeo = {
            "Nunca": 1,
            "Raramente": 2,
            "A veces": 3,
            "Frecuentemente": 4,
            "Siempre": 5
        }

        # Función auxiliar para convertir el texto recibido a número
        def get_valor(key):
            texto = respuestas_texto.get(key, "Nunca")
            return mapeo.get(texto, 1) # Si el texto no existe, devuelve 1 por seguridad

        # Cálculos de promedios (ahora usando números)
        atencion = (get_valor('p1') + get_valor('p2')) / 2
        ejecutivas = (get_valor('p3') + get_valor('p4') + get_valor('p5')) / 3
        memoria = (get_valor('p6') + get_valor('p7')) / 2
        orientacion = (get_valor('p8') + get_valor('p9')) / 2

        # Lógica de interpretación
        def obtener_estado(promedio):
            return "Fortaleza" if promedio >= 3.5 else "Oportunidad"

        resultados_enriquecidos = {
            "Atención": {"puntuacion": round(atencion, 2), "estado": obtener_estado(atencion)},
            "Funciones Ejecutivas": {"puntuacion": round(ejecutivas, 2), "estado": obtener_estado(ejecutivas)},
            "Memoria": {"puntuacion": round(memoria, 2), "estado": obtener_estado(memoria)},
            "Orientación": {"puntuacion": round(orientacion, 2), "estado": obtener_estado(orientacion)}
        }

        # Guardar en Firestore
        db.collection('test_cognitivo').add({
            "id_usuario": usuario_id,
            "fecha": datetime.datetime.utcnow().isoformat(),
            "resultados": resultados_enriquecidos,
            "dimension_bloqueo": bloqueo_selec,
            "nivel_academico": nivel_selec,
            "proposito_usuario": proposito
        })

        return jsonify({"status": "success", "resultados": resultados_enriquecidos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)