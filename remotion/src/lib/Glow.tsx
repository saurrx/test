import React from "react";
import { useCurrentFrame } from "remotion";
import { noise, prog, rnd } from "./util";

type Pt = [number, number];
const toPath = (pts: Pt[]) => pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ");

// Named light paths, all in a 1080x1920 space around (cx, cy).
export const trailPoints = (shape: string, cx: number, cy: number, r: number, loops = 1, seed = 1): Pt[] => {
  const pts: Pt[] = []; const N = 220 * Math.max(1, Math.round(loops));
  for (let i = 0; i <= N; i++) {
    const t = i / N, a = t * Math.PI * 2 * loops - Math.PI / 2;
    if (shape === "circle") pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
    else if (shape === "ellipse") pts.push([cx + r * 0.62 * Math.cos(a), cy + r * 1.25 * Math.sin(a)]);
    else if (shape === "spiral") { const rr = r * (0.15 + 0.85 * t); pts.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a)]); }
    else if (shape === "scribble") { // chaotic "wrong way" motion
      const a2 = t * 14 + seed; pts.push([cx + r * (0.9 * Math.sin(a2 * 1.3) * Math.cos(a2 * 0.7) + 0.25 * Math.sin(a2 * 3.1)), cy + r * 1.3 * (0.8 * Math.sin(a2 * 0.9 + 1) * Math.cos(a2 * 1.9) + 0.2 * Math.cos(a2 * 2.7))]);
    } else if (shape === "infinity") pts.push([cx + r * Math.sin(a), cy + r * 0.5 * Math.sin(2 * a)]);
    else if (shape === "line") pts.push([cx - r + 2 * r * t, cy]);
    else if (shape === "rise") pts.push([cx + r * 0.25 * Math.sin(t * 9), cy + r - 2 * r * t]);
    else pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
  }
  return pts;
};

// A glowing light trail that draws itself: wide soft halo + core + bright head spark.
export const GlowTrail: React.FC<{ shape?: string; cx?: number; cy?: number; r?: number; loops?: number; from?: number; to?: number;
  color?: string; core?: string; width?: number; persist?: number; seed?: number; fadeOutAt?: number }> =
  ({ shape = "circle", cx = 540, cy = 900, r = 300, loops = 1, from = 0, to = 45, color = "#ffb648", core = "#fff6d8", width = 14, persist = 1, seed = 1, fadeOutAt }) => {
    const f = useCurrentFrame();
    const pts = trailPoints(shape, cx, cy, r, loops, seed);
    const t = prog(f, from, to, (x) => x * x * (3 - 2 * x));
    if (t <= 0) return null;
    const n = Math.max(2, Math.floor(pts.length * t));
    const start = persist >= 1 ? 0 : Math.max(0, n - Math.floor(pts.length * persist));
    const d = toPath(pts.slice(start, n)); const head = pts[n - 1];
    const fade = fadeOutAt === undefined ? 1 : 1 - prog(f, fadeOutAt, fadeOutAt + 12);
    const fl = 0.9 + 0.1 * noise(f / 2, seed);
    return (
      <g opacity={fade * fl} fill="none" strokeLinecap="round" strokeLinejoin="round">
        {glowStroke(d, color, width, 1.5)}
        <path d={d} stroke={core} strokeWidth={width * 0.45} />
        {t < 1 && <Halo cx={head[0]} cy={head[1]} r={width * 9} color={color} opacity={0.9} />}
        {t < 1 && <Halo cx={head[0]} cy={head[1]} r={width * 2.6} color={core} hard={0.3} />}
      </g>
    );
  };

// Soft light without SVG blur filters (software rendering makes big blurs cost seconds per frame):
// a radial gradient that fades to transparent. Works for circles and ellipses.
export const Halo: React.FC<{ cx: number; cy: number; r: number; ry?: number; color: string; opacity?: number; hard?: number }> = ({ cx, cy, r, ry, color, opacity = 1, hard = 0 }) => {
  const id = "h" + React.useId().replace(/[^a-zA-Z0-9]/g, "");
  return (
    <g>
      <defs><radialGradient id={id}><stop offset={`${hard * 100}%`} stopColor={color} stopOpacity={1} /><stop offset="45%" stopColor={color} stopOpacity={0.35} /><stop offset="100%" stopColor={color} stopOpacity={0} /></radialGradient></defs>
      <ellipse cx={cx} cy={cy} rx={r} ry={ry ?? r} fill={`url(#${id})`} opacity={opacity} />
    </g>
  );
};
export const GlowDefs: React.FC = () => null;
// Fake glow for strokes: stacked wider, fainter copies of the same path.
export const glowStroke = (d: string, color: string, w: number, k = 1) => (
  <>{[[7, 0.05], [4.4, 0.08], [2.6, 0.14], [1.6, 0.26]].map(([m, o], i) => <path key={i} d={d} stroke={color} strokeWidth={w * m} opacity={o * k} />)}</>
);

// Oil-lamp flame with flicker and a breathing halo.
export const Flame: React.FC<{ x: number; y: number; s?: number; color?: string; seed?: number }> = ({ x, y, s = 1, color = "#ffb648", seed = 1 }) => {
  const f = useCurrentFrame();
  const k = 1 + 0.12 * noise(f / 2.5, seed), sway = 5 * noise(f / 6, seed + 3) * s, h = 70 * s * k, w = 22 * s;
  const d = `M ${x - w} ${y} C ${x - w} ${y - h * 0.5}, ${x + sway - 4} ${y - h * 0.7}, ${x + sway} ${y - h} C ${x + sway + 4} ${y - h * 0.7}, ${x + w} ${y - h * 0.5}, ${x + w} ${y} C ${x + w} ${y + w * 0.9}, ${x - w} ${y + w * 0.9}, ${x - w} ${y} Z`;
  return (
    <g>
      <Halo cx={x} cy={y - h * 0.4} r={330 * s * k} color={color} opacity={0.5} />
      <Halo cx={x} cy={y - h * 0.4} r={110 * s} color={color} opacity={0.8} />
      <path d={d} fill={color} />
      <path d={d} fill="#fff8e0" transform={`translate(${x} ${y}) scale(0.5) translate(${-x} ${-y})`} />
    </g>
  );
};

