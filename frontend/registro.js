document.getElementById('registroForm').addEventListener('submit', async (e) => {
    // Evitamos que el formulario se envíe de la forma tradicional
    e.preventDefault();

    // Capturamos los valores de los inputs
    const datos = {
    nombre: document.getElementById('nombre').value,
    correo: document.getElementById('correo').value,
    rango_academico: document.getElementById('rango_academico').value,
    password: document.getElementById('password').value // Ahora coincide con el HTML
};

    try {
        // Enviamos los datos al backend mediante una petición POST
        const respuesta = await fetch('http://127.0.0.1:5000/api/registro', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(datos)
        });

        // Convertimos la respuesta del servidor a formato JSON
        const resultado = await respuesta.json();

        // Verificamos si la respuesta fue exitosa (código 200 o 201)
        if (respuesta.ok) {
            alert('¡Registro exitoso! Ahora inicia sesión.');
            // Redirigimos al usuario al login
            window.location.href = 'login.html';
        } else {
            // Si el servidor devolvió un error (ej. 400), mostramos el mensaje
            alert('Error: ' + (resultado.error || 'No se pudo completar el registro.'));
        }
    } catch (error) {
        // Si hay un error de conexión (el servidor está apagado, por ejemplo)
        console.error('Error al conectar con el servidor:', error);
        alert('No se pudo conectar con el servidor. Asegúrate de que Flask esté corriendo.');
    }
});