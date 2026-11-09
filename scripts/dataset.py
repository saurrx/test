#!/usr/bin/env python3
"""Build data/features.csv: one row per reel with view stats, timing, and every analysed feature available.
virality = log(views / creator median), median taken over that creator's reels that are >= MIN_AGE days old."""
import csv, glob, json, math, re, statistics, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; MIN_AGE = 7; IST = timezone(timedelta(hours=5, minutes=30))
NUM = re.compile(r"\d"); Q = re.compile(r"\?|क्या|क्यों|कैसे|\b(why|what|how|who|did you|do you)\b", re.I)
NEG = re.compile(r"\b(wrong|never|don't|not|stop|mistake|galat)\b|गलत|कभी नहीं|मत ", re.I); YOU = re.compile(r"\b(you|your|aap|tum)\b|आप|तुम", re.I)

def text_feats(prefix, txt):
    txt = txt or ""; w = txt.split()
    return {f"{prefix}_words": len(w), f"{prefix}_has_number": int(bool(NUM.search(txt))), f"{prefix}_is_question": int(bool(Q.search(txt))),
            f"{prefix}_negation": int(bool(NEG.search(txt))), f"{prefix}_second_person": int(bool(YOU.search(txt)))}

def main():
    rows = []
    for f in glob.glob(str(ROOT / "data/creators/*.csv")):
        for r in csv.DictReader(open(f)):
            try: rows.append({"code": r["shortcode"], "creator": r["username"], "views": int(r["views"]), "likes": int(r["likes"]), "comments": int(r["comments"]), "duration_s": float(r["duration_s"] or 0), "created": int(r["created_unix"])})
            except ValueError: pass
    now = time.time(); by = {}
    for r in rows: r["age_days"] = round((now - r["created"]) / 86400, 1); by.setdefault(r["creator"], []).append(r)
    for c, items in by.items():
        old = [x["views"] for x in items if x["age_days"] >= MIN_AGE] or [x["views"] for x in items]; med = statistics.median(old) or 1
        items.sort(key=lambda x: x["created"])
        for i, r in enumerate(items):
            dt = datetime.fromtimestamp(r["created"], IST)
            r.update({"virality": round(math.log(max(r["views"], 1) / med), 4), "creator_median": med, "creator_n": len(items), "hour_ist": dt.hour, "weekday": dt.weekday(),
                      "likes_hidden": int(r["likes"] == 3), "gap_prev_h": round((r["created"] - items[i - 1]["created"]) / 3600, 1) if i else "",
                      "prev_virality": "", "eligible": int(r["age_days"] >= MIN_AGE)})
        for i, r in enumerate(items):
            if i: r["prev_virality"] = items[i - 1]["virality"]
            # detrended virality: views against the creator's 6 nearest-in-time OTHER reels (removes account growth and time trends)
            nb = [items[j]["views"] for j in range(max(0, i - 3), min(len(items), i + 4)) if j != i]
            r["virality_local"] = round(math.log(max(r["views"], 1) / (statistics.median(nb) or 1)), 4) if len(nb) >= 4 else ""
            # same, but the baseline leaves out the previous reel (for a clean momentum test)
            nb2 = [items[j]["views"] for j in range(max(0, i - 4), min(len(items), i + 4)) if j not in (i, i - 1)]
            r["virality_local_xprev"] = round(math.log(max(r["views"], 1) / (statistics.median(nb2) or 1)), 4) if len(nb2) >= 4 else ""
        for i, r in enumerate(items):
            # previous reel's own detrended score, with a baseline that leaves out THIS reel
            if i:
                nb3 = [items[j]["views"] for j in range(max(0, i - 5), min(len(items), i + 3)) if j not in (i, i - 1)]
                r["prev_virality_local"] = round(math.log(max(items[i - 1]["views"], 1) / (statistics.median(nb3) or 1)), 4) if len(nb3) >= 4 else ""
            else: r["prev_virality_local"] = ""
    idx = {r["code"]: r for r in rows}
    for d in (ROOT / "analysis").glob("*__*"):
        r = idx.get(d.name.split("__")[-1])
        if not r: continue
        try:
            m = json.loads((d / "meta.json").read_text()); t = json.loads((d / "transcript.json").read_text())
        except Exception: continue
        if m.get("analyzer_version", 1) < 3: continue
        segs = t.get("segments", []); first = " ".join(s["text"] for s in segs if s["start"] < 3.5); lo = [x[1] for x in m.get("loudness_lufs", []) if x[1] > -60]
        r.update({"analysed": 1, "cuts_per_10s": m.get("cuts_per_10s"), "first_cut_s": m.get("first_cut_s") or "", "view_changes_per_10s": m.get("view_changes_per_10s"),
                  "motion_mean": m.get("motion_mean"), "motion_first3s": m.get("motion_first3s"), "still_frac": round(m.get("still_seconds", 0) / max(m["duration"], 1), 3),
                  "lang": t.get("language"), "wpm": t.get("wpm") or "", "first_word_s": t.get("first_word_s") if t.get("first_word_s") is not None else "", "has_speech": int(t.get("word_count", 0) > 8),
                  "speech_frac": round(t.get("speech_seconds", 0) / max(m["duration"], 1), 3), "loud_mean": round(statistics.mean(lo), 1) if lo else "", "loud_sd": round(statistics.pstdev(lo), 2) if len(lo) > 2 else "",
                  "hook_text": first[:160].replace("\n", " ")})
        r.update(text_feats("hook", first))
    for f in glob.glob(str(ROOT / "data/reels/*/*.info.json")):
        r = idx.get(Path(f).name.split(".")[0])
        if not r: continue
        try: j = json.load(open(f))
        except Exception: continue
        cap = j.get("description") or ""
        r.update({"has_meta": 1, "caption_chars": len(cap), "caption_hashtags": cap.count("#"), "caption_lines": cap.count("\n") + 1, "caption_first": cap.split("\n")[0][:120].replace(",", " ")})
        r.update(text_feats("cap", cap.split("\n")[0]))
        low = cap.lower()
        r["cap_is_series"] = int(bool(re.search(r"\bpart\s*\d|\bpart[- ]?(one|two|three)|\bep(isode)?\s*\d|भाग|series|to be continued", low)))
        r["cap_cta_comment"] = int(bool(re.search(r"comment|कमेंट|type |likho|लिखो|बताओ|tell me", low)))
        r["cap_cta_follow"] = int(bool(re.search(r"follow|फ़ॉलो|फॉलो", low)))
        r["cap_cta_share"] = int(bool(re.search(r"share|send this|शेयर|भेजो", low)))
        for name, pat in {"shiva": r"shiv|mahadev|shankar|bholenath|शिव|महादेव", "ram": r"\bram\b|rama\b|ramayan|hanuman|sita|राम|हनुमान|सीता", "krishna": r"krishna|kanha|radha|mahabharat|arjun|gita|कृष्ण|महाभारत|अर्जुन|गीता"}.items():
            r[f"topic_{name}"] = int(bool(re.search(pat, low)))
    keys = []
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    with open(ROOT / "data/features.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(len(rows), "reels;", sum(1 for r in rows if r.get("analysed")), "analysed;", sum(1 for r in rows if r.get("has_meta")), "with caption;", sum(r["eligible"] for r in rows), "eligible (age>=7d)")

if __name__ == "__main__": main()
