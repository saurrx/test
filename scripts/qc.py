#!/usr/bin/env python3
"""Automatic quality checks for a rendered reel or hook.  qc.py <video.mp4> [props.json] [--final]
Writes <video>.qc.json and prints one line: PASS/FAIL, failed checks, key numbers. --final adds 1080x1920 and loudness gates."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import analyze_reel as A

def frame_gray(path, t, w=270, h=480):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(h, w).astype(np.float32) / 255 if len(raw) == w * h else None

def lin(c): return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def loud(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s*(-?[\d.]+) LUFS", r); p = re.findall(r"Peak:\s*(-?[\d.]+) dBFS", r)
    return (float(i[-1]) if i else None, float(p[-1]) if p else None)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; final = "--final" in sys.argv
    v = Path(args[0]); props = json.load(open(args[1])) if len(args) > 1 else {}
    m = A.probe(v); d = m["duration"]; mo = A.hook_and_motion(v, Path("/tmp")); cuts = A.cuts(v)
    words = (props.get("captions") or {}).get("words") or []
    checks, nums = {}, {"duration": round(d, 2), "cuts": len(cuts), "cuts_per_10s": round(10 * len(cuts) / d, 2), "view_changes_per_10s": mo.get("view_changes_per_10s"),
                        "motion_mean": mo.get("motion_mean"), "motion_first3s": mo.get("motion_first3s"), "still_seconds": mo.get("still_seconds")}
    per = mo.get("motion_per_s", [])
    checks["moves_in_first_second"] = bool(per) and per[0] >= 0.5
    checks["no_long_still"] = mo.get("still_seconds", 0) <= max(1, 0.08 * d)
    first_change = min([c for c in cuts + mo.get("view_changes", []) if c > 0.2] or [99]); nums["first_visual_change_s"] = first_change
    checks["visual_change_by_3s"] = first_change <= 3.0
    f0 = frame_gray(v, 0.05); nums["first_frame_luma"] = round(float(f0.mean()), 3) if f0 is not None else None
    checks["first_frame_not_black"] = f0 is not None and f0.mean() >= 0.06 and (f0 > 0.5).mean() >= 0.004
    if words:
        nums["first_word_s"] = words[0]["s"]; checks["speaks_by_0.5s"] = words[0]["s"] <= 0.5
        speech = sum(w["e"] - w["s"] for w in words); span = words[-1]["e"] - words[0]["s"]
        nums["wpm"] = round(60 * len(words) / max(span, 1)); checks["pace_120_to_200_wpm"] = 120 <= nums["wpm"] <= 200 or len(words) < 8
        gaps = [words[i + 1]["s"] - words[i]["e"] for i in range(len(words) - 1)]; nums["max_gap_s"] = round(max(gaps), 2) if gaps else 0
        checks["no_dead_air_over_1.5s"] = nums["max_gap_s"] <= 1.5
        checks["voice_not_cut_off"] = words[-1]["e"] <= d + 0.05
        y = (props.get("captions") or {}).get("y", 1240); checks["caption_in_safe_area"] = 260 <= y <= 1500
        # legibility: inside the caption band, bright text pixels vs the typical background
        ratios = []
        for w in words[:: max(1, len(words) // 6)][:6]:
            g = frame_gray(v, min(d - 0.05, (w["s"] + w["e"]) / 2 + 0.1))
            if g is None: continue
            band = g[int((y - 110) / 4): int((y + 110) / 4), 20:250]; L = lin(band)
            ratios.append((np.percentile(L, 97) + 0.05) / (np.median(L) + 0.05))
        nums["caption_contrast"] = round(float(np.median(ratios)), 1) if ratios else None
        checks["caption_contrast_ge_4.5"] = bool(ratios) and nums["caption_contrast"] >= 4.5
    if m.get("audio"):
        I, P = loud(v); nums["lufs"] = I; nums["peak_db"] = P
        if final: checks["loudness_-16_to_-12"] = I is not None and -16 <= I <= -12; checks["peak_below_-1"] = P is not None and P <= -0.9
    elif final: checks["has_audio"] = False
    if final: checks["is_1080x1920"] = (m["width"], m["height"]) == (1080, 1920)
    failed = [k for k, ok in checks.items() if not ok]
    out = {"video": str(v), "pass": not failed, "failed": failed, "checks": {k: bool(x) for k, x in checks.items()}, "numbers": nums}
    Path(str(v) + ".qc.json").write_text(json.dumps(out, indent=1))
    print("PASS" if not failed else "FAIL", v.name, failed, {k: nums[k] for k in ("duration", "cuts", "first_visual_change_s", "caption_contrast", "wpm", "lufs") if k in nums})

if __name__ == "__main__": main()
