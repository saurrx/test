#!/usr/bin/env python3
"""Reel 3: "You pour water on the Shivling wrong" (original, English, glow lane with varied scenes, 67 s, free edge-tts voice).
Applies P1 (60-90 s), P6/P11 (frame-1 headline over a focal image), P8 (labelled part 1, ends on part 2), P14 lead (Shiva topic)."""
import json
from pathlib import Path
D = Path(__file__).parent; G, W, DARK, RED, BLUE = "#ffb648", "#fff4dc", "#120a07", "#ff3b30", "#9fe3ff"
words = json.load(open(D / "audio/vo.words.json"))
LEAD = 0.5  # P4: half a second of picture, headline and sound before the first word
for w in words: w["s"] = round(w["s"] + LEAD, 3); w["e"] = round(w["e"] + LEAD, 3)
def T(tok, n=1):
    k = 0
    for w in words:
        if w["w"].strip(".,?:") == tok.strip(".,?:"):
            k += 1
            if k == n: return w["s"]
    raise KeyError(tok)
def txt(t, x=540, y=330, size=130, font="serif", col=W, at=0, enter="fade", glow=G, **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": font, "color": col, "glow": glow, "at": at, "textEnter": enter, "width": 1000, **k}
def glow(x=540, y=800, r=480, o=0.5, **k): return {"kind": "glowdot", "x": x, "y": y, "r": r, "color2": G, "opacity": o, "enter": "none", **k}
def lingam(**k): return {"kind": "lingam", "x": 540, "y": 800, "s": 1.0, "color": DARK, "color2": G, "enter": "none", **k}
def lota(**k): return {"kind": "lota", "x": 700, "y": 330, "s": 0.9, "color": "#b8652a", "color2": G, "enter": "none", **k}
def person(**k): return {"kind": "person", "x": 540, "y": 1690, "s": 1.1, "pose": "stand", "color": "#0c0705", "color2": G, "enter": "none", **k}
def step(n): return txt(str(n), x=150, y=420, size=260, enter="slam")
def cross(x=540, y=700, size=220, at=0, **k): return {"kind": "cross", "x": x, "y": y, "color": RED, "size": size, "at": at, "enter": "none", **k}
temple = lambda idol="none", g=1.5, lamps=2: {"kind": "temple", "idol": idol, "lamps": lamps, "glow": g}
rad = lambda cy=45: {"kind": "radial", "cy": cy}
S = []
def sc(at, **k): S.append((at, k))
# hook: headline over the lit Shivling, a careless broken pour, a red cross on "wrong"
sc(0.0, bg=temple(g=1.9), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[glow(y=820), lingam(y=860, s=0.9), lota(x=720, y=560, s=0.7, broken=1, drop=250, pourAt=4, thick=16),
   txt("YOU POUR IT WRONG", y=360, size=128, font="pop", enter="slam", glow="#ff6a1f")])
sc(T("Shivling") - 0.15, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.5, "z1": 1.62, "y0": -150, "y1": -150, "shakeAt": T("wrong") - T("Shivling") + 0.2, "shake": 16}, layers=[glow(y=820), lingam(y=860, s=0.9), lota(x=720, y=560, s=0.7, broken=1, drop=250, pourAt=0, thick=16),
   cross(y=800, size=230, at=T("wrong") - T("Shivling") + 0.2)])
# they splash it, and leave
t = T("They") - 0.1; sc(t, trans="punch", bg=temple(g=1.5), dust=True, cam={"z0": 1.0, "z1": 1.06}, layers=[glow(y=720, o=0.35), lingam(y=760, s=0.8), lota(x=690, y=420, s=0.6, broken=1, drop=260, pourAt=2, thick=16, until=T("and") - t),
   person(x=420, y=1700, at=0, move={"x": 700, "over": 2.2}), txt("SPLASH", x=800, y=420, size=96, font="pop", col=BLUE, glow=BLUE, at=0.1, enter="pop", until=T("and") - t)])
# the Shiva Purana describes something else
t = T("The") - 0.1; sc(t, trans="fade", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "moon", "x": 800, "y": 400, "color": "#f4f1ff", "color2": "#0d1330", "r": 70}, {"kind": "trishul", "x": 540, "y": 760, "s": 0.95, "color": "#f4f1ff", "color2": "#7aa2ff", "enter": "rise"},
   txt("SHIVA PURANA", y=1640, size=110, col="#f4f1ff", glow="#7aa2ff", at=T("Shiva") - t)])
# a thin unbroken stream: jal-dhaara (close shot)
t = T("A") - 0.1; sc(t, trans="flash", bg=rad(55), dust=True, cam={"z0": 1.1, "z1": 1.22}, layers=[glow(y=820, r=520), lingam(y=900, s=1.0, wet=1), lota(x=690, y=600, s=0.7, drop=120, pourAt=6, thick=9),
   txt("JAL-DHAARA", y=400, size=120, at=T("jal-dhaara") - t, enter="slam")])
