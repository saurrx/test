# Tasks

## Now
Loop RUNNING (started 2026-11-09T19:59Z, ends 2026-11-10T04:59Z). Iteration 9 as of 00:42Z.
- In progress: PC job `r5g` = reel 5 final with screen-fixed headlines -> `scripts/finish.sh reel5g_final reel5_never_1080`, QC `--final`, check the first second (headline must not collide with the header).
- In progress: PC job `r6v1` = reel 6 draft ("Om Namah Shivaya: five syllables, five elements", `makes/reel6_mantra`) -> sheet review, QC, playbook check, 2 blind judges vs `renders/reel5_v3.mp4` + `data/ref/aarti_ref.mp4`, at most 3 versions, then final as `reel6_mantra_1080`.
- Done this session: reel 4 corrected final; reels 1 and 3 upgraded finals; checkpoint 3 (5/9, not improved) -> headline clipping fixed (`fixedText: true` in props, use it in every new reel) -> checkpoint 3b **8/9 vs cp1, QC 3/3**; F20 (first frame, suggestive), F21 (endings, underpowered).
- Next: hook lab 3 with `fixedText`; checkpoint 4 near the end (vs cp3b); re-render reels 2 and 4 with `fixedText` only if a headline is visibly clipped.
- Virality next: rerun `scripts/pc_sync.sh pull && python3 -I scripts/dataset.py && python3 -I scripts/vtest.py report && python3 -I scripts/model.py` near 04:00Z with whatever the PC worker has analysed by then (241 so far).
- From 04:25Z: `research/FINAL_REPORT.md`, push, disable the two watchdog scheduled tasks.
- No Treg calls. At most 2 render jobs at once on the PC.

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
