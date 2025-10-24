from fastapi import FastAPI
from app.routers import chat, health

app = FastAPI(title="Food Sales Agent API", version="1.0.0")
app.include_router(chat.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "API del Asistente de Ventas en línea ✅"}
