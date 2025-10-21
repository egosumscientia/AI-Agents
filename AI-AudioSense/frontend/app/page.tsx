"use client";
import { useState } from "react";
import AudioUploader from "./components/AudioUploader";
import ResultCard from "./components/ResultCard";
import ChartView from "./components/ChartView";

export default function HomePage() {
  const [data, setData] = useState<any>(null);

  return (
    <main className="min-h-screen bg-[#0f172a] text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-2">Demos de Inteligencia Artificial</h1>
      <h2 className="text-xl text-cyan-400 mb-6">AI–AudioSense</h2>
      <p className="text-center max-w-md mb-6">
        Analiza sonidos industriales para detectar patrones anómalos en motores,
        compresores o líneas de producción.
      </p>

      <AudioUploader onResult={setData} />

      {data && (
        <>
          <ChartView />
          <ResultCard data={data} />
        </>
      )}
    </main>
  );
}
