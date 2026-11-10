import React from "react";
import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Dust, Film, Gradient, Stars } from "./lib/Backdrop";
import { SHAPES } from "./lib/Flat";
import { Diya, Flame, GlowDefs, GlowTrail, Halo, Rays, Yantra } from "./lib/Glow";
import { Temple } from "./lib/Temple";
import { BigText, Captions, Word } from "./lib/Text";
import { fontFor } from "./lib/fonts";
import { clamp, ease, easeIO, noise, Palette, PALETTES, prog } from "./lib/util";

export type Layer = { kind: string; at?: number; until?: number; x?: number; y?: number; s?: number; rot?: number; opacity?: number; color?: string; color2?: string;
  enter?: "fade" | "pop" | "rise" | "drop" | "slide_l" | "slide_r" | "none"; exit?: "fade" | "none"; move?: { x?: number; y?: number; s?: number; rot?: number; over?: number }; [k: string]: any };
export type Scene = { dur: number; palette?: string; bg?: { kind?: "radial" | "linear" | "horizon" | "temple" | "solid"; idol?: any; lamps?: number; cy?: number; glow?: number };
  cam?: { z0?: number; z1?: number; x0?: number; x1?: number; y0?: number; y1?: number; shakeAt?: number; shake?: number }; layers?: Layer[];
  dust?: boolean | number; stars?: boolean; trans?: "cut" | "fade" | "flash" | "punch" };
export type ReelProps = { palette?: string; scenes: Scene[]; captions?: { words: Word[]; style?: "serif" | "pop"; y?: number; max?: number; size?: number };
  audio?: { vo?: string; voAt?: number; music?: string; musicVol?: number; voVol?: number; sfx?: { src: string; at: number; vol?: number }[] }; film?: { grain?: number; vignette?: number }; duration?: number; header?: { text: string; color?: string }; fixedText?: boolean };

const TEXT_KINDS = new Set(["text"]);

const LayerView: React.FC<{ l: Layer; p: Palette; sceneFrames: number; svg: boolean }> = ({ l, p, sceneFrames, svg }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const a = Math.round((l.at ?? 0) * fps), u = l.until === undefined ? sceneFrames + 30 : Math.round(l.until * fps), t = f - a;
  if (t < 0 || f > u) return null;
  const isText = TEXT_KINDS.has(l.kind); if (isText === svg) return null;
  const kin = l.enter === "none" ? 1 : prog(t, 0, l.enter === "pop" ? 9 : 12, l.enter === "pop" ? (x) => 1 + 1.4 * Math.pow(x - 1, 3) + 0.4 * Math.pow(x - 1, 2) : ease);
  const kout = l.exit === "fade" ? 1 - prog(f, u - 8, u) : 1;
  const mo = l.move ? prog(t, 0, (l.move.over ?? (sceneFrames - a) / fps) * fps, easeIO) : 0;
  let x = (l.x ?? 540) + (l.move?.x ?? 0) * mo, y = (l.y ?? 960) + (l.move?.y ?? 0) * mo, s = (l.s ?? 1) * (1 + ((l.move?.s ?? 1) - 1) * mo), op = (l.opacity ?? 1) * kout;
  const rot = (l.rot ?? 0) + (l.move?.rot ?? 0) * mo;
  const e = l.enter ?? "fade";
  if (e === "fade") op *= kin; if (e === "pop") { s *= kin; op *= Math.min(1, t / 3); } if (e === "rise") { y += (1 - kin) * 160; op *= kin; } if (e === "drop") { y -= (1 - kin) * 400; op *= Math.min(1, t / 3); }
  if (e === "slide_l") { x -= (1 - kin) * 900; } if (e === "slide_r") { x += (1 - kin) * 900; }
  const color = l.color ?? p.fg, color2 = l.color2 ?? p.accent;
  if (isText) return <div style={{ position: "absolute", left: x, top: y, opacity: op, transform: `rotate(${rot}deg) scale(${s})` }}><BigText t={t} text={l.text} color={color} glow={l.glow} size={l.size} style={l.font} enter={l.textEnter ?? "slam"} count={l.count} width={Math.min(l.width ?? 920, 940)} sub={l.sub} panel={l.panel} /></div>;
  const tr = `translate(${x} ${y}) rotate(${rot}) scale(${s})`;
  // absolute-space glow primitives take frames relative to the scene, so shift by `a`
  if (l.kind === "trail") return <g opacity={op}><GlowTrail {...(l as any)} cx={l.x ?? 540} cy={l.y ?? 900} from={a + (l.from ?? 0) * fps} to={a + (l.to ?? 1.5) * fps} fadeOutAt={l.fadeAt === undefined ? undefined : a + l.fadeAt * fps} color={l.color ?? p.accent} /></g>;
  if (l.kind === "yantra") return <g opacity={op}><Yantra {...(l as any)} cx={l.x ?? 540} cy={l.y ?? 900} from={a} dur={(l.draw ?? 1.5) * fps} color={l.color ?? p.accent} /></g>;
  if (l.kind === "rays") return <g opacity={op}><Rays {...(l as any)} cx={l.x ?? 540} cy={l.y ?? 700} color={l.color ?? p.accent} /></g>;
  if (l.kind === "flame") return <g opacity={op}><Flame x={x} y={y} s={s} color={l.color ?? p.accent} seed={l.seed} /></g>;
  if (l.kind === "diya") return <g opacity={op}><Diya x={x} y={y} s={s} color={l.color ?? p.accent} seed={l.seed} lean={(l.lean ?? 0) * prog(t, l.leanAt ?? 0, (l.leanAt ?? 0) + 14)} /></g>;
  if (l.kind === "glowdot") return <g opacity={op}><Halo cx={x} cy={y} r={(l.r ?? 200) * s * 1.8} color={color2} /></g>;
  if (l.kind === "rect") return <rect x={x - (l.w ?? 200) / 2} y={y - (l.h ?? 200) / 2} width={l.w ?? 200} height={l.h ?? 200} rx={l.rx ?? 0} fill={color} opacity={op} />;
  const Shape = SHAPES[l.kind]; if (!Shape) return null;
  return <g transform={tr} opacity={op}><Shape {...(l as any)} t={t} color={color} color2={color2} /></g>;
};

