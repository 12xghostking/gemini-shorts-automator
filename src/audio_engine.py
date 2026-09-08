"""Audio Engine for synthesizing voiceovers and handling background music."""

import os
import time
import asyncio
import logging
from pathlib import Path
from typing import Optional

from src import config

logger = logging.getLogger(__name__)

class AudioEngine:
    def __init__(self):
        self.engine = config.TTS_ENGINE
        self.voice = config.EDGE_TTS_VOICE

    def generate_voiceover(self, text: str, output_path: Optional[Path] = None) -> Path:
        """Generates voiceover narration using Edge-TTS or ElevenLabs."""
        timestamp = int(time.time())
        dest_path = output_path or (config.AUDIO_DIR / f"voiceover_{timestamp}.mp3")

        if self.engine == "elevenlabs" and config.ELEVENLABS_API_KEY:
            return self._generate_elevenlabs(text, dest_path)
        else:
            return self._generate_edge_tts(text, dest_path)

    def _generate_edge_tts(self, text: str, dest_path: Path) -> Path:
        """Generates hyper-realistic neural voiceover using Edge TTS (free)."""
        logger.info(f"[VOICE] Generating voiceover with Edge-TTS ({self.voice})...")
        try:
            import edge_tts

            async def _run():
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(str(dest_path))

            asyncio.run(_run())
            logger.info(f"[OK] Voiceover saved at: {dest_path}")
            return dest_path
        except Exception as e:
            logger.warning(f"Edge-TTS synthesis failed: {e}. Generating silent placeholder audio.")
            return self._generate_silent_audio(dest_path, duration=5.0)

    def _generate_elevenlabs(self, text: str, dest_path: Path) -> Path:
        """Generates voiceover using ElevenLabs API."""
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
