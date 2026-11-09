#!/usr/bin/env python3
"""Reel 4: Ramayana part 2, Parashuram confronts Ram (original script, Hindi, flat/Warli lane, ~79 s, free edge-tts voice).
Sequel to reel 2 (P8). Applies P1, P4 (0.5 s lead-in), P10/P11 (stakes headline over a focal image), P15, P16."""
import json
from pathlib import Path
D = Path(__file__).parent; C, DK, Y, INK, RED, BL = "#ffe9c4", "#2b0f06", "#ffcf5c", "#12081f", "#0a0202", "#7aa2ff"
words = json.load(open(D / "audio/vo.words.json")); LEAD = 0.5
for w in words: w["s"] = round(w["s"] + LEAD, 3); w["e"] = round(w["e"] + LEAD, 3)
def T(tok, n=1):
    k = 0
    for w in words:
        if w["w"].strip("।,?.:") == tok.strip("।,?.:"):
            k += 1
            if k == n: return w["s"]
    raise KeyError(tok)
def txt(t, x=540, y=400, size=150, col=C, at=0, enter="slam", glow="#ff6a1f", **k): return {"kind": "text", "text": t, "x": x, "y": y, "size": size, "font": "pop", "color": col, "glow": glow, "at": at, "textEnter": enter, "width": 1000, **k}
def fig(**k): return {"kind": "figure", "x": 540, "y": 1100, "s": 2.4, "enter": "none", **k}
hills = lambda col=INK, y=1560: {"kind": "hills", "x": 540, "y": y, "color": col, "enter": "none"}
para = lambda **k: fig(**{"color": RED, "prop": "axe", **k})
ram = lambda **k: fig(**{"color": INK, "crown": True, **k})
vbow = lambda **k: {"kind": "bow", "x": 560, "y": 800, "s": 0.8, "color": "#bfe0ff", "color2": BL, "enter": "none", **k}
def name(t, x, y, col="#ffe9d6", at=0): return {"kind": "text", "text": t, "x": x, "y": y, "size": 64, "font": "pop", "color": col, "glow": None, "at": at, "textEnter": "fade", "width": 500, "panel": True}
S = []
def sc(at, **k): k.setdefault("bg", {"kind": "linear"}); S.append((at, k))
# 1 hook: Parashuram blocks Ram's path (stakes, two figures, lightning between them)
sc(0.0, palette="blood", bg={"kind": "radial", "cy": 50}, cam={"z0": 1.15, "z1": 1.0, "shakeAt": 0.5, "shake": 22}, layers=[{"kind": "bolt", "x": 540, "y": 520, "color": "#ffd24a", "len": 1100, "enter": "none", "until": 2.6}, {"kind": "fire", "x": 200, "y": 1560, "color": "#ff5a2a", "color2": "#ffd24a", "w": 520, "h": 420, "enter": "none"},
   para(x=250, y=1100, s=3.0), ram(x=830, y=1120, s=2.8, color="#fff1dd"), name("परशुराम", 250, 760), name("राम", 830, 760), txt("परशुराम vs राम", y=400, size=128, col="#ffe9d6", glow="#ff5a2a")])
# 2 the wedding party heads home
t = T("विवाह") - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, cam={"x0": -70, "x1": 70}, layers=[{"kind": "sun", "x": 780, "y": 640, "r": 160, "color": Y}, {"kind": "palace", "x": 220, "y": 1180, "s": 0.42, "color": INK, "color2": "#e2603a", "enter": "none"}, hills(),
   {"kind": "crowd", "x": 420, "y": 1260, "count": 6, "cols": 6, "gap": 150, "s": 1.6, "color": INK, "anim": "walk", "enter": "none", "move": {"x": 260}}, {"kind": "chest", "x": 240, "y": 1330, "s": 0.4, "roll": 3, "color": INK, "color2": "#e2603a", "enter": "none", "move": {"x": 260}}, {"kind": "birds", "x": 80, "y": 380, "color": INK, "count": 6, "enter": "none"}])
