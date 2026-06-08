from flask import Flask, jsonify, request
from flask_cors import CORS
from config.firebase_config import db
from firebase_admin import firestore
from orchestration import orquestar_peticion  # Capa de orquestación lógica (IA)

# IMPORTACIÓN DE LA ETAPA 1.1 (Con el nombre actualizado)
from services.autentic_service import AuthService  

app = Flask(__name__)
CORS(app)

# Inicializamos el servicio de autenticación globalmente
auth_service = AuthService()

# =====================================================================
# RUTA BASE: ESTADO DEL SERVIDOR
# =====================================================================
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Servidor backend de ApoyoEstudiantil funcionando perfectamente."
    })

# =====================================================================
# RUTA DE DIAGNÓSTICO: PRUEBA DE CONEXIÓN A FIRESTORE
# =====================================================================
@app.route('/test-db')
def test_db():
    try:
        doc_ref = db.collection('test_logs').document('conexion')
        doc_ref.set({
            'mensaje': '¡Conexión exitosa desde el backend de Python!',
            'timestamp': firestore.SERVER_TIMESTAMP 
        })
        return jsonify({
            "status": "success", 
            "message": "Documento creado en Firebase Firestore correctamente."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Fallo al conectar con Firebase: {str(e)}"
        }), 500

# =====================================================================
# ETAPA 1.2: ENDPOINT PARA INICIO DE SESIÓN (POST)
# =====================================================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        correo = data.get("correo")
        contrasena = data.get("contraseña") # Sincronizado con el campo de Firestore
        
        # Validación preventiva de campos vacíos
        if not correo or not contrasena:
            return jsonify({
                "status": "error", 
                "message": "Por favor, complete todos los campos (correo y contraseña)."
            }), 400
            
        # Ejecución de la consulta en el servicio (Etapa 1.1)
        resultado = auth_service.verificar_credenciales(correo, contrasena)
        
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
            return jsonify({
                "status": "error",
                "message": resultado["mensaje"]
            }), 401
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en el servidor: {str(e)}"}), 500

# =====================================================================
# ETAPA 1.3: ENDPOINT PARA REGISTRO ALTERNATIVO (POST)
# =====================================================================
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        correo = data.get("correo")
        contrasena = data.get("contraseña")
        nombre = data.get("nombre")
        rango_academico = data.get("rango_academico", "Pregrado")
        
        # Validación: campos estrictamente obligatorios para crear cuenta nueva
        if not correo or not contrasena or not nombre:
            return jsonify({
                "status": "error",
                "message": "Faltan campos obligatorios para el registro (nombre, correo o contraseña)."
            }), 400
            
        # 1. Verificar si el correo ya existe para evitar duplicados
        cuentas_ref = db.collection('cuenta')
        query = cuentas_ref.where('correo', '==', correo).limit(1).stream()
        
        if any(query):
            return jsonify({
                "status": "error",
                "message": "Este correo electrónico ya se encuentra registrado."
            }), 400
            
        # 2. Generar un ID único automático usando el generador de Firestore
        nuevo_usuario_ref = db.collection('usuario').document()
        id_usuario = nuevo_usuario_ref.id
        
        # 3. Crear documento en colección 'usuario'
        nuevo_usuario_ref.set({
            "nombre": nombre,
            "rango_academico": rango_academico,
            "proposito": "" # Se inicializa en blanco para que lo configure la IA más adelante
        })
        
        # 4. Crear documento en colección 'cuenta' enlazado por el id_usuario
        db.collection('cuenta').document().set({
            "correo": correo,
            "contraseña": contrasena,
            "id_usuario": id_usuario
        })
        
        return jsonify({
            "status": "success",
            "message": "Estudiante registrado exitosamente. Ahora puede iniciar sesión.",
            "id_usuario": id_usuario
        }), 201
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al registrar usuario: {str(e)}"}), 500

# =====================================================================
# RUTA OPERATIVA: CHAT Y CAPA DE ORQUESTACIÓN LOGICA (POST)
# =====================================================================
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        texto_usuario = data.get("mensaje")
        
        # Se recibe el ID real guardado en el navegador, o un temporal por seguridad
        usuario_id = data.get("usuario_id", "estudiante_luz_123") 
        
        if not texto_usuario:
            return jsonify({
                "status": "error", 
                "message": "Falta el campo 'mensaje' en la petición"
            }), 400
            
        # Invocación al orquestador en Python que procesa con el LLM
        resultado = orquestar_peticion(texto_usuario, usuario_id)
        
        return jsonify({
            "status": "success",
            "analisis_orquestador": resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error interno en el servidor: {str(e)}"
        }), 500

# =====================================================================
# ARRANQUE DEL SERVIDOR LOCAL
# =====================================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)