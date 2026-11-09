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

**F6. Hashtag count: no effect (V15). Caption length: weak, unconfirmed (V14).** (21:38, 324 reels with captions so far)
Hashtags: rho +0.06, p = 0.38, signs split 6/11 → null, as predicted. Caption length: rho +0.12, p = 0.048, the
opposite of my prediction (longer captions do slightly better), only 10 of 17 creators agree. The caption sample is
incomplete and not random (the scrape runs lowest-priority reels first), so both are re-run when all captions are in.
→ P12 (`null` so far): don't spend effort on hashtags.

## Iteration 4 (2026-11-09 21:47, caption content, 324 reels with captions; interim until all captions are in)

**F7. Series reels get about 2.6x the creator's usual views (V23).**
Reels whose caption marks them as part of a series ("part 2", "भाग", "episode") beat the same creator's other reels by
2.6x (p = 0.0016, 6 of 7 creators who use series labels, stable leaving any creator out). This agrees with F5 (momentum).
Caveat: creators tend to make a "part 2" after a part 1 did well, so some of this is selection, not the label itself.
→ P8 upgraded: plan stories as 2–3 parts and label them.

**F8. Calls to action in the caption: no detectable effect (V24–V26).** Comment: 0.65x (p = 0.23); follow: 1.65x
(p = 0.11); share: 1.28x (p = 0.53). All unstable across creators. → `null`: a CTA is free to include but is not a lever.

**F9. Topic (exploratory, few creators).** Shiva / Mahadev mentions: 2.3x (p = 0.025, but only 3 of 5 creators agree).
Krishna / Mahabharat mentions: 0.44x (p = 0.023, 3 of 4 creators). Ram / Hanuman: 1.1x (null).
Too few creators cover each topic to call this evidenced; treat as a lead: Shiva content may travel best for these accounts.

