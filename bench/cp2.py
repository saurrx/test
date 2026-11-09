#!/usr/bin/env python3
"""Checkpoint 2 (after iterations 3-6): 0.5 s lead-in before the voice (P4), caption strip, keyword panels, stakes headline over a
focal image on the Pinaka brief (P10/P11), softer transitions on the diya brief. Built on checkpoint 1:

Checkpoint 1 (after iterations 1-2): same briefs and voice; new library (richer temple, devotee silhouette, bolder captions, wave)
plus playbook rules P6 (headline on frame 1) and P4 (visual change by 3 s). Writes bench/cp0/<brief>.json (Reel props)."""
import json, sys
from pathlib import Path
CP = Path(__file__).stem; OUT = Path(__file__).parent / CP; OUT.mkdir(exist_ok=True)
LEAD = 0.5
def words(b): return [{**w, "s": round(w["s"] + LEAD, 3), "e": round(w["e"] + LEAD, 3)} for w in json.load(open(f"bench/audio/{b}.words.json"))]
def scenes(cuts, end, specs):
    cuts = [c + LEAD if c > 0 else 0 for c in cuts]; end = end + LEAD
    out = []
    for i, sc in enumerate(specs):
        sc = dict(sc); sc["dur"] = round((cuts[i + 1] if i + 1 < len(cuts) else end) - cuts[i], 3); out.append(sc)
    return out
def save(b, props):
    props["audio"]["voAt"] = LEAD
    for x in props["audio"].get("sfx", []):
        if x["at"] > 0.05: x["at"] = round(x["at"] + LEAD, 3)
    (OUT / f"{b}.json").write_text(json.dumps(props, ensure_ascii=False, indent=1)); print(OUT / f"{b}.json")
G, W = "#ffb648", "#fff4dc"
def head(t, y=300, size=150, col=W, glow="#ff6a1f", font="pop", until=None, width=980):
    d = {"kind": "text", "text": t, "x": 540, "y": y, "size": size, "font": font, "color": col, "glow": glow, "at": 0.0, "textEnter": "slam", "width": width}
    if until: d["until"] = until; d["exit"] = "fade"
    return d
P = lambda **k: {"kind": "person", "x": 540, "y": 1690, "s": 1.15, "pose": "pray", "color": "#0c0705", "color2": G, "enter": "none", **k}

