from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import dashboard, api

app = FastAPI(title="AI–EcoPredict")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routers
app.include_router(dashboard.router)
app.include_router(api.router)
