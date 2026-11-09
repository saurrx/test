#!/usr/bin/env python3
"""Judge calibration: can a blind judge tell a creator's hit from the same creator's flop using only the first 3 seconds?
  calib.py pack <name>            builds judgments/<name>/ with P01_A.jpg / P01_B.jpg ... (hit on a random side), lines.txt, key.json
  calib.py tally <name> "<P01:A,P02:B,...>" ["<second judge>" ...]     accuracy per judge + binomial p-value vs 50%"""
import csv, glob, json, math, random, statistics, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; J = ROOT / "judgments"

def stats():
    rows = {}
    for f in glob.glob(str(ROOT / "data/creators/*.csv")):
        for r in csv.DictReader(open(f)):
            try: rows.setdefault(r["username"], []).append((r["shortcode"], int(r["views"]), int(r["created_unix"])))
            except ValueError: pass
    out = {}
    for h, items in rows.items():
        med = statistics.median(v for _, v, _ in items) or 1
        for s, v, t in items: out[s] = {"handle": h, "views": v, "ratio": v / med, "log_ratio": math.log(max(v, 1) / med), "age_days": (time.time() - t) / 86400}
    return out

def first_line(d):
    try:
        t = json.loads((d / "transcript.json").read_text()); txt = " ".join(s["text"] for s in t["segments"] if s["start"] < 4.0)
        return txt[:140] or "(no speech in first 4 s)"
    except Exception: return "(no transcript)"

def pack(name):
    st = stats(); by = {}
    for d in sorted((ROOT / "analysis").glob("*__*")):
        code = d.name.split("__")[-1]
        if code in st and (d / "hook_strip.jpg").exists() and st[code]["age_days"] >= 7: by.setdefault(st[code]["handle"], []).append((st[code]["log_ratio"], code, d))
    out = J / name; out.mkdir(parents=True, exist_ok=True); rnd = random.Random(name); key = {}; lines = []; n = 0
    for h, items in sorted(by.items()):
        items.sort(); hits = [x for x in items if x[0] > 0.7][::-1]; flops = [x for x in items if x[0] < -0.5]
        for hit, flop in zip(hits, flops):
            n += 1; pid = f"P{n:02d}"; side = rnd.choice("AB"); pair = {side: hit, ("B" if side == "A" else "A"): flop}
            for L, (_, code, d) in pair.items():
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(d / "hook_strip.jpg"), "-filter_complex", "split[a][b];[a]crop=iw/2:ih:0:0[t];[b]crop=iw/2:ih:iw/2:0[u];[t][u]vstack,scale=1080:-2", "-frames:v", "1", str(out / f"{pid}_{L}.jpg")], check=True)
                lines.append(f"{pid}_{L}: {first_line(d)}")
            key[pid] = {"hit": side, "handle": h, "hit_code": hit[1], "flop_code": flop[1], "hit_ratio": round(math.exp(hit[0]), 1), "flop_ratio": round(math.exp(flop[0]), 2)}
    (out / "lines.txt").write_text("\n".join(lines)); (out / "key.json").write_text(json.dumps(key, indent=1))
    print("pairs:", n, "from", len({v['handle'] for v in key.values()}), "creators ->", out)

def tally(name, answers):
    key = json.loads((J / name / "key.json").read_text()); res = []
    for j, a in enumerate(answers, 1):
        picks = dict(x.strip().split(":") for x in a.replace(" ", "").split(",") if ":" in x)
        ok = sum(1 for p, k in key.items() if picks.get(p, "").upper() == k["hit"]); n = sum(1 for p in key if p in picks)
        pval = sum(math.comb(n, i) for i in range(ok, n + 1)) / 2 ** n if n else 1
        res.append({"judge": j, "correct": ok, "n": n, "accuracy": round(ok / n, 3) if n else None, "p_one_sided": round(pval, 4)}); print(res[-1])
    (J / name / "result.json").write_text(json.dumps(res, indent=1))

if __name__ == "__main__":
    pack(sys.argv[2]) if sys.argv[1] == "pack" else tally(sys.argv[2], sys.argv[3:])
