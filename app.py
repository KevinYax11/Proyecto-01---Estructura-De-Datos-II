from flask import Flask, render_template, request, jsonify
import time
from arbol_b import ArbolB
from proveedor import Proveedor

app = Flask(__name__)

# Inicializar el árbol B vacío
arbol_servicios = ArbolB(grado=3)


@app.route('/api/cargar_datos_ejemplo', methods=['POST'])
def cargar_datos_ejemplo():
    """Carga datos de ejemplo en el árbol B (opcional para demostraciones)"""
    try:
        proveedores_ejemplo = [
            (1, "Juan Pérez", "electricista", 4.5),
            (2, "María González", "plomera", 4.8),
            (3, "Carlos López", "carpintero", 4.2),
            (4, "Ana Rodríguez", "programadora", 4.9),
            (5, "Pedro Martínez", "diseñador", 4.3),
            (6, "Luisa García", "electricista", 4.6),
            (7, "Roberto Silva", "albañil", 4.1),
            (8, "Carmen Torres", "programadora", 4.7),
            (9, "Diego Morales", "plomero", 4.4),
            (10, "Isabel Jiménez", "diseñadora", 4.8),
            (11, "Fernando Castro", "carpintero", 4.0),
            (12, "Sofía Herrera", "electricista", 4.5)
        ]

        agregados = 0
        for id_prov, nombre, servicio, calificacion in proveedores_ejemplo:
            # Solo agregar si el ID no existe
            if not arbol_servicios.buscar(id_prov):
                proveedor = Proveedor(id_prov, nombre, servicio, calificacion)
                arbol_servicios.insertar(id_prov, proveedor.to_dict())
                agregados += 1

        return jsonify({
            'mensaje': f'Se agregaron {agregados} proveedores de ejemplo',
            'total_agregados': agregados
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/proveedores', methods=['GET'])
def obtener_proveedores():
    """Obtiene todos los proveedores ordenados"""
    orden = request.args.get('orden', 'nombre')
    proveedores = arbol_servicios.obtener_todos_ordenados(orden)
    return jsonify(proveedores)


@app.route('/api/proveedores', methods=['POST'])
def agregar_proveedor():
    """Agrega un nuevo proveedor"""
    try:
        datos = request.json

        # Validar datos
        if not all(key in datos for key in ['id', 'nombre', 'servicio', 'calificacion']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400

        # Verificar que el ID no exista
        if arbol_servicios.buscar(datos['id']):
            return jsonify({'error': 'El ID ya existe'}), 400

        # Validar calificación
        if not 1 <= datos['calificacion'] <= 5:
            return jsonify({'error': 'La calificación debe estar entre 1 y 5'}), 400

        # Crear y agregar proveedor
        proveedor = Proveedor(
            datos['id'],
            datos['nombre'],
            datos['servicio'],
            datos['calificacion']
        )

        arbol_servicios.insertar(datos['id'], proveedor.to_dict())

        return jsonify({'mensaje': 'Proveedor agregado exitosamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/buscar/<tipo_servicio>')
def buscar_por_servicio(tipo_servicio):
    """Busca proveedores por tipo de servicio"""
    inicio = time.time()
    resultados = arbol_servicios.buscar_por_servicio(tipo_servicio)
    tiempo_busqueda = time.time() - inicio

    return jsonify({
        'resultados': resultados,
        'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),  # en milisegundos
        'total_encontrados': len(resultados)
    })


@app.route('/api/buscar_id/<int:id_proveedor>')
def buscar_por_id(id_proveedor):
    """Busca un proveedor por ID"""
    inicio = time.time()
    resultado = arbol_servicios.buscar(id_proveedor)
    tiempo_busqueda = time.time() - inicio

    if resultado:
        return jsonify({
            'resultado': resultado,
            'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),
            'encontrado': True
        })
    else:
        return jsonify({
            'mensaje': 'Proveedor no encontrado',
            'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),
            'encontrado': False
        })


@app.route('/api/comparar_busqueda/<tipo_servicio>')
def comparar_busqueda(tipo_servicio):
    """Compara búsqueda en árbol B vs búsqueda lineal"""
    # Obtener todos los proveedores para búsqueda lineal
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()

    # Búsqueda con árbol B
    inicio_arbol = time.time()
    resultados_arbol = arbol_servicios.buscar_por_servicio(tipo_servicio)
    tiempo_arbol = time.time() - inicio_arbol

    # Búsqueda lineal
    inicio_lineal = time.time()
    resultados_lineal = []
    for proveedor in todos_proveedores:
        if proveedor['servicio'].lower() == tipo_servicio.lower():
            resultados_lineal.append(proveedor)
    tiempo_lineal = time.time() - inicio_lineal

    return jsonify({
        'arbol_b': {
            'resultados': resultados_arbol,
            'tiempo': round(tiempo_arbol * 1000, 2),
            'total': len(resultados_arbol)
        },
        'busqueda_lineal': {
            'resultados': resultados_lineal,
            'tiempo': round(tiempo_lineal * 1000, 2),
            'total': len(resultados_lineal)
        },
        'mejora_rendimiento': round((tiempo_lineal / tiempo_arbol) if tiempo_arbol > 0 else 1, 2)
    })


@app.route('/api/estadisticas')
def obtener_estadisticas():
    """Obtiene estadísticas del árbol B"""
    stats = arbol_servicios.obtener_estadisticas()

    # Obtener tipos de servicios únicos
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()
    servicios = {}
    for proveedor in todos_proveedores:
        servicio = proveedor['servicio']
        if servicio in servicios:
            servicios[servicio] += 1
        else:
            servicios[servicio] = 1

    stats['servicios_disponibles'] = servicios
    return jsonify(stats)


@app.route('/api/servicios_unicos')
def obtener_servicios_unicos():
    """Obtiene la lista de tipos de servicios únicos"""
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()
    servicios_unicos = set()
    for proveedor in todos_proveedores:
        servicios_unicos.add(proveedor['servicio'])

    return jsonify(sorted(list(servicios_unicos)))


if __name__ == '__main__':
    app.run(debug=True, port=5000)