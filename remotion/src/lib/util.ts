import { Easing, interpolate } from "remotion";

// Deterministic pseudo-random in [0,1) from any number of seeds (Remotion renders frames in parallel: no Math.random).
export const rnd = (...s: number[]) => {
  let h = 2166136261;
  for (const v of s) { h ^= Math.floor(v * 1000) + 0x9e3779b9; h = Math.imul(h, 16777619); h ^= h >>> 13; }
  h = Math.imul(h ^ (h >>> 15), 2246822507); h ^= h >>> 13;
  return ((h >>> 0) % 100000) / 100000;
};
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const ease = Easing.bezier(0.22, 1, 0.36, 1); // fast out, soft landing
export const easeIO = Easing.inOut(Easing.cubic);
export const prog = (frame: number, from: number, to: number, e = ease) =>
  interpolate(frame, [from, Math.max(to, from + 1)], [0, 1], { ...clamp, easing: e });
// smooth value noise in [-1,1] for flicker / drift
export const noise = (t: number, seed = 0) => {
  const i = Math.floor(t), f = t - i, u = f * f * (3 - 2 * f);
  return (rnd(i, seed) * (1 - u) + rnd(i + 1, seed) * u) * 2 - 1;
};
export type Palette = { bg: string; bg2: string; fg: string; accent: string; accent2: string };
export const PALETTES: Record<string, Palette> = {
  glow: { bg: "#050308", bg2: "#1a0d06", fg: "#fff4dc", accent: "#ffb648", accent2: "#ff6a1f" },
  night: { bg: "#070b1c", bg2: "#1b2350", fg: "#f4f1ff", accent: "#ffd166", accent2: "#7aa2ff" },
  clay: { bg: "#7a2e12", bg2: "#b5522a", fg: "#fff6e6", accent: "#ffe9c4", accent2: "#2b0f06" }, // Warli: white on terracotta
  dusk: { bg: "#1d0f2e", bg2: "#e2603a", fg: "#fff1dd", accent: "#ffcf5c", accent2: "#12081f" },
  storm: { bg: "#0b1016", bg2: "#2a3a4c", fg: "#eef6ff", accent: "#9fe3ff", accent2: "#ffd24a" },
};
