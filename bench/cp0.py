#!/usr/bin/env python3
"""Checkpoint 0: the three benchmark briefs built with the Phase-0 library. Writes bench/cp0/<brief>.json (Reel props)."""
import json, sys
from pathlib import Path
CP = Path(__file__).stem; OUT = Path(__file__).parent / CP; OUT.mkdir(exist_ok=True)
def words(b): return json.load(open(f"bench/audio/{b}.words.json"))
def scenes(cuts, end, specs):
    out = []
    for i, sc in enumerate(specs):
        sc = dict(sc); sc["dur"] = round((cuts[i + 1] if i + 1 < len(cuts) else end) - cuts[i], 3); out.append(sc)
    return out
def save(b, props): (OUT / f"{b}.json").write_text(json.dumps(props, ensure_ascii=False, indent=1)); print(OUT / f"{b}.json")
G, W = "#ffb648", "#fff4dc"

# ---- b1: temple bell (glow, English)
b = "b1_bell_en"
save(b, {"palette": "glow", "captions": {"style": "serif", "words": words(b), "y": 1330},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/bed_drone.mp3", "musicVol": 0.16, "sfx": [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.5}, {"src": "audio/sfx_bell_low.mp3", "at": 7.7, "vol": 0.9}, {"src": "audio/sfx_bell_low.mp3", "at": 16.2, "vol": 0.8}]},
 "scenes": scenes([0, 3.0, 5.3, 7.1, 9.1, 14.8], 20.4, [
  {"bg": {"kind": "temple", "idol": "none", "lamps": 2}, "dust": True, "cam": {"z0": 1.15, "z1": 1.0}, "layers": [
    {"kind": "bell", "x": 540, "y": 760, "s": 1.25, "color": "#1a0f08", "color2": G, "swing": 22, "speed": 3.2, "enter": "none"},
    {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 230, "at": 1.5, "enter": "none", "opacity": 0.9}]},
  {"trans": "fade", "bg": {"kind": "temple", "idol": "murti", "lamps": 2, "glow": 0.6}, "dust": True, "cam": {"z0": 1.0, "z1": 1.1}, "layers": []},
  {"trans": "flash", "bg": {"kind": "radial", "cy": 42}, "dust": True, "cam": {"z0": 1.0, "z1": 1.12}, "layers": [
    {"kind": "yantra", "x": 540, "y": 800, "r": 400, "draw": 1.2}, {"kind": "figure", "x": 540, "y": 930, "s": 4.2, "pose": "pray", "color": W, "enter": "rise"}]},
  {"trans": "punch", "bg": {"kind": "temple", "idol": "none", "lamps": 2}, "cam": {"z0": 1.25, "z1": 1.3, "shakeAt": 0.65, "shake": 18}, "layers": [
    {"kind": "bell", "x": 540, "y": 800, "s": 1.5, "color": "#1a0f08", "color2": G, "swing": 2, "strikeAt": 18, "enter": "none"},
    {"kind": "rings", "x": 540, "y": 1010, "color": G, "at": 0.65, "count": 5, "max": 1000}]},
  {"trans": "fade", "bg": {"kind": "radial", "cy": 50}, "dust": True, "cam": {"z0": 1.0, "z1": 1.08}, "layers": [
    {"kind": "figure", "x": 400, "y": 1150, "s": 5.0, "pose": "pray", "color": "#2a1a10", "enter": "fade"},
    {"kind": "chakras", "x": 400, "y": 1260, "at": 1.6, "every": 14, "gap": 96, "r": 24, "enter": "none"},
    {"kind": "text", "text": "#", "count": [1, 7, 110], "x": 800, "y": 800, "size": 380, "font": "serif", "color": W, "glow": G, "at": 1.6, "textEnter": "pop"},
    {"kind": "rings", "x": 400, "y": 900, "color": G, "at": 0.2, "count": 7, "every": 22, "max": 900, "width": 8}]},
  {"trans": "fade", "bg": {"kind": "temple", "idol": "none", "lamps": 3}, "dust": True, "cam": {"z0": 1.1, "z1": 1.0}, "layers": [
    {"kind": "bell", "x": 540, "y": 760, "s": 1.25, "color": "#1a0f08", "color2": G, "swing": 1, "strikeAt": 42, "enter": "none"},
    {"kind": "rings", "x": 540, "y": 950, "color": G, "at": 1.45, "count": 3, "every": 30, "max": 1100, "width": 10},
    {"kind": "text", "text": "ONCE", "x": 540, "y": 1560, "size": 120, "font": "serif", "color": G, "at": 1.4, "textEnter": "fade", "opacity": 0.0}]}])})

