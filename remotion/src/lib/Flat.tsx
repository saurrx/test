import React from "react";
import { noise, prog, rnd } from "./util";
import { Halo } from "./Glow";

// All shapes draw around (0,0) in their own space; Layer positions and scales them. `t` = frames since the layer appeared.
type SP = { t: number; color: string; color2: string; [k: string]: any };

// Warli-style figure: circle head, two triangles, stick limbs. Poses are limb angles in degrees; `anim` moves them.
export const Figure: React.FC<SP> = ({ t, color, pose = "stand", anim = "idle", prop, crown, seed = 1 }) => {
  const sw = Math.sin(t / 5 + seed), sl = Math.sin(t / 9 + seed);
  let aL = 200, aR = -20, lL = 100, lR = 80, lean = 0, dy = 0;
  if (pose === "arms_up") { aL = 250; aR = -70; }
  if (pose === "pray") { aL = 300; aR = -120; }
  if (pose === "point") { aR = -10; aL = 160; }
  if (pose === "lift") { aL = 270 - 20 * Math.min(1, t / 20); aR = -90 + 20 * Math.min(1, t / 20); }
  if (pose === "pull") { aL = 185; aR = 175; lean = -22; lL = 120; lR = 95; }
  if (pose === "draw") { aL = 180; aR = 0 - 25 * prog(t, 10, 40); }
  if (pose === "kneel") { lL = 150; lR = 20; dy = 30; lean = 12; }
  if (pose === "fall") { lean = 90 * prog(t, 0, 14); dy = 60 * prog(t, 0, 14); }
  if (anim === "walk") { lL = 90 + 28 * sw; lR = 90 - 28 * sw; aL = 190 + 20 * sw; aR = -10 - 20 * sw; dy += 3 * Math.abs(sw); }
  if (anim === "dance") { aL = 240 + 35 * sw; aR = -60 - 35 * sw; lL = 105 + 15 * sw; lR = 75 - 15 * sw; dy += 8 * Math.abs(sw); }
  if (anim === "idle") { aL += 4 * sl; aR -= 4 * sl; }
  if (anim === "strain") { lean += 3 * sw; }
  if (anim === "tremble") { lean += 4 * noise(t / 1.5, seed); }
  const limb = (x: number, y: number, a: number, len: number, w = 7) => { const r = (a * Math.PI) / 180; return <line x1={x} y1={y} x2={x + len * Math.cos(r)} y2={y + len * Math.sin(r)} stroke={color} strokeWidth={w} strokeLinecap="round" />; };
  return (
    <g transform={`translate(0 ${dy}) rotate(${lean} 0 60)`}>
      {limb(-10, 58, lL, 62)}{limb(10, 58, lR, 62)}
      <path d="M-30 -40 L30 -40 L0 12 Z" fill={color} /><path d="M0 8 L-26 60 L26 60 Z" fill={color} />
      {limb(-26, -36, aL, 52, 6)}{limb(26, -36, aR, 52, 6)}
      <circle cx={0} cy={-62} r={17} fill={color} />
      {crown && <path d="M-16 -78 L-16 -98 L-8 -86 L0 -102 L8 -86 L16 -98 L16 -78 Z" fill={color} />}
      {prop === "staff" && <line x1={52} y1={-90} x2={52} y2={120} stroke={color} strokeWidth={6} strokeLinecap="round" />}
      {prop === "bun" && <circle cx={0} cy={-84} r={9} fill={color} />}
      {prop === "axe" && <g><line x1={60} y1={-110} x2={60} y2={60} stroke={color} strokeWidth={6} strokeLinecap="round" /><path d="M60 -110 Q100 -100 96 -66 Q78 -78 60 -76 Z" fill={color} /></g>}
    </g>
  );
};

