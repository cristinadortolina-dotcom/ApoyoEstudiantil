async function enviarDiagnostico(idUsuario) {
    // 1. Recolectar respuestas de escala (p1 a p9)
    const respuestas = {};
    for (let i = 1; i <= 9; i++) {
        const seleccionado = document.querySelector(`input[name="p${i}"]:checked`);
        respuestas[`p${i}`] = seleccionado ? seleccionado.value : 0; // Si no marcó nada, pone 0
    }

    // 2. Crear el paquete (payload)
    // Usamos ?. (encadenamiento opcional) para evitar errores si algún elemento no existe
    const payload = {
        usuario_id: idUsuario,
        respuestas: respuestas,
        bloqueo: document.querySelector('input[name="bloqueo"]:checked')?.value || "No especificado",
        nivel: document.querySelector('input[name="nivel"]:checked')?.value || "No especificado",
        proposito: document.getElementById('proposito_texto')?.value || ""
    };

    // 3. Envío al backend
    try {
        const response = await fetch('http://127.0.0.1:5000/api/cognitivo/evaluar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        console.log("Resultado del servidor:", result);
        return result;

    } catch (error) {
        console.error("Error al enviar el diagnóstico:", error);
        return { status: "error", message: "Error de red" };
    }
}