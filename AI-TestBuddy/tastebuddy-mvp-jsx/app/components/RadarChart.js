import React from 'react';
import Svg, { Polygon, Circle, Line, Text as SvgText } from 'react-native-svg';

const DIMENSIONS = ['Dulce', 'Salado', 'Ácido', 'Amargo', 'Umami', 'Picante', 'Crujiente'];

export const RadarChart = ({ values, size = 260, levels = 4 }) => {
  const N = DIMENSIONS.length;
  const R = size / 2 - 24;
  const center = { x: size / 2, y: size / 2 };

  const points = values.map((val, i) => {
    const angle = (Math.PI * 2 * i) / N - Math.PI / 2;
    const r = val * R;
    return [center.x + r * Math.cos(angle), center.y + r * Math.sin(angle)];
  });

  return (
    <Svg width={size} height={size}>
      {[...Array(levels)].map((_, idx) => (
        <Circle key={idx} cx={center.x} cy={center.y} r={(idx + 1) * (R / levels)} fill="none" stroke="#e6e6e6" />
      ))}
      {DIMENSIONS.map((label, i) => {
        const angle = (Math.PI * 2 * i) / N - Math.PI / 2;
        const x = center.x + R * Math.cos(angle);
        const y = center.y + R * Math.sin(angle);
        const lx = center.x + (R + 12) * Math.cos(angle);
        const ly = center.y + (R + 12) * Math.sin(angle);
        return (
          <React.Fragment key={i}>
            <Line x1={center.x} y1={center.y} x2={x} y2={y} stroke="#d0d0d0" />
            <SvgText x={lx} y={ly} fontSize="12" fill="#333" textAnchor="middle">{label}</SvgText>
          </React.Fragment>
        );
      })}
      <Polygon points={points.map(([x, y]) => `${x},${y}`).join(' ')} fill="rgba(40,167,69,0.25)" stroke="#28a745" strokeWidth={2} />
    </Svg>
  );
};
