from grafo import GrafoMetro
from grafo_extra import GrafoMetroExpress
from Trenes import Tren, TrenExpress
import random
import csv
import matplotlib.pyplot as plt



class SimuladorMetro:
    """Clase que simula el funcionamiento del Metro Línea 3 de Guadalajara."""
    def __init__(self):
        self.grafo_normal = GrafoMetro('flujo_estaciones_linea3.csv')
        estaciones_express = ["Plaza Patria", "Guadalajara Centro"]
        inicio = "Arcos de Zapopan"
        fin = "Central de Autobuses"
        self.grafo_express = GrafoMetroExpress(self.grafo_normal, estaciones_express, inicio, fin)

        self.trenes = self._inicializar_trenes()
        self.flujos_csv = self._cargar_flujos_csv()

        self.historial_normal = {}
        self.historial_express = {}
        self.historial_movimiento = self.historial_normal

    def _inicializar_trenes(self, total=15, express=3):
        """Inicializa los trenes del sistema, tanto normales como express."""
        inicio = self.grafo_normal.estaciones["Arcos de Zapopan"]
        trenes = [Tren(i) for i in range(1, total - express + 1)]
        trenes_express = [TrenExpress(i) for i in range(total - express + 1, total + 1)]
        """Asignar la estación de inicio a todos los trenes y agregarlos a la lista de trenes actuales."""
        for tren in trenes + trenes_express:
            tren.estacion_actual = inicio
            inicio.trenes_actuales.append(tren)
        return trenes + trenes_express

    def _cargar_flujos_csv(self, archivo='flujo_estaciones_linea3.csv'):
        """Carga los flujos de pasajeros desde el archivo CSV."""
        with open(archivo, mode='r', encoding='utf-8') as file:
            return {row['Estación']: {
                'min': int(row['Flujo Min (pasajeros/hora)']),
                'max': int(row['Flujo Max (pasajeros/hora)'])
            } for row in csv.DictReader(file)}

    def simular(self, dias=6, usar_express=False):
        """Simula el funcionamiento del Metro durante un número de días."""
        self.historial_movimiento = self.historial_express if usar_express else self.historial_normal
        for dia in range(1, dias + 1):
            print(f"\n=== Día {dia} {'(con Express)' if usar_express else ''} ===")
            self._simular_dia(usar_express)

    def _simular_dia(self, usar_express):
        """Simula un día completo de operaciones del Metro."""
        grafo = self.grafo_express if usar_express else self.grafo_normal
        for hora in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0]:
            self._actualizar_flujos(grafo)
            self._mover_trenes(hora)
            self._mostrar_estado(grafo, hora)

    def _actualizar_flujos(self, grafo):
        """Actualiza el flujo de pasajeros en las estaciones."""
        for nombre, estacion in grafo.estaciones.items():
            if nombre in self.flujos_csv:
                rango = self.flujos_csv[nombre]
                estacion.actualizar_flujo(random.randint(rango['min'], rango['max']))

    def _mover_trenes(self, hora_actual):
        """Mueve los trenes a sus estaciones destino según el horario actual."""
        for tren in self.trenes:
            if tren.en_mantenimiento:
                continue

            grafo = self.grafo_express if isinstance(tren, TrenExpress) else self.grafo_normal
            estacion_actual = tren.estacion_actual
            vecinos = grafo.obtener_vecinos(estacion_actual.nombre)

            """Si la estación actual no tiene vecinos, no se puede mover el tren."""
            if vecinos:
                if isinstance(tren, TrenExpress):
                    vecinos_validos = [v for v in vecinos if
                                       v.startswith("Express") or v in ["Plaza Patria", "Guadalajara Centro",
                                                                        "Independencia", "Central de Autobuses"]]
                    if not vecinos_validos:

                        print(f"Tren express {tren.id} sin vecinos válidos desde {estacion_actual.nombre}")
                        continue
                    estacion_destino_nombre = random.choice(vecinos_validos)
                else:
                    estacion_destino_nombre = random.choice(vecinos)

                estacion_destino = grafo.estaciones.get(estacion_destino_nombre)
                if estacion_destino is None:
                    print(f"Estación destino '{estacion_destino_nombre}' no encontrada")
                    continue

                resultado = tren.mover(estacion_destino, hora_actual=hora_actual, historial=self.historial_movimiento)
                print(resultado)

    def _mostrar_estado(self, grafo, hora):
        """Muestra el estado actual de las estaciones y trenes."""
        hora_str = f"{int(hora)}:{'00' if hora % 1 == 0 else '30'}"
        print(f"\n[hora = {hora_str}]")
        for nombre, estacion in grafo.estaciones.items():
            if nombre in self.flujos_csv or 'Express' in nombre:
                print(f"{nombre}: {estacion.flujo_promedio} pasajeros | {len(estacion.trenes_actuales)} trenes")

        """Registro de movimiento de pasajeros en las estaciones."""
        for estacion in grafo.estaciones.values():
            if hasattr(estacion, 'registro_movimiento'):
                estacion.registro_movimiento.clear()

    def simular_visualmente(self, dias=1, usar_express=False):
        """Simula visualmente el funcionamiento del Metro durante un número de días."""
        self.historial_movimiento = self.historial_express if usar_express else self.historial_normal
        grafo = self.grafo_express if usar_express else self.grafo_normal
        estaciones = list(grafo.estaciones.keys())
        posiciones = {nombre: i for i, nombre in enumerate(estaciones)}

        for dia in range(1, dias + 1):
            """Simula un día completo de operaciones del Metro con visualización."""
            print(f"\n=== Día {dia} {'(con Express)' if usar_express else ''} ===")
            for hora in [6.5, 7.0, 7.5, 8.0, 8.5, 9.0]:
                self._actualizar_flujos(grafo)
                self._mover_trenes(hora)
                self._mostrar_estado(grafo, hora)

                plt.clf()
                x_vals, y_vals, colores, labels = [], [], [], []

                for nombre, estacion in grafo.estaciones.items():
                    """Si la estación no tiene flujo, no la mostramos."""
                    x = posiciones[nombre]
                    flujo = estacion.flujo_promedio or 0
                    suben = sum([mov['suben'] for mov in getattr(estacion, 'registro_movimiento', [])])
                    bajan = sum([mov['bajan'] for mov in getattr(estacion, 'registro_movimiento', [])])
                    label = (f"{nombre}\n"
                             f"{flujo} pasajeros\n"
                             f"{len(estacion.trenes_actuales)} trenes\n"
                             f"⬆ {suben} ⬇ {bajan}")
                    x_vals.append(x)
                    y_vals.append(0)
                    colores.append(flujo)
                    labels.append(label)

                """Visualización de las estaciones y sus flujos de pasajeros."""
                sc = plt.scatter(x_vals, y_vals, c=colores, cmap='coolwarm', s=200)
                for i, label in enumerate(labels):
                    plt.text(x_vals[i], y_vals[i] + 0.1, label, ha='center', fontsize=8)

                plt.colorbar(sc, label='Flujo de pasajeros')
                plt.title(f'Simulación Visual - Día {dia} Hora {int(hora)}:{int((hora % 1) * 60):02}')
                plt.xticks([])
                plt.yticks([])
                plt.pause(0.8)

        plt.show()

    def graficar_movimiento(self):
        """Genera gráficos comparativos del movimiento de pasajeros en las estaciones."""
        import matplotlib.pyplot as plt

        estaciones = sorted(set(self.historial_normal.keys()).union(self.historial_express.keys()))

        for estacion in estaciones:
            fig, ax = plt.subplots(figsize=(9, 4))

            if estacion in self.historial_normal:
                """Si la estación tiene datos en el historial normal, los graficamos."""
                datos = self.historial_normal[estacion]
                ax.plot(datos['horas'], datos['suben'], label='Normal - Suben ⬆', marker='o', linestyle='--', color='blue')
                ax.plot(datos['horas'], datos['bajan'], label='Normal - Bajan ⬇', marker='x', linestyle='--', color='skyblue')

            if estacion in self.historial_express:
                """Si la estación tiene datos en el historial express, los graficamos."""
                datos = self.historial_express[estacion]
                ax.plot(datos['horas'], datos['suben'], label='Express - Suben ⬆', marker='o', linestyle='-', color='red')
                ax.plot(datos['horas'], datos['bajan'], label='Express - Bajan ⬇', marker='x', linestyle='-', color='black')

            ax.set_title(f"Comparativa de Pasajeros en {estacion}")
            ax.set_xlabel("Hora")
            ax.set_ylabel("Cantidad de pasajeros")
            ax.legend()
            ax.grid(True)
            horas = sorted(set(
                self.historial_normal.get(estacion, {}).get('horas', []) +
                self.historial_express.get(estacion, {}).get('horas', [])
            ))
            ax.set_xticks(horas)
            ax.set_xticklabels([f"{h:.1f}" for h in horas], rotation=45)
            plt.tight_layout()
            plt.show()

"""Main para ejecutar la simulación del Metro"""
if __name__ == "__main__":
    simulador = SimuladorMetro()
    print("=== SIMULACIÓN NORMAL ===")
    simulador.simular(usar_express=False)

    print("\n=== SIMULACIÓN CON RUTAS EXPRESS ===")
    simulador.simular(usar_express=True)
    print("\n=== GRAFICANDO COMPARATIVAS DE MOVIMIENTO ===")
    simulador.graficar_movimiento()  # Compara ambos históricos