# ---- b1: temple bell (glow, English)
b = "b1_bell_en"
save(b, {"palette": "glow", "captions": {"style": "serif", "words": words(b), "y": 1250, "size": 86, "max": 4},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/music_temple.mp3", "musicVol": 0.16, "sfx": [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.5}, {"src": "audio/sfx_bell_low.mp3", "at": 7.7, "vol": 0.9}, {"src": "audio/sfx_bell_low.mp3", "at": 16.2, "vol": 0.8}]},
 "scenes": scenes([0, 3.0, 5.3, 7.1, 9.1, 14.8], 20.4, [
  {"bg": {"kind": "temple", "idol": "none", "lamps": 2}, "dust": True, "cam": {"z0": 1.2, "z1": 1.0}, "layers": [
    head("YOU RING IT WRONG", y=380, size=128), {"kind": "glowdot", "x": 540, "y": 700, "r": 520, "color2": G, "opacity": 0.5, "enter": "none"},
    {"kind": "bell", "x": 540, "y": 720, "s": 1.1, "color": "#1a0f08", "color2": G, "swing": 22, "speed": 3.2, "enter": "none"},
    {"kind": "cross", "x": 540, "y": 760, "color": "#ff3b30", "size": 240, "at": 1.6, "enter": "none"}]},
  {"trans": "fade", "bg": {"kind": "temple", "idol": "murti", "lamps": 2, "glow": 1.2}, "dust": True, "cam": {"z0": 1.0, "z1": 1.1}, "layers": []},
  {"trans": "flash", "bg": {"kind": "solid"}, "dust": True, "cam": {"z0": 1.0, "z1": 1.14}, "layers": [
    {"kind": "doorway", "x": 540, "y": 1000, "color": "#080403", "color2": G, "enter": "none"}, P(y=1620, s=1.2, pose="stand"), {"kind": "text", "text": "YOU", "x": 540, "y": 700, "size": 240, "font": "pop", "color": W, "glow": "#ff6a1f", "at": 0.7, "textEnter": "slam"}]},
  {"trans": "punch", "bg": {"kind": "temple", "idol": "none", "lamps": 2}, "cam": {"z0": 1.25, "z1": 1.3, "shakeAt": 0.65, "shake": 18}, "layers": [
    {"kind": "glowdot", "x": 540, "y": 640, "r": 480, "color2": G, "opacity": 0.6, "enter": "none"}, {"kind": "bell", "x": 540, "y": 640, "s": 1.1, "color": "#1a0f08", "color2": G, "swing": 2, "strikeAt": 18, "enter": "none"},
    {"kind": "rings", "x": 540, "y": 830, "color": G, "at": 0.65, "count": 5, "max": 1000}]},
  {"trans": "fade", "bg": {"kind": "radial", "cy": 50}, "dust": True, "cam": {"z0": 1.0, "z1": 1.08}, "layers": [
    {"kind": "glowdot", "x": 360, "y": 800, "r": 420, "color2": G, "opacity": 0.35, "enter": "none"}, P(x=360, y=1500, s=2.3),
    {"kind": "chakras", "x": 360, "y": 1560, "at": 1.6, "every": 14, "gap": 150, "r": 26, "enter": "none"}, {"kind": "wave", "x": 540, "y": 1010, "color": G, "fade": 170, "w": 900, "amp": 70, "enter": "fade"},
    {"kind": "text", "text": "#", "count": [1, 7, 110], "x": 820, "y": 620, "size": 380, "font": "serif", "color": W, "glow": G, "at": 1.6, "textEnter": "pop"},
    {"kind": "rings", "x": 360, "y": 800, "color": G, "at": 0.2, "count": 7, "every": 22, "max": 900, "width": 8}]},
  {"trans": "fade", "palette": "dusk", "bg": {"kind": "horizon"}, "stars": True, "cam": {"z0": 1.12, "z1": 1.0}, "layers": [
    {"kind": "moon", "x": 840, "y": 300, "color": "#fff1dd", "color2": "#3a1f3e", "r": 64}, {"kind": "mandir", "x": 540, "y": 1330, "s": 1.2, "color": "#12081f", "color2": "#ffcf5c", "enter": "none"},
    {"kind": "wave", "x": 540, "y": 1000, "color": G, "at": 1.45, "fade": 110, "w": 900, "amp": 90, "enter": "fade"},
    {"kind": "rings", "x": 540, "y": 1400, "color": G, "at": 1.45, "count": 3, "every": 30, "max": 1100, "width": 10},
    {"kind": "text", "text": "ONCE", "x": 540, "y": 1560, "size": 120, "font": "serif", "color": G, "at": 1.4, "textEnter": "fade", "opacity": 0.0}]}])})