# ---- b2: Pinaka (flat / Warli, Hinglish)
b = "b2_pinaka_hinglish"; C, D = "#ffe9c4", "#2b0f06"
save(b, {"palette": "clay", "captions": {"style": "pop", "words": words(b), "y": 1430},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/bed_folk.mp3", "musicVol": 0.2, "sfx": [{"src": "audio/sfx_hit.mp3", "at": 0.1}, {"src": "audio/sfx_whoosh.mp3", "at": 4.9, "vol": 0.6}, {"src": "audio/sfx_riser.mp3", "at": 17.6, "vol": 0.5}, {"src": "audio/sfx_crack.mp3", "at": 19.4, "vol": 1.0}]},
 "scenes": scenes([0, 2.2, 5.0, 8.0, 13.3, 16.3, 17.9], 21.0, [
  {"bg": {"kind": "linear"}, "cam": {"z0": 1.25, "z1": 1.0}, "layers": [
    {"kind": "border", "x": 540, "y": 250}, {"kind": "crowd", "x": 540, "y": 520, "count": 56, "cols": 8, "gap": 118, "rowGap": 118, "s": 1.0, "stagger": 0.45, "anim": "walk", "enter": "none"},
    {"kind": "text", "text": "#", "count": [1, 5000, 34], "x": 540, "y": 1700, "size": 150, "color": C, "textEnter": "pop", "opacity": 0.0}]},
  {"trans": "punch", "bg": {"kind": "linear"}, "cam": {"x0": -50, "x1": 50}, "layers": [
    {"kind": "chest", "x": 720, "y": 900, "s": 0.9, "roll": 2.5, "enter": "slide_r", "move": {"x": -60}},
    {"kind": "rope", "x": 150, "y": 880, "len": 280}, {"kind": "crowd", "x": 190, "y": 860, "count": 6, "cols": 6, "gap": 62, "pose": "pull", "anim": "strain", "s": 0.95, "enter": "none"},
    {"kind": "border", "x": 540, "y": 1180}]},
  {"trans": "flash", "palette": "dusk", "bg": {"kind": "radial", "cy": 45}, "dust": True, "cam": {"z0": 1.0, "z1": 1.15}, "layers": [
    {"kind": "rays", "x": 540, "y": 820, "opacity": 0.22}, {"kind": "bow", "x": 600, "y": 820, "s": 0.95, "color": "#12081f", "color2": "#ffcf5c", "enter": "pop"}]},
  {"trans": "fade", "bg": {"kind": "linear"}, "cam": {"z0": 1.0, "z1": 1.08}, "layers": [
    {"kind": "palace", "x": 540, "y": 720, "s": 1.05, "color": C, "color2": "#7a2e12"},
    {"kind": "figure", "x": 330, "y": 1130, "s": 2.3, "crown": True, "pose": "point", "enter": "rise"},
    {"kind": "figure", "x": 760, "y": 1150, "s": 2.0, "prop": "bun", "pose": "stand", "at": 2.9, "enter": "pop"},
    {"kind": "rings", "x": 760, "y": 1100, "at": 2.9, "count": 2, "max": 320, "color": C}]},
  {"trans": "punch", "bg": {"kind": "linear"}, "cam": {"z0": 1.05, "z1": 1.0}, "layers": [
    {"kind": "bow", "x": 540, "y": 1180, "s": 0.5, "rot": 90, "color": D, "color2": D, "glow": False, "enter": "none"},
    {"kind": "figure", "x": 250, "y": 980, "s": 1.8, "crown": True, "pose": "lift", "anim": "tremble", "enter": "none", "until": 1.0},
    {"kind": "figure", "x": 250, "y": 980, "s": 1.8, "crown": True, "pose": "fall", "at": 1.0, "enter": "none"},
    {"kind": "figure", "x": 540, "y": 980, "s": 1.8, "crown": True, "pose": "lift", "anim": "tremble", "enter": "none", "until": 1.6},
    {"kind": "figure", "x": 540, "y": 980, "s": 1.8, "crown": True, "pose": "fall", "at": 1.6, "enter": "none"},
    {"kind": "figure", "x": 830, "y": 980, "s": 1.8, "crown": True, "pose": "lift", "anim": "tremble", "enter": "none", "until": 2.2},
    {"kind": "figure", "x": 830, "y": 980, "s": 1.8, "crown": True, "pose": "fall", "at": 2.2, "enter": "none"}]},
  {"trans": "flash", "palette": "dusk", "bg": {"kind": "horizon"}, "cam": {"z0": 1.0, "z1": 1.1}, "layers": [
    {"kind": "sun", "x": 540, "y": 880, "r": 250, "color": "#ffcf5c"}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"},
    {"kind": "figure", "x": 540, "y": 1300, "s": 3.4, "pose": "stand", "crown": True, "color": "#12081f", "enter": "rise"}]},
  {"trans": "cut", "palette": "dusk", "bg": {"kind": "horizon"}, "cam": {"z0": 1.1, "z1": 1.25, "shakeAt": 1.55, "shake": 34}, "layers": [
    {"kind": "sun", "x": 540, "y": 880, "r": 250, "color": "#ffcf5c"}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"},
    {"kind": "figure", "x": 540, "y": 1300, "s": 3.4, "pose": "lift", "crown": True, "color": "#12081f", "enter": "none"},
    {"kind": "bow", "x": 540, "y": 900, "s": 0.6, "rot": 90, "color": "#12081f", "color2": "#fff", "breakAt": 46, "enter": "drop"},
    {"kind": "bolt", "x": 300, "y": 0, "color": "#fff", "at": 1.55, "until": 2.3, "enter": "none"}, {"kind": "bolt", "x": 800, "y": 0, "color": "#fff", "at": 1.7, "until": 2.5, "seed": 5, "enter": "none"}]}])})

