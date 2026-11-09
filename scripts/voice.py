#!/usr/bin/env python3
"""Voice tools. Run ON THE PC inside ~/reels-loop/repo with ../.venv/bin/python.
  voice.py tts   <out_base> <voice> <rate> "<text>"   free edge-tts voice -> <out_base>.mp3 + <out_base>.words.json
  voice.py align <audio> <out_base> <lang> "<text>"   any audio + its script -> <out_base>.words.json (whisper word times
                                                      mapped back onto the exact script words)
Words JSON: [{"s": sec, "e": sec, "w": "word"}], plus a trailing-silence-trimmed duration printed to stdout.
Emphasis: wrap a word in *stars*; it is spoken normally and marked "emph": true.
Transliteration: write spoken|SHOWN (e.g. पाँच|PAANCH) to speak one form and caption another."""
import asyncio, difflib, json, re, subprocess, sys

def split_script(text):
    toks = []
    for raw in text.split():
        emph = "*" in raw; raw = raw.replace("*", "")
        spoken, _, disp = raw.partition("|")  # "पाँच|PAANCH": speak the left side, show the right side
        toks.append({"w": disp or spoken, "say": spoken, "emph": emph})
    return toks

def norm(w): return re.sub(r"[^\wऀ-ॿ]", "", w.lower())

def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def map_times(script, timed):
    """timed: [(s, e, word)] from TTS boundaries or whisper. Map onto script tokens; interpolate where unmatched."""
    a = [norm(t["say"]) for t in script]; b = [norm(w) for _, _, w in timed]
    out = [None] * len(script)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): out[i1 + k] = (timed[j1 + k][0], timed[j1 + k][1])
        elif tag == "replace" and j2 > j1:
            s, e = timed[j1][0], timed[j2 - 1][1]; n = i2 - i1
            for k in range(n): out[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
    last_e = 0.0
    for i, o in enumerate(out):
        if o is None:
            nxt = next((x for x in out[i + 1:] if x), None); e = nxt[0] if nxt else last_e + 0.3
            out[i] = (last_e, max(last_e + 0.12, e))
        last_e = out[i][1]
    res = []
    for t, (s, e) in zip(script, out):
        d = {"s": round(s, 3), "e": round(max(e, s + 0.08), 3), "w": t["w"]}
        if t["emph"]: d["emph"] = True
        res.append(d)
    return res

async def tts(out, voice, rate, text):
    import edge_tts
    script = split_script(text); plain = " ".join(t["say"] for t in script)
    com = edge_tts.Communicate(plain, voice, rate=rate, boundary="WordBoundary")
    timed = []
    with open(out + ".mp3", "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary": timed.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    words = map_times(script, timed) if timed else None
    if not words: return align(out + ".mp3", out, "hi" if re.search(r"[ऀ-ॿ]", text) else "en", text)
    json.dump(words, open(out + ".words.json", "w"), ensure_ascii=False)
    print(json.dumps({"audio": out + ".mp3", "duration": round(duration(out + ".mp3"), 2), "words": len(words), "last_word_end": words[-1]["e"]}))

def align(audio, out, lang, text):
    from faster_whisper import WhisperModel
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=6)
    segs, _ = m.transcribe(audio, language=lang, word_timestamps=True, vad_filter=False, initial_prompt=text[:200])
    timed = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
    words = map_times(split_script(text), timed)
    json.dump(words, open(out + ".words.json", "w"), ensure_ascii=False)
    print(json.dumps({"audio": audio, "duration": round(duration(audio), 2), "words": len(words), "last_word_end": words[-1]["e"]}))

if __name__ == "__main__":
    if sys.argv[1] == "tts": asyncio.run(tts(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else: align(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
