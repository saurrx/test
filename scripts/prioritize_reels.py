"""Order reel downloads so a partial download is still a valid sample. Writes data/reels_priority.tsv.
Tier 1 (balanced): per creator, the 3 biggest hits and 3 biggest flops among reels >= 7 days old
  (younger reels are still accruing views), by log(views / creator median), creators interleaved.
Tier 2: everything else, biggest |log ratio| first, creators interleaved."""
import csv, glob, math, statistics, time
NOW = time.time(); MIN_AGE = 7 * 86400
rows = {}
for f in glob.glob("data/creators/*.csv"):
    for r in csv.DictReader(open(f)):
        try: v, t = int(r["views"]), int(r["created_unix"])
        except (ValueError, KeyError): continue
        rows.setdefault(r["username"], []).append((r["shortcode"], v, t))
want = [l.split("\t") for l in open("data/all_reels.tsv").read().split("\n") if l.strip()]
tier1, tier2 = {}, {}
for h, items in rows.items():
    med = statistics.median(v for _, v, _ in items) or 1
    score = {s: math.log(max(v, 1) / med) for s, v, _ in items}
    old = sorted((s for s, _, t in items if NOW - t >= MIN_AGE), key=score.get)
    k = min(3, len(old) // 2)
    picks = []
    for i in range(k): picks += [old[-1 - i], old[i]]          # hit, flop, hit, flop...
    tier1[h] = picks
    tier2[h] = sorted((s for s, _, _ in items if s not in picks), key=lambda s: -abs(score[s]))
def interleave(q):
    out = []
    while any(q.values()):
        for h in sorted(q):
            if q[h]: out.append((h, q[h].pop(0)))
    return out
n1 = sum(map(len, tier1.values()))
out = interleave(tier1) + interleave(tier2)
seen = {s for _, s in out}
out += [(h, s) for h, s in want if s not in seen]
open("data/reels_priority.tsv", "w").writelines(f"{h}\t{s}\n" for h, s in out)
print(len(out), "reels;", n1, "in balanced tier 1")
