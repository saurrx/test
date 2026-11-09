# Tasks

## Now
- Loop RUNNING 2026-11-09T19:59Z → 2026-11-10T04:59Z. **Phase 0 done at 20:30** (judge calibration deferred: only 6 hit/flop pairs analysed so far; run `scripts/calib.py pack calib_2` once `data/features.csv` shows ≥ 100 analysed).
- Iterations 1–4 done (see `makes/LOG.md`): reel 1 final in `renders/best/`; checkpoint 1 = improved (6/9); hook labs 1–2; findings F1–F9.
- **Treg is off** (permission prompts): free voice via `scripts/voice.py tts` on the PC, saved music loops, `scripts/synth.py`.
- After any restart run `scripts/ensure_up.sh`. Renders: `scripts/render_bg.sh <job> <draft|final> <props> <name>...` then `scripts/render_get.sh <job> [wait]`; finals: `scripts/finish.sh <pc render name> <out name>` → `renders/best/`.
- **Iteration 5 (started 22:15)**. In flight on the PC: job `r2final` (reel 2 final 1080p → then `scripts/finish.sh reel2_final reel2_pinaka_1080`, QC `--final`, judge with 3 judges vs `data/ref/pinaka_ref.mp4`), job `r3v1` (reel 3 draft, `makes/reel3_jal/`: view sheet, fix, judge vs `data/ref/aarti_ref.mp4` and reel 1, max 3 versions, then final).
- Next: once `python3 -I scripts/dataset.py` shows ≥ 150 analysed, run V6–V13, V16–V18 exactly as in `research/prereg.md`, `vtest.py report`, write findings; then fit the views model (leave-one-creator-out) and write its accuracy.
- Then: hook lab 3 (glow lane, Shiva: test P10 stakes line vs "you do X wrong" line), checkpoint 2 after iteration 6 (`bench/cp2.py` from cp1 + new scenes), reel 4 = part 2 of reel 2 or 3 (P8), calibration 2 when ≥ 45 pairs.
- Final 30 minutes (from 04:25 UTC): checkpoint 3, `research/FINAL_REPORT.md`, ranked queue of originals, disable watchdogs.

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
