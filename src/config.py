"""Configuration manager for the Shorts Automator."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "output"
RAW_VIDEO_DIR = OUTPUT_DIR / "raw"
AUDIO_DIR = OUTPUT_DIR / "audio"
FINAL_VIDEO_DIR = OUTPUT_DIR / "final"
IMAGES_DIR = OUTPUT_DIR / "images"
ASSETS_DIR = PROJECT_ROOT / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"

for path in [OUTPUT_DIR, RAW_VIDEO_DIR, AUDIO_DIR, FINAL_VIDEO_DIR, IMAGES_DIR, ASSETS_DIR, MUSIC_DIR, FONTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Optional Concept Generation Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")

# Free Video Engine Settings
# Generates 5-6 distinct AI visuals per Short with 2.5D cinematic camera panning
VIDEO_ENGINE = "free"
NUM_SCENES = int(os.getenv("NUM_SCENES", "5"))



# YouTube Settings
YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")
YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "public").lower()

# TTS Settings
TTS_ENGINE = os.getenv("TTS_ENGINE", "edge-tts").lower()
EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "random")
RANDOMIZE_VOICES = os.getenv("RANDOMIZE_VOICES", "true").lower() in ("true", "1", "yes")
EDGE_TTS_VOICE_POOL = [
    v.strip() for v in os.getenv(
        "EDGE_TTS_VOICE_POOL",
        "en-US-GuyNeural,en-US-ChristopherNeural,en-GB-RyanNeural,en-US-EricNeural,en-GB-ThomasNeural"
    ).split(",") if v.strip()
]
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

# Subtitle / Caption Settings
BURN_SUBTITLES = os.getenv("BURN_SUBTITLES", "true").lower() in ("true", "1", "yes")
SUBTITLE_FONT_SIZE = int(os.getenv("SUBTITLE_FONT_SIZE", "42"))
SUBTITLE_MARGIN_V = int(os.getenv("SUBTITLE_MARGIN_V", "160"))
SUBTITLE_WORDS_PER_CARD = int(os.getenv("SUBTITLE_WORDS_PER_CARD", "4"))

# Video Settings
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "720"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1280"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "24"))
MAX_DURATION_SECONDS = int(os.getenv("MAX_DURATION_SECONDS", "59"))
NUM_SCENES = int(os.getenv("NUM_SCENES", "5"))


# Pipeline Behavior
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")
DAILY_TARGET_SHORTS = int(os.getenv("DAILY_TARGET_SHORTS", "24"))
