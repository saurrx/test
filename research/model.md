# Views-prediction model

Ridge regression, leave-one-creator-out. A score of 0 means no predictive power; 1 would be perfect ranking.
The video rows use the balanced hit/flop sample, so their scores are optimistic for ordinary reels.

| Feature set | reels | creators | pooled Spearman | mean per-creator Spearman | creators with positive score |
|---|---|---|---|---|---|
| A timing + history (CSV only) | 571 | 17 | -0.01 | 0.21 | 11/14 |
| B + caption | 479 | 17 | -0.14 | 0.00 | 6/14 |
| C + video | 98 | 16 | 0.07 | 0.14 | 7/12 |
| D video only | 164 | 36 | 0.16 | 0.31 | 14/18 |
| E video + first frame | 164 | 36 | 0.12 | 0.27 | 12/18 |
| F first frame only | 164 | 36 | -0.06 | 0.13 | 9/18 |

## Standardised weights (full-data fit; positive = more views)

**A timing + history (CSV only)**

- log_duration: +0.37
- prev_virality_local: +0.14
- log_gap: +0.08

**B + caption**

- log_caption_chars: +0.26
- cap_cta_follow: -0.17
- cap_is_series: +0.15
- log_duration: +0.12
- log_gap: +0.12
- topic_krishna: -0.10
- topic_shiva: -0.09
- topic_ram: +0.07
- prev_virality_local: +0.06
- caption_hashtags: -0.01
- cap_cta_comment: -0.00

**C + video**

- has_speech: +1.10
- loud_sd: -0.98
- view_changes_per_10s: +0.92
- log_gap: +0.71
- cuts_per_10s: -0.61
- first_word_beat: +0.39
- wpm_z: -0.21
- prev_virality_local: +0.15
- log_duration: +0.07
- motion_first3s: +0.06

**D video only**

- has_speech: +0.86
- view_changes_per_10s: +0.60
- loud_sd: -0.42
- first_word_beat: +0.29
- cuts_per_10s: -0.16
- motion_first3s: +0.14
- log_duration: +0.03

**E video + first frame**

- has_speech: +0.86
- view_changes_per_10s: +0.52
- loud_sd: -0.41
- ff_luma: -0.33
- first_word_beat: +0.27
- cuts_per_10s: -0.17
- motion_first3s: +0.16
- ff_sat: -0.12
- log_duration: -0.01

**F first frame only**

- ff_luma: -0.49
- ff_sat: -0.06
