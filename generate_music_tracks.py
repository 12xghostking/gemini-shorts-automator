"""Generate 15+ procedurally created background music WAV tracks with different moods.
Each track uses sine/triangle wave synthesis with varying tempos, keys, and atmospheres.
Designed to be lightweight (no external dependencies beyond standard library).
"""

import struct
import math
import random
import os
from pathlib import Path

SAMPLE_RATE = 22050  # Lower sample rate to keep files small
DURATION = 30        # 30-second loops (will be looped by the pipeline)

def write_wav(filepath: str, samples: list, sample_rate: int = SAMPLE_RATE):
    """Write a mono WAV file from a list of float samples (-1.0 to 1.0)."""
    num_samples = len(samples)
    data_size = num_samples * 2
    with open(filepath, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))       # PCM
        f.write(struct.pack('<H', 1))       # mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            f.write(struct.pack('<h', int(clamped * 32767)))


def sine_wave(freq, t, volume=0.3):
    return volume * math.sin(2 * math.pi * freq * t)

def triangle_wave(freq, t, volume=0.3):
    period = 1.0 / freq if freq > 0 else 1.0
    phase = (t % period) / period
    return volume * (4 * abs(phase - 0.5) - 1)

def square_wave(freq, t, volume=0.15):
    return volume * (1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0)

def sawtooth_wave(freq, t, volume=0.2):
    period = 1.0 / freq if freq > 0 else 1.0
    phase = (t % period) / period
    return volume * (2 * phase - 1)

def noise(volume=0.05):
    return volume * (random.random() * 2 - 1)

def envelope(t, attack=0.5, sustain_end=None, release=0.5, total=None):
    """Simple ADSR-like envelope."""
    if total is None:
        total = DURATION
    if sustain_end is None:
        sustain_end = total - release
    if t < attack:
        return t / attack
    elif t < sustain_end:
        return 1.0
    elif t < total:
        return max(0, 1.0 - (t - sustain_end) / release)
    return 0.0

def low_pass_filter(samples, cutoff_ratio=0.1):
    """Simple single-pole low-pass filter."""
    alpha = cutoff_ratio
    filtered = [samples[0]]
    for i in range(1, len(samples)):
        filtered.append(filtered[-1] + alpha * (samples[i] - filtered[-1]))
    return filtered


# ═══════════════════════════════════════════════════════════════
# Track generators - each creates a unique mood
# ═══════════════════════════════════════════════════════════════

def gen_dark_cinematic():
    """Deep, ominous drone with low brass-like sounds."""
    samples = []
    base = 55  # A1
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        env = envelope(t, attack=2.0, release=3.0)
        s = sine_wave(base, t, 0.25) + sine_wave(base * 1.5, t, 0.12) + sine_wave(base * 2, t, 0.08)
        s += triangle_wave(base * 0.5, t, 0.15)
        s += noise(0.02) * env
        # Slow LFO modulation
        lfo = 1.0 + 0.15 * math.sin(2 * math.pi * 0.1 * t)
        samples.append(s * env * lfo * 0.7)
    return low_pass_filter(samples, 0.05)

def gen_epic_orchestral():
    """Rising strings-like sound with building intensity."""
    samples = []
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        progress = t / DURATION
        base = 130.81 + progress * 30  # C3 rising
        env = envelope(t, attack=3.0, release=2.0)
        s = sine_wave(base, t, 0.2)
        s += sine_wave(base * 2, t, 0.1 * progress)
        s += sine_wave(base * 3, t, 0.05 * progress)
        s += triangle_wave(base * 0.5, t, 0.15)
        # Tremolo
        trem = 1.0 + 0.1 * math.sin(2 * math.pi * 5 * t)
        samples.append(s * env * trem * 0.6)
    return low_pass_filter(samples, 0.08)

