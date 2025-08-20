# Importaciones necesarias para el funcionamiento de la aplicación Flask
from flask import Flask, render_template, request, \
    jsonify  # Flask: framework web, render_template: renderizar HTML, request: manejar peticiones HTTP, jsonify: convertir datos a JSON
import time  # Para medir tiempos de ejecución de búsquedas - si se elimina, no se podrán medir los tiempos de respuesta
from arbol_b import ArbolB  # Importa la clase del árbol B personalizado - CRÍTICO: sin esto la app no funciona
from proveedor import Proveedor  # Importa la clase Proveedor - CRÍTICO: sin esto no se pueden crear objetos proveedor

# Crear la instancia de la aplicación Flask
app = Flask(__name__)  # Crea la aplicación web - CRÍTICO: sin esto no hay servidor web

# Inicializar el árbol B vacío con grado 3
arbol_servicios = ArbolB(
    grado=3)  # Estructura de datos principal que almacena todos los proveedores - CRÍTICO: sin esto no hay almacenamiento de datos


@app.route('/')  # Decorador que define la ruta raíz del sitio web - sin esto no se puede acceder a la página principal
def index():
    """Página principal - renderiza el archivo HTML principal"""
    return render_template(
        'index.html')  # Busca y renderiza el archivo index.html en la carpeta templates - sin esto no hay interfaz de usuario


@app.route('/api/proveedores',
           methods=['GET'])  # Define endpoint GET para obtener proveedores - sin esto no se pueden consultar los datos
def obtener_proveedores():
    """Obtiene todos los proveedores ordenados según el parámetro especificado"""
    orden = request.args.get('orden',
                             'nombre')  # Obtiene el parámetro 'orden' de la URL, por defecto 'nombre' - sin esto siempre ordenaría por nombre
    proveedores = arbol_servicios.obtener_todos_ordenados(
        orden)  # Llama al método del árbol para obtener datos ordenados - CRÍTICO: sin esto no hay datos de respuesta
    return jsonify(
        proveedores)  # Convierte la lista de proveedores a formato JSON para la respuesta HTTP - sin esto el frontend no puede procesar los datos


@app.route('/api/proveedores', methods=[
    'POST'])  # Define endpoint POST para agregar nuevos proveedores - sin esto no se pueden añadir datos
def agregar_proveedor():
    """Agrega un nuevo proveedor al sistema con validaciones completas"""
    try:  # Manejo de errores - sin esto cualquier error crashearía la aplicación
        datos = request.json  # Obtiene los datos JSON del cuerpo de la petición HTTP - CRÍTICO: sin esto no hay datos para procesar

        # Validar que todos los campos requeridos estén presentes
        campos_requeridos = ['id', 'nombre', 'servicio', 'calificacion',
                             'ubicacion']  # Lista de campos obligatorios - sin esto no hay validación de integridad
        if not all(key in datos for key in
                   campos_requeridos):  # Verifica que todos los campos existan - sin esto se podrían insertar datos incompletos
            return jsonify({
                               'error': 'Faltan campos requeridos'}), 400  # Respuesta de error HTTP 400 - sin esto el cliente no sabría qué está mal

        # Verificar que el ID no exista ya en el sistema
        if arbol_servicios.buscar(datos['id']):  # Busca si el ID ya existe - sin esto habría IDs duplicados
            return jsonify({'error': 'El ID ya existe'}), 400  # Error de conflicto - sin esto se sobreescribirían datos

        # Validar que la calificación esté en el rango válido (1-5)
        if not 1 <= datos['calificacion'] <= 5:  # Validación de rango - sin esto podrían haber calificaciones inválidas
            return jsonify({
                               'error': 'La calificación debe estar entre 1 y 5'}), 400  # Error de validación - sin esto datos inconsistentes

        # Validar que la ubicación no esté vacía
        if not datos['ubicacion'].strip():  # Verifica que la ubicación tenga contenido - sin esto ubicaciones vacías
            return jsonify(
                {'error': 'La ubicación es requerida'}), 400  # Error de validación - sin esto datos incompletos

        # Crear objeto Proveedor con los datos validados
        proveedor = Proveedor(  # Instancia un nuevo objeto proveedor - CRÍTICO: sin esto no hay objeto para almacenar
            datos['id'],  # ID único del proveedor
            datos['nombre'],  # Nombre del proveedor
            datos['servicio'],  # Tipo de servicio que ofrece
            datos['calificacion'],  # Calificación del 1 al 5
            datos['ubicacion']  # Ubicación geográfica
        )

        # Insertar el proveedor en el árbol B
        arbol_servicios.insertar(datos['id'],
                                 proveedor.to_dict())  # Almacena en la estructura de datos - CRÍTICO: sin esto no se persisten los datos

        return jsonify({
                           'mensaje': 'Proveedor agregado exitosamente'}), 201  # Respuesta de éxito HTTP 201 - sin esto el cliente no sabría si fue exitoso

    except Exception as e:  # Captura cualquier error no previsto - sin esto errores inesperados crashearían la app
        return jsonify({'error': str(e)}), 500  # Error interno del servidor - sin esto no habría feedback de errores


