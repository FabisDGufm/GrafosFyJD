import os
import sys
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def main():
    # 1. Pedir ruta del CSV
    ruta_csv = input(
        "Ruta del CSV de intersecciones (ENTER para usar 'intersecciones.csv'): "
    ).strip()

    if ruta_csv == "":
        ruta_csv = "intersecciones.csv"

    if not os.path.exists(ruta_csv):
        print(f"No se encontró el archivo: {ruta_csv}")
        print("Coloca el CSV en la misma carpeta o escribe la ruta completa.")
        sys.exit(1)

    print(f"Usando archivo: {ruta_csv}")

    # 2. Cargar CSV
    try:
        df = pd.read_csv(ruta_csv)
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        sys.exit(1)

    # Validar columnas mínimas
    columnas_requeridas = {"lat", "lon"}
    if not columnas_requeridas.issubset(df.columns):
        print("El CSV debe tener al menos las columnas: lat, lon")
        print(f"Columnas encontradas: {list(df.columns)}")
        sys.exit(1)

    total_filas = len(df)
    print(f"Filas totales en el CSV: {total_filas}")

    # 3. Preguntar si quieres limitar el número de filas (para probar)
    limite_input = input(
        "¿Cuántas filas quieres procesar? (ENTER = todas, o escribe un número para prueba): "
    ).strip()

    limite = None
    if limite_input != "":
        try:
            limite = int(limite_input)
            if limite <= 0:
                print("Número no válido, se procesarán todas las filas.")
                limite = None
            else:
                print(f"Se procesarán solo las primeras {limite} filas.")
        except ValueError:
            print("Entrada no válida, se procesarán todas las filas.")
    else:
        print("Se procesarán todas las filas.")

    # 4. Configurar geolocalizador
    geolocator = Nominatim(user_agent="rd375_reverse_geocoder")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    def obtener_direccion(row, idx, total):
        lat = row["lat"]
        lon = row["lon"]
        try:
            print(f"[{idx+1}/{total}] Buscando dirección para ({lat}, {lon})...")
            location = reverse((lat, lon), language="es")

            if location is None:
                print("  -> No se encontró dirección, se deja vacío.")
                return None

            address = location.raw.get("address", {})

            road = address.get("road")
            neighbourhood = address.get("neighbourhood")
            suburb = address.get("suburb")
            city = address.get("city") or address.get("town") or address.get("village")
            state = address.get("state")
            country = address.get("country")

            partes = []
            if road:
                partes.append(road)
            if neighbourhood:
                partes.append(neighbourhood)
            if suburb:
                partes.append(suburb)
            if city:
                partes.append(city)
            if state:
                partes.append(state)
            if country:
                partes.append(country)

            direccion = ", ".join(partes) if partes else location.address

            print(f"  -> Dirección: {direccion}")
            return direccion

        except Exception as e:
            print(f"Error en ({lat}, {lon}): {e}")
            return None

    # 5. Aplicar con progreso
    total_procesar = limite if limite else len(df)

    if "direccion" not in df.columns:
        df["direccion"] = None

    contador = 0
    for idx, row in df.iterrows():
        if limite and contador >= limite:
            break
        if pd.isna(row.get("direccion")) or row.get("direccion") == "" or row.get("direccion") is None:
            direccion = obtener_direccion(row, contador, total_procesar)
            df.at[idx, "direccion"] = direccion
        else:
            print(f"[{contador+1}/{total_procesar}] Ya tiene direccion, saltando...")
        contador += 1

    # 7. Nombre de salida
    nombre_salida_defecto = "intersecciones_con_dir.csv"
    salida_input = input(
        f"Nombre del CSV de salida (ENTER para usar '{nombre_salida_defecto}'): "
    ).strip()
    if salida_input == "":
        salida_csv = nombre_salida_defecto
    else:
        salida_csv = salida_input

    df.to_csv(salida_csv, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {salida_csv}")
    print("Listo.")


if __name__ == "__main__":
    main()
