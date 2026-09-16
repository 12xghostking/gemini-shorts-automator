"""Video Generation Engine using Google Veo with Dry-Run / Mock capability."""

import time
import logging
from pathlib import Path
from typing import Optional

from src import config

logger = logging.getLogger(__name__)

class VideoEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize GenAI client for video: {e}")

    def generate_video(
        self,
        prompt: str,
        output_filename: Optional[str] = None,
        dry_run: bool = False,
        aspect_ratio: str = "9:16",
        resolution: str = "720p"
    ) -> Path:
        """
        Generates a 9:16 vertical video using Google Veo or generates a test clip in dry-run mode.
        """
        timestamp = int(time.time())
        filename = output_filename or f"clip_{timestamp}.mp4"
        dest_path = config.RAW_VIDEO_DIR / filename

        if dry_run or not self.client:
            logger.info("[VIDEO] Generating synthetic test clip (Dry-Run / Mock Mode)...")
            return self._generate_mock_clip(dest_path, prompt)

        from google.genai import types

        logger.info(f"[VIDEO] Sending video generation request to Veo ({config.GEMINI_VIDEO_MODEL})...")
        logger.info(f"Prompt: {prompt[:120]}...")

        operation = self.client.models.generate_videos(
            model=config.GEMINI_VIDEO_MODEL,
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                resolution=resolution
            )
        )

        logger.info("[VIDEO] Waiting for Veo video generation to complete (polling every 15s)...")
        wait_seconds = 0
        while not operation.done:
            time.sleep(15)
            wait_seconds += 15
            operation = self.client.operations.get(operation)
            logger.info(f"   ... still processing ({wait_seconds}s elapsed)")

        if operation.error:
            raise RuntimeError(f"Veo video generation failed: {operation.error}")

        generated_video = operation.response.generated_videos[0]
        # Download and save the video file
        generated_video.video.save(str(dest_path))
        logger.info(f"[OK] Video generated and saved successfully: {dest_path}")
        return dest_path

    def _generate_mock_clip(self, dest_path: Path, prompt_text: str) -> Path:
        """Creates a dynamic animated 9:16 vertical MP4 with visual motion and badges for testing."""
        import math
        import numpy as np
        from PIL import Image, ImageDraw

        try:
            from moviepy import VideoClip
        except ImportError:
            from moviepy.editor import VideoClip

        duration = 5.0
        fps = 24
        w, h = 540, 960  # Render at clean mobile 9:16 resolution for fast rendering

        clean_prompt = prompt_text[:70] + "..." if len(prompt_text) > 70 else prompt_text

        def make_frame(t):
            # Dynamic gradient background
            r_bg = int(18 + 10 * math.sin(t * 1.5))
            g_bg = int(14 + 8 * math.cos(t * 2.0))
            b_bg = int(32 + 15 * math.sin(t * 1.2))

            img = Image.new("RGB", (w, h), color=(r_bg, g_bg, b_bg))
            draw = ImageDraw.Draw(img)

            cx, cy = w // 2, h // 2 - 60

            # Pulsing energy circles
            pulse1 = int(80 + 30 * math.sin(t * 3.5))
            pulse2 = int(50 + 20 * math.cos(t * 4.0))
            draw.ellipse([cx - pulse1, cy - pulse1, cx + pulse1, cy + pulse1], outline=(0, 220, 255), width=3)
            draw.ellipse([cx - pulse2, cy - pulse2, cx + pulse2, cy + pulse2], outline=(255, 60, 160), width=2)

            # Animated horizontal scan lines
            scan_y = int((t * 220) % h)
            draw.line([(0, scan_y), (w, scan_y)], fill=(0, 255, 200, 100), width=2)

            # Top Badge
            draw.rectangle([30, 60, w - 30, 120], fill=(28, 24, 48), outline=(0, 220, 255), width=2)
            draw.text((w // 2 - 100, 80), "[ DRY-RUN / MOCK PREVIEW ]", fill=(0, 255, 220))

            # Center Info Box
            draw.rectangle([30, h - 340, w - 30, h - 80], fill=(22, 18, 38), outline=(255, 60, 160), width=2)
            draw.text((50, h - 310), "AI Video Generator Status:", fill=(255, 200, 50))
            draw.text((50, h - 280), "Live Veo 3 Video replaces this visual", fill=(240, 240, 255))
            draw.text((50, h - 250), "when you run with: --live", fill=(0, 255, 180))

            # Prompt preview
            draw.text((50, h - 200), "Prompt Preview:", fill=(180, 180, 210))
            draw.text((50, h - 170), f"\"{clean_prompt}\"", fill=(220, 220, 240))

            # Dynamic timeline / progress bar
            prog_w = int(((t / duration)) * (w - 60))
            draw.rectangle([30, h - 50, 30 + prog_w, h - 40], fill=(0, 255, 200))

            return np.array(img)

        clip = VideoClip(make_frame, duration=duration)
        clip.write_videofile(
            str(dest_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        logger.info(f"Mock video created at: {dest_path}")
        return dest_path
