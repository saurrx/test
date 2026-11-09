# Tasks

## Now
- Loop RUNNING 2026-11-09T19:59Z → 2026-11-10T04:59Z. **Phase 0 done at 20:30** (judge calibration deferred: only 6 hit/flop pairs analysed so far; run `scripts/calib.py pack calib_2` once `data/features.csv` shows ≥ 100 analysed).
- Iterations 1–2 done (see `makes/LOG.md`). Reel 1 closed as `hard` after 3 versions (v1 < v2 < v3 by blind judges, still loses to the reference on scene variety).
- **Iteration 3 (started 21:24)**: new scene types built (mandir exterior, doorway, feet, hand, thali). In flight on the PC: (1) `reel1_final` 1080p render then checkpoint-1 drafts `cp1_b1..3` (log: scratchpad/final1.log; if lost, re-run `scripts/render2.sh makes/reel1_bell/reel.json reel1_final final` and the cp1 line), (2) hook lab 2 `h2_*` (7 variants, Pinaka, line test).
  Next: QC + judge hook lab 2 (3 judges, include `analysis/kathayug27__De9qY85zaQk/hook_strip.jpg`); judge cp1 vs cp0 (3 briefs × 3 judges, pairwise, `--whole`); copy reel1_final to `renders/best/`.
- Iteration 4: reel 2 = Pinaka story, flat lane + new scenes, 60–75 s, ends on a "part 2" hook (P8). Use `scripts/render2.sh` (own bundle dir) for all renders.
- When `data/features.csv` shows ≥ 150 analysed: run V6–V18 per prereg, then fit the views model.

## How to work (for a restart)
- Render: `scripts/render.sh <props.json> <name> [draft|final]` (PC). QC: `python3 -I scripts/qc.py renders/<name>.mp4 <props.json>`.
- Voice: `scripts/pc "cd ~/reels-loop/repo && ../.venv/bin/python scripts/voice.py tts <out_base> <voice> <rate> '<text>'"`, then copy the mp3 to `remotion/public/audio/`.
- Judge: `scripts/judge.py pack|prompt|tally`, judges are Sonnet subagents, one per `jN` folder.
- Data tests: `scripts/pc_sync.sh pull && python3 -I scripts/dataset.py && python3 -I scripts/vtest.py run ...`, then `vtest.py report`.
- Watchdogs: A `trig_01W81GSJRHEHJ1JUPrxaG8Bc` (:56), B `trig_018B98jFa4hDE7PHcmLxUtpt` (:27), both enabled.

## Running in the background
- PC `reels-worker2` (systemd user unit on `arch`, 3 whisper threads so renders get the CPU; the old `reels-worker` is stopped) and `reels-meta` (metadata-only scrape): balanced reel download + analysis v3. Check with `scripts/pc 'cat ~/reels-loop/repo/data/reels/_progress.txt'`; pull with `scripts/pc_sync.sh pull`.
- Cloud `scripts/autocommit.sh`: commits and pushes every 10 minutes.

## Done (setup, 2026-11-09)
- [x] Treg works without prompts ($0.58); TTS path tested end to end ($0.0006 for a 3 s line) with `scripts/treg_audio.py`
- [x] Remotion scaffold; smoke render OK on cloud and on the PC (PC needs `--browser-executable=/usr/bin/chromium --chrome-mode=chrome-for-testing`)
- [x] Tailscale link to the PC; `~/reels-loop` venv with yt-dlp, faster-whisper, edge-tts
- [x] Instagram downloads work from the PC without cookies
- [x] Analyzer v3 (cut detector for dark footage, view changes, motion, Hindi-aware transcript with word timings, hook strip)
- [x] Fable 5.2 review of the plan; `LOOP.md` v3
- [x] Devanagari text renders correctly in Remotion on the PC (`@remotion/google-fonts`, Noto Sans Devanagari)
- [x] WebGL shaders render on the PC only with `--gl=swangle` (software); GPU backends give no WebGL over SSH. A 30-frame 1080p shader clip takes 7 s including bundling
- [x] Blind judge mechanism: a Sonnet 5.5 subagent reads two hook strips and returns a pick
- [x] Watchdog wake-ups created (disabled until "go")