export const Diya: React.FC<{ x: number; y: number; s?: number; color?: string; seed?: number; metal?: string }> = ({ x, y, s = 1, color, seed, metal = "#8a5a1c" }) => (
  <g>
    <path d={`M ${x - 46 * s} ${y} Q ${x} ${y + 44 * s} ${x + 46 * s} ${y} L ${x + 58 * s} ${y - 6 * s} Q ${x} ${y + 10 * s} ${x - 46 * s} ${y} Z`} fill={metal} />
    <rect x={x - 12 * s} y={y + 20 * s} width={24 * s} height={10 * s} fill={metal} />
    <Flame x={x + 4 * s} y={y - 4 * s} s={s} color={color} seed={seed} />
  </g>
);

// Sacred geometry that draws itself: rings, petals, interlocked triangles, bindu. Purely geometric.
export const Yantra: React.FC<{ cx?: number; cy?: number; r?: number; from?: number; dur?: number; color?: string; petals?: number; spin?: number; rings?: number; triangles?: number }> =
  ({ cx = 540, cy = 900, r = 380, from = 0, dur = 45, color = "#ffb648", petals = 8, spin = 0.15, rings = 3, triangles = 4 }) => {
    const f = useCurrentFrame(); const t = prog(f, from, from + dur); if (t <= 0) return null;
    const rot = (f - from) * spin; const C = 2 * Math.PI;
    const dash = (len: number, k: number) => ({ strokeDasharray: len, strokeDashoffset: len * (1 - prog(t, k, Math.min(1, k + 0.5), (x) => x)) });
    const tri = (rr: number, up: boolean, i: number) => {
      const a0 = up ? -Math.PI / 2 : Math.PI / 2; const p = [0, 1, 2].map((k) => [cx + rr * Math.cos(a0 + k * C / 3), cy + rr * Math.sin(a0 + k * C / 3)]);
      return <path key={`t${i}`} d={`M${p[0]} L${p[1]} L${p[2]} Z`} {...dash(rr * 5.2, 0.25 + i * 0.07)} />;
    };
    const body = (
      <g fill="none" stroke={color} strokeLinecap="round">
        {Array.from({ length: rings }).map((_, i) => { const rr = r * (1 - i * 0.07); return <circle key={i} cx={cx} cy={cy} r={rr} strokeWidth={i ? 3 : 6} {...dash(C * rr, i * 0.08)} transform={`rotate(-90 ${cx} ${cy})`} />; })}
        <g transform={`rotate(${rot} ${cx} ${cy})`}>
          {Array.from({ length: petals }).map((_, i) => {
            const a = (i / petals) * C, r1 = r * 0.6, r2 = r * 0.8, w = (C / petals) * 0.5;
            const p0 = [cx + r1 * Math.cos(a - w), cy + r1 * Math.sin(a - w)], p1 = [cx + r2 * 1.05 * Math.cos(a), cy + r2 * 1.05 * Math.sin(a)], p2 = [cx + r1 * Math.cos(a + w), cy + r1 * Math.sin(a + w)];
            return <path key={i} d={`M${p0} Q${cx + r2 * Math.cos(a - w * 0.6)} ${cy + r2 * Math.sin(a - w * 0.6)} ${p1} Q${cx + r2 * Math.cos(a + w * 0.6)} ${cy + r2 * Math.sin(a + w * 0.6)} ${p2}`} strokeWidth={4} {...dash(r * 1.2, 0.15 + (i / petals) * 0.3)} />;
          })}
        </g>
        <circle cx={cx} cy={cy} r={r * 0.58} strokeWidth={3} {...dash(C * r * 0.58, 0.2)} />
        <g strokeWidth={4} transform={`rotate(${-rot * 0.6} ${cx} ${cy})`}>
          {Array.from({ length: triangles }).map((_, i) => tri(r * (0.55 - i * 0.09), i % 2 === 0, i))}
        </g>
        <circle cx={cx} cy={cy} r={10 * prog(t, 0.7, 1)} fill={color} stroke="none" />
      </g>
    );
    return <g><g opacity={0.22} strokeWidth={18} style={{ strokeWidth: 18 }}>{body}</g>{body}<Halo cx={cx} cy={cy} r={r * 1.25} color={color} opacity={0.22 * t} /></g>;
  };

// Rays of light fanning from a point.
export const Rays: React.FC<{ cx?: number; cy?: number; color?: string; count?: number; len?: number; opacity?: number; spin?: number }> = ({ cx = 540, cy = 700, color = "#ffb648", count = 14, len = 1500, opacity = 0.18, spin = 0.1 }) => {
  const f = useCurrentFrame();
  return (
    <g opacity={opacity} transform={`rotate(${f * spin} ${cx} ${cy})`}>
      {Array.from({ length: count }).map((_, i) => {
        const a = (i / count) * Math.PI * 2, w = 0.05 + 0.05 * rnd(i, 4), k = 0.6 + 0.4 * Math.abs(Math.sin(f / 30 + i));
        return <path key={i} opacity={k} fill={color} d={`M${cx} ${cy} L${cx + len * Math.cos(a - w)} ${cy + len * Math.sin(a - w)} L${cx + len * Math.cos(a + w)} ${cy + len * Math.sin(a + w)} Z`} />;
      })}
    </g>
  );
};