# 3 a storm rises, darkness falls
t = T("अचानक") - 0.1; sc(t, trans="flash", palette="storm", bg={"kind": "radial", "cy": 40}, cam={"z0": 1.0, "z1": 1.12, "shakeAt": 0.2, "shake": 26}, layers=[{"kind": "bolt", "x": 300, "y": 0, "color": "#9fe3ff", "len": 1000, "enter": "none", "until": 1.6}, {"kind": "bolt", "x": 800, "y": 0, "color": "#9fe3ff", "len": 900, "seed": 4, "at": 1.4, "enter": "none"},
   {"kind": "birds", "x": 300, "y": 700, "color": "#cfe6f5", "count": 9, "s": 1.8, "enter": "none", "move": {"x": -500, "y": -400}}, {"kind": "crowd", "x": 540, "y": 980, "count": 12, "cols": 6, "gap": 150, "rowGap": 150, "s": 1.15, "color": "#cfe6f5", "anim": "tremble", "enter": "none"}, txt("आँधी", y=400, size=190, col="#eef6ff", glow="#9fe3ff", at=T("आँधी") - t)])
# 4 and there stood Parashuram
t = T("और") - 0.1; sc(t, trans="cut", palette="blood", bg={"kind": "radial", "cy": 45}, dust=True, cam={"z0": 1.3, "z1": 1.45, "shakeAt": T("परशुराम", 2) - t, "shake": 24}, layers=[{"kind": "glowdot", "x": 540, "y": 900, "r": 520, "color2": "#ff5a2a", "opacity": 0.75, "enter": "none"}, {"kind": "fire", "x": 540, "y": 1700, "color": "#ff5a2a", "color2": "#ffd24a", "w": 1000, "h": 380, "enter": "none"}, {"kind": "rays", "x": 540, "y": 800, "opacity": 0.3, "color": "#ff5a2a"}, para(x=540, y=1040, s=3.9),
   txt("परशुराम", y=400, size=190, col="#ffe9d6", glow="#ff5a2a", at=T("परशुराम", 2) - t)])
# 5 axe on his shoulder, another bow in his hand
t = T("कंधे") - 0.1; sc(t, trans="punch", palette="blood", bg={"kind": "radial", "cy": 50}, dust=True, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "glowdot", "x": 330, "y": 900, "r": 480, "color2": "#ff5a2a", "opacity": 0.75, "enter": "none"}, {"kind": "fire", "x": 540, "y": 1700, "color": "#ff5a2a", "color2": "#ffd24a", "w": 1000, "h": 380, "enter": "none"}, para(x=330, y=1060, s=3.1), name("परशुराम", 330, 700), {"kind": "glowdot", "x": 760, "y": 860, "r": 300, "color2": BL, "at": T("हाथ") - t, "enter": "fade"}, vbow(x=790, y=860, s=0.7, at=T("हाथ") - t, enter="pop")])
# 6 "you broke Shiva's old bow; this is Vishnu's bow"
t = T("उन्होंने") - 0.1; vt = T("यह") - t
sc(t, trans="fade", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.0, "z1": 1.1}, layers=[{"kind": "bow", "x": 300, "y": 820, "s": 0.45, "rot": 90, "color": "#ffe08a", "color2": "#fff", "glow": False, "breakAt": 0, "enter": "none"}, txt("शिव", x=300, y=1120, size=90, col="#ffe08a", enter="fade", glow=None),
   {"kind": "glowdot", "x": 760, "y": 820, "r": 340, "color2": BL, "at": vt, "enter": "fade"}, vbow(x=790, y=820, s=0.85, at=vt, enter="pop"), txt("विष्णु का धनुष", y=400, size=130, col="#f4f1ff", glow=BL, at=T("विष्णु") - t)])