export const Crowd: React.FC<SP> = ({ t, color, color2, count = 24, cols = 8, gap = 78, rowGap = 110, pose = "stand", anim = "idle", stagger = 1 }) => (
  <g>
    {Array.from({ length: count }).map((_, i) => {
      const c = i % cols, r = Math.floor(i / cols), show = prog(t, i * stagger, i * stagger + 6);
      return show <= 0 ? null : (
        <g key={i} opacity={show} transform={`translate(${(c - (cols - 1) / 2) * gap + (r % 2 ? gap / 2 : 0)} ${r * rowGap}) scale(${0.55 + 0.45 * show})`}>
          <Figure t={t + i * 3} color={color} color2={color2} pose={pose} anim={anim} seed={i} />
        </g>
      );
    })}
  </g>
);

// A great bow. `draw` 0..1 pulls the string; `broken` 0..1 snaps it in two.
export const Bow: React.FC<SP> = ({ t, color, color2, draw = 0, breakAt, glow = true }) => {
  const b = breakAt === undefined ? 0 : prog(t, breakAt, breakAt + 10); const pull = 120 * draw * (1 - b);
  const half = (sign: number) => (
    <g transform={`rotate(${sign * 38 * b}) translate(${-40 * b} ${sign * 60 * b})`}>
      <path d={`M0 0 Q-150 ${sign * 160} 0 ${sign * 420}`} fill="none" stroke={color} strokeWidth={22} strokeLinecap="round" />
      <path d={`M0 ${sign * 420} q14 ${sign * 22} -22 ${sign * 34}`} fill="none" stroke={color} strokeWidth={12} strokeLinecap="round" />
      {b < 0.2 && <line x1={0} y1={sign * 420} x2={pull} y2={0} stroke={color2} strokeWidth={4} />}
      {b >= 0.2 && <path d={`M0 ${sign * 420} q${40 + 30 * noise(t / 3, sign)} ${-sign * 120} ${20} ${-sign * 230}`} fill="none" stroke={color2} strokeWidth={4} opacity={1 - b * 0.4} />}
    </g>
  );
  return (
    <g>
      {glow && <Halo cx={-40} cy={0} r={320} ry={640} color={color2} opacity={0.35 + 0.6 * b} />}
      {half(-1)}{half(1)}
      {b > 0 && b < 1 && <circle cx={0} cy={0} r={320 * b} fill="none" stroke="#fff" strokeWidth={30 * (1 - b)} />}
    </g>
  );
};

export const Chest: React.FC<SP> = ({ t, color, color2, wheels = 8, roll = 0 }) => (
  <g>
    <rect x={-330} y={-150} width={660} height={190} rx={14} fill={color} />
    {[-220, -110, 0, 110, 220].map((x) => <rect key={x} x={x - 6} y={-150} width={12} height={190} fill={color2} opacity={0.5} />)}
    <rect x={-330} y={-70} width={660} height={12} fill={color2} opacity={0.5} />
    {Array.from({ length: wheels / 2 }).map((_, i) => { const x = -270 + (i * 540) / (wheels / 2 - 1); return (
      <g key={i} transform={`translate(${x} 60) rotate(${t * roll})`}><circle r={52} fill="none" stroke={color} strokeWidth={14} />{[0, 45, 90, 135].map((a) => <line key={a} x1={-50} x2={50} y1={0} y2={0} stroke={color} strokeWidth={8} transform={`rotate(${a})`} />)}</g>); })}
  </g>
);

export const Hills: React.FC<SP> = ({ color, seed = 1, amp = 120, w = 1400 }) => {
  let d = `M${-w / 2} 400`; for (let i = 0; i <= 14; i++) { const x = -w / 2 + (i * w) / 14; d += ` L${x} ${-amp * (0.3 + 0.7 * rnd(i, seed)) * Math.abs(Math.sin(i * 0.9 + seed))}`; }
  return <path d={d + ` L${w / 2} 400 Z`} fill={color} />;
};
export const Mountain: React.FC<SP> = ({ color, color2 }) => (<g><path d="M-420 300 L-60 -420 L40 -260 L140 -380 L460 300 Z" fill={color} /><path d="M-60 -420 L-130 -280 L-40 -320 L10 -250 L40 -260 Z" fill={color2} opacity={0.9} /></g>);
export const Sun: React.FC<SP> = ({ t, color, r = 150, rays = true }) => (
  <g><Halo cx={0} cy={0} r={r * 3.4} color={color} opacity={0.55} /><circle r={r} fill={color} />
    {rays && Array.from({ length: 16 }).map((_, i) => <line key={i} x1={r + 24} x2={r + 60 + 14 * Math.sin(t / 8 + i)} y1={0} y2={0} stroke={color} strokeWidth={9} strokeLinecap="round" transform={`rotate(${i * 22.5 + t * 0.3})`} />)}</g>);
