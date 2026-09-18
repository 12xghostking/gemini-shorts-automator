"""Audio Engine for synthesizing voiceovers and handling background music."""

import os
import re
import time
import random
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from src import config

logger = logging.getLogger(__name__)

# Curated profiles for dramatic, cinematic, non-robotic narration
DRAMATIC_VOICE_PROFILES: Dict[str, Dict[str, str]] = {
    "en-US-GuyNeural": {
        "rate": "-4%",
        "pitch": "-3Hz",
        "name": "Guy (Movie Trailer Deep)"
    },
    "en-US-ChristopherNeural": {
        "rate": "-4%",
        "pitch": "-2Hz",
        "name": "Christopher (Epic Lorekeeper)"
    },
    "en-GB-RyanNeural": {
        "rate": "-3%",
        "pitch": "-2Hz",
        "name": "Ryan (British Fantasy Narrator)"
    },
    "en-US-EricNeural": {
        "rate": "-3%",
        "pitch": "-1Hz",
        "name": "Eric (Intense Battlefield Action)"
    },
    "en-GB-ThomasNeural": {
        "rate": "-5%",
        "pitch": "-3Hz",
        "name": "Thomas (Ancient Myth Chronicler)"
    }
}


def format_dramatic_narration(text: str) -> str:
    """Pre-processes narration text to introduce natural dramatic pauses, cadence, and tension,
    preventing flat robotic reading in Edge-TTS.
    """
    cleaned = text.strip().strip('"').strip("'")

    # Replace em-dashes and long dashes with anticipatory breath pauses
    cleaned = re.sub(r'\s*[—–]{1,2}\s*', ' ... ', cleaned)

    # Add breath pauses for dramatic conjunctions
    for conj in ["reminding the world", "before the realm", "and in doing so"]:
        if conj in cleaned and f" ... {conj}" not in cleaned:
            cleaned = cleaned.replace(f" {conj}", f" ... {conj}")

    # Punctuate colons and semicolons with natural pauses
    cleaned = cleaned.replace(':', ' ... ').replace(';', ', ')

    # Clean up excessive ellipsis or whitespace
    cleaned = re.sub(r'\.{4,}', '...', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned


from datetime import timedelta

def format_srt_time(td: timedelta) -> str:
    """Formats timedelta into SRT timestamp format: HH:MM:SS,mmm"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def split_cues_into_punchy_chunks(cues, max_words_per_chunk: int = 4):
    """Splits long sentence cues into punchy 3-5 word subtitle cards with natural timing."""
    punchy_cues = []
    cue_idx = 1
    for cue in cues:
        text = cue.content.strip()
        words = text.split()
        if len(words) <= max_words_per_chunk:
            punchy_cues.append({
                "index": cue_idx,
                "start": cue.start,
                "end": cue.end,
                "text": text
            })
            cue_idx += 1
            continue

        chunks = []
        for i in range(0, len(words), max_words_per_chunk):
            chunks.append(" ".join(words[i:i + max_words_per_chunk]))

        total_duration = (cue.end - cue.start).total_seconds()
        total_chars = sum(len(c) for c in chunks)

        current_start = cue.start
        for chunk in chunks:
            chunk_dur = total_duration * (len(chunk) / max(1, total_chars))
            current_end = current_start + timedelta(seconds=chunk_dur)
            punchy_cues.append({
                "index": cue_idx,
                "start": current_start,
                "end": current_end,
                "text": chunk
            })
            cue_idx += 1
            current_start = current_end

    return punchy_cues


def generate_srt(punchy_cues) -> str:
    """Renders cue dictionaries into standard SRT subtitle format."""
    lines = []
    for c in punchy_cues:
        lines.append(str(c["index"]))
        lines.append(f"{format_srt_time(c['start'])} --> {format_srt_time(c['end'])}")
        lines.append(c["text"])
        lines.append("")
    return "\n".join(lines)


def generate_fallback_subtitles(text: str, duration: float, srt_path: Path, max_words: int = 4):
    """Generates evenly spaced subtitle cards across audio duration if direct word boundaries are unavailable."""
    words = text.strip().split()
    if not words or duration <= 0:
        return
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))

    time_per_chunk = duration / len(chunks)
    cues = []
    for idx, chunk in enumerate(chunks, 1):
        start = timedelta(seconds=(idx - 1) * time_per_chunk)
        end = timedelta(seconds=min(duration, idx * time_per_chunk))
        cues.append({
            "index": idx,
            "start": start,
            "end": end,
            "text": chunk
        })
    srt_content = generate_srt(cues)
    with open(str(srt_path), "w", encoding="utf-8") as f:
        f.write(srt_content)


class AudioEngine:
    def __init__(self):
        self.engine = config.TTS_ENGINE
        self.voice = config.EDGE_TTS_VOICE
        self.voice_pool = config.EDGE_TTS_VOICE_POOL
        self.randomize_voices = config.RANDOMIZE_VOICES

    def _select_voice_profile(self) -> Dict[str, str]:
        """Selects a voice profile, randomizing across the pool if enabled."""
        if self.randomize_voices or self.voice in ("random", "", "auto"):
            voice_name = random.choice(self.voice_pool) if self.voice_pool else "en-US-GuyNeural"
        else:
            voice_name = self.voice

        profile = DRAMATIC_VOICE_PROFILES.get(voice_name, {
            "rate": "-4%",
            "pitch": "-2Hz",
            "name": f"{voice_name} (Custom)"
        })
        profile_copy = dict(profile)
        profile_copy["voice"] = voice_name
        return profile_copy

    def generate_voiceover(self, text: str, output_path: Optional[Path] = None) -> Path:
        """Generates voiceover narration using Edge-TTS or ElevenLabs."""
        timestamp = int(time.time())
        dest_path = output_path or (config.AUDIO_DIR / f"voiceover_{timestamp}.mp3")

        if self.engine == "elevenlabs" and config.ELEVENLABS_API_KEY:
            return self._generate_elevenlabs(text, dest_path)
        else:
            return self._generate_edge_tts(text, dest_path)

    def _generate_edge_tts(self, text: str, dest_path: Path) -> Path:
        """Generates hyper-realistic neural voiceover using Edge TTS with dramatic cadence and synced SRT subtitles."""
        profile = self._select_voice_profile()
        voice_id = profile["voice"]
        voice_label = profile.get("name", voice_id)
        rate = profile.get("rate", "-4%")
        pitch = profile.get("pitch", "-2Hz")

        dramatic_text = format_dramatic_narration(text)

        logger.info(f"[VOICE] Synthesizing voiceover with {voice_label} (Voice: {voice_id}, Rate: {rate}, Pitch: {pitch})...")
        try:
            import edge_tts

            async def _run():
                communicate = edge_tts.Communicate(
                    dramatic_text,
                    voice=voice_id,
                    rate=rate,
                    pitch=pitch
                )
                submaker = edge_tts.SubMaker()
                with open(str(dest_path), "wb") as f:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])
                        elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                            submaker.feed(chunk)

                srt_path = dest_path.with_suffix(".srt")
                if submaker.cues:
                    punchy = split_cues_into_punchy_chunks(
                        submaker.cues,
                        max_words_per_chunk=getattr(config, "SUBTITLE_WORDS_PER_CARD", 4)
                    )
                    srt_content = generate_srt(punchy)
                    with open(str(srt_path), "w", encoding="utf-8") as sf:
                        sf.write(srt_content)
                    logger.info(f"[SUBTITLES] Generated {len(punchy)} punchy subtitle cues: {srt_path.name}")
                else:
                    generate_fallback_subtitles(
                        dramatic_text,
                        15.0,
                        srt_path,
                        max_words=getattr(config, "SUBTITLE_WORDS_PER_CARD", 4)
                    )

            asyncio.run(_run())
            logger.info(f"[OK] Dramatic voiceover saved at: {dest_path}")
            return dest_path
        except Exception as e:
            logger.warning(f"Edge-TTS synthesis failed: {e}. Generating silent placeholder audio.")
            return self._generate_silent_audio(dest_path, duration=5.0)

    def _generate_elevenlabs(self, text: str, dest_path: Path) -> Path:
        """Generates voiceover using ElevenLabs API with synced fallback subtitles."""
        import requests
        logger.info(f"[VOICE] Generating voiceover with ElevenLabs...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config.ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        resp = requests.post(url, json=data, headers=headers)
        if resp.status_code == 200:
            with open(dest_path, "wb") as f:
                f.write(resp.content)
            logger.info(f"ElevenLabs voiceover saved to: {dest_path}")

            # Generate subtitles matching audio duration
            try:
                from src.composer import get_media_duration
                vo_dur = get_media_duration(dest_path)
                generate_fallback_subtitles(text, vo_dur, dest_path.with_suffix(".srt"))
            except Exception:
                pass

            return dest_path
        else:
            logger.error(f"ElevenLabs API error ({resp.status_code}): {resp.text}")
            return self._generate_edge_tts(text, dest_path)

    def _generate_silent_audio(self, dest_path: Path, duration: float = 5.0) -> Path:
        """Creates a silent WAV/MP3 fallback file if TTS dependencies are unavailable."""
        import wave
        import struct

        wav_path = dest_path.with_suffix(".wav")
        sample_rate = 44100
        num_frames = int(duration * sample_rate)
        with wave.open(str(wav_path), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            data = struct.pack('<' + ('h' * num_frames), *([0] * num_frames))
            wav_file.writeframes(data)
        return wav_path

    def get_background_music(self) -> Optional[Path]:
        """Returns a random royalty-free background track from assets/music/ if available."""
        tracks = list(config.MUSIC_DIR.glob("*.mp3")) + list(config.MUSIC_DIR.glob("*.wav"))
        if tracks:
            import random
            return random.choice(tracks)
        return None
