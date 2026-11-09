#!/usr/bin/env python3
"""Reel 2: the Pinaka bow (original script, Hindi, flat/Warli lane + varied scenes, 64 s). Applies P1 (60-90 s), P6/P10/P11
(stakes headline over a focal image on frame 1), P8 (ends on a part-2 hook)."""
import json
from pathlib import Path
D = Path(__file__).parent; C, DK, Y, INK = "#ffe9c4", "#2b0f06", "#ffcf5c", "#12081f"
words = json.load(open(D / "audio/vo.words.json"))
LEAD = 0.5  # P4: half a second of picture, headline and sound before the first word
for w in words: w["s"] = round(w["s"] + LEAD, 3); w["e"] = round(w["e"] + LEAD, 3)
def T(tok, n=1):
    k = 0
    for w in words:
        if w["w"].strip("।,?.") == tok.strip("।,?."):
            k += 1
            if k == n: return w["s"]
    raise KeyError(tok)
def txt(t, x=540, y=330, size=150, col=C, at=0, enter="slam", glow="#ff6a1f", **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": "pop", "color": col, "glow": glow, "at": at, "textEnter": enter, "width": 1000, **k}
def band(y=330, h=300, o=0.8, col=DK): return {"kind": "rect", "x": 540, "y": y, "w": 1080, "h": h, "color": col, "opacity": o, "enter": "none"}
def fig(**k): return {"kind": "figure", "x": 540, "y": 1100, "s": 2.4, "enter": "none", **k}
border = lambda y, rot=0: {"kind": "border", "x": 540, "y": y, "rot": rot}
hills = lambda col=INK, y=1560: {"kind": "hills", "x": 540, "y": y, "color": col, "enter": "none"}
S = []
def sc(at, **k): k.setdefault("bg", {"kind": "linear"}); S.append((at, k))
# 1 hook: 5,000 men (headline inside the frame, over the crowd)
sc(0.0, cam={"z0": 1.2, "z1": 1.0}, layers=[{"kind": "glowdot", "x": 540, "y": 760, "r": 380, "color2": Y, "opacity": 0.75, "enter": "none"}, {"kind": "bow", "x": 590, "y": 760, "s": 0.78, "color": "#ffe08a", "color2": "#fff", "glow": False, "enter": "none"},
   {"kind": "crowd", "x": 540, "y": 1640, "count": 32, "cols": 16, "gap": 64, "rowGap": 70, "s": 0.55, "stagger": 0.2, "anim": "walk", "enter": "none"}, txt("5,000 आदमी हारे", y=380, size=140)])
# 2 ...to pull ONE bow
t = T("सिर्फ़") - 0.1; sc(t, trans="punch", cam={"x0": -50, "x1": 50}, layers=[{"kind": "chest", "x": 720, "y": 900, "s": 0.9, "roll": 2.5, "enter": "slide_r", "move": {"x": -70}}, {"kind": "rope", "x": 150, "y": 880, "len": 280},
   {"kind": "crowd", "x": 190, "y": 860, "count": 6, "cols": 6, "gap": 62, "pose": "pull", "anim": "strain", "s": 0.95, "enter": "none"}, border(1180), txt("1 धनुष", y=330, size=170, at=T("एक") - t)])
# 3 this was Pinaka
t = T("यह") - 0.1; sc(t, trans="flash", palette="dusk", bg={"kind": "radial", "cy": 42}, dust=True, cam={"z0": 1.0, "z1": 1.16}, layers=[{"kind": "rays", "x": 540, "y": 800, "opacity": 0.24}, {"kind": "glowdot", "x": 560, "y": 800, "r": 420, "color2": Y, "opacity": 0.7, "enter": "fade"}, {"kind": "bow", "x": 600, "y": 800, "s": 1.05, "color": "#ffe08a", "color2": "#fff", "enter": "pop"},
   txt("पिनाक", y=400, size=200, col="#fff1dd", at=T("पिनाक") - t)])
# 4 Mahadev's own bow: night, mountain
t = T("स्वयं") - 0.1; sc(t, trans="fade", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.12, "z1": 1.0}, layers=[{"kind": "moon", "x": 800, "y": 380, "color": "#f4f1ff", "color2": "#0d1330", "r": 80}, {"kind": "mountain", "x": 540, "y": 1250, "s": 1.5, "color": "#0d1230", "color2": "#dfe6ff", "enter": "none"},
   {"kind": "glowdot", "x": 520, "y": 560, "r": 240, "color2": "#7aa2ff", "enter": "fade"}, {"kind": "bow", "x": 540, "y": 560, "s": 0.42, "color": "#ffe08a", "color2": "#fff", "glow": False, "enter": "pop", "at": 0.3}, {"kind": "rings", "x": 520, "y": 560, "color": "#7aa2ff", "at": 0.4, "count": 3, "max": 500, "width": 8, "enter": "none"}, txt("महादेव", y=1640, size=150, col="#f4f1ff", glow="#7aa2ff", at=T("महादेव") - t)])
