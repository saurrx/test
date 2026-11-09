import React from "react";
import { noise, prog, rnd } from "./util";
import { BRASS, COPPER, Halo, STONE, useShade } from "./Glow";

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
      {prop === "axe" && <g><line x1={62} y1={-120} x2={62} y2={90} stroke={color} strokeWidth={7} strokeLinecap="round" /><path d="M62 -116 Q106 -112 108 -84 Q106 -56 62 -52 Q78 -84 62 -116 Z" fill={color} /></g>}
    </g>
  );
};

export const Crowd: React.FC<SP> = ({ t, color, color2, count = 24, cols = 8, gap = 78, rowGap = 110, pose = "stand", anim = "idle", stagger = 1, crown, prop }) => (
  <g>
    {Array.from({ length: count }).map((_, i) => {
      const c = i % cols, r = Math.floor(i / cols), show = prog(t, i * stagger, i * stagger + 6);
      return show <= 0 ? null : (
        <g key={i} opacity={show} transform={`translate(${(c - (cols - 1) / 2) * gap + (r % 2 ? gap / 2 : 0)} ${r * rowGap}) scale(${0.55 + 0.45 * show})`}>
          <Figure t={t + i * 3} color={color} color2={color2} pose={pose} anim={anim} seed={i} crown={crown} prop={prop} />
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
  const [bd, bf] = useShade(BRASS);
  return (
    <g>{bd}
      <line x1={0} y1={-420} x2={0} y2={-250} stroke={color} strokeWidth={10} />
      <g transform={`rotate(${a} 0 -250)`}>
        <Halo cx={0} cy={0} r={420} color={color2} opacity={0.35} />
        <path d="M-40 -250 Q-40 -210 -70 -190 Q-150 -120 -170 60 L-210 150 L210 150 L170 60 Q150 -120 70 -190 Q40 -210 40 -250 Z" fill={bf} stroke="#3a2408" strokeWidth={4} />
        <path d="M-210 150 L210 150 L196 120 L-196 120 Z" fill="#000" opacity={0.25} />
        <ellipse cx={0} cy={150} rx={210} ry={22} fill="#1a0f05" /><ellipse cx={0} cy={146} rx={196} ry={15} fill="#4a310c" />
        <path d="M-196 120 L196 120" stroke={color2} strokeWidth={7} opacity={0.8} /><path d="M-150 20 L150 20" stroke={color2} strokeWidth={4} opacity={0.5} />
        <g transform={`rotate(${-a * 1.6} 0 100)`}><line x1={0} y1={120} x2={0} y2={196} stroke="#c08a2a" strokeWidth={8} /><circle cx={0} cy={206} r={26} fill="#e9c46a" /><circle cx={-8} cy={198} r={8} fill="#fff6d8" opacity={0.8} /></g>
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

// Devotee silhouette for the glow lane: no face; hair bun, shawl, joined hands and a warm rim light make it read as a person.
export const Person: React.FC<SP> = ({ t, color, color2, pose = "pray", rim = true }) => {
  const br = 1 + 0.012 * Math.sin(t / 14); const sw = pose === "ring" ? 7 * Math.sin(t / 3.2) : 0; const st = { stroke: rim ? color2 : "none", strokeOpacity: 0.75, strokeWidth: 4, strokeLinejoin: "round" as const };
  return (
    <g transform={`scale(${br})`}>
      {rim && <Halo cx={0} cy={-60} r={250} ry={400} color={color2} opacity={0.3} />}
      {/* dhoti + torso */}
      <path d="M-150 420 Q-128 250 -92 150 Q-128 60 -124 -40 Q-120 -96 -52 -108 L52 -108 Q120 -96 124 -40 Q128 60 92 150 Q128 250 150 420 Z" fill={color} {...st} />
      {/* shawl across the chest */}
      <path d="M-118 -70 Q-20 40 96 140 L70 176 Q-40 90 -124 -10 Z" fill={color2} opacity={0.3} />
      <path d="M-112 250 Q0 290 112 250" fill="none" stroke={color2} strokeOpacity={0.35} strokeWidth={4} />
      {/* neck, head, bun */}
      <rect x={-22} y={-130} width={44} height={36} fill={color} />
      <circle cx={0} cy={-178} r={58} fill={color} {...st} /><circle cx={0} cy={-246} r={22} fill={color} {...st} />
      <path d="M-34 -100 Q0 -60 34 -100" fill="none" stroke={color2} strokeOpacity={0.8} strokeWidth={5} strokeDasharray="2 9" strokeLinecap="round" />
      {pose === "pray" && <g><path d="M-116 -30 Q-80 60 -8 10 L-8 -44 Q-60 -10 -96 -70 Z" fill={color} {...st} /><path d="M116 -30 Q80 60 8 10 L8 -44 Q60 -10 96 -70 Z" fill={color} {...st} />
        <path d="M0 -62 Q16 -30 10 14 L-10 14 Q-16 -30 0 -62 Z" fill={color2} opacity={0.9} /></g>}
      {pose === "ring" && <g><path d={`M84 -86 Q150 -200 ${118 + sw} -372 L${150 + sw} -368 Q196 -190 122 -30 Z`} fill={color} {...st} /><circle cx={134 + sw} cy={-380} r={20} fill={color} {...st} />
        <path d="M-120 -40 Q-150 70 -110 170 L-84 160 Q-110 70 -92 -50 Z" fill={color} {...st} /></g>}
      {pose === "stand" && <g><path d="M-120 -40 Q-150 70 -110 170 L-84 160 Q-110 70 -92 -50 Z" fill={color} {...st} /><path d="M120 -40 Q150 70 110 170 L84 160 Q110 70 92 -50 Z" fill={color} {...st} /></g>}
    </g>
  );
};

// A sound wave that rings out: amplitude decays over `fade` frames. Shows "the sound till it is gone".
export const Wave: React.FC<SP> = ({ t, color, w = 900, amp = 150, fade = 200, cycles = 9 }) => {
  const k = Math.max(0, 1 - t / fade); let d = "";
  for (let i = 0; i <= 120; i++) { const u = i / 120, x = (u - 0.5) * w, env = Math.sin(Math.PI * u) * k; d += `${i ? "L" : "M"}${x.toFixed(1)} ${(amp * env * Math.sin(u * cycles * Math.PI * 2 - t / 2.2)).toFixed(1)} `; }
  return <g fill="none" strokeLinecap="round"><path d={d} stroke={color} strokeWidth={34} opacity={0.08} /><path d={d} stroke={color} strokeWidth={16} opacity={0.2} /><path d={d} stroke="#fff6d8" strokeWidth={6} /></g>;
};

// Temple seen from outside: stepped shikhara with kalash and flag, side shrines, steps, a glowing doorway. Pure silhouette.
export const Mandir: React.FC<SP> = ({ t, color, color2, door = true, flag = true }) => {
  const tiers = 9; const parts: React.ReactNode[] = [];
  for (let i = 0; i < tiers; i++) { const w = 330 - i * 30, y = -200 - i * 62; parts.push(<path key={i} d={`M${-w / 2} ${y} L${-w / 2 + 14} ${y - 62} L${w / 2 - 14} ${y - 62} L${w / 2} ${y} Z`} fill={color} />); parts.push(<rect key={`b${i}`} x={-w / 2 - 8} y={y - 6} width={w + 16} height={10} fill={color} />); }
  const top = -200 - tiers * 62; const wave = 10 * Math.sin(t / 6);
  return (
    <g>
      {door && <Halo cx={0} cy={60} r={420} ry={520} color={color2} opacity={0.5} />}
      {[-330, 330].map((x) => <g key={x}><rect x={x - 90} y={-60} width={180} height={300} fill={color} /><path d={`M${x - 100} -60 L${x - 60} -220 L${x} -300 L${x + 60} -220 L${x + 100} -60 Z`} fill={color} /><circle cx={x} cy={-316} r={14} fill={color} /></g>)}
      <rect x={-200} y={-200} width={400} height={440} fill={color} />
      {parts}
      <path d={`M-40 ${top} Q0 ${top - 70} 40 ${top} Z`} fill={color} /><circle cx={0} cy={top - 52} r={18} fill={color2} /><line x1={0} y1={top - 60} x2={0} y2={top - 190} stroke={color} strokeWidth={6} />
      {flag && <path d={`M0 ${top - 190} L${110} ${top - 165 + wave} L0 ${top - 130} Z`} fill="#e8641c" />}
      {door && <path d="M-80 240 L-80 40 Q0 -70 80 40 L80 240 Z" fill={color2} />}
      {door && <path d="M-80 240 L-80 40 Q0 -70 80 40 L80 240 Z" fill="#fff6d8" opacity={0.55} transform="translate(0 60) scale(0.7) translate(0 26)" />}
      {[0, 1, 2, 3].map((i) => <rect key={i} x={-300 - i * 60} y={240 + i * 34} width={600 + i * 120} height={34} fill={color} opacity={1 - i * 0.04} />)}
    </g>
  );
};
// Looking through a dark doorway into the lit sanctum: jambs, lintel, threshold. Everything beyond is glow.
export const Doorway: React.FC<SP> = ({ t, color, color2, open = 1 }) => {
  const k = Math.min(1, open) * prog(t, 0, 24); const half = 300 * k;
  return (
    <g>
      <Halo cx={0} cy={-80} r={900} ry={1300} color={color2} opacity={0.85 * k} />
      <path d={`M${-half} 620 L${-half} -520 Q0 ${-520 - 330 * k} ${half} -520 L${half} 620 Z`} fill={color2} opacity={0.9 * k} />
      <path d={`M${-half * 0.6} 620 L${-half * 0.6} -400 Q0 ${-400 - 240 * k} ${half * 0.6} -400 L${half * 0.6} 620 Z`} fill="#fff6d8" opacity={0.6 * k} />
      {/* the wall around the opening */}
      <path d={`M-700 -1200 L700 -1200 L700 900 L-700 900 Z M${-half} 620 L${-half} -520 Q0 ${-520 - 330 * k} ${half} -520 L${half} 620 Z`} fill={color} fillRule="evenodd" />
      <path d={`M${-half} 620 L${-half} -520 Q0 ${-520 - 330 * k} ${half} -520 L${half} 620`} fill="none" stroke={color2} strokeOpacity={0.8} strokeWidth={10} />
      <rect x={-700} y={620} width={1400} height={60} fill="#2a1a10" /><rect x={-700} y={620} width={1400} height={8} fill={color2} opacity={0.6} />
    </g>
  );
};
// Two bare feet seen from behind/above; `step` 0..1 moves the right foot forward over a threshold.
export const Feet: React.FC<SP> = ({ t, color, color2, stepAt = 20 }) => {
  const k = prog(t, stepAt, stepAt + 16); const foot = (x: number, y: number, flip: number) => (
    <g transform={`translate(${x} ${y}) scale(${flip} 1)`}><path d="M-46 120 Q-70 20 -50 -70 Q-30 -150 20 -150 Q66 -150 60 -60 Q54 30 50 120 Q0 170 -46 120 Z" fill={color} stroke={color2} strokeOpacity={0.8} strokeWidth={5} />
      {[0, 1, 2, 3, 4].map((i) => <circle key={i} cx={-44 + i * 24} cy={-166 + Math.abs(i - 1.5) * 9} r={i === 0 ? 17 : 12} fill={color} stroke={color2} strokeOpacity={0.8} strokeWidth={4} />)}</g>);
  return <g>{foot(-110, 0, -1)}{foot(110, -330 * k - 40 * Math.sin(Math.PI * k), 1)}</g>;
};
// A hand and forearm reaching up (side view), rim-lit. Fingers are a simple curled shape: enough to read as a hand.
export const Hand: React.FC<SP> = ({ t, color, color2, pull = 0 }) => {
  const dy = pull ? 26 * Math.sin(t / 3.2) : 0;
  return (
    <g transform={`translate(0 ${dy})`}>
      <path d="M-70 520 L-52 80 Q-60 -10 -40 -60 L-34 -150 Q-30 -180 -8 -178 Q10 -176 10 -150 L12 -196 Q14 -224 36 -222 Q56 -220 54 -192 L54 -168 Q60 -194 80 -190 Q98 -186 94 -158 L88 -100 Q110 -120 124 -104 Q134 -90 116 -64 L84 -6 Q70 40 66 80 L84 520 Z" fill={color} stroke={color2} strokeOpacity={0.8} strokeWidth={5} strokeLinejoin="round" />
      <path d="M-46 110 Q10 140 70 110" fill="none" stroke={color2} strokeOpacity={0.9} strokeWidth={7} strokeDasharray="3 12" strokeLinecap="round" />
    </g>
  );
};
// Brass aarti plate from above with a ring of small flames.
export const Thali: React.FC<SP> = ({ t, color2, wicks = 5, r = 240 }) => (
  <g>
    <Halo cx={0} cy={0} r={r * 2.4} color={color2} opacity={0.5} />
    <circle r={r} fill="#8a5a1c" stroke="#d9a441" strokeWidth={10} /><circle r={r * 0.8} fill="none" stroke="#d9a441" strokeWidth={4} opacity={0.7} /><circle r={r * 0.2} fill="#c4521a" />
    {Array.from({ length: wicks }).map((_, i) => { const a = (i / wicks) * Math.PI * 2 - Math.PI / 2, x = r * 0.56 * Math.cos(a), y = r * 0.56 * Math.sin(a), k = 1 + 0.2 * noise(t / 2.5, i);
      return <g key={i}><Halo cx={x} cy={y} r={70 * k} color={color2} opacity={0.9} /><circle cx={x} cy={y} r={20 * k} fill={color2} /><circle cx={x} cy={y} r={9} fill="#fff8e0" /></g>; })}
  </g>
);

// Shivling on its base (yoni-pitha) with the water spout to one side. `wet` 0..1 adds a sheen and a trickle off the spout.
export const Lingam: React.FC<SP> = ({ t, color, color2, wet = 0, spout = -1 }) => {
  const k = Math.min(1, wet) * prog(t, 0, 20); const [sd, sf] = useShade(STONE);
  return (
    <g>{sd}
      <Halo cx={0} cy={-120} r={420} ry={520} color={color2} opacity={0.4} />
      <path d={`M${spout * 150} 150 L${spout * 420} 150 Q${spout * 470} 170 ${spout * 420} 196 L${spout * 150} 210 Z`} fill={color} stroke={color2} strokeOpacity={0.6} strokeWidth={5} />
      <ellipse cx={0} cy={196} rx={300} ry={74} fill="#050302" /><ellipse cx={0} cy={180} rx={290} ry={70} fill={sf} stroke={color2} strokeOpacity={0.5} strokeWidth={4} /><ellipse cx={0} cy={172} rx={236} ry={50} fill="#0b0705" opacity={0.7} />
      <path d="M-120 170 L-120 -170 Q-120 -310 0 -310 Q120 -310 120 -170 L120 170 Q0 215 -120 170 Z" fill={sf} stroke={color2} strokeOpacity={0.45} strokeWidth={3} />
      <path d="M-74 120 L-74 -170 Q-72 -262 -30 -284 Q-52 -236 -52 -160 L-52 130 Z" fill="#fff1d6" opacity={0.16 + 0.3 * k} />
      {[0, 1, 2].map((i) => <path key={i} d={`M-66 ${-150 + i * 30} Q0 ${-136 + i * 30} 66 ${-150 + i * 30}`} fill="none" stroke="#efe6d2" strokeWidth={11} strokeLinecap="round" opacity={0.85} />)}
      <circle cx={0} cy={-120} r={13} fill="#c4281a" />
      <path d="M40 150 L40 -180 Q40 -262 84 -200 L96 150 Z" fill="#000" opacity={0.28} />
      <path d="M-118 -40 Q0 60 118 -40" fill="none" stroke="#f08a1c" strokeWidth={20} strokeDasharray="3 24" strokeLinecap="round" /><path d="M-118 -40 Q0 60 118 -40" fill="none" stroke="#ffd24a" strokeWidth={9} strokeDasharray="3 24" strokeLinecap="round" />
      {[-210, -150, 150, 210].map((x, i) => <g key={x}><circle cx={x} cy={168 + (i % 2) * 14} r={17} fill="#f08a1c" /><circle cx={x} cy={168 + (i % 2) * 14} r={8} fill="#ffd24a" /></g>)}
      {k > 0 && [0, 1, 2].map((i) => { const u = ((t / 26 + i / 3) % 1); return <ellipse key={`r${i}`} cx={0} cy={176} rx={130 + 150 * u} ry={26 + 40 * u} fill="none" stroke="#9fe3ff" strokeWidth={5 * (1 - u)} opacity={(1 - u) * 0.8 * k} />; })}
      {k > 0 && <g opacity={k}><path d={`M${spout * 440} 176 q${spout * 30} 60 ${spout * 14} ${240 + 12 * Math.sin(t / 3)}`} fill="none" stroke="#9fe3ff" strokeWidth={9} strokeLinecap="round" />
        {[0, 1, 2].map((i) => <circle key={i} cx={spout * 452} cy={430 + ((t * 9 + i * 60) % 200)} r={7} fill="#9fe3ff" opacity={0.8} />)}</g>}
    </g>
  );
};
// Copper pot (lota) that tilts and pours one stream down to `drop` px below. `broken` makes the stream stutter (the wrong way).
export const Lota: React.FC<SP> = ({ t, color = "#b8652a", color2, tilt = 55, drop = 620, pourAt = 12, broken = 0, thick = 12 }) => {
  const a = tilt * prog(t, 0, 14); const p = prog(t, pourAt, pourAt + 12); const lip: [number, number] = [-118, -38];
  const gaps = broken ? `${40 + 30 * Math.abs(noise(t / 3, 5))} ${50 + 40 * Math.abs(noise(t / 2, 9))}` : undefined;
  const [cd, cf] = useShade(COPPER); const body = color === "#b8652a" ? cf : color;
  return (
    <g>{cd}
      <g transform={`rotate(${-a})`}>
        <Halo cx={0} cy={0} r={230} color={color2} opacity={0.45} />
        <path d="M-96 -40 Q-150 40 -100 110 Q0 170 100 110 Q150 40 96 -40 Q60 -70 70 -100 L-70 -100 Q-60 -70 -96 -40 Z" fill={body} stroke="#3a1806" strokeWidth={4} />
        <ellipse cx={0} cy={-100} rx={78} ry={16} fill="#5a2a0c" stroke="#ffd9a0" strokeOpacity={0.8} strokeWidth={4} />
        <path d="M-70 10 Q0 40 70 10" fill="none" stroke="#ffd9a0" strokeWidth={5} opacity={0.6} /><path d="M-80 -20 Q-110 40 -78 96" fill="none" stroke="#fff1d6" strokeWidth={9} opacity={0.5} strokeLinecap="round" />
      </g>
      {p > 0 && (() => { const r = (-a * Math.PI) / 180, x0 = lip[0] * Math.cos(r) - (lip[1] - 62) * Math.sin(r), y0 = lip[0] * Math.sin(r) + (lip[1] - 62) * Math.cos(r); const d = `M${x0} ${y0} Q${x0 - 26} ${y0 + drop * 0.3} ${x0 - 30 + 4 * Math.sin(t / 4)} ${y0 + drop * p}`;
        return <g fill="none" strokeLinecap="round"><path d={d} stroke="#9fe3ff" strokeWidth={thick * 3} opacity={0.14} /><path d={d} stroke="#9fe3ff" strokeWidth={thick} strokeDasharray={gaps} /><path d={d} stroke="#fff" strokeWidth={thick * 0.35} strokeDasharray={gaps} /></g>; })()}
    </g>
  );
};
// Bilva leaf: three leaflets on one stalk.
export const Belpatra: React.FC<SP> = ({ t, color = "#4c9a3f" }) => { const sw = 3 * Math.sin(t / 12); const leaf = (rot: number) => <path d="M0 0 Q-46 -70 0 -150 Q46 -70 0 0 Z" fill={color} stroke="#1d4d1f" strokeWidth={4} transform={`rotate(${rot + sw})`} />; return <g>{leaf(-48)}{leaf(48)}{leaf(0)}<line x1={0} y1={0} x2={0} y2={70} stroke="#1d4d1f" strokeWidth={7} strokeLinecap="round" /></g>; };
export const Trishul: React.FC<SP> = ({ color, color2 }) => (<g><Halo cx={0} cy={-200} r={300} ry={420} color={color2} opacity={0.4} /><line x1={0} y1={-260} x2={0} y2={460} stroke={color} strokeWidth={18} strokeLinecap="round" />
  <path d="M0 -430 L26 -280 L-26 -280 Z" fill={color} /><path d="M-120 -400 Q-150 -250 -30 -230 L-30 -200 Q-190 -220 -150 -400 Z" fill={color} /><path d="M120 -400 Q150 -250 30 -230 L30 -200 Q190 -220 150 -400 Z" fill={color} />
  <path d="M-70 -150 L0 -110 L70 -150 L70 -110 L0 -70 L-70 -110 Z" fill={color2} /></g>);
// Path for walking half-way round and turning back (pradakshina that stops at the spout). progress 0..1.
export const HalfCircle: React.FC<SP> = ({ t, color, r = 360, dur = 70, back = true, squash = 0.42, turns = 0.75 }) => {
  const k = prog(t, 0, dur, (x) => x); const out = Math.min(1, k * 2), ret = Math.max(0, k * 2 - 1); const a0 = Math.PI / 2, sweep = Math.PI * 2 * turns;
  const pt = (u: number) => [r * Math.cos(a0 + sweep * u), r * squash * Math.sin(a0 + sweep * u)]; const u = back ? out - ret : out; let d = "";
  for (let i = 0; i <= 60; i++) { const p = pt((out * i) / 60); d += `${i ? "L" : "M"}${p[0].toFixed(1)} ${p[1].toFixed(1)} `; } const h = pt(u);
  return <g fill="none" strokeLinecap="round"><path d={d} stroke={color} strokeWidth={30} opacity={0.12} /><path d={d} stroke={color} strokeWidth={10} strokeDasharray="6 26" /><circle cx={h[0]} cy={h[1]} r={26} fill="#fff6d8" /><Halo cx={h[0]} cy={h[1]} r={110} color={color} opacity={0.9} /></g>;
};

// Shivling seen from above: round base, the lingam, and the water channel pointing up (north).
export const LingamTop: React.FC<SP> = ({ t, color, color2 }) => (
  <g>
    <Halo cx={0} cy={0} r={420} color={color2} opacity={0.45} />
    <path d="M-46 -150 L-46 -330 Q0 -372 46 -330 L46 -150 Z" fill={color} stroke={color2} strokeOpacity={0.8} strokeWidth={6} />
    <path d={`M0 -160 L0 ${-330 + 6 * Math.sin(t / 5)}`} stroke="#9fe3ff" strokeWidth={14} strokeLinecap="round" opacity={0.9} />
    <circle r={190} fill={color} stroke={color2} strokeOpacity={0.8} strokeWidth={6} /><circle r={150} fill="none" stroke={color2} strokeOpacity={0.35} strokeWidth={4} />
    <circle r={84} fill="#241710" stroke={color2} strokeWidth={6} /><circle r={30} fill={color2} opacity={0.5} />
    {[0, 1, 2].map((i) => <line key={i} x1={-40} x2={40} y1={-16 + i * 16} y2={-16 + i * 16} stroke="#efe6d2" strokeWidth={7} strokeLinecap="round" />)}
  </g>
);

// Offerings for the "never offer" reel. All drawn around (0,0).
export const Flower: React.FC<SP> = ({ t, color = "#f4ead0", color2 }) => (<g transform={`rotate(${3 * Math.sin(t / 14)})`}><Halo cx={0} cy={-40} r={260} color={color2} opacity={0.35} />
  <path d="M0 200 Q-10 80 0 0" fill="none" stroke="#3f8f3a" strokeWidth={12} strokeLinecap="round" /><path d="M-4 120 Q-70 90 -90 30 Q-30 50 -4 120 Z" fill="#3f8f3a" />
  {[-56, -28, 0, 28, 56].map((a) => <path key={a} d="M0 0 Q-34 -110 0 -230 Q34 -110 0 0 Z" fill={color} stroke="#b9a66a" strokeWidth={4} transform={`rotate(${a})`} />)}<circle r={16} fill="#e9c46a" /></g>);
export const Tulsi: React.FC<SP> = ({ t, color = "#4c9a3f" }) => (<g><line x1={0} y1={220} x2={0} y2={-200} stroke="#2e5d2a" strokeWidth={9} strokeLinecap="round" />
  {[0, 1, 2, 3, 4].map((i) => { const y = 150 - i * 80, s = 1 - i * 0.12, sw = 3 * Math.sin(t / 10 + i); return <g key={i}><path d={`M0 ${y} Q${-90 * s} ${y - 60 + sw} ${-120 * s} ${y - 10} Q${-70 * s} ${y + 30} 0 ${y} Z`} fill={color} stroke="#1d4d1f" strokeWidth={3} /><path d={`M0 ${y} Q${90 * s} ${y - 60 - sw} ${120 * s} ${y - 10} Q${70 * s} ${y + 30} 0 ${y} Z`} fill={color} stroke="#1d4d1f" strokeWidth={3} /></g>; })}
  <path d="M0 -200 Q-26 -250 0 -290 Q26 -250 0 -200 Z" fill="#7a4a8a" /></g>);
export const Bowls: React.FC<SP> = () => { const bowl = (x: number, c: string, c2: string) => (<g transform={`translate(${x} 0)`}><path d={`M-90 0 Q0 -150 90 0 Z`} fill={c} /><path d="M-70 -20 Q-20 -110 10 -60" fill="none" stroke={c2} strokeWidth={10} opacity={0.6} strokeLinecap="round" />
    <path d="M-120 0 L120 0 Q110 90 0 100 Q-110 90 -120 0 Z" fill="#8a5a1c" stroke="#d9a441" strokeWidth={6} /><ellipse cx={0} cy={0} rx={120} ry={20} fill="#5a3a10" opacity={0.5} /></g>); return <g>{bowl(-150, "#f2b90c", "#ffe27a")}{bowl(150, "#c4281a", "#ff7a66")}</g>; };
export const Conch: React.FC<SP> = ({ t, color = "#f1e9da", color2 }) => (<g transform={`rotate(${-18 + 2 * Math.sin(t / 12)})`}><Halo cx={0} cy={0} r={300} color={color2} opacity={0.3} />
  <path d="M-220 20 Q-150 -150 40 -150 Q230 -140 250 20 Q230 150 60 150 Q-80 150 -150 90 Q-190 70 -300 110 Q-250 60 -220 20 Z" fill={color} stroke="#b9a98a" strokeWidth={6} />
  <path d="M40 -150 Q120 -60 60 150" fill="none" stroke="#b9a98a" strokeWidth={5} /><path d="M120 -130 Q190 -40 150 130" fill="none" stroke="#b9a98a" strokeWidth={5} /><path d="M-40 -130 Q20 -30 -30 140" fill="none" stroke="#b9a98a" strokeWidth={5} />
  <path d="M250 20 Q300 -10 330 30 Q300 60 250 20 Z" fill={color} stroke="#b9a98a" strokeWidth={5} /><ellipse cx={-110} cy={30} rx={70} ry={40} fill="#e7b9a8" opacity={0.7} /></g>);
export const Rice: React.FC<SP> = ({ t, color = "#f6f1e2", broken = 0, count = 13 }) => (<g>{Array.from({ length: count }).map((_, i) => { const a = (i / count) * Math.PI * 2, r = 60 + 110 * rnd(i, 3), x = r * Math.cos(a), y = r * 0.7 * Math.sin(a), rot = 360 * rnd(i, 7);
  const isB = broken && i % 3 === 0; return <g key={i} transform={`translate(${x} ${y}) rotate(${rot})`}>{isB ? <g><ellipse cx={-17} rx={15} ry={12} fill={color} stroke="#ff3b30" strokeWidth={4} /><ellipse cx={21} cy={6} rx={12} ry={11} fill={color} stroke="#ff3b30" strokeWidth={4} /></g> : <ellipse rx={38} ry={13} fill={color} stroke="#cfc6ad" strokeWidth={3} />}</g>; })}</g>);

export const SHAPES: Record<string, React.FC<SP>> = { figure: Figure, crowd: Crowd, bow: Bow, chest: Chest, hills: Hills, mountain: Mountain, sun: Sun, moon: Moon, palace: Palace, throne: Throne, tree: Tree, bolt: Bolt, rings: Rings, fire: Fire, river: River, arrow: Arrow, rope: Rope, birds: Birds, border: Border, bell: Bell, chakras: Chakras, cross: Cross, coins: Coins, needle: Needle, person: Person, wave: Wave, mandir: Mandir, doorway: Doorway, feet: Feet, hand: Hand, thali: Thali, lingam: Lingam, lota: Lota, belpatra: Belpatra, trishul: Trishul, halfcircle: HalfCircle, lingamtop: LingamTop, flower: Flower, tulsi: Tulsi, bowls: Bowls, conch: Conch, rice: Rice };
