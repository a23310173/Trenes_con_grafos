#simulador de metro Linea 3 Guadalajara

Este proyecto plantea una solución basada en simulación algorítmica para evaluar el impacto de implementar rutas express en el sistema de metro de Guadalajara (Línea 3). 
El modelo propuesto analiza cómo la incorporación de trenes directos a estaciones estratégicas durante horas pico puede mejorar la fluidez del servicio y reducir tiempos de traslado.
los datos se recopilaron desde el sitio oficial de SITEUR 

Los datos utilizados en esta simulación fueron recopilados del sitio oficial de SITEUR, organismo encargado del sistema de transporte eléctrico urbano de Guadalajara.
---

##Justificacion

Este proyecto surge como búsqueda a la respuesta de este problema cotidiano el que afecta a la población en general de los municipios declarados anteriormente, 
ya que al ser uno de los principales medios de transporte de la zona metropolitana de Guadalajara, la saturación de la línea 3 en horas pico representa una perdida de tiempo significativa para los usuarios, 
además generando condiciones incomodas e ineficientes en el sistema de transporte.

---

##Tecnologias utilizadas

Lenguaje:	Python 3.8+
Algoritmos:	Dijkstra (rutas óptimas), Grafos (NetworkX opcional)
Visualización:	Matplotlib, Seaborn
Datos:	CSV (originados de SITEUR)
Estructuras:	Grafos, Diccionarios, Heaps

---

##Estructura del proyecto

src/
├── core/
│   ├── estaciones.py       # Clase Estación (nodos del grafo)
│   ├── grafo.py            # GrafoMetro + Dijkstra
│   └── trenes.py           # Trenes normales/express
├── data/                   # Datos de SITEUR
│   └── flujo_estaciones_linea3.csv
└── simulacion.py           # Lógica principal

---

##Instalacion

1. Clonar repositorio:
   ```bash
   git clone https://github.com/tu-usuario/simulador-metro.git
   cd simulador-metro
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

---

##Uso

-simulacion basica de consola:

from src.main import SimuladorMetro

simulador = SimuladorMetro()
simulador.simular(dias=3)  # Modo normal
simulador.simular(dias=3, usar_express=True)  # Con trenes express

-visualizacion grafica:

simulador.simular_visualmente(dias=2)  # Muestra animación interactiva
simulador.graficar_movimiento()       # Genera gráficos comparativos

-parametros configurablea:

ARCHIVO                    	|       VARIABLES CLAVE        	 |       DESCRIPCION
flujo_estaciones_linea3.csv |	Flujo Min/Max (pasajeros/hora) |	Ajusta capacidad de estaciones
Trenes.py	capacidad         | velocidad_maxima               |  Características de trenes
main.py	dias                | usar_express	Duración         |  tipo de simulación

---

##Metricas de rendimiento y caracteristicas implementadas

-El sistema genera automáticamente:

1. Gráficos de flujo por estación
2. Comparativa Express vs Normal

   # En main.py:
self.historial_normal  # Almacena datos modo regular
self.historial_express # Datos modo express

3. Eficiencia por hora (pasajeros transportados/trenes activos)

---

##Posibles mejoras futuras

-mejoras en simulacion

1. Datos en tiempo real
2. eventos aleatorios

-Implementacion de algoritmos avanzados

1.A* puede ser una opcion viable al ser mas eficiente que DIJKSTRA en grafios mas complejos

---

##Autores

-Ivan Alejandro Lujan Amezcua
-Santiago Ramirez Orozco
-Luis Uriel Arriaga Castañeda

##Profesora 

-Ximena Aquino Perez