@app.route(
    '/api/buscar/<tipo_servicio>')  # Endpoint dinámico para buscar por tipo de servicio - sin esto no hay búsqueda por servicio
def buscar_por_servicio(tipo_servicio):
    """Busca todos los proveedores que ofrecen un tipo específico de servicio"""
    inicio = time.time()  # Marca el tiempo de inicio - sin esto no hay medición de rendimiento
    resultados = arbol_servicios.buscar_por_servicio(
        tipo_servicio)  # Ejecuta la búsqueda en el árbol - CRÍTICO: sin esto no hay funcionalidad de búsqueda
    tiempo_busqueda = time.time() - inicio  # Calcula el tiempo transcurrido - sin esto no hay métricas de rendimiento

    return jsonify({  # Retorna respuesta estructurada en JSON
        'resultados': resultados,  # Lista de proveedores encontrados - sin esto no hay datos de respuesta
        'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),
        # Tiempo en milisegundos redondeado - sin esto no hay métricas
        'total_encontrados': len(resultados)  # Contador de resultados - sin esto no hay información de cantidad
    })


@app.route(
    '/api/buscar_id/<int:id_proveedor>')  # Endpoint para buscar por ID específico - sin esto no hay búsqueda por ID
def buscar_por_id(id_proveedor):
    """Busca un proveedor específico por su ID único"""
    inicio = time.time()  # Marca tiempo de inicio para métricas
    resultado = arbol_servicios.buscar(
        id_proveedor)  # Busca directamente por clave en el árbol - CRÍTICO: funcionalidad principal
    tiempo_busqueda = time.time() - inicio  # Calcula tiempo de ejecución

    if resultado:  # Si se encontró el proveedor - sin esta validación habría respuestas inconsistentes
        return jsonify({
            'resultado': resultado,  # Datos del proveedor encontrado
            'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),  # Métricas de rendimiento
            'encontrado': True  # Flag booleano para el frontend
        })
    else:  # Si no se encontró - sin esto no hay manejo de casos negativos
        return jsonify({
            'mensaje': 'Proveedor no encontrado',  # Mensaje descriptivo para el usuario
            'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),  # Métricas incluso en casos negativos
            'encontrado': False  # Flag para indicar resultado negativo
        })


@app.route(
    '/api/buscar_ubicacion/<ubicacion>')  # Endpoint para buscar por ubicación - sin esto no hay filtrado geográfico
def buscar_por_ubicacion(ubicacion):
    """Busca todos los proveedores en una ubicación geográfica específica"""
    inicio = time.time()  # Tiempo de inicio para métricas
    resultados = arbol_servicios.buscar_por_ubicacion(ubicacion)  # Búsqueda por ubicación en el árbol
    tiempo_busqueda = time.time() - inicio  # Cálculo de tiempo transcurrido

    return jsonify({
        'resultados': resultados,  # Lista de proveedores en la ubicación
        'tiempo_busqueda': round(tiempo_busqueda * 1000, 2),  # Métricas de rendimiento
        'total_encontrados': len(resultados)  # Contador de resultados
    })


