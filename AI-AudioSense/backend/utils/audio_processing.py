
import librosa
import numpy as np
import tempfile
import os

# 🧠 Conversión recursiva de tipos NumPy a tipos nativos de Python


def to_native_types(data):
    if isinstance(data, dict):
        return {k: to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_native_types(v) for v in data]
    elif isinstance(data, (np.floating, np.float32, np.float64)):
        return float(data)
    elif isinstance(data, (np.integer,)):
        return int(data)
    elif isinstance(data, (np.bool_)):
        return bool(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data


# 🚀 Función principal de análisis
async def analyze_audio(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # --- Carga de audio ---
        y, sr = librosa.load(tmp_path, sr=None)
        y = librosa.util.normalize(y)

        # --- Cálculos principales ---
        rms = np.mean(librosa.feature.rms(y=y))
        spectrum = np.abs(np.fft.rfft(y))
        freqs = np.fft.rfftfreq(len(y), 1 / sr)
        dominant_freq = freqs[np.argmax(spectrum)]

        # --- Métricas avanzadas ---
        signal_power = np.mean(y**2)
        noise_est = np.percentile(np.abs(y), 5)
        snr_db = 10 * np.log10(signal_power / (noise_est**2 + 1e-10))
        flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        crest_factor = np.max(np.abs(y)) / np.sqrt(np.mean(y**2))

        # --- Detección espectral por bandas (normalizada) ---
        band_levels, peak_flags = analyze_spectrum(y, sr)

        # --- Reglas heurísticas (versión equilibrada) ---
        max_band = max(band_levels)
        avg_band = np.mean(band_levels)
        std_band = np.std(band_levels)
        band_spread = max_band - avg_band

        # 🔹 Umbrales ajustables (parámetros de sensibilidad)
        SPREAD_LIMIT = 15       # dB entre banda más alta y promedio
        STD_LIMIT = 6           # dB de desviación típica entre bandas
        FREQ_LIMIT = 8800       # Hz
        FLATNESS_LIMIT = 0.4    # sin unidad

        # Evaluación por criterios combinados
        spread_anomaly = band_spread > SPREAD_LIMIT
        variance_anomaly = std_band > STD_LIMIT
        freq_anomaly = dominant_freq > FREQ_LIMIT
        flatness_anomaly = flatness > FLATNESS_LIMIT

        # Condición general: spread + varianza o alta frecuencia o ruido excesivo
        anomaly = (
            spread_anomaly and variance_anomaly) or freq_anomaly or flatness_anomaly

        confianza = 95.0 if not anomaly else 83.0
        estado = "Anómalo" if anomaly else "Normal"
        mensaje = "⚠️ Vibración anómala detectada" if anomaly else "✅ Sin anomalías detectadas"

        # --- Resultado JSON final ---
        result = {
            "rms_db": round(rms * 100, 1),
            "dominant_freq_hz": int(dominant_freq),
            "confidence_percent": round(confianza, 1),
            "status": estado,
            "mensaje": mensaje,
            "snr_db": round(snr_db, 2),
            "flatness": round(flatness, 3),
            "crest_factor": round(crest_factor, 2),
            "band_levels": band_levels,
            "peak_flags": peak_flags,
        }

        # ✅ Conversión profunda antes de retornar (garantiza JSON válido)
        return to_native_types(result)

    finally:
        os.remove(tmp_path)


# 📊 Función auxiliar para análisis por bandas (FFT normalizada)
def analyze_spectrum(y, sr):
    """
    Calcula energía promedio (en dB normalizados) por banda de frecuencia
    y marca picos anómalos según desviación estándar.
    """
    # FFT y energía espectral
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1 / sr)

    # 🔹 Normalización: 0 dB = pico máximo de la señal
    spectrum_db = 20 * np.log10(spectrum / (np.max(spectrum) + 1e-6) + 1e-6)

    # Definición de bandas industriales
    bands = [0, 500, 1000, 4000, 8000, 12000]
    band_levels = []

    for i in range(len(bands) - 1):
        idx = np.where((freqs >= bands[i]) & (freqs < bands[i + 1]))[0]
        if len(idx) > 0:
            energy = np.mean(spectrum_db[idx])
            band_levels.append(round(energy, 2))
        else:
            band_levels.append(-120.0)  # ruido de fondo

    avg = np.mean(band_levels)
    std = np.std(band_levels)
    peak_flags = [abs(b - avg) > 1.5 * std for b in band_levels]

    return band_levels, peak_flags