# the temple way (title over the sanctum)
t = T("Here") - 0.1; sc(t, trans="flash", bg=temple("lingam", 1.3, 3), dust=True, cam={"z0": 1.2, "z1": 1.05}, layers=[{"kind": "rect", "x": 540, "y": 700, "w": 1080, "h": 440, "color": "#000", "opacity": 0.72, "enter": "none"}, {"kind": "border", "x": 540, "y": 510, "color": G}, {"kind": "border", "x": 540, "y": 890, "color": G, "rot": 180},
   txt("THE TEMPLE WAY", y=700, size=128, at=T("temple") - t - 0.2, enter="slam")])
# ONE: a copper pot, not steel
t = T("One.") - 0.1; st = T("Tradition") - t
sc(t, trans="punch", bg=rad(42), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[step(1), glow(y=760, r=520, o=0.7), {"kind": "lota", "x": 540, "y": 780, "s": 2.0, "tilt": 0, "pourAt": 999, "color": "#b8652a", "color2": G, "enter": "pop", "until": st, "exit": "fade"},
   txt("COPPER", y=1650, size=130, font="pop", col=G, at=T("copper") - t, enter="slam", until=st),
   {"kind": "lota", "x": 540, "y": 780, "s": 1.7, "tilt": 0, "pourAt": 999, "color": "#9aa3ab", "color2": "#9fb8c8", "at": st, "enter": "pop"}, cross(y=760, size=260, at=T("steel") - t), txt("NOT STEEL", y=1650, size=120, font="pop", col="#cfd8df", glow="#9fb8c8", at=st, enter="slam")])
# TWO: never standing tall above him; sit or bend low
t = T("Two.") - 0.1; sit = T("Sit") - t
sc(t, trans="punch", bg=temple(g=1.5), dust=True, cam={"z0": 1.0, "z1": 1.06}, layers=[step(2), glow(x=700, y=900, r=380, o=0.4), lingam(x=720, y=980, s=0.6),
   person(x=360, y=980, s=1.55, pose="stand", until=sit), lota(x=520, y=520, s=0.55, drop=300, pourAt=20, until=sit), cross(x=420, y=760, size=230, at=T("standing") - t + 0.3, until=sit),
   person(x=360, y=1420, s=1.2, pose="stand", at=sit), lota(x=540, y=900, s=0.55, tilt=40, drop=110, pourAt=8, thick=8, at=sit), txt("SIT", x=800, y=420, size=150, font="pop", col=G, at=sit, enter="slam")])
# THREE: face north (seen from above)
t = T("Three.") - 0.1; sc(t, trans="punch", bg=rad(48), dust=True, cam={"z0": 1.12, "z1": 1.0}, layers=[step(3), {"kind": "lingamtop", "x": 540, "y": 860, "s": 1.0, "color": DARK, "color2": G, "enter": "pop"},
   {"kind": "needle", "x": 540, "y": 860, "color": W, "color2": G, "angle": 0, "from": 140, "len": 300, "at": T("Face") - t, "enter": "none"}, txt("FACE NORTH", y=1650, size=120, font="pop", col=G, at=T("north") - t, enter="slam"), txt("N", x=540, y=440, size=80, at=T("north") - t)])
# FOUR: pour slowly, one thin stream, Om Namah Shivaya until the pot is empty; don't break the stream
t = T("Four.") - 0.1; om = T("Om") - t; db = T("Do") - t
sc(t, trans="punch", bg=temple(g=1.7), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[step(4), glow(y=820, o=0.45), lingam(y=860, s=0.85, wet=1), lota(x=690, y=420, s=0.62, tilt=35, drop=250, pourAt=30, thick=7, until=om - 0.2),
   {"kind": "belpatra", "x": 330, "y": 1040, "s": 0.8, "rot": -20, "at": 1.4, "enter": "pop"}, {"kind": "belpatra", "x": 760, "y": 1060, "s": 0.7, "rot": 25, "at": 1.7, "enter": "pop"}])
sc(T("Say") - 0.15, trans="flash", bg=rad(52), dust=40, cam={"z0": 1.12, "z1": 1.25}, layers=[{"kind": "rays", "x": 540, "y": 860, "opacity": 0.2}, glow(y=860, r=520, o=0.7), lingam(y=920, s=1.0, wet=1), lota(x=690, y=620, s=0.7, tilt=45, drop=120, pourAt=0, thick=7),
   txt("ॐ नमः शिवाय", y=400, size=124, col=G, at=0.25, enter="fade"), {"kind": "wave", "x": 540, "y": 1660, "color": G, "w": 800, "amp": 40, "fade": 500, "enter": "fade"}])
sc(T("Do") - 0.1, trans="cut", bg=temple(g=1.6), dust=True, cam={"z0": 1.05, "z1": 1.0}, layers=[glow(y=820, o=0.45), lingam(y=860, s=0.85, wet=1), lota(x=690, y=420, s=0.62, tilt=45, drop=250, pourAt=0, thick=7, broken=1), cross(x=660, y=600, size=150, width=34, at=0.35),
   txt("DON'T BREAK IT", y=380, size=116, font="pop", enter="slam", glow="#ff6a1f")])
