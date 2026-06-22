document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('login-form');

    if (formulario) {
        formulario.addEventListener('submit', async (e) => {
            e.preventDefault(); 

            // 1. Obtener valores usando los IDs correctos del HTML
            const correo = document.getElementById('correo').value.trim();
            const clave = document.getElementById('clave').value; // Usamos 'clave' porque así está en login.html
            const btnLogin = document.getElementById('btn-login');

            // Feedback visual
            if (btnLogin) {
                btnLogin.innerText = 'Ingresando...';
                btnLogin.disabled = true;
            }

            try {
                // 2. Realizar la petición. 
                // Asegúrate de que la ruta sea '/api/login' y enviamos 'password'
                const respuesta = await fetch('http://127.0.0.1:5000/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        correo: correo,
                        password: clave // <--- ESTA ES LA CLAVE: El backend necesita "password"
                    })
                });

                const datos = await respuesta.json();

                if (respuesta.ok && datos.status === 'success') {
                    // Guardar los datos del usuario para mantener la sesión
                    localStorage.setItem("usuario_id", datos.usuario_id);
                    localStorage.setItem("usuario_nombre", datos.nombre || "Estudiante");
                    
                    alert('¡Bienvenido!');
                    window.location.href = "index.html";
                } else {
                    mostrarError(datos.message || "Credenciales incorrectas.");
                }

            } catch (error) {
                console.error("Error de conexión:", error);
                mostrarError("No se pudo conectar con el servidor Flask.");
            } finally {
                if (btnLogin) {
                    btnLogin.innerText = 'Ingresar';
                    btnLogin.disabled = false;
                }
            }
        });
    }
});

// Función auxiliar para errores
function mostrarError(mensaje) {
    const mensajeError = document.getElementById('mensaje-error');
    if (mensajeError) {
        mensajeError.innerText = mensaje;
        mensajeError.style.display = 'block';
    } else {
        alert(mensaje);
    }
}