const SceneView: React.FC<{ sc: Scene; p: Palette; frames: number; fixedText?: boolean }> = ({ sc, p, frames, fixedText }) => {
  const f = useCurrentFrame(); const c = sc.cam ?? {}; const k = prog(f, 0, frames, easeIO);
  const z = interpolate(k, [0, 1], [c.z0 ?? 1.0, c.z1 ?? 1.06]), cx = interpolate(k, [0, 1], [c.x0 ?? 0, c.x1 ?? 0]), cy = interpolate(k, [0, 1], [c.y0 ?? 0, c.y1 ?? 0]);
  let sx = 0, sy = 0; if (c.shakeAt !== undefined) { const st = f - c.shakeAt * 30; if (st >= 0 && st < 22) { const amp = (c.shake ?? 26) * (1 - st / 22); sx = amp * noise(f * 1.7, 1); sy = amp * noise(f * 1.9, 2); } }
  const tr = sc.trans ?? "cut"; const tin = tr === "fade" ? 0.4 + 0.6 * prog(f, 0, 6) : 1; const punch = tr === "punch" ? 1 + 0.18 * (1 - prog(f, 0, 7)) : 1;
  const bg = sc.bg ?? {}; const layers = sc.layers ?? [];
  return (
    <AbsoluteFill style={{ opacity: tin, background: p.bg }}>
      <AbsoluteFill style={{ transform: `translate(${-cx + sx}px, ${-cy + sy}px) scale(${z * punch})`, transformOrigin: "50% 45%" }}>
        {bg.kind !== "temple" && bg.kind !== "solid" && <Gradient p={p} kind={bg.kind ?? "radial"} cy={bg.cy} />}
        {sc.stars && <Stars color={p.fg} />}
        <svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{ position: "absolute" }}>
          <GlowDefs />
          {bg.kind === "temple" && <Temple idol={bg.idol} lamps={bg.lamps} warm={p.accent} glow={bg.glow} />}
          {layers.map((l, i) => <LayerView key={i} l={l} p={p} sceneFrames={frames} svg />)}
        </svg>
        {!fixedText && <AbsoluteFill>{layers.map((l, i) => <LayerView key={i} l={l} p={p} sceneFrames={frames} svg={false} />)}</AbsoluteFill>}
        {sc.dust && <Dust color={p.accent} count={typeof sc.dust === "number" ? sc.dust : 36} />}
      </AbsoluteFill>
      {fixedText && <AbsoluteFill style={{ transform: `translate(${sx}px, ${sy}px)` }}>{layers.map((l, i) => <LayerView key={i} l={l} p={p} sceneFrames={frames} svg={false} />)}</AbsoluteFill>}
      {tr === "flash" && <AbsoluteFill style={{ background: p.fg, opacity: 0.75 * (1 - prog(f, 0, 5)) }} />}
    </AbsoluteFill>
  );
};

export const reelFrames = (props: ReelProps, fps: number) => Math.round((props.duration ?? props.scenes.reduce((a, s) => a + s.dur, 0)) * fps);

export const Reel: React.FC<ReelProps> = (props) => {
  const { fps } = useVideoConfig(); let at = 0;
  const base = PALETTES[props.palette ?? "glow"] ?? PALETTES.glow;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {props.scenes.map((sc, i) => {
        const from = Math.round(at * fps), frames = Math.round(sc.dur * fps); at += sc.dur;
        const p = sc.palette ? PALETTES[sc.palette] ?? base : base;
        return <Sequence key={i} from={from} durationInFrames={frames}><SceneView sc={sc} p={p} frames={frames} fixedText={props.fixedText} /></Sequence>;
      })}
      <Film grain={props.film?.grain ?? 0.1} vignette={props.film?.vignette ?? 0.6} />
      {props.header && (
        <div style={{ position: "absolute", top: 96, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
          <div style={{ fontFamily: fontFor("clean", props.header.text), fontWeight: 800, fontSize: 44, letterSpacing: 5, color: props.header.color ?? base.accent, background: "rgba(0,0,0,0.55)",
            border: `2px solid ${props.header.color ?? base.accent}`, borderRadius: 40, padding: "8px 34px", textTransform: "uppercase" }}>{props.header.text}</div>
        </div>
      )}
      {props.captions && <Captions words={props.captions.words} style={props.captions.style} p={base} y={props.captions.y} max={props.captions.max} size={props.captions.size} />}
      {props.audio?.vo && <Sequence from={Math.round((props.audio.voAt ?? 0) * fps)}><Audio src={staticFile(props.audio.vo)} volume={props.audio.voVol ?? 1} /></Sequence>}
      {props.audio?.music && <Audio src={staticFile(props.audio.music)} volume={props.audio.musicVol ?? 0.22} loop />}
      {(props.audio?.sfx ?? []).map((s, i) => <Sequence key={i} from={Math.round(s.at * fps)}><Audio src={staticFile(s.src)} volume={s.vol ?? 0.7} /></Sequence>)}
    </AbsoluteFill>
  );
};
