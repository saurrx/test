# Review of LOOP.md v2, by Claude Fable 5.2

_2026-11-09. Read-only review by a separate cloud session (session_01Gy5RgGKoGyUaVwvMW6jtJd). The platform reports `last_served_model: claude-fable-5-2`. Summary of the full report the reviewer sent to the runner session._

## Verdict
The plan is a sound production checklist, but it is not yet a self-improving loop. It has no fixed yardstick, so "better each iteration" can't be verified. The virality data can't support findings yet: video-level features exist for only 21 seed reels, almost all of them top hits. The target of 8–12 iterations is roughly 2–3x optimistic.

## Blind spots (ranked)
1. **No fixed yardstick.** Each make is a different reel scored 1–10 by a fresh grader, so noise alone passes the "beat best on one dimension" rule. Fix: 3 frozen benchmark briefs, re-rendered at checkpoints, with blind pairwise judging and deterministic QC metrics.
2. **The virality sample is weak.**
   - 832 reels from 19 creators; 3 creators make up 44% of rows. The top 10% of reels hold 80% of views. The SD of log-relative views is 1.91, so a 1.65x effect needs about 230 reels per group.
   - 21% of reels are under 7 days old and still gaining views (age vs normalised views: Spearman −0.29).
   - The seed reels are all hits, with no flops for contrast.
   - The shot detector undercounts cuts, and Whisper `small` mislabels the language of Hindi reels.
   - Fix: allow null findings, analyse only reels ≥ 7 days old, use within-creator permutation tests, leave-one-creator-out validation and Benjamini–Hochberg correction, and label rules `evidenced` vs `prior`.
3. **The AI grader measures craft, not virality.** It sees low-res frames with no motion and no audio, and there's a Goodhart risk. Fix: calibrate it on hit/flop pairs, judge pairwise only, give it 540 px frames, the first 3 s at 4 fps and the loudness curve, and re-judge a frozen anchor set to catch drift.
4. **Renders and paid audio are gitignored, so they're lost on a container reclaim.** Fix: add `.gitignore` exceptions for `renders/best/` and `makes/**/audio/`, and commit reference frame strips for the benchmark reels.
5. **Throughput.** Realistically 4–6 finished reels in 10 h, not 8–12. Fix: draft at 540p and 15 fps, and do most iteration on the first 5 s.
6. **Painterly references can't be matched in code.** Fix: two code-native lanes, "glow temple and sacred geometry" and "flat-vector story with silhouettes", plus geometric folk styles (Warli, shadow puppetry, yantras). C3 becomes study-only.
7. **Smaller issues.**
   - "Never stop for budget" contradicts CLAUDE.md's $0.10 rule.
   - Two runners share the branch.
   - Rebuilding another creator's script is a private benchmark only, not something to post.
   - An hourly wake-up is too coarse to recover a stalled iteration.

## 10x levers
1. A Phase 0 harness, before any reel is made: QC script, pairwise judge, benchmark briefs, component gallery.
2. A hook lab: 8–12 variants of the first 5 s per iteration, judged in a blind tournament.
3. A style bank and component library, so a reel becomes JSON over reusable components.
4. A metadata-only scrape of all 832 reels from the PC (captions, cover frames, audio titles).
5. A balanced video sample: 3 hits and 3 flops per creator, all ≥ 7 days old. This replaces the extremes-only ordering.
6. Pre-registered hypotheses in `research/prereg.md`, with nulls reported.
7. The PC GPU for three.js and shader rendering.
8. A real audience signal: post 4–6 originals as Instagram Trial Reels and log views at 24 h and 72 h.

## Owner decisions
1. Post test reels (yes/no).
2. Tailscale SSH accept rule for `arch`, plus Instagram cookies.
3. Confirm the two code lanes, and top up Treg to about $3.
