#En este archivo implementaremos la clase de los trenes y la lista enlazada que los contendra
class Tren:
    def __init__(self, id_tren: int, estacion_actual: str = "Depósito", en_mantenimiento: bool = False):
        self.id = id_tren
        self.modelo = "Hitachi NS-74"
        self.capacidad = 230
        self.velocidad_maxima = 80  # km/h
        self.longitud = 60.0  # 3 vagones x 20m
        self.estacion_actual = estacion_actual
        self.en_mantenimiento = en_mantenimiento
        self.pasajeros_actuales = 0  # Inicialmente vacío
        self.tiempo_entre_estaciones = 4  # mins (promedio)

    def mover(self, estacion_destino: str):
        if not self.en_mantenimiento:
            self.estacion_actual = estacion_destino
            return f"Tren {self.id} ha llegado a {estacion_destino}"
        return f"Tren {self.id} no puede moverse (en mantenimiento)"

    def cargar_pasajeros(self, cantidad: int):
        if self.pasajeros_actuales + cantidad <= self.capacidad:
            self.pasajeros_actuales += cantidad
            return f"Pasajeros embarcados: {cantidad}"
        return "¡Capacidad excedida!"

    def descargar_pasajeros(self, cantidad: int):

        if self.pasajeros_actuales >= cantidad:
            self.pasajeros_actuales -= cantidad
            return f"Pasajeros desembarcados: {cantidad}"
        return "No hay suficientes pasajeros."