export const Moon: React.FC<SP> = ({ color, color2, r = 110 }) => (<g><Halo cx={0} cy={0} r={r * 3.2} color={color} opacity={0.45} /><circle r={r} fill={color} /><circle cx={r * 0.4} cy={-r * 0.2} r={r * 0.9} fill={color2} /></g>);
export const Palace: React.FC<SP> = ({ color, color2 }) => (
  <g>
    <rect x={-380} y={-200} width={760} height={420} fill={color} />
    {[-300, -150, 0, 150, 300].map((x, i) => (<g key={x}><path d={`M${x - 60} -200 Q${x - 60} ${-300 - (i === 2 ? 90 : 0)} ${x} ${-340 - (i === 2 ? 110 : 0)} Q${x + 60} ${-300 - (i === 2 ? 90 : 0)} ${x + 60} -200 Z`} fill={color} /><line x1={x} x2={x} y1={-340 - (i === 2 ? 110 : 0)} y2={-390 - (i === 2 ? 110 : 0)} stroke={color} strokeWidth={8} /></g>))}
    {[-260, -130, 0, 130, 260].map((x) => <path key={x} d={`M${x - 34} 220 L${x - 34} 20 Q${x} -40 ${x + 34} 20 L${x + 34} 220 Z`} fill={color2} />)}
  </g>
);
export const Throne: React.FC<SP> = ({ color }) => (<g><path d="M-90 100 L-90 -160 Q0 -260 90 -160 L90 100 Z" fill={color} /><rect x={-130} y={20} width={260} height={100} rx={12} fill={color} /></g>);
export const Tree: React.FC<SP> = ({ t, color, seed = 1 }) => (
  <g><path d="M-14 200 L-8 0 L8 0 L14 200 Z" fill={color} />{Array.from({ length: 9 }).map((_, i) => { const a = -Math.PI + (i / 8) * Math.PI, sway = 3 * Math.sin(t / 20 + i + seed); return <g key={i}><line x1={0} y1={0} x2={150 * Math.cos(a)} y2={150 * Math.sin(a) + sway} stroke={color} strokeWidth={6} /><circle cx={150 * Math.cos(a)} cy={150 * Math.sin(a) + sway} r={34} fill={color} /></g>; })}<circle r={90} cy={-50} fill={color} /></g>);
export const Bolt: React.FC<SP> = ({ t, color, seed = 1, len = 900 }) => {
  const on = (Math.floor(t / 3) % 3) !== 2 || t < 6; let d = "M0 0", x = 0; for (let i = 1; i <= 9; i++) { x += (rnd(i, seed, Math.floor(t / 4)) - 0.5) * 190; d += ` L${x} ${(i * len) / 9}`; }
  return on ? <g><path d={d} fill="none" stroke={color} strokeWidth={90} opacity={0.08} /><path d={d} fill="none" stroke={color} strokeWidth={44} opacity={0.18} /><path d={d} fill="none" stroke={color} strokeWidth={22} opacity={0.4} /><path d={d} fill="none" stroke="#fff" strokeWidth={9} strokeLinejoin="bevel" /></g> : null;
};
export const Rings: React.FC<SP> = ({ t, color, count = 4, max = 900, every = 9, width = 14 }) => (
  <g>{Array.from({ length: count }).map((_, i) => { const k = prog(t, i * every, i * every + 28); return k > 0 && k < 1 ? <circle key={i} r={max * k} fill="none" stroke={color} strokeWidth={width * (1 - k)} opacity={1 - k} /> : null; })}</g>);
