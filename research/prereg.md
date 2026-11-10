# Pre-registered hypotheses

Written 2026-11-09 20:29 UTC, before any test was run. Each test is run once with the command shown
(`scripts/vtest.py`), on reels at least 7 days old, comparing reels **within the same creator**. Results, including
nulls, go to `research/tests.jsonl` and `research/tests_table.md`. A rule is `evidenced` only if its corrected
q-value (Benjamini–Hochberg over every test run) is ≤ 0.10 **and** its sign survives leaving any one creator out.
Tests that need analysed video are re-run once when at least 150 reels are analysed; the later run replaces the earlier.

## Virality (data tests)
| id | Claim | Expected | Command |
|---|---|---|---|
| V1 | Shorter reels get more views than the same creator's longer reels | negative | `run V1 duration_s --continuous` |
| V2 | Reels posted 18:00–23:59 IST do better | positive | `run V2 hour_ist --split 18` |
| V3 | Weekend posts do better | positive | `run V3 weekday --split 5` |
| V4 | A longer gap since the previous post helps | positive | `run V4 gap_prev_h --split median` |
| V5 | Hits cluster: a reel does better when the creator's previous reel did | positive | `run V5 prev_virality --continuous` |
| V6 | A question in the first 3.5 s of speech helps | positive | `run V6 hook_is_question --split binary` |
| V7 | A number in the first 3.5 s of speech helps | positive | `run V7 hook_has_number --split binary` |
| V8 | A negation / "you're doing it wrong" opening helps | positive | `run V8 hook_negation --split binary` |
| V9 | Speaking sooner helps (time to first word) | negative | `run V9 first_word_s --continuous` |
| V10 | Faster speech helps | positive | `run V10 wpm --continuous --where has_speech==1` |
| V11 | More cuts per 10 s help | positive | `run V11 cuts_per_10s --continuous` |
| V12 | More visual change per 10 s helps (cuts + dissolves + camera moves) | positive | `run V12 view_changes_per_10s --continuous` |
| V13 | More motion in the first 3 s helps | positive | `run V13 motion_first3s --continuous` |
| V14 | Shorter Instagram captions help | negative | `run V14 caption_chars --continuous` |
| V15 | Hashtag count makes no difference | null | `run V15 caption_hashtags --continuous` |
| V16 | Addressing the viewer ("you/aap/tum") in the opening helps | positive | `run V16 hook_second_person --split binary` |
| V17 | More loudness variation (drops and hits) helps | positive | `run V17 loud_sd --continuous` |
| V18 | Voice-led reels beat music-only reels | positive | `run V18 has_speech --split binary` |

### Follow-ups registered 2026-11-09 20:33 UTC, after V1–V5 and before running these
V1 came out opposite to the prediction (longer reels do better) and V5 showed strong clustering, so both may be
account-growth trends. These repeat them on **detrended** views: each reel against the creator's 6 nearest-in-time
other reels (`virality_local`).

| id | Claim | Expected | Command |
|---|---|---|---|
| V19 | Longer reels still do better after removing time trends | positive | `run V19 duration_s --continuous --outcome virality_local` |
| V20 | A hit is followed by another hit even after removing trends (series / momentum effect) | positive | `run V20 prev_virality_local --continuous --outcome virality_local` |
| V21 | Longer gap since the previous post helps, detrended | positive | `run V21 gap_prev_h --split median --outcome virality_local` |
| V22 | Momentum, clean version: previous reel's detrended views vs this reel's views against a baseline that excludes the previous reel (registered 20:36 after spotting the flaw in V20; needs a new feature `virality_local_xprev`) | positive | `run V22 prev_virality_local --continuous --outcome virality_local_xprev` |

### Caption-content tests registered 2026-11-09 21:45 UTC (before running)
| id | Claim | Expected | Command |
|---|---|---|---|
| V23 | Reels whose caption marks them as part of a series ("part 2", "भाग") do better | positive | `run V23 cap_is_series --split binary` |
| V24 | A "comment ..." call to action in the caption goes with more views | positive | `run V24 cap_cta_comment --split binary` |
| V25 | A "follow" call to action in the caption makes no difference | null | `run V25 cap_cta_follow --split binary` |
| V26 | A "share / send this" call to action goes with more views | positive | `run V26 cap_cta_share --split binary` |
| V27–V29 | Topic (exploratory, no prediction): Shiva / Ram-Hanuman / Krishna-Mahabharat mentions vs the creator's other reels | none | `run V27 topic_shiva --split binary`, `V28 topic_ram`, `V29 topic_krishna` |

