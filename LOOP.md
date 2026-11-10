# 9-hour self-improving reel loop (v3, awaiting owner "go")

Status: **FINISHED** (ran 2026-11-09T19:59Z to 2026-11-10T04:59Z). Results: `research/FINAL_REPORT.md`.
Runner: session_01Gy5RgGBibuvxR5H9sESUN3.

- Loop start (UTC): 2026-11-09T19:59Z
- Loop end (UTC): 2026-11-10T04:59Z

v3 folds in the Fable 5.2 review (`research/loop_review_fable52.md`) and the owner's answers:
no posting for now, no Treg top-up, the PC is available, Fable 5.2 runs the loop.

## Goals
1. **Make best-in-class reels in code.** Measured by blind side-by-side wins against earlier versions and against
   the reference reels' hooks, plus automatic quality checks. Not by a 1–10 score.
2. **Understand virality well enough to program it.** With no posting, this means *predicting* views: every claim
   is tested on reels held out of the analysis. Each iteration tests one hypothesis written down in advance.
   A null result is a valid result. Rules are labelled `evidenced` (passed the held-out test) or `prior` (craft belief).
3. **Never block.** Every blocker gets a workaround and a `BLOCKER:` log entry. A watchdog keeps the loop alive.

## Hard rules
- **Visuals are 100% code**: Remotion/React, SVG, Canvas, shaders, three.js, procedural textures, fonts, vector icons.
  No AI images or video, stock footage, photos, or frames from other reels.
- **Audio from anywhere**, within $0.58 of Treg credit (no top-up): Gemini TTS for voice (measured $0.0006 per 3 s,
  about $0.015 per minute), at most 3 Lyria music clips ($0.04 each) reused across reels, everything else free:
  `edge-tts` on the PC (Hindi and Indian-English voices with timestamps, tested) and code-made music and SFX.
  Keep a $0.10 reserve. Below it, switch to free audio only and keep going.
- **Rebuilds of other creators' reels are private benchmarks.** Only originals go in the final "ready to post" queue.
- **One runner.** Only this session runs the loop on this branch.

## Machines and models
| Where | Does what |
|---|---|
| This cloud session (Fable 5.2) | Runs the loop: plans, writes code, integrates, commits. |
| Owner's PC `gamer@arch` over Tailscale (16 threads, 31 GB, RTX 4060) | Instagram downloads, transcription, analysis, and **all rendering** (system Chromium; smoke clip renders in 8 s). Driven with `scripts/pc` and `scripts/pc_sync.sh`. |
| Subagents | Builders inherit the session model (Fable 5.2). Judges run on a **different model** (Sonnet) and never see which variant is which. Routine data work uses Haiku or Sonnet. |

Usage is the scarcest resource (the weekly limit resets about 05:00 UTC). So: the runner builds most things itself,
subagents are used only for parallel hook variants and for blind judging, and judges get small, cropped inputs.

If the PC drops: fall back to cloud rendering (4 vCPUs, slower drafts) and the reels already analysed. If the
container is reclaimed: Tailscale needs a new login link from the owner; until then the loop runs cloud-only.

## Treg is off for the rest of the loop (2026-11-09 22:00)
Treg calls can still raise a permission prompt, and a prompt would stall an unattended loop. From now on the loop
makes **no Treg calls**: voice is free `edge-tts` on the PC, music is the two saved Lyria loops plus `scripts/synth.py`.

## Two visual lanes (what code is good at)
- **Lane A, "glow temple"**: dark scene, simple 3D or layered 2D forms, glowing light trails, sacred geometry
  (yantras, mandalas), serif captions. Reference: therishikatha (4.8M-view Aarti reel).
- **Lane B, "flat story"**: flat vector scenes, silhouettes, shadow-puppet and Warli-style figures, bold kinetic
  captions in Hindi/Hinglish/English. Reference: anchorlinedigital.
- Painterly and watercolour references (visionmachina, artandartists_ai) are **study only**: their hooks, scripts
  and pacing feed the virality research, but we don't try to imitate the look. No realistic deity faces or hands.

## Phase 0: build the yardstick (first 75 minutes, no reel is made)
1. `scripts/qc.py`: automatic checks on any render. Caption contrast and safe area, Devanagari renders, loudness
   (target −14 LUFS), words per minute, time to first motion / first word / first text, dead air, still seconds,
   per-second motion, caption-to-voice sync. Output: JSON with pass/fail per check.
2. `scripts/judge_pair.py` + judge prompt: blind pairwise comparison of two clips (540 px frames, first 3 s at
   4 fps, loudness curve, script). Order randomised, 3 judges, majority wins.
3. **Calibrate the judge**: give it pairs of a hit and a flop from the same creator (hook frames + first line only)
   and record how often it picks the hit. If that is near 50%, its verdicts are labelled "craft", never "virality".
4. `bench/briefs/*.json`: 3 fixed briefs that never change (Lane A English, Lane B Hinglish, one Hindi).
   Reference frame strips for them are committed.
5. Component library skeleton in `remotion/src/lib/` and a `Gallery` composition: `KineticCaption` (Devanagari
   font loaded), `GlowTrail`, `Yantra`, `TempleScene`, `SilhouetteRig`, `FlatScene`, `FilmGrain`, `Transition`.
   A reel is a props JSON over these components.
