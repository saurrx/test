# Tasks

## Now
- Loop RUNNING 2026-11-09T19:59Z → 2026-11-10T04:59Z. **Phase 0 done at 20:30** (judge calibration deferred: only 6 hit/flop pairs analysed so far; run `scripts/calib.py pack calib_2` once `data/features.csv` shows ≥ 100 analysed).
- Iteration 1 done 20:38 (V1–V5, V19–V21; hook lab 1: frame-1 headline wins).
- **Iteration 2 (now)**: full reel #1 `makes/reel1_bell/` (original, 60–70 s per P1, glow lane, headline on frame 1 per P6): script → Gemini voice → align on PC → 1 Lyria music clip → props → draft → QC → final 1080p → `renders/best/`.
- Then iteration 3: hook lab 2 on the Pinaka brief (C3 line variants, bigger captions) + checkpoint 1 + calibration if ≥ 20 pairs + V22 and analysed-feature tests.

## How to work (for a restart)
- Render: `scripts/render.sh <props.json> <name> [draft|final]` (PC). QC: `python3 -I scripts/qc.py renders/<name>.mp4 <props.json>`.
- Voice: `scripts/pc "cd ~/reels-loop/repo && ../.venv/bin/python scripts/voice.py tts <out_base> <voice> <rate> '<text>'"`, then copy the mp3 to `remotion/public/audio/`.
- Judge: `scripts/judge.py pack|prompt|tally`, judges are Sonnet subagents, one per `jN` folder.
- Data tests: `scripts/pc_sync.sh pull && python3 -I scripts/dataset.py && python3 -I scripts/vtest.py run ...`, then `vtest.py report`.
- Watchdogs: A `trig_01W81GSJRHEHJ1JUPrxaG8Bc` (:56), B `trig_018B98jFa4hDE7PHcmLxUtpt` (:27), both enabled.

## Running in the background
- PC `reels-worker` (systemd user unit on `arch`): balanced reel download + analysis v3. Check with `scripts/pc 'cat ~/reels-loop/repo/data/reels/_progress.txt'`; pull with `scripts/pc_sync.sh pull`.
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
