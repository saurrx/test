import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { noise, Palette, rnd } from "./util";

export const Gradient: React.FC<{ p: Palette; kind?: "radial" | "linear" | "horizon"; cy?: number }> = ({ p, kind = "radial", cy = 45 }) => (
  <AbsoluteFill style={{
    background: kind === "radial" ? `radial-gradient(ellipse 90% 60% at 50% ${cy}%, ${p.bg2} 0%, ${p.bg} 75%)`
      : kind === "horizon" ? `linear-gradient(180deg, ${p.bg} 0%, ${p.bg} 30%, ${p.bg2} 78%, ${p.accent} 130%)`
      : `linear-gradient(180deg, ${p.bg} 0%, ${p.bg2} 100%)`,
  }} />
);

// Floating dust motes / embers. Cheap: plain divs with radial gradients.
export const Dust: React.FC<{ color: string; count?: number; rise?: number; seed?: number; size?: number }> = ({ color, count = 40, rise = 30, seed = 1, size = 6 }) => {
  const f = useCurrentFrame(); const { width: W, height: H } = useVideoConfig();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: count }).map((_, i) => {
        const x0 = rnd(i, seed) * W, y0 = rnd(i, seed, 2) * H, sp = 0.3 + rnd(i, seed, 3);
        const y = ((y0 - f * rise * sp / 30) % H + H) % H;
        const x = x0 + Math.sin(f / 40 + i) * 30 * sp;
        const s = size * (0.4 + rnd(i, seed, 4));
        const tw = 0.35 + 0.65 * Math.abs(Math.sin(f / (12 + 20 * rnd(i, 5)) + i));
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: s, height: s, borderRadius: "50%",
          background: color, opacity: tw * 0.8, boxShadow: `0 0 ${s * 2}px ${color}` }} />;
      })}
    </AbsoluteFill>
  );
};

// Film treatment: animated grain (low-res turbulence scaled up), vignette, slight flicker.
export const Film: React.FC<{ grain?: number; vignette?: number; flicker?: number }> = ({ grain = 0.12, vignette = 0.7, flicker = 0.04 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {grain > 0 && (
        <svg width="100%" height="100%" viewBox="0 0 270 480" preserveAspectRatio="none" style={{ position: "absolute", opacity: grain, mixBlendMode: "overlay" }}>
          <filter id="gr"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 97} /><feColorMatrix type="saturate" values="0" /></filter>
          <rect width="270" height="480" filter="url(#gr)" />
        </svg>
      )}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 75% 65% at 50% 48%, transparent 45%, rgba(0,0,0,${vignette}) 100%)` }} />
      <AbsoluteFill style={{ background: "#000", opacity: Math.max(0, flicker * noise(f / 3, 9)) }} />
    </AbsoluteFill>
  );
};

export const Stars: React.FC<{ color?: string; count?: number; seed?: number; maxY?: number }> = ({ color = "#fff", count = 90, seed = 3, maxY = 0.6 }) => {
  const f = useCurrentFrame(); const { width: W, height: H } = useVideoConfig();
  return (
    <AbsoluteFill>
      {Array.from({ length: count }).map((_, i) => {
        const s = 2 + 4 * rnd(i, seed, 1);
        return <div key={i} style={{ position: "absolute", left: rnd(i, seed) * W, top: rnd(i, seed, 2) * H * maxY, width: s, height: s, borderRadius: "50%",
          background: color, opacity: 0.3 + 0.7 * Math.abs(Math.sin(f / (15 + 30 * rnd(i, 7)) + i * 3)) }} />;
      })}
    </AbsoluteFill>
  );
};
