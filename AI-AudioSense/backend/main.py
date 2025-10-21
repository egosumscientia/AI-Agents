from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import librosa
import numpy as np

# 🚀 Inicializa app
app = FastAPI(title="AI-AudioSense Backend")

# 🚀 Configura CORS antes de registrar cualquier ruta
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Endpoint principal


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ Usa tu función avanzada desde utils/audio_processing
        from utils.audio_processing import analyze_audio
        result = await analyze_audio(file)
        result["filename"] = file.filename
        return result

    except Exception as e:
        import traceback
        print("🔥 Error en /analyze:", e)
        traceback.print_exc()
        return {"error": str(e)}

# 🚀 Punto de arranque
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
