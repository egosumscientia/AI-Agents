"use client";
import { useState } from "react";

export default function AudioUploader({ onResult }: any) {
  const [loading, setLoading] = useState(false);

  const handleFile = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    onResult(data);
    setLoading(false);
  };

  return (
    <div className="mb-6 flex flex-col items-center">
      <input type="file" accept="audio/*" onChange={handleFile} />
      <button
        disabled={loading}
        className="mt-3 bg-emerald-500 px-4 py-2 rounded hover:bg-emerald-600"
      >
        {loading ? "Analizando..." : "Reanalizar"}
      </button>
    </div>
  );
}
