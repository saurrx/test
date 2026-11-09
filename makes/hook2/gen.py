#!/usr/bin/env python3
"""Hook lab 2 (iteration 3): Pinaka story, flat lane, first ~5 s. Tests opening LINE (C3 family: number vs question vs
"nobody told you" vs stakes) and first-frame picture (crowd vs bow vs payoff-first vs dusk silhouettes). Every variant
has a frame-1 headline (P6)."""
import json
from pathlib import Path
OUT = Path(__file__).parent; C, D, Y = "#ffe9c4", "#2b0f06", "#ffcf5c"
W = lambda l: json.load(open(OUT / f"audio/{l}.words.json"))
def head(t, y=1050, size=150, col=C, band=True):
    L = [{"kind": "rect", "x": 540, "y": y, "w": 1080, "h": 340, "color": D, "opacity": 0.82, "enter": "none"}] if band else []
    return L + [{"kind": "text", "text": t, "x": 540, "y": y, "size": size, "font": "pop", "color": col, "glow": "#ff6a1f", "at": 0.0, "textEnter": "slam", "width": 1000}]
crowd = lambda **k: {"kind": "crowd", "x": 540, "y": 430, "count": 40, "cols": 8, "gap": 118, "rowGap": 112, "s": 1.0, "stagger": 0.35, "anim": "walk", "enter": "none", **k}
border = [{"kind": "border", "x": 540, "y": 230}, {"kind": "border", "x": 540, "y": 1700, "rot": 180}]
bigbow = lambda **k: {"kind": "bow", "x": 600, "y": 620, "s": 1.0, "color": "#12081f", "color2": Y, "enter": "pop", **k}
def reel(line, scenes, dur=5.2, pal="clay"):
    for s in scenes: s.setdefault("bg", {"kind": "linear"})
    scenes[-1]["dur"] = round(dur - sum(s["dur"] for s in scenes[:-1]), 2)
    return {"palette": pal, "captions": {"style": "pop", "words": W(line), "y": 1440}, "audio": {"vo": f"audio/h2_{line}.mp3", "music": "audio/bed_folk.mp3", "musicVol": 0.2, "sfx": [{"src": "audio/sfx_hit.mp3", "at": 0.05}]}, "scenes": scenes}
pull = {"dur": 2.4, "trans": "punch", "cam": {"x0": -50, "x1": 50}, "layers": [{"kind": "chest", "x": 720, "y": 800, "s": 0.9, "roll": 2.5, "enter": "slide_r", "move": {"x": -60}}, {"kind": "rope", "x": 150, "y": 780, "len": 280},
        {"kind": "crowd", "x": 190, "y": 760, "count": 6, "cols": 6, "gap": 62, "pose": "pull", "anim": "strain", "s": 0.95, "enter": "none"}, {"kind": "border", "x": 540, "y": 1100}]}
dusk_break = lambda at=0.0: {"dur": 2.6, "trans": "flash", "palette": "dusk", "bg": {"kind": "horizon"}, "cam": {"z0": 1.05, "z1": 1.22, "shakeAt": at + 1.2, "shake": 30}, "layers": [
    {"kind": "sun", "x": 540, "y": 700, "r": 240, "color": Y}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"}, {"kind": "figure", "x": 540, "y": 1130, "s": 3.2, "pose": "lift", "crown": True, "color": "#12081f", "enter": "none"},
    {"kind": "bow", "x": 540, "y": 730, "s": 0.6, "rot": 90, "color": "#12081f", "color2": "#fff", "breakAt": int((at + 1.2) * 30), "enter": "none"}, {"kind": "bolt", "x": 280, "y": 0, "color": "#fff", "at": at + 1.2, "until": at + 2.0, "enter": "none"}]}
V = {
 "a_number_crowd":  reel("L1", [{"dur": 2.2, "cam": {"z0": 1.25, "z1": 1.0}, "layers": border + [crowd()] + head("5,000 MEN. ONE BOW.")}, dict(pull)]),
 "b_number_bow":    reel("L1", [{"dur": 2.2, "palette": "dusk", "bg": {"kind": "radial", "cy": 35}, "dust": True, "cam": {"z0": 1.0, "z1": 1.15}, "layers": [{"kind": "rays", "x": 540, "y": 620, "opacity": 0.22}, bigbow(), crowd(y=1620, count=16, s=0.5, gap=120, anim="idle")] + head("5,000 MEN. ONE BOW.", col=C, band=False)}, dict(pull)]),
 "c_question":      reel("L2", [{"dur": 2.0, "cam": {"z0": 1.25, "z1": 1.0}, "layers": border + [crowd()] + head("WHY 5,000 MEN?")}, {**dict(pull), "dur": 2.2}], dur=4.3),
 "d_nobody_told":   reel("L3", [{"dur": 2.0, "palette": "dusk", "bg": {"kind": "radial", "cy": 35}, "dust": True, "cam": {"z0": 1.0, "z1": 1.15}, "layers": [{"kind": "rays", "x": 540, "y": 620, "opacity": 0.22}, bigbow()] + head("NOBODY TOLD YOU THIS", band=False)}, {**dict(pull), "dur": 2.4}], dur=4.5),
 "e_stakes_payoff": reel("L4", [dusk_break(0.0), {"dur": 2.0, "trans": "punch", "cam": {"z0": 1.2, "z1": 1.0}, "layers": border + [crowd()]}, {"dur": 1.5, "trans": "flash", "palette": "dusk", "bg": {"kind": "radial", "cy": 35}, "layers": [bigbow(y=800)]}], dur=6.2),
 "f_stakes_headline": reel("L4", [{"dur": 2.4, "cam": {"z0": 1.25, "z1": 1.0}, "layers": border + [crowd()] + head("5,000 MEN FAILED.")}, {"dur": 1.2, "trans": "punch", "palette": "dusk", "bg": {"kind": "radial", "cy": 35}, "layers": [bigbow(y=800)] + head("ONE PRINCE.", y=1150, band=False)}, dusk_break(0.0)], dur=6.2),
 "g_number_dusk":   reel("L1", [{"dur": 2.2, "palette": "dusk", "bg": {"kind": "horizon"}, "cam": {"z0": 1.2, "z1": 1.0}, "layers": [{"kind": "sun", "x": 540, "y": 560, "r": 230, "color": Y}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"}, crowd(y=1000, count=24, color="#12081f", s=1.0)] + head("5,000 MEN. ONE BOW.", y=330, band=False)}, {**dict(pull), "palette": "dusk", "bg": {"kind": "horizon"}}]),
}
for k, v in V.items(): (OUT / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False))
print(len(V), "variants")
