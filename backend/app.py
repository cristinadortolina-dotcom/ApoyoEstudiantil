from flask import Flask, jsonify, request
from flask_cors import CORS
from config.firebase_config import db
from firebase_admin import firestore
from orchestration import orquestar_peticion  # Conecta el orquestador

# 1. IMPORTAR EL NUEVO SERVICIO DE AUTENTICACIÓN
from services.autentic_service import AuthService  

app = Flask(__name__)
CORS(app)

# Inicializamos el servicio para usarlo en las rutas
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

# =====================================================================
# NUEVA RUTA - PASO 1.2 Y 1.3: MODULO DE INICIO DE SESIÓN
# =====================================================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        correo = data.get("correo")
        contrasena = data.get("contraseña") # Con la ñ para que combine con Firestore
        
        # Validación simple de campos obligatorios
        if not correo or not contrasena:
            return jsonify({
                "status": "error", 
                "message": "Por favor, complete todos los campos (correo y contraseña)."
            }), 400
            
        # Llamamos a la lógica de tu servicio
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
            # Si las credenciales no coinciden o no existen
            return jsonify({
                "status": "error",
                "message": resultado["mensaje"]
            }), 401
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en el servidor: {str(e)}"}), 500

# =====================================================================
# RUTA EXISTENTE PARA CHAT / ORQUESTADOR
# =====================================================================
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        texto_usuario = data.get("mensaje")
        
        # ¡Ojo aquí! Ahora que tenemos login real, el frontend nos enviará 
        # el id_usuario real de localStorage, si no, cae en el temporal.
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)