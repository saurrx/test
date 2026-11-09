#!/usr/bin/env python3
"""Break a reel down the way an editor would: cuts, shot lengths, key frames, audio, transcript.

Usage: python3 scripts/analyze_reel.py <video.mp4> [<video.mp4> ...]
Writes analysis/<stem>/ with:
  meta.json        duration, resolution, fps, audio info, cut list, shot stats, loudness curve
  transcript.json  whisper segments (auto language) with timestamps
  frames/          one frame per shot (mid-shot) + contact sheet
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis"
SCENE_THRESH = 0.25
VERSION = 3  # v3: frame-diff spike cuts (brightness-normalised), large-v3-turbo + word timestamps, hook strip, motion energy
_model = None


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)])
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    num, den = v.get("avg_frame_rate", "0/1").split("/")
    return {
        "duration": float(d["format"]["duration"]),
        "width": v["width"], "height": v["height"],
        "fps": round(float(num) / float(den), 2) if float(den) else None,
        "audio": {"codec": a["codec_name"], "sample_rate": a.get("sample_rate"), "channels": a.get("channels")} if a else None,
    }


def cuts(path):
    """Hard cuts via frame-difference spikes relative to local motion. Works on dark, low-contrast and animated
    footage where ffmpeg's scene score and PySceneDetect miss cuts. Falls back to ffmpeg's scene filter without numpy."""
    try:
        import numpy as np
        w, h, fps = 64, 114, 15
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.float32)
        # normalise each frame's brightness so dark scenes are as sensitive as bright ones
        f = f / (f.mean(axis=(1, 2), keepdims=True) + 8.0)
        d = np.abs(f[1:] - f[:-1]).mean(axis=(1, 2))
        out, last = [], -1.0
        for i in range(len(d)):
            lo, hi = max(0, i - 8), min(len(d), i + 9)
            around = np.concatenate([d[lo:i], d[i + 1:hi]])
            base = float(np.median(around)) if around.size else 0.0
            t = (i + 1) / fps
            if d[i] > 0.12 and d[i] > 4.0 * base + 0.03 and t - last >= 0.4:
                out.append(round(t, 2)); last = t
        return out
    except Exception:
        pass
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", f"select='gt(scene,{SCENE_THRESH})',showinfo", "-an", "-f", "null", "-"])
    return [round(float(m), 3) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def loudness(path):
    """Momentary loudness (LUFS) sampled ~every 0.5s, to see music drops / beat hits / silences."""
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=none", "-f", "null", "-"])
    pts = re.findall(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)", r.stderr)
    out, last = [], -1.0
    for t, m in pts:
        t = float(t)
        if t - last >= 0.5:
            out.append([round(t, 1), float(m)]); last = t
    return out


def frames(path, shots, dest):
    dest.mkdir(parents=True, exist_ok=True)
    for i, (s, e) in enumerate(shots):
        mid = (s + e) / 2
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(path), "-frames:v", "1",
             "-vf", "scale=360:-2", str(dest / f"shot_{i:03d}_{mid:06.2f}s.jpg")])
    # time-based sampling too: many AI reels are continuous camera moves with few hard cuts
    tdir = dest.parent / "frames_2s"; tdir.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", "fps=1/2,scale=360:-2", str(tdir / "t_%03d.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", "fps=1/2,scale=150:-2,tile=8x4",
         "-frames:v", "1", str(dest.parent / "timeline_2s.jpg")])
    n = len(shots)
    cols = 6
    rows = max(1, -(-n // cols))
    run(["ffmpeg", "-y", "-v", "error", "-pattern_type", "glob", "-i", str(dest / "shot_*.jpg"),
         "-vf", f"scale=180:-2,tile={cols}x{rows}", "-frames:v", "1", str(dest.parent / "contact_sheet.jpg")])


def _whisper():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        import os
        name = os.environ.get("WHISPER_MODEL", "large-v3-turbo")
        try:
            if os.environ.get("WHISPER_DEVICE", "auto") == "cpu":
                raise RuntimeError("cpu forced")
            _model = WhisperModel(name, device="cuda", compute_type="float16")
            list(_model.transcribe(__import__("numpy").zeros(16000, dtype="float32"))[0])  # fail early if no VRAM
        except Exception:
            _model = WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=int(os.environ.get("WHISPER_THREADS", "8")))
    return _model


def transcribe(path):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    if audio.size == 0:
        return {"language": None, "segments": []}
    model = _whisper()
    # These creators post in Hindi/English/Hinglish. Whisper often guesses pa/ur/sa for Hindi; pin to hi unless clearly en.
    _, info = model.transcribe(audio[: 16000 * 30], vad_filter=True, beam_size=1)
    lang = info.language if info.language in ("hi", "en") else "hi"
    segs, _ = model.transcribe(audio, vad_filter=True, beam_size=5, language=lang, word_timestamps=True)
    out, words = [], 0
    for sg in segs:
        ws = [{"s": round(w.start, 2), "e": round(w.end, 2), "w": w.word.strip()} for w in (sg.words or [])]
        words += len(ws)
        out.append({"start": round(sg.start, 2), "end": round(sg.end, 2), "text": sg.text.strip(), "words": ws})
    speech = sum(x["end"] - x["start"] for x in out)
    return {"language": lang, "detected_language": info.language, "language_prob": round(info.language_probability, 3),
            "word_count": words, "first_word_s": out[0]["start"] if out else None,
            "speech_seconds": round(speech, 1), "wpm": round(60 * words / speech) if speech > 1 else None,
            "segments": out}


def hook_and_motion(path, d):
    """First frame (540px), first 3 s at 4 fps as one strip, and per-second motion energy (mean abs frame diff, 0-255)."""
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-frames:v", "1", "-vf", "scale=540:-2", str(d / "first_frame.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-t", "3", "-i", str(path), "-vf", "fps=4,scale=270:-2,tile=12x1",
         "-frames:v", "1", str(d / "hook_strip.jpg")])
    try:
        import numpy as np
        w, h, fps = 54, 96, 5
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w).astype(np.int16)
        diff = np.abs(f[1:] - f[:-1]).mean(axis=(1, 2))
        per_s = [round(float(diff[i:i + fps].mean()), 2) for i in range(0, len(diff), fps)]
        still = [i for i, v in enumerate(per_s) if v < 0.3]
        # "view changes": the picture 1 s later is substantially different (catches dissolves and fast camera moves
        # that are not hard cuts). Brightness-normalised, merged when adjacent.
        g = f.astype(np.float32); g = g / (g.mean(axis=(1, 2), keepdims=True) + 8.0)
        far = np.abs(g[fps:] - g[:-fps]).mean(axis=(1, 2))
        vc, last = [], -9.0
        for i, v in enumerate(far):
            t = i / fps
            if v > 0.45 and t - last >= 1.5:
                vc.append(round(t + 0.5, 1)); last = t
        return {"motion_per_s": per_s, "motion_mean": round(float(diff.mean()), 2),
                "motion_first3s": round(float(diff[: 3 * fps].mean()), 2), "still_seconds": len(still),
                "view_changes": vc, "view_changes_per_10s": round(10 * len(vc) / max(len(per_s), 1), 2)}
    except Exception as e:
        return {"motion_error": str(e)}


def analyze(path):
    path = Path(path)
    # data/reels/<handle>/<id>.mp4 -> analysis/<handle>__<id>, same naming as the seed reels
    name = f"{path.parent.name}__{path.stem}" if path.parent.parent.name == "reels" else path.stem
    d = OUT / name
    if (d / "meta.json").exists() and (d / "transcript.json").exists():
        try:
            if json.loads((d / "meta.json").read_text()).get("analyzer_version") == VERSION:
                print("skip", path.stem); return
        except Exception:
            pass
    d.mkdir(parents=True, exist_ok=True)
    m = probe(path)
    c = cuts(path)
    bounds = [0.0] + c + [m["duration"]]
    shots = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1) if bounds[i + 1] - bounds[i] > 0.05]
    lens = sorted(e - s for s, e in shots)
    m.update({
        "cuts": c, "shot_count": len(shots),
        "shot_len": {"mean": round(sum(lens) / len(lens), 2), "median": round(lens[len(lens) // 2], 2),
                     "min": round(lens[0], 2), "max": round(lens[-1], 2)},
        "cuts_per_10s": round(10 * len(c) / m["duration"], 2),
        "first_cut_s": c[0] if c else None,
        "loudness_lufs": loudness(path),
        "analyzer_version": VERSION,
    })
    m.update(hook_and_motion(path, d))
    (d / "meta.json").write_text(json.dumps(m, indent=1))
    frames(path, shots, d / "frames")
    (d / "transcript.json").write_text(json.dumps(transcribe(path), ensure_ascii=False, indent=1))
    print("done", path.stem, m["shot_count"], "shots")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            analyze(p)
        except Exception as e:
            print("FAIL", p, e)
