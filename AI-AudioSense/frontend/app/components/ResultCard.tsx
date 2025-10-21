export default function ResultCard({ data }: any) {
  const isAnomalous = data.status === "Anómalo";

  return (
    <div className="bg-slate-800 rounded-xl p-4 mt-6 w-full max-w-md shadow-lg">
      <h3
        className={`font-bold text-lg mb-2 ${
          isAnomalous ? "text-red-400" : "text-green-400"
        }`}
      >
        Diagnóstico IA
      </h3>

      <ul className="mt-2 text-sm space-y-1">
        <li>🎧 <b>Nivel RMS:</b> {data.rms_db?.toFixed(2)} dB</li>
        <li>🎚 <b>Frecuencia dominante:</b> {data.dominant_freq_hz} Hz</li>
        <li>📈 <b>Relación SNR:</b> {data.snr_db?.toFixed(2)} dB</li>
        <li>🌀 <b>Flatness:</b> {data.flatness?.toFixed(3)}</li>
        <li>⚡ <b>Crest Factor:</b> {data.crest_factor?.toFixed(2)}</li>
        <li>🤖 <b>Confianza IA:</b> {data.confidence_percent?.toFixed(1)}%</li>
        <li>📊 <b>Estado:</b> {data.status}</li>
      </ul>

      {/* Indicador visual de confianza */}
      <div className="mt-3">
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-700 ${
              data.confidence_percent > 85
                ? "bg-green-400"
                : data.confidence_percent > 60
                ? "bg-yellow-400"
                : "bg-red-500"
            }`}
            style={{ width: `${data.confidence_percent}%` }}
          ></div>
        </div>
      </div>

      {/* Mensaje final */}
      <p
        className={`mt-3 font-medium ${
          isAnomalous ? "text-yellow-400" : "text-green-400"
        }`}
      >
        {data.mensaje}
      </p>

      {/* Nombre del archivo */}
      <p className="text-xs text-slate-400 mt-2 italic">
        Archivo analizado: {data.filename}
      </p>
    </div>
  );
}
