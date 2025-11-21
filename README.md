# GrafosFyJD

# No Waze

## Descripción del Proyecto

No Waze es una aplicación web de navegación que permite calcular rutas óptimas dentro de la ciudad de Guatemala utilizando grafos y el algoritmo de Dijkstra. El objetivo principal es encontrar la ruta más rápida bajo diferentes escenarios:

1. **Ruta directa:** Ir de un punto A a un punto B.
2. **Ruta pasando por un punto intermedio:** Ir de A a B pasando por un nodo C.
3. **Ruta evitando un nodo específico:** Ir de A a B sin pasar por C.
4. **Ruta considerando tráfico:** Simulación de tráfico con multiplicadores en el peso de las aristas.

El proyecto fue desarrollado como un ejercicio académico en la universidad para aplicar estructuras de datos avanzadas, algoritmos de grafos y visualización interactiva de mapas.

---

## Tecnologías y Librerías Utilizadas

* **Python**

  * `networkx`: Para la representación del grafo y la implementación del algoritmo de Dijkstra.
  * `osmnx`: Para generar el grafo base a partir de datos de OpenStreetMap.
  * `pandas`: Para leer y exportar información de nodos y aristas en formato CSV.
  * `shapely`: Para definir áreas geográficas mediante polígonos.
* **Frontend**

  * `Leaflet`: Librería para la visualización interactiva de mapas.
  * HTML, CSS, JavaScript: Interfaz de usuario, manejo de eventos y renderizado de rutas y POIs.
  * FontAwesome: Iconografía para la interfaz.

---

## Estructura del Proyecto

* `index.html`: Interfaz principal del proyecto con la barra lateral, formulario de cálculo de rutas y mapa interactivo.
* `css/styles.css`: Estilos visuales de la aplicación.
* `js/api.js`, `js/map.js`, `js/main.js`: Scripts de interacción con el mapa, POIs y rutas.
* `algorithm.py`: Implementación de las funciones de Dijkstra y los distintos escenarios de rutas.
* `graph_manager.py`: Gestión del grafo, carga de nodos y aristas desde OpenStreetMap y CSV personalizados.
* `config.py`: Configuración de archivos CSV, área geográfica y tipo de red.
* `nodos_personalizados.csv` y `aristas_personalizadas.csv`: Archivos con nombres personalizados y puntos de interés (POIs) agregados manualmente.

---

## Funcionamiento del Proyecto

### 1. Generación del Grafo

El grafo se genera a partir de un área geográfica definida mediante coordenadas (polígono). Se utiliza `osmnx` para construir los nodos (intersecciones) y aristas (calles) de la ciudad.

El archivo `graph_manager.py` contiene métodos para:

* Cargar el grafo base.
* Exportar nodos y aristas a CSV.
* Cargar nombres personalizados y POIs desde CSV.
* Obtener nodos cercanos a coordenadas específicas.
* Obtener información detallada de nodos y aristas.

### 2. Personalización de Nodos y Aristas

* **POIs:** Se agregan manualmente en `nodos_personalizados.csv` con su nombre y coordenadas.
* **Aristas personalizadas:** Se pueden modificar los pesos de las aristas o agregar nuevas conexiones en `aristas_personalizadas.csv`.

### 3. Cálculo de Rutas

El archivo `algorithm.py` define la clase `Algorithms` que implementa funciones de Dijkstra para cuatro escenarios:

#### a) Ruta simple

```python
ruta_simple(origen, destino)
```

Calcula la ruta más corta entre dos nodos usando el peso de las aristas.

#### b) Ruta con parada

```python
ruta_con_parada(origen, parada, destino)
```

Calcula la ruta pasando por un nodo intermedio. Combina la ruta de origen a parada y de parada a destino.

#### c) Ruta evitando un nodo

```python
ruta_con_obstaculo(origen, destino, obstaculo)
```

Evita un nodo específico eliminado temporalmente del grafo para calcular la ruta alternativa más corta.

#### d) Ruta considerando tráfico

```python
ruta_con_trafico(origen, destino, factor_calles=None, factor_extra=8.0)
```

Aplica un factor de tráfico a las aristas. Se puede definir un diccionario `factor_calles` para calles específicas, o aplicar un factor global a todas las aristas.

---

## Interfaz de Usuario

La aplicación web permite:

* Seleccionar **origen** y **destino** de la ruta.
* Seleccionar un **punto intermedio** si se desea.
* Elegir el **tipo de ruta**: directa, pasando por un punto, evitando un nodo.
* Calcular y mostrar la ruta en el mapa usando `Leaflet`.
* Visualizar POIs en el mapa y la lista de nodos de interés.
* Controlar visualización del mapa, calles y rutas mediante botones de la interfaz.

---

## Cómo Ejecutar el Proyecto

1. **Instalar dependencias de Python**

```bash
pip install networkx osmnx pandas shapely
```

2. **Cargar el grafo y generar CSV**

```python
from graph_manager import GraphManager

gm = GraphManager()
gm.cargar_grafo()
gm.exportar_nodos_csv()
gm.exportar_aristas_csv()
```

3. **Agregar POIs y nombres personalizados**

* Editar `nodos_personalizados.csv` y `aristas_personalizadas.csv`.
* Guardar los archivos en la ruta correspondiente.

4. **Ejecutar la aplicación web**

* Abrir `index.html` en un navegador.
* Interactuar con el mapa y calcular rutas según los escenarios.

---

## Consideraciones y Limitaciones

* El algoritmo de Dijkstra calcula rutas óptimas considerando el peso de las aristas; los factores de tráfico son simulados.
* Los POIs y nombres personalizados deben agregarse manualmente en los CSV para reflejar puntos reales de interés.
* El proyecto está diseñado para un área específica de Guatemala City; su escalabilidad a otras ciudades requiere ajustar el polígono en `config.py`.

---

## Conclusión

No Waze combina grafos, algoritmos de rutas y visualización en mapas interactivos para ofrecer una experiencia de navegación académica. Permite entender cómo funcionan los algoritmos de grafos en un contexto real y cómo interactúan con datos geográficos y de tráfico.
