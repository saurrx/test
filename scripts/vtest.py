#!/usr/bin/env python3
"""Pre-registered virality tests on data/features.csv. Every run is appended to research/tests.jsonl (nulls included).
  vtest.py run <id> <feature> [--split median|<number>|binary] [--continuous] [--where "col>=x"] [--note "..."]
     Binary split: per creator, mean(virality | high) - mean(virality | low); statistic = n-weighted mean of those differences.
     --continuous: per creator Spearman correlation with virality; statistic = n-weighted mean.
     p-value: 5000 permutations shuffling the feature WITHIN each creator. Only reels >= 7 days old.
     Robustness: the statistic recomputed leaving each creator out (min/max), and the count of creators agreeing in sign.
  vtest.py report      Benjamini-Hochberg across all recorded tests -> research/tests_table.md"""
import csv, json, math, random, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; LOG = ROOT / "research/tests.jsonl"

def load(where):
    rows = [r for r in csv.DictReader(open(ROOT / "data/features.csv")) if r["eligible"] == "1"]
    for cond in where:
        import re; col, op, val = re.match(r"(\w+)(>=|<=|==|!=|>|<)(.+)", cond).groups()
        def ok(r):
            x = r.get(col, "")
            if x == "": return False
            try: a, b = float(x), float(val)
            except ValueError: a, b = x, val
            return {">=": a >= b, "<=": a <= b, "==": a == b, "!=": a != b, ">": a > b, "<": a < b}[op]
        rows = [r for r in rows if ok(r)]
    return rows

def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r
def corr(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n; sa = sum((x - ma) ** 2 for x in a); sb = sum((y - mb) ** 2 for y in b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sa * sb) if sa > 0 and sb > 0 else None

def stat(groups, continuous, skip=None):
    num = den = 0.0; signs = []
    for c, (x, y) in groups.items():
        if c == skip: continue
        if continuous:
            if len(x) < 5: continue
            s = corr(rank(x), rank(y)); w = len(x)
        else:
            hi = [yy for xx, yy in zip(x, y) if xx]; lo = [yy for xx, yy in zip(x, y) if not xx]
            if len(hi) < 2 or len(lo) < 2: continue
            s = sum(hi) / len(hi) - sum(lo) / len(lo); w = 2 * len(hi) * len(lo) / (len(hi) + len(lo))
        if s is None: continue
        num += s * w; den += w; signs.append(s)
    return (num / den if den else None), signs

def run(tid, feature, split, continuous, where, note):
    rows = [r for r in load(where) if r.get(feature, "") != ""]; groups = {}; vals = [float(r[feature]) for r in rows]
    thr = None
    if not continuous:
        if split == "median":  # per-creator median split
            pass
        elif split != "binary": thr = float(split)
    by = {}
    for r in rows: by.setdefault(r["creator"], []).append((float(r[feature]), float(r["virality"])))
    for c, it in by.items():
        x = [a for a, _ in it]; y = [b for _, b in it]
        if not continuous:
            if split == "median": m = sorted(x)[len(x) // 2]; x = [int(a >= m) if len(set(x)) > 1 else 0 for a in x]
            elif split == "binary": x = [int(a > 0) for a in x]
            else: x = [int(a >= thr) for a in x]
        groups[c] = (x, y)
    obs, signs = stat(groups, continuous)
    res = {"id": tid, "feature": feature, "kind": "spearman" if continuous else f"split:{split}", "where": where, "n": len(rows), "creators_used": len(signs), "note": note, "ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}
    if obs is None: res.update({"statistic": None, "p": None, "verdict": "not testable yet (too few reels per creator)"})
    else:
        rnd = random.Random(1); B = 5000; ge = 0
        for _ in range(B):
            g2 = {}
            for c, (x, y) in groups.items(): xs = x[:]; rnd.shuffle(xs); g2[c] = (xs, y)
            s, _ = stat(g2, continuous)
            if s is not None and abs(s) >= abs(obs) - 1e-12: ge += 1
        loo = [stat(groups, continuous, skip=c)[0] for c in groups]; loo = [x for x in loo if x is not None]
        agree = sum(1 for s in signs if (s > 0) == (obs > 0))
        res.update({"statistic": round(obs, 4), "effect_x": round(math.exp(obs), 2) if not continuous else None, "p": round((ge + 1) / (B + 1), 4),
                    "loo_min": round(min(loo), 4), "loo_max": round(max(loo), 4), "sign_agree": f"{agree}/{len(signs)}", "loo_sign_stable": (min(loo) > 0) == (max(loo) > 0)})
    LOG.parent.mkdir(exist_ok=True)
    with open(LOG, "a") as fh: fh.write(json.dumps(res) + "\n")
    print(json.dumps(res))

def report():
    tests = {}
    for l in open(LOG):
        t = json.loads(l); tests[t["id"]] = t  # latest run per id wins
    ts = [t for t in tests.values() if t.get("p") is not None]; ts.sort(key=lambda t: t["p"]); m = len(ts)
    q = [min(1.0, t["p"] * m / (i + 1)) for i, t in enumerate(ts)]
    for i in range(m - 2, -1, -1): q[i] = min(q[i], q[i + 1])
    lines = ["| id | feature | test | n | creators | effect | p | q (BH) | sign agree | LOO stable | status |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t, qq in zip(ts, q):
        eff = f"{t['effect_x']}x" if t.get("effect_x") else f"rho {t['statistic']}"
        status = "evidenced" if qq <= 0.10 and t["loo_sign_stable"] else ("suggestive" if t["p"] <= 0.05 else "null")
        lines.append(f"| {t['id']} | {t['feature']} | {t['kind']} | {t['n']} | {t['creators_used']} | {eff} | {t['p']} | {round(qq, 3)} | {t['sign_agree']} | {t['loo_sign_stable']} | {status} |")
    for t in tests.values():
        if t.get("p") is None: lines.append(f"| {t['id']} | {t['feature']} | {t['kind']} | {t['n']} | {t['creators_used']} | - | - | - | - | - | not testable yet |")
    (ROOT / "research/tests_table.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "report": report()
    else:
        opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
        where = [a[i + 1] for i, x in enumerate(a) if x == "--where"]
        run(a[1], a[2], opt("--split", "median"), "--continuous" in a, where, opt("--note", ""))
