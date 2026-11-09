#!/usr/bin/env python3
"""Reel 1: "You ring the temple bell wrong" (original, glow lane, 62 s). Applies P1 (60-90 s), P4, P5, P6 (frame-1 headline).
Usage: build.py [hook]   -> makes/reel1_bell/reel.json (or hook.json = first 6.6 s)"""
import json, sys
from pathlib import Path
D = Path(__file__).parent; G, W, DARK, RED = "#ffb648", "#fff4dc", "#1a0f08", "#ff3b30"
words = json.load(open(D / "audio/vo.words.json"))
def T(tok, n=1):  # start time of the n-th occurrence of a word
    k = 0
    for w in words:
        if w["w"].strip(".,?:") == tok.strip(".,?:"):  # case-sensitive: "It" != "it", "Three." != "three,"
            k += 1
            if k == n: return w["s"]
    raise KeyError(tok)
def bell(**k): return {"kind": "bell", "x": 540, "y": 760, "s": 1.25, "color": DARK, "color2": G, "swing": 12, "speed": 4, "enter": "none", **k}
def glow(y=800, r=520, o=0.5, **k): return {"kind": "glowdot", "x": 540, "y": y, "r": r, "color2": G, "opacity": o, "enter": "none", **k}
def person(**k): return {"kind": "person", "x": 540, "y": 1680, "s": 1.05, "pose": "stand", "color": "#0c0705", "color2": G, "enter": "none", **k}
def txt(t, x=540, y=400, size=130, font="serif", col=W, at=0, enter="fade", **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": font, "color": col, "glow": G, "at": at, "textEnter": enter, **k}
def step(n): return txt(str(n), x=170, y=330, size=300, font="serif", col=W, enter="slam")
temple = lambda idol="none", lamps=2, g=1.5: {"kind": "temple", "idol": idol, "lamps": lamps, "glow": g}
rad = lambda cy=45: {"kind": "radial", "cy": cy}

S = []  # (start_time, scene)
def sc(at, **k): S.append((at, k))
# --- hook: headline on frame 1, three shots in 2.7 s
sc(0.0, bg=temple(g=1.9), dust=True, cam={"z0": 1.28, "z1": 1.16, "y0": -60, "y1": -60}, layers=[glow(y=700), bell(swing=20, speed=3.4, y=720, s=1.1),
   txt("YOU RING IT WRONG", y=300, size=150, font="pop", col=W, enter="slam", width=980, glow="#ff6a1f", at=0.0)])
sc(1.55, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.0, "z1": 1.06, "shakeAt": 0.2, "shake": 18}, layers=[glow(y=700), bell(swing=20, speed=3.4, y=700, s=1.1),
   {"kind": "cross", "x": 540, "y": 740, "color": RED, "size": 250, "at": 0.15, "enter": "none"}])
# --- most of us hit it three, four times and walk in
t = T("Most"); sc(t - 0.1, trans="flash", bg=temple(g=1.6), dust=True, cam={"z0": 1.05, "z1": 1.0}, layers=[glow(y=640, r=420), bell(y=600, s=0.95, swing=26, speed=2.2),
   person(x=330, y=1660, s=1.1, pose="ring", until=T("and") - t + 0.2), person(x=330, y=1660, s=1.1, pose="stand", at=T("and") - t + 0.2, move={"x": 700, "over": 1.0}),
   txt("1", x=800, y=700, size=150, at=T("hit") - t, until=T("three,") - t, enter="pop"), txt("2", x=800, y=700, size=150, at=T("three,") - t - 0.25, until=T("three,") - t + 0.15, enter="pop"),
   txt("3", x=800, y=700, size=150, at=T("three,") - t + 0.15, until=T("four") - t, enter="pop"), txt("4", x=800, y=700, size=150, at=T("four") - t, until=T("and") - t + 0.2, enter="pop")])
# --- not a doorbell for God
t = T("But"); sc(t - 0.1, trans="fade", bg=temple("murti", 2, 1.2), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[
   {"kind": "rect", "x": 540, "y": 430, "w": 250, "h": 330, "rx": 40, "color": "#2a1a10", "at": T("doorbell") - t - 0.3, "enter": "pop"},
   {"kind": "glowdot", "x": 540, "y": 430, "r": 70, "color2": W, "at": T("doorbell") - t - 0.3, "enter": "pop"},
   {"kind": "cross", "x": 540, "y": 430, "color": RED, "size": 170, "width": 34, "at": T("doorbell") - t + 0.15, "enter": "none"}])
# --- there is a mantra for it
t = T("There"); sc(t - 0.1, trans="fade", bg=rad(46), dust=True, cam={"z0": 1.15, "z1": 1.0}, layers=[{"kind": "yantra", "x": 540, "y": 850, "r": 430, "draw": 2.2}, txt("MANTRA", y=850, size=120, at=T("mantra") - t, enter="fade")])
# --- the mantra itself, in Devanagari
t = T("Aagamaartham"); sc(t - 0.15, trans="flash", bg=rad(42), dust=40, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "rays", "x": 540, "y": 780, "opacity": 0.14}, {"kind": "yantra", "x": 540, "y": 720, "r": 500, "draw": 0.1, "opacity": 0.3},
   txt("आगमार्थं तु देवानां", y=560, size=132, col=W, at=0.1, enter="fade", width=1000), txt("गमनार्थं तु रक्षसाम्", y=860, size=132, col=G, at=T("Gamanaartham") - t, enter="fade", width=1000),
   {"kind": "trail", "shape": "line", "y": 710, "r": 400, "from": 0.2, "to": 1.6, "width": 5}])
