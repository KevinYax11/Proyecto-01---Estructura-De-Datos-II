// Variables globales
let proveedoresData = [];
let serviciosUnicos = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarServiciosUnicos();
    cargarTodosProveedores();
    configurarFormulario();
    showTab('buscar'); // Mostrar pestaña por defecto
});

// Gestión de pestañas
function showTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remover clase active de todos los botones
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Mostrar pestaña seleccionada
    document.getElementById(tabName).classList.add('active');

    // Marcar botón como activo
    event.target.classList.add('active');

    // Cargar datos específicos según la pestaña
    switch(tabName) {
        case 'todos':
            cargarTodosProveedores();
            break;
        case 'estadisticas':
            cargarEstadisticas();
            break;
    }
}

// Cargar servicios únicos para los selectores
async function cargarServiciosUnicos() {
    try {
        showLoading();
        const response = await fetch('/api/servicios_unicos');
        serviciosUnicos = await response.json();

        const servicioSelect = document.getElementById('servicioSelect');
        const servicioComparar = document.getElementById('servicioComparar');

        // Limpiar opciones existentes (excepto la primera)
        servicioSelect.innerHTML = '<option value="">Seleccione un servicio</option>';
        servicioComparar.innerHTML = '<option value="">Seleccione un servicio</option>';

        // Agregar servicios únicos
        serviciosUnicos.forEach(servicio => {
            const option1 = new Option(servicio.charAt(0).toUpperCase() + servicio.slice(1), servicio);
            const option2 = new Option(servicio.charAt(0).toUpperCase() + servicio.slice(1), servicio);
            servicioSelect.add(option1);
            servicioComparar.add(option2);
        });

    } catch (error) {
        console.error('Error cargando servicios:', error);
        showMessage('Error cargando servicios', 'error');
    } finally {
        hideLoading();
    }
}

// Buscar proveedores por servicio
async function buscarPorServicio() {
    const servicio = document.getElementById('servicioSelect').value;

    if (!servicio) {
        showMessage('Por favor seleccione un tipo de servicio', 'warning');
        return;
    }

    try {
        showLoading();
        const response = await fetch(`/api/buscar/${servicio}`);
        const data = await response.json();

        mostrarResultadosBusqueda(data.resultados, {
            tiempo: data.tiempo_busqueda,
            total: data.total_encontrados,
            tipo: 'servicio',
            termino: servicio
        });

    } catch (error) {
        console.error('Error en búsqueda por servicio:', error);
        showMessage('Error en la búsqueda', 'error');
    } finally {
        hideLoading();
    }
}

// Buscar proveedor por ID
async function buscarPorId() {
    const id = document.getElementById('idInput').value;

    if (!id) {
        showMessage('Por favor ingrese un ID', 'warning');
        return;
    }

    try {
        showLoading();
        const response = await fetch(`/api/buscar_id/${id}`);
        const data = await response.json();

        if (data.encontrado) {
            mostrarResultadosBusqueda([data.resultado], {
                tiempo: data.tiempo_busqueda,
                total: 1,
                tipo: 'id',
                termino: id
            });
        } else {
            mostrarResultadosBusqueda([], {
                tiempo: data.tiempo_busqueda,
                total: 0,
                tipo: 'id',
                termino: id
            });
        }

    } catch (error) {
        console.error('Error en búsqueda por ID:', error);
        showMessage('Error en la búsqueda', 'error');
    } finally {
        hideLoading();
    }
}

// Mostrar resultados de búsqueda
function mostrarResultadosBusqueda(resultados, metadata) {
    const container = document.getElementById('resultadosBusqueda');

    let html = `
        <div class="search-metadata">
            <h3>Resultados de búsqueda por ${metadata.tipo}: "${metadata.termino}"</h3>
            <p>Encontrados: <strong>${metadata.total}</strong> resultados en <strong>${metadata.tiempo} ms</strong></p>
        </div>
    `;

    if (resultados.length === 0) {
        html += '<div class="no-results"><p>No se encontraron proveedores.</p></div>';
    } else {
        html += '<div class="providers-grid">';
        resultados.forEach(proveedor => {
            html += crearTarjetaProveedor(proveedor);
        });
        html += '</div>';
    }

    container.innerHTML = html;
}

