"""Free Multi-Image Storytelling Video Engine.
Generates 5-6 distinct AI visuals per Short and animates them with dynamic camera panning and atmosphere.
Completely free, with zero dependencies on paid API keys.
"""

import time
import math
import random
import logging
import urllib.request
import urllib.parse
import json
import io
from pathlib import Path
from typing import Optional, List

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

from src import config

logger = logging.getLogger(__name__)


class VideoEngine:
    def __init__(self, api_key: Optional[str] = None):
        # Zero API key required for free multi-image video generation
        pass

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
        Generates a 9:16 vertical video clip consisting of 5-6 distinct AI images
        choreographed with multi-angle camera panning (push-in, pan-right, tilt-up, pull-out, orbit-drift).
        100% Free - zero paid API key required!
        """
        timestamp = int(time.time())
        filename = output_filename or f"clip_{timestamp}.mp4"
        dest_path = config.RAW_VIDEO_DIR / filename

        # Explicit mock preview test
        if dry_run and engine == "mock":
            logger.info("[VIDEO] Generating synthetic test clip (Dry-Run / Mock Mode)...")
            return self._generate_mock_clip(dest_path, prompt)

        num_scenes = getattr(config, "NUM_SCENES", 5)
        logger.info(f"[VIDEO] Generating {num_scenes} distinct AI images for the topic...")

        # Step 1: Generate 5-6 genuinely distinct images for the topic
        image_paths = self._generate_distinct_images(prompt, count=num_scenes, base_timestamp=timestamp)

        # Step 2: Animate the 5-6 different images with multi-angle camera panning
        logger.info(f"[VIDEO] Animating {len(image_paths)} distinct images with cinematic camera panning & atmosphere...")
        return self._render_multi_image_cinematic_video(image_paths, dest_path, total_duration=duration)

    def _generate_distinct_images(self, prompt: str, count: int = 5, base_timestamp: int = 0) -> List[Path]:
        """
        Fetches 5-6 genuinely distinct AI images for the given topic.
        Primary: AI Horde free anonymous distributed generation (generates 5 distinct images in batch).
        Secondary: Pollinations free diffusion API with distinct camera angle prompts.
        """
        config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        image_paths = []

        # Extract core subject from prompt
        core = prompt.strip()
        for prefix in ["Cinematic vertical 9:16 framing.", "Cinematic vertical 9:16 framing", "Dynamic vertical 9:16 framing."]:
            core = core.replace(prefix, "").strip()
        core = core.split("Dynamic vertical")[0].split("Cinematic vertical")[0].strip()

        # Method 1: AI Horde Batch Generation (Generates 5-6 distinct images in one call)
        try:
            logger.info(f"   [AI IMAGES] Requesting batch of {count} distinct images from distributed free cluster...")
            horde_urls = self._fetch_horde_batch(core, count=count)
            if horde_urls:
                for url in horde_urls:
                    if len(image_paths) >= count:
                        break
                    dest_img = config.IMAGES_DIR / f"img_{base_timestamp}_scene{len(image_paths) + 1}.jpg"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=25) as resp:
                        img = Image.open(resp).convert("RGB")
                        if self._is_image_corrupt_or_censored(img):
                            logger.warning(f"   [AI IMAGES] Downloaded image is censored/corrupted. Discarding to regenerate clean image...")
                            continue
                        img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                        img.save(str(dest_img), "JPEG", quality=95)
                        image_paths.append(dest_img)
                        logger.info(f"   [SCENE {len(image_paths)}/{count}] Saved verified distinct image to {dest_img.name}")
        except Exception as e:
            logger.warning(f"   [AI IMAGES] AI Horde batch generation error: {e}")

        # Method 2: Resilient retry loop with backoff for any remaining scenes (filters out any censored images)
        if len(image_paths) < count:
            logger.info(f"   [AI IMAGES] Generating remaining {count - len(image_paths)} distinct scenes...")
            scene_modifiers = [
                "wide panoramic establishing shot, dark storm clouds, volumetric god rays",
                "intense macro close-up portrait, glowing eyes, intricate armor details",
                "high-speed dynamic combat action shot, flying debris, motion blur",
                "epic low-angle hero shot, unleashing glowing elemental energy shockwaves",
                "cinematic silhouette wide shot, standing victorious amidst embers and dust",
                "aerial top-down dramatic view, shattered environment, neon reflections"
            ]

            attempt_idx = 0
            while len(image_paths) < count and attempt_idx < 12:
                attempt_idx += 1
                idx = len(image_paths)
                dest_img = config.IMAGES_DIR / f"img_{base_timestamp}_scene{idx + 1}.jpg"
                modifier = scene_modifiers[idx % len(scene_modifiers)]
                clean_p = f"{core}, {modifier}, vertical 9:16 framing, photorealistic, 8k"

                # Polite spacing between scene requests
                if attempt_idx > 1:
                    wait_sec = min(20, 5 + attempt_idx * 3)
                    logger.info(f"   [SCENE {idx + 1}] Waiting {wait_sec}s before retry #{attempt_idx} to avoid rate limits...")
                    time.sleep(wait_sec)

                success = False
                try:
                    seed = random.randint(1000, 999999)
                    encoded_p = urllib.parse.quote(clean_p)
                    url = f"https://image.pollinations.ai/prompt/{encoded_p}?width=720&height=1280&nologo=true&seed={seed}"
                    req = urllib.request.Request(
                        url,
                        headers={"User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) ShortsBot/{seed % 100}"}
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        img = Image.open(resp).convert("RGB")
                        if self._is_image_corrupt_or_censored(img):
                            logger.warning(f"   [SCENE {idx + 1}] Downloaded image is censored/corrupt! Discarding to regenerate another in place...")
                        else:
                            w, h = img.size
                            if h > 50:
                                img = img.crop((0, 0, w, h - 45))
                                img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                            img.save(str(dest_img), "JPEG", quality=95)
                            image_paths.append(dest_img)
                            logger.info(f"   [SCENE {len(image_paths)}/{count}] Saved verified distinct image to {dest_img.name}")
                            success = True
                except Exception as e:
                    logger.warning(f"   [SCENE {idx + 1}] Pollinations attempt error: {e}")

                if not success and len(image_paths) < count:
                    # Single cluster fallback
                    logger.info(f"   [SCENE {idx + 1}] Requesting single fresh scene from cluster...")
                    try:
                        single_urls = self._fetch_horde_batch(clean_p, count=1, max_wait_seconds=45)
                        if single_urls:
                            sreq = urllib.request.Request(single_urls[0], headers={"User-Agent": "Mozilla/5.0"})
                            with urllib.request.urlopen(sreq, timeout=20) as sresp:
                                img = Image.open(sresp).convert("RGB")
                                if not self._is_image_corrupt_or_censored(img):
                                    img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                                    img.save(str(dest_img), "JPEG", quality=95)
                                    image_paths.append(dest_img)
                                    logger.info(f"   [SCENE {len(image_paths)}/{count}] Saved verified fallback image to {dest_img.name}")
                    except Exception as he:
                        logger.warning(f"   [SCENE {idx + 1}] Single cluster fallback error: {he}")

        return image_paths

    def _is_image_corrupt_or_censored(self, img: Image.Image) -> bool:
        """
        Validates an image to ensure it is not a censored warning, black placeholder, or corrupt render.
        Returns True if image is bad / censored, False if it is a valid scene image.
        """
        w, h = img.size
        if w < 200 or h < 200:
            return True
        arr = np.array(img)
        # Check for predominant black screen (> 75% pure black pixels) with low brightness
        # (Standard AI Horde / Stable Diffusion "CENSORED" warning text on pure black screen)
        black_ratio = float((arr < 25).all(axis=-1).mean())
        mean_brightness = float(arr.mean())
        if black_ratio > 0.75 and mean_brightness < 35.0:
            return True
        # Check for flat solid single color (corrupt or blank render)
        if float(arr.std()) < 6.0:
            return True
        return False

    def _fetch_horde_batch(self, prompt: str, count: int = 5, max_wait_seconds: int = 105) -> List[str]:
        """Submits a batch generation job to AI Horde and waits for completed, uncensored image URLs."""
        url = "https://aihorde.net/api/v2/generate/async"
        payload = json.dumps({
            "prompt": f"{prompt}, vertical 9:16 framing, masterpiece, photorealistic, 8k, cinematic lighting",
            "params": {"width": 512, "height": 768, "steps": 15, "n": count}
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "apikey": "0000000000",
            "User-Agent": "ShortsAutomator/2.0"
        }

        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            job_id = data.get("id")

        if not job_id:
            return []

        # Poll status every 3 seconds up to max_wait_seconds
        num_polls = max(10, max_wait_seconds // 3)
        for poll_i in range(num_polls):
            time.sleep(3)
            check_url = f"https://aihorde.net/api/v2/generate/check/{job_id}"
            creq = urllib.request.Request(check_url, headers=headers)
            try:
                with urllib.request.urlopen(creq, timeout=10) as cresp:
                    cdata = json.loads(cresp.read().decode())
                    done = cdata.get("done")
                    finished = cdata.get("finished", 0)
                    proc = cdata.get("processing", 0)
                    wait = cdata.get("waiting", 0)
                    if (poll_i + 1) % 4 == 0 or done:
                        logger.info(f"   [AI HORDE] Cluster status: {finished}/{count} ready (processing: {proc}, waiting: {wait})")
                    if done or (finished and finished >= count):
                        break
            except Exception:
                pass

        # Retrieve completed image URLs (ignoring any censored generations)
        status_url = f"https://aihorde.net/api/v2/generate/status/{job_id}"
        sreq = urllib.request.Request(status_url, headers=headers)
        with urllib.request.urlopen(sreq, timeout=15) as sresp:
            sdata = json.loads(sresp.read().decode())
            valid_urls = []
            for g in sdata.get("generations", []):
                if g.get("img") and not g.get("censored", False):
                    valid_urls.append(g.get("img"))
                elif g.get("censored"):
                    logger.warning("   [AI HORDE] Safety filter censored a generation. Discarding to regenerate clean image.")
            return valid_urls

    def _render_multi_image_cinematic_video(
        self,
        image_paths: List[Path],
        dest_video_path: Path,
        total_duration: float = 12.0,
        fps: int = 24
    ) -> Path:
        """
        Transforms distinct scene images into a seamless cinematic video montage using
        single-pass low-memory rendering (optimized for 512MB RAM cloud containers):
        - Alternates camera panning/zooming styles (Push-in, Pan Right, Tilt-Up, Pull-out, Orbit Drift).
        - Renders atmospheric floating embers and dust particles.
        - Employs single-clip evaluation with preset='ultrafast' and threads=1 to prevent OOM.
        """
        import gc
        gc.collect()

        try:
            from moviepy import VideoClip
        except ImportError:
            from moviepy.editor import VideoClip

        target_w, target_h = config.VIDEO_WIDTH, config.VIDEO_HEIGHT
        num_shots = len(image_paths)
        shot_duration = total_duration / max(1, num_shots)
        actual_total_duration = total_duration

        # Dynamic motion choreographies for distinct images
        motion_choreography = ["push_in", "pan_right", "tilt_up", "pull_out", "hero_drift", "push_in"]

        # Precompute floating atmospheric embers / starlight
        num_particles = 22
        particles = [
            {
                "x": random.uniform(0, target_w),
                "y": random.uniform(0, target_h),
                "vx": random.uniform(-8, 8),
                "vy": random.uniform(30, 60),
                "size": random.randint(2, 4),
                "color": random.choice([(255, 195, 70), (255, 120, 40), (120, 225, 255), (255, 255, 255)])
            }
            for _ in range(num_particles)
        ]

        # Pre-scale base images to target resolution
        base_images = [
            Image.open(str(p)).convert("RGB").resize((target_w, target_h), Image.Resampling.LANCZOS)
            for p in image_paths
        ]

        def make_frame(t):
            scene_idx = min(num_shots - 1, int(t / shot_duration))
            local_t = t - (scene_idx * shot_duration)
            progress = min(1.0, max(0.0, local_t / shot_duration))
            src_img = base_images[scene_idx]
            motion_type = motion_choreography[scene_idx % len(motion_choreography)]

            if motion_type == "push_in":
                scale = 1.0 + 0.15 * progress
                pan_x, pan_y = 0, 0
            elif motion_type == "pan_right":
                scale = 1.12
                pan_x = int(30.0 * (2.0 * progress - 1.0))
                pan_y = 0
            elif motion_type == "tilt_up":
                scale = 1.10
                pan_x = 0
                pan_y = int(30.0 * (1.0 - 2.0 * progress))
            elif motion_type == "pull_out":
                scale = 1.17 - 0.15 * progress
                pan_x, pan_y = 0, 0
            else:  # hero_drift
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
            brightness = 1.0 + 0.03 * math.sin(local_t * 2.5 + scene_idx)
            if brightness != 1.0:
                frame = ImageEnhance.Brightness(frame).enhance(brightness)

            # Draw floating embers / starlight
            draw = ImageDraw.Draw(frame)
            for p in particles:
                py = int((p["y"] - p["vy"] * t) % target_h)
                px = int((p["x"] + p["vx"] * t + 4.0 * math.sin(t * 2.0)) % target_w)
                sz = p["size"]
                draw.ellipse([px, py, px + sz, py + sz], fill=p["color"])

            return np.array(frame)

        logger.info(f"[COMPOSER] Rendering {num_shots} scenes into master montage (Low-RAM Single-Pass Mode)...")
        dest_video_path.parent.mkdir(parents=True, exist_ok=True)
        final_video = VideoClip(make_frame, duration=actual_total_duration)
        final_video.write_videofile(
            str(dest_video_path),
            fps=fps,
            codec="libx264",
            preset="ultrafast",
            threads=1,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            audio=False,
            logger=None
        )
        final_video.close()
        del final_video
        del base_images
        gc.collect()

        logger.info(f"[OK] Multi-Image Storytelling Montage created: {dest_video_path} (Duration: {actual_total_duration}s)")
        return dest_video_path

    def _generate_procedural_poster(self, dest_path: Path, prompt_text: str) -> Path:
        """Generates an atmospheric graphic poster if external image APIs are unreachable."""
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
            draw.text((50, h - 270), "Free Multi-Image Storytelling Engine", fill=(255, 200, 50))
            draw.text((50, h - 240), "5-6 Distinct AI Visuals with Panning", fill=(240, 240, 255))
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
