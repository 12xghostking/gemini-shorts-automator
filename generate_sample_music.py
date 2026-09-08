"""Generates a pleasant 10-second royalty-free ambient harmonic loop for testing."""

import math
import wave
import struct
from pathlib import Path

def generate_ambient_loop(file_path: str, duration: float = 10.0):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # Chord frequencies: C minor 9 (C, Eb, G, Bb, D) for atmospheric cinematic feel
    freqs = [130.81, 155.56, 196.00, 233.08, 293.66]
    
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            # Smooth envelope (fade in and fade out)
            env = math.sin(math.pi * t / duration)
            
            # Combine frequencies with slow subtle vibrato/phasing
            sample_val = 0.0
            for idx, f in enumerate(freqs):
                mod = math.sin(2 * math.pi * 0.2 * t + idx) * 1.5
                sample_val += math.sin(2 * math.pi * (f + mod) * t) * (0.18 / len(freqs))
            
            val = int(sample_val * env * 32767)
            val = max(-32768, min(32767, val))
            
            # Stereo frame (left, right)
            frames.extend(struct.pack('<hh', val, val))
            
        wav_file.writeframes(frames)

if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "assets" / "music" / "ambient_sample.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    generate_ambient_loop(str(out))
    print(f"Generated sample track: {out}")