# 5 Janak's iron chest on eight wheels
t = T("राजा") - 0.1; e8 = T("आठ") - t
sc(t, trans="punch", cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "palace", "x": 540, "y": 560, "s": 1.0, "color": C, "color2": "#7a2e12", "enter": "none"}, {"kind": "chest", "x": 540, "y": 1080, "s": 1.15, "roll": 0, "color": "#3a2a22", "color2": C, "enter": "rise"},
   {"kind": "rings", "x": 300, "y": 1150, "at": e8, "count": 2, "max": 220, "color": Y, "enter": "none"}, {"kind": "rings", "x": 780, "y": 1150, "at": e8 + 0.1, "count": 2, "max": 220, "color": Y, "enter": "none"}, txt("8 पहिये", y=1640, size=130, at=e8)])
# 6 the vow -> Sita
t = T("और") - 0.1; si = T("सीता") - t
sc(t, trans="fade", cam={"z0": 1.08, "z1": 1.0}, layers=[border(215), {"kind": "throne", "x": 300, "y": 980, "s": 1.4, "color": "#5a1f0c", "enter": "none"}, fig(x=300, y=930, s=2.3, crown=True, pose="point"),
   {"kind": "bow", "x": 560, "y": 1210, "s": 0.4, "rot": 90, "color": DK, "color2": DK, "glow": False, "enter": "none"}, {"kind": "glowdot", "x": 800, "y": 900, "r": 230, "color2": Y, "at": si, "enter": "fade"}, fig(x=800, y=950, s=2.1, prop="bun", at=si, enter="pop"),
   txt("प्रण", y=420, size=160, at=T("प्रण") - t, until=si - 0.2), txt("सीता", y=420, x=800, size=140, at=si)])
# 7 kings came from every land
t = T("देश") - 0.1; sc(t, trans="punch", palette="dusk", bg={"kind": "horizon"}, cam={"x0": 60, "x1": -60}, layers=[{"kind": "sun", "x": 800, "y": 620, "r": 150, "color": Y}, hills(),
   {"kind": "crowd", "x": 380, "y": 1240, "count": 5, "cols": 5, "gap": 200, "s": 1.9, "color": INK, "crown": True, "anim": "walk", "enter": "none", "move": {"x": 240}}, {"kind": "birds", "x": 100, "y": 380, "color": INK, "count": 6, "enter": "none"}])
# 8 no one could even move it
t = T("कोई") - 0.1; sc(t, trans="cut", cam={"z0": 1.05, "z1": 1.0}, layers=[{"kind": "bow", "x": 540, "y": 1210, "s": 0.5, "rot": 90, "color": DK, "color2": DK, "glow": False, "enter": "none"},
   fig(x=250, y=1010, s=1.9, crown=True, pose="lift", anim="tremble", until=0.8), fig(x=250, y=1010, s=1.9, crown=True, pose="fall", at=0.8),
   fig(x=540, y=1010, s=1.9, crown=True, pose="lift", anim="tremble", until=1.4), fig(x=540, y=1010, s=1.9, crown=True, pose="fall", at=1.4),
   fig(x=830, y=1010, s=1.9, crown=True, pose="lift", anim="tremble", until=2.0), fig(x=830, y=1010, s=1.9, crown=True, pose="fall", at=2.0), {"kind": "cross", "x": 540, "y": 520, "color": "#ff3b30", "size": 150, "width": 34, "at": 2.1, "enter": "none"}])
# 9 the sage arrives with a prince
t = T("फिर") - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "sun", "x": 300, "y": 700, "r": 170, "color": Y}, {"kind": "mandir", "x": 820, "y": 1200, "s": 0.7, "color": INK, "color2": Y, "enter": "none"}, hills(),
   fig(x=250, y=1320, s=2.6, color=INK, prop="staff", anim="walk", move={"x": 150}), fig(x=470, y=1370, s=2.1, color=INK, crown=True, anim="walk", move={"x": 150})])
