document.getElementById('sendBtn').addEventListener('click', enviarMensaje);
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') enviarMensaje();
});

async function enviarMensaje() {
    const inputElement = document.getElementById('userInput');
    const mensajeTexto = inputElement.value.trim();
    
    if (!mensajeTexto) return; // No hacer nada si está vacío

    // 1. Pintar el mensaje del usuario en la pantalla
    agregarMensajeAlChat(mensajeTexto, 'user-message');
    inputElement.value = ''; // Limpiar el campo de texto

    // 2. Crear una burbuja de carga temporal para la IA
    const loadingMessageId = agregarMensajeAlChat('✍️ Pensando...', 'ia-message');

    try {
        // 3. Hacer la llamada real a tu API local de Flask
        const response = await fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensajeTexto,
                usuario_id: "estudiante_luz_123" // ID persistente de prueba
            })
        });

        const data = await response.json();
        
        // Remover el mensaje de carga
        document.getElementById(loadingMessageId).remove();

        if (data.status === 'success') {
            // 4. Extraer la respuesta empática que generó Gemini
            const respuestaIA = data.analisis_orquestador.respuesta_ia;
            agregarMensajeAlChat(respuestaIA, 'ia-message');
        } else {
            agregarMensriageAlChat('❌ Hubo un inconveniente al procesar tu solicitud.', 'ia-message');
        }

    } catch (error) {
        console.error('Error de conexión:', error);
        document.getElementById(loadingMessageId).remove();
        agregarMensajeAlChat('❌ No se pudo conectar con el servidor backend.', 'ia-message');
    }
}

function agregarMensajeAlChat(texto, claseEstilo) {
    const chatBox = document.getElementById('chatBox');
    const nuevoMensaje = document.createElement('div');
    
    // Asignamos un ID único temporal por si necesitamos borrarlo (como el de carga)
    const idUnico = 'msg-' + Date.now();
    nuevoMensaje.id = idUnico;
    
    nuevoMensaje.className = `message ${claseEstilo}`;
    nuevoMensaje.innerText = texto;
    
    chatBox.appendChild(nuevoMensaje);
    
    // Auto-scroll hacia abajo para ver el último mensaje
    chatBox.scrollTop = chatBox.scrollHeight;
    
    return idUnico;
}