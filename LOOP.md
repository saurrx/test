# 10-hour self-improving research loop (DRAFT, awaiting owner review)

Status: **NOT STARTED**. Do not begin iterations until the owner says "go" in this session.
On go: write `Loop start (UTC)` and `Loop end = start + 10h` below, then start iteration 1.

- Loop start (UTC): _not set_
- Loop end (UTC): _not set_

## Goals
1. **Make best-in-class reels** with AI + code, matching the reference reels end to end (story, visuals, cuts, sound, captions).
2. **Understand virality** well enough to program it. Every iteration must add at least one *new, evidenced* finding.
3. **Unblock yourself.** Any blocker gets a workaround, logged, and the loop continues. Never wait on the owner.

## Iteration (target 45–75 min each, ~8–12 iterations)
Run the two tracks in parallel (subagents), then integrate.

**Track A: make**
1. Pick the target: next reference reel by (virality × feasibility tier T1/T2), see `research/02_feasibility_triage.md`.
2. Break it down: scene list with timings, hook, VO script, caption style, music/SFX, colour/look. Save to `makes/<id>/spec.md`.
3. Build: assets (Treg stills/TTS/music within budget, else code-only), compose in Remotion or the Python/ffmpeg pipeline, render 1080×1920.
4. Grade against the reference with `scripts/analyze_reel.py` plus a vision review of side-by-side frames. Score 1–10 on
   hook, story clarity, visual quality, motion/cuts rhythm, audio mix, captions, "would a viewer believe this is the creator's reel".
   Use a fresh subagent as the grader so it is not anchored on the builder.
5. Fix the biggest 2–3 gaps, re-render, re-grade. Max 3 iterations per reel, then mark it `hard` and log the blocker.
6. Log to `makes/LOG.md`: version, score per dimension, what changed, cost.

**Track B: virality**
1. Advance one research question per iteration (examples: hook type vs views, duration, cut rate, VO vs music-only, language,
   story shape, posting time, series effects, CTA type, first-frame text).
2. Use the full dataset: `data/creators/*.csv` (views, likes*, comments, duration, date) + per-reel analysis + labels.
   Metric: `log(views / creator median)`. *Likes of 3 = hidden, exclude.
3. Write each finding with its evidence (n, effect size, examples) to `research/03_virality_analysis.md`, and turn it into
   a rule in `research/virality_playbook.md` that Track A must apply to the next make.

**Integrate:** update `TASKS.md`, `DECISIONS.md`, commit and push. Every iteration must change the playbook or the pipeline.

## Getting better each iteration (checked, not hoped)
- The make score of the newest reel must beat the previous best on at least one dimension, without regressing more than 1 point elsewhere.
- Each pipeline improvement becomes reusable code in `scripts/` or `remotion/`, not a one-off.
- Each virality finding must be new (check `research/03_virality_analysis.md` first).

## Blocker policy
- If a tool call is refused or prompts, skip that step, log it in `DECISIONS.md` as `BLOCKER:` with the workaround tried, and continue.
- Instagram 429: back off, use already-downloaded reels, retry later.
- Treg balance < $0.10: switch to code-only (T1) makes and keep going; note the top-up needed.
- Container restart: everything needed is in git; re-run `scripts/download_reels.sh` and continue from `TASKS.md`.

## Wake-ups
An hourly scheduled task wakes this session with: "Continue the 10-hour loop per LOOP.md". On each wake: if now > Loop end,
write the final summary to `research/FINAL_REPORT.md`, push, and stop; otherwise continue the current iteration.

## Final deliverables (at hour 10)
- `renders/best/`: the best reels made, with scores and side-by-side comparisons
- `research/virality_playbook.md`: the rules, each with evidence
- `research/FINAL_REPORT.md`: what worked, what didn't, cost, next steps
