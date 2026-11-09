import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { fontFor } from "./fonts";
import { clamp, Palette, prog } from "./util";

export type Word = { s: number; e: number; w: string; emph?: boolean };
type Chunk = { s: number; e: number; words: Word[] };

// Group timed words into short on-screen chunks: break on punctuation, long pauses, or the size limit.
export const chunkWords = (words: Word[], max: number): Chunk[] => {
  const out: Chunk[] = []; let cur: Word[] = [];
  const flush = () => { if (cur.length) { out.push({ s: cur[0].s, e: cur[cur.length - 1].e, words: cur }); cur = []; } };
  words.forEach((w, i) => {
    cur.push(w); const next = words[i + 1];
    if (/[.!?।,;:—]$/.test(w.w) || cur.length >= max || (next && next.s - w.e > 0.45)) flush();
  });
  flush();
  out.forEach((c, i) => { const n = out[i + 1]; c.e = n ? Math.min(n.s, c.e + 0.6) : c.e + 0.5; });
  return out;
};

// Captions. "serif": calm glowing small caps, words light up as spoken. "pop": big bold words that punch in, active word in accent.
export const Captions: React.FC<{ words: Word[]; style?: "serif" | "pop"; p: Palette; y?: number; max?: number; size?: number }> = ({ words, style = "serif", p, y = 1240, max, size }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const chunks = React.useMemo(() => chunkWords(words, max ?? (style === "pop" ? 3 : 5)), [words, max, style]);
  const c = chunks.find((k) => t >= k.s - 0.04 && t < k.e); if (!c) return null;
  const text = c.words.map((w) => w.w).join(" "); const pop = style === "pop";
  const fs = size ?? (pop ? (text.length > 16 ? 104 : 132) : 68);
  return (
    <>
    {/* soft dark pool behind the words so they read on any picture */}
    <div style={{ position: "absolute", left: -100, right: -100, top: y - 260, height: 520, background: `radial-gradient(ellipse 55% 50% at 50% 50%, rgba(0,0,0,${pop ? 0.62 : 0.78}) 0%, rgba(0,0,0,0) 100%)` }} />
    <div style={{ position: "absolute", left: 70, right: 70, top: y, transform: "translateY(-50%)", textAlign: "center", fontFamily: fontFor(style, text),
      fontSize: fs, lineHeight: pop ? 1.12 : 1.3, fontWeight: 800, letterSpacing: pop ? 1 : 3, textTransform: "uppercase", color: p.fg }}>
      {c.words.map((w, i) => {
        const said = t >= w.s - 0.03, active = t >= w.s - 0.03 && t < w.e + 0.08, k = spring({ frame: f - Math.round((w.s - 0.03) * fps), fps, config: { damping: 13, stiffness: 220, mass: 0.6 } });
        const col = w.emph || (pop && active) ? p.accent : p.fg;
        return (
          <span key={i} style={{ display: "inline-block", margin: pop ? "0 14px" : "0 10px", color: col,
            opacity: said ? 1 : 0, transform: pop ? `scale(${said ? 0.6 + 0.4 * k : 0.6}) rotate(${said ? (1 - k) * (i % 2 ? 4 : -4) : 0}deg)` : `translateY(${said ? (1 - k) * 10 : 10}px)`,
            textShadow: pop ? `0 6px 0 rgba(0,0,0,.55), 0 0 28px rgba(0,0,0,.8)${w.emph || active ? `, 0 0 34px ${p.accent}` : ""}` : `0 0 22px rgba(0,0,0,.95), 0 2px 6px rgba(0,0,0,.9)${w.emph ? `, 0 0 26px ${p.accent}` : ""}`,
            WebkitTextStroke: pop ? "2px rgba(0,0,0,.35)" : undefined }}>{w.w}</span>
        );
      })}
    </div>
    </>
  );
};

// Big on-screen text / numbers used inside scenes.
export const BigText: React.FC<{ t: number; text: string; color: string; glow?: string; size?: number; style?: "serif" | "pop" | "clean"; enter?: string; count?: [number, number, number]; width?: number; sub?: string }> =
  ({ t, text, color, glow, size = 150, style = "pop", enter = "slam", count, width = 960, sub }) => {
    const { fps } = useVideoConfig();
    const k = spring({ frame: t, fps, config: { damping: enter === "slam" ? 11 : 16, stiffness: enter === "slam" ? 260 : 140, mass: 0.7 } });
    let shown = text;
    if (count) { const v = Math.round(interpolate(t, [0, count[2]], [count[0], count[1]], { ...clamp, easing: (x) => 1 - Math.pow(1 - x, 3) })); shown = text.replace("#", v.toLocaleString("en-IN")); }
    if (enter === "type") shown = shown.slice(0, Math.floor(shown.length * prog(t, 0, Math.max(8, shown.length * 1.4), (x) => x)));
    const sc = enter === "slam" ? 1.45 - 0.45 * k : enter === "pop" ? 0.5 + 0.5 * k : 1;
    return (
      <div style={{ width, marginLeft: -width / 2, textAlign: "center", transform: `translateY(-50%) scale(${sc})`, opacity: enter === "fade" ? prog(t, 0, 14) : Math.min(1, t / 3) }}>
        <div style={{ fontFamily: fontFor(style, shown), fontSize: size, lineHeight: 1.05, fontWeight: 800, color, textTransform: "uppercase", letterSpacing: style === "serif" ? 6 : 1,
          textShadow: `0 8px 0 rgba(0,0,0,.5)${glow ? `, 0 0 50px ${glow}, 0 0 120px ${glow}` : ""}` }}>{shown}</div>
        {sub && <div style={{ fontFamily: fontFor("serif", sub), fontSize: size * 0.3, color, opacity: 0.85 * prog(t, 8, 20), letterSpacing: 6, marginTop: 18, textTransform: "uppercase" }}>{sub}</div>}
      </div>
    );
  };
