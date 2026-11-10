#!/usr/bin/env python3
"""Reel 6: "Om Namah Shivaya: five syllables, five elements" (original, English, glow lane, ~67 s, free voice).
Part 3 of the Shiva series, promised at the end of reel 5 (P8). Applies P1, P4 (lead-in), P6/P10/P11 (stakes headline over a focal image), P16 (a new picture every 2-4 s),
P17 (a usable list worth saving), P18 (no comment-bait ending: "save this" + part 3)."""
import json
from pathlib import Path
D = Path(__file__).parent; G, W, DARK, RED, BLUE = "#ffb648", "#fff4dc", "#120a07", "#ff3b30", "#9fe3ff"
words = json.load(open(D / "audio/vo.words.json")); LEAD = 0.5
for w in words: w["s"] = round(w["s"] + LEAD, 3); w["e"] = round(w["e"] + LEAD, 3)
def T(tok, n=1):
    k = 0
    for w in words:
        if w["w"].strip(".,?:") == tok.strip(".,?:"):
            k += 1
            if k == n: return w["s"]
    raise KeyError(tok)
def txt(t, x=540, y=400, size=110, font="pop", col=W, at=0, enter="slam", glow="#ff6a1f", panel=True, **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": font, "color": col, "glow": glow, "at": at, "textEnter": enter, "panel": panel, **k}
def glow(x=540, y=860, r=520, o=0.6, c=G, **k): return {"kind": "glowdot", "x": x, "y": y, "r": r, "color2": c, "opacity": o, "enter": "none", **k}
def lingam(**k): return {"kind": "lingam", "x": 540, "y": 860, "s": 0.9, "color": DARK, "color2": G, "enter": "none", **k}
def cross(x=540, y=860, size=240, at=0, **k): return {"kind": "cross", "x": x, "y": y, "color": RED, "size": size, "at": at, "enter": "none", **k}
def step(n): return {"kind": "text", "text": str(n), "x": 150, "y": 420, "size": 260, "font": "serif", "color": W, "glow": G, "textEnter": "slam"}
def item(kind, **k): return {**{"kind": kind, "x": 540, "y": 880, "s": 1.5, "color2": G, "enter": "pop"}, **k}
temple = lambda idol="none", g=1.7, lamps=2: {"kind": "temple", "idol": idol, "lamps": lamps, "glow": g}
rad = lambda cy=46: {"kind": "radial", "cy": cy}
night = dict(palette="night", bg={"kind": "linear"}, stars=True)
S = []
def sc(at, **k): S.append((at, k))
EARTH, WATER, FIRE, AIR, SPACE = "#e0a35a", "#6fc3ff", "#ff7a2a", "#cfe9ff", "#c9b8ff"
person = lambda **k: {"kind": "person", "x": 540, "y": 1700, "s": 1.3, "pose": "pray", "color": "#0c0705", "color2": G, "enter": "none", **k}
def syl(t, s, col, i):  # one syllable slams in, big, with five progress dots
    dots = [{"kind": "glowdot", "x": 300 + j * 120, "y": 1240, "r": 34 if j <= i else 16, "color2": col if j <= i else "#6b5a45", "opacity": 0.95 if j <= i else 0.5, "enter": "none"} for j in range(5)]
    sc(t, trans="punch", bg=rad(44), dust=True, cam={"z0": 1.0, "z1": 1.1, "shakeAt": 0.0, "shake": 8}, layers=[glow(y=780, r=560, o=0.6, c=col), {"kind": "rings", "x": 540, "y": 780, "color": col, "count": 1, "max": 520, "width": 6, "enter": "none"}, txt(s, y=780, size=420, font="serif", col=W, glow=col, panel=False)] + dots)
def element(tok, s, name, col, body, body_tok, body_occ, pal, bgk, art, art2):
    t = T(tok, 2) - 0.1
    sc(t, trans="flash", palette=pal, bg=bgk, dust=True, stars=(pal == "night"), cam={"z0": 1.0, "z1": 1.1}, layers=art + [txt(s, x=250, y=420, size=230, font="serif", col=W, glow=col, panel=False), txt(name, x=690, y=420, size=120, col=col, glow=None, at=T(name.lower() + ".") - t - 0.15)])
    t2 = T(body_tok, body_occ) - 0.1
    sc(t2, trans="punch", palette=pal, bg=bgk, dust=True, stars=(pal == "night"), cam={"z0": 1.25, "z1": 1.4}, layers=art2 + [txt(body, y=400, size=120, col=W, glow=col, at=0.25)])

# hook
sc(0.0, bg=temple(g=2.0), dust=True, cam={"z0": 1.25, "z1": 1.0}, layers=[glow(y=820, o=0.75), {"kind": "rays", "x": 540, "y": 860, "opacity": 0.16}, lingam(y=900, s=1.0), txt("YOU CHANT IT. DO YOU KNOW IT?", y=400, size=112)])
t = T("But") - 0.1; sc(t, trans="punch", bg=temple("lingam", 1.5, 3), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[person(s=1.2), {"kind": "wave", "x": 540, "y": 1180, "color": G, "at": 0.2, "fade": 190, "w": 900, "amp": 70, "enter": "fade"}, txt("WHAT ARE YOU SAYING?", y=400, size=104, col=G, at=T("what") - t)])
t = T("Om") - 0.1; sc(t, trans="flash", bg=rad(44), dust=True, cam={"z0": 1.12, "z1": 1.0}, layers=[glow(y=860, r=600, o=0.65), {"kind": "yantra", "x": 540, "y": 860, "r": 430, "draw": 1.2}, txt("OM NAMAH SHIVAYA", y=400, size=118, font="serif", col=W, glow=G)])
t = T("Five") - 0.1; sc(t, trans="punch", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(), {"kind": "rays", "x": 540, "y": 860, "opacity": 0.14}, txt("5", y=820, size=560, font="serif", col=G, glow="#ff6a1f", panel=False), txt("SYLLABLES", y=1240, size=120, at=T("syllables.") - t)])
for i, (s, col) in enumerate([("NA", EARTH), ("MA", WATER), ("SHI", FIRE), ("VA", AIR), ("YA", SPACE)]): syl(T(s.capitalize() + ".", 1) - 0.1, s, col, i)
t = T("It") - 0.1; sc(t, trans="fade", **night, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(y=860, r=480, o=0.5, c="#7aa2ff"), {"kind": "yantra", "x": 540, "y": 860, "r": 400, "draw": 0.9, "color": "#bfe0ff", "spin": 0.5}, txt("PANCHAKSHARA", y=400, size=110, col="#f4f1ff", glow="#7aa2ff", at=T("Panchakshara:") - t), txt("THE 5-LETTER MANTRA", y=1640, size=76, col="#ffcf5c", glow=None, at=T("five-letter") - t)])
t = T("And") - 0.1; sc(t, trans="punch", bg=rad(48), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[glow(y=980, r=620, o=0.55), person(y=1560, s=2.0, pose="stand")] + [{"kind": "glowdot", "x": 540, "y": 640 + j * 170, "r": 46, "color2": c, "opacity": 0.95, "at": 0.5 + j * 0.3, "enter": "pop"} for j, c in enumerate([SPACE, AIR, FIRE, WATER, EARTH])] + [txt("5 ELEMENTS. YOUR BODY.", y=400, size=104, col=G, at=T("element") - t)])
element("Na", "NA", "EARTH", EARTH, "YOUR BONES", "Your", 1, "clay", {"kind": "horizon"},
        [{"kind": "mountain", "x": 540, "y": 1330, "s": 1.5, "color": "#2a160a", "color2": EARTH, "enter": "none"}, glow(y=900, r=520, o=0.45, c=EARTH)],
        [glow(y=900, r=520, o=0.5, c=EARTH), person(y=1500, s=2.2, pose="stand", color2=EARTH), {"kind": "rings", "x": 540, "y": 900, "color": EARTH, "count": 2, "max": 420, "width": 8, "enter": "none"}])