// Crear tarjeta de proveedor
function crearTarjetaProveedor(proveedor) {
    const estrellas = generarEstrellas(proveedor.calificacion);

    return `
        <div class="provider-card">
            <h3>${proveedor.nombre}</h3>
            <p><strong>ID:</strong> ${proveedor.id}</p>
            <p><strong>Servicio:</strong> ${proveedor.servicio}</p>
            <div class="provider-rating">
                <span class="stars">${estrellas}</span>
                <span><strong>${proveedor.calificacion}</strong>/5</span>
            </div>
        </div>
    `;
}

// Generar estrellas visuales
function generarEstrellas(calificacion) {
    const estrellaLlena = '⭐';
    const estrellaVacia = '☆';
    let estrellas = '';

    for (let i = 1; i <= 5; i++) {
        estrellas += i <= Math.round(calificacion) ? estrellaLlena : estrellaVacia;
    }

    return estrellas;
}

// Cargar datos de ejemplo (opcional para demostraciones)
async function cargarDatosEjemplo() {
    try {
        showLoading();
        const response = await fetch('/api/cargar_datos_ejemplo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(`${data.mensaje}`, 'success');
            cargarServiciosUnicos(); // Actualizar servicios disponibles
            cargarTodosProveedores(); // Actualizar lista de proveedores
        } else {
            showMessage(data.error || 'Error cargando datos de ejemplo', 'error');
        }

    } catch (error) {
        console.error('Error cargando datos de ejemplo:', error);
        showMessage('Error cargando datos de ejemplo', 'error');
    } finally {
        hideLoading();
    }
}

// Configurar formulario
function configurarFormulario() {
    const form = document.getElementById('proveedorForm');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = {
            id: parseInt(document.getElementById('nuevoId').value),
            nombre: document.getElementById('nuevoNombre').value.trim(),
            servicio: document.getElementById('nuevoServicio').value.trim().toLowerCase(),
            calificacion: parseFloat(document.getElementById('nuevaCalificacion').value)
        };

        // Validaciones básicas
        if (!formData.nombre || !formData.servicio) {
            showMessage('Por favor complete todos los campos', 'warning');
            return;
        }

        if (formData.calificacion < 1 || formData.calificacion > 5) {
            showMessage('La calificación debe estar entre 1 y 5', 'warning');
            return;
        }

        try {
            showLoading();
            const response = await fetch('/api/proveedores', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('Proveedor agregado exitosamente', 'success');
                form.reset();
                cargarServiciosUnicos(); // Actualizar servicios
                cargarTodosProveedores(); // Actualizar lista
            } else {
                showMessage(data.error || 'Error al agregar proveedor', 'error');
            }

        } catch (error) {
            console.error('Error agregando proveedor:', error);
            showMessage('Error al agregar proveedor', 'error');
        } finally {
            hideLoading();
        }
    });
}

// Cargar todos los proveedores
async function cargarTodosProveedores() {
    try {
        const orden = document.getElementById('ordenSelect')?.value || 'nombre';
        const response = await fetch(`/api/proveedores?orden=${orden}`);
        proveedoresData = await response.json();

        const container = document.getElementById('todosProveedores');

        if (proveedoresData.length === 0) {
            container.innerHTML = '<p>No hay proveedores registrados.</p>';
            return;
        }

        let html = '';
        proveedoresData.forEach(proveedor => {
            html += crearTarjetaProveedor(proveedor);
        });

        container.innerHTML = html;

    } catch (error) {
        console.error('Error cargando proveedores:', error);
        showMessage('Error cargando proveedores', 'error');
    }
}

// Comparar rendimiento de búsqueda
async function compararBusqueda() {
    const servicio = document.getElementById('servicioComparar').value;

    if (!servicio) {
        showMessage('Por favor seleccione un servicio para comparar', 'warning');
        return;
    }

    try {
        showLoading();
        const response = await fetch(`/api/comparar_busqueda/${servicio}`);
        const data = await response.json();

        mostrarResultadosComparacion(data, servicio);

    } catch (error) {
        console.error('Error en comparación:', error);
        showMessage('Error en la comparación', 'error');
    } finally {
        hideLoading();
    }
}