# ---- b3: diya direction (glow, Hindi)
b = "b3_diya_hi"
lab = lambda t, x, y, at=0, col=W, size=84: {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": "serif", "color": col, "glow": G, "at": at, "textEnter": "fade"}
save(b, {"palette": "glow", "captions": {"style": "serif", "words": words(b), "y": 1420, "size": 68},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/bed_drone.mp3", "musicVol": 0.16, "sfx": [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.4}, {"src": "audio/sfx_boom.mp3", "at": 13.9, "vol": 0.9}]},
 "scenes": scenes([0, 4.0, 8.9, 11.6, 15.6], 19.4, [
  {"bg": {"kind": "radial", "cy": 50}, "dust": True, "cam": {"z0": 1.3, "z1": 1.0}, "layers": [
    {"kind": "yantra", "x": 540, "y": 880, "r": 430, "draw": 2.0, "opacity": 0.5}, {"kind": "diya", "x": 540, "y": 960, "s": 3.0, "enter": "none"},
    lab("पूर्व", 900, 880, 1.0), lab("उत्तर", 540, 380, 1.3), lab("पश्चिम", 170, 880, 1.6), lab("दक्षिण", 540, 1250, 1.9), lab("?", 540, 640, 2.2, G, 200)]},
  {"trans": "fade", "palette": "dusk", "bg": {"kind": "horizon"}, "dust": True, "cam": {"z0": 1.0, "z1": 1.1}, "layers": [
    {"kind": "sun", "x": 880, "y": 1050, "r": 190, "color": "#ffcf5c", "move": {"y": -260}, "enter": "fade"}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"},
    {"kind": "diya", "x": 440, "y": 1180, "s": 2.6, "lean": 26, "leanAt": 20, "enter": "none"}, lab("पूर्व", 860, 560, 1.0, "#12081f", 110),
    {"kind": "arrow", "x": 640, "y": 960, "color": "#fff1dd", "len": 260, "at": 1.2, "enter": "slide_l"}]},
  {"trans": "flash", "bg": {"kind": "radial", "cy": 45}, "dust": True, "cam": {"z0": 1.0, "z1": 1.08}, "layers": [
    {"kind": "diya", "x": 540, "y": 1180, "s": 2.4, "enter": "none"}, {"kind": "needle", "x": 540, "y": 860, "color": W, "color2": G, "angle": 0, "from": 90, "enter": "none"},
    lab("उत्तर", 540, 400, 0.3, G, 120), {"kind": "coins", "x": 540, "y": 1050, "color": "#ffd24a", "at": 1.2, "enter": "none"}]},
  {"trans": "cut", "palette": "storm", "bg": {"kind": "radial", "cy": 50}, "cam": {"z0": 1.0, "z1": 1.15, "shakeAt": 2.3, "shake": 24}, "layers": [
    {"kind": "diya", "x": 540, "y": 900, "s": 2.6, "color": "#9fb8c8", "lean": 0, "enter": "none"}, {"kind": "needle", "x": 540, "y": 640, "color": W, "color2": "#ff3b30", "angle": 180, "from": 0, "enter": "none"},
    lab("दक्षिण", 540, 1180, 0.4, "#ff6b60", 120), {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 300, "at": 2.3, "enter": "none"}]},
  {"trans": "fade", "bg": {"kind": "temple", "idol": "none", "lamps": 2}, "dust": True, "cam": {"z0": 1.0, "z1": 1.12}, "layers": [
    {"kind": "diya", "x": 540, "y": 1180, "s": 2.8, "lean": 22, "leanAt": 30, "enter": "none"}, {"kind": "yantra", "x": 540, "y": 800, "r": 300, "draw": 1.5, "opacity": 0.6}]}])})
