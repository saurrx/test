#!/usr/bin/env python3
"""Reel 5: "Five things you must never offer to Shiva" (original, English, glow lane with shaded objects, ~68 s, free voice).
Sequel to reel 3 (P8). Applies P1, P4 (lead-in), P6/P10/P11 (stakes headline over a focal image), P16 (a new picture every 2-4 s),
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
def hero(tok, n, kind, label, occ=1, **ik):  # big object + number + keyword
    t = T(tok, occ) - 0.1; sc(t, trans="punch", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[glow(), {"kind": "rays", "x": 540, "y": 880, "opacity": 0.14}, item(kind, **ik), step(n), txt(label, x=620, y=400, at=0.45)])
def banned(at, kind, label=None, v=0, **ik):  # four different "refused" pictures so no two verdict scenes look alike
    sm = ik.pop("s", None)
    if v == 0:    # small, crossed out beside the Shivling
        L = [glow(y=820, o=0.45), lingam(x=400, y=880, s=0.72), item(kind, **{"x": 800, "y": 820, "s": sm or 0.62, "enter": "none", **ik}), cross(x=800, y=820, size=170, width=36, at=0.25)]; kw = dict(bg=temple(g=1.6), cam={"z0": 1.0, "z1": 1.08, "shakeAt": 0.25, "shake": 12})
    elif v == 1:  # big, alone, on a blood-red ground, cross slams over it
        L = [glow(y=880, o=0.5, c=RED), item(kind, **{"s": (sm or 0.62) * 2.0, "enter": "none", **ik}), cross(y=880, size=420, width=54, at=0.25)]; kw = dict(palette="blood", bg=rad(46), cam={"z0": 1.12, "z1": 1.0, "shakeAt": 0.25, "shake": 16})
    elif v == 2:  # offered, then it falls away from the Shivling
        L = [glow(y=820, o=0.5), lingam(y=980, s=0.8), item(kind, **{"x": 540, "y": 560, "s": (sm or 0.62) * 0.9, "enter": "drop", "move": {"x": 380, "y": 900, "rot": 70, "over": 1.1}, "exit": "fade", **ik}), cross(x=540, y=600, size=200, width=38, at=0.2, until=0.9)]; kw = dict(bg=temple(g=1.8), cam={"z0": 1.25, "z1": 1.35, "y0": -40, "y1": -60})
    else:         # night, the object dims out under a cold moon
        L = [glow(y=880, o=0.35, c=BLUE), {"kind": "moon", "x": 860, "y": 330, "s": 0.5, "color": W, "enter": "none"}, item(kind, **{"s": (sm or 0.62) * 1.8, "enter": "none", "exit": "fade", **ik}), cross(y=880, size=380, width=50, at=0.35)]; kw = dict(**night, cam={"z0": 1.0, "z1": 1.1})
    if label: L.append(txt(label, y=520 if v == 2 else 400, at=0.3))
    sc(at, trans="cut", dust=True, layers=L, **kw)
# hook
sc(0.0, bg=temple(g=2.0), dust=True, cam={"z0": 1.28, "z1": 1.0, "y0": -60, "y1": 0}, layers=[glow(y=820, o=0.75), {"kind": "rays", "x": 540, "y": 860, "opacity": 0.16}, lingam(y=900, s=1.05), {"kind": "text", "text": "5", "x": 540, "y": 330, "size": 300, "font": "serif", "color": G, "glow": "#ff6a1f", "textEnter": "slam"}, txt("NEVER OFFER THESE TO SHIVA", y=560, size=112, at=0.12)])
sc(T("never") - 0.1, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.35, "z1": 1.45, "y0": -80, "y1": -80, "shakeAt": 0.3, "shake": 14}, layers=[glow(y=820), lingam(y=880),
   item("flower", x=250, y=640, s=0.45, enter="pop", at=0.1), item("conch", x=850, y=640, s=0.36, enter="pop", at=0.3), item("bowls", x=540, y=1240, s=0.5, enter="pop", at=0.5), cross(y=860, size=330, width=44, at=0.7)])
t = T("Most") - 0.1; sc(t, trans="fade", bg=temple("lingam", 1.5, 3), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "person", "x": 540, "y": 1700, "s": 1.15, "pose": "pray", "color": "#0c0705", "color2": G, "enter": "none"}, txt("AT LEAST 1 OF 5", y=400, at=T("least") - t - 0.2)])
# 1 ketaki
hero("One.", 1, "flower", "KETAKI FLOWER")
t = T("In") - 0.1; sc(t, trans="fade", **night, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "moon", "x": 820, "y": 380, "color": "#f4f1ff", "color2": "#0d1330", "r": 66}, glow(x=540, y=900, r=420, o=0.5, c="#7aa2ff"), item("flower", y=940, s=1.2, enter="none", color="#dfe6ff"),
   txt("IT LIED", y=400, col="#f4f1ff", glow="#7aa2ff", at=T("lied") - t)])
banned(T("Shiva", 3) - 0.1, "flower", "BANNED FOREVER", v=1)
# 2 tulsi
hero("Two.", 2, "tulsi", "TULSI", s=1.6)
t = T("Loved") - 0.1; sc(t, trans="fade", **night, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(y=820, r=460, o=0.5, c="#7aa2ff"), {"kind": "yantra", "x": 540, "y": 820, "r": 400, "draw": 0.9, "color": "#bfe0ff", "spin": 0.5}, item("tulsi", y=860, s=1.1, enter="none"), txt("VISHNU'S", y=400, col="#f4f1ff", glow="#7aa2ff", at=0.3)])
banned(T("But") - 0.1, "tulsi", "NOT ON THE SHIVLING", v=2)
# 3 turmeric and kumkum
hero("Three.", 3, "bowls", "TURMERIC · KUMKUM", s=1.5, y=920)
t = T("They") - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, stars=True, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "mandir", "x": 540, "y": 1150, "s": 1.0, "color": "#12081f", "color2": "#ffcf5c", "enter": "none"}, item("bowls", y=1560, s=0.7, enter="rise"), txt("FOR THE GODDESS", y=400, at=0.3)])
t = T("Shiva", 4) - 0.1; sc(t, trans="cut", **night, cam={"z0": 1.0, "z1": 1.12}, layers=[{"kind": "mountain", "x": 540, "y": 1330, "s": 1.3, "color": "#0d1230", "color2": "#dfe6ff", "enter": "none"}, glow(y=700, r=380, o=0.5, c="#7aa2ff"), {"kind": "trishul", "x": 540, "y": 740, "s": 0.8, "color": "#f4f1ff", "color2": "#7aa2ff", "enter": "rise"}, txt("THE ASCETIC", y=1650, col="#f4f1ff", glow="#7aa2ff", at=T("ascetic") - t)])
t = T("He") - 0.1; sc(t, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.5, "z1": 1.7, "y0": -160, "y1": -200}, layers=[glow(y=820), lingam(y=900, s=1.0), {"kind": "rings", "x": 540, "y": 770, "color": W, "at": T("ash") - t, "count": 2, "max": 260, "width": 8, "enter": "none"}, txt("ASH · SANDALWOOD", y=1420, size=58, at=T("ash") - t)])
# 4 conch
hero("Four.", 4, "conch", "CONCH WATER", s=1.25)
t = T("Shiva", 5) - 0.1; sc(t, trans="flash", palette="blood", bg={"kind": "radial", "cy": 46}, dust=True, cam={"z0": 1.0, "z1": 1.15, "shakeAt": 0.5, "shake": 22}, layers=[glow(y=820, r=520, o=0.6, c="#ff5a2a"), {"kind": "trishul", "x": 540, "y": 800, "s": 0.95, "color": "#ffe9d6", "color2": "#ff5a2a", "enter": "drop"},
   {"kind": "bolt", "x": 300, "y": 0, "color": "#ffd24a", "at": 0.5, "until": 1.6, "enter": "none"}, txt("SHANKHACHUDA", y=1650, size=96, col="#ffe9d6", glow="#ff5a2a", at=T("Shankhachuda") - t)])
banned(T("And", 1) - 0.1, "conch", "NO CONCH WATER", s=0.4)
# 5 broken rice
hero("Five.", 5, "rice", "BROKEN RICE", occ=2, s=1.7, broken=1)
t = T("Every") - 0.1; sc(t, trans="cut", bg=rad(46), dust=True, cam={"z0": 1.12, "z1": 1.0}, layers=[glow(), item("rice", s=1.7, enter="none"), {"kind": "rings", "x": 540, "y": 880, "color": G, "at": 0.4, "count": 2, "max": 600, "enter": "none"}, txt("WHOLE GRAINS ONLY", y=400, col=G, at=T("whole") - t - 0.3)])
t = T("A", 1) - 0.1; sc(t, trans="cut", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.08}, layers=[glow(y=880, o=0.5, c=RED), item("rice", s=1.7, enter="none", broken=1), cross(y=880, size=420, width=54, at=0.3)], palette="blood")
# what he accepts
t = T("So") - 0.1; sc(t, trans="flash", bg=temple(g=2.0, lamps=3), dust=True, cam={"z0": 1.15, "z1": 1.0}, layers=[glow(y=820), {"kind": "rays", "x": 540, "y": 820, "opacity": 0.18}, lingam(y=880, s=1.0), txt("WHAT DOES HE ACCEPT?", y=400, size=96, col=G, at=0.2)])
t = T("Plain") - 0.1; sc(t, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.3, "z1": 1.42, "y0": -60, "y1": -90}, layers=[glow(y=820), lingam(y=900, s=0.95, wet=1), {"kind": "lota", "x": 700, "y": 600, "s": 0.7, "color": "#b8652a", "color2": G, "tilt": 45, "drop": 130, "pourAt": 3, "thick": 8, "enter": "none"}, txt("PLAIN WATER", y=1400, size=76, col=G, at=0.2)])
t = T("A", 2) - 0.1; sc(t, trans="punch", bg=rad(46), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[glow(), {"kind": "belpatra", "x": 540, "y": 980, "s": 2.6, "enter": "pop"}, txt("3", x=860, y=640, size=200, font="serif", col=W, glow=G, at=T("three") - t, panel=False), txt("BEL LEAF", y=400, col=G, at=0.2)])
t = T("And", 2) - 0.1; sc(t, trans="fade", bg=rad(42), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(y=760, r=520, o=0.6), {"kind": "yantra", "x": 540, "y": 760, "r": 380, "draw": 1.0}, {"kind": "person", "x": 540, "y": 1700, "s": 1.45, "pose": "pray", "color": "#0c0705", "color2": G, "enter": "none"}, txt("A CALM MIND", y=400, col=G, at=T("calm") - t)])
# part 3 + recap to save
t = T("In", 2) - 0.1; sc(t, trans="flash", **night, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "mandir", "x": 540, "y": 1180, "s": 1.05, "color": "#090d22", "color2": "#ffcf5c", "enter": "none"}, {"kind": "moon", "x": 830, "y": 300, "color": "#f4f1ff", "color2": "#0d1330", "r": 60},
   txt("PART 3", y=420, size=180, col="#f4f1ff", glow="#7aa2ff", panel=False), txt("THE ONE MANTRA", y=640, size=84, col="#ffcf5c", glow=None, at=T("mantra") - t - 0.3)])
t = T("Follow.") - 0.1; rows5 = ["✕  KETAKI FLOWER", "✕  TULSI", "✕  TURMERIC · KUMKUM", "✕  CONCH WATER", "✕  BROKEN RICE"]
sc(t, trans="punch", bg=temple("none", 1.3, 2), dust=True, cam={"z0": 1.06, "z1": 1.0}, layers=[{"kind": "rect", "x": 540, "y": 800, "w": 940, "h": 900, "rx": 40, "color": "#000", "opacity": 0.8, "enter": "none"}, {"kind": "border", "x": 540, "y": 385, "color": G, "w": 860, "n": 14},
   {"kind": "text", "text": "NEVER OFFER TO SHIVA", "x": 540, "y": 520, "size": 56, "font": "serif", "color": G, "glow": None, "textEnter": "fade"}] +
   [{"kind": "text", "text": r, "x": 540, "y": 640 + i * 108, "size": 62, "font": "serif", "color": W, "glow": None, "at": 0.2 + i * 0.25, "textEnter": "fade"} for i, r in enumerate(rows5)] + [txt("SAVE THIS · FOLLOW FOR PART 3", y=1650, size=70, col=G, at=T("save") - t - 0.4)])
END = words[-1]["e"] + 1.4; scenes = []
for i, (at, k) in enumerate(S):
    k["dur"] = round((S[i + 1][0] if i + 1 < len(S) else END) - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [(i, s["dur"]) for i, s in enumerate(scenes)]
hit = lambda tok, n=1, v=0.7: {"src": "audio/sfx_hit.mp3", "at": T(tok, n) - 0.1, "vol": v}
sfx = [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.5}, hit("never", 1, 0.9), hit("One."), hit("Two."), hit("Three."), hit("Four."), hit("Five.", 2), {"src": "audio/sfx_crack.mp3", "at": T("Shiva", 5) + 0.4, "vol": 0.7},
       {"src": "audio/sfx_bell_low.mp3", "at": T("So"), "vol": 0.7}, {"src": "audio/sfx_boom.mp3", "at": T("In", 2) - 0.1, "vol": 0.7}, hit("Follow.")]
props = {"palette": "glow", "header": {"text": "SHIVA · PART 2"}, "captions": {"style": "serif", "words": words, "y": 1440, "size": 86, "max": 4}, "audio": {"vo": "audio/reel5_vo.mp3", "voAt": LEAD, "music": "audio/music_temple.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
(D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes; longest", max(s["dur"] for s in scenes), "s; mean", round(sum(s["dur"] for s in scenes) / len(scenes), 2))
