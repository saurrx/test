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


def transcribe(path):
    global _model
    from faster_whisper import WhisperModel
    if _model is None:
        _model = WhisperModel("small", device="cpu", compute_type="int8")
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    if audio.size == 0:
        return {"language": None, "segments": []}
    segs, info = _model.transcribe(audio, vad_filter=True, beam_size=5)
    return {"language": info.language, "language_prob": round(info.language_probability, 3),
            "segments": [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segs]}


def analyze(path):
    path = Path(path)
    d = OUT / path.stem
    if (d / "meta.json").exists() and (d / "transcript.json").exists():
        print("skip", path.stem); return
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
    })
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
