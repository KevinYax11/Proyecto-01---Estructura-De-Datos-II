class Proveedor:
    def __init__(self, id_proveedor, nombre, servicio, calificacion):
        self.id = id_proveedor
        self.nombre = nombre
        self.servicio = servicio
        self.calificacion = calificacion

    def to_dict(self):
        """Convierte el proveedor a diccionario para facilitar el manejo"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'servicio': self.servicio,
            'calificacion': self.calificacion
        }

    @staticmethod
    def from_dict(datos):
        """Crea un proveedor desde un diccionario"""
        return Proveedor(
            datos['id'],
            datos['nombre'],
            datos['servicio'],
            datos['calificacion']
        )

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Servicio: {self.servicio}, Calificación: {self.calificacion}"

    def __repr__(self):
        return self.__str__()