# 10 RAM
t = T("राम") - 0.15; sc(t, trans="flash", palette="dusk", bg={"kind": "horizon"}, cam={"z0": 1.25, "z1": 1.35}, layers=[{"kind": "sun", "x": 540, "y": 760, "r": 300, "color": Y}, hills(), fig(x=540, y=1230, s=3.6, color=INK, crown=True, pose="stand"), txt("राम", y=430, size=240, col="#fff1dd")])
# 11 lifted it like a flower
t = T("उसने") - 0.1; sc(t, trans="cut", palette="dusk", bg={"kind": "radial", "cy": 40}, dust=True, cam={"z0": 1.5, "z1": 1.7, "y0": -260, "y1": -330}, layers=[{"kind": "rays", "x": 540, "y": 700, "opacity": 0.25}, {"kind": "glowdot", "x": 540, "y": 760, "r": 380, "color2": Y, "opacity": 0.7, "enter": "none"}, fig(x=540, y=1300, s=3.3, color=INK, crown=True, pose="lift"),
   {"kind": "bow", "x": 540, "y": 1100, "s": 0.6, "rot": 90, "color": "#ffe08a", "color2": "#fff", "glow": False, "enter": "none", "move": {"y": -230, "over": 1.4}}, txt("फूल जैसा", y=560, size=110, at=T("फूल") - t, enter="pop")])
# 12 drew the string... and it broke
t = T("प्रत्यंचा", 2) - 0.1; br = T("टूट") - t
sc(t, trans="punch", palette="dusk", bg={"kind": "horizon"}, cam={"z0": 1.1, "z1": 1.3, "shakeAt": br, "shake": 36}, layers=[{"kind": "sun", "x": 540, "y": 760, "r": 260, "color": Y}, hills(), fig(x=430, y=1300, s=3.3, color=INK, crown=True, pose="draw"),
   {"kind": "bow", "x": 640, "y": 1060, "s": 0.62, "color": INK, "color2": "#fff", "draw": 0.9, "breakAt": int(br * 30), "enter": "none"}, {"kind": "bolt", "x": 260, "y": 0, "color": "#fff", "at": br, "until": br + 0.8, "enter": "none"}, {"kind": "bolt", "x": 820, "y": 0, "color": "#fff", "at": br + 0.15, "until": br + 0.9, "seed": 5, "enter": "none"}])
# 13 a sound like lightning; the whole court shook
t = T("आवाज़") - 0.1; sc(t, trans="flash", palette="storm", bg={"kind": "radial", "cy": 40}, cam={"z0": 1.0, "z1": 1.12, "shakeAt": 0.1, "shake": 30}, layers=[{"kind": "bolt", "x": 540, "y": 0, "color": "#9fe3ff", "len": 1000, "enter": "none", "until": 2.2}, {"kind": "rings", "x": 540, "y": 900, "color": "#9fe3ff", "count": 6, "every": 12, "max": 1200, "enter": "none"},
   {"kind": "crowd", "x": 540, "y": 1230, "count": 14, "cols": 7, "gap": 140, "rowGap": 150, "s": 1.2, "color": "#cfe6f5", "anim": "tremble", "enter": "none"}, txt("बिजली", y=400, size=190, col="#eef6ff", glow="#9fe3ff", at=T("बिजली") - t)])
# 14 the sound travelled far
t = T("पर", 3) - 0.1; sc(t, trans="fade", palette="night", bg={"kind": "linear"}, stars=True, cam={"x0": -90, "x1": 90}, layers=[{"kind": "mountain", "x": 880, "y": 1200, "s": 1.1, "color": "#0d1230", "color2": "#dfe6ff", "enter": "none"}, hills("#070b1c", 1500),
   {"kind": "wave", "x": 300, "y": 760, "color": "#7aa2ff", "w": 900, "amp": 120, "fade": 400, "enter": "fade", "move": {"x": 420}}, {"kind": "rings", "x": 120, "y": 760, "color": "#7aa2ff", "count": 5, "every": 16, "max": 1300, "width": 8, "enter": "none"}])
