from fastapi import APIRouter, Request
from services.weather_service import fetch_weather_data
from services.model_service import train_and_predict
import requests

router = APIRouter(prefix="/api")


@router.get("/predict")
async def predict(
    city: str = "",
    lat: float | None = None,
    lon: float | None = None,
    target: str = "temperature_2m"
):
    """Fetch data from Open-Meteo, geocode city name if needed, then predict."""

    # --- Try geocoding if a city name was provided ---
    if city:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            resp = requests.get(geo_url, timeout=10)
            if resp.ok and resp.json().get("results"):
                loc = resp.json()["results"][0]
                lat = loc["latitude"]
                lon = loc["longitude"]
                city = loc.get("name", city)
                print(f"Resolved city '{city}' -> ({lat}, {lon})")
            else:
                print(f"⚠️ City '{city}' not found, no coordinates resolved.")
        except Exception as e:
            print(f"⚠️ Geocoding failed: {e}")

    # --- Default fallback only if *nothing* is provided ---
    if (
        lat is None
        or lon is None
        or str(lat).lower() == "nan"
        or str(lon).lower() == "nan"
    ):
        if not city:
            # Only use Bogotá if there is no city and no coordinates
            city = "Bogotá"
            lat, lon = 4.61, -74.08
            print(f"Using fallback coordinates for {city}: ({lat}, {lon})")
        else:
            print(
                f"No coordinates found for '{city}', cannot geocode — using name only.")

    # --- Fetch weather data ---
    df = fetch_weather_data(lat, lon)
    preds = train_and_predict(df, target=target)
    actual = df[target].tolist()
    timestamps = df["time"].astype(str).tolist()[-len(preds):]

    return {
        "city": city,
        "target": target,
        "predictions": preds,
        "actual": actual,
        "timestamps": timestamps,
    }


@router.post("/update")
async def update_model(request: Request):
    """Manual retraining triggered from UI button."""
    payload = await request.json()
    lat, lon = payload.get("lat"), payload.get("lon")
    df = fetch_weather_data(lat, lon)
    _ = train_and_predict(df, retrain=True)
    return {"status": "Model retrained successfully"}
