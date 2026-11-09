#!/usr/bin/env python3
"""Proof that a reel can be made 100% in code: visuals, hook text, cuts, camera move, music bed, SFX.
No generative API used. Output: renders/demo_code_reel.mp4 (1080x1920, 30fps, ~10s)."""
import math, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "renders"; OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
SR = 44100
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CUTS = [0.0, 3.2, 6.4, 10.0]  # hard cuts land on audio hits
LINES = [("YOU'VE BEEN DOING", "AARTI WRONG."), ("4 CIRCLES", "AT HIS FEET"), ("COMMENT 1 OR 3", "WHAT DOES YOUR FAMILY DO?")]
GOLD = (255, 196, 92)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def ease(t):  # easeOutCubic
    return 1 - (1 - min(max(t, 0), 1)) ** 3


def background(shot, t):
    """Dark temple-gold radial glow; slow push-in (camera move) and flicker."""
    zoom = 1 + 0.08 * t
    cx, cy = W / 2, H * (0.42 if shot != 2 else 0.5)
    r = np.hypot((xx - cx) / zoom, (yy - cy) / zoom)
    flicker = 1 + 0.06 * math.sin(t * 17) + 0.04 * math.sin(t * 7.3)
    glow = np.exp(-(r / (260 * flicker)) ** 2)
    halo = np.exp(-(r / 700) ** 2) * 0.35
    img = np.zeros((H, W, 3), np.float32)
    for i, c in enumerate((255, 150, 40)):
        img[..., i] = (glow * 1.0 + halo) * c
    img += np.array([12, 6, 4], np.float32)  # warm black floor
    if shot == 1:  # light-trail rings drawn around the "feet"
        for k in range(4):
            ring_r = 140 + k * 55
            a = ease((t - k * 0.35) / 0.6)
            band = np.exp(-((r * zoom - ring_r) / 5) ** 2) * a
            img += band[..., None] * np.array([255, 220, 150], np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


def draw_text(im, shot, t):
    d = ImageDraw.Draw(im)
    l1, l2 = LINES[shot]
    f1, f2 = ImageFont.truetype(FONT, 78), ImageFont.truetype(FONT, 110 if shot == 0 else 70)
    for j, (txt, f, y) in enumerate(((l1, f1, H * 0.70), (l2, f2, H * 0.70 + 120))):
        a = ease((t - 0.15 - j * 0.35) / 0.45)  # staggered kinetic reveal
        if a <= 0: continue
        dy = (1 - a) * 40
        while d.textlength(txt, font=f) > W * 0.88:  # auto-fit to safe area
            f = ImageFont.truetype(FONT, f.size - 4)
        w = d.textlength(txt, font=f)
        col = GOLD if j == 1 else (245, 235, 220)
        d.text(((W - w) / 2, y + dy), txt, font=f, fill=tuple(int(c * a) for c in col),
               stroke_width=3, stroke_fill=(0, 0, 0))


def render_video():
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                          str(OUT / "_video.mp4")], stdin=subprocess.PIPE)
    for f in range(int(CUTS[-1] * FPS)):
        T = f / FPS
        shot = max(i for i in range(3) if CUTS[i] <= T)
        t = T - CUTS[shot]
        im = Image.fromarray(background(shot, t))
        draw_text(im, shot, t)
        if t < 0.08:  # white flash frame on each cut
            im = Image.blend(im, Image.new("RGB", (W, H), (255, 240, 220)), 0.5)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()


def render_audio():
    n = int(CUTS[-1] * SR); t = np.arange(n) / SR
    # drone bed: D2 + A2 + D3 with slow swell (tanpura-ish)
    bed = sum(a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.2 * t)) for f, a in ((73.4, .5), (110, .3), (146.8, .2)))
    bed *= np.minimum(t / 1.5, 1) * 0.35
    # temple bell partials every 1.6s
    bell = np.zeros(n)
    for s in np.arange(0.4, CUTS[-1], 1.6):
        i = int(s * SR); tt = t[: n - i]
        bell[i:] += sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((880, .4), (1320, .25), (2290, .15))) * np.exp(-tt * 2.5) * 0.25
    # impact hit on every cut: sub thump + noise burst
    hit = np.zeros(n); rng = np.random.default_rng(1)
    for s in CUTS[1:-1]:
        i = int(s * SR); L = int(0.6 * SR); tt = np.arange(L) / SR
        hit[i:i + L] += (np.sin(2 * np.pi * 55 * tt * (1 - tt)) * np.exp(-tt * 6) * 0.9
                         + rng.normal(0, 1, L) * np.exp(-tt * 30) * 0.3)
    # whoosh riser into each cut
    for s in CUTS[1:-1]:
        L = int(0.5 * SR); i = int(s * SR) - L
        hit[i:i + L] += rng.normal(0, 1, L) * np.linspace(0, 1, L) ** 2 * 0.15
    mix = bed + bell + hit
    mix *= np.minimum((CUTS[-1] - t) / 0.8, 1)  # fade out
    mix = (mix / np.abs(mix).max() * 0.9 * 32767).astype(np.int16)
    with wave.open(str(OUT / "_audio.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(mix.tobytes())


if __name__ == "__main__":
    render_audio(); render_video()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT / "_video.mp4"), "-i", str(OUT / "_audio.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT / "demo_code_reel.mp4")], check=True)
    print(OUT / "demo_code_reel.mp4")