6. `research/prereg.md`: 15+ hypotheses, each with its metric and test, written before looking at results.
7. Render the 3 benchmark briefs once = **checkpoint 0**, the baseline everything is compared against.

## Iteration (45-minute hard cap; the clock ends it, not the output)
1. **Pick one hypothesis** from `prereg.md` (craft or virality). Write the expected result first.
2. **Hook lab.** Build 8–12 variants of the *first 5 seconds* from props JSON (line, first frame, motion, caption
   style, sound). Render drafts on the PC at 540×960. Run `qc.py`, drop failures. Blind pairwise tournament
   including the previous champion and, for rebuilds, the reference reel's own first 5 seconds.
3. **Promote** (every 2nd iteration): extend the champion hook to a full 30–60 s reel. Voice first, word timings
   drive the cuts, then music and SFX. Draft at 540p, final once at 1080×1920. Save to `renders/best/`.
4. **Virality test.** Run the one pre-registered test: within-creator comparison, only reels ≥ 7 days old,
   permutation p-value, corrected for all tests so far (Benjamini–Hochberg), then checked leaving one creator out.
   Record the result in `research/03_virality_analysis.md`, null or not. Update `research/virality_playbook.md`.
5. **Checkpoint** (every 3rd iteration): re-render the 3 benchmark briefs with the current library. Pairwise vs the
   last checkpoint, 3 judges × 3 briefs. Re-judge a frozen anchor pair to detect judge drift.
   **"Improved" = wins more than 60% of judgments and no QC regressions.** Log the win rate in `makes/LOG.md`.
6. **Commit and push**: code, props, QC JSON, judgments, best mp4s, audio. Update `TASKS.md` and `DECISIONS.md`.

Stop rule: two checkpoints in a row without improvement → change lane or rebuild the weakest component, and log why.

### Schedule (9 hours)
| Time | Work |
|---|---|
| 0:00–1:15 | Phase 0 |
| 1:15–8:30 | About 9 iterations: checkpoints after iterations 3, 6, 9; full reels in iterations 2, 4, 6, 8 |
| from ~4:00 | Once ≥ 150 reels are analysed: fit a views-prediction model (hook text, duration, pace, motion, cover), validated leaving one creator out. Report its accuracy honestly; use it to rank our variants as "predicted" |
| 8:30–9:00 | Final checkpoint, `research/FINAL_REPORT.md`, ranked queue of originals, push |

Expected output: 4–5 finished reels, about 80–100 judged hook variants, 9 tested hypotheses, 4 checkpoints.

## Background work (runs the whole time on the PC)
`reels-worker` (systemd user unit on the PC) downloads reels in a balanced order (per creator: 3 biggest hits and
3 biggest flops at least a week old first, 116 reels; then the rest) and analyses each one: cuts, view changes,
motion, loudness, Hindi-aware transcript with word timings, first frame, 3-second hook strip. About 1 reel per
minute. `scripts/pc_sync.sh pull` brings results into git every iteration.

## Staying alive for 9 hours
- **Watchdog wake-ups**: two hourly scheduled tasks, 30 minutes apart, fire into this session. Each one checks the
  clock, `TASKS.md`, the PC worker, Tailscale, the last commit time and the Treg balance, fixes what is broken,
  and continues the iteration. After the loop end they write the final report and are disabled.
- **Unblocker agent**: when a step fails twice, a background subagent takes that one blocker (with the error and
  what was tried) while the runner moves to the next step. Its fix is merged at the next integrate step.
- **State in git**: `TASKS.md` always says the current iteration, step and next action. Renders and paid audio are
  committed (`renders/best/`, `makes/**/audio/`), so a restart loses nothing.
- **Known limits I cannot remove**: the Claude usage limit (a paused session resumes at the reset), and a container
  reclaim needing a new Tailscale login (the loop continues cloud-only until then).

## Blocker playbook
| Blocker | Workaround |
|---|---|
| Instagram blocks the PC | Back off 30 min (built in); set `COOKIES_BROWSER=firefox` on the worker; use reels already downloaded |
| PC unreachable | Cloud rendering and cloud analysis; retry Tailscale each wake |
| Treg low or refused | `edge-tts` voices, code-made music; never below the $0.10 reserve |
| Render slow or crashing | 540p drafts, lower concurrency, bake shader backgrounds to 2D canvas |
| Missing font / library | npm (`@remotion/google-fonts`, `@fontsource/*`); never image assets |
| Judge unreliable (calibration ≈ 50%, or drift) | Label verdicts "craft only"; lean on QC metrics and the views model |
| Usage running out | Drop to 1 judge + QC, fewer variants (6), no parallel builders |

## Final deliverables
- `renders/best/`: finished reels with QC reports and their win records
- `remotion/src/lib/`: the reusable code-visual library, plus the `Gallery`
- `research/virality_playbook.md`: rules labelled `evidenced` or `prior`, each with its evidence
- `research/03_virality_analysis.md`: every pre-registered test, including nulls; the views model and its accuracy
- `research/FINAL_REPORT.md`: what improved (checkpoint win rates), what didn't, cost, and a ranked queue of
  originals ready for the owner to post if they choose
