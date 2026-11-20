"""Synthesize a lo-fi chill hop bed (~50 s) and a set of quiet SFX. Pure numpy/scipy, no downloads."""
import os, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "sfx"), exist_ok=True)
SR = 48000
rng = np.random.default_rng(7)


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


# ---------------------------------------------------------------- BED
BPM = 76.0
BEAT = 60.0 / BPM
BARS = 16
TOTAL = BARS * 4 * BEAT + 1.5
bed = np.zeros(int(TOTAL * SR))


def put(buf, sig, at):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


def keys(freq, dur, vel=1.0):
    t = tt(dur)
    det = 1.0 + 0.0025 * np.sin(2 * np.pi * 0.4 * t)
    s = (np.sin(2 * np.pi * freq * t * det)
         + 0.45 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-3.0 * t)
         + 0.2 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-6.0 * t)
         + 0.12 * np.sin(2 * np.pi * 4.01 * freq * t) * np.exp(-9.0 * t))
    env = np.minimum(1, t / 0.008) * np.exp(-1.5 * t)
    trem = 1 + 0.07 * np.sin(2 * np.pi * 4.2 * t)
    return s * env * trem * vel


def sub(freq, dur, vel=1.0):
    t = tt(dur)
    env = np.minimum(1, t / 0.015) * np.exp(-1.7 * t)
    return (np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)) * env * vel


def kick(vel=1.0):
    t = tt(0.32)
    f = 50 + 95 * np.exp(-28 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-9 * t) * np.minimum(1, t / 0.002) * vel


def snare(vel=1.0):
    t = tt(0.22)
    n = bp(rng.standard_normal(len(t)), 1200, 6500) * np.exp(-22 * t)
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-26 * t) * 0.5
    return (n + body) * np.minimum(1, t / 0.002) * vel


def hat(vel=1.0):
    t = tt(0.06)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-60 * t) * vel


CHORDS = [  # (bass midi, chord midi notes)
    (45, [57, 60, 64, 67]),  # Am7
    (41, [57, 60, 64, 65]),  # Fmaj7 (F A C E ~ voiced close)
    (48, [52, 55, 59, 60]),  # Cmaj7 (E G B C)
    (43, [55, 59, 62, 64]),  # G6 / Em7
]
SWING = 0.12  # offbeat 8ths pushed late (in beats)

for bar in range(BARS):
    t0 = bar * 4 * BEAT
    bass, notes = CHORDS[bar % 4]
    last = bar == BARS - 1
    intro = bar < 2
    # chords: hit on 1 and a soft one on the swung "and of 2"
    for k, n in enumerate(notes):
        put(bed, keys(midi(n), 2.6, 0.30) * (1.0 + 0.02 * k), t0 + k * 0.012)
    if not last:
        for k, n in enumerate(notes):
            put(bed, keys(midi(n), 1.6, 0.16), t0 + (2.5 + SWING) * BEAT + k * 0.01)
    put(bed, sub(midi(bass), 2.4, 0.55), t0)
    if not intro and not last:
        put(bed, sub(midi(bass), 1.0, 0.40), t0 + 2.0 * BEAT)
    # drums
    if not intro and not last:
        for b in (0.0, 2.0, 3.5 + SWING):
            put(bed, kick(0.70 if b != 3.5 + SWING else 0.45), t0 + b * BEAT)
        for b in (1.0, 3.0):
            put(bed, snare(0.38), t0 + (b + 0.02) * BEAT)
    if not last:
        for i in range(8):
            b = i * 0.5 + (SWING if i % 2 else 0.0)
            v = (0.20 if i % 2 == 0 else 0.11) * (0.5 if intro else 1.0) * rng.uniform(0.8, 1.15)
            put(bed, hat(v), t0 + b * BEAT)

# warm it up, add faint vinyl crackle
bed = lp(bed, 7500, 2)
crack = np.zeros_like(bed)
for pos in rng.integers(0, len(bed), int(TOTAL * 14)):
    crack[pos] = rng.uniform(-1, 1) * rng.uniform(0.2, 1.0)
crack = hp(lp(crack, 6000), 1200)
bed += crack * 0.035 + hp(lp(rng.standard_normal(len(bed)), 5000), 800) * 0.0025
bed = np.tanh(bed * 1.15)

# trim to a clean 50.0 s: fade in 0.8 s, fade out 3 s
bed = bed[: int(50.0 * SR)]
bed *= np.minimum(1, tt(len(bed) / SR)[: len(bed)] / 0.8)
fo = np.minimum(1, (len(bed) - np.arange(len(bed))) / (3.0 * SR))
bed *= fo
bed = bed / np.max(np.abs(bed)) * 10 ** (-3 / 20)
# mild stereo: tiny Haas on the right channel
d = int(0.011 * SR)
right = np.concatenate([np.zeros(d), bed[:-d]]) * 0.97
stereo = np.stack([bed, right], axis=1)
wavfile.write(os.path.join(OUT, "bed.wav"), SR, (stereo * 32767).astype(np.int16))

# ---------------------------------------------------------------- SFX
PEAK = 10 ** (-12 / 20)


def save(name, x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    x *= np.minimum(1, np.arange(n) / (0.006 * SR))            # soft attack
    x *= np.minimum(1, (n - np.arange(n)) / (0.012 * SR))      # soft end
    x = x / np.max(np.abs(x)) * PEAK
    st = np.stack([x, x], axis=1)
    wavfile.write(os.path.join(OUT, "sfx", name + ".wav"), SR, (st * 32767).astype(np.int16))


def bell(freq, dur, decay=7.0):
    t = tt(dur)
    s = (np.sin(2 * np.pi * freq * t)
         + 0.35 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-9 * t)
         + 0.15 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-14 * t))
    return s * np.exp(-decay * t)


def sweep_sine(f0, f1, dur, env):
    t = tt(dur)
    f = f0 + (f1 - f0) * (t / dur) ** 1.4
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t)


t = tt(0.12)
save("pop", sweep_sine(650, 240, 0.12, lambda t: np.exp(-30 * t)))
t = tt(0.05)
save("tick", hp(rng.standard_normal(len(t)), 3000) * np.exp(-90 * t) + 0.5 * np.sin(2 * np.pi * 2200 * t) * np.exp(-80 * t))
t = tt(0.06)
save("click", bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-110 * t) + 0.6 * np.sin(2 * np.pi * 140 * t) * np.exp(-70 * t))
t = tt(0.55)
n = rng.standard_normal(len(t))
sig = np.zeros_like(n)
for lo, hi, w in ((250, 700, 1.0), (700, 1800, 0.9), (1800, 4200, 0.6)):
    sig += bp(n, lo, hi) * w
env = np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 2
save("whoosh", sig * env)
t = tt(0.5)
save("sweep", sweep_sine(420, 2300, 0.5, lambda t: np.sin(np.pi * np.clip(t / 0.5, 0, 1)) ** 1.5))
t = tt(0.3)
f1 = hp(rng.standard_normal(len(t)), 2500) * (np.exp(-50 * t) + 0.8 * np.exp(-50 * np.clip(t - 0.09, 0, None)) * (t > 0.09))
save("flip", f1)
t = tt(0.25)
save("stamp", np.sin(2 * np.pi * (90 - 30 * t) * t) * np.exp(-20 * t) + 0.5 * lp(rng.standard_normal(len(t)), 1800) * np.exp(-45 * t))
t = tt(0.55)
save("rise", sweep_sine(300, 1250, 0.55, lambda t: np.sin(np.pi * np.clip(t / 0.55, 0, 1) ** 0.8) ** 1.2) * 1.0
     + 0.3 * sweep_sine(600, 2500, 0.55, lambda t: np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 2))
save("chime", bell(1318.5, 0.58, 6.5) + 0.6 * bell(1975.5, 0.58, 8.0))
save("ding_c6", bell(1046.5, 0.55))
save("ding_e6", bell(1318.5, 0.55))
save("ding_g6", bell(1568.0, 0.55))
t = tt(0.25)
save("swish", hp(lp(rng.standard_normal(len(t)), 7000), 1500) * np.sin(np.pi * np.clip(t / 0.25, 0, 1)) ** 2)
t = tt(0.3)
save("thud", np.sin(2 * np.pi * (70 - 25 * t) * t) * np.exp(-14 * t) + 0.25 * lp(rng.standard_normal(len(t)), 600) * np.exp(-35 * t))
t = tt(0.12)
save("snap", bp(rng.standard_normal(len(t)), 1800, 6000) * np.exp(-55 * t) + 0.4 * np.sin(2 * np.pi * 900 * t) * np.exp(-60 * t))
print("ok")
