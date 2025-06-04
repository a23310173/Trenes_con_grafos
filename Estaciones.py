class Estacion:
    def __init__(self, nombre: str, ubicacion: str, flujo_promedio: int, es_transbordo: bool = False, es_express: bool = False):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.flujo_promedio = flujo_promedio
        self.es_transbordo = es_transbordo
        self.es_express = es_express
        self.trenes_actuales = []
        self.conexiones = {}

    def agregar_conexion(self, estacion_vecina: str, tiempo: int):
        self.conexiones[estacion_vecina] = tiempo

    def recibir_tren(self, tren):
        self.trenes_actuales.append(tren)
        tren.estacion_actual = self.nombre

    def despachar_tren(self, tren):
        if tren in self.trenes_actuales:
            self.trenes_actuales.remove(tren)
            return True
        return False

    def actualizar_flujo(self, cambio: int):
        self.flujo_promedio = max(0, self.flujo_promedio + cambio)

    def __str__(self):
        return f"{self.nombre} ({'Express' if self.es_express else 'Regular'})"