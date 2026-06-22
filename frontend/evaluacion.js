// Configuración global del endpoint
const API_URL = "http://127.0.0.1:5000"; // Ajustado a tu puerto estándar de Flask (5000)

document.addEventListener("DOMContentLoaded", () => {
    const formTest = document.getElementById("form-test-cognitivo"); // ID de tu formulario HTML
    const btnVolverInicio = document.getElementById("btnVolverInicio"); // ID del botón de inicio

    // =================================================================
    // INTEGRACIÓN OPCIÓN 1: CONTROL DEL BOTÓN VOLVER AL INICIO
    // =================================================================
    if (btnVolverInicio) {
        btnVolverInicio.addEventListener("click", () => {
            window.location.href = "index.html"; 
        });
    }
    
    if (formTest) {
        formTest.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            // 1. Recolectar datos del formulario dinámicamente
            const formData = new FormData(formTest);
            const respuestas = {};
            
            // Asumiendo que tus inputs/selects tienen name="p1", name="p2", etc.
            for (let i = 1; i <= 9; i++) {
                respuestas[`p${i}`] = formData.get(`p${i}`) || "Nunca";
            }

            const datosPeticion = {
                usuario_id: localStorage.getItem("usuario_id") || "estudiante_luz_123", // ID dinámico o de prueba
                respuestas: respuestas,
                bloqueo: formData.get("bloqueo") || "Ninguno",
                nivel: formData.get("nivel") || "Pregrado",
                proposito: formData.get("proposito") || "General"
            };

            try {
                // 2. Enviar respuestas al backend para su evaluación e interpretación
                const response = await fetch(`${API_URL}/api/cognitivo/evaluar`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(datosPeticion)
                });

                const resultado = await response.json();

                if (resultado.status === "success") {
                    console.log("[Test Exitoso]:", resultado.resultados);
                    
                    // --- Cambiar de pantallas (Ocultar Formulario / Mostrar Resultados) ---
                    const testScreen = document.getElementById("testScreen");
                    const resultsScreen = document.getElementById("resultsScreen");
                    if (testScreen) testScreen.style.display = "none";
                    if (resultsScreen) resultsScreen.style.display = "block";

                    // =================================================================
                    // INTEGRACIÓN OPCIÓN 2: RENDERIZAR EL DIAGNÓSTICO PERSONALIZADO
                    // =================================================================
                    const diagContainer = document.getElementById("diagnostico-container");
                    const diagTexto = document.getElementById("diagnostico-texto");
                    
                    if (diagContainer && diagTexto && resultado.diagnostico) {
                        diagTexto.textContent = resultado.diagnostico;
                        diagContainer.style.display = "block";
                    }
                    
                    // 3. Renderizar tu tabla de resultados tradicional
                    mostrarTablaResultados(resultado.resultados);
                    
                    // 4. EJECUCIÓN AUTOMÁTICA DE EJERCICIOS RECOMENDADOS
                    identificarYBuscarEjercicios(resultado.resultados);

                } else {
                    alert("Error al procesar el test: " + resultado.message);
                }

            } catch (error) {
                console.error("Error en la conexión con el servidor:", error);
                alert("No se pudo conectar con el servidor backend.");
            }
        });
    }
});

/**
 * Identifica qué áreas cognitivas necesitan refuerzo ("Oportunidad")
 * y solicita los ejercicios correspondientes al backend.
 */