def gen_ethereal_ambient():
    """Soft, floating pads with reverb-like tails."""
    samples = []
    notes = [261.63, 329.63, 392.0, 523.25]  # C4, E4, G4, C5
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        env = envelope(t, attack=4.0, release=5.0)
        s = 0
        for idx, note in enumerate(notes):
            phase_shift = idx * 0.7
            vol = 0.12 - idx * 0.02
            s += sine_wave(note, t + phase_shift, vol)
        # Slow chorus effect
        s += sine_wave(261.63 * 1.003, t, 0.08)
        s += sine_wave(329.63 * 0.997, t, 0.06)
        samples.append(s * env * 0.5)
    return low_pass_filter(samples, 0.04)

def gen_tension_pulse():
    """Rhythmic pulsing tension builder."""
    samples = []
    bpm = 80
    beat_dur = 60.0 / bpm
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        beat_phase = (t % beat_dur) / beat_dur
        pulse = math.exp(-beat_phase * 8)  # Sharp decay
        base = 73.42  # D2
        s = sine_wave(base, t, 0.3) * pulse
        s += sine_wave(base * 2, t, 0.1) * pulse
        # Sub bass drone
        s += sine_wave(36.71, t, 0.15)
        env = envelope(t, attack=1.0, release=2.0)
        samples.append(s * env * 0.6)
    return low_pass_filter(samples, 0.06)

def gen_war_drums():
    """Tribal war drum pattern with deep impacts."""
    samples = []
    bpm = 100
    beat_dur = 60.0 / bpm
    pattern = [1.0, 0.0, 0.5, 0.0, 0.8, 0.0, 0.3, 0.6]  # Volume pattern
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        beat_num = int(t / (beat_dur / 2)) % len(pattern)
        local_t = (t % (beat_dur / 2))
        hit_vol = pattern[beat_num]
        # Drum hit: sine sweep down
        drum_freq = 120 * math.exp(-local_t * 15) + 40
        hit = sine_wave(drum_freq, t, 0.35 * hit_vol) * math.exp(-local_t * 6)
        # Low rumble
        rumble = sine_wave(30, t, 0.1)
        env = envelope(t, attack=0.5, release=1.0)
        samples.append((hit + rumble) * env * 0.7)
    return samples

def gen_mystical_chimes():
    """Shimmering bell-like tones with random sparkle."""
    samples = []
    chime_times = sorted([random.uniform(0, DURATION - 2) for _ in range(40)])
    chime_freqs = [random.choice([523, 659, 784, 880, 1047, 1175, 1319]) for _ in chime_times]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        s = 0
        # Background pad
        s += sine_wave(220, t, 0.06)
        s += sine_wave(330, t, 0.04)
        # Chime hits
        for ct, cf in zip(chime_times, chime_freqs):
            dt = t - ct
            if 0 <= dt < 2.0:
                chime_env = math.exp(-dt * 3)
                s += sine_wave(cf, t, 0.15 * chime_env)
                s += sine_wave(cf * 2, t, 0.05 * chime_env)
        env = envelope(t, attack=1.0, release=2.0)
        samples.append(s * env * 0.5)
    return samples

def gen_cyber_synth():
    """Pulsing cyberpunk synthwave bass."""
    samples = []
    bpm = 120
    beat_dur = 60.0 / bpm
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        beat_phase = (t % beat_dur) / beat_dur
        # Arpeggiated bass
        arp_idx = int(t / (beat_dur / 4)) % 4
        arp_notes = [82.41, 110.0, 130.81, 110.0]  # E2, A2, C3, A2
        base = arp_notes[arp_idx]
        arp_env = math.exp(-(t % (beat_dur / 4)) * 8)
        s = sawtooth_wave(base, t, 0.2) * arp_env
        s += square_wave(base * 2, t, 0.08) * arp_env
        # Pad
        s += sine_wave(164.81, t, 0.08)  # E3 pad
        s += sine_wave(246.94, t, 0.05)  # B3 pad
        env = envelope(t, attack=0.5, release=1.5)
        samples.append(s * env * 0.6)
    return low_pass_filter(samples, 0.12)