@app.route(
    '/api/estadisticas')  # Endpoint para obtener estadísticas del sistema - sin esto no hay información analítica
def obtener_estadisticas():
    """Genera estadísticas completas del sistema incluyendo distribución de servicios y ubicaciones"""
    stats = arbol_servicios.obtener_estadisticas()  # Obtiene estadísticas básicas del árbol - sin esto no hay métricas estructurales

    # Obtener todos los proveedores para análisis adicional
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()  # Lista completa de proveedores - CRÍTICO para análisis
    servicios = {}  # Diccionario para contar servicios - sin esto no hay distribución por servicio
    ubicaciones = {}  # Diccionario para contar ubicaciones - sin esto no hay distribución geográfica

    # Procesar cada proveedor para generar estadísticas
    for proveedor in todos_proveedores:  # Itera sobre todos los datos - sin esto no hay análisis completo
        servicio = proveedor['servicio']  # Extrae el tipo de servicio
        ubicacion = proveedor['ubicacion']  # Extrae la ubicación

        # Contar ocurrencias de cada servicio
        servicios[servicio] = servicios.get(servicio,
                                            0) + 1  # Incrementa contador o inicializa en 1 - sin esto no hay conteo
        # Contar ocurrencias de cada ubicación
        ubicaciones[ubicacion] = ubicaciones.get(ubicacion, 0) + 1  # Incrementa contador o inicializa en 1

    # Agregar estadísticas adicionales al objeto de respuesta
    stats[
        'servicios_disponibles'] = servicios  # Distribución de tipos de servicios - sin esto no hay análisis por categoría
    stats['ubicaciones_disponibles'] = ubicaciones  # Distribución geográfica - sin esto no hay análisis geográfico
    return jsonify(stats)  # Retorna todas las estadísticas en formato JSON


@app.route(
    '/api/servicios_unicos')  # Endpoint para obtener lista única de servicios - sin esto no hay opciones para filtros
def obtener_servicios_unicos():
    """Obtiene la lista de todos los tipos de servicios únicos disponibles en el sistema"""
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()  # Obtiene todos los proveedores
    servicios_unicos = set()  # Conjunto para eliminar duplicados automáticamente - sin esto habría servicios repetidos

    # Extraer servicios únicos
    for proveedor in todos_proveedores:  # Itera sobre cada proveedor
        servicios_unicos.add(proveedor['servicio'])  # Agrega al conjunto (automáticamente elimina duplicados)

    return jsonify(
        sorted(list(servicios_unicos)))  # Convierte a lista ordenada y retorna en JSON - sin sorted() no habría orden


@app.route(
    '/api/ubicaciones_unicas')  # Endpoint para obtener lista única de ubicaciones - sin esto no hay opciones geográficas
def obtener_ubicaciones_unicas():
    """Obtiene la lista de todas las ubicaciones únicas disponibles en el sistema"""
    todos_proveedores = arbol_servicios.obtener_todos_ordenados()  # Obtiene todos los proveedores
    ubicaciones_unicas = set()  # Conjunto para eliminar duplicados automáticamente

    # Extraer ubicaciones únicas
    for proveedor in todos_proveedores:  # Itera sobre cada proveedor
        ubicaciones_unicas.add(proveedor['ubicacion'])  # Agrega al conjunto

    return jsonify(sorted(list(ubicaciones_unicas)))  # Lista ordenada en formato JSON


# Punto de entrada principal de la aplicación
if __name__ == '__main__':  # Solo ejecuta si el archivo se ejecuta directamente (no si se importa) - sin esto se ejecutaría al importar
    app.run(debug=True,
            port=5000)  # Inicia el servidor Flask en modo debug en puerto 5000 - CRÍTICO: sin esto no hay servidor web