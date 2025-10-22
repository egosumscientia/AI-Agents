"use client";
import { useState } from "react";
import AudioUploader from "./components/AudioUploader";
import ResultCard from "./components/ResultCard";
import ChartView from "./components/ChartView";

export default function HomePage() {
  const [data, setData] = useState<any>(null);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 text-slate-100">
      <section className="mx-auto max-w-4xl px-4 py-12 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-cyan-300">
          Demos de Inteligencia Artificial
        </h1>
        <h2 className="text-2xl md:text-3xl text-cyan-400 mt-2 font-semibold">
          AI–AudioSense
        </h2>
        <p className="mt-4 text-slate-400 max-w-2xl mx-auto">
          Analiza sonidos industriales para detectar patrones anómalos en motores,
          compresores o líneas de producción.
        </p>
      </section>

      <section className="mx-auto max-w-3xl px-4 pb-16">
        <AudioUploader onResult={setData} />

        {data && (
          <div className="mt-10 space-y-8">
            <ChartView levels={data.band_levels} />
            <ResultCard data={data} />
          </div>
        )}
      </section>
    </main>
  );
}