export const Fire: React.FC<SP> = ({ t, color, color2, w = 300, h = 380 }) => (
  <g>{Array.from({ length: 9 }).map((_, i) => { const x = (i / 8 - 0.5) * w, hh = h * (0.45 + 0.55 * Math.abs(noise(t / 4 + i * 1.7, i))) * (1 - Math.abs(i / 8 - 0.5) * 0.9);
    return <path key={i} d={`M${x - 40} 0 Q${x - 30 + 20 * noise(t / 5, i)} ${-hh * 0.6} ${x + 14 * noise(t / 3, i + 9)} ${-hh} Q${x + 34} ${-hh * 0.5} ${x + 40} 0 Z`} fill={i % 2 ? color : color2} opacity={0.9} />; })}
    <Halo cx={0} cy={-h * 0.3} r={w * 1.6} ry={h * 1.4} color={color} opacity={0.5} /></g>);
export const River: React.FC<SP> = ({ t, color, w = 1300, rows = 5 }) => (
  <g>{Array.from({ length: rows }).map((_, r) => { let d = ""; for (let i = 0; i <= 26; i++) { const x = -w / 2 + (i * w) / 26; d += `${i ? "L" : "M"}${x} ${r * 46 + 14 * Math.sin(i * 0.9 + t / 9 + r * 1.3)} `; } return <path key={r} d={d} fill="none" stroke={color} strokeWidth={7} strokeLinecap="round" opacity={0.9 - r * 0.13} />; })}</g>);
export const Arrow: React.FC<SP> = ({ color, len = 420 }) => (<g><line x1={-len / 2} x2={len / 2} y1={0} y2={0} stroke={color} strokeWidth={9} strokeLinecap="round" /><path d={`M${len / 2 + 34} 0 L${len / 2 - 14} -22 L${len / 2 - 14} 22 Z`} fill={color} /><path d={`M${-len / 2} 0 l-34 -24 M${-len / 2 + 18} 0 l-34 -24 M${-len / 2} 0 l-34 24 M${-len / 2 + 18} 0 l-34 24`} stroke={color} strokeWidth={6} /></g>);
export const Rope: React.FC<SP> = ({ t, color, len = 800 }) => (<path d={`M0 0 Q${len / 2} ${26 + 6 * Math.sin(t / 4)} ${len} 0`} fill="none" stroke={color} strokeWidth={8} strokeLinecap="round" />);
export const Birds: React.FC<SP> = ({ t, color, count = 7 }) => (<g>{Array.from({ length: count }).map((_, i) => { const x = i * 60 - (i % 2) * 20 + t * 2.2, y = (i % 3) * 44 + 10 * Math.sin(t / 10 + i), fl = 14 * Math.sin(t / 3 + i); return <path key={i} d={`M${x - 22} ${y - fl} Q${x - 10} ${y - 8} ${x} ${y} Q${x + 10} ${y - 8} ${x + 22} ${y - fl}`} fill="none" stroke={color} strokeWidth={5} strokeLinecap="round" />; })}</g>);
// Madhubani/Warli-style border band of triangles and dots.
export const Border: React.FC<SP> = ({ t, color, w = 1080, n = 18 }) => (<g>{Array.from({ length: n }).map((_, i) => { const x = -w / 2 + ((i + 0.5) * w) / n, k = prog(t, i, i + 8); return <g key={i} opacity={k} transform={`translate(${x} 0) scale(${k})`}><path d="M-22 18 L0 -22 L22 18 Z" fill="none" stroke={color} strokeWidth={5} /><circle cy={34} r={5} fill={color} /></g>; })}<line x1={-w / 2} x2={w / 2} y1={50} y2={50} stroke={color} strokeWidth={5} /><line x1={-w / 2} x2={w / 2} y1={-34} y2={-34} stroke={color} strokeWidth={5} /></g>);