## Iteration 5 (2026-11-09 22:27, video features, 140 analysed reels ≥ 7 days old, 16 creators)
The analysed set is the balanced sample (each creator's biggest hits and flops first), so effect sizes are inflated;
directions are what matter. Hits here = more than 2x the creator's median (52 reels); flops = under 0.6x (48 reels).

**F10. Voice-led reels beat music-only reels by a wide margin (V18).** Within the 5 creators who post both kinds,
voiced reels do far better (5 of 5 creators, p = 0.004). 94% of hits have a voiceover vs 71% of flops.
→ P15 (`evidenced`): always voice-led.

**F11. More visual change wins; hard-cut count alone does not (V12, V11).** Visual changes per 10 s (cuts, dissolves,
big camera moves): rho +0.25, p = 0.019, q = 0.06, 11 of 16 creators; hits have twice the rate of flops (median 1.6 vs
0.8 per 10 s). Hard cuts per 10 s: rho +0.09, p = 0.43 (null). → P16 (`evidenced`): a new picture at least every 6 s,
ideally every 3–4 s; how you get there (cut, dissolve, camera move) doesn't matter.

**F12. Starting the voice at 0.0 s is not best; a short beat first does better (V9, opposite to my prediction).**
Time to first word vs views: rho +0.27, p = 0.024, 9 of 13 creators. Median views vs the creator's norm: voice at
0–0.15 s: 1.0x (n = 80); 0.15–0.6 s: 2.6x (n = 25); 0.6–2 s: 4.9x (n = 9); later than 2 s: 1.1x (n = 14).
Small groups, so treat the exact window as a lead. → P4 revised (`suggestive`): open with 0.3–1 s of picture, headline
and sound before the first spoken word; never wait more than 2 s.

**Nulls.** Motion in the first 3 s (V13, p = 0.83), loudness variation (V17, p = 0.46), speech pace (V10, p = 0.14;
hits are if anything slower: 144 vs 161 words a minute).
**Not testable.** Question / number / negation / "you" in the opening line (V6–V8, V16): my keyword detector fires on
too few reels in too few creators (2–6). Needs hand or model labelling of opening lines; planned as hook-type labels.
**Descriptive only.** Hindi reels: 28 hits to 13 flops; English: 21 to 21. Creators rarely post in both, so this cannot
be separated from who the creator is.

## Views-prediction model (2026-11-09 22:35) — `research/model.md`, `scripts/model.py`
Ridge regression predicting views relative to the creator's median, scored on creators the model never saw.

| Features | Reels | Ranking skill on unseen creators (per-creator Spearman) |
|---|---|---|
| Timing and history only (length, gap, previous reel) | 571 | 0.21 (11 of 14 creators positive); pooled across creators: about 0 |
| + caption features | 372 | 0.14 (5 of 12) — captions add nothing |
| Video features only (voice, visual change, beat before voice, cuts, loudness) | 140 | **0.36 (15 of 18 creators positive)**; pooled 0.24 |

**What this says, plainly.** The measurable features carry real but modest signal. The best model ranks a creator's
hits above their flops better than chance for 15 of 18 creators, and it does so on the hit/flop sample, which is the
easy case. It cannot predict how many views a reel gets. Most of what separates a hit from a flop is not in these
features: the idea, the opening line, and the story are not measured yet. The strongest weights match the tests:
voiceover (+), visual change (+), a beat before the first word (+).
**So "programming virality" today means:** follow the evidenced rules to avoid the known ways of losing (too short,
music-only, static picture, no series), then compete on hook and story, where the evidence so far is only blind-judge craft.

## Hook types (2026-11-09 22:40, 92 labelled reels ≥ 7 days old; labels made blind to views)

**F13. The type of opening line does not separate hits from flops in this sample (V31–V36).**
Within-creator tests are underpowered (most creators have too few reels of each type: 1–7 creators usable per test),
so none passes. An exploratory pooled comparison (not pre-registered) shows the same: question openings 25% hits vs
40% without (n = 12, p = 0.55); numbers 44% vs 35% (n = 27, p = 1.0); addressing the viewer 42% vs 36%; plain narration
35% vs 39%; "you're doing it wrong" openings are rare (n = 5). The only lean is **stakes** (danger, death, a vow):
47% hits vs 34% (n = 30, p = 0.14).
Reading: a hook formula by itself is not what makes these reels hit. This matches the judge calibration (64–68%) and
the modest model score. → P10 stays a `prior`; stakes is the one device with a consistent (weak) lean in both the
judges' ranking and the real data. Re-test when all 832 reels are analysed.

## Iteration 6 (2026-11-09 22:42, CSV-only, 610–658 reels)
**F14. The 60–90 s sweet spot holds as its own test (V40).** 60–90 s reels get 1.42x the creator's local baseline
(p = 0.029, 7 of 11 creators, stable leaving any creator out). Confirms P1.
**F15. Posting two reels within 12 hours looks costly (V41, suggestive).** 0.69x (p = 0.10, 5 of 9 creators). Same
direction as F4 (longer gaps help). Not confirmed on its own.
**F16. Hiding likes makes no detectable difference (V37).** 1.31x, p = 0.60, creators split 2/4 → null.

## Judge calibration 2 (2026-11-09 23:06, 34 hit/flop pairs from 15 creators)
Two blind Sonnet judges picked the real hit in **19/34 (56%)** and **18/34 (53%)**: no better than chance. Both chose
clip "A" about three times in four (the real hit was "A" in 18 of 34), so they also show a position bias.
Pooled with the first run: 70 correct of 118 judgments (59%).
**Conclusion: the blind judge cannot tell which real reel went viral from its first 3 seconds.** Its rankings measure
craft as an AI sees it (legible text, a clear focal image, variety), which is worth having, but they are not evidence
about views. Every "beats the real reel" result in `makes/LOG.md` must be read that way. My own packs give each judge a
different random lettering, which limits the position bias in those rankings.