# 7 "string it, then fight me"
t = T("इस") - 0.1; yd = T("युद्ध") - t
sc(t, trans="punch", palette="blood", bg={"kind": "radial", "cy": 48}, cam={"z0": 1.0, "z1": 1.15, "shakeAt": yd, "shake": 28}, layers=[vbow(x=560, y=820, s=0.9), {"kind": "arrow", "x": 520, "y": 820, "color": "#fff1dd", "len": 520, "at": T("बाण") - t, "enter": "slide_l"}, txt("युद्ध", y=400, size=230, col="#ffe9d6", glow="#ff5a2a", at=yd)])
# 8 Dasharath trembles and pleads; Parashuram does not listen
t = T("राजा") - 0.1; sc(t, trans="fade", cam={"z0": 1.05, "z1": 1.0}, layers=[{"kind": "border", "x": 540, "y": 250}, fig(x=330, y=1000, s=2.5, crown=True, pose="pray", anim="tremble"), fig(x=800, y=960, s=2.8, color=DK, prop="axe"), name("दशरथ", 330, 700, C),
   {"kind": "cross", "x": 560, "y": 760, "color": "#ff3b30", "size": 120, "width": 30, "at": T("पर", 3) - t + 0.6, "enter": "none"}, txt("विनती", x=330, y=620, size=110, at=T("विनती") - t, enter="pop")])
# 9 Ram steps forward and takes the bow
t = T("राम", 2) - 0.1; sc(t, trans="flash", palette="dusk", bg={"kind": "horizon"}, cam={"z0": 1.0, "z1": 1.12}, layers=[{"kind": "sun", "x": 540, "y": 720, "r": 250, "color": Y}, hills(), ram(x=380, y=1300, s=3.2, anim="walk", move={"x": 160, "over": 2.0}), vbow(x=820, y=980, s=0.5, at=T("धनुष", 4) - t, enter="pop")])
# 10 strung in a moment; the arrow is drawn
t = T("एक", 3) - 0.1; sc(t, trans="punch", palette="dusk", bg={"kind": "radial", "cy": 42}, dust=True, cam={"z0": 1.15, "z1": 1.35}, layers=[{"kind": "rays", "x": 540, "y": 800, "opacity": 0.25}, ram(x=420, y=1300, s=3.3, pose="draw"), {"kind": "bow", "x": 640, "y": 1060, "s": 0.62, "color": "#bfe0ff", "color2": "#fff", "draw": 0.9, "enter": "none"},
   {"kind": "arrow", "x": 700, "y": 1060, "color": "#fff", "len": 300, "at": T("बाण", 2) - t, "enter": "fade"}, txt("एक पल", y=400, size=190, col="#fff1dd")])
# 11 "this arrow will not go in vain"
t = T("अब") - 0.1; sc(t, trans="cut", palette="night", bg={"kind": "radial", "cy": 50}, stars=True, cam={"z0": 1.2, "z1": 1.4}, layers=[{"kind": "rays", "x": 540, "y": 860, "opacity": 0.22, "color": BL}, {"kind": "glowdot", "x": 540, "y": 860, "r": 520, "color2": BL, "enter": "none"}, {"kind": "arrow", "x": 540, "y": 860, "s": 1.6, "color": "#fff", "len": 420, "enter": "slide_l"},
   {"kind": "rings", "x": 760, "y": 860, "color": BL, "at": 1.6, "count": 4, "every": 14, "max": 700, "width": 8, "enter": "none"}, txt("खाली नहीं जाएगा", y=400, size=110, col="#f4f1ff", glow=BL, at=T("खाली") - t)])