# --- let the divine come in
t = T("It"); sc(t - 0.1, trans="fade", bg=rad(40), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "rays", "x": 540, "y": 520, "opacity": 0.3, "count": 18}, glow(y=520, r=420, o=0.8),
   {"kind": "trail", "shape": "rise", "x": 540, "y": 900, "r": 420, "from": T("divine") - t - 0.4, "to": T("in.", 2) - t + 0.5, "width": 12}, person(y=1700, s=1.25, pose="pray")])
# --- let the darkness leave
t = T("Let", 1) if False else T("darkness") - 0.5; sc(t, trans="cut", palette="storm", bg=rad(50), cam={"z0": 1.1, "z1": 1.0}, layers=[
   {"kind": "birds", "x": 300, "y": 700, "color": "#0b1016", "count": 9, "s": 2.2, "enter": "none", "move": {"x": 700, "y": -500}}, {"kind": "birds", "x": 100, "y": 1000, "color": "#0b1016", "count": 7, "s": 1.6, "enter": "none", "move": {"x": 800, "y": -600}},
   person(y=1700, s=1.25, pose="pray", color="#05080c", color2="#9fe3ff"), {"kind": "moon", "x": 820, "y": 420, "color": "#dfe9f5", "color2": "#141c26", "r": 90, "enter": "fade"}])
# --- the temple way (title card)
t = T("So"); sc(t - 0.1, trans="flash", bg=temple("murti", 3, 1.3), dust=True, cam={"z0": 1.2, "z1": 1.05}, layers=[{"kind": "rect", "x": 540, "y": 760, "w": 1080, "h": 470, "color": "#000", "opacity": 0.72, "enter": "none"}, {"kind": "border", "x": 540, "y": 560, "color": G}, {"kind": "border", "x": 540, "y": 960, "color": G, "rot": 180},
   txt("THE TEMPLE WAY", y=760, size=128, at=T("temple", 2) - t - 0.2, enter="slam", width=980)])
# --- ONE: stop at the door, empty your hands
t = T("One."); sc(t - 0.1, trans="punch", bg=temple(g=1.5), dust=True, cam={"z0": 1.0, "z1": 1.08}, layers=[glow(y=700, r=420, o=0.35), bell(y=560, s=0.8, swing=1.5), step(1), person(y=1690, s=1.15, pose="stand"),
   txt("STOP", x=820, y=420, size=110, font="pop", col=G, at=T("Stop") - t, enter="pop")])
# --- TWO: ring it once, right hand
t = T("Two."); strike = T("once.") - t
sc(t - 0.1, trans="punch", bg=temple(g=1.7), dust=True, cam={"z0": 1.0, "z1": 1.1, "shakeAt": strike + 0.1, "shake": 16}, layers=[glow(y=640, r=440), bell(y=600, s=0.95, swing=1, strikeAt=int(strike * 30)), step(2),
   person(x=330, y=1660, s=1.1, pose="ring")])
sc(T("once.") - 0.12, trans="punch", bg=temple(g=2.0), dust=True, cam={"z0": 1.75, "z1": 1.6, "y0": -330, "y1": -330, "shakeAt": 0.12, "shake": 14}, layers=[glow(y=640, r=480, o=0.7), bell(y=600, s=0.95, swing=1, strikeAt=3),
   {"kind": "rings", "x": 540, "y": 780, "color": G, "at": 0.12, "count": 6, "every": 8, "max": 900, "enter": "none"}, txt("ONCE", x=540, y=1010, size=120, font="pop", col=G, at=0.15, enter="slam")])
# --- THREE: don't walk; seven seconds; stand till the sound is gone
t = T("Three."); c7 = T("seven") - t
sc(t - 0.1, trans="punch", bg=temple(g=1.4), dust=True, cam={"z0": 1.08, "z1": 1.0}, layers=[glow(y=640, r=420, o=0.4), bell(y=600, s=0.95, swing=2.5, speed=9), step(3), person(y=1690, s=1.15, pose="stand"), {"kind": "wave", "x": 540, "y": 980, "color": G, "at": 2.2, "fade": 190, "w": 940, "amp": 110, "enter": "fade"},
   {"kind": "rings", "x": 540, "y": 760, "color": G, "at": 0.4, "count": 9, "every": 24, "max": 1100, "width": 8, "enter": "none"},
   txt("#s", x=830, y=430, size=170, font="serif", col=W, at=c7 - 0.2, count=[1, 7, 150], enter="pop")])