element("Ma", "MA", "WATER", WATER, "YOUR BLOOD", "Your", 2, "night", {"kind": "linear"},
        [glow(y=1000, r=560, o=0.5, c=WATER), {"kind": "river", "x": 540, "y": 1000, "color": WATER, "w": 1100, "rows": 3, "enter": "none"}],
        [glow(y=900, r=520, o=0.55, c="#ff4a4a"), person(y=1500, s=2.2, pose="stand", color2="#ff6a5a"), {"kind": "wave", "x": 540, "y": 900, "color": "#ff6a5a", "fade": 190, "w": 900, "amp": 90, "enter": "none"}])
element("Shi", "SHI", "FIRE", FIRE, "THE HEAT IN YOUR BELLY", "The", 1, "blood", rad(50),
        [glow(y=1100, r=640, o=0.6, c=FIRE), {"kind": "fire", "x": 540, "y": 1500, "color": "#ff5a2a", "color2": "#ffd24a", "w": 900, "h": 760, "enter": "fade"}],
        [glow(y=1040, r=420, o=0.75, c=FIRE), person(y=1500, s=2.2, pose="stand", color2=FIRE), {"kind": "flame", "x": 540, "y": 1080, "s": 1.4, "enter": "pop"}])
element("Va", "VA", "AIR", AIR, "YOUR BREATH", "Your", 3, "dusk", {"kind": "horizon"},
        [glow(y=800, r=560, o=0.4, c=AIR), {"kind": "birds", "x": 200, "y": 1000, "color": "#f1f6ff", "count": 9, "s": 2.2, "enter": "none", "move": {"x": 700, "y": -400}}],
        [glow(y=820, r=520, o=0.45, c=AIR), person(y=1500, s=2.2, pose="stand", color2=AIR), {"kind": "rings", "x": 540, "y": 860, "color": AIR, "count": 3, "max": 520, "width": 5, "enter": "none"}])
