import random

class Tren:
    """Clase base para representar un tren del sistema de transporte."""
    def __init__(self, id_tren: int, estacion_actual=None, en_mantenimiento: bool = False):

        """Args:
        id_tren (int): Identificador único del tren.
        estacion_actual (Estacion): Estación donde se encuentra el tren.
        en_mantenimiento (bool): Indica si el tren está en mantenimiento.
        """
        self.id = id_tren
        self.modelo = "Hitachi NS-74"
        self.capacidad = 230
        self.velocidad_maxima = 80  # km/h
        self.estacion_actual = estacion_actual  # ahora será objeto Estacion o None
        self.en_mantenimiento = en_mantenimiento
        self.pasajeros_actuales = 0
        self.tiempo_entre_estaciones = 4  # mins

    def mover(self, estacion_destino, hora_actual=None, historial=None):
        if self.en_mantenimiento:
            """Intenta mover el tren a una nueva estación gestionando los pasajeros."""
            return f"Tren {self.id} no puede moverse (en mantenimiento)"

        # Bajada de pasajeros (entre 10% y 30% de los pasajeros actuales)
        if self.pasajeros_actuales > 0:
            bajan = random.randint(int(0.1 * self.pasajeros_actuales), int(0.5 * self.pasajeros_actuales))
        else:
            bajan = 0
        self.descargar_pasajeros(bajan)

        # Subida de pasajeros (hasta capacidad y flujo disponible en la estación)
        espacio_disponible = self.capacidad - self.pasajeros_actuales
        posibles_subir = min(espacio_disponible, estacion_destino.flujo_promedio)
        self.cargar_pasajeros(posibles_subir)

        # Reducir el flujo de la estación destino por los que subieron
        estacion_destino.flujo_promedio = max(0, estacion_destino.flujo_promedio - posibles_subir)

        # Quitar tren de la estación actual
        if self.estacion_actual and self in self.estacion_actual.trenes_actuales:
            self.estacion_actual.trenes_actuales.remove(self)

        # Actualizar estación actual
        self.estacion_actual = estacion_destino

        # Agregar tren a la nueva estación
        self.estacion_actual.trenes_actuales.append(self)

        if hasattr(estacion_destino, 'registro_movimiento') is False:
            estacion_destino.registro_movimiento = []

        estacion_destino.registro_movimiento.append({
            'tren_id': self.id,
            'suben': posibles_subir,
            'bajan': bajan
        })

        if historial is not None and hora_actual is not None:
            """Registra el movimiento del tren en el historial."""
            nombre = estacion_destino.nombre
            if nombre not in historial:
                historial[nombre] = {'horas': [], 'suben': [], 'bajan': []}
            historial[nombre]['horas'].append(hora_actual)
            historial[nombre]['suben'].append(posibles_subir)
            historial[nombre]['bajan'].append(bajan)

        return (f"Tren {self.id} ha llegado a {estacion_destino.nombre} "
                f"(bajaron {bajan}, subieron {posibles_subir}, pasajeros actuales: {self.pasajeros_actuales})")

    def cargar_pasajeros(self, cantidad: int):
        """Carga pasajeros al tren si hay espacio disponible."""
        if self.pasajeros_actuales + cantidad <= self.capacidad:
            self.pasajeros_actuales += cantidad
            return True
        return False

    def descargar_pasajeros(self, cantidad: int):
        """Descarga pasajeros del tren si hay suficientes a bordo."""
        if self.pasajeros_actuales >= cantidad:
            self.pasajeros_actuales -= cantidad
            return True
        return False

class TrenExpress(Tren):
    """Clase que representa un tren express del sistema de transporte."""
    def __init__(self, id_tren: int):
        """Args:
        id_tren (int): Identificador único del tren express.
        """
        super().__init__(id_tren)
        self.modelo = "Hitachi NS-74 Express"
        self.capacidad = 300
        self.velocidad_maxima = 100  # km/h
        self.tiempo_entre_estaciones = 3  # mins

    def mover(self, estacion_destino, hora_actual=None, historial=None):
        # Validación de estaciones permitidas para tren express
        estaciones_permitidas = ["Plaza Patria", "Guadalajara Centro", "Independencia", "Central de Autobuses"]
        if not estacion_destino.nombre.startswith("Express") and estacion_destino.nombre not in estaciones_permitidas:
            return f"Tren express {self.id} no puede ir a {estacion_destino.nombre}"

        # Bajada de pasajeros (10% a 30% de pasajeros actuales)
        if self.pasajeros_actuales > 0:
            bajan = random.randint(int(0.1 * self.pasajeros_actuales), int(0.3 * self.pasajeros_actuales))
        else:
            bajan = 0
        self.descargar_pasajeros(bajan)

        # Subida de pasajeros con capacidad y flujo
        espacio_disponible = self.capacidad - self.pasajeros_actuales
        posibles_subir = min(espacio_disponible, estacion_destino.flujo_promedio)
        self.cargar_pasajeros(posibles_subir)

        # Ajustar flujo en la estación destino
        estacion_destino.flujo_promedio = max(0, estacion_destino.flujo_promedio - posibles_subir)

        # Quitar tren de la estación actual
        if self.estacion_actual and self in self.estacion_actual.trenes_actuales:
            self.estacion_actual.trenes_actuales.remove(self)

        # Actualizar estación actual
        self.estacion_actual = estacion_destino

        # Agregar tren a la nueva estación
        self.estacion_actual.trenes_actuales.append(self)

        if hasattr(estacion_destino, 'registro_movimiento') is False:
            estacion_destino.registro_movimiento = []

        estacion_destino.registro_movimiento.append({
            'tren_id': self.id,
            'suben': posibles_subir,
            'bajan': bajan
        })

        if historial is not None and hora_actual is not None:
            """Registra el movimiento del tren express en el historial."""
            nombre = estacion_destino.nombre
            if nombre not in historial:
                historial[nombre] = {'horas': [], 'suben': [], 'bajan': []}
            historial[nombre]['horas'].append(hora_actual)
            historial[nombre]['suben'].append(posibles_subir)
            historial[nombre]['bajan'].append(bajan)

        return (f"Tren express {self.id} ha llegado a {estacion_destino.nombre} "
                f"(bajaron {bajan}, subieron {posibles_subir}, pasajeros actuales: {self.pasajeros_actuales})")