def gen_ocean_depths():
    """Deep underwater ambient with whale-like sounds."""
    samples = []
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Deep water rumble
        s = sine_wave(40, t, 0.15)
        s += sine_wave(60, t, 0.1)
        # Whale-like calls (slow frequency sweeps)
        whale_freq = 120 + 80 * math.sin(2 * math.pi * 0.05 * t)
        s += sine_wave(whale_freq, t, 0.12 * envelope(t % 10, attack=1, sustain_end=6, release=3, total=10))
        # Bubbles (random high pings)
        if random.random() < 0.001:
            s += sine_wave(random.uniform(800, 2000), t, 0.1)
        # Water noise
        s += noise(0.03)
        env = envelope(t, attack=3.0, release=3.0)
        samples.append(s * env * 0.5)
    return low_pass_filter(samples, 0.03)

def gen_frozen_tundra():
    """Cold, crystalline atmosphere with wind."""
    samples = []
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Wind (filtered noise with LFO)
        wind_vol = 0.08 + 0.05 * math.sin(2 * math.pi * 0.07 * t)
        s = noise(wind_vol)
        # Crystal tones
        s += sine_wave(1760, t, 0.03 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.2 * t)))
        s += sine_wave(2093, t, 0.02 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.15 * t + 1)))
        # Low drone
        s += sine_wave(65.41, t, 0.12)
        s += sine_wave(98.0, t, 0.08)
        env = envelope(t, attack=3.0, release=4.0)
        samples.append(s * env * 0.5)
    return low_pass_filter(samples, 0.06)

def gen_sacred_choir():
    """Ethereal choir-like harmonies."""
    samples = []
    chord = [261.63, 329.63, 392.0, 493.88]  # C major 7
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        s = 0
        for idx, note in enumerate(chord):
            # Slight vibrato per voice
            vib = 1.0 + 0.005 * math.sin(2 * math.pi * (4.5 + idx * 0.3) * t)
            s += sine_wave(note * vib, t, 0.12)
            s += sine_wave(note * 2 * vib, t, 0.04)  # Overtone
        # Breath modulation
        breath = 0.7 + 0.3 * math.sin(2 * math.pi * 0.15 * t)
        env = envelope(t, attack=4.0, release=4.0)
        samples.append(s * env * breath * 0.4)
    return low_pass_filter(samples, 0.05)

def gen_volcanic_rumble():
    """Deep seismic rumble with explosive bursts."""
    samples = []
    burst_times = [3, 8, 14, 19, 24]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Constant deep rumble
        s = sine_wave(25, t, 0.2)
        s += sine_wave(35, t, 0.15)
        s += noise(0.04)
        # Explosive bursts
        for bt in burst_times:
            dt = t - bt
            if 0 <= dt < 3.0:
                burst_env = math.exp(-dt * 1.5)
                s += sine_wave(50 + random.uniform(-5, 5), t, 0.25 * burst_env)
                s += noise(0.1 * burst_env)
        env = envelope(t, attack=1.0, release=2.0)
        samples.append(s * env * 0.6)
    return low_pass_filter(samples, 0.04)

def gen_desert_wind():
    """Haunting desert wind with sparse melodic fragments."""
    samples = []
    melody_times = sorted([random.uniform(2, DURATION - 3) for _ in range(12)])
    melody_notes = [random.choice([293.66, 349.23, 440.0, 523.25, 587.33]) for _ in melody_times]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Wind layers
        wind = noise(0.06 + 0.04 * math.sin(2 * math.pi * 0.03 * t))
        # Drone
        s = sine_wave(146.83, t, 0.08)  # D3
        s += sine_wave(220.0, t, 0.05)  # A3
        # Sparse melody
        for mt, mn in zip(melody_times, melody_notes):
            dt = t - mt
            if 0 <= dt < 2.5:
                mel_env = math.sin(math.pi * dt / 2.5)  # Smooth bell
                s += sine_wave(mn, t, 0.12 * mel_env)
        s += wind
        env = envelope(t, attack=2.0, release=3.0)
        samples.append(s * env * 0.5)
    return low_pass_filter(samples, 0.05)