# ---- b2: Pinaka (flat / Warli, Hinglish)
b = "b2_pinaka_hinglish"; C, D = "#ffe9c4", "#2b0f06"
save(b, {"palette": "clay", "captions": {"style": "pop", "words": words(b), "y": 1440},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/bed_folk.mp3", "musicVol": 0.2, "sfx": [{"src": "audio/sfx_hit.mp3", "at": 0.1}, {"src": "audio/sfx_whoosh.mp3", "at": 4.9, "vol": 0.6}, {"src": "audio/sfx_riser.mp3", "at": 17.6, "vol": 0.5}, {"src": "audio/sfx_crack.mp3", "at": 19.4, "vol": 1.0}]},
 "scenes": scenes([0, 2.2, 5.0, 8.0, 13.3, 16.3, 17.9], 21.0, [
  {"bg": {"kind": "linear"}, "cam": {"z0": 1.25, "z1": 1.0}, "layers": [
    {"kind": "glowdot", "x": 540, "y": 800, "r": 380, "color2": "#ffcf5c", "opacity": 0.75, "enter": "none"}, {"kind": "bow", "x": 590, "y": 800, "s": 0.78, "color": "#ffe08a", "color2": "#fff", "glow": False, "enter": "none"},
    {"kind": "crowd", "x": 540, "y": 1640, "count": 32, "cols": 16, "gap": 64, "rowGap": 70, "s": 0.55, "stagger": 0.2, "anim": "walk", "enter": "none"}, head("5,000 MEN FAILED.", y=380, size=128, col=C, glow="#ff6a1f")]},
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
lab = lambda t, x, y, at=0, col=W, size=84: {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": "serif", "color": col, "glow": None, "at": at, "textEnter": "fade", "panel": True}
save(b, {"palette": "glow", "captions": {"style": "serif", "words": words(b), "y": 1330, "size": 84, "max": 4},
 "audio": {"vo": f"audio/{b}.mp3", "music": "audio/music_temple.mp3", "musicVol": 0.16, "sfx": [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.4}, {"src": "audio/sfx_boom.mp3", "at": 13.9, "vol": 0.9}]},
 "scenes": scenes([0, 2.2, 4.0, 8.9, 11.6, 15.6], 19.4, [
  {"bg": {"kind": "temple", "idol": "none", "lamps": 2, "glow": 1.8}, "dust": True, "cam": {"z0": 1.25, "z1": 1.1}, "layers": [
    head("दीया किस दिशा में?", y=400, size=112, glow="#ff6a1f"), {"kind": "glowdot", "x": 540, "y": 880, "r": 460, "color2": G, "opacity": 0.6, "enter": "none"}, {"kind": "diya", "x": 540, "y": 980, "s": 3.2, "enter": "none"}]},
  {"trans": "punch", "bg": {"kind": "radial", "cy": 50}, "dust": True, "cam": {"z0": 1.15, "z1": 1.0}, "layers": [
    {"kind": "yantra", "x": 540, "y": 820, "r": 430, "draw": 0.8, "opacity": 0.5}, {"kind": "diya", "x": 540, "y": 900, "s": 2.6, "enter": "none"},
    lab("पूर्व", 900, 820, 0.1), lab("उत्तर", 540, 330, 0.3), lab("पश्चिम", 170, 820, 0.5), lab("दक्षिण", 540, 1120, 0.7)]},
  {"trans": "fade", "palette": "dusk", "bg": {"kind": "horizon"}, "dust": True, "cam": {"z0": 1.0, "z1": 1.1}, "layers": [
    {"kind": "sun", "x": 880, "y": 1050, "r": 190, "color": "#ffcf5c", "move": {"y": -260}, "enter": "fade"}, {"kind": "hills", "x": 540, "y": 1560, "color": "#12081f"},
    {"kind": "diya", "x": 440, "y": 1180, "s": 2.6, "lean": 26, "leanAt": 20, "enter": "none"}, lab("पूर्व", 860, 560, 1.0, "#12081f", 110),
    {"kind": "arrow", "x": 640, "y": 960, "color": "#fff1dd", "len": 260, "at": 1.2, "enter": "slide_l"}]},
  {"trans": "punch", "bg": {"kind": "radial", "cy": 45}, "dust": True, "cam": {"z0": 1.0, "z1": 1.08}, "layers": [
    {"kind": "thali", "x": 540, "y": 1640, "color2": G, "wicks": 5, "r": 150, "enter": "none"}, {"kind": "needle", "x": 540, "y": 860, "color": W, "color2": G, "angle": 0, "from": 90, "enter": "none"},
    lab("उत्तर", 540, 400, 0.3, G, 120), {"kind": "coins", "x": 540, "y": 1050, "color": "#ffd24a", "at": 1.2, "enter": "none"}]},
  {"trans": "cut", "palette": "storm", "bg": {"kind": "radial", "cy": 50}, "cam": {"z0": 1.0, "z1": 1.15, "shakeAt": 2.3, "shake": 24}, "layers": [
    {"kind": "diya", "x": 540, "y": 900, "s": 2.6, "color": "#9fb8c8", "lean": 0, "enter": "none"}, {"kind": "needle", "x": 540, "y": 640, "color": W, "color2": "#ff3b30", "angle": 180, "from": 0, "enter": "none"},
    lab("दक्षिण", 540, 1180, 0.4, "#ff6b60", 120), {"kind": "cross", "x": 540, "y": 800, "color": "#ff3b30", "size": 300, "at": 2.3, "enter": "none"}]},
  {"trans": "fade", "palette": "dusk", "bg": {"kind": "horizon"}, "stars": True, "dust": True, "cam": {"z0": 1.0, "z1": 1.12}, "layers": [
    {"kind": "mandir", "x": 540, "y": 1000, "s": 0.95, "color": "#12081f", "color2": "#ffcf5c", "enter": "none"}, {"kind": "diya", "x": 540, "y": 1640, "s": 2.4, "lean": 22, "leanAt": 30, "enter": "none"}]}])})