# FIVE: never a full circle; stop at the water channel and turn back (diagram from above)
t = T("And") - 0.1; stop = T("Stop") - t
sc(t, trans="punch", bg=rad(48), dust=True, cam={"z0": 1.0, "z1": 1.08}, layers=[step(5), {"kind": "lingamtop", "x": 540, "y": 860, "s": 0.85, "color": DARK, "color2": G, "enter": "none"},
   {"kind": "trail", "shape": "circle", "x": 540, "y": 860, "r": 400, "from": T("Never", 2) - t, "to": stop - 0.5, "width": 8, "fadeAt": stop - 0.3, "color": "#ff8a3c"}, cross(y=860, size=330, width=40, at=T("circle") - t + 0.3, until=stop - 0.1, opacity=0.9),
   {"kind": "halfcircle", "x": 540, "y": 860, "r": 400, "squash": 1, "turns": 0.47, "dur": 75, "color": G, "at": stop, "enter": "none"}, txt("TURN BACK", y=1650, size=120, font="pop", col=G, at=T("turn") - t, enter="slam")])
# why: the channel carries what was offered; you never step across it
t = T("Why?") - 0.1; stp = T("You") - t
sc(t, trans="fade", bg=rad(60), dust=True, cam={"z0": 1.5, "z1": 1.7, "x0": -200, "x1": -260, "y0": 120, "y1": 160}, layers=[glow(x=300, y=1000, r=420, o=0.5), lingam(y=900, s=1.0, wet=1), txt("WHY?", x=380, y=560, size=120, font="pop", enter="slam", until=1.0)])
sc(T("You") - 0.1, trans="cut", bg=rad(70), cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "rect", "x": 540, "y": 1010, "w": 1080, "h": 46, "color": "#3a2412", "enter": "none"}, {"kind": "river", "x": 540, "y": 990, "color": BLUE, "w": 1100, "rows": 1, "enter": "none"},
   {"kind": "feet", "x": 540, "y": 1650, "s": 1.25, "color": "#0c0705", "color2": G, "stepAt": 9999, "enter": "rise"}, cross(y=760, size=200, width=40, at=T("across") - T("You") + 0.1), txt("NEVER CROSS IT", y=400, size=116, font="pop", at=T("never", 1) - T("You"), enter="slam", glow="#ff6a1f")])
# part two tease
t = T("In") - 0.1; sc(t, trans="flash", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.1, "z1": 1.0}, layers=[{"kind": "mandir", "x": 540, "y": 1180, "s": 1.05, "color": "#090d22", "color2": "#ffcf5c", "enter": "none"}, {"kind": "moon", "x": 830, "y": 300, "color": "#f4f1ff", "color2": "#0d1330", "r": 60},
   txt("PART 2", y=420, size=190, font="pop", col="#f4f1ff", glow="#7aa2ff", at=T("part") - t, enter="slam"), {"kind": "belpatra", "x": 250, "y": 640, "s": 0.8, "at": T("offer") - t, "enter": "pop"}, cross(x=830, y=620, size=90, width=26, at=T("never", 2) - t)])
# follow + comment
t = T("Follow,") - 0.1; sc(t, trans="fade", bg=temple("lingam", 1.7, 3), dust=True, cam={"z0": 1.0, "z1": 1.15}, layers=[txt("FOLLOW FOR PART 2", y=380, size=96, font="pop", col=G, enter="slam")])
t = T("How") - 0.1; sc(t, trans="punch", bg=rad(46), dust=True, cam={"z0": 1.08, "z1": 1.0}, layers=[glow(y=700, r=520, o=0.6), {"kind": "yantra", "x": 540, "y": 700, "r": 380, "draw": 1.2, "opacity": 0.5},
   txt("# / 5 ?", y=700, size=260, at=0.1, count=[0, 5, 50], enter="pop"), txt("COMMENT YOUR NUMBER", y=1650, size=88, font="pop", col=G, at=T("Comment") - t, enter="slam")])
END = 67.6 + LEAD; scenes = []
for i, (at, k) in enumerate(S):
    k["dur"] = round((S[i + 1][0] if i + 1 < len(S) else END) - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [s["dur"] for s in scenes]
hit = lambda tok, n=1, v=0.7: {"src": "audio/sfx_hit.mp3", "at": T(tok, n) - 0.1, "vol": v}
sfx = [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.5}, hit("They"), {"src": "audio/sfx_whoosh.mp3", "at": T("The") - 0.3, "vol": 0.4}, {"src": "audio/sfx_boom.mp3", "at": T("Here") - 0.1, "vol": 0.6}, hit("One."), hit("Two."), hit("Three."), hit("Four."),
       {"src": "audio/sfx_bell_low.mp3", "at": T("Om"), "vol": 0.7}, hit("And"), {"src": "audio/sfx_boom.mp3", "at": T("In") - 0.1, "vol": 0.7}, hit("How")]
props = {"palette": "glow", "header": {"text": "SHIVA · PART 1"}, "captions": {"style": "serif", "words": words, "y": 1420, "size": 86, "max": 4}, "audio": {"vo": "audio/reel3_vo.mp3", "voAt": LEAD, "music": "audio/music_temple.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
(D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes", [s["dur"] for s in scenes])
