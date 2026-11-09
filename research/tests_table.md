| id | feature | test | n | creators | effect | p | q (BH) | sign agree | LOO stable | status |
|---|---|---|---|---|---|---|---|---|---|---|
| V1 | duration_s | spearman | 657 | 18 | rho 0.2206 | 0.0002 | 0.002 | 14/18 | True | evidenced |
| V5 | prev_virality | spearman | 619 | 15 | rho 0.5282 | 0.0002 | 0.002 | 12/15 | True | evidenced |
| V20 | prev_virality_local | spearman | 590 | 14 | rho -0.1692 | 0.0002 | 0.002 | 9/14 | True | evidenced |
| V43 | like_rate | spearman | 632 | 17 | rho 0.3996 | 0.0002 | 0.002 | 15/17 | True | evidenced |
| V45 | reel_index_frac | spearman | 658 | 18 | rho 0.4867 | 0.0002 | 0.002 | 12/18 | True | evidenced |
| V22 | prev_virality_local | spearman | 570 | 13 | rho 0.1691 | 0.0004 | 0.003 | 11/13 | True | evidenced |
| V44 | comment_rate | spearman | 658 | 18 | rho -0.1355 | 0.0008 | 0.005 | 12/18 | True | evidenced |
| V23 | cap_is_series | split:binary | 324 | 7 | 2.6x | 0.0016 | 0.008 | 6/7 | True | evidenced |
| V18 | has_speech | split:binary | 140 | 5 | 39.36x | 0.0038 | 0.017 | 5/5 | True | evidenced |
| V19 | duration_s | spearman | 609 | 15 | rho 0.1104 | 0.007 | 0.029 | 13/15 | True | evidenced |
| V21 | gap_prev_h | split:median | 609 | 17 | 1.38x | 0.0126 | 0.047 | 11/17 | True | evidenced |
| V12 | view_changes_per_10s | spearman | 140 | 16 | rho 0.2516 | 0.0194 | 0.066 | 11/16 | True | evidenced |
| V29 | topic_krishna | split:binary | 324 | 4 | 0.44x | 0.0234 | 0.068 | 3/4 | True | evidenced |
| V9 | first_word_s | spearman | 128 | 13 | rho 0.2709 | 0.024 | 0.068 | 9/13 | True | evidenced |
| V27 | topic_shiva | split:binary | 324 | 5 | 2.27x | 0.0248 | 0.068 | 3/5 | True | evidenced |
| V40 | dur_60_90 | split:binary | 610 | 11 | 1.42x | 0.0288 | 0.074 | 7/11 | True | evidenced |
| V32 | hook_question | split:binary | 92 | 1 | 0.02x | 0.0476 | 0.11 | 1/1 | True | suggestive |
| V14 | caption_chars | spearman | 324 | 17 | rho 0.119 | 0.0484 | 0.11 | 10/17 | True | suggestive |
| V7 | hook_has_number | split:binary | 140 | 3 | 0.07x | 0.0942 | 0.198 | 3/3 | True | null |
| V41 | burst | split:binary | 610 | 9 | 0.69x | 0.0966 | 0.198 | 5/9 | True | null |
| V25 | cap_cta_follow | split:binary | 324 | 6 | 1.65x | 0.1126 | 0.22 | 4/6 | False | null |
| V4 | gap_prev_h | split:median | 619 | 18 | 1.27x | 0.1192 | 0.222 | 11/18 | True | null |
| V10 | wpm | spearman | 114 | 11 | rho -0.1935 | 0.1376 | 0.24 | 7/11 | True | null |
| V36 | hook_plain | split:binary | 92 | 6 | 3.76x | 0.1402 | 0.24 | 4/6 | True | null |
| V24 | cap_cta_comment | split:binary | 324 | 8 | 0.65x | 0.2256 | 0.37 | 6/8 | False | null |
| V35 | hook_you | split:binary | 92 | 2 | 6.21x | 0.2412 | 0.38 | 1/2 | False | null |
| V15 | caption_hashtags | spearman | 324 | 11 | rho 0.057 | 0.3751 | 0.57 | 6/11 | False | null |
| V8 | hook_negation | split:binary | 140 | 3 | 4.73x | 0.3909 | 0.572 | 2/3 | False | null |
| V11 | cuts_per_10s | spearman | 140 | 16 | rho 0.0856 | 0.4269 | 0.604 | 11/16 | True | null |
| V33 | hook_number | split:binary | 92 | 4 | 0.38x | 0.4425 | 0.605 | 2/4 | True | null |
| V17 | loud_sd | spearman | 140 | 16 | rho 0.0784 | 0.4571 | 0.605 | 9/16 | True | null |
| V26 | cap_cta_share | split:binary | 324 | 5 | 1.28x | 0.5327 | 0.683 | 3/5 | False | null |
| V16 | hook_second_person | split:binary | 140 | 6 | 1.98x | 0.5519 | 0.686 | 3/6 | True | null |
| V6 | hook_is_question | split:binary | 140 | 2 | 3.17x | 0.5933 | 0.703 | 2/2 | True | null |
| V37 | likes_hidden | split:binary | 658 | 4 | 1.31x | 0.5999 | 0.703 | 2/4 | False | null |
| V28 | topic_ram | split:binary | 324 | 3 | 1.11x | 0.6979 | 0.795 | 2/3 | False | null |
| V3 | weekday | split:5 | 657 | 17 | 0.95x | 0.7225 | 0.801 | 10/17 | False | null |
| V34 | hook_stakes | split:binary | 92 | 7 | 1.24x | 0.8252 | 0.875 | 3/7 | False | null |
| V13 | motion_first3s | spearman | 140 | 16 | rho 0.0237 | 0.8332 | 0.875 | 9/16 | False | null |
| V2 | hour_ist | split:18 | 657 | 15 | 1.03x | 0.8534 | 0.875 | 7/15 | False | null |
| V31 | hook_contradiction | split:binary | 92 | 1 | 0.61x | 0.9324 | 0.932 | 1/1 | True | null |