# 15 a warrior who, 21 times...
t = T("एक", 3) - 0.1; n21 = T("इक्कीस") - t
sc(t, trans="cut", palette="blood", bg={"kind": "radial", "cy": 55}, dust=True, cam={"z0": 1.0, "z1": 1.18}, layers=[{"kind": "fire", "x": 540, "y": 1560, "color": "#ff5a2a", "color2": "#ffd24a", "w": 900, "h": 420, "enter": "fade"}, {"kind": "mountain", "x": 540, "y": 1380, "s": 1.0, "color": "#0a0202", "color2": "#3a0c06", "enter": "none"},
   fig(x=540, y=830, s=3.0, color="#0a0202", prop="axe", pose="stand"), txt("#", x=540, y=330, size=260, col="#ffe9d6", glow="#ff5a2a", at=n21, count=[1, 21, 22], enter="pop"), txt("बार", x=820, y=380, size=90, col="#ffe9d6", at=n21 + 0.5, enter="fade")])
# 16 PARASHURAM
t = T("परशुराम") - 0.15; sc(t, trans="flash", palette="blood", bg={"kind": "radial", "cy": 45}, cam={"z0": 1.3, "z1": 1.45, "shakeAt": 0.1, "shake": 24}, layers=[{"kind": "rays", "x": 540, "y": 800, "opacity": 0.3, "color": "#ff5a2a"}, fig(x=540, y=1100, s=4.2, color="#0a0202", prop="axe", pose="stand"),
   txt("परशुराम", y=400, size=190, col="#ffe9d6", glow="#ff5a2a")])
# 17 marching to Mithila in rage
t = T("और", 3) - 0.1; sc(t, trans="cut", palette="blood", bg={"kind": "horizon"}, cam={"x0": -70, "x1": 70}, layers=[{"kind": "fire", "x": 200, "y": 1500, "color": "#ff5a2a", "color2": "#ffd24a", "w": 500, "h": 520, "enter": "none"}, hills("#0a0202"),
   fig(x=360, y=1280, s=3.0, color="#0a0202", prop="axe", anim="walk", move={"x": 380}), {"kind": "palace", "x": 900, "y": 1180, "s": 0.4, "color": "#0a0202", "color2": "#7a1408", "enter": "none"}])
# 18 what happened next? follow for part 2
t = T("आगे") - 0.1; sc(t, trans="flash", palette="blood", bg={"kind": "radial", "cy": 50}, dust=True, cam={"z0": 1.08, "z1": 1.0}, layers=[{"kind": "bow", "x": 540, "y": 900, "s": 0.7, "rot": 90, "color": "#0a0202", "color2": "#ffd24a", "breakAt": 0, "enter": "none"},
   txt("आगे क्या हुआ?", y=400, size=150, col="#ffe9d6", glow="#ff5a2a"), txt("भाग 2 · FOLLOW", y=1620, size=120, col="#ffd24a", glow="#ff5a2a", at=T("भाग") - t)])
END = 64.6 + LEAD; scenes = []
for i, (at, k) in enumerate(S):
    k["dur"] = round((S[i + 1][0] if i + 1 < len(S) else END) - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [s["dur"] for s in scenes]
sfx = [{"src": "audio/sfx_hit.mp3", "at": 0.0, "vol": 0.9}, {"src": "audio/sfx_hit.mp3", "at": T("सिर्फ़") - 0.1, "vol": 0.7}, {"src": "audio/sfx_boom.mp3", "at": T("पिनाक"), "vol": 0.8}, {"src": "audio/sfx_bell_low.mp3", "at": T("सीता"), "vol": 0.5},
       {"src": "audio/sfx_whoosh.mp3", "at": T("फिर") - 0.2, "vol": 0.5}, {"src": "audio/sfx_boom.mp3", "at": T("राम") - 0.1, "vol": 0.9}, {"src": "audio/sfx_riser.mp3", "at": T("टूट") - 2.0, "vol": 0.5}, {"src": "audio/sfx_crack.mp3", "at": T("टूट"), "vol": 1.0},
       {"src": "audio/sfx_crack.mp3", "at": T("आवाज़"), "vol": 0.8}, {"src": "audio/sfx_boom.mp3", "at": T("परशुराम") - 0.1, "vol": 1.0}, {"src": "audio/sfx_hit.mp3", "at": T("आगे") - 0.1, "vol": 0.8}]
props = {"palette": "clay", "header": {"text": "रामायण · भाग 1", "color": "#ffcf5c"}, "captions": {"style": "pop", "words": words, "y": 1440, "max": 3}, "audio": {"vo": "audio/reel2_vo.mp3", "voAt": LEAD, "music": "audio/music_epic.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
(D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes", [s["dur"] for s in scenes])
