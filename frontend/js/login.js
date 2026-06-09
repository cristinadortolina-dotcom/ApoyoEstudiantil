document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita que la página se recargue automáticamente

    // 1. Obtener los elementos del DOM usando los IDs del HTML
    const correo = document.getElementById('correo').value.trim();
    const contrasena = document.getElementById('clave').value; // Lee de id="clave" y guarda en 'contrasena'
    const mensajeError = document.getElementById('mensaje-error');
    const btnLogin = document.getElementById('btn-login');

    // Ocultar cualquier error previo y deshabilitar el botón temporalmente
    mensajeError.style.display = 'none';
    btnLogin.innerText = 'Cargando...';
    btnLogin.disabled = true;

    try {
        console.log("=== [FRONTEND] 1. Datos capturados ===");
        console.log("Correo:", correo);
        console.log("Contrasena:", contrasena); // <-- Línea 18: Ahora sí coincide perfectamente

        // 2. Enviar la petición al backend de Flask
        const respuesta = await fetch('http://127.0.0.1:5000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                correo: correo,
                contraseña: contrasena // Envía la variable 'contrasena' con la etiqueta 'contraseña'
            })
        });

        console.log("=== [FRONTEND] 2. Respuesta de red recibida ===");
        console.log("Código de estado HTTP:", respuesta.status);

        const datos = await respuesta.json();
        console.log("Cuerpo de la respuesta JSON:", datos);

        // 3. Evaluar la respuesta del servidor
        if (respuesta.status === 200 && datos.status === "success") {
            console.log("=== [FRONTEND] 3. Éxito, redirigiendo... ===");
            localStorage.setItem('usuario_id', datos.id_usuario);
            localStorage.setItem('usuario_nombre', datos.nombre);
            localStorage.setItem('usuario_proposito', datos.proposito);
            
            // Redirección limpia subiendo un nivel de carpeta
            window.location.href = 'index.html'; 
        } else {
            mostrarError(datos.message || "Credenciales incorrectas.");
        }

    } catch (error) {
        console.error("=== [FRONTEND] CLAVE DE ERROR EN RED ===");
        console.error(error);
        mostrarError("No se pudo conectar con el servidor.");
    } finally {
        // Restablecer el estado del botón
        btnLogin.innerText = 'Ingresar';
        btnLogin.disabled = false;
    }
});

// Función auxiliar para mostrar alertas visuales en la interfaz
function mostrarError(mensaje) {
    const mensajeError = document.getElementById('mensaje-error');
    if (mensajeError) {
        mensajeError.innerText = mensaje;
        mensajeError.style.display = 'block';
    }
}