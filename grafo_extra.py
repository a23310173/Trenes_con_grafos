from grafo import GrafoMetro

class GrafoMetroExpress(GrafoMetro):
    """Clase que representa un grafo del Metro con estaciones express."""
    def __init__(self, grafo_original: GrafoMetro, estaciones_express: list, inicio: str, fin: str):
        """Args:
        grafo_original (GrafoMetro): Grafo original del Metro.
        estaciones_express (list): Lista de nombres de estaciones express.
        inicio (str): Nombre de la estación de inicio.
        fin (str): Nombre de la estación de fin."""

        super().__init__(archivo_csv=None)  # grafo vacío
        nodos_a_incluir = set(estaciones_express)
        nodos_a_incluir.add(inicio)
        nodos_a_incluir.add(fin)

        # Agregar estaciones copiando desde el grafo original
        for nombre in nodos_a_incluir:
            estacion = grafo_original.obtener_estacion(nombre)
            if estacion:
                self.estaciones[nombre] = estacion
            else:
                print(f"Advertencia: estación {nombre} no existe en grafo original")

        # Agregar conexiones solo entre nodos incluidos
        for nombre in nodos_a_incluir:
            est = self.obtener_estacion(nombre)
            if est:
                conexiones = grafo_original.obtener_estacion(nombre).conexiones
                for vecino, tiempo in conexiones.items():
                    if vecino in nodos_a_incluir:
                        self.agregar_conexion(nombre, vecino, tiempo)

    def obtener_vecinos(self, estacion):
        est = self.estaciones.get(estacion)
        if est:
            return list(est.conexiones.keys())
        return []

"""# Algoritmo de Dijkstra para encontrar el camino más corto en un grafo"""
def dijkstra(grafo, inicio, fin):
    import heapq

    cola = []
    heapq.heappush(cola, (0, inicio))
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    predecesores = {}

    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == fin:
            break

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual].items():
            nuevo_costo = costo_actual + peso
            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola, (nuevo_costo, vecino))

    # Reconstruir camino
    camino = []
    actual = fin
    while actual != inicio:
        camino.append(actual)
        actual = predecesores.get(actual)
        if actual is None:
            return [], float('inf')  # No hay camino
    camino.append(inicio)
    camino.reverse()

    return camino, distancias[fin]
