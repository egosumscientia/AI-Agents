"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { name: "0–500 Hz", nivel: 67 },
  { name: "500–1k Hz", nivel: 68 },
  { name: "1–2k Hz", nivel: 70 },
  { name: "2–4k Hz", nivel: 65 },
  { name: "4–8k Hz", nivel: 72 },
  { name: "8–12k Hz", nivel: 90 },
];

export default function ChartView() {
  return (
    <div className="w-full max-w-md mt-4">
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip />
          <Bar dataKey="nivel" fill="#06b6d4" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