def gen_battle_march():
    """Militaristic march rhythm with brass-like tones."""
    samples = []
    bpm = 130
    beat_dur = 60.0 / bpm
    march_pattern = [1.0, 0.0, 0.7, 0.0, 0.9, 0.0, 0.5, 0.7]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        beat_idx = int(t / (beat_dur / 2)) % len(march_pattern)
        local_t = t % (beat_dur / 2)
        vol = march_pattern[beat_idx]
        # Snare-like hit
        snare = noise(0.2 * vol) * math.exp(-local_t * 12)
        # Bass drum
        drum_freq = 80 * math.exp(-local_t * 10) + 30
        kick = sine_wave(drum_freq, t, 0.3 * vol) * math.exp(-local_t * 8)
        # Brass drone
        brass = triangle_wave(196.0, t, 0.1)  # G3
        brass += triangle_wave(246.94, t, 0.07)  # B3
        env = envelope(t, attack=0.3, release=1.5)
        samples.append((snare + kick + brass) * env * 0.6)
    return samples

def gen_astral_meditation():
    """Peaceful cosmic meditation with singing bowl sounds."""
    samples = []
    bowl_freqs = [174.61, 261.63, 349.23, 523.25, 698.46]  # F3, C4, F4, C5, F5
    bowl_times = [0, 5, 10, 15, 20, 25]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        s = 0
        # Singing bowls
        for bt in bowl_times:
            dt = t - bt
            if dt >= 0:
                bowl_env = math.exp(-dt * 0.3)
                bf = bowl_freqs[bowl_times.index(bt) % len(bowl_freqs)]
                s += sine_wave(bf, t, 0.15 * bowl_env)
                s += sine_wave(bf * 2.01, t, 0.05 * bowl_env)  # Slight detune
        # Om drone
        s += sine_wave(136.1, t, 0.08)  # Om frequency
        s += sine_wave(272.2, t, 0.04)
        env = envelope(t, attack=3.0, release=5.0)
        samples.append(s * env * 0.45)
    return low_pass_filter(samples, 0.04)

def gen_storm_chaos():
    """Chaotic storm with thunder hits and rain."""
    samples = []
    thunder_times = [2, 7, 12, 18, 23, 27]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Rain (constant noise)
        s = noise(0.06)
        # Wind gusts
        s += noise(0.04 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.08 * t)))
        # Thunder
        for tt in thunder_times:
            dt = t - tt
            if 0 <= dt < 4.0:
                thunder_env = math.exp(-dt * 0.8)
                s += noise(0.3 * thunder_env)
                s += sine_wave(30 + random.uniform(-10, 10), t, 0.2 * thunder_env)
        # Ominous low tone
        s += sine_wave(55, t, 0.06)
        env = envelope(t, attack=1.5, release=2.0)
        samples.append(s * env * 0.55)
    return low_pass_filter(samples, 0.07)

def gen_steampunk_clockwork():
    """Mechanical clicking and gear sounds with melodic elements."""
    samples = []
    bpm = 140
    beat_dur = 60.0 / bpm
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Clock tick (high freq ping)
        tick_phase = (t % (beat_dur / 2))
        tick = sine_wave(3000, t, 0.08) * math.exp(-tick_phase * 40) if tick_phase < 0.05 else 0
        # Gear grind
        gear_phase = (t % beat_dur)
        gear = sawtooth_wave(100, t, 0.05) * math.exp(-gear_phase * 5)
        # Music box melody
        melody_notes = [523.25, 587.33, 659.25, 587.33, 523.25, 440.0, 493.88, 440.0]
        mel_idx = int(t / (beat_dur * 2)) % len(melody_notes)
        mel_local = t % (beat_dur * 2)
        mel_env = math.exp(-mel_local * 2)
        melody = sine_wave(melody_notes[mel_idx], t, 0.12 * mel_env)
        s = tick + gear + melody
        # Base drone
        s += triangle_wave(130.81, t, 0.06)
        env = envelope(t, attack=0.5, release=1.0)
        samples.append(s * env * 0.5)
    return samples