# 12 "which shall I destroy: your speed, or the worlds you won?"
t = T("बताइए") - 0.1; g1 = T("गति") - t; l1 = T("लोक") - t
sc(t, trans="fade", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.0, "z1": 1.06}, layers=[{"kind": "rect", "x": 540, "y": 900, "w": 6, "h": 900, "color": "#f4f1ff", "opacity": 0.4, "enter": "none"},
   {"kind": "glowdot", "x": 280, "y": 860, "r": 220, "color2": Y, "opacity": 0.5, "enter": "none"}, {"kind": "wave", "x": 280, "y": 860, "color": Y, "w": 420, "amp": 90, "fade": 900, "enter": "none"}, {"kind": "birds", "x": 150, "y": 640, "color": Y, "count": 4, "enter": "none"}, txt("गति", x=280, y=1120, size=130, col=Y, glow=Y, at=0.1, enter="pop"),
   {"kind": "glowdot", "x": 800, "y": 860, "r": 220, "color2": BL, "opacity": 0.6, "enter": "none"}, {"kind": "yantra", "x": 800, "y": 860, "r": 190, "draw": 1.5, "color": "#f4f1ff", "petals": 6, "triangles": 2}, txt("लोक", x=800, y=1120, size=130, col="#f4f1ff", glow=BL, at=0.3, enter="pop"), {"kind": "rings", "x": 280, "y": 860, "color": Y, "at": g1, "count": 2, "max": 320, "enter": "none"}, {"kind": "rings", "x": 800, "y": 860, "color": BL, "at": l1, "count": 2, "max": 320, "enter": "none"}, txt("क्या नष्ट करूँ?", y=400, size=110, col="#f4f1ff", glow=BL, at=0.2)])
# 13 Parashuram's glow drains; he understands this is Vishnu himself
t = T("परशुराम", 4) - 0.1; vs = T("विष्णु", 2) - t
sc(t, trans="fade", palette="night", bg={"kind": "radial", "cy": 40}, stars=True, cam={"z0": 1.0, "z1": 1.15}, layers=[{"kind": "rays", "x": 660, "y": 760, "opacity": 0.22, "color": BL, "at": vs - 0.6, "enter": "fade"}, {"kind": "yantra", "x": 660, "y": 760, "r": 400, "at": vs - 0.8, "draw": 1.2, "color": "#bfe0ff", "spin": 0.6},
   {"kind": "glowdot", "x": 660, "y": 800, "r": 420, "color2": BL, "opacity": 0.5, "enter": "none"}, ram(x=660, y=1220, s=3.4, color="#f4f1ff"), para(x=240, y=1200, s=1.9, color="#c9584a", pose="kneel"), txt("विष्णु", y=400, size=200, col="#f4f1ff", glow=BL, at=vs)])
# 14 "leave me my speed; take the worlds"
t = T("उन्होंने", 2) - 0.1; sc(t, trans="cut", palette="blood", bg={"kind": "radial", "cy": 55}, cam={"z0": 1.12, "z1": 1.0}, layers=[{"kind": "glowdot", "x": 800, "y": 820, "r": 360, "color2": BL, "opacity": 0.6, "enter": "none"}, ram(x=800, y=1100, s=3.0, color="#f4f1ff"), para(x=300, y=1160, s=2.8, color="#c9584a", pose="kneel"), name("परशुराम", 300, 800), name("राम", 800, 720), txt("लोक ले लो", y=400, size=130, col="#ffe9d6", glow="#ff5a2a", at=T("लोक", 2) - t)])
# 15 Ram lets the arrow fly
t = T("राम", 4) - 0.1; rel = T("छोड़") - t
sc(t, trans="punch", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.0, "z1": 1.1, "shakeAt": rel, "shake": 30}, layers=[{"kind": "arrow", "x": 200, "y": 860, "s": 1.3, "color": "#fff", "len": 420, "enter": "none", "at": rel, "move": {"x": 1400, "over": 0.5}},
   {"kind": "trail", "shape": "line", "x": 540, "y": 860, "r": 520, "from": rel, "to": rel + 0.4, "width": 10, "color": BL}, {"kind": "rings", "x": 900, "y": 860, "color": BL, "at": rel + 0.35, "count": 5, "every": 8, "max": 1100, "enter": "none"}, ram(x=200, y=1320, s=2.6, color="#f4f1ff", pose="draw")])
