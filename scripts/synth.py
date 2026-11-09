#!/usr/bin/env python3
"""Code-made music beds and sound effects (numpy only). Writes 44.1 kHz stereo WAVs.
  synth.py all <outdir>                       -> a starter kit of beds and SFX
  synth.py bed <out.wav> <seconds> <style> [root_hz] [bpm]   styles: drone | pulse | tension | folk"""
import sys, wave
import numpy as np
SR = 44100
rng = np.random.default_rng(7)

def t(sec): return np.arange(int(SR * sec)) / SR
def env(n, a=0.01, r=0.2):
    e = np.ones(n); na, nr = int(SR * a), int(SR * r)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e
def lp(x, k):  # one-pole low-pass, k in (0,1]: smaller = darker
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += k * (x[i] - acc); y[i] = acc
    return y
def fast_lp(x, win):  # moving-average low-pass (vectorised)
    c = np.cumsum(np.insert(x, 0, 0.0)); out = (c[win:] - c[:-win]) / win
    return np.concatenate([np.full(len(x) - len(out), out[0]), out])
def save(path, x, peak=0.9):
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype("<i2").tobytes())
    print(path, round(len(x) / SR, 2), "s")

def pluck(f, sec, bright=6, decay=3.0):
    tt = t(sec); x = sum(np.sin(2 * np.pi * f * h * tt) / h * np.exp(-tt * decay * (1 + 0.25 * h)) for h in range(1, bright + 1))
    return x * env(len(tt), 0.003, 0.05)

def tanpura(sec, root=130.81):
    """Sa-Pa-Sa'-Sa drone: slow plucks with buzzing harmonics (the 'jivari' shimmer)."""
    tt = t(sec); out = np.zeros(len(tt)); order = [root * 1.5, root * 2, root * 2, root]; step = 1.15; i = 0; pos = 0.0
    while pos < sec:
        f = order[i % 4]; n = int(min(4.5, sec - pos) * SR); s = int(pos * SR); tn = np.arange(n) / SR
        note = sum(np.sin(2 * np.pi * f * h * tn + 0.6 * np.sin(2 * np.pi * 0.7 * tn)) * (1 / h ** 0.75) * np.exp(-tn * (0.5 + 0.12 * h)) for h in range(1, 14))
        out[s:s + n] += note * env(n, 0.02, 0.3); pos += step; i += 1
    return out

def pad(sec, freqs, wob=0.15):
    tt = t(sec); x = np.zeros(len(tt))
    for k, f in enumerate(freqs):
        for d in (-0.4, 0, 0.4): x += np.sin(2 * np.pi * (f + d) * tt + wob * np.sin(2 * np.pi * (0.11 + 0.03 * k) * tt))
    return x * env(len(tt), 1.5, 2.0)

def boom(sec=1.6, f0=95):
    tt = t(sec); f = f0 * np.exp(-tt * 5) + 34; ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-tt * 3.2) + 0.5 * fast_lp(rng.standard_normal(len(tt)), 60) * np.exp(-tt * 14)) * env(len(tt), 0.002, 0.2)
def whoosh(sec=0.6):
    n = rng.standard_normal(int(SR * sec)); tt = t(sec); sweep = fast_lp(n, 30) * np.sin(np.pi * tt / sec) ** 2
    return sweep * (0.6 + 0.4 * np.sin(2 * np.pi * (2 + 6 * tt / sec) * tt))
def riser(sec=2.0):
    tt = t(sec); f = 180 * 2 ** (2.2 * tt / sec); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + fast_lp(rng.standard_normal(len(tt)), 12) * 0.6
    return x * (tt / sec) ** 2
def bell(f=880, sec=3.0):
    tt = t(sec); return sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * d) for m, a, d in [(1, 1, 1.2), (2.01, .6, 1.8), (2.76, .45, 2.4), (5.4, .25, 3.5), (8.9, .12, 5)]) * env(len(tt), 0.002, 0.3)
def tick(): tt = t(0.06); return np.sin(2 * np.pi * 2100 * tt) * np.exp(-tt * 90)
def hit(sec=0.5):  # dry frame-drum thump
    tt = t(sec); return (np.sin(2 * np.pi * (140 * np.exp(-tt * 18) + 60) * tt) * np.exp(-tt * 11) + 0.3 * fast_lp(rng.standard_normal(len(tt)), 8) * np.exp(-tt * 40))
def crack(sec=1.4):  # thunder-like snap: noise burst + low rumble
    tt = t(sec); n = rng.standard_normal(len(tt))
    return n * np.exp(-tt * 30) + 1.4 * fast_lp(n, 220) * np.exp(-tt * 2.5) * 6 + 0.8 * boom(sec, 70)

def bed(sec, style="drone", root=130.81, bpm=84):
    tt = t(sec); x = np.zeros(len(tt))
    if style in ("drone", "folk", "pulse"): x += 0.5 * tanpura(sec, root)
    if style in ("drone", "tension"): x += 0.12 * pad(sec, [root / 2, root, root * 1.5])
    if style == "tension": x += 0.2 * pad(sec, [root / 2, root * 1.06, root * 1.41], wob=0.5) + 0.05 * fast_lp(rng.standard_normal(len(tt)), 300) * 8
    if style in ("pulse", "folk", "tension"):
        beat = 60 / bpm; k = 0
        while k * beat < sec - 0.6:
            s = int(k * beat * SR); h = hit() * (1.0 if k % 4 == 0 else 0.45 if k % 2 == 0 else 0.25) * (0.8 if style != "tension" else 0.5); x[s:s + len(h)] += h[: len(x) - s]; k += 1
    if style == "folk":  # pentatonic plucked melody
        scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2]; beat = 60 / bpm; k = 0; r2 = np.random.default_rng(int(root))
        while k * beat < sec - 1.5:
            if r2.random() < 0.7:
                p = pluck(root * 2 * scale[r2.integers(0, 6)], 1.4); s = int(k * beat * SR); x[s:s + len(p)] += 0.35 * p[: len(x) - s]
            k += 1
    x *= env(len(x), 0.4, 1.2)
    l = x + 0.25 * np.roll(x, int(0.011 * SR)); r = x + 0.25 * np.roll(x, int(0.017 * SR))
    return np.stack([l, r], 1)

if __name__ == "__main__":
    if sys.argv[1] == "bed":
        save(sys.argv[2], bed(float(sys.argv[3]), sys.argv[4], float(sys.argv[5]) if len(sys.argv) > 5 else 130.81, float(sys.argv[6]) if len(sys.argv) > 6 else 84), 0.8)
    else:
        d = sys.argv[2]
        for name, x in [("boom", boom()), ("whoosh", whoosh()), ("riser", riser()), ("bell", bell()), ("bell_low", bell(440, 4)), ("tick", tick()), ("hit", hit()), ("crack", crack())]:
            save(f"{d}/sfx_{name}.wav", x)
        for style in ("drone", "pulse", "tension", "folk"): save(f"{d}/bed_{style}.wav", bed(40, style), 0.8)
