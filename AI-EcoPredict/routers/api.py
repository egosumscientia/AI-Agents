from fastapi import APIRouter
import requests
import pandas as pd
from services.weather_service import fetch_weather_data
from services.model_service import train_and_predict

router = APIRouter()


@router.get("/predict")
async def predict(
    city: str = "",
    lat: float | None = None,
    lon: float | None = None,
    target: str = "temperature_2m"
):
    """
    Endpoint para obtener predicciones de clima.
    Si se pasa una ciudad, usa geocoding.
    Si se pasan coordenadas, las corrige si están invertidas o con signo incorrecto.
    """

    # === CASO 1: Nombre de ciudad ===
    if city:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es"
            resp = requests.get(geo_url, timeout=10)
            if not resp.ok:
                print(f"⚠️ Error en API de geocodificación para '{city}'")
                return {"error": f"No se pudo obtener coordenadas para '{city}'"}

            data = resp.json()
            if not data.get("results"):
                print(f"⚠️ Ciudad '{city}' no encontrada en geocoding API.")
                return {"error": f"La ciudad '{city}' no existe o está mal escrita."}

            loc = data["results"][0]
            lat, lon = loc["latitude"], loc["longitude"]
            city = loc["name"]
            print(f"✅ Resolved city '{city}' -> ({lat}, {lon})")

        except Exception as e:
            print(f"❌ Error geocodificando '{city}': {e}")
            return {"error": f"No se pudo validar la ciudad '{city}'. Error: {e}"}

    # === CASO 2: Coordenadas ===
    elif lat is not None and lon is not None:
        try:
            # Corrige coordenadas invertidas (usuario pone lon en lat)
            if abs(lat) > 90 and abs(lon) < 90:
                lat, lon = lon, lat
                print(f"⚠️ Coordenadas invertidas -> ({lat}, {lon})")

            # Corrige signo de longitud (si el usuario mete positivo en occidente)
            if lon > 0:
                lon = -lon
                print(f"⚠️ Corrigiendo signo de longitud -> ({lon})")

            # Reverse geocoding para mostrar ciudad en el gráfico
            geo_url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
            resp = requests.get(
                geo_url, headers={"User-Agent": "AI-EcoPredict"}, timeout=10)
            if resp.ok:
                address = resp.json().get("address", {})
                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or address.get("county")
                    or f"Lat: {lat:.2f}, Lon: {lon:.2f}"
                )
                print(f"✅ Reverse geocoded to '{city}'")
            else:
                city = f"Lat: {lat:.2f}, Lon: {lon:.2f}"

        except Exception as e:
            print(f"⚠️ Error en reverse geocoding: {e}")
            city = f"Lat: {lat:.2f}, Lon: {lon:.2f}"

    # === CASO 3: Sin parámetros válidos ===
    else:
        print("❌ Debes ingresar una ciudad o coordenadas.")
        return {"error": "Debes ingresar una ciudad o coordenadas válidas."}

    # === Obtiene datos y predicciones ===
    print(f"🌍 Fetching weather for {city} @ ({lat}, {lon})")

    df = fetch_weather_data(lat, lon)
    preds = train_and_predict(df, target=target)

    actual = df[target].tolist()
    timestamps = df["time"].astype(str).tolist()[-len(preds):]

    mae = abs(df[target] - pd.Series(preds)).mean()
    print(f"✅ MAE for {target}: {mae:.3f}")

    return {
        "city": city,
        "target": target,
        "predictions": preds,
        "actual": actual,
        "timestamps": timestamps,
    }
