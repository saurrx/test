"""Order data/all_reels.tsv so the most informative reels download first.
Per creator, rank by |log(views/creator median)| (biggest hits and flops first), then interleave creators
round-robin so every creator is covered early. Writes data/reels_priority.tsv (handle<TAB>shortcode)."""
import csv, glob, math, os, statistics
rows = {}
for f in glob.glob("data/creators/*.csv"):
    with open(f) as fh:
        for r in csv.DictReader(fh):
            try: v = int(r["views"])
            except (ValueError, KeyError): continue
            rows.setdefault(r["username"], []).append((r["shortcode"], v))
want = [l.split("\t") for l in open("data/all_reels.tsv").read().split("\n") if l.strip()]
queues = {}
for h, items in rows.items():
    med = statistics.median(v for _, v in items) or 1
    items.sort(key=lambda x: -abs(math.log(max(x[1], 1) / med)))
    queues[h] = [s for s, _ in items]
seen, out = set(), []
while any(queues.values()):
    for h in sorted(queues):
        if queues[h]:
            s = queues[h].pop(0); out.append((h, s)); seen.add(s)
out += [(h, s) for h, s in want if s not in seen]  # anything without stats goes last
with open("data/reels_priority.tsv", "w") as fh:
    fh.writelines(f"{h}\t{s}\n" for h, s in out)
print(len(out), "reels prioritised")
