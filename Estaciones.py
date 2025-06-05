class Estacion:
    """Clase que representa una estación de tren."""
    def __init__(self, nombre: str, ubicacion: str, flujo_promedio: int, es_transbordo: bool = False, es_express: bool = False):
        """Args:
        nombre (str): Nombre de la estación.
        ubicacion (str): Ubicación de la estación (puede ser una coordenada o descripción).
        flujo_promedio (int): Flujo promedio de pasajeros por hora.
        es_transbordo (bool): Indica si la estación es un punto de transbordo.
        es_express (bool): Indica si la estación es de tipo express.
        """
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.flujo_promedio = flujo_promedio
        self.es_transbordo = es_transbordo
        self.es_express = es_express
        self.trenes_actuales = []
        self.conexiones = {}

    def agregar_conexion(self, estacion_vecina: str, tiempo: int):
        self.conexiones[estacion_vecina] = tiempo
        """Agrega una conexión a otra estación"""

    def recibir_tren(self, tren):
        self.trenes_actuales.append(tren)
        tren.estacion_actual = self.nombre
        """Recibe un tren en la estación y actualiza su estado."""

    def despachar_tren(self, tren):
        if tren in self.trenes_actuales:
            self.trenes_actuales.remove(tren)
            return True
        return False
    """Despacha un tren de la estación, removiéndolo de la lista de trenes actuales."""

    def actualizar_flujo(self, cambio: int):
        self.flujo_promedio = max(0, self.flujo_promedio + cambio)
    """Actualiza el flujo promedio de pasajeros en la estación."""

    def __str__(self):
        return f"{self.nombre} ({'Express' if self.es_express else 'Regular'})"