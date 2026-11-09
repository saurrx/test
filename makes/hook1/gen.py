#!/usr/bin/env python3
"""Hook lab 1 (iteration 1): bell brief, first 5.3 s, same voice line, one visual factor changed per variant.
Tests craft hypotheses C1 (bright first frame), C4 (motion from frame 1), C2-ish (slam text), C8 (red cross), C6 (person), C7 (3 shots), C5 (caption style)."""
import copy, json
from pathlib import Path
OUT = Path(__file__).parent; G, W, DARK = "#ffb648", "#fff4dc", "#1a0f08"
words = [w for w in json.load(open("bench/audio/b1_bell_en.words.json")) if w["s"] < 5.0]
audio = {"vo": "audio/b1_bell_en.mp3", "music": "audio/bed_drone.mp3", "musicVol": 0.16}
def bell(**k): return {"kind": "bell", "x": 540, "y": 760, "s": 1.25, "color": DARK, "color2": G, "swing": 14, "speed": 4, "enter": "none", **k}
glow = {"kind": "glowdot", "x": 540, "y": 800, "r": 520, "color2": G, "opacity": 0.5, "enter": "none"}
murti = {"dur": 2.3, "trans": "fade", "bg": {"kind": "temple", "idol": "murti", "lamps": 2, "glow": 1.0}, "dust": True, "cam": {"z0": 1.0, "z1": 1.1}, "layers": []}
def reel(first, caps="serif", extra_scenes=None):
    sc = first if isinstance(first, list) else [first]
    return {"palette": "glow", "captions": {"style": caps, "words": words, "y": 1330}, "audio": audio, "scenes": sc + (extra_scenes if extra_scenes is not None else [murti])}
A = lambda layers, cam=None, glowk=1.0: {"dur": 3.0, "bg": {"kind": "temple", "idol": "none", "lamps": 2, "glow": glowk}, "dust": True, "cam": cam or {"z0": 1.1, "z1": 1.0}, "layers": layers}
V = {
 "v1_base":    reel(A([bell(swing=22, speed=3.2), {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 230, "at": 1.5, "enter": "none", "opacity": 0.9}], {"z0": 1.15, "z1": 1.0}, 0.6)),
 "v2_bright":  reel(A([glow, bell()], None, 1.8)),
 "v3_strike0": reel(A([glow, bell(swing=2, strikeAt=2), {"kind": "rings", "x": 540, "y": 960, "color": G, "at": 0.08, "count": 4, "max": 1000, "enter": "none"}], {"z0": 1.38, "z1": 1.0, "shakeAt": 0.07, "shake": 20}, 1.8)),
 "v4_text":    reel(A([glow, bell(y=900, s=1.05), {"kind": "text", "text": "YOU RING IT WRONG", "x": 540, "y": 330, "size": 132, "font": "pop", "color": W, "glow": "#ff6a1f", "at": 0.1, "width": 900}], None, 1.8)),
 "v5_cross":   reel(A([glow, bell(), {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 260, "at": 1.55, "enter": "none"}], {"z0": 1.1, "z1": 1.0, "shakeAt": 1.6, "shake": 16}, 1.8)),
 "v6_person":  reel(A([glow, bell(y=640, s=1.0), {"kind": "person", "x": 420, "y": 1250, "s": 1.5, "pose": "ring", "color": "#0c0705", "color2": G, "enter": "none"}], None, 1.8)),
 "v7_3shots":  reel([{"dur": 1.7, "bg": {"kind": "temple", "idol": "none", "lamps": 2, "glow": 1.8}, "dust": True, "cam": {"z0": 1.7, "z1": 1.55, "y0": -160, "y1": -160}, "layers": [glow, bell()]},
                     {"dur": 1.3, "trans": "punch", "bg": {"kind": "temple", "idol": "none", "lamps": 2, "glow": 1.8}, "dust": True, "cam": {"z0": 1.0, "z1": 1.05, "shakeAt": 0.1, "shake": 16}, "layers": [glow, bell(), {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 260, "at": 0.05, "enter": "none"}]}]),
 "v8_popcaps": reel(A([glow, bell()], None, 1.8), caps="pop"),
}
for k, v in V.items(): (OUT / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False))
print(len(V), "variants")
