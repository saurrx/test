import { loadFont as cinzel } from "@remotion/google-fonts/Cinzel";
import { loadFont as anton } from "@remotion/google-fonts/Anton";
import { loadFont as baloo } from "@remotion/google-fonts/Baloo2";
import { loadFont as tiro } from "@remotion/google-fonts/TiroDevanagariHindi";
import { loadFont as mukta } from "@remotion/google-fonts/Mukta";

const C = cinzel("normal", { weights: ["600", "800"], subsets: ["latin"] }).fontFamily;
const A = anton("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;
const B = baloo("normal", { weights: ["700", "800"], subsets: ["devanagari", "latin"] }).fontFamily;
const T = tiro("normal", { weights: ["400"], subsets: ["devanagari", "latin"] }).fontFamily;
const M = mukta("normal", { weights: ["600", "800"], subsets: ["devanagari", "latin"] }).fontFamily;
const hasDeva = (s: string) => /[ऀ-ॿ]/.test(s);
// Pick a face that can shape the script: Latin display faces have no Devanagari glyphs.
export const fontFor = (style: "serif" | "pop" | "clean", text: string) =>
  style === "serif" ? (hasDeva(text) ? `${T}, ${C}` : `${C}, ${T}`) : style === "pop" ? (hasDeva(text) ? `${B}, ${A}` : `${A}, ${B}`) : `${M}`;
