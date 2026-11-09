# Views-prediction model

Ridge regression, leave-one-creator-out. A score of 0 means no predictive power; 1 would be perfect ranking.
The video rows use the balanced hit/flop sample, so their scores are optimistic for ordinary reels.

| Feature set | reels | creators | pooled Spearman | mean per-creator Spearman | creators with positive score |
|---|---|---|---|---|---|
| A timing + history (CSV only) | 571 | 17 | -0.01 | 0.21 | 11/14 |
| B + caption | 372 | 17 | -0.13 | 0.14 | 5/12 |
| C + video | 77 | 16 | 0.15 | 0.02 | 6/11 |
| D video only | 140 | 36 | 0.24 | 0.36 | 15/18 |

## Standardised weights (full-data fit; positive = more views)

**A timing + history (CSV only)**

- log_duration: +0.37
- prev_virality_local: +0.14
- log_gap: +0.08

**B + caption**

- log_caption_chars: +0.20
- cap_cta_follow: -0.18
- log_gap: +0.18
- cap_cta_comment: -0.14
- topic_ram: +0.13
- cap_is_series: +0.12
- topic_krishna: -0.12
- caption_hashtags: +0.10
- topic_shiva: +0.08
- log_duration: +0.06
- prev_virality_local: +0.01

**C + video**

- view_changes_per_10s: +1.26
- has_speech: +1.01
- loud_sd: -0.82
- wpm_z: -0.56
- cuts_per_10s: -0.52
- log_gap: +0.44
- log_duration: -0.33
- first_word_beat: +0.30
- prev_virality_local: -0.05
- motion_first3s: -0.03

**D video only**

- has_speech: +0.84
- view_changes_per_10s: +0.67
- loud_sd: -0.41
- first_word_beat: +0.31
- cuts_per_10s: -0.18
- motion_first3s: +0.12
- log_duration: -0.04
