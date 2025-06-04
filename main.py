from grafo import GrafoMetro
from grafo_extra import GrafoMetroExpress
from Trenes import Tren, TrenExpress
import random
import csv
import matplotlib.pyplot as plt



class SimuladorMetro:
    def __init__(self):
        self.grafo_normal = GrafoMetro('flujo_estaciones_linea3.csv')
        estaciones_express = ["Plaza Patria", "Guadalajara Centro"]  # Cambia por las que tengas realmente
        inicio = "Arcos de Zapopan"
        fin = "Central de Autobuses"
        self.grafo_express = GrafoMetroExpress(self.grafo_normal, estaciones_express, inicio, fin)

        self.trenes = self._inicializar_trenes()
        self.flujos_csv = self._cargar_flujos_csv()
        self.historial_movimiento = {}  # {estacion: {'horas': [], 'suben': [], 'bajan': []}}

    def _inicializar_trenes(self, total=15, express=3):
        inicio = self.grafo_normal.estaciones["Arcos de Zapopan"]
        trenes = [Tren(i) for i in range(1, total - express + 1)]
        trenes_express = [TrenExpress(i) for i in range(total - express + 1, total + 1)]
        for tren in trenes + trenes_express:
            tren.estacion_actual = inicio
            inicio.trenes_actuales.append(tren)
        return trenes + trenes_express

    def _cargar_flujos_csv(self, archivo='flujo_estaciones_linea3.csv'):
        with open(archivo, mode='r', encoding='utf-8') as file:
            return {row['Estación']: {
                'min': int(row['Flujo Min (pasajeros/hora)']),
                'max': int(row['Flujo Max (pasajeros/hora)'])
            } for row in csv.DictReader(file)}

    def simular(self, dias=6, usar_express=False):
        for dia in range(1, dias + 1):
            print(f"\n=== Día {dia} {'(con Express)' if usar_express else ''} ===")
            self._simular_dia(usar_express)

    def _simular_dia(self, usar_express):
        grafo = self.grafo_express if usar_express else self.grafo_normal
        for hora in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0]:
            self._actualizar_flujos(grafo)
            self._mover_trenes()
            self._mostrar_estado(grafo, hora)

    def _actualizar_flujos(self, grafo):
        for nombre, estacion in grafo.estaciones.items():
            if nombre in self.flujos_csv:
                rango = self.flujos_csv[nombre]
                estacion.actualizar_flujo(random.randint(rango['min'], rango['max']))

    def _mover_trenes(self):
        for tren in self.trenes:
            if tren.en_mantenimiento:
                continue

            # Selecciona el grafo según el tipo de tren
            if isinstance(tren, TrenExpress):
                grafo = self.grafo_express
            else:
                grafo = self.grafo_normal

            estacion_actual = tren.estacion_actual
            vecinos = grafo.obtener_vecinos(estacion_actual.nombre)  # vecinos es lista de nombres

            if vecinos:
                if isinstance(tren, TrenExpress):
                    vecinos_validos = [
                        v for v in vecinos if
                        v.startswith("Express") or v in ["Plaza Patria", "Guadalajara Centro",
                                                         "Independencia", "Central de Autobuses"]
                    ]
                    if not vecinos_validos:
                        print(
                            f"Tren express {tren.id} no tiene vecinos válidos desde {estacion_actual.nombre}, no se mueve.")
                        continue
                    estacion_destino_nombre = random.choice(vecinos_validos)
                else:
                    estacion_destino_nombre = random.choice(vecinos)

                estacion_destino = grafo.estaciones.get(estacion_destino_nombre)
                if estacion_destino is None:
                    print(
                        f"Estación destino '{estacion_destino_nombre}' no encontrada en el grafo, salto movimiento del tren {tren.id}.")
                    continue

                resultado = tren.mover(estacion_destino)
                print(resultado)

    def _mostrar_estado(self, grafo, hora):
        hora_str = f"{int(hora)}:{'00' if hora % 1 == 0 else '30'}"
        print(f"\n[hora = {hora_str}]")
        for nombre, estacion in grafo.estaciones.items():
            if nombre in self.flujos_csv or 'Express' in nombre:
                print(f"{nombre}: {estacion.flujo_promedio} pax | {len(estacion.trenes_actuales)} trenes")

        for estacion in grafo.estaciones.values():
            if hasattr(estacion, 'registro_movimiento'):
                estacion.registro_movimiento.clear()

    def simular_visualmente(self, dias=1, usar_express=False):
        grafo = self.grafo_express if usar_express else self.grafo_normal
        estaciones = list(grafo.estaciones.keys())

        # Posiciones en eje x para cada estación (simplificado)
        posiciones = {nombre: i for i, nombre in enumerate(estaciones)}

        for dia in range(1, dias + 1):
            print(f"\n=== Día {dia} {'(con Express)' if usar_express else ''} ===")
            for hora in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0]:
                self._actualizar_flujos(grafo)
                self._mover_trenes()
                self._mostrar_estado(grafo, hora)

                # Visualización
                plt.clf()
                x_vals = []
                y_vals = []
                colores = []
                labels = []

                for nombre, estacion in grafo.estaciones.items():
                    x = posiciones[nombre]
                    x_vals.append(x)
                    y_vals.append(0)
                    flujo = estacion.flujo_promedio or 0
                    colores.append(flujo)
                    labels.append(f"{nombre}\n{flujo} pax\n{len(estacion.trenes_actuales)} trenes")

                # Dibujar estaciones
                sc = plt.scatter(x_vals, y_vals, c=colores, cmap='coolwarm', s=200)
                for i, label in enumerate(labels):
                    plt.text(x_vals[i], y_vals[i] + 0.1, label, ha='center', fontsize=8)

                plt.colorbar(sc, label='Flujo de pasajeros')
                plt.title(f'Simulación Visual - Día {dia} Hora {int(hora)}:{int((hora % 1) * 60):02}')
                plt.xticks([])
                plt.yticks([])
                plt.pause(0.8)

                suben = sum([mov['suben'] for mov in getattr(estacion, 'registro_movimiento', [])])
                bajan = sum([mov['bajan'] for mov in getattr(estacion, 'registro_movimiento', [])])

                label = (f"{nombre}\n"
                         f"{flujo} pax\n"
                         f"{len(estacion.trenes_actuales)} trenes\n"
                         f"⬆ {suben} ⬇ {bajan}")
                labels.append(label)

        plt.show()



if __name__ == "__main__":
    simulador = SimuladorMetro()
    print("=== SIMULACIÓN NORMAL ===")
    simulador.simular(usar_express=False)

    print("\n=== SIMULACIÓN CON RUTAS EXPRESS ===")
    simulador.simular(usar_express=True)

    print("=== SIMULACIÓN VISUAL ===")
    simulador.simular_visualmente(usar_express=False)

    print("\n=== SIMULACIÓN VISUAL CON RUTAS EXPRESS ===")
    simulador.simular_visualmente(usar_express=True)
