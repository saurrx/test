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
def person(**k): return {"kind": "person", "x": 540, "y": 1180, "s": 1.5, "pose": "stand", "color": "#0c0705", "color2": G, "enter": "none", **k}
def txt(t, x=540, y=400, size=130, font="serif", col=W, at=0, enter="fade", **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": font, "color": col, "glow": G, "at": at, "textEnter": enter, **k}
def step(n): return txt(str(n), x=170, y=330, size=300, font="serif", col=W, enter="slam")
temple = lambda idol="none", lamps=2, g=1.5: {"kind": "temple", "idol": idol, "lamps": lamps, "glow": g}
rad = lambda cy=45: {"kind": "radial", "cy": cy}

S = []  # (start_time, scene)
def sc(at, **k): S.append((at, k))
# --- hook: headline on frame 1, three shots in 2.7 s
sc(0.0, bg=temple(g=1.9), dust=True, cam={"z0": 1.5, "z1": 1.32, "y0": -120, "y1": -120}, layers=[glow(), bell(swing=20, speed=3.4, y=820),
   txt("YOU RING IT WRONG", y=300, size=150, font="pop", col=W, enter="slam", width=980, glow="#ff6a1f", at=0.0)])
sc(1.55, trans="punch", bg=temple(g=1.9), dust=True, cam={"z0": 1.0, "z1": 1.06, "shakeAt": 0.2, "shake": 18}, layers=[glow(), bell(swing=20, speed=3.4),
   {"kind": "cross", "x": 540, "y": 800, "color": RED, "size": 270, "at": 0.15, "enter": "none"}])
# --- most of us hit it three, four times and walk in
t = T("Most"); sc(t - 0.1, trans="flash", bg=temple(g=1.6), dust=True, cam={"z0": 1.05, "z1": 1.0}, layers=[glow(y=640, r=420), bell(y=600, s=0.95, swing=26, speed=2.2),
   person(x=430, y=1240, pose="ring", until=T("and") - t + 0.2), person(x=430, y=1240, pose="stand", at=T("and") - t + 0.2, move={"x": 520, "over": 1.0}),
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
t = T("Aagamaartham"); sc(t - 0.15, trans="flash", bg=rad(42), dust=40, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "rays", "x": 540, "y": 780, "opacity": 0.14}, {"kind": "yantra", "x": 540, "y": 780, "r": 470, "draw": 0.1, "opacity": 0.22},
   txt("आगमार्थं तु देवानां", y=640, size=112, col=W, at=0.1, enter="fade", width=1000), txt("गमनार्थं तु रक्षसाम्", y=900, size=112, col=G, at=T("Gamanaartham") - t, enter="fade", width=1000),
   {"kind": "trail", "shape": "line", "y": 770, "r": 380, "from": 0.2, "to": 1.6, "width": 5}])
# --- let the divine come in
t = T("It"); sc(t - 0.1, trans="fade", bg=rad(40), dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "rays", "x": 540, "y": 520, "opacity": 0.3, "count": 18}, glow(y=520, r=420, o=0.8),
   {"kind": "trail", "shape": "rise", "x": 540, "y": 900, "r": 420, "from": T("divine") - t - 0.4, "to": T("in.", 2) - t + 0.5, "width": 12}, person(y=1320, pose="pray")])
# --- let the darkness leave
t = T("Let", 1) if False else T("darkness") - 0.5; sc(t, trans="cut", palette="storm", bg=rad(50), cam={"z0": 1.1, "z1": 1.0}, layers=[
   {"kind": "birds", "x": 300, "y": 700, "color": "#0b1016", "count": 9, "s": 2.2, "enter": "none", "move": {"x": 700, "y": -500}}, {"kind": "birds", "x": 100, "y": 1000, "color": "#0b1016", "count": 7, "s": 1.6, "enter": "none", "move": {"x": 800, "y": -600}},
   person(y=1320, pose="pray", color="#05080c", color2="#9fe3ff")])
# --- the temple way (title card)
t = T("So"); sc(t - 0.1, trans="flash", bg=rad(46), dust=True, cam={"z0": 1.12, "z1": 1.0}, layers=[{"kind": "border", "x": 540, "y": 640, "color": G}, {"kind": "border", "x": 540, "y": 1060, "color": G, "rot": 180},
   txt("THE TEMPLE WAY", y=850, size=128, at=T("temple", 2) - t - 0.2, enter="slam", width=980)])
# --- ONE: stop at the door, empty your hands
t = T("One."); sc(t - 0.1, trans="punch", bg=temple(g=1.5), dust=True, cam={"z0": 1.0, "z1": 1.08}, layers=[glow(y=700, r=420, o=0.35), bell(y=560, s=0.8, swing=1.5), step(1), person(y=1260, s=1.6, pose="stand"),
   txt("STOP", x=820, y=420, size=110, font="pop", col=G, at=T("Stop") - t, enter="pop")])
# --- TWO: ring it once, right hand
t = T("Two."); strike = T("once.") - t
sc(t - 0.1, trans="punch", bg=temple(g=1.7), dust=True, cam={"z0": 1.0, "z1": 1.1, "shakeAt": strike + 0.1, "shake": 16}, layers=[glow(y=640, r=440), bell(y=600, s=0.95, swing=1, strikeAt=int(strike * 30)), step(2),
   person(x=430, y=1240, pose="ring"), {"kind": "rings", "x": 540, "y": 760, "color": G, "at": strike, "count": 5, "max": 1000, "enter": "none"}, txt("ONCE", x=820, y=420, size=110, font="pop", col=G, at=strike, enter="pop")])
