class Proveedor:
    """
    Clase que representa un proveedor de servicios en el sistema.
    Encapsula toda la información relevante de un proveedor y proporciona
    métodos para convertir entre diferentes representaciones de datos.
    """

    def __init__(self, id_proveedor, nombre, servicio, calificacion, ubicacion):
        """
        Inicializa una nueva instancia de Proveedor con todos los datos requeridos
        Args:
            id_proveedor (int): Identificador único del proveedor - CRÍTICO: clave primaria
            nombre (str): Nombre del proveedor o empresa
            servicio (str): Tipo de servicio que ofrece
            calificacion (float): Calificación del proveedor (1-5)
            ubicacion (str): Ubicación geográfica del proveedor
        """
        self.id = id_proveedor  # Almacena ID único - CRÍTICO: sin esto no hay identificación, se perdería la clave de búsqueda
        self.nombre = nombre  # Almacena nombre - sin esto no hay identificación humana legible
        self.servicio = servicio  # Almacena tipo de servicio - CRÍTICO: sin esto no hay categorización funcional
        self.calificacion = calificacion  # Almacena calificación - sin esto no hay métrica de calidad
        self.ubicacion = ubicacion  # Almacena ubicación - sin esto no hay información geográfica

    def to_dict(self):
        """
        Convierte el objeto Proveedor a un diccionario Python
        Esto facilita la serialización JSON y el manejo de datos en la API
        Returns:
            dict: Representación en diccionario del proveedor

        CRÍTICO: Sin este método no se pueden almacenar objetos en el árbol B
        ni enviar respuestas JSON al frontend. Es fundamental para la interoperabilidad.
        """
        return {
            'id': self.id,  # Clave primaria - sin esto no hay identificación en JSON
            'nombre': self.nombre,  # Nombre legible - sin esto no hay display name
            'servicio': self.servicio,  # Categoría de servicio - sin esto no hay filtrado por tipo
            'calificacion': self.calificacion,  # Métrica de calidad - sin esto no hay ordenamiento por calidad
            'ubicacion': self.ubicacion  # Información geográfica - sin esto no hay filtrado geográfico
        }

    @staticmethod
    def from_dict(datos):
        """
        Método estático que crea una instancia de Proveedor desde un diccionario
        Útil para deserializar datos JSON o de base de datos
        Args:
            datos (dict): Diccionario con los datos del proveedor
        Returns:
            Proveedor: Nueva instancia de la clase Proveedor

        Sin este método no se pueden reconstruir objetos Proveedor desde datos JSON,
        lo que limitaría la flexibilidad del sistema para trabajar con diferentes fuentes de datos.
        """
        return Proveedor(
            datos['id'],  # Extrae ID del diccionario - CRÍTICO: sin esto no hay clave primaria
            datos['nombre'],  # Extrae nombre - sin esto objeto sin identidad
            datos['servicio'],  # Extrae servicio - sin esto no hay categorización
            datos['calificacion'],  # Extrae calificación - sin esto no hay métrica de calidad
            datos['ubicacion']  # Extrae ubicación - sin esto no hay información geográfica
        )

    def __str__(self):
        """
        Representación en cadena legible para humanos del proveedor
        Se usa cuando se imprime el objeto o se convierte a string
        Returns:
            str: Representación formateada del proveedor

        Sin este método, imprimir un objeto Proveedor mostraría solo la referencia
        de memoria, haciendo difícil el debugging y la visualización de datos.
        """
        return f"ID: {self.id}, Nombre: {self.nombre}, Servicio: {self.servicio}, Calificación: {self.calificacion}, Ubicación: {self.ubicacion}"
        # Formato legible con todos los campos - sin esto no hay representación humana comprensible

    def __repr__(self):
        """
        Representación oficial del objeto para debugging
        Debe ser una expresión que pueda recrear el objeto idealmente
        Returns:
            str: Representación técnica del objeto

        Sin este método, la representación en debugging sería menos clara.
        Al delegarlo a __str__, mantiene consistencia en la representación.
        """
        return self.__str__()  # Delega a __str__ para mantener consistencia - sin esto representaciones diferentes en contextos distintos