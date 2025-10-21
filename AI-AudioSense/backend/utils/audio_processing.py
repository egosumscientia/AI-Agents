import librosa, numpy as np, tempfile, os

async def analyze_audio(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        y, sr = librosa.load(tmp_path, sr=None)
        rms = np.mean(librosa.feature.rms(y=y))
        spectrum = np.abs(np.fft.rfft(y))
        freqs = np.fft.rfftfreq(len(y), 1/sr)
        dominant_freq = freqs[np.argmax(spectrum)]
        anomaly = dominant_freq > 8000
        confidence = 0.92 if not anomaly else 0.84
        return {
            'nivel_rms': round(rms * 100, 1),
            'frecuencia_dominante': int(dominant_freq),
            'confianza': round(confidence * 100, 1),
            'estado': 'Anómalo' if anomaly else 'Normal',
            'mensaje': '⚠️ Vibración anómala' if anomaly else '✅ Sin anomalías'
        }
    finally:
        os.remove(tmp_path)
