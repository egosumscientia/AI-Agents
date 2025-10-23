from fastapi import APIRouter, Request
from services.weather_service import fetch_weather_data
from services.model_service import train_and_predict

router = APIRouter(prefix="/api")

@router.get("/predict")
async def predict(city: str = "Bogotá", lat: float = 4.61, lon: float = -74.08):
    data = fetch_weather_data(lat, lon)
    predictions = train_and_predict(data)
    return {"city": city, "predictions": predictions}

@router.post("/update")
async def update_model(request: Request):
    payload = await request.json()
    lat, lon = payload.get("lat"), payload.get("lon")
    data = fetch_weather_data(lat, lon)
    predictions = train_and_predict(data, retrain=True)
    return {"status": "Model retrained", "predictions": predictions}
