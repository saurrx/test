# Tasks

## Now
- [ ] Waiting for the owner's "go" to start the 9-hour loop (`LOOP.md` v3). Nothing in the loop has run.

## On "go"
1. Write loop start/end (UTC) in `LOOP.md`; create the two hourly watchdog wake-ups (30 min apart).
2. Phase 0 (75 min): `scripts/qc.py`, `scripts/judge_pair.py`, judge calibration, `bench/briefs/`, component library + Gallery, `research/prereg.md`, checkpoint 0.
3. Iterations per `LOOP.md`.

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
