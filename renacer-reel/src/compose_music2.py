"""Original electro-pop track for the Renacer reel.

120 BPM, C major, progression C - G - Am - F (one chord per bar), 30 s.
Structure (bars of 2 s):
  0-1   intro   : filtered chords + pluck arp, filter slowly opening
  2-3   build   : kick, bass, hats, snare roll + riser, gap before drop
  4-11  drop    : full kit, sidechained supersaw, offbeat bass, lead hook
  12-13 drop 2  : hook an octave up, extra percussion
  14    outro   : final chord hit with tail
"""
import sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 36.0
N = int(SR * DUR)
rng = np.random.default_rng(11)


def t_of(n):
    return np.arange(n) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "low", output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "high", output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x)


def saw(freq, n, phase=0.0):
    t = t_of(n)
    return 2 * ((freq * t + phase) % 1.0) - 1


def place(buf, sig, start_s, gain=1.0):
    i = int(start_s * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def adsr(n, a=0.005, d=0.1, s=0.7, r=0.05):
    env = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n)
    env[:na] = np.linspace(0, 1, na)
    nd2 = min(nd, max(0, n - na))
    env[na:na + nd2] = np.linspace(1, s, nd2)
    if nr > 0 and n > nr:
        env[-nr:] *= np.linspace(1, 0, nr)
    return env


# ---------------------------------------------------------------- instruments
def kick():
    n = int(0.45 * SR)
    t = t_of(n)
    f = 45 + 115 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t * 400) * 0.25
    return np.tanh((body + click) * 1.6)


def clap():
    n = int(0.3 * SR)
    t = t_of(n)
    noise = bp(rng.standard_normal(n), 900, 5000)
    env = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        env[i:] += np.exp(-(t[: n - i]) * (90 if k < 2 else 18))
    return noise * env * 0.6


def hat(open_=False):
    n = int((0.22 if open_ else 0.05) * SR)
    t = t_of(n)
    noise = hp(rng.standard_normal(n), 7500, 4)
    return noise * np.exp(-t * (14 if open_ else 90)) * (0.28 if open_ else 0.22)


def snare():
    n = int(0.18 * SR)
    t = t_of(n)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
    noise = bp(rng.standard_normal(n), 1500, 8000) * np.exp(-t * 22)
    return (tone + noise) * 0.5


def supersaw(midis, dur, cutoff=5000, voices=7, detune=0.22):
    n = int(dur * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    for m in midis:
        f0 = mtof(m)
        for v in range(voices):
            d = (v - (voices - 1) / 2) / ((voices - 1) / 2)
            f = f0 * 2 ** (d * detune / 12)
            s = saw(f, n, phase=rng.random())
            pan = 0.5 + 0.45 * d
            L += s * (1 - pan)
            R += s * pan
    env = adsr(n, a=0.01, d=0.3, s=0.8, r=0.08)
    L = lp(L, cutoff) * env
    R = lp(R, cutoff) * env
    return np.stack([L, R], 1) / (voices * len(midis)) * 2.2


def pluck(m, dur=0.22, cutoff=3800):
    n = int(dur * SR)
    t = t_of(n)
    f = mtof(m)
    s = 0.6 * saw(f, n) + 0.4 * np.sign(np.sin(2 * np.pi * f * t))
    return lp(s, cutoff) * np.exp(-t * 16) * 0.5


def bass(m, dur):
    n = int(dur * SR)
    t = t_of(n)
    f = mtof(m)
    s = saw(f, n) * 0.7 + np.sin(2 * np.pi * f * t) * 0.6
    env = adsr(n, a=0.004, d=0.12, s=0.6, r=0.03)
    k = np.exp(-t * 18)  # filter envelope: crossfade bright -> dark
    filt = lp(s, 2100) * k + lp(s, 700) * (1 - k)
    return np.tanh(filt * env * 1.5) * 0.55


def lead(m, dur):
    n = int(dur * SR)
    t = t_of(n)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 4 - 0.4, 0, 1)
    f = mtof(m) * vib
    ph = np.cumsum(f) / SR
    s = 0.55 * (2 * (ph % 1) - 1) + 0.45 * np.sign(np.sin(2 * np.pi * ph * 1.003))
    env = adsr(n, a=0.006, d=0.15, s=0.75, r=0.06)
    return lp(s, 4200) * env * 0.32


# ---------------------------------------------------------------- arrangement
CHORDS = [  # (bass root, chord voicing)
    (38, [62, 66, 69, 74]),   # D
    (47, [62, 66, 71, 74]),   # Bm
    (43, [62, 67, 71, 74]),   # G
    (45, [61, 64, 69, 73]),   # A
]
HOOK = [
    [(0, .5, 76), (.5, .5, 79), (1, .75, 81), (1.75, .25, 79), (2, .5, 76), (2.5, .5, 74), (3, 1, 72)],
    [(0, .5, 74), (.5, .5, 76), (1, .75, 79), (1.75, .25, 76), (2, 1, 74), (3, .5, 71), (3.5, .5, 74)],
    [(0, .5, 72), (.5, .5, 76), (1, .75, 81), (1.75, .25, 79), (2, .5, 76), (2.5, .5, 72), (3, 1, 76)],
    [(0, .5, 77), (.5, .5, 76), (1, .5, 74), (1.5, .5, 72), (2, 1.5, 74), (3.5, .5, 79)],
]

drums = np.zeros(N)
bassbus = np.zeros(N)
chords = np.zeros((N, 2))
arp = np.zeros(N)
leadbus = np.zeros(N)
fx = np.zeros(N)

K, C, S = kick(), clap(), snare()
HC, HO = hat(), hat(True)

DROP_BARS = range(4, 17)

for bar in range(18):
    b0 = bar * BAR
    root, voicing = CHORDS[bar % 4]

    # chords: intro filtered pad, drop full supersaw
    if bar < 4:
        cut = 600 + bar * 900
        chords[int(b0 * SR):int(b0 * SR) + int(BAR * SR)] += supersaw(voicing, BAR, cutoff=cut)[: N - int(b0 * SR)] * 0.8
    elif bar < 17:
        for beat in range(4):  # retriggered per beat = pumping stabs
            seg = supersaw(voicing, BEAT, cutoff=6500)
            i = int((b0 + beat * BEAT) * SR)
            chords[i:i + len(seg)] += seg[: N - i]
    else:
        seg = supersaw(voicing + [50], 2.0, cutoff=4000)
        i = int(b0 * SR)
        chords[i:i + len(seg)] += seg[: N - i] * 1.2

    # arp 16ths (intro through drop)
    if bar < 17:
        pattern = [voicing[k] + 12 for k in (0, 1, 2, 3, 2, 1, 2, 3)]
        for s16 in range(16):
            place(arp, pluck(pattern[s16 % 8], cutoff=1500 + 2500 * min(1, bar / 4)), b0 + s16 * BEAT / 4,
                  0.55 if bar < 4 else 0.35)

    # build
    if bar in (2, 3):
        for beat in range(4):
            place(drums, K, b0 + beat * BEAT, 0.8)
        for e in range(8):
            place(bassbus, bass(root, BEAT / 2 * 0.9), b0 + e * BEAT / 2, 0.7)
            place(drums, HC, b0 + e * BEAT / 2 + BEAT / 4, 0.8)
    if bar == 3:  # snare roll accelerating, stop at 3.75 beats for the gap
        times = [k * BEAT / 2 for k in range(4)] + [2 * BEAT + k * BEAT / 4 for k in range(4)] + \
                [3 * BEAT + k * BEAT / 8 for k in range(6)]
        for k, tt in enumerate(times):
            place(drums, S, b0 + tt, 0.4 + 0.6 * k / len(times))

    # drop
    if bar in DROP_BARS:
        for beat in range(4):
            place(drums, K, b0 + beat * BEAT, 1.0)
            place(drums, HO, b0 + beat * BEAT + BEAT / 2, 0.9)
            if beat in (1, 3):
                place(drums, C, b0 + beat * BEAT, 1.0)
        for s16 in range(16):
            if s16 % 2 == 1:
                place(drums, HC, b0 + s16 * BEAT / 4, 0.7)
        for e in range(8):  # offbeat bass with octave jumps
            m = root + (12 if e in (3, 7) else 0)
            if e % 2 == 1 or e == 0:
                place(bassbus, bass(m, BEAT / 2 * 0.95), b0 + e * BEAT / 2, 1.0)
        octave = 12 if bar >= 13 else 0
        for (st, du, m) in HOOK[bar % 4]:
            place(leadbus, lead(m + 2 + octave, du * BEAT * 0.95), b0 + st * BEAT, 0.75 if bar < 8 else 1.0)
        if bar >= 13:  # extra snare fill at end of bar 13
            if bar == 16:
                for k in range(8):
                    place(drums, S, b0 + 3 * BEAT + k * BEAT / 8, 0.3 + 0.08 * k)

    if bar == 17:
        place(drums, K, b0, 1.0)
        place(drums, C, b0, 0.8)
        place(bassbus, bass(root, 1.5), b0, 1.0)

# riser over the build (bars 2-3) ending at 7.75 s
rn = int(3.75 * SR)
rt = t_of(rn)
noise = rng.standard_normal(rn)
riser = np.zeros(rn)
for k in range(0, rn, 2048):
    seg = noise[k:k + 2048]
    fc = 400 + 9000 * (k / rn) ** 2
    riser[k:k + len(seg)] = bp(seg, fc * 0.7, min(fc * 1.4, 20000))
riser *= (rt / rt[-1]) ** 2 * 0.35
f_sweep = 200 + 1600 * (rt / rt[-1]) ** 2
riser += np.sin(2 * np.pi * np.cumsum(f_sweep) / SR) * (rt / rt[-1]) ** 3 * 0.08
place(fx, riser, 4.0)

# impact / downlifter on the drop (8 s) and at 24 s
imp_n = int(2.0 * SR)
it = t_of(imp_n)
impact = lp(rng.standard_normal(imp_n), 3000) * np.exp(-it * 3) * 0.35
impact += np.sin(2 * np.pi * np.cumsum(80 * np.exp(-it * 1.5) + 30) / SR) * np.exp(-it * 2.5) * 0.5
place(fx, impact, 8.0)
place(fx, impact * 0.6, 26.0)

# ---------------------------------------------------------------- sidechain
side = np.ones(N)
duck_n = int(BEAT * SR)
dt = t_of(duck_n)
duck = 1 - 0.75 * np.exp(-dt * 11)
for bar in DROP_BARS:
    for beat in range(4):
        i = int((bar * BAR + beat * BEAT) * SR)
        side[i:i + duck_n] = np.minimum(side[i:i + duck_n], duck[: N - i])
for bar in (2, 3):
    for beat in range(4):
        i = int((bar * BAR + beat * BEAT) * SR)
        side[i:i + duck_n] = np.minimum(side[i:i + duck_n], 1 - 0.45 * np.exp(-dt * 11)[: N - i])

# gap right before the drop (7.75 - 8.0 s): mute everything but fx tail
gap = np.ones(N)
g0, g1 = int(7.75 * SR), int(8.0 * SR)
gap[g0:g1] = 0.0


# ---------------------------------------------------------------- reverb + delay
def reverb(x, secs=1.6, mix=0.25):
    n = int(secs * SR)
    t = t_of(n)
    irL = rng.standard_normal(n) * np.exp(-t * 4.0)
    irR = rng.standard_normal(n) * np.exp(-t * 4.0)
    irL, irR = lp(irL, 6000), lp(irR, 6000)
    wl = fftconvolve(x, irL)[: len(x)]
    wr = fftconvolve(x, irR)[: len(x)]
    s = np.max(np.abs(np.concatenate([wl, wr]))) + 1e-9
    wet = np.stack([wl, wr], 1) / s * np.max(np.abs(x))
    return wet * mix


def delay(x, time=BEAT * 0.75, fb=0.35, mix=0.3):
    d = int(time * SR)
    y = np.zeros_like(x)
    y[:] = x
    out = np.zeros_like(x)
    tap = x.copy()
    g = mix
    for _ in range(5):
        tap = np.concatenate([np.zeros(d), tap[:-d]])
        out += tap * g
        g *= fb
    return out


lead_st = np.stack([leadbus + delay(leadbus) * 0.6, leadbus + delay(leadbus, BEAT * 0.5) * 0.6], 1)
arp_st = np.stack([arp, np.concatenate([np.zeros(int(0.012 * SR)), arp[:-int(0.012 * SR)]])], 1)

mix = np.zeros((N, 2))
mix += np.stack([drums, drums], 1) * 0.95
mix += np.stack([bassbus, bassbus], 1) * side[:, None] * 0.9
mix += chords * side[:, None] * 0.45
mix += arp_st * side[:, None] * 0.6
mix += lead_st * 0.75
intro_gain = np.ones(N)
intro_gain[: int(4 * SR)] = 3.2
ramp = int(0.5 * SR)
intro_gain[int(4 * SR) - ramp:int(4 * SR)] = np.linspace(3.2, 1.0, ramp)
mix *= intro_gain[:, None]
mix *= gap[:, None]
mix += np.stack([fx, fx], 1) * 0.9

wet_src = (chords * 0.4 + lead_st * 0.5 + arp_st * 0.3)[:, 0]
mix += reverb(wet_src, mix=0.22)

# master: highpass rumble, soft clip, normalise, fade out tail
mix[:, 0] = hp(mix[:, 0], 28)
mix[:, 1] = hp(mix[:, 1], 28)
mix = np.tanh(mix * 1.25)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.93
fade = int(1.2 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 1.5
fin = int(0.02 * SR)
mix[:fin] *= np.linspace(0, 1, fin)[:, None]

out = sys.argv[1]
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print("wrote", out, mix.shape[0] / SR, "s")