# --- sound cuts your thoughts; silence is the real darshan
t = T("Tradition"); sil = T("silence") - t
sc(t - 0.1, trans="fade", bg=rad(40), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[person(y=1720, s=1.45, pose="pray"),
   {"kind": "trail", "shape": "scribble", "x": 540, "y": 800, "r": 300, "from": 0.2, "to": sil - 0.3, "width": 7, "seed": 4, "fadeAt": sil - 0.2, "color": "#ff8a3c"},
   {"kind": "rings", "x": 540, "y": 800, "color": W, "at": sil - 0.25, "count": 2, "max": 900, "enter": "none"},
   {"kind": "yantra", "x": 540, "y": 760, "r": 360, "at": sil, "draw": 1.6}, txt("SILENCE", y=300, size=130, at=sil, enter="fade")])
# --- FOUR: step in, right foot first
t = T("Four."); sc(t - 0.1, trans="punch", bg=temple("murti", 3, 1.6), dust=True, cam={"z0": 1.0, "z1": 1.22}, layers=[step(4), person(x=540, y=1760, s=1.3, pose="pray", move={"y": -90, "s": 0.9})])
# --- never meant to wake God
t = T("The", 5) if False else T("never") - 0.9; sc(t, trans="fade", bg=temple("murti", 2, 0.9), dust=True, cam={"z0": 1.25, "z1": 1.32, "y0": -200, "y1": -200}, layers=[])
# --- it was meant to wake YOU
t = T("It", 2) - 0.1; you = T("you.") - t
sc(t, trans="cut", bg=rad(42), dust=40, cam={"z0": 1.0, "z1": 1.18, "shakeAt": you, "shake": 14}, layers=[{"kind": "rays", "x": 540, "y": 700, "opacity": 0.2, "enter": "fade"}, glow(y=700, r=460, o=0.6), {"kind": "yantra", "x": 540, "y": 700, "r": 420, "draw": 1.2},
   {"kind": "wave", "x": 540, "y": 700, "color": G, "fade": 400, "w": 700, "amp": 60, "enter": "fade"}, person(y=1740, s=1.5, pose="pray"), {"kind": "rings", "x": 540, "y": 760, "color": G, "at": you, "count": 3, "max": 1100, "enter": "none"}, txt("YOU", y=700, size=260, font="pop", col=W, at=you, enter="slam", glow="#ff6a1f")])
# --- CTA: ring it once, count the seconds, comment the number
t = T("Tomorrow,") - 0.1; st = T("once,", 3) - t
sc(t, trans="flash", bg=temple(g=1.8), dust=True, cam={"z0": 1.1, "z1": 1.0}, layers=[glow(y=820), bell(y=800, s=0.9, swing=1, strikeAt=int(st * 30)), {"kind": "rings", "x": 540, "y": 960, "color": G, "at": st, "count": 8, "every": 18, "max": 1100, "width": 8, "enter": "none"},
   txt("1 STOP   2 RING ONCE", y=230, size=66, at=0.2, enter="fade", width=1000), txt("3 STAND TILL SILENT   4 RIGHT FOOT", y=330, size=52, at=0.5, enter="fade", width=1040),
   txt("#s ?", x=860, y=640, size=150, font="serif", col=W, at=T("count") - t, count=[1, 9, 110], enter="pop"), txt("COMMENT THE NUMBER", y=1580, size=84, font="pop", col=G, at=T("Comment") - t, enter="slam", width=1000)])
END = 62.3
scenes = []
for i, (at, k) in enumerate(S):
    nxt = S[i + 1][0] if i + 1 < len(S) else END; k["dur"] = round(nxt - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [s["dur"] for s in scenes]
sfx = [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.55}, {"src": "audio/sfx_hit.mp3", "at": 1.55, "vol": 0.8}, {"src": "audio/sfx_whoosh.mp3", "at": T("There") - 0.3, "vol": 0.4}, {"src": "audio/sfx_riser.mp3", "at": T("Aagamaartham") - 2.0, "vol": 0.3},
       {"src": "audio/sfx_boom.mp3", "at": T("So") - 0.1, "vol": 0.6}, {"src": "audio/sfx_hit.mp3", "at": T("One.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_hit.mp3", "at": T("Two.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_bell_low.mp3", "at": T("once."), "vol": 0.9},
       {"src": "audio/sfx_hit.mp3", "at": T("Three.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_hit.mp3", "at": T("Four.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_boom.mp3", "at": T("you."), "vol": 0.8}, {"src": "audio/sfx_bell_low.mp3", "at": T("once,", 3), "vol": 0.9}]
props = {"palette": "glow", "captions": {"style": "serif", "words": words, "y": 1250, "size": 86, "max": 4}, "audio": {"vo": "audio/reel1_vo.mp3", "music": "audio/music_temple.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
if len(sys.argv) > 1 and sys.argv[1] == "hook":
    cut = T("But") - 0.1; hs = []; acc = 0
    for s in scenes:
        if acc >= cut: break
        hs.append(s); acc += s["dur"]
    props = {**props, "scenes": hs, "captions": {**props["captions"], "words": [w for w in words if w["s"] < cut]}}
    (D / "hook.json").write_text(json.dumps(props, ensure_ascii=False)); print("hook", round(acc, 2), "s")
else:
    (D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes", [s["dur"] for s in scenes])