function identificarYBuscarEjercicios(resultados) {
    // Mapeo para transformar los nombres del backend a las categorías de tus rutas de Flask
    const mapeoCategorias = {
        "Atención": "atencion",
        "Funciones Ejecutivas": "ejecutivas",
        "Memoria": "memoria",
        "Orientación": "orientacion"
    };

    // Limpiar el contenedor de ejercicios antes de agregar nuevos
    const contenedorEjercicios = document.getElementById("contenedor-ejercicios");
    if (contenedorEjercicios) contenedorEjercicios.innerHTML = "";

    let tieneOportunidades = false;

    // Iterar sobre las dimensiones del test
    Object.entries(resultados).forEach(async ([nombreArea, datos]) => {
        if (datos.estado === "Oportunidad") {
            tieneOportunidades = true;
            const categoriaRuta = mapeoCategorias[nombreArea];
            console.log(`[Plan de Entrenamiento]: Detectada oportunidad en ${nombreArea}. Buscando ejercicios...`);
            
            // Consumir el endpoint GET /api/ejercicios/<categoria> de tu app.py
            try {
                const response = await fetch(`${API_URL}/api/ejercicios/${categoriaRuta}`);
                const dataEjercicios = await response.json();

                if (dataEjercicios.status === "success") {
                    renderizarEjerciciosEnPantalla(nombreArea, dataEjercicios.data);
                }
            } catch (err) {
                console.error(`Error al traer ejercicios de ${categoriaRuta}:`, err);
            }
        }
    });

    // Si pasados unos segundos determinamos que no hay oportunidades, mostrar mensaje de éxito
    setTimeout(() => {
        if (!tieneOportunidades && contenedorEjercicios) {
            contenedorEjercicios.innerHTML = `
                <h2>📚 Plan de Estimulación Recomendado</h2>
                <div class="instruccion-ejercicio" style="border-left-color: #48bb78; background-color: #f0fff4; padding: 15px; border-radius: 6px;">
                    <strong>¡Felicitaciones!</strong> Has mantenido un rendimiento óptimo en todas las áreas cognitivas evaluadas hoy. No requieres ejercicios de nivelación inmediatos.
                </div>
            `;
        }
    }, 500);
}

/**
 * Renderiza visualmente los ejercicios devueltos por Firestore en el DOM
 */
function renderizarEjerciciosEnPantalla(areaNombre, listaEjercicios) {
    const contenedorEjercicios = document.getElementById("contenedor-ejercicios");
    if (!contenedorEjercicios) return;

    // Si es el primer ejercicio que entra, agregamos el título general
    if (contenedorEjercicios.innerHTML === "") {
        contenedorEjercicios.innerHTML = `<h2>📚 Plan de Estimulación Recomendado</h2>`;
    }

    // Crear una sección para el área cognitiva si no existe
    const seccionArea = document.createElement("div");
    seccionArea.classList.add("seccion-ejercicios-area");
    seccionArea.innerHTML = `<h3>💡 Ejercicios de refuerzo para: ${areaNombre}</h3>`;

    const grid = document.createElement("div");
    grid.classList.add("ejercicios-grid");

    listaEjercicios.forEach(ejercicio => {
        const card = document.createElement("div");
        card.classList.add("card-ejercicio");
        card.innerHTML = `
            <div class="card-ejercicio-header">
                <h4>${ejercicio.nombre || "Ejercicio Cognitivo"}</h4>
                <span class="badge-nivel">${ejercicio.nivel || "General"}</span>
            </div>
            <p class="descripcion-ejercicio">${ejercicio.descripcion || "Realiza la actividad sugerida."}</p>
            ${ejercicio.instruccion ? `
                <div class="instruccion-ejercicio">
                    <strong>Instrucción práctica:</strong> ${ejercicio.instruccion}
                </div>` : ''}
            <button class="btn-completar-ejercicio" onclick="alert('¡Excelente trabajo! Ejercicio registrado.')">
                Marcar como Realizado
            </button>
        `;
        grid.appendChild(card);
    });

    seccionArea.appendChild(grid);
    contenedorEjercicios.appendChild(seccionArea);
}

/**
 * Tu función existente para rellenar la tabla de resultados
 */
function mostrarTablaResultados(resultados) {
    console.log("Renderizando tabla de resultados tradicional...", resultados);
    const tbody = document.getElementById("resultsTableBody");
    if (!tbody) return;
    
    tbody.innerHTML = "";
    for (const [area, info] of Object.entries(resultados)) {
        tbody.innerHTML += `
            <tr>
                <td><strong>${area}</strong></td>
                <td>${info.puntuacion} / 5.0</td>
                <td><span class="${info.estado === 'Fortaleza' ? 'badge-fortaleza' : 'badge-oportunidad'}">
                    ${info.estado}
                </span></td>
            </tr>`;
    }
}