### Hook-type tests registered 2026-11-09 22:36 UTC (before labelling)
The keyword detector could not test V6–V8 and V16. Instead a model labels each reel's opening line (first 6 s of speech)
without seeing views or creator: `data/hook_lines.tsv` → `data/hook_labels.csv`. Each label is then tested within creator.

| id | Claim | Expected | Command |
|---|---|---|---|
| V31 | Contradiction / "you're doing it wrong" / myth-busting openings do better | positive | `run V31 hook_contradiction --split binary` |
| V32 | Question openings do better | positive | `run V32 hook_question --split binary` |
| V33 | Openings with a concrete number or scale ("5,000 men") do better | positive | `run V33 hook_number --split binary` |
| V34 | Openings with explicit stakes or danger (death, curse, war, loss) do better | positive | `run V34 hook_stakes --split binary` |
| V35 | Openings that address the viewer directly ("you", "aap") do better | positive | `run V35 hook_you --split binary` |
| V36 | Plain scene-setting openings ("Once there was a king...") do worse | negative | `run V36 hook_plain --split binary` |

### More CSV-only tests registered 2026-11-09 22:41 UTC (before running)
| id | Claim | Expected | Command |
|---|---|---|---|
| V40 | Reels of 60–90 s beat the same creator's other lengths (the sweet spot seen in F1) | positive | `run V40 dur_60_90 --split binary --outcome virality_local` |
| V41 | A reel posted within 12 h of another by the same creator does worse (bursts split attention) | negative | `run V41 burst --split binary --outcome virality_local` |
| V37 | Reels with likes hidden do no better or worse | null | `run V37 likes_hidden --split binary` |

### Reach and engagement tests registered 2026-11-09 23:27 UTC (before running)
These describe what a viral reel looks like afterwards; they are not levers.
| id | Claim | Expected | Command |
|---|---|---|---|
| V43 | A creator's viral reels have a LOWER like rate (likes per view): they reach people outside the fan base | negative | `run V43 like_rate --continuous` |
| V44 | A creator's viral reels have a LOWER comment rate (comments per 1,000 views) | negative | `run V44 comment_rate --continuous` |
| V45 | Later reels in a creator's history do better than earlier ones (account growth) | positive | `run V45 reel_index_frac --continuous` |
| V46 | A brighter first frame does better (real-reel version of craft belief C1) | positive | `run V46 ff_luma --continuous` |
| V47 | A more colourful (saturated) first frame does better | positive | `run V47 ff_sat --continuous` |
| V48 | A first frame with more contrast (spread of brightness) does better | positive | `run V48 ff_contrast --continuous` |
| V49 | A first frame with more fine detail in the top/middle third (proxy for on-screen text) does better | positive | `run V49 ff_detail --continuous` |
| V50 | Reels whose last 10 s promise a next part or tell the viewer to follow for more do better (model-labelled ending, blind to views) | positive | `run V50 end_next --split binary` |
| V51 | Reels that end on a question to the viewer do better | positive | `run V51 end_question --split binary` |
| V52 | Reels that end on a moral, lesson or blessing do worse than those ending on a twist or open loop | negative | `run V52 end_moral --split binary` |
| V53 | Reels that end by asking for comments ("comment Jai Shri Ram", "type yes") do no better (matches F8, F18) | null | `run V53 end_comment --split binary` |

## Craft (blind judge tournaments in the hook lab)
Each is tested by rendering matched variants that differ only in the named factor and ranking them blind (3 judges).
These can only ever produce `prior` rules about craft, unless judge calibration shows the judge predicts real views.

| id | Claim |
|---|---|
| C1 | A bright, high-contrast first frame beats a dark first frame |
| C2 | A big number on screen in the first second beats no number |
| C3 | A "you've been doing X wrong" line beats a neutral statement of the same fact |
| C4 | Motion from frame 1 (punch-in or drawing light) beats a static first second |
| C5 | Bold pop captions beat serif captions in the flat lane; serif beats pop in the glow lane |
| C6 | A human figure in the first frame beats an object-only first frame |
| C7 | Three shots in the first 5 s beat one continuous shot |
| C8 | A red "wrong" cross / visual contradiction in the first 2 s beats a neutral demonstration |

## Judge calibration
Before any craft result is called a virality signal: the judge must pick the real hit over the same creator's flop
(first 3 s only) clearly above chance (one-sided binomial p ≤ 0.05 on at least 20 pairs). `scripts/calib.py`.
