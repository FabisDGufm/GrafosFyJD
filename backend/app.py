from algorithms import Algorithms

def mostrar_menu():
    print("\n=== MENU ===")
    print("1. Listar todos los POIs")
    print("2. Ver información de un POI")
    print("3. Ruta simple")
    print("4. Ruta con parada")
    print("5. Ruta con obstáculo")
    print("6. Ruta considerando tráfico")
    print("0. Salir")

def seleccionar_poi(algo):
    pois = algo.obtener_pois()
    print("\nPOIs disponibles:")
    for poi in pois:
        info = algo.obtener_info_poi(poi)
        print(f"{poi}: {info['nombre']}")
    try:
        elegido = int(input("Ingresa el ID del POI: "))
        if elegido in pois:
            return elegido
        else:
            print("POI no válido.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def main():
    algo = Algorithms()
    print(f"Grafo cargado: {len(algo.grafo.nodes)} nodos, {len(algo.grafo.edges)} aristas")
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            pois = algo.obtener_pois()
            print("\nPOIs disponibles:")
            for poi in pois:
                info = algo.obtener_info_poi(poi)
                print(f"{poi}: {info['nombre']} - {info['direccion']}")

        elif opcion == "2":
            poi_id = seleccionar_poi(algo)
            if poi_id:
                info = algo.obtener_info_poi(poi_id)
                print(f"\nInfo POI {poi_id}: {info}")

        elif opcion == "3":
            print("\nRuta simple")
            inicio = seleccionar_poi(algo)
            destino = seleccionar_poi(algo)
            if inicio and destino:
                resultado = algo.ruta_simple(inicio, destino)
                print(f"Ruta: {resultado['ruta']}")
                print(f"Distancia: {resultado['distancia']}")

        elif opcion == "4":
            print("\nRuta con parada")
            inicio = seleccionar_poi(algo)
            parada = seleccionar_poi(algo)
            destino = seleccionar_poi(algo)
            if inicio and parada and destino:
                resultado = algo.ruta_con_parada(inicio, parada, destino)
                print(f"Ruta: {resultado['ruta']}")
                print(f"Distancia: {resultado['distancia']}")

        elif opcion == "5":
            print("\nRuta con obstáculo")
            inicio = seleccionar_poi(algo)
            destino = seleccionar_poi(algo)
            obstaculo = seleccionar_poi(algo)
            if inicio and destino and obstaculo:
                resultado = algo.ruta_con_obstaculo(inicio, destino, obstaculo)
                print(f"Ruta: {resultado['ruta']}")
                print(f"Distancia: {resultado['distancia']}")

        elif opcion == "6":
            print("\nRuta considerando tráfico")
            inicio = seleccionar_poi(algo)
            destino = seleccionar_poi(algo)
            if inicio and destino:
                # Aquí puedes definir un dict de calles con factor de tráfico
                factor_calles = {}
                resultado = algo.ruta_con_trafico(inicio, destino, factor_calles=factor_calles)
                print(f"Ruta: {resultado['ruta']}")
                print(f"Distancia: {resultado['distancia']}")

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
