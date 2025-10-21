export default function ResultCard({ data }: any) {
  return (
    <div className="bg-slate-800 rounded-xl p-4 mt-6 w-full max-w-md">
      <h3 className={`font-bold ${data.estado === "Anómalo" ? "text-red-400" : "text-green-400"}`}>
        Diagnóstico IA
      </h3>
      <ul className="mt-2 text-sm">
        <li>🎧 Nivel RMS: {data.nivel_rms} dB</li>
        <li>🎚 Frecuencia dominante: {data.frecuencia_dominante} Hz</li>
        <li>🤖 Confianza IA: {data.confianza}%</li>
        <li>📊 Estado: {data.estado}</li>
      </ul>
      <p className="mt-3 text-yellow-400">{data.mensaje}</p>
    </div>
  );
}
