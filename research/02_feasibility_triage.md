# Feasibility triage: which reels we try to make, and which we only learn from

Not every reel can be rebuilt in code. We don't skip the hard ones silently. Every reel gets a
**production label**, every label maps to a **feasibility tier**, and we cross that with **virality**
to decide where the 8-hour make loop spends its time.

## 1. Label each reel (vision + transcript, per reel)

From `analysis/<reel>/timeline_2s.jpg`, `contact_sheet.jpg`, `transcript.json`, `meta.json`:

| Field | Values |
|---|---|
| visual_source | ai_stills · ai_video · 3d_render · motion_graphics · stock_footage · live_action · screen_recording · mixed |
| motion_type | static/ken_burns · parallax_layers · camera_move_render · character_animation · lip_sync · real_camera |
| people | none · illustrated/AI characters · real person on camera · creator's own face/voice |
| audio | ai_voiceover · human_voiceover · music_only · trending/licensed track · original song · sfx-led |
| text | none · subtitles · kinetic_captions · title_cards |
| language | hi · en · hinglish · other |
| story_shape | myth retelling · "you're doing X wrong" · list/facts · mystery/twist · POV · emotional/devotional · explainer |
| hook (0–3s) | verbatim first line + first visual |

## 2. Feasibility tiers

| Tier | Meaning | How we make it | Cost/reel |
|---|---|---|---|
| **T1** | Code only | Remotion/ffmpeg: motion graphics, kinetic type, light FX, generated SFX | ~$0 |
| **T2** | Code + AI assets | AI stills (layered for parallax) + TTS voice + AI music, all animated/cut in code | ~$0.3–3 |
| **T3** | Needs AI video gen | Character motion, cinematic moving shots, lip-sync, from image-to-video models | ~$3–10, quality risk |
| **T4** | Not reproducible | Real people filmed, creator's own face/voice identity, real-event footage, a specific licensed trending song | — |

A reel's tier is the **highest tier any of its essential elements needs**. Before assigning T3/T4 we ask:
*is there a feasible substitute that keeps what makes it work?* (e.g. lip-sync → voiceover over stills;
licensed song → AI music with the same tempo/mood). If yes, it gets the lower tier and a note
`substitute: …`, and the make loop tests whether the substitute holds quality.

## 3. Decide where to spend effort

- Virality score per reel = `log(views / creator median views)` (removes follower-count effect).
  Likes are unreliable: many reels report `likes=3` (hidden likes), so likes are only used where real.
- Build a **tier × story_shape × virality** table.
- **Make loop targets:** high-virality cells in T1/T2 first, T3 only for 1–3 hero shots per reel.
- **T4 reels stay in the virality study.** Their hooks, story shapes and pacing are often transferable
  into T1/T2 formats even when the visuals are not.

## 4. Time-box the hard ones

Each make attempt is graded (frames side by side, cut rhythm, loudness curve, hook timing, captions).
If a reel doesn't reach the quality bar after **3 iterations**, it's marked `hard`, the blocking
element is recorded in `DECISIONS.md`, and the loop moves on. Hard reels are revisited only if a new
tool or approach removes the blocker.

## Output files
- `data/labels.csv`: one row per reel with the fields above plus tier and substitute note
- `research/03_virality_analysis.md`: what drives views, by tier and story shape
