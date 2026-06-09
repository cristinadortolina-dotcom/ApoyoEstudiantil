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

# inicio de seccion
@app.route('/api/auth/login', methods=['POST'])

def login():
    try:
        print("\n--> [BACKEND app.py] 1. Petición POST recibida en /api/auth/login")
        data = request.get_json()
        print(f"--> Data cruda en JSON: {data}")
        
        correo = data.get("correo")
        contrasena = data.get("contraseña") 
        print(f"--> Variables extraídas: Correo='{correo}' | Contrasena='{contrasena}'")
        
        if not correo or not contrasena:
            print("--> [BACKEND app.py] X. Error: Campos vacíos detectados.")
            return jsonify({"status": "error", "message": "Campos obligatorios vacíos."}), 400
            
        print("--> [BACKEND app.py] 2. Enviando datos al AuthService...")
        resultado = autentic_service.verificar_credenciales(correo, contrasena)
        print(f"--> [BACKEND app.py] 3. Resultado devuelto por AuthService: {resultado}")
        
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
        print(f"--> [BACKEND app.py] EXCEPCIÓN CRÍTICA: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
# para el chat y el orquestador
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