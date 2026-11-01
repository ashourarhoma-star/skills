"""Procedural score + SFX for the 20 s revenue-recognition video (fully original, royalty-free).

Writes a 48 kHz stereo WAV: python3 audio.py out.wav
Bars are 2.5 s (96 BPM, 4/4) so chord changes land on the scene cuts.
"""

import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48_000
DUR = 20.0
N = int(SR * DUR)
BEAT = 60 / 96
BAR = BEAT * 4
rng = np.random.default_rng(11)
t_all = np.arange(N) / SR


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def env_adsr(n, a, d, s, r):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n)
    e[:na] = np.linspace(0, 1, na)
    nd = min(nd, n - na)
    e[na : na + nd] = np.linspace(1, s, nd)
    if nr > 0 and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


# Chords (MIDI). D major: Bm7 | Gmaj7 | Dmaj7 | Asus4->A | Bm7 | Gmaj7 | Asus4->A | Dadd9
CHORDS = [
    [47, 59, 62, 66, 69],  # Bm7
    [43, 59, 62, 66, 71],  # Gmaj7
    [50, 57, 61, 66, 69],  # Dmaj7
    [45, 57, 62, 64, 69],  # Asus4 (resolves to A in 2nd half)
    [47, 59, 62, 66, 69],  # Bm7
    [43, 59, 62, 66, 71],  # Gmaj7
    [45, 57, 62, 64, 69],  # Asus4 -> A
    [50, 62, 64, 66, 69],  # Dadd9
]
SUS_BARS = (3, 6)
ARP = [
    [71, 74, 78, 81],
    [71, 74, 78, 83],
    [69, 73, 78, 81],
    [69, 74, 76, 81],
    [71, 74, 78, 81],
    [71, 74, 78, 83],
    [69, 74, 76, 81],
    [74, 76, 78, 81],
]

pad = np.zeros(N)
arp = np.zeros(N)
bass = np.zeros(N)
drums = np.zeros(N)
sfx = np.zeros(N)

# ---- pad: detuned saw-ish stack, slow attack, lowpassed ----
for b, chord in enumerate(CHORDS):
    t0 = b * BAR
    n = int((BAR + 0.6) * SR)
    tt = np.arange(n) / SR
    sig = np.zeros(n)
    for m in chord[1:]:
        if b in SUS_BARS:  # Asus4 -> A on beat 3
            m2 = 61 if m == 62 else m
        for det in (-0.08, 0.0, 0.08):
            f = hz(m + det)
            ph = rng.uniform(0, 2 * np.pi)
            if b in SUS_BARS and m == 62:
                fsig = np.where(tt < BAR / 2, hz(62 + det), hz(m2 + det))
                phase = 2 * np.pi * np.cumsum(fsig) / SR + ph
            else:
                phase = 2 * np.pi * f * tt + ph
            sig += np.sin(phase) + 0.35 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)
    sig = lp(sig, 1400 if b < 7 else 2600)
    sig *= env_adsr(n, 0.9 if b == 0 else 0.35, 0.5, 0.85, 0.6)
    place(pad, sig, t0, 0.018)

# ---- sub bass ----
for b, chord in enumerate(CHORDS):
    if b == 0:
        continue
    n = int(BAR * SR)
    tt = np.arange(n) / SR
    sig = np.sin(2 * np.pi * hz(chord[0] - 12) * tt) + 0.25 * np.sin(2 * np.pi * hz(chord[0]) * tt)
    place(bass, sig * env_adsr(n, 0.08, 0.3, 0.8, 0.3), b * BAR, 0.16)

# ---- pluck arpeggio (8ths) from 4.0 s ----
step = BEAT / 2
k = 0
t = 4.0
while t < 19.6:
    b = min(int(t // BAR), 7)
    m = ARP[b][[0, 1, 2, 3, 2, 1, 3, 2][k % 8]]
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    f = hz(m)
    s = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt) + 0.15 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 9)
    s *= np.minimum(1, tt / 0.004)
    g = 0.05 if t < 10.0 else 0.065
    if t > 16.0:
        g = 0.07
    place(arp, s, t, g * (0.85 + 0.15 * (k % 2 == 0)))
    k += 1
    t = 4.0 + k * step

# ---- soft kick + shaker ----
def kick():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    f = 48 + 90 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)


def shaker():
    n = int(0.08 * SR)
    tt = np.arange(n) / SR
    return hp(rng.standard_normal(n), 6000) * np.exp(-tt * 60)


bi = 0
t = 4.0
while t < 19.5:
    full = 10.0 <= t < 15.5 or t >= 16.0
    if bi % 2 == 0 or full:
        place(drums, kick(), t, 0.35 if full else 0.26)
    place(drums, shaker(), t + BEAT / 2, 0.05 if full else 0.03)
    bi += 1
    t = 4.0 + bi * BEAT

# ---- SFX ----
def riser(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 2048
    for i in range(0, n, seg):
        fr = 400 + 7000 * (i / n) ** 2
        out[i : i + seg] = bp(noise[i : i + seg], fr * 0.7, min(fr * 1.4, 20000))[: len(out[i : i + seg])]
    return out * (tt / dur) ** 2


def whoosh(dur=0.7):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    e = np.sin(np.pi * tt / dur) ** 2
    return lp(hp(rng.standard_normal(n), 300), 3500) * e


def chime(m, dur=2.2):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * hz(m) * r * tt) * np.exp(-tt * d) for a, r, d in [(1, 1, 2.2), (0.5, 2.0, 3.5), (0.25, 2.76, 5), (0.15, 5.4, 8)])
    return s * np.minimum(1, tt / 0.003)


def thud():
    n = int(0.5 * SR)
    tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-tt * 30)) / SR) * np.exp(-tt * 14)
    slap = bp(rng.standard_normal(n), 800, 4000) * np.exp(-tt * 40)
    return body + 0.5 * slap


def flip():
    n = int(0.45 * SR)
    tt = np.arange(n) / SR
    flutter = 0.6 + 0.4 * np.sin(2 * np.pi * 28 * tt)
    return bp(rng.standard_normal(n), 1500, 7000) * np.exp(-tt * 9) * flutter


place(sfx, chime(81), 0.5, 0.05)  # title shimmer
place(sfx, chime(86), 0.8, 0.03)
place(sfx, riser(1.0), 3.15, 0.04)
place(sfx, whoosh(0.8), 3.75, 0.12)
place(sfx, chime(74, 1.6), 4.1, 0.05)  # impact on reveal
place(sfx, whoosh(0.5), 4.4, 0.05)  # card slide
place(sfx, chime(86, 1.8), 7.05, 0.06)  # obligation satisfied
place(sfx, chime(90, 1.8), 7.2, 0.035)
place(sfx, riser(0.8), 9.3, 0.035)
place(sfx, whoosh(0.8), 9.8, 0.11)
place(sfx, chime(78), 10.88, 0.05)  # 20 Oct highlight
place(sfx, flip(), 12.4, 0.18)  # page flip
place(sfx, chime(81), 13.08, 0.045)  # 18 Nov highlight
place(sfx, riser(0.9), 15.1, 0.035)
place(sfx, whoosh(0.9), 15.75, 0.12)
place(sfx, chime(86, 2.5), 16.6, 0.045)  # report reveal
place(sfx, chime(90, 2.5), 18.1, 0.035)  # closing line

# ---- mix + reverb ----
def stereo_reverb(x, decay=1.8, wet=0.25):
    n = int(decay * SR)
    tt = np.arange(n) / SR
    irs = [lp(rng.standard_normal(n), 6000) * np.exp(-tt * 6.9 / decay) for _ in range(2)]
    out = []
    for ir in irs:
        ir /= np.sqrt(np.sum(ir**2))
        out.append(x + wet * fftconvolve(x, ir)[: len(x)])
    return np.stack(out, 1)


music = pad + arp + bass + drums
mix = stereo_reverb(music, 2.2, 0.35) + stereo_reverb(sfx, 1.4, 0.3)
# gentle pan movement on arp/pad for width
pan = 0.5 + 0.12 * np.sin(2 * np.pi * 0.15 * t_all)
mix[:, 0] *= 1.1 - pan * 0.2
mix[:, 1] *= 0.9 + pan * 0.2
# fades
fade_in = np.minimum(1, t_all / 0.25)
fade_out = np.clip((DUR - t_all) / 0.6, 0, 1)
mix *= (fade_in * fade_out)[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.7

out = sys.argv[1] if len(sys.argv) > 1 else "music_sfx.wav"
from scipy.io import wavfile

wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print("wrote", out)
