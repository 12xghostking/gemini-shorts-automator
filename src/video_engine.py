"""Video Generation Engine supporting Google Veo and Free 5-Scene Multi-Image Cinematic Storytelling Montages."""

import time
import math
import random
import logging
import urllib.request
import urllib.parse
import io
from pathlib import Path
from typing import Optional, List

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
        duration: float = 12.0
    ) -> Path:
        """
        Generates a 9:16 vertical video clip.
        Engines:
          - 'free': 5-scene cinematic storytelling montage with dynamic camera panning across 5 AI images (0 API credits!).
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
        # 1. FREE ENGINE: 5-Scene Multi-Image Cinematic Storytelling Montage
        # -------------------------------------------------------------
        if chosen_engine in ("free", "cinematic", "image", "montage"):
            num_scenes = getattr(config, "NUM_SCENES", 5)
            logger.info(f"[VIDEO] Using Free AI Video Engine ({num_scenes}-Shot Storytelling Montage, FLUX)...")

            # Step A: Decompose concept into 5 progressive storytelling scene prompts
            scene_prompts = self._decompose_into_storyboard_scenes(prompt, num_scenes=num_scenes)

            # Step B: Fetch scene images
            logger.info(f"[VIDEO] Fetching {len(scene_prompts)} cinematic storyboard scenes...")
            image_paths = self._fetch_scene_images(scene_prompts, base_timestamp=timestamp)

            # Step C: Animate and concatenate 5 panning/zooming cinematic shots
            logger.info(f"[VIDEO] Animating {len(image_paths)} scenes with multi-angle camera panning & atmosphere...")
            return self._render_multi_image_cinematic_video(image_paths, dest_path, total_duration=duration)

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

    def _decompose_into_storyboard_scenes(self, prompt: str, num_scenes: int = 5) -> List[str]:
        """
        Decomposes a single concept prompt into 5 progressive storytelling shots:
        1. Wide establishing environment shot
        2. Macro character / weapon close-up
        3. High-speed combat action charge
        4. Apocalyptic power climax
        5. Heroic aftermath / victory silhouette
        """
        core = prompt.strip()
        for prefix in ["Cinematic vertical 9:16 framing.", "Cinematic vertical 9:16 framing", "Dynamic vertical 9:16 framing."]:
            core = core.replace(prefix, "").strip()
        core = core.split("Dynamic vertical")[0].split("Cinematic vertical")[0].strip()

        shot_templates = [
            # Shot 1: Wide Establishing
            f"Cinematic vertical 9:16 wide establishing shot. {core}, panoramic grand environment, dark storm clouds, volumetric atmospheric god rays, photorealistic 8k",
            # Shot 2: Intense Macro Close-up
            f"Cinematic vertical 9:16 macro close-up portrait. {core}, glowing focused eyes, intricate weapon engravings, rain reflections, high-contrast chiaroscuro, 8k",
            # Shot 3: High-speed Action
            f"Cinematic vertical 9:16 dynamic combat action shot. {core}, charging at supersonic speed, shattered debris flying, motion blur, 8k render",
            # Shot 4: Apocalyptic Climax
            f"Cinematic vertical 9:16 low-angle hero shot. {core}, unleashing apocalyptic glowing elemental blast, blinding shockwaves ripping the sky, 8k",
            # Shot 5: Heroic Aftermath
            f"Cinematic vertical 9:16 cinematic wide silhouette shot. {core}, standing victorious atop mountain of ruins, embers drifting through dark mist, masterpiece 8k"
        ]

        return shot_templates[:num_scenes]

    def _fetch_scene_images(self, scene_prompts: List[str], base_timestamp: int) -> List[Path]:
        """Fetches multiple storyboard scenes, gracefully handling API pacing and caching."""
        image_paths = []
        config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        rate_limited = False

        for idx, prompt_text in enumerate(scene_prompts):
            dest_image = config.IMAGES_DIR / f"img_{base_timestamp}_scene{idx + 1}.jpg"

            # If rate-limiting was detected, instantly generate dramatic multi-angle framing from master scene
            if rate_limited and image_paths:
                logger.info(f"   [SCENE {idx + 1}/{len(scene_prompts)}] Composing cinematic angle from master scene...")
                self._create_storyboard_angle(image_paths[0], dest_image, angle_idx=idx)
                image_paths.append(dest_image)
                continue

            logger.info(f"   [SCENE {idx + 1}/{len(scene_prompts)}] Generating visual...")
            success = False

            try:
                seed = random.randint(1000, 999999)
                clean_p = f"{prompt_text.strip()}, photorealistic, 8k, masterpiece"
                encoded_p = urllib.parse.quote(clean_p)
                url = f"https://image.pollinations.ai/prompt/{encoded_p}?width=720&height=1280&nologo=true&model=flux&seed={seed}"

                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=18) as resp:
                    data = resp.read()
                    img = Image.open(io.BytesIO(data)).convert("RGB")

                    # Remove bottom watermark area cleanly
                    w, h = img.size
                    if h > 50:
                        img = img.crop((0, 0, w, h - 45))
                        img = img.resize((720, 1280), Image.Resampling.LANCZOS)

                    img.save(str(dest_image), "JPEG", quality=95)
                    image_paths.append(dest_image)
                    success = True
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    logger.info(f"   [SCENE {idx + 1}] Public API rate-limited (429). Switching to cinematic multi-angle camera framing...")
                    rate_limited = True
            except Exception as e:
                logger.warning(f"   [SCENE {idx + 1}] Fetch failed ({e})")

            if not success:
                if image_paths:
                    self._create_storyboard_angle(image_paths[0], dest_image, angle_idx=idx)
                    image_paths.append(dest_image)
                else:
                    self._generate_procedural_poster(dest_image, prompt_text)
                    image_paths.append(dest_image)

            # Brief pause between scene requests
            if not rate_limited:
                time.sleep(0.5)

        return image_paths

    def _create_storyboard_angle(self, master_image_path: Path, dest_path: Path, angle_idx: int) -> Path:
        """
        Creates 5 distinct cinematic camera framing angles from a high-resolution master scene:
        Angle 0: Full establishing wide shot
        Angle 1: Intense upper-body / face macro close-up (1.45x zoom)
        Angle 2: Mid-action weapon focus (1.35x zoom with slight lateral offset)
        Angle 3: Atmospheric panoramic reveal (shifted background perspective)
        Angle 4: Low-angle heroic silhouette
        """
        master = Image.open(str(master_image_path)).convert("RGB")
        w, h = 720, 1280
        master = master.resize((w, h), Image.Resampling.LANCZOS)

        if angle_idx == 1:
            # Macro Face / Eyes Close-Up (Zoom in to upper-middle third)
            crop_w, crop_h = int(w / 1.45), int(h / 1.45)
            left = (w - crop_w) // 2
            top = int(h * 0.15)
            framed = master.crop((left, top, left + crop_w, top + crop_h))
            framed = ImageEnhance.Contrast(framed).enhance(1.08)
        elif angle_idx == 2:
            # Weapon / Combat Focus (Zoom in to middle-right third)
            crop_w, crop_h = int(w / 1.35), int(h / 1.35)
            left = int(w * 0.20)
            top = int(h * 0.25)
            framed = master.crop((left, top, left + crop_w, top + crop_h))
            framed = ImageEnhance.Color(framed).enhance(1.12)
        elif angle_idx == 3:
            # Panoramic Environment (Lower-third focus looking up)
            crop_w, crop_h = int(w / 1.25), int(h / 1.25)
            left = int(w * 0.05)
            top = int(h * 0.05)
            framed = master.crop((left, top, left + crop_w, top + crop_h))
        elif angle_idx == 4:
            # Low-Angle Heroic Stance (Centered lower third)
            crop_w, crop_h = int(w / 1.30), int(h / 1.30)
            left = (w - crop_w) // 2
            top = int(h * 0.20)
            framed = master.crop((left, top, left + crop_w, top + crop_h))
            framed = ImageEnhance.Brightness(framed).enhance(1.04)
        else:
            # Wide establishing shot
            framed = master

        framed = framed.resize((w, h), Image.Resampling.LANCZOS)
        framed.save(str(dest_path), "JPEG", quality=95)
        return dest_path


    def _render_multi_image_cinematic_video(
        self,
        image_paths: List[Path],
        dest_video_path: Path,
        total_duration: float = 12.0,
        fps: int = 24
    ) -> Path:
        """
        Transforms 5 distinct scene images into a seamless cinematic video montage:
        - Alternates 5 camera panning/zooming styles (Push-in, Pan Right, Tilt-Up, Pull-out, Hero Drift).
        - Renders atmospheric floating embers and dust particles.
        - Concatenates into a single 9:16 vertical MP4 video.
        """
        try:
            from moviepy import VideoClip, concatenate_videoclips
        except ImportError:
            from moviepy.editor import VideoClip, concatenate_videoclips

        target_w, target_h = 720, 1280
        num_shots = len(image_paths)
        shot_duration = max(2.0, total_duration / max(1, num_shots))

        # Motion choreographies corresponding to the 5 storytelling beats
        motion_choreography = ["push_in", "pan_right", "tilt_up", "pull_out", "hero_drift"]

        # Precompute floating atmospheric particles / embers
        num_particles = 28
        particles = [
            {
                "x": random.uniform(0, target_w),
                "y": random.uniform(0, target_h),
                "vx": random.uniform(-10, 10),
                "vy": random.uniform(35, 70),
                "size": random.randint(2, 5),
                "color": random.choice([(255, 195, 70), (255, 120, 40), (120, 225, 255), (255, 255, 255)])
            }
            for _ in range(num_particles)
        ]

        clips = []
        for idx, img_path in enumerate(image_paths):
            base_img = Image.open(str(img_path)).convert("RGB").resize((target_w, target_h), Image.Resampling.LANCZOS)
            motion = motion_choreography[idx % len(motion_choreography)]

            def make_frame_factory(src_img, motion_type, scene_idx):
                def make_frame(t):
                    progress = min(1.0, max(0.0, t / shot_duration))

                    if motion_type == "push_in":
                        # Dramatic slow zoom into character (1.0 -> 1.15)
                        scale = 1.0 + 0.15 * progress
                        pan_x, pan_y = 0, 0
                    elif motion_type == "pan_right":
                        # Horizontal camera pan from left to right
                        scale = 1.12
                        pan_x = int(32.0 * (2.0 * progress - 1.0))
                        pan_y = 0
                    elif motion_type == "tilt_up":
                        # Dramatic vertical tilt from ground to sky
                        scale = 1.10
                        pan_x = 0
                        pan_y = int(32.0 * (1.0 - 2.0 * progress))
                    elif motion_type == "pull_out":
                        # Reveal pull back expanding the view (1.17 -> 1.02)
                        scale = 1.17 - 0.15 * progress
                        pan_x, pan_y = 0, 0
                    else:  # hero_drift
                        # Organic circular orbit drift with subtle zoom
                        scale = 1.04 + 0.10 * progress
                        pan_x = int(4.0 * math.sin(progress * math.pi * 2))
                        pan_y = int(3.0 * math.cos(progress * math.pi * 2))

                    crop_w = int(target_w / scale)
                    crop_h = int(target_h / scale)

                    left = max(0, min(target_w - crop_w, (target_w - crop_w) // 2 + pan_x))
                    top = max(0, min(target_h - crop_h, (target_h - crop_h) // 2 + pan_y))

                    cropped = src_img.crop((left, top, left + crop_w, top + crop_h))
                    frame = cropped.resize((target_w, target_h), Image.Resampling.BILINEAR)

                    # Dynamic atmospheric lighting breathing
                    brightness = 1.0 + 0.03 * math.sin(t * 2.5 + scene_idx)
                    if brightness != 1.0:
                        frame = ImageEnhance.Brightness(frame).enhance(brightness)

                    # Draw floating embers / starlight
                    draw = ImageDraw.Draw(frame)
                    for p in particles:
                        py = int((p["y"] - p["vy"] * (t + scene_idx * shot_duration)) % target_h)
                        px = int((p["x"] + p["vx"] * (t + scene_idx * shot_duration) + 5.0 * math.sin(t * 2.0)) % target_w)
                        sz = p["size"]
                        draw.ellipse([px, py, px + sz, py + sz], fill=p["color"])

                    return np.array(frame)
                return make_frame

            clip = VideoClip(make_frame_factory(base_img, motion, idx), duration=shot_duration)
            clips.append(clip)

        logger.info(f"[COMPOSER] Assembling {len(clips)} panning shots into master montage...")
        dest_video_path.parent.mkdir(parents=True, exist_ok=True)
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            str(dest_video_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        logger.info(f"[OK] 5-Shot Storytelling Montage created: {dest_video_path} (Duration: {final_video.duration}s)")
        return dest_video_path

    def _generate_procedural_poster(self, dest_path: Path, prompt_text: str) -> Path:
        """Generates an atmospheric graphic poster if external image API is unreachable."""
        w, h = 720, 1280
        img = Image.new("RGB", (w, h), color=(14, 10, 26))
        draw = ImageDraw.Draw(img)

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
            draw.text((50, h - 240), "Engine: Free AI 5-Shot Montage or Veo", fill=(240, 240, 255))
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
