import React from "react";
import { useCurrentFrame } from "remotion";
import { Diya, Halo } from "./Glow";
import { noise } from "./util";

// A temple sanctum built from primitives: brick wall, alcove arch, pillars, steps, altar and an abstract idol
// (crowned silhouette with gold rim light, no facial features), lit by flickering lamps.
export const Temple: React.FC<{ idol?: "murti" | "lingam" | "lamp" | "none"; warm?: string; lamps?: number; glow?: number }> = ({ idol = "murti", warm = "#ffb648", lamps = 2, glow = 1 }) => {
  const f = useCurrentFrame(); const fl = 0.85 + 0.15 * noise(f / 3, 21);
  const bricks: React.ReactNode[] = [];
  for (let r = 0; r < 26; r++) for (let c = -1; c < 7; c++) {
    const x = c * 180 + (r % 2 ? 90 : 0), y = r * 74;
    bricks.push(<rect key={`${r}-${c}`} x={x + 3} y={y + 3} width={174} height={68} rx={4} fill="#2a1a10" opacity={0.25 + 0.2 * ((r * 7 + c * 13) % 5) / 5} />);
  }
  return (
    <g>
      <rect width={1080} height={1920} fill="#0b0605" />
      <g opacity={0.9}>{bricks}</g>
      {/* warm light pool from the lamps */}
      <Halo cx={540} cy={1000} r={760} ry={1050} color={warm} opacity={0.42 * fl * glow} />
      {/* alcove */}
      <path d="M250 1500 L250 640 Q250 330 540 330 Q830 330 830 640 L830 1500 Z" fill="#050203" />
      <path d="M250 1500 L250 640 Q250 330 540 330 Q830 330 830 640 L830 1500" fill="none" stroke="#6b4420" strokeWidth={16} />
      <path d="M214 1500 L214 640 Q214 290 540 290 Q866 290 866 640 L866 1500" fill="none" stroke="#3a2412" strokeWidth={10} />
      {/* pillars */}
      {[110, 906].map((x) => (
        <g key={x}>
          <rect x={x} y={420} width={64} height={1100} fill="#1c110a" /><rect x={x - 14} y={400} width={92} height={36} fill="#2c1b0f" /><rect x={x - 14} y={1500} width={92} height={36} fill="#2c1b0f" />
          <rect x={x} y={420} width={10} height={1100} fill={warm} opacity={0.12 * fl} />
        </g>
      ))}
      {/* idol */}
      {idol === "murti" && (
        <g>
          <Halo cx={540} cy={900} r={420} ry={640} color={warm} opacity={0.3 * fl * glow} />
          <path id="murti" d="M540 520 L575 600 Q640 610 640 700 Q640 770 600 800 Q720 830 730 980 L745 1320 L335 1320 L350 980 Q360 830 480 800 Q440 770 440 700 Q440 610 505 600 Z" fill="#150c07" stroke={warm} strokeOpacity={0.55 * fl} strokeWidth={5} />
          <path d="M470 610 Q540 560 610 610" fill="none" stroke={warm} strokeWidth={8} opacity={0.8 * fl} />
          <circle cx={540} cy={585} r={12} fill={warm} opacity={fl} />
          {/* garland */}
          <path d="M455 830 Q540 1060 625 830" fill="none" stroke="#d98b2b" strokeWidth={14} strokeDasharray="4 22" strokeLinecap="round" opacity={0.9} />
          <path d="M430 850 Q540 1180 650 850" fill="none" stroke="#b5451f" strokeWidth={12} strokeDasharray="3 24" strokeLinecap="round" opacity={0.8} />
        </g>
      )}
      {idol === "lingam" && (
        <g>
          <Halo cx={540} cy={1000} r={400} ry={560} color={warm} opacity={0.3 * fl * glow} />
          <path d="M440 1260 L440 900 Q440 780 540 780 Q640 780 640 900 L640 1260 Z" fill="#120a07" stroke={warm} strokeOpacity={0.5 * fl} strokeWidth={5} />
          <ellipse cx={540} cy={1270} rx={250} ry={52} fill="#1b100a" stroke={warm} strokeOpacity={0.4} strokeWidth={4} />
          {[0, 1, 2].map((i) => <path key={i} d={`M478 ${930 + i * 26} L602 ${930 + i * 26}`} stroke="#e8e0d0" strokeWidth={9} strokeLinecap="round" opacity={0.75} />)}
        </g>
      )}
      {idol === "lamp" && (
        <g><rect x={528} y={900} width={24} height={420} fill="#8a5a1c" /><path d="M450 1320 L630 1320 L600 1280 L480 1280 Z" fill="#8a5a1c" /><Diya x={540} y={890} s={1.6} color={warm} seed={5} /></g>
      )}
      {/* altar + steps */}
      <rect x={300} y={1320} width={480} height={70} fill="#24160d" /><rect x={300} y={1320} width={480} height={8} fill={warm} opacity={0.35 * fl} />
      <rect x={190} y={1500} width={700} height={50} fill="#1d120b" /><rect x={120} y={1550} width={840} height={60} fill="#170e09" /><rect x={0} y={1610} width={1080} height={310} fill="#0e0806" />
      {[...Array(9)].map((_, i) => <circle key={i} cx={340 + i * 50} cy={1308} r={11} fill={i % 2 ? "#d9541e" : "#f0b23a"} opacity={0.9} />)}
      {lamps >= 1 && <Diya x={170} y={1492} s={0.9} color={warm} seed={1} />}
      {lamps >= 2 && <Diya x={910} y={1492} s={0.9} color={warm} seed={2} />}
      {lamps >= 3 && <Diya x={540} y={1600} s={1.1} color={warm} seed={3} />}
    </g>
  );
};
