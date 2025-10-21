from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.audio_processing import analyze_audio
import uvicorn

app = FastAPI(title='AI-AudioSense Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    results = await analyze_audio(file)
    return results

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
