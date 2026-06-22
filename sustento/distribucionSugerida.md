mi-proyecto-mvp/
│
├──/                  # Capa Lógica y Orquestación (Python)
│   ├── config/
│   │   ├── firebase_config.py# Inicialización de Firebase Admin SDK
|   |   |
│   │   └── firebase-key.json
│   │
│   ├── services/
│   │   ├── ai_service.py     # Conexión con la API de IA y parseo de lenguaje natural
        |--autentic_service.py #encargado de la lógica de autenticación consultando y escribiendo en Firestore.
│   │   └── db_service.py     # Funciones CRUD específicas para interactuar con Firebase
│   │
│   ├── orchestration.py      # EL NÚCLEO: Medía entre el texto de la IA y las acciones de db_service
│   ├── app.py                # Punto de entrada de la API (Flask/FastAPI) y rutas
│   └── requirements.txt      # Dependencias de Python (firebase-admin, openai, flask, etc.)
│
├── frontend/                 # Capa de Presentación (HTML/CSS/JS)
│   ├── index.html            # Interfaz de usuario limpia e interactiva
│   ├── css/
│   │   └── styles.css        # Estilos de la aplicación
│   └── js/
│       ├── api.js            # Módulo para hacer los fetch() al backend de Python
│       └── main.js           # Manejo del DOM, eventos de usuario y dinamismo de la página
│
└── .env                      # Archivo local con credenciales y llaves secretas (¡No subir a GitHub!)