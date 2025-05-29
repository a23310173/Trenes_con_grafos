#En este archivo implementaremos la clase de las estaciones y el grafo del metro
from Trenes import Tren


class Estacion:
    def __init__(self, nombre: str, ubicacion: str, flujo_promedio: int, es_transbordo: bool = False):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.flujo_promedio = flujo_promedio # Pasajeros/hora
        self.es_transbordo = es_transbordo
        self.trenes_actuales = []
        self.conexiones = {}

    def agregar_conexion(self, estacion_vecina: str, tiempo: int):
        self.conexiones[estacion_vecina] = tiempo

    def recibir_tren(self, tren: Tren):
        self.trenes_actuales.append(tren)
        tren.estacion_actual = self.nombre

    def despachar_tren(self, tren: Tren):
        if tren in self.trenes_actuales:
            self.trenes_actuales.remove(tren)
            return f"Tren {tren.id} despachado de {self.nombre}"
        return "El tren no está en esta estación."

    def actualizar_flujo(self, pasajeros: int):
        self.flujo_promedio += pasajeros

    def __str__(self):
        return f"Estación {self.nombre} | Flujo: {self.flujo_promedio} pasajeros/hora | Trenes: {len(self.trenes_actuales)}"