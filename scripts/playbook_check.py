#!/usr/bin/env python3
"""Check a reel against the playbook rules that can be checked mechanically.
  playbook_check.py <props.json> [<video.mp4>]     (the video adds the measured rules via its .qc.json or a fresh analysis)
Prints one line per rule: OK / MISS, the rule id, and the measured value."""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
props = json.load(open(sys.argv[1])); video = sys.argv[2] if len(sys.argv) > 2 else None
words = (props.get("captions") or {}).get("words") or []; scenes = props["scenes"]; dur = sum(s["dur"] for s in scenes)
out = []
def rule(pid, ok, what, val): out.append((pid, bool(ok), what, val))
rule("P1", 60 <= dur <= 90, "length 60-90 s", round(dur, 1))
rule("P4", bool(words) and 0.3 <= words[0]["s"] <= 1.0, "0.3-1 s beat before the first word", words[0]["s"] if words else None)
first = scenes[0].get("layers", [])
rule("P6", any(l.get("kind") == "text" and l.get("at", 0) <= 0.15 for l in first), "headline on frame 1", [l.get("text") for l in first if l.get("kind") == "text"][:1])
focal = {"bow", "bell", "lingam", "sun", "mandir", "trishul", "thali", "diya", "bolt", "doorway", "flower", "conch"}
rule("P11", any(l.get("kind") in focal for l in first), "headline over one strong focal image", [l["kind"] for l in first if l.get("kind") in focal][:2])
rule("P8", bool(props.get("header")) and bool(re.search(r"part|भाग", props["header"]["text"], re.I)), "labelled as part of a series", (props.get("header") or {}).get("text"))
last_texts = " ".join(str(l.get("text", "")) for l in scenes[-1].get("layers", []) if l.get("kind") == "text") + " " + " ".join(w["w"] for w in words[-12:])
rule("P8b", bool(re.search(r"part\s*\d|part (two|three)|भाग", last_texts, re.I)), "ends on a hook for the next part", None)
rule("P15", bool((props.get("audio") or {}).get("vo")) and len(words) > 40, "voice-led", len(words))
longest = max(s["dur"] for s in scenes); rule("P16", longest <= 6.0 and dur / len(scenes) <= 4.0, "new picture at least every 6 s (ideally 3-4 s)", f"longest {longest:.1f} s, mean {dur / len(scenes):.1f} s")
rule("P18", not re.search(r"comment", last_texts, re.I), "ending is not comment-bait", None)
y = (props.get("captions") or {}).get("y", 1240); rule("P5", 260 <= y <= 1500, "captions in the safe area", y)
if video:
    qc = Path(video + ".qc.json")
    if not qc.exists(): subprocess.run([sys.executable, "-I", str(Path(__file__).parent / "qc.py"), video, sys.argv[1]], capture_output=True)
    n = json.loads(qc.read_text())["numbers"]; q = json.loads(qc.read_text())
    rule("P16m", (n.get("view_changes_per_10s") or 0) >= 1.6, "measured visual changes per 10 s >= 1.6 (hit median)", n.get("view_changes_per_10s"))
    rule("P5m", (n.get("caption_contrast") or 0) >= 4.5, "caption contrast >= 4.5", n.get("caption_contrast"))
    rule("QC", q["pass"], "all automatic quality checks", q["failed"])
for pid, ok, what, val in out: print(("OK  " if ok else "MISS"), pid.ljust(5), what, "|", val)
print(f"{sum(ok for _, ok, _, _ in out)}/{len(out)} rules met")
