"""Video Generation Engine supporting Google Veo and Free AI Image + 2.5D Cinematic Motion."""

import time
import math
import random
import logging
import urllib.request
import urllib.parse
import io
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

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
        resolution: str = "720p",
        engine: Optional[str] = None,
        duration: float = 6.0
    ) -> Path:
        """
        Generates a 9:16 vertical video clip.
        Engines:
          - 'free': High-definition AI image (FLUX/SDXL) + 2.5D cinematic camera motion (0 API credits!).
          - 'veo': Google Veo 3.1 video diffusion model (requires Gemini API key).
          - 'auto': Uses Veo if API key is active and not dry-run, else uses Free engine.
        """
        timestamp = int(time.time())
        filename = output_filename or f"clip_{timestamp}.mp4"
        dest_path = config.RAW_VIDEO_DIR / filename

        chosen_engine = (engine or config.VIDEO_ENGINE or "auto").lower()

        # Resolve 'auto' engine based on credential availability
        if chosen_engine == "auto":
            if self.client and not dry_run:
                chosen_engine = "veo"
            else:
                chosen_engine = "free"

        # Explicit dry-run mock mode
        if dry_run and chosen_engine == "mock":
            logger.info("[VIDEO] Generating synthetic test clip (Dry-Run / Mock Mode)...")
            return self._generate_mock_clip(dest_path, prompt)

        # -------------------------------------------------------------
        # 1. FREE ENGINE: AI Image + 2.5D Cinematic Motion (Zero Cost)
        # -------------------------------------------------------------
        if chosen_engine in ("free", "cinematic", "image"):
            logger.info("[VIDEO] Using Free AI Video Engine (FLUX/SDXL + 2.5D Cinematic Motion)...")
            image_filename = f"img_{timestamp}.jpg"
            image_dest = config.IMAGES_DIR / image_filename

            # Step A: Fetch free high-res AI visual
            self._fetch_free_ai_image(prompt, image_dest)

            # Step B: Render 9:16 dynamic camera motion and particle FX
            logger.info("[VIDEO] Animating image with cinematic camera pan, zoom & atmosphere...")
            return self._render_cinematic_motion_video(image_dest, dest_path, duration=duration)

        # -------------------------------------------------------------
        # 2. VEO ENGINE: Google Veo API (Requires Gemini Key)
        # -------------------------------------------------------------
        if not self.client:
            logger.warning("[VIDEO] Gemini API key not found. Falling back to Free AI Video Engine...")
            return self.generate_video(prompt, output_filename, dry_run, aspect_ratio, resolution, engine="free", duration=duration)

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
        try:
            self.client.files.download(file=generated_video.video, destination=str(dest_path))
        except Exception:
            if getattr(generated_video.video, "video_bytes", None):
                generated_video.video.save(str(dest_path))
            else:
                self.client.files.download(file=generated_video, destination=str(dest_path))

        logger.info(f"[OK] Video generated and saved successfully: {dest_path}")
        return dest_path

    def _fetch_free_ai_image(self, prompt: str, dest_path: Path) -> Path:
        """Fetches a free high-resolution vertical AI image without requiring an API key."""
        logger.info(f"[FREE IMAGE] Generating AI visual via Pollinations (FLUX)...")
        seed = random.randint(1000, 999999)
        # Clean and formulate the visual prompt
        clean_prompt = f"{prompt.strip()}, vertical 9:16 framing, photorealistic, 8k, masterpiece, cinematic lighting"
        encoded_prompt = urllib.parse.quote(clean_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true&model=flux&seed={seed}"

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
                img = Image.open(io.BytesIO(data)).convert("RGB")
                
                # Automatically remove any tiny footer watermark area cleanly
                w, h = img.size
                if h > 50:
                    img = img.crop((0, 0, w, h - 45))
                    img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                
                img.save(str(dest_path), "JPEG", quality=95)
                logger.info(f"[FREE IMAGE] Successfully saved AI image to {dest_path}")
                return dest_path
        except Exception as e:
            logger.warning(f"[FREE IMAGE] Pollinations fetch failed ({e}). Creating procedural fallback artwork...")
            return self._generate_procedural_poster(dest_path, prompt)

    def _render_cinematic_motion_video(
        self,
        image_path: Path,
        dest_video_path: Path,
        duration: float = 6.0,
        fps: int = 24
    ) -> Path:
        """
        Transforms a static 9:16 vertical image into a dynamic cinematic video
        with 2.5D Ken Burns camera zoom, tilt pan, floating embers, and breathing atmosphere.
        """
        try:
            from moviepy import VideoClip
        except ImportError:
            from moviepy.editor import VideoClip

        base_img = Image.open(str(image_path)).convert("RGB")
        target_w, target_h = 720, 1280
        base_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # Select camera movement profile
        motion_profile = random.choice(["push_in", "pull_out", "tilt_up"])
        
        # Precompute atmospheric floating embers / light particles
        num_particles = 32
        particles = [
            {
                "x": random.uniform(0, target_w),
                "y": random.uniform(0, target_h),
                "vx": random.uniform(-12, 12),
                "vy": random.uniform(35, 75),
                "size": random.randint(2, 5),
                "color": random.choice([(255, 195, 70), (255, 120, 40), (120, 225, 255), (255, 255, 255)])
            }
            for _ in range(num_particles)
        ]

        def make_frame(t):
            progress = min(1.0, max(0.0, t / duration))

            # Camera zoom and pan calculations
            if motion_profile == "push_in":
                # Dramatic slow zoom into the center/subject (1.0 -> 1.15)
                scale = 1.0 + 0.15 * progress
                pan_y_offset = 0
            elif motion_profile == "pull_out":
                # Reveal zoom pulling back (1.16 -> 1.02)
                scale = 1.16 - 0.14 * progress
                pan_y_offset = 0
            else:  # tilt_up
                # Vertical tilt upward from ground to sky
                scale = 1.08 + 0.05 * math.sin(progress * math.pi)
                pan_y_offset = int(35 * (1.0 - 2.0 * progress))

            crop_w = int(target_w / scale)
            crop_h = int(target_h / scale)

            # Organic handheld micro-drift
            drift_x = int(3.5 * math.sin(t * 1.8))
            drift_y = int(2.5 * math.cos(t * 1.3)) + pan_y_offset

            left = max(0, min(target_w - crop_w, (target_w - crop_w) // 2 + drift_x))
            top = max(0, min(target_h - crop_h, (target_h - crop_h) // 2 + drift_y))

            cropped = base_img.crop((left, top, left + crop_w, top + crop_h))
            frame = cropped.resize((target_w, target_h), Image.Resampling.BILINEAR)

            # Dynamic lighting pulse & cinematic contrast
            brightness_factor = 1.0 + 0.03 * math.sin(t * 2.2)
            if brightness_factor != 1.0:
                frame = ImageEnhance.Brightness(frame).enhance(brightness_factor)

            # Draw floating atmospheric embers / dust
            draw = ImageDraw.Draw(frame)
            for p in particles:
                py = int((p["y"] - p["vy"] * t) % target_h)
                px = int((p["x"] + p["vx"] * t + 6.0 * math.sin(t * 2.0)) % target_w)
                sz = p["size"]
                draw.ellipse([px, py, px + sz, py + sz], fill=p["color"])

            return np.array(frame)

        dest_video_path.parent.mkdir(parents=True, exist_ok=True)
        clip = VideoClip(make_frame, duration=duration)
        clip.write_videofile(
            str(dest_video_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        logger.info(f"[OK] Free cinematic motion video rendered: {dest_video_path}")
        return dest_video_path

    def _generate_procedural_poster(self, dest_path: Path, prompt_text: str) -> Path:
        """Generates an atmospheric graphic poster if external image API is unreachable."""
        w, h = 720, 1280
        img = Image.new("RGB", (w, h), color=(14, 10, 26))
        draw = ImageDraw.Draw(img)

        # Concentric glowing rings
        cx, cy = w // 2, h // 2 - 80
        for r, col in [(280, (40, 25, 70)), (200, (60, 40, 110)), (130, (0, 200, 255)), (70, (255, 80, 160))]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)

        draw.text((w // 2 - 110, h - 300), "ANCIENT LEGEND", fill=(255, 215, 0))
        img.save(str(dest_path), "JPEG", quality=95)
        return dest_path

    def _generate_mock_clip(self, dest_path: Path, prompt_text: str) -> Path:
        """Creates a synthetic animated 9:16 vertical MP4 with visual motion and badges for testing."""
        duration = 5.0
        fps = 24
        w, h = 540, 960

        try:
            from moviepy import VideoClip
        except ImportError:
            from moviepy.editor import VideoClip

        clean_prompt = prompt_text[:70] + "..." if len(prompt_text) > 70 else prompt_text

        def make_frame(t):
            r_bg = int(18 + 10 * math.sin(t * 1.5))
            g_bg = int(14 + 8 * math.cos(t * 2.0))
            b_bg = int(32 + 15 * math.sin(t * 1.2))

            img = Image.new("RGB", (w, h), color=(r_bg, g_bg, b_bg))
            draw = ImageDraw.Draw(img)

            cx, cy = w // 2, h // 2 - 60
            pulse1 = int(80 + 30 * math.sin(t * 3.5))
            draw.ellipse([cx - pulse1, cy - pulse1, cx + pulse1, cy + pulse1], outline=(0, 220, 255), width=3)

            scan_y = int((t * 220) % h)
            draw.line([(0, scan_y), (w, scan_y)], fill=(0, 255, 200, 100), width=2)

            draw.rectangle([30, 60, w - 30, 120], fill=(28, 24, 48), outline=(0, 220, 255), width=2)
            draw.text((w // 2 - 100, 80), "[ DRY-RUN / MOCK PREVIEW ]", fill=(0, 255, 220))

            draw.rectangle([30, h - 300, w - 30, h - 100], fill=(22, 18, 38), outline=(255, 60, 160), width=2)
            draw.text((50, h - 270), "AI Video Generator Status:", fill=(255, 200, 50))
            draw.text((50, h - 240), "Engine: Free AI + 2.5D Motion or Veo", fill=(240, 240, 255))
            draw.text((50, h - 210), f"Prompt: {clean_prompt}", fill=(180, 180, 210))

            return np.array(img)

        clip = VideoClip(make_frame, duration=duration)
        clip.write_videofile(
            str(dest_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        return dest_path
