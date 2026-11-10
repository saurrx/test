# Tasks

## Now
Loop FINISHED at 2026-11-10T04:59Z. Read `research/FINAL_REPORT.md` first.
- Finals: `renders/best/reel{1..7}_*_1080.mp4` (reel 7 = Hindi edition of reel 5). Reels 2 and 4 each have one black frame to fix before posting.
- Watchdog scheduled tasks disabled at the end. PC services `reels-worker2` and `reels-meta` stopped and disabled (05:15Z). Treg is hard-blocked by deny rules in `.claude/settings.json` (delete them to re-enable).
- Next session ideas: post reel 5 first; A/B the first frame; continue the Shiva series (part 4 "why Shiva wears the moon" was promised in reel 6).

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
