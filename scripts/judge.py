#!/usr/bin/env python3
"""Blind judging packets.
  judge.py pack <name> [--whole] [--judges N] <clip.mp4 | hook_strip.jpg> ...
      Builds judgments/<name>/j1..jN/ with A.jpg, B.jpg, ... (a different random lettering per judge) and key.json.
      Default strip = first 3 s at 4 fps (12 frames, 6x2). --whole = 12 frames spread over the whole clip.
  judge.py tally <name> "<ranking j1>" "<ranking j2>" ...      ranking like "C>A>B" (best first)
      Borda count across judges -> judgments/<name>/result.json, prints the order by clip.
  judge.py prompt <name> <j> [context]      prints the judge prompt for judge j"""
import json, random, string, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; J = ROOT / "judgments"

def strip(src, dst, whole):
    src = str(src)
    if src.endswith(".jpg"):  # analysis hook_strip.jpg: 12x1 of 270px frames -> 6x2
        vf = "split[a][b];[a]crop=iw/2:ih:0:0[t];[b]crop=iw/2:ih:iw/2:0[u];[t][u]vstack"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", vf, "-frames:v", "1", str(dst)], check=True)
    else:
        if whole:
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
            # frame 1 is the real opening (0.3 s), then 11 frames spread evenly (the old fps filter started ~d/24 in, hiding the opening)
            import tempfile; tmp = tempfile.mkdtemp(); times = [0.3] + [d * (i + 0.5) / 11.5 for i in range(1, 12)]
            for i, t in enumerate(times): subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{min(t, d - 0.2):.2f}", "-i", src, "-frames:v", "1", "-vf", "scale=270:480", f"{tmp}/{i:02d}.jpg"], check=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{tmp}/%02d.jpg", "-vf", "tile=6x2", "-frames:v", "1", str(dst)], check=True)
        else:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", "3", "-i", src, "-vf", "fps=4,scale=270:480,tile=6x2", "-frames:v", "1", str(dst)], check=True)

def pack(name, clips, judges, whole):
    d = J / name; d.mkdir(parents=True, exist_ok=True); key = {}
    rnd = random.Random(name)
    for j in range(1, judges + 1):
        order = clips[:]; rnd.shuffle(order); jd = d / f"j{j}"; jd.mkdir(exist_ok=True); key[f"j{j}"] = {}
        for old in jd.glob("*.jpg"): old.unlink()
        for letter, c in zip(string.ascii_uppercase, order):
            strip(ROOT / c if not Path(c).is_absolute() else c, jd / f"{letter}.jpg", whole); key[f"j{j}"][letter] = c
    (d / "key.json").write_text(json.dumps({"clips": clips, "whole": whole, "key": key}, indent=1))
    print("packed", name, len(clips), "clips x", judges, "judges ->", d)

def tally(name, rankings):
    d = J / name; k = json.loads((d / "key.json").read_text()); n = len(k["clips"]); score = {c: 0 for c in k["clips"]}; firsts = {c: 0 for c in k["clips"]}; per = []
    for j, r in enumerate(rankings, 1):
        letters = [x.strip().upper() for x in r.replace(",", ">").split(">") if x.strip()]
        names = [k["key"][f"j{j}"][l] for l in letters]; per.append(names)
        for pos, c in enumerate(names): score[c] += n - 1 - pos
        firsts[names[0]] += 1
    order = sorted(score, key=lambda c: (-score[c], -firsts[c]))
    res = {"name": name, "judges": len(rankings), "order": order, "borda": score, "first_place_votes": firsts, "per_judge": per}
    (d / "result.json").write_text(json.dumps(res, indent=1))
    for c in order: print(f"{score[c]:>3}  firsts={firsts[c]}  {c}")

def prompt(name, j, context=""):
    d = J / name / f"j{j}"; files = sorted(p.name for p in d.glob("*.jpg")); k = json.loads((J / name / "key.json").read_text())
    what = "12 frames spread evenly over the whole clip" if k["whole"] else "the first 3 seconds (12 frames, 4 per second)"
    print(f"""You are a blind judge of short vertical videos (Instagram Reels) for an Indian mythology / devotional story audience.
Read every image in {d} with the Read tool: {', '.join(files)}. Each image shows {what} of one clip, reading left to right, top row then bottom row.
Do not read any other file, do not run commands, do not look for which clip is which.
{context}
Rank ALL clips from best to worst on one question: which would make a viewer stop scrolling and keep watching?
Judge only what you can see: is the very first frame striking and readable, is there motion and change across the frames, is the text large, legible and intriguing, is the picture polished rather than amateur, does it create curiosity.
Reply in exactly this format, nothing else:
RANKING: <letters best to worst, like C>A>B>
WHY_BEST: <one sentence>
WHY_WORST: <one sentence>
FIX: <for the worst clip, the single most valuable fix, one sentence>""")

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "pack":
        whole = "--whole" in a; judges = int(a[a.index("--judges") + 1]) if "--judges" in a else 3
        clips = [x for i, x in enumerate(a[2:]) if not x.startswith("--") and a[2:][i - 1] != "--judges"]
        pack(a[1], clips, judges, whole)
    elif a[0] == "tally": tally(a[1], a[2:])
    elif a[0] == "prompt": prompt(a[1], int(a[2]), a[3] if len(a) > 3 else "")
