import csv
import heapq
from Estaciones import Estacion

class GrafoMetro:
    """Clase que representa el grafo del Metro Línea 3 de Guadalajara."""
    def __init__(self, archivo_csv=None):
        """Args:
        archivo_csv (str): Ruta al archivo CSV con los datos de las estaciones."""
        self.estaciones = {}
        if archivo_csv:
            self._cargar_datos_csv(archivo_csv)
            self._inicializar_conexiones()


    """Carga los datos de las estaciones desde un archivo CSV."""
    def _cargar_datos_csv(self, archivo_csv):
        with open(archivo_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            """Leer el archivo CSV y crear las estaciones."""
            for row in reader:
                nombre = row['Estación']
                flujo_min = int(row['Flujo Min (pasajeros/hora)'])
                flujo_max = int(row['Flujo Max (pasajeros/hora)'])
                es_transbordo = nombre in ["Plaza Patria", "Guadalajara Centro"]
                self.estaciones[nombre] = Estacion(
                    nombre=nombre,
                    ubicacion="",
                    flujo_promedio=(flujo_min + flujo_max) // 2,
                    es_transbordo=es_transbordo
                )

    """Grafo del Metro Línea 3 de Guadalajara."""
    def _inicializar_conexiones(self):
        conexiones = [
            ("Arcos de Zapopan", "Periférico Belenes", 3),
            ("Periférico Belenes", "Plaza Patria", 3),
            ("Plaza Patria", "Circunvalación", 4),
            ("Circunvalación", "Ávila Camacho", 2),
            ("Ávila Camacho", "La Normal", 3),
            ("La Normal", "Santuario", 2),
            ("Santuario", "Guadalajara Centro", 3),
            ("Guadalajara Centro", "Independencia", 2),
            ("Independencia", "Plaza de la Bandera", 3),
            ("Plaza de la Bandera", "CUCEI", 2),
            ("CUCEI", "Revolución", 3),
            ("Revolución", "Río Nilo", 2),
            ("Río Nilo", "Tlaquepaque Centro", 3),
            ("Tlaquepaque Centro", "Lázaro Cárdenas", 2),
            ("Lázaro Cárdenas", "Central de Autobuses", 3)
        ]
        for origen, destino, tiempo in conexiones:
            self.agregar_conexion(origen, destino, tiempo)

    def obtener_vecinos(self, estacion):
        """Obtiene las estaciones conectadas a una estación dada."""
        est = self.estaciones.get(estacion)
        if est:
            return list(est.conexiones.keys())
        return []


    def agregar_conexion(self, estacion1: str, estacion2: str, tiempo: int):
        """Agrega una conexión entre dos estaciones con un tiempo de viaje."""
        if estacion1 in self.estaciones and estacion2 in self.estaciones:
            self.estaciones[estacion1].agregar_conexion(estacion2, tiempo)
            self.estaciones[estacion2].agregar_conexion(estacion1, tiempo)

    def obtener_estacion(self, nombre: str) -> Estacion:
        return self.estaciones.get(nombre)

    def obtener_todas_estaciones(self) -> list:
        return list(self.estaciones.values())

    def encontrar_camino_mas_corto(self, inicio: str, fin: str):
        """Algoritmo de Dijkstra para encontrar el camino más corto basado en tiempos.
        Returns:
             tuple: (camino, tiempo_total):"""
        distancias = {est: float('inf') for est in self.estaciones}
        distancias[inicio] = 0
        prev = {est: None for est in self.estaciones}
        heap = [(0, inicio)]

        while heap:
            distancia_actual, actual = heapq.heappop(heap)

            if actual == fin:
                break

            if distancia_actual > distancias[actual]:
                continue

            conexiones = self.estaciones[actual].conexiones  # dict {vecino: tiempo}
            for vecino, tiempo in conexiones.items():
                nueva_dist = distancia_actual + tiempo
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    prev[vecino] = actual
                    heapq.heappush(heap, (nueva_dist, vecino))

        # Reconstruir camino
        camino = []
        actual = fin
        while actual:
            camino.append(actual)
            actual = prev[actual]
        camino.reverse()

        if distancias[fin] == float('inf'):
            return [], float('inf')  # No hay camino

        return camino, distancias[fin]


    def __str__(self):
        return f"Grafo del Metro Línea 3 | Estaciones: {len(self.estaciones)}"