def gen_hellfire_inferno():
    """Aggressive, fiery soundscape with demonic undertones."""
    samples = []
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Crackling fire (sporadic noise bursts)
        fire = noise(0.08 * (0.3 + 0.7 * abs(math.sin(2 * math.pi * random.uniform(10, 50) * t))))
        # Deep demonic drone
        s = sawtooth_wave(41.2, t, 0.15)  # E1
        s += sawtooth_wave(61.74, t, 0.1)  # B1
        # Distorted power chord
        s += square_wave(82.41, t, 0.08)
        s += square_wave(123.47, t, 0.06)
        s += fire
        # Pulsing intensity
        pulse = 0.6 + 0.4 * math.sin(2 * math.pi * 0.5 * t)
        env = envelope(t, attack=1.5, release=2.0)
        samples.append(s * env * pulse * 0.5)
    return low_pass_filter(samples, 0.08)

def gen_ancient_forest():
    """Peaceful forest ambiance with birdsong-like elements."""
    samples = []
    bird_times = sorted([random.uniform(1, DURATION - 1) for _ in range(25)])
    bird_freqs = [random.uniform(1500, 3500) for _ in bird_times]
    for i in range(SAMPLE_RATE * DURATION):
        t = i / SAMPLE_RATE
        # Gentle wind through leaves
        s = noise(0.03 + 0.02 * math.sin(2 * math.pi * 0.04 * t))
        # Forest floor drone
        s += sine_wave(110, t, 0.06)
        s += sine_wave(165, t, 0.04)
        # Bird calls (quick trills)
        for bt, bf in zip(bird_times, bird_freqs):
            dt = t - bt
            if 0 <= dt < 0.5:
                trill = sine_wave(bf + 200 * math.sin(2 * math.pi * 20 * dt), t, 0.08)
                trill_env = math.sin(math.pi * dt / 0.5)
                s += trill * trill_env
        # Gentle stream
        s += noise(0.015)
        env = envelope(t, attack=3.0, release=3.0)
        samples.append(s * env * 0.5)
    return low_pass_filter(samples, 0.06)


# ═══════════════════════════════════════════════════════════════
# Track registry
# ═══════════════════════════════════════════════════════════════

TRACKS = {
    "dark_cinematic":       gen_dark_cinematic,
    "epic_orchestral":      gen_epic_orchestral,
    "ethereal_ambient":     gen_ethereal_ambient,
    "tension_pulse":        gen_tension_pulse,
    "war_drums":            gen_war_drums,
    "mystical_chimes":      gen_mystical_chimes,
    "cyber_synth":          gen_cyber_synth,
    "ocean_depths":         gen_ocean_depths,
    "frozen_tundra":        gen_frozen_tundra,
    "sacred_choir":         gen_sacred_choir,
    "volcanic_rumble":      gen_volcanic_rumble,
    "desert_wind":          gen_desert_wind,
    "battle_march":         gen_battle_march,
    "astral_meditation":    gen_astral_meditation,
    "storm_chaos":          gen_storm_chaos,
    "steampunk_clockwork":  gen_steampunk_clockwork,
    "hellfire_inferno":     gen_hellfire_inferno,
    "ancient_forest":       gen_ancient_forest,
}


if __name__ == "__main__":
    music_dir = Path(__file__).resolve().parent / "assets" / "music"
    music_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(TRACKS)} background music tracks...")
    print("=" * 50)

    for name, gen_func in TRACKS.items():
        filepath = music_dir / f"{name}.wav"
        print(f"  Generating: {name}.wav ...", end=" ", flush=True)
        samples = gen_func()
        write_wav(str(filepath), samples)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"OK ({size_kb:.0f} KB)")

    print("=" * 50)
    total_files = len(list(music_dir.glob("*.wav")))
    print(f"Done! {total_files} music tracks available in {music_dir}")