// Mostrar resultados de comparación
function mostrarResultadosComparacion(data, servicio) {
    const container = document.getElementById('resultadosComparacion');

    const mejora = data.mejora_rendimiento;
    const mejoraTexto = mejora > 1 ?
        `El árbol B es ${mejora.toFixed(2)}x más rápido` :
        'Ambos métodos tienen rendimiento similar';

    container.innerHTML = `
        <div class="comparison-header">
            <h3>Comparación de búsqueda para: "${servicio}"</h3>
            <div class="performance-improvement">
                🚀 ${mejoraTexto}
            </div>
        </div>

        <div class="comparison-card">
            <div class="method-result">
                <h4>🌳 Árbol B</h4>
                <div class="metric">
                    <span>Tiempo de búsqueda:</span>
                    <span class="metric-value">${data.arbol_b.tiempo} ms</span>
                </div>
                <div class="metric">
                    <span>Resultados encontrados:</span>
                    <span class="metric-value">${data.arbol_b.total}</span>
                </div>
                <div class="metric">
                    <span>Estructura utilizada:</span>
                    <span class="metric-value">Árbol B (Grado 3)</span>
                </div>
            </div>

            <div class="method-result linear">
                <h4>📋 Búsqueda Lineal</h4>
                <div class="metric">
                    <span>Tiempo de búsqueda:</span>
                    <span class="metric-value">${data.busqueda_lineal.tiempo} ms</span>
                </div>
                <div class="metric">
                    <span>Resultados encontrados:</span>
                    <span class="metric-value">${data.busqueda_lineal.total}</span>
                </div>
                <div class="metric">
                    <span>Estructura utilizada:</span>
                    <span class="metric-value">Lista secuencial</span>
                </div>
            </div>
        </div>

        <div style="margin-top: 20px;">
            <h4>Análisis de Escalabilidad:</h4>
            <p>• Con <strong>1,000 proveedores</strong>, el Árbol B mantendría un rendimiento logarítmico O(log n)</p>
            <p>• La búsqueda lineal degradaría a O(n), siendo significativamente más lenta</p>
            <p>• Los árboles B son especialmente eficientes para grandes volúmenes de datos</p>
        </div>
    `;
}

// Cargar estadísticas
async function cargarEstadisticas() {
    try {
        showLoading();
        const response = await fetch('/api/estadisticas');
        const stats = await response.json();

        mostrarEstadisticas(stats);

    } catch (error) {
        console.error('Error cargando estadísticas:', error);
        showMessage('Error cargando estadísticas', 'error');
    } finally {
        hideLoading();
    }
}

// Mostrar estadísticas
function mostrarEstadisticas(stats) {
    const container = document.getElementById('estadisticasInfo');

    let serviciosHtml = '';
    for (const [servicio, cantidad] of Object.entries(stats.servicios_disponibles)) {
        serviciosHtml += `
            <div class="service-item">
                <span>${servicio.charAt(0).toUpperCase() + servicio.slice(1)}</span>
                <span class="service-count">${cantidad}</span>
            </div>
        `;
    }

    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">${stats.total_proveedores}</span>
                <span class="stat-label">Proveedores Registrados</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">${stats.total_nodos}</span>
                <span class="stat-label">Nodos en el Árbol</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">${stats.altura}</span>
                <span class="stat-label">Altura del Árbol</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">${stats.grado}</span>
                <span class="stat-label">Grado del Árbol B</span>
            </div>
        </div>

        <div class="services-breakdown">
            <h4>Distribución por Tipo de Servicio</h4>
            ${serviciosHtml}
        </div>

        <div style="margin-top: 20px; padding: 16px; background: var(--bg-color); border-radius: 8px;">
            <h4>Características del Árbol B implementado:</h4>
            <p>• <strong>Grado mínimo:</strong> ${stats.grado} (cada nodo puede tener entre ${stats.grado-1} y ${2*stats.grado-1} claves)</p>
            <p>• <strong>Balanceado automáticamente:</strong> Todas las hojas están al mismo nivel</p>
            <p>• <strong>Búsqueda eficiente:</strong> Complejidad O(log n)</p>
            <p>• <strong>Inserción ordenada:</strong> Mantiene el orden de las claves automáticamente</p>
        </div>
    `;
}

// Utilidades para mensajes y loading
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('mensaje');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove('hidden');

    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 4000);
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// Manejo de errores globales
window.addEventListener('error', function(e) {
    console.error('Error global:', e.error);
    hideLoading();
});

// Manejo de promesas rechazadas
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promesa rechazada:', e.reason);
    hideLoading();
});