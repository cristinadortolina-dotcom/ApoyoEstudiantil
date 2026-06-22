const API_URL = "http://127.0.0.1:5000";
const USUARIO_ID = localStorage.getItem("usuario_id");

// Si alguien entra a la página sin haber iniciado sesión, lo sacamos de inmediato
if (!USUARIO_ID) {
    window.location.href = "login.html";
}

let datosOriginales = {};

document.addEventListener("DOMContentLoaded", () => {
    const formPerfil = document.getElementById("formPerfil");
    const btnRegresarMenu = document.getElementById("btnRegresarMenu");
    const btnCerrarSesion = document.getElementById("btnCerrarSesion");
    
    const btnEditar = document.getElementById("btnEditar");
    const btnGuardar = document.getElementById("btnGuardar");
    const btnCancelar = document.getElementById("btnCancelar");
    
    const perfilNombre = document.getElementById("perfilNombre");
    const perfilCorreo = document.getElementById("perfilCorreo");
    const perfilNivel = document.getElementById("perfilNivel");
    const perfilProposito = document.getElementById("perfilProposito");

    // ¡LLAMADA AUTOMÁTICA! Si estamos en la página del perfil, cargamos los datos de inmediato
    if (formPerfil) {
        cargarDatosPerfil();
    }

    // ACCIÓN: Habilitar campos seleccionados al hacer clic en Modificar
    if (btnEditar) {
        btnEditar.addEventListener("click", () => {
            // Respaldamos los valores por si decide cancelar
            datosOriginales = {
                nombre: perfilNombre.value,
                nivel_academico: perfilNivel.value
            };

            // Habilitamos SOLO los campos modificables
            perfilNombre.disabled = false;
            perfilNivel.disabled = false;

            // Cambiamos los botones visibles
            btnEditar.style.display = "none";
            btnGuardar.style.display = "block";
            btnCancelar.style.display = "block";
        });
    }

    // ACCIÓN: Cancelar los cambios y restablecer valores
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            perfilNombre.value = datosOriginales.nombre;
            perfilNivel.value = datosOriginales.nivel_academico;

            perfilNombre.disabled = true;
            perfilNivel.disabled = true;

            btnEditar.style.display = "block";
            btnGuardar.style.display = "none";
            btnCancelar.style.display = "none";
        });
    }

    if (btnRegresarMenu) {
        btnRegresarMenu.addEventListener("click", () => {
            window.location.href = "index.html"; // Regresa físicamente al archivo index.html
        });
    }

    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener("click", () => {
            localStorage.clear();
            alert("Sesión cerrada correctamente.");
            window.location.href = "login.html";
        });
    }

    // Función para obtener y pintar toda la información recolectada del estudiante
    // Función para obtener y pintar toda la información recolectada del estudiante
    async function cargarDatosPerfil() {
        try {
            const res = await fetch(`${API_URL}/api/usuario/${USUARIO_ID}`);
            
            // Si la respuesta no es un código 200-299, atrapamos el error del servidor
            if (!res.ok) {
                throw new Error(`El servidor respondió con código ${res.status}`);
            }
            
            const data = await res.json();

            if (data.status === "success") {
                // Rellenamos todos los campos del formulario
                if (perfilNombre) perfilNombre.value = data.nombre || "";
                if (perfilCorreo) perfilCorreo.value = data.correo || "";
                if (perfilNivel) perfilNivel.value = data.nivel_academico || "Pregrado";
                if (perfilProposito) perfilProposito.value = data.proposito || "No definido";

                // Construimos el Plan Cognitivo Dinámico
                const contenedorPlan = document.getElementById("planCognitivoContenedor");
                if (contenedorPlan) {
                    contenedorPlan.innerHTML = "";
                    if (!data.plan_cognitivo || data.plan_cognitivo.length === 0) {
                        contenedorPlan.innerHTML = "<p style='color: #64748b; font-size: 0.9rem;'>No posees áreas críticas pendientes. ¡Tu rendimiento está optimizado!</p>";
                    } else {
                        contenedorPlan.innerHTML = "<p style='margin-bottom: 8px; font-weight:600; font-size:0.9rem;'>Áreas bajo entrenamiento activo:</p>";
                        data.plan_cognitivo.forEach(area => {
                            contenedorPlan.innerHTML += `<span style="display:inline-block; background-color:#feebc8; color:#c05621; padding:3px 8px; border-radius:10px; margin:2px; font-size:0.8rem; font-weight:bold;">Focus: ${area}</span>`;
                        });
                    }
                }
            } else {
                alert("Error detectado en la base de datos: " + data.message);
            }
        } catch (error) {
            console.error("Error al cargar perfil:", error);
            alert("Detalle del problema: " + error.message + "\n\n1. Asegúrate de que ejecutaste tu archivo Python.\n2. Presiona F12 e inspecciona la consola para más detalles.");
        }
    }

    // Guardar los datos modificados en la Base de Datos
    if (formPerfil) {
        formPerfil.addEventListener("submit", async (e) => {
            e.preventDefault();

            const datosActualizados = {
                nombre: perfilNombre.value,
                nivel_academico: perfilNivel.value
            };

            try {
                const res = await fetch(`${API_URL}/api/usuario/${USUARIO_ID}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosActualizados)
                });

                const data = await res.json();
                if (data.status === "success") {
                    localStorage.setItem('usuario_nombre', datosActualizados.nombre);
                    alert("Datos actualizados con éxito.");

                    // Volvemos a bloquear los campos a modo lectura segura
                    perfilNombre.disabled = true;
                    perfilNivel.disabled = true;
                    btnEditar.style.display = "block";
                    btnGuardar.style.display = "none";
                    btnCancelar.style.display = "none";
                } else {
                    alert("Error al actualizar: " + data.message);
                }
            } catch (error) {
                console.error("Error al guardar perfil:", error);
                alert("Hubo un problema de conexión con el servidor Flask.");
            }
        });
    }
});