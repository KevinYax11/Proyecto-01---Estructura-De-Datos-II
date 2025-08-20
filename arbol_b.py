class NodoB:
    def __init__(self, es_hoja=False):
        self.claves = []  # Lista de claves (IDs de proveedores)
        self.datos = []  # Lista de datos asociados a las claves
        self.hijos = []  # Lista de hijos
        self.es_hoja = es_hoja

    def esta_lleno(self, grado):
        return len(self.claves) == 2 * grado - 1


class ArbolB:
    def __init__(self, grado=3):
        self.raiz = NodoB(es_hoja=True)
        self.grado = grado  # Grado mínimo del árbol B

    def insertar(self, clave, datos):
        """Inserta una nueva clave con sus datos en el árbol B"""
        if self.raiz.esta_lleno(self.grado):
            # Si la raíz está llena, crear nueva raíz
            nueva_raiz = NodoB()
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz

        self._insertar_no_lleno(self.raiz, clave, datos)

    def _insertar_no_lleno(self, nodo, clave, datos):
        """Inserta en un nodo que no está lleno"""
        i = len(nodo.claves) - 1

        if nodo.es_hoja:
            # Insertar en nodo hoja
            nodo.claves.append(None)
            nodo.datos.append(None)

            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                nodo.datos[i + 1] = nodo.datos[i]
                i -= 1

            nodo.claves[i + 1] = clave
            nodo.datos[i + 1] = datos
        else:
            # Encontrar el hijo donde insertar
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1

            if nodo.hijos[i].esta_lleno(self.grado):
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1

            self._insertar_no_lleno(nodo.hijos[i], clave, datos)

    def _dividir_hijo(self, nodo_padre, indice):
        """Divide un hijo lleno"""
        grado = self.grado
        nodo_lleno = nodo_padre.hijos[indice]
        nuevo_nodo = NodoB(es_hoja=nodo_lleno.es_hoja)

        # Mover la mitad de las claves al nuevo nodo
        nuevo_nodo.claves = nodo_lleno.claves[grado:]
        nuevo_nodo.datos = nodo_lleno.datos[grado:]
        nodo_lleno.claves = nodo_lleno.claves[:grado - 1]
        nodo_lleno.datos = nodo_lleno.datos[:grado - 1]

        # Si no es hoja, mover también los hijos
        if not nodo_lleno.es_hoja:
            nuevo_nodo.hijos = nodo_lleno.hijos[grado:]
            nodo_lleno.hijos = nodo_lleno.hijos[:grado]

        # Insertar la clave media en el padre
        clave_media = nodo_lleno.claves[grado - 1]
        datos_media = nodo_lleno.datos[grado - 1]

        nodo_padre.hijos.insert(indice + 1, nuevo_nodo)
        nodo_padre.claves.insert(indice, clave_media)
        nodo_padre.datos.insert(indice, datos_media)

    def buscar(self, clave):
        """Busca una clave específica en el árbol"""
        return self._buscar_en_nodo(self.raiz, clave)

    def _buscar_en_nodo(self, nodo, clave):
        """Busca en un nodo específico"""
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return nodo.datos[i]

        if nodo.es_hoja:
            return None

        return self._buscar_en_nodo(nodo.hijos[i], clave)

    def buscar_por_servicio(self, tipo_servicio):
        """Busca todos los proveedores de un tipo de servicio específico"""
        resultados = []
        self._buscar_servicio_en_nodo(self.raiz, tipo_servicio.lower(), resultados)
        return resultados

    def _buscar_servicio_en_nodo(self, nodo, tipo_servicio, resultados):
        """Busca por servicio en un nodo específico"""
        # Buscar en las claves del nodo actual
        for datos in nodo.datos:
            if datos['servicio'].lower() == tipo_servicio:
                resultados.append(datos)

        # Si no es hoja, buscar en todos los hijos
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self._buscar_servicio_en_nodo(hijo, tipo_servicio, resultados)

    def buscar_por_ubicacion(self, ubicacion):
        """Busca todos los proveedores de una ubicación específica"""
        resultados = []
        self._buscar_ubicacion_en_nodo(self.raiz, ubicacion.lower(), resultados)
        return resultados

    def _buscar_ubicacion_en_nodo(self, nodo, ubicacion, resultados):
        """Busca por ubicación en un nodo específico"""
        # Buscar en las claves del nodo actual
        for datos in nodo.datos:
            if datos['ubicacion'].lower() == ubicacion:
                resultados.append(datos)

        # Si no es hoja, buscar en todos los hijos
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self._buscar_ubicacion_en_nodo(hijo, ubicacion, resultados)

    def obtener_todos_ordenados(self, orden_por='nombre'):
        """Obtiene todos los proveedores ordenados"""
        todos = []
        self._recorrer_inorden(self.raiz, todos)

        if orden_por == 'nombre':
            return sorted(todos, key=lambda x: x['nombre'].lower())
        elif orden_por == 'calificacion':
            return sorted(todos, key=lambda x: x['calificacion'], reverse=True)
        elif orden_por == 'ubicacion':
            return sorted(todos, key=lambda x: x['ubicacion'].lower())
        else:
            return todos

    def _recorrer_inorden(self, nodo, resultado):
        """Recorre el árbol en orden"""
        if nodo.es_hoja:
            for datos in nodo.datos:
                resultado.append(datos)
        else:
            for i in range(len(nodo.claves)):
                self._recorrer_inorden(nodo.hijos[i], resultado)
                resultado.append(nodo.datos[i])
            self._recorrer_inorden(nodo.hijos[-1], resultado)

    def obtener_estadisticas(self):
        """Obtiene estadísticas del árbol"""
        total_nodos = self._contar_nodos(self.raiz)
        total_proveedores = len(self.obtener_todos_ordenados())
        altura = self._obtener_altura(self.raiz)

        return {
            'total_nodos': total_nodos,
            'total_proveedores': total_proveedores,
            'altura': altura,
            'grado': self.grado
        }

    def _contar_nodos(self, nodo):
        """Cuenta el total de nodos en el árbol"""
        if nodo.es_hoja:
            return 1

        total = 1
        for hijo in nodo.hijos:
            total += self._contar_nodos(hijo)
        return total

    def _obtener_altura(self, nodo):
        """Obtiene la altura del árbol"""
        if nodo.es_hoja:
            return 1

        if nodo.hijos:
            return 1 + self._obtener_altura(nodo.hijos[0])
        return 1