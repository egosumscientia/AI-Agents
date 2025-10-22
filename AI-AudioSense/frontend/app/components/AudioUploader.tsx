"use client";
import { useState } from "react";

export default function AudioUploader({ onResult }: any) {
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const analyzeFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://ai-audiosense-backend:8000"}/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);

      const data = await res.json();
      onResult(data);
    } catch (err) {
      console.error("Error al analizar el archivo:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFile = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    await analyzeFile(file);
  };

  const handleAnalyzeClick = async () => {
    if (selectedFile) {
      await analyzeFile(selectedFile);
    }
  };

  return (
    <div className="mb-6 flex flex-col items-center space-y-4">
      <input
        type="file"
        accept="audio/*"
        onChange={handleFile}
        title="Seleccionar archivo de audio"
        aria-label="Seleccionar archivo de audio"
      />

      <button
        onClick={handleAnalyzeClick}
        disabled={!selectedFile || loading}
        className={`px-4 py-2 rounded text-white transition ${
          loading
            ? "bg-emerald-500 animate-pulse"
            : selectedFile
            ? "bg-emerald-500 hover:bg-emerald-600"
            : "bg-gray-500 cursor-not-allowed"
        }`}
      >
        {loading ? "Analizando..." : "Analizar"}
      </button>

      {selectedFile && (
        <p className="text-xs text-gray-400 mt-1 italic">
          Archivo actual: {selectedFile.name}
        </p>
      )}
    </div>
  );
}
