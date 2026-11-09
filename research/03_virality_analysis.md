# Virality analysis: every pre-registered test, nulls included

Method: `research/prereg.md`. Outcome = log(views / creator median) unless "detrended" (views against the creator's
6 nearest-in-time other reels). Only reels ≥ 7 days old; comparisons within creator; 5,000 within-creator permutations;
q = Benjamini–Hochberg across all tests so far. Full table: `research/tests_table.md`. No reel was posted by us, so
these are patterns in other creators' data, not experiments.

## Iteration 1 (2026-11-09, 657 eligible reels, 19 creators, CSV-only features)

**F1. Longer reels do better, the opposite of what I predicted (V1, V19).**
Within a creator, duration and views are positively related (rho +0.22, p = 0.0002, 14 of 18 creators). After removing
time trends it shrinks but holds (rho +0.11, p = 0.007, q = 0.014, 13 of 15 creators, stable leaving any creator out).
By length, the share of reels that beat twice their local baseline: under 30 s 12% (n=77), 30–60 s 25% (n=151),
**60–90 s 32% (n=156)**, 90–150 s 25% (n=179), over 150 s 24% (n=46).
Caveat: creators may give their best stories more time, so length may mark effort rather than cause views.
→ Rule P1 (`evidenced`, correlational): full reels target 60–90 s; never under 30 s.

**F2. Posting time and weekday make no detectable difference (V2, V3).**
Evening (18:00–24:00 IST) vs earlier: 1.03x, p = 0.85. Weekend vs weekday: 0.95x, p = 0.72. Signs split across creators.
→ Rule P2 (`null`): don't spend effort on posting time.

**F3. Hits cluster in the raw data, but that is trend, not momentum (V5, V20).**
A reel's views track the previous reel's (rho +0.53, p = 0.0002): accounts have hot and cold stretches.
V20 (detrended) came out negative (rho −0.17), but that test is flawed: the local baseline includes the previous reel,
which forces a negative relation. I am not drawing a conclusion from V20. A clean version (baseline excluding the
previous reel) is registered as V22.
→ No rule yet.

**F4. A longer gap since the previous post goes with more views (V4, V21).**
Raw: 1.27x, p = 0.12 (null). Detrended: 1.38x, p = 0.013, q = 0.02, stable leaving any creator out, but only 11 of 17
creators agree in sign. → Rule P3 (`evidenced`, weak): don't post in bursts; space posts by at least the creator's usual gap.

## Judge calibration 1 (2026-11-09 21:10, 25 hit/flop pairs from 15 creators, first 3 s + opening line only)
Two blind Sonnet judges picked the real hit in **17/25 (68%, one-sided p = 0.054)** and **16/25 (64%, p = 0.11)**.
Chance is 50%. This narrowly misses the pre-registered bar (p ≤ 0.05), so judge verdicts stay labelled **craft**:
the judge is probably a little better than a coin at spotting real hits from the opening, but not reliably.
Both judges said they relied on a curiosity gap or bold claim in the opening line plus legible on-screen hook text.
To be repeated when about 50 pairs are available.

## Iteration 3 (2026-11-09 21:18)

**F5. Short-range momentum is real (V22, the clean version of V20).**
With baselines that exclude each other's reel, a reel that beats its local baseline tends to be followed by one that
also does: rho +0.17, p = 0.0004, 11 of 13 creators, stable leaving any creator out (n = 570).
Reading: after a hit, the next post gets a lift (audience spill-over, the algorithm, or the creator riding a topic).
Caveat: hot streaks longer than the ±3-reel window would also produce this.
→ Rule P8 (`evidenced`, correlational): when a reel hits, post a closely related follow-up next (a "part 2"), don't change topic.