// Temple bell: swings on its hook; `strikeAt` (frames) gives one hard swing. Dark body with a warm rim.
export const Bell: React.FC<SP> = ({ t, color, color2, swing = 10, speed = 7, strikeAt }) => {
  let a = swing * Math.sin(t / speed);
  if (strikeAt !== undefined && t >= strikeAt) a += 24 * Math.exp(-(t - strikeAt) / 18) * Math.cos((t - strikeAt) / 3.2);
  return (
    <g>
      <line x1={0} y1={-420} x2={0} y2={-250} stroke={color} strokeWidth={10} />
      <g transform={`rotate(${a} 0 -250)`}>
        <Halo cx={0} cy={0} r={420} color={color2} opacity={0.35} />
        <path d="M-40 -250 Q-40 -210 -70 -190 Q-150 -120 -170 60 L-210 150 L210 150 L170 60 Q150 -120 70 -190 Q40 -210 40 -250 Z" fill={color} stroke={color2} strokeWidth={6} />
        <path d="M-196 120 L196 120" stroke={color2} strokeWidth={7} opacity={0.8} /><path d="M-150 20 L150 20" stroke={color2} strokeWidth={4} opacity={0.5} />
        <g transform={`rotate(${-a * 1.6} 0 100)`}><line x1={0} y1={100} x2={0} y2={190} stroke={color2} strokeWidth={8} /><circle cx={0} cy={200} r={26} fill={color2} /></g>
      </g>
    </g>
  );
};
// Seven points of light up a vertical line, lighting one by one (every `every` frames).
export const Chakras: React.FC<SP> = ({ t, every = 12, gap = 120, r = 30 }) => {
  const cols = ["#ff3b30", "#ff8a1f", "#ffd60a", "#34c759", "#32ade6", "#5856d6", "#c77dff"];
  return <g>{cols.map((c, i) => { const k = prog(t, i * every, i * every + 8); return k > 0 ? <g key={i} opacity={k}><Halo cx={0} cy={-i * gap} r={r * 4.5 * (0.7 + 0.3 * k)} color={c} opacity={0.8} /><circle cx={0} cy={-i * gap} r={r * k} fill={c} /><circle cx={0} cy={-i * gap} r={r * 0.4 * k} fill="#fff" /></g> : null; })}</g>;
};
export const Cross: React.FC<SP> = ({ t, color, size = 200, width = 44 }) => { const k = prog(t, 0, 7); const k2 = prog(t, 4, 11); return (
  <g strokeLinecap="round" stroke={color} strokeWidth={width}><line x1={-size} y1={-size} x2={-size + 2 * size * k} y2={-size + 2 * size * k} />{k2 > 0 && <line x1={size} y1={-size} x2={size - 2 * size * k2} y2={-size + 2 * size * k2} />}</g>); };
export const Coins: React.FC<SP> = ({ t, color, count = 14, spread = 500, fall = 700 }) => (
  <g>{Array.from({ length: count }).map((_, i) => { const st = i * 2.2, k = prog(t, st, st + 26, (x) => x * x); return k > 0 ? <g key={i} transform={`translate(${(rnd(i, 3) - 0.5) * spread} ${-fall + fall * k})`}><ellipse rx={36} ry={36 * Math.abs(Math.cos(t / 5 + i))} fill={color} stroke="#7a4b00" strokeWidth={5} /></g> : null; })}</g>);
// Compass pointer: a glowing needle that swings to `angle` degrees (0 = up, 90 = right).
export const Needle: React.FC<SP> = ({ t, color, color2, angle = 0, from = 0, len = 330 }) => { const a = from + (angle - from) * prog(t, 0, 16) + 3 * Math.sin(t / 4) * (1 - prog(t, 16, 40)); return (
  <g transform={`rotate(${a})`}><path d={`M0 ${-len} L26 0 L0 40 L-26 0 Z`} fill={color2} /><Halo cx={0} cy={-len} r={90} color={color2} opacity={0.8} /><circle r={16} fill={color} /></g>); };

export const SHAPES: Record<string, React.FC<SP>> = { figure: Figure, crowd: Crowd, bow: Bow, chest: Chest, hills: Hills, mountain: Mountain, sun: Sun, moon: Moon, palace: Palace, throne: Throne, tree: Tree, bolt: Bolt, rings: Rings, fire: Fire, river: River, arrow: Arrow, rope: Rope, birds: Birds, border: Border, bell: Bell, chakras: Chakras, cross: Cross, coins: Coins, needle: Needle };
