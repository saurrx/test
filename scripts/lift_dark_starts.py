#!/usr/bin/env python3
"""Stop scenes from opening on 1-2 near-black frames: any non-temple scene with no always-on glow gets a soft glow from frame 0,
and "fade" transitions into such scenes become cuts.  lift_dark_starts.py <reel.json> [...]   (edits in place, prints what changed)"""
import json, sys
ACC = {"glow": "#ffb648", "night": "#7aa2ff", "clay": "#ffcf8a", "dusk": "#ff9a5c", "storm": "#9fb6ff", "blood": "#ff5a2a"}
for path in sys.argv[1:]:
    p = json.load(open(path)); n = 0
    for s in p["scenes"]:
        if (s.get("bg") or {}).get("kind") == "temple": continue
        L = s.setdefault("layers", [])
        if any(l.get("kind") == "glowdot" and not l.get("at") and l.get("enter") == "none" for l in L): continue
        pal = s.get("palette") or p.get("palette") or "glow"
        L.insert(0, {"kind": "glowdot", "x": 540, "y": 900, "r": 760, "color2": ACC.get(pal, "#ffb648"), "opacity": 0.5, "enter": "none"}); n += 1
        if s.get("trans") == "fade": s["trans"] = "cut"
    json.dump(p, open(path, "w"), ensure_ascii=False); print(path, "scenes lifted:", n, "of", len(p["scenes"]))
