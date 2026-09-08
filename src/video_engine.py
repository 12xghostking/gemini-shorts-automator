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
        """Creates a smooth animated gradient 9:16 vertical MP4 for testing without API usage."""
        try:
            from moviepy import ColorClip
        except ImportError:
            from moviepy.editor import ColorClip

        duration = 5.0
        fps = config.VIDEO_FPS
        w, h = config.VIDEO_WIDTH, config.VIDEO_HEIGHT

        bg_clip = ColorClip(size=(w, h), color=(18, 18, 28), duration=duration)

        bg_clip.write_videofile(
            str(dest_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        logger.info(f"Mock video created at: {dest_path}")
        return dest_path