# --- THREE: don't walk; seven seconds; stand till the sound is gone
t = T("Three."); c7 = T("seven") - t
sc(t - 0.1, trans="punch", bg=temple(g=1.4), dust=True, cam={"z0": 1.08, "z1": 1.0}, layers=[glow(y=640, r=420, o=0.4), bell(y=600, s=0.95, swing=2.5, speed=9), step(3), person(y=1260, s=1.6, pose="stand"),
   {"kind": "rings", "x": 540, "y": 760, "color": G, "at": 0.4, "count": 9, "every": 24, "max": 1100, "width": 8, "enter": "none"},
   txt("#s", x=830, y=430, size=170, font="serif", col=W, at=c7 - 0.2, count=[1, 7, 150], enter="pop")])
# --- sound cuts your thoughts; silence is the real darshan
t = T("Tradition"); sil = T("silence") - t
sc(t - 0.1, trans="fade", bg=rad(40), dust=True, cam={"z0": 1.0, "z1": 1.12}, layers=[person(y=1250, s=1.9, pose="pray"),
   {"kind": "trail", "shape": "scribble", "x": 540, "y": 720, "r": 260, "from": 0.2, "to": sil - 0.3, "width": 7, "seed": 4, "fadeAt": sil - 0.2, "color": "#ff8a3c"},
   {"kind": "rings", "x": 540, "y": 760, "color": W, "at": sil - 0.25, "count": 2, "max": 900, "enter": "none"},
   {"kind": "yantra", "x": 540, "y": 700, "r": 330, "at": sil, "draw": 1.6}, txt("SILENCE", y=330, size=120, at=sil, enter="fade")])
# --- FOUR: step in, right foot first
t = T("Four."); sc(t - 0.1, trans="punch", bg=temple("murti", 3, 1.6), dust=True, cam={"z0": 1.0, "z1": 1.22}, layers=[step(4), person(x=540, y=1500, s=1.5, pose="pray", move={"y": -170, "s": 0.86})])
# --- never meant to wake God
t = T("The", 5) if False else T("never") - 0.9; sc(t, trans="fade", bg=temple("murti", 2, 0.9), dust=True, cam={"z0": 1.25, "z1": 1.32, "y0": -200, "y1": -200}, layers=[])
# --- it was meant to wake YOU
t = T("It", 2) - 0.1; you = T("you.") - t
sc(t, trans="cut", bg=rad(42), dust=40, cam={"z0": 1.0, "z1": 1.18, "shakeAt": you, "shake": 14}, layers=[{"kind": "rays", "x": 540, "y": 760, "opacity": 0.26, "at": you, "enter": "fade"}, {"kind": "yantra", "x": 540, "y": 760, "r": 440, "at": you - 0.5, "draw": 0.9},
   person(y=1180, s=2.0, pose="pray"), {"kind": "rings", "x": 540, "y": 760, "color": G, "at": you, "count": 3, "max": 1100, "enter": "none"}, txt("YOU", y=330, size=220, font="pop", col=W, at=you, enter="slam", glow="#ff6a1f")])
# --- CTA: ring it once, count the seconds, comment the number
t = T("Tomorrow,") - 0.1; st = T("once,", 3) - t
sc(t, trans="flash", bg=temple(g=1.8), dust=True, cam={"z0": 1.1, "z1": 1.0}, layers=[glow(), bell(swing=1, strikeAt=int(st * 30)), {"kind": "rings", "x": 540, "y": 960, "color": G, "at": st, "count": 8, "every": 18, "max": 1100, "width": 8, "enter": "none"},
   txt("#s ?", y=330, size=200, font="serif", col=W, at=T("count") - t, count=[1, 9, 110], enter="pop"), txt("COMMENT THE NUMBER", y=1650, size=84, font="pop", col=G, at=T("Comment") - t, enter="slam", width=1000)])
END = 62.3
scenes = []
for i, (at, k) in enumerate(S):
    nxt = S[i + 1][0] if i + 1 < len(S) else END; k["dur"] = round(nxt - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [s["dur"] for s in scenes]
sfx = [{"src": "audio/sfx_bell.mp3", "at": 0.0, "vol": 0.55}, {"src": "audio/sfx_hit.mp3", "at": 1.55, "vol": 0.8}, {"src": "audio/sfx_whoosh.mp3", "at": T("There") - 0.3, "vol": 0.4}, {"src": "audio/sfx_riser.mp3", "at": T("Aagamaartham") - 2.0, "vol": 0.3},
       {"src": "audio/sfx_boom.mp3", "at": T("So") - 0.1, "vol": 0.6}, {"src": "audio/sfx_hit.mp3", "at": T("One.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_hit.mp3", "at": T("Two.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_bell_low.mp3", "at": T("once."), "vol": 0.9},
       {"src": "audio/sfx_hit.mp3", "at": T("Three.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_hit.mp3", "at": T("Four.") - 0.1, "vol": 0.7}, {"src": "audio/sfx_boom.mp3", "at": T("you."), "vol": 0.8}, {"src": "audio/sfx_bell_low.mp3", "at": T("once,", 3), "vol": 0.9}]
props = {"palette": "glow", "captions": {"style": "serif", "words": words, "y": 1400, "size": 76, "max": 4}, "audio": {"vo": "audio/reel1_vo.mp3", "music": "audio/music_temple.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
if len(sys.argv) > 1 and sys.argv[1] == "hook":
    cut = T("But") - 0.1; hs = []; acc = 0
    for s in scenes:
        if acc >= cut: break
        hs.append(s); acc += s["dur"]
    props = {**props, "scenes": hs, "captions": {**props["captions"], "words": [w for w in words if w["s"] < cut]}}
    (D / "hook.json").write_text(json.dumps(props, ensure_ascii=False)); print("hook", round(acc, 2), "s")
else:
    (D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes", [s["dur"] for s in scenes])