element("Ya", "YA", "SPACE", SPACE, "THE SILENCE INSIDE YOU", "The", 2, "night", {"kind": "linear"},
        [glow(y=860, r=520, o=0.4, c=SPACE), {"kind": "moon", "x": 800, "y": 760, "color": "#f4f1ff", "color2": "#0d1330", "r": 90}],
        [glow(y=900, r=260, o=0.8, c=SPACE), {"kind": "yantra", "x": 540, "y": 900, "r": 300, "draw": 1.5, "color": SPACE, "spin": 0.3}])
t = T("So", 1) - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, stars=True, cam={"z0": 1.12, "z1": 1.0}, layers=[{"kind": "mandir", "x": 540, "y": 1180, "s": 0.7, "color": "#12081f", "color2": "#ffcf5c", "enter": "none"}, cross(y=1000, size=300, width=40, at=T("not") - t), txt("NOT A GOD FAR AWAY", y=400, size=104, at=T("not") - t)])
t = T("You", 2) - 0.1; sc(t, trans="punch", bg=rad(48), dust=True, cam={"z0": 1.0, "z1": 1.14}, layers=[glow(y=980, r=640, o=0.6), person(y=1560, s=2.0, pose="pray")] + [{"kind": "glowdot", "x": 540, "y": 640 + j * 170, "r": 46, "color2": c, "opacity": 0.95, "enter": "none"} for j, c in enumerate([SPACE, AIR, FIRE, WATER, EARTH])] + [txt("EVERYTHING YOU ARE", y=400, size=108, col=G, at=T("everything") - t)])
t = T("and") - 0.1; sc(t, trans="flash", bg=temple(g=2.1, lamps=3), dust=True, cam={"z0": 1.2, "z1": 1.0}, layers=[glow(y=820, o=0.8), {"kind": "rays", "x": 540, "y": 820, "opacity": 0.2}, lingam(y=900, s=1.0), txt("OFFERED TO SHIVA", y=400, size=110, at=T("offering") - t)])
t = T("So", 2) - 0.1; sc(t, trans="cut", palette="blood", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.08, "shakeAt": 0.3, "shake": 12}, layers=[glow(y=880, o=0.45, c=RED), txt("DON'T RUSH IT", y=860, size=170, col=W, glow=RED, at=0.2, panel=False)])
t = T("One", 1) - 0.1; sc(t, trans="fade", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(y=900, r=560, o=0.5), {"kind": "rings", "x": 540, "y": 900, "color": G, "count": 3, "max": 620, "width": 6, "enter": "none"}, txt("1 SYLLABLE", y=780, size=130, col=W, panel=False), txt("1 BREATH", y=1020, size=130, col=G, at=T("One", 2) - t, panel=False)])
t = T("Tomorrow") - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "sun", "x": 540, "y": 1050, "r": 190, "color": "#ffcf5c", "move": {"y": -260, "over": 2.5}}, {"kind": "hills", "x": 540, "y": 1400, "color": "#1a0d22", "enter": "none"}, person(y=1760, s=1.0, pose="pray", color="#0a0612"), txt("TOMORROW MORNING", y=400, size=104, at=0.2)])
t = T("Na.", 3) - 0.1; cols = [EARTH, WATER, FIRE, AIR, SPACE]; toks = ["Na.", "Ma.", "Shi.", "Va.", "Ya."]
sc(t, trans="punch", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[glow(y=900, r=640, o=0.5), {"kind": "yantra", "x": 540, "y": 900, "r": 460, "draw": 4.5, "spin": 0.2}] +
   [txt(s.strip(".").upper(), y=520 + j * 190, size=150, font="serif", col=W, glow=cols[j], at=max(0, T(s, 3 if j == 0 else 2) - t - 0.05), panel=False) for j, s in enumerate(toks)])