# 16 the warrior who won the earth 21 times bows his head and leaves
t = T("और", 4) - 0.1; sc(t, trans="fade", palette="dusk", bg={"kind": "horizon"}, cam={"x0": -60, "x1": 60}, layers=[{"kind": "sun", "x": 300, "y": 760, "r": 170, "color": Y}, {"kind": "mountain", "x": 820, "y": 1260, "s": 0.9, "color": INK, "color2": "#e2603a", "enter": "none"}, hills(),
   para(x=420, y=1330, s=2.6, color=INK, pose="kneel", until=T("लौट") - t), para(x=420, y=1300, s=2.6, color=INK, anim="walk", at=T("लौट") - t, move={"x": 380, "s": 0.6}), txt("#", x=540, y=420, size=230, col="#fff1dd", at=T("इक्कीस") - t, count=[1, 21, 20], enter="pop")])
# 17 part 3 tease
t = T("भाग") - 0.1; sc(t, trans="flash", palette="night", bg={"kind": "linear"}, stars=True, cam={"z0": 1.08, "z1": 1.0}, layers=[{"kind": "moon", "x": 820, "y": 380, "color": "#f4f1ff", "color2": "#0d1330", "r": 70}, {"kind": "tree", "x": 200, "y": 1250, "s": 2.0, "color": "#070b1c"}, {"kind": "tree", "x": 880, "y": 1330, "s": 1.7, "color": "#070b1c", "seed": 4}, hills("#070b1c", 1600),
   txt("भाग 3", y=420, size=220, col="#f4f1ff", glow=BL), txt("वनवास की असली वजह", y=900, size=100, col=Y, glow=Y, at=T("वनवास") - t, enter="pop"), txt("FOLLOW", y=1650, size=120, col="#f4f1ff", glow=BL, at=T("फ़ॉलो") - t)])
END = words[-1]["e"] + 1.3; scenes = []
for i, (at, k) in enumerate(S):
    k["dur"] = round((S[i + 1][0] if i + 1 < len(S) else END) - at, 3); scenes.append(k)
assert all(s["dur"] > 0.4 for s in scenes), [s["dur"] for s in scenes]
sfx = [{"src": "audio/sfx_crack.mp3", "at": 0.05, "vol": 0.9}, {"src": "audio/sfx_crack.mp3", "at": T("अचानक") + 0.1, "vol": 0.9}, {"src": "audio/sfx_boom.mp3", "at": T("परशुराम", 2), "vol": 1.0}, {"src": "audio/sfx_whoosh.mp3", "at": T("यह") - 0.1, "vol": 0.5}, {"src": "audio/sfx_boom.mp3", "at": T("युद्ध"), "vol": 0.9},
       {"src": "audio/sfx_hit.mp3", "at": T("राम", 2) - 0.1, "vol": 0.8}, {"src": "audio/sfx_riser.mp3", "at": T("एक", 3) - 0.3, "vol": 0.5}, {"src": "audio/sfx_bell_low.mp3", "at": T("विष्णु", 2), "vol": 0.7}, {"src": "audio/sfx_whoosh.mp3", "at": T("छोड़"), "vol": 0.9}, {"src": "audio/sfx_boom.mp3", "at": T("छोड़") + 0.35, "vol": 0.9}, {"src": "audio/sfx_hit.mp3", "at": T("भाग") - 0.1, "vol": 0.8}]
props = {"palette": "clay", "header": {"text": "रामायण · भाग 2", "color": Y}, "captions": {"style": "pop", "words": words, "y": 1440, "max": 3}, "audio": {"vo": "audio/reel4_vo.mp3", "voAt": LEAD, "music": "audio/music_epic.mp3", "musicVol": 0.2, "sfx": sfx}, "scenes": scenes}
(D / "reel.json").write_text(json.dumps(props, ensure_ascii=False)); print(len(scenes), "scenes", [s["dur"] for s in scenes])
