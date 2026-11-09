# Make log

| When (UTC) | What | Result |
|---|---|---|
| 2026-11-09 20:27 | **Checkpoint 0** (Phase-0 library): 3 benchmark briefs rendered as 540p drafts, `renders/cp0_b{1,2,3}.mp4`, props in `bench/cp0/` | QC: b1 PASS, b2 PASS, b3 FAIL (no visual change by 3 s; caption contrast 2.3). Known defects kept as the baseline: yantra glow artefact (blocky rectangles), dark first frames, hollow-looking bell, weak figure in the glow lane |
| 2026-11-09 20:38 | **Hook lab 1** (bell, first 5.3 s, 8 variants + the reference Aarti reel's hook; 3 blind Sonnet judges, Borda) | 1st `v4_text` 24 pts, first place from all 3 judges (big "YOU RING IT WRONG" headline on frame 1). 2nd `v7_3shots` 15. **Reference hook 13 (3rd of 9).** Then cross 12, person 12, base 11, strike-at-0 11, pop captions 7, bright-only 3. Below first place the order is noisy (judges disagree). All 3 judges asked for the same fix: a large high-contrast headline on frame 1; thin serif captions are too small. QC: all 8 pass |
| 2026-11-09 20:52 | Worker process restarted mid-iteration. Tailscale and autocommit restarted from saved state, no new login needed; PC jobs were unaffected | Recovered in 2 min |
| 2026-11-09 21:07 | **Reel 1 v1** `renders/reel1_v1.mp4` (original "You ring the temple bell wrong", 62 s, Gemini voice $0.014, Lyria music $0.04, 17 scenes) | QC PASS (13 cuts, caption contrast 12.0, 140 wpm, first change 1.1 s). Own review: devotee silhouette reads as an icon and sits under the captions |
| 2026-11-09 21:10 | Judge calibration 1 (25 hit/flop pairs) | 68% and 64% correct; narrowly misses the bar; verdicts stay "craft" |
