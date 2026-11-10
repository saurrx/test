# Views-prediction model

Ridge regression, leave-one-creator-out. A score of 0 means no predictive power; 1 would be perfect ranking.
The video rows use the balanced hit/flop sample, so their scores are optimistic for ordinary reels.

| Feature set | reels | creators | pooled Spearman | mean per-creator Spearman | creators with positive score |
|---|---|---|---|---|---|
| A timing + history (CSV only) | 575 | 18 | 0.00 | 0.22 | 11/14 |
| B + caption | 571 | 18 | -0.08 | 0.04 | 7/14 |
| C + video | 148 | 17 | -0.01 | 0.19 | 9/13 |
| D video only | 218 | 36 | 0.08 | 0.22 | 13/19 |
| E video + first frame | 218 | 36 | 0.06 | 0.26 | 13/19 |
| F first frame only | 218 | 36 | -0.11 | 0.12 | 13/19 |

## Standardised weights (full-data fit; positive = more views)

**A timing + history (CSV only)**

- log_duration: +0.38
- prev_virality_local: +0.18
- log_gap: +0.09

**B + caption**

- log_duration: +0.26
- cap_cta_follow: -0.21
- log_caption_chars: +0.20
- topic_shiva: -0.16
- prev_virality_local: +0.16
- cap_is_series: +0.16
- topic_krishna: -0.07
- log_gap: +0.07
- topic_ram: +0.04
- cap_cta_comment: +0.04
- caption_hashtags: -0.00

**C + video**

- loud_sd: -0.79
- log_duration: +0.75
- view_changes_per_10s: +0.69
- first_word_beat: +0.46
- has_speech: +0.44
- cuts_per_10s: -0.39
- prev_virality_local: +0.36
- log_gap: +0.34
- motion_first3s: +0.32
- wpm_z: -0.15

**D video only**

- has_speech: +0.53
- view_changes_per_10s: +0.49
- log_duration: +0.42
- loud_sd: -0.40
- first_word_beat: +0.36
- motion_first3s: +0.29
- cuts_per_10s: -0.09

**E video + first frame**

- has_speech: +0.54
- view_changes_per_10s: +0.40
- loud_sd: -0.39
- log_duration: +0.37
- first_word_beat: +0.35
- motion_first3s: +0.31
- ff_luma: -0.22
- cuts_per_10s: -0.08
- ff_sat: -0.00

**F first frame only**

- ff_luma: -0.38
- ff_sat: +0.07
