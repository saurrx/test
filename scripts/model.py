#!/usr/bin/env python3
"""Views-prediction model: ridge regression on standardised features, validated by leaving one creator out.
Outcome: virality = log(views / creator median). Score: Spearman correlation between predicted and actual on held-out
creators (pooled, and the mean of per-creator correlations). Writes research/model.md and data/model.json."""
import csv, json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
rows = [r for r in csv.DictReader(open(ROOT / "data/features.csv")) if r["eligible"] == "1"]
def num(r, k):
    v = r.get(k, "")
    return float(v) if v not in ("", None) else None
SETS = {
 "A timing + history (CSV only)": ["log_duration", "log_gap", "prev_virality_local"],
 "B + caption": ["log_duration", "log_gap", "prev_virality_local", "cap_is_series", "log_caption_chars", "caption_hashtags", "cap_cta_comment", "cap_cta_follow", "topic_shiva", "topic_ram", "topic_krishna"],
 "C + video": ["log_duration", "log_gap", "prev_virality_local", "has_speech", "view_changes_per_10s", "cuts_per_10s", "first_word_beat", "motion_first3s", "wpm_z", "loud_sd"],
 "D video only": ["log_duration", "has_speech", "view_changes_per_10s", "cuts_per_10s", "first_word_beat", "motion_first3s", "loud_sd"],
}
for r in rows:
    d, g, c, fw, w = num(r, "duration_s"), num(r, "gap_prev_h"), num(r, "caption_chars"), num(r, "first_word_s"), num(r, "wpm")
    r["log_duration"] = math.log(max(d, 1)) if d else ""; r["log_gap"] = math.log(max(g, 0.5)) if g is not None else ""
    r["log_caption_chars"] = math.log(1 + c) if c is not None else ""
    r["first_word_beat"] = (1.0 if 0.15 <= fw <= 2 else 0.0) if fw is not None else (0.0 if r.get("analysed") == "1" else "")
    r["wpm_z"] = (w - 150) / 30 if w else (0.0 if r.get("analysed") == "1" else "")
def rank(v):
    o = np.argsort(v); r = np.empty(len(v)); r[o] = np.arange(len(v)); return r
def spearman(a, b):
    if len(a) < 4 or np.std(a) == 0 or np.std(b) == 0: return None
    return float(np.corrcoef(rank(np.array(a)), rank(np.array(b)))[0, 1])
def ridge(X, y, lam):
    return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)
out, lines = {}, ["# Views-prediction model", "", "Ridge regression, leave-one-creator-out. A score of 0 means no predictive power; 1 would be perfect ranking.",
                   "The video rows use the balanced hit/flop sample, so their scores are optimistic for ordinary reels.", "",
                   "| Feature set | reels | creators | pooled Spearman | mean per-creator Spearman | creators with positive score |", "|---|---|---|---|---|---|"]
for name, feats in SETS.items():
    data = [r for r in rows if all(r.get(f, "") != "" for f in feats)]
    if len(data) < 40: lines.append(f"| {name} | {len(data)} | - | not enough data | - | - |"); continue
    X = np.array([[float(r[f]) for f in feats] for r in data]); y = np.array([float(r["virality"]) for r in data]); cr = np.array([r["creator"] for r in data])
    preds = np.zeros(len(y)); per = []
    for c in sorted(set(cr)):
        te = cr == c; tr = ~te
        if te.sum() < 1 or tr.sum() < 20: continue
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        w = ridge(np.c_[np.ones(tr.sum()), (X[tr] - mu) / sd], y[tr], 3.0)
        preds[te] = np.c_[np.ones(te.sum()), (X[te] - mu) / sd] @ w
        s = spearman(preds[te], y[te])
        if s is not None: per.append(s)
    pooled = spearman(preds, y); mu, sd = X.mean(0), X.std(0) + 1e-9
    w = ridge(np.c_[np.ones(len(y)), (X - mu) / sd], y, 3.0)
    out[name] = {"n": len(data), "creators": len(set(cr)), "pooled_spearman": round(pooled, 3), "mean_creator_spearman": round(float(np.mean(per)), 3) if per else None,
                 "features": feats, "mean": mu.tolist(), "sd": sd.tolist(), "weights": w.tolist()}
    lines.append(f"| {name} | {len(data)} | {len(set(cr))} | {pooled:.2f} | {np.mean(per):.2f} | {sum(1 for s in per if s > 0)}/{len(per)} |")
    lines += [""] if False else []
lines += ["", "## Standardised weights (full-data fit; positive = more views)"]
for name, m in out.items():
    lines += ["", f"**{name}**", ""] + [f"- {f}: {w:+.2f}" for f, w in sorted(zip(m["features"], m["weights"][1:]), key=lambda x: -abs(x[1]))]
(ROOT / "research/model.md").write_text("\n".join(lines) + "\n"); (ROOT / "data/model.json").write_text(json.dumps(out, indent=1)); print("\n".join(lines))
