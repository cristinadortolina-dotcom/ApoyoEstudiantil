document.getElementById('sendBtn').addEventListener('click', enviarMensaje);
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') enviarMensaje();
});

async function enviarMensaje() {
    const inputElement = document.getElementById('userInput');
    const mensajeTexto = inputElement.value.trim();
    
    if (!mensajeTexto) return; // No hacer nada si está vacío

    // Agrega el mensaje del usuario en la pantalla
    agregarMensajeAlChat(mensajeTexto, 'user-message');
    inputElement.value = ''; // Limpiar el campo de texto

    // Burbuja de carga temporal para la IA
    const loadingMessageId = agregarMensajeAlChat('✍️ Pensando...', 'ia-message');

    try {
        // Llamada real al API local de Flask
        const response = await fetch('https://apoyoestudiantil.onrender.com/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensajeTexto,
                usuario_id: localStorage.getItem('usuario_id') // ID persistente real obtenido del Login
            })
        });

        const data = await response.json();
        
        // Remover el mensaje de carga
        document.getElementById(loadingMessageId).remove();

        if (data.status === 'success') {
            // Extrae la respuesta empática que generó Gemini
            const respuestaIA = data.analisis_orquestador.respuesta_ia;
            agregarMensajeAlChat(respuestaIA, 'ia-message');
        } else {
            // Corrección: se eliminó el error de tipeo 'agregarMensriageAlChat'
            agregarMensajeAlChat('Hubo un inconveniente al procesar tu solicitud.', 'ia-message');
        }

    } catch (error) {
        console.error('Error de conexión:', error);
        document.getElementById(loadingMessageId).remove();
        agregarMensajeAlChat('No se pudo conectar con el servidor backend.', 'ia-message');
    }
}

function agregarMensajeAlChat(texto, claseEstilo) {
    const chatBox = document.getElementById('chatBox');
    const nuevoMensaje = document.createElement('div');
    
    // Se pone un ID único temporal en tal caso de ser borrado
    const idUnico = 'msg-' + Date.now();
    nuevoMensaje.id = idUnico;
    
    nuevoMensaje.className = `message ${claseEstilo}`;
    nuevoMensaje.innerText = texto;
    
    chatBox.appendChild(nuevoMensaje);
    
    // Auto-scroll hacia abajo para ver el último mensaje
    chatBox.scrollTop = chatBox.scrollHeight;
    
    return idUnico;
}

// =====================================================================
// 🚪 GESTIÓN DE CIERRE DE SESIÓN
// =====================================================================
document.getElementById('btn-logout').addEventListener('click', () => {
    // 1. Limpiar los datos del usuario persistidos en el navegador
    localStorage.removeItem('usuario_id');
    localStorage.removeItem('usuario_nombre');
    localStorage.removeItem('usuario_proposito');
    
    console.log("Sesión finalizada con éxito. Redireccionando...");

    // 2. Redireccionar de inmediato a la pantalla de login
    window.location.href = 'login.html';
});