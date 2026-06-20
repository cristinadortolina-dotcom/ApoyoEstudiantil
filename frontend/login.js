document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('login-form');

    if (formulario) {
        formulario.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita que la página se recargue automáticamente

            // 1. Obtener los elementos del DOM usando los IDs del HTML
            const correo = document.getElementById('correo').value.trim();
            const contrasena = document.getElementById('clave').value; 
            const mensajeError = document.getElementById('mensaje-error');
            const btnLogin = document.getElementById('btn-login');

            // Ocultar cualquier error previo y deshabilitar el botón temporalmente
            if (mensajeError) mensajeError.style.display = 'none';
            if (btnLogin) {
                btnLogin.innerText = 'Cargando...';
                btnLogin.disabled = true;
            }

            try {
                console.log("=== [FRONTEND] 1. Datos capturados ===");
                console.log("Correo:", correo);

                // 2. Enviar la petición al backend local de Flask
                const respuesta = await fetch('http://127.0.0.1:5000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        correo: correo,
                        contraseña: contrasena 
                    })
                });

                console.log("=== [FRONTEND] 2. Respuesta de red recibida ===");
                console.log("Código de estado HTTP:", respuesta.status);

                const datos = await respuesta.json();
                console.log("Cuerpo de la respuesta JSON:", datos);

                // 3. Evaluar la respuesta usando las claves reales que devuelve tu backend
                if (respuesta.ok && (datos.exito === true || datos.id_usuario)) {
                    console.log("=== [FRONTEND] 3. Éxito, guardando sesión y redirigiendo... ===");
                    
                    // Guardamos el ID exacto que tu index.html va a validar al cargar
                    localStorage.setItem('usuario_id', datos.id_usuario);
                    localStorage.setItem('usuario_nombre', datos.nombre || '');
                    localStorage.setItem('usuario_proposito', datos.proposito || '');
                    
                    alert('¡Inicio de sesión exitoso!');
                    window.location.href = 'index.html'; 
                } else {
                    mostrarError(datos.mensaje || datos.error || "Correo o contraseña incorrectos.");
                }

            } catch (error) {
                console.error("=== [FRONTEND] CLAVE DE ERROR EN RED ===");
                console.error(error);
                mostrarError("No se pudo conectar con el servidor. Asegúrate de que Flask esté corriendo.");
            } finally {
                // Restablecer el estado del botón de manera segura
                if (btnLogin) {
                    btnLogin.innerText = 'Ingresar';
                    btnLogin.disabled = false;
                }
            }
        });
    }
});

// Función auxiliar para mostrar alertas visuales en la interfaz
function mostrarError(mensaje) {
    const mensajeError = document.getElementById('mensaje-error');
    if (mensajeError) {
        mensajeError.innerText = mensaje;
        mensajeError.style.display = 'block';
    } else {
        alert(mensaje); // Respaldo si el contenedor no existe en el HTML
    }
}