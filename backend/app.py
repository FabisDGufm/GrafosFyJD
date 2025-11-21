from algorithms import Algorithms

algo = Algorithms()
print("Primeros 20 nodos del grafo:", list(algo.grafo.nodes())[:20])


# POIs fijos
POIS = [
    {"id": 14206194901, "nombre": "Parque 14"},
    {"id": 14206194902, "nombre": "Pollo Campero Las Americas"},
    {"id": 14206194903, "nombre": "Plaza Obelisco"},
    {"id": 14206194904, "nombre": "Plaza Espana"},
    {"id": 14206194905, "nombre": "CC Montufar"},
    {"id": 14206194906, "nombre": "McDonalds Blvd Liberacion"},
    {"id": 14206194907, "nombre": "Shell Aeropuerto"},
    {"id": 14206194908, "nombre": "Reloj de Flores"},
    {"id": 14206194909, "nombre": "Hospital Liberacion"},
    {"id": 14206194910, "nombre": "SIB Superintendencia de Bancos"},
]

def mostrar_menu():
    print("\n=== Waze Simplificado - Terminal ===")
    print("1. Ruta simple")
    print("2. Ruta con parada")
    print("3. Ruta con obstáculo")
    print("4. Ruta con tráfico")
    print("5. Salir")

def seleccionar_poi(prompt="Ingrese el ID del POI"):
    print("\nPOIs disponibles:")
    for poi in POIS:
        print(f"{poi['id']}: {poi['nombre']}")
    while True:
        try:
            poi_id = int(input(f"{prompt}: "))
            if any(p['id'] == poi_id for p in POIS):
                return poi_id
            else:
                print("ID no válido. Intente de nuevo.")
        except ValueError:
            print("Ingrese un número válido.")

def main():
    algo = Algorithms()
    print("Cargando datos del grafo y POIs...")
    print("¡Datos cargados correctamente!")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Ruta simple
            origen = seleccionar_poi("Seleccione POI de origen")
            destino = seleccionar_poi("Seleccione POI de destino")
            resultado = algo.ruta_simple(origen, destino)
            print("\nResultado Ruta Simple:")
            print("Ruta:", resultado['ruta'])
            print("Distancia:", resultado['distancia'])

        elif opcion == "2":  # Ruta con parada
            origen = seleccionar_poi("Seleccione POI de origen")
            parada = seleccionar_poi("Seleccione POI de parada")
            destino = seleccionar_poi("Seleccione POI de destino")
            resultado = algo.ruta_con_parada(origen, parada, destino)
            print("\nResultado Ruta con Parada:")
            print("Ruta:", resultado['ruta'])
            print("Distancia:", resultado['distancia'])

        elif opcion == "3":  # Ruta con obstáculo
            origen = seleccionar_poi("Seleccione POI de origen")
            destino = seleccionar_poi("Seleccione POI de destino")
            obstaculo = seleccionar_poi("Seleccione POI a evitar como obstáculo")
            resultado = algo.ruta_con_obstaculo(origen, destino, obstaculo)
            print("\nResultado Ruta con Obstáculo:")
            print("Ruta:", resultado['ruta'])
            print("Distancia:", resultado['distancia'])

        elif opcion == "4":  # Ruta con tráfico
            origen = seleccionar_poi("Seleccione POI de origen")
            destino = seleccionar_poi("Seleccione POI de destino")
            # Por simplicidad, no pedimos calles específicas, se usa factor extra por defecto
            resultado = algo.ruta_con_trafico(origen, destino)
            print("\nResultado Ruta con Tráfico:")
            print("Ruta:", resultado['ruta'])
            print("Distancia:", resultado['distancia'])

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
