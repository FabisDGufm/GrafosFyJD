from algorithms import Algorithms

def main():
    algo = Algorithms()  

    
    origen = 14206194901  # Parque 14
    destino = 14206194905  # CC Montufar
    parada = 14206194903   # Plaza Obelisco
    obstaculo = 14206194904  # Plaza España

    print("\n=== RUTA SIMPLE ===")
    res = algo.ruta_simple(origen, destino)
    print(res)

    print("\n=== RUTA CON PARADA ===")
    res = algo.ruta_con_parada(origen, parada, destino)
    print(res)

    print("\n=== RUTA CON OBSTACULO ===")
    res = algo.ruta_con_obstaculo(origen, destino, obstaculo)
    print(res)

    print("\n=== RUTA CON TRAFICO ===")
    res = algo.ruta_con_trafico(origen, destino)
    print(res)

if __name__ == "__main__":
    main()