t = T("Save") - 0.1; rows5 = ["NA  ·  EARTH  ·  BONES", "MA  ·  WATER  ·  BLOOD", "SHI  ·  FIRE  ·  WARMTH", "VA  ·  AIR  ·  BREATH", "YA  ·  SPACE  ·  SILENCE"]
sc(t, trans="punch", bg=temple("none", 1.3, 2), dust=True, cam={"z0": 1.06, "z1": 1.0}, layers=[{"kind": "rect", "x": 540, "y": 800, "w": 960, "h": 900, "rx": 40, "color": "#000", "opacity": 0.8, "enter": "none"}, {"kind": "border", "x": 540, "y": 385, "color": G, "w": 860, "n": 14},
   {"kind": "text", "text": "OM NAMAH SHIVAYA", "x": 540, "y": 520, "size": 60, "font": "serif", "color": G, "glow": None, "textEnter": "fade"}] +
   [{"kind": "text", "text": r, "x": 540, "y": 650 + i * 108, "size": 56, "font": "serif", "color": W, "glow": None, "at": 0.2 + i * 0.25, "textEnter": "fade"} for i, r in enumerate(rows5)] + [txt("SAVE THIS", y=1650, size=90, col=G, at=0.3)])
t = T("In") - 0.1; sc(t, trans="flash", **night, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "mountain", "x": 540, "y": 1380, "s": 1.4, "color": "#0d1230", "color2": "#dfe6ff", "enter": "none"}, glow(x=540, y=760, r=420, o=0.5, c="#7aa2ff"), {"kind": "moon", "x": 540, "y": 760, "color": "#f4f1ff", "color2": "#0d1330", "r": 150},
   txt("PART 4", y=400, size=170, col="#f4f1ff", glow="#7aa2ff", panel=False), txt("WHY SHIVA WEARS THE MOON", y=1640, size=76, col="#ffcf5c", glow=None, at=T("why") - t)])
END = words[-1]["e"] + 1.4; scenes = []
for i, (at, k) in enumerate(S):
    k["dur"] = round((S[i + 1][0] if i + 1 < len(S) else END) - at, 3); assert k["dur"] > 0.3, (i, at, k["dur"]); scenes.append(k)
hit = lambda tok, n=1, v=0.7: {"src": "audio/sfx_hit.mp3", "at": T(tok, n) - 0.1, "vol": v}
sfx = [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.5}] + [hit(s, 1, 0.8) for s in toks] + [hit(s, 2, 0.6) for s in ("Na", "Ma", "Shi", "Va", "Ya")] + [{"src": "audio/sfx_bell_low.mp3", "at": T("and") - 0.1, "vol": 0.7}, {"src": "audio/sfx_boom.mp3", "at": T("In") - 0.1, "vol": 0.7}]
props = {"fixedText": True, "palette": "glow", "header": {"text": "SHIVA · PART 3"}, "captions": {"style": "serif", "words": words, "y": 1440, "size": 86, "max": 4}, "audio": {"vo": "audio/reel6_vo.mp3", "voAt": LEAD, "music": "audio/music_temple.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
(D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes; longest", max(s["dur"] for s in scenes), "s; mean", round(sum(s["dur"] for s in scenes) / len(scenes), 2))
