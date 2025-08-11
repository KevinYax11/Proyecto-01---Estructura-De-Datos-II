class NodoB:
    """Nodo del árbol B"""

    def __init__(self, es_hoja=True):
        self.claves = []
        self.hijos = []
        self.es_hoja = []


    def esta_lleno(self, orden):
        return len(self.claves) == orden - 1



class ArbolB:
    def __init__(self, orden: 3):
        if orden < 3:
            raise ValueError("El orden del árbol debe ser mínimo 3")

        self.orden = orden
        self.raiz = NodoB()
        self.total_proveedores = 0

    def insertar (self, proveedor):
        if self.raiz.esta_lleno(self.orden):
            nueva_raiz = NodoB(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self.raiz = nueva_raiz


    self._insertar_no_lleno(self.raiz, proveedor)
    self.total_proveedores +=1


    def _insertar_no_lleno(self, nodo, proveedor):
        i = len(nodo.clave) - 1

        if nodo.es_hoja:
            nodo.clave.append(None)
            while i >= 0 and proveedor.id < nodo.claves[i].id:
                nodo.claves[i+1] = nodo.claves[i]
                i -= 1
            nodo.claves[i+1] = proveedor

        else:
            while i > 0 and proveedor.id > nodo.claves[i].id:
                i -= 1
            i += 1

            if nodo.hijos[i].esta_lleno(self.orden):
                self._dividir_hijo(nodo,i)
                if proveedor.id > nodo.claves[i].id:
                    i +=1

            self._insertar_no_lleno(nodo, proveedor.hijos[i], proveedor)


    def _dividir_hijo(self, padre, indice):
        hijo_lleno = padre.hijos[indice]
        nuevo_hijo = NodoB(es_hoja=hijo_lleno.es_hoja)
        medio = self.orden //2

        nuevo_hijo.claves = hijo_lleno.claves [medio + 1:]
        hijo_lleno.claves = hijo_lleno.claves[:medio]

        if not hijo_lleno.es_hoja:
            nuevo_hijo.hijos = hijo_lleno.hijos[medio + 1]
            hijo_lleno.hijos = hijo_lleno.hijos[:medio + 1]

        padre.hijos.insert(indice + 1, nuevo_hijo)
        padre.claves.insert(indice, hijo_lleno.hijos[medio])


    def buscar_por_servicio(self, tipo_servicio):
        tipo_servicio = tipo_servicio.lower()
        resultados = []
        self.buscar_por_servicio_recursivo(self.raiz, tipo_servicio, resultados)
        return resultados

    def _buscar_por_servicios_recursivo(self,nodo, tipo_servicio, resultados):
        for proveedor in nodo.claves:
            if proveedor.servicio == tipo_servicio:
                resultados.append(proveedor)

            if not nodo.es_hoja:
                for hijo in nodo.hijos:
                    self._buscar_por_servicios_recursivo(hijo, tipo_servicio, resultados)


    def buscar_por_id(self, id_proveedor):
        return self._buscar_id_recursivo(self.raiz, id_proveedor)

    def _buscar_id_recursivo(self, nodo, id_proveedor):
        i = 0
        while i < len(nodo.claves) and id_proveedor > nodo.claves[i].id:
            i += 1

        if i < len(nodo.claves) and id_proveedor == nodo.claves[i].id:
            return nodo.claves[i]

        if nodo.es_hoja:
            return None

        return self._buscar_id_recursivo(nodo.hijos[i], id_proveedor)