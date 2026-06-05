from flask import Flask, jsonify, request
from flask_cors import CORS
from config.firebase_config import db
from firebase_admin import firestore
from orchestration import orquestar_peticion  # <-- IMPORTANTE: Conecta tu orquestador

app = Flask(__name__)
CORS(app)

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

# 🌟 NUEVA RUTA: Aquí es donde Postman finalmente encontrará la puerta abierta
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        # Extraemos el mensaje enviado desde Postman
        texto_usuario = data.get("mensaje")
        usuario_id = data.get("usuario_id", "estudiante_luz_123") # Un ID temporal por defecto
        
        if not texto_usuario:
            return jsonify({"status": "error", "message": "Falta el campo 'mensaje' en la petición"}), 400
            
        # Ejecutamos tu lógica de orquestación
        resultado = orquestar_peticion(texto_usuario, usuario_id)
        
        return jsonify({
            "status": "success",
            "analisis_orquestador": resultado
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error interno en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)