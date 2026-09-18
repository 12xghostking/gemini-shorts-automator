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
                for idx, url in enumerate(horde_urls):
                    dest_img = config.IMAGES_DIR / f"img_{base_timestamp}_scene{idx + 1}.jpg"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        img = Image.open(resp).convert("RGB")
                        img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                        img.save(str(dest_img), "JPEG", quality=95)
                        image_paths.append(dest_img)
                        logger.info(f"   [SCENE {idx + 1}/{len(horde_urls)}] Saved distinct image to {dest_img.name}")
        except Exception as e:
            logger.warning(f"   [AI IMAGES] AI Horde batch generation error: {e}")

        # Method 2: Fallback via Pollinations if AI Horde was unavailable or returned < 2 images
        if len(image_paths) < count:
            logger.info(f"   [AI IMAGES] Generating remaining scenes via Pollinations...")
            scene_modifiers = [
                "wide panoramic establishing shot, dark storm clouds, volumetric god rays",
                "intense macro close-up portrait, glowing eyes, intricate armor details",
                "high-speed dynamic combat action shot, flying debris, motion blur",
                "epic low-angle hero shot, unleashing glowing elemental energy shockwaves",
                "cinematic silhouette wide shot, standing victorious amidst embers and dust",
                "aerial top-down dramatic view, shattered environment, neon reflections"
            ]

            needed = count - len(image_paths)
            start_idx = len(image_paths)
            for i in range(needed):
                idx = start_idx + i
                dest_img = config.IMAGES_DIR / f"img_{base_timestamp}_scene{idx + 1}.jpg"
                modifier = scene_modifiers[idx % len(scene_modifiers)]
                clean_p = f"{core}, {modifier}, vertical 9:16 framing, photorealistic, 8k"

                try:
                    seed = random.randint(1000, 999999)
                    encoded_p = urllib.parse.quote(clean_p)
                    url = f"https://image.pollinations.ai/prompt/{encoded_p}?width=720&height=1280&nologo=true&seed={seed}"
                    req = urllib.request.Request(url, headers={"User-Agent": f"Mozilla/5.0 App/{seed % 100}"})
                    with urllib.request.urlopen(req, timeout=18) as resp:
                        img = Image.open(resp).convert("RGB")
                        w, h = img.size
                        if h > 50:
                            img = img.crop((0, 0, w, h - 45))
                            img = img.resize((720, 1280), Image.Resampling.LANCZOS)
                        img.save(str(dest_img), "JPEG", quality=95)
                        image_paths.append(dest_img)
                        logger.info(f"   [SCENE {idx + 1}/{count}] Saved distinct image to {dest_img.name}")
                except Exception as e:
                    logger.warning(f"   [SCENE {idx + 1}] Pollinations error: {e}")
                    # If network was rate-limited, create an artistic angle variation
                    if image_paths:
                        self._create_storyboard_angle(image_paths[0], dest_img, angle_idx=idx)
                        image_paths.append(dest_img)
                    else:
                        self._generate_procedural_poster(dest_img, core)
                        image_paths.append(dest_img)

        return image_paths

    def _fetch_horde_batch(self, prompt: str, count: int = 5) -> List[str]:
        """Submits a batch generation job to AI Horde and waits for completed image URLs."""
        url = "https://aihorde.net/api/v2/generate/async"
        payload = json.dumps({
            "prompt": f"{prompt}, vertical 9:16 framing, masterpiece, photorealistic, 8k, cinematic lighting",
            "params": {"width": 512, "height": 768, "steps": 15, "n": count}
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "apikey": "0000000000",
            "User-Agent": "ShortsAutomator/1.0"
        }

        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            job_id = data.get("id")

        if not job_id:
            return []

        # Poll status every 2 seconds for up to 35 seconds
        for _ in range(18):
            time.sleep(2)
            check_url = f"https://aihorde.net/api/v2/generate/check/{job_id}"
            creq = urllib.request.Request(check_url, headers=headers)
            try:
                with urllib.request.urlopen(creq, timeout=10) as cresp:
                    cdata = json.loads(cresp.read().decode())
                    if cdata.get("done"):
                        break
            except Exception:
                pass

        # Retrieve completed image URLs
        status_url = f"https://aihorde.net/api/v2/generate/status/{job_id}"
        sreq = urllib.request.Request(status_url, headers=headers)
        with urllib.request.urlopen(sreq, timeout=15) as sresp:
            sdata = json.loads(sresp.read().decode())
            return [g.get("img") for g in sdata.get("generations", []) if g.get("img")]

    def _create_storyboard_angle(self, master_image_path: Path, dest_path: Path, angle_idx: int) -> Path:
        """Creates an artistic framing angle variation if an API call was dropped."""
        master = Image.open(str(master_image_path)).convert("RGB")
        w, h = 720, 1280
        master = master.resize((w, h), Image.Resampling.LANCZOS)

        if angle_idx == 1:
            crop_w, crop_h = int(w / 1.45), int(h / 1.45)
            framed = master.crop(((w - crop_w) // 2, int(h * 0.15), (w - crop_w) // 2 + crop_w, int(h * 0.15) + crop_h))
            framed = ImageEnhance.Contrast(framed).enhance(1.08)
        elif angle_idx == 2:
            crop_w, crop_h = int(w / 1.35), int(h / 1.35)
            framed = master.crop((int(w * 0.20), int(h * 0.25), int(w * 0.20) + crop_w, int(h * 0.25) + crop_h))
            framed = ImageEnhance.Color(framed).enhance(1.12)
        elif angle_idx == 3:
            crop_w, crop_h = int(w / 1.25), int(h / 1.25)
            framed = master.crop((int(w * 0.05), int(h * 0.05), int(w * 0.05) + crop_w, int(h * 0.05) + crop_h))
        elif angle_idx == 4:
            crop_w, crop_h = int(w / 1.30), int(h / 1.30)
            framed = master.crop(((w - crop_w) // 2, int(h * 0.20), (w - crop_w) // 2 + crop_w, int(h * 0.20) + crop_h))
            framed = ImageEnhance.Brightness(framed).enhance(1.04)
        else:
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
        Transforms 5-6 distinct scene images into a seamless cinematic video montage:
        - Alternates camera panning/zooming styles (Push-in, Pan Right, Tilt-Up, Pull-out, Orbit Drift).
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

        # Dynamic motion choreographies for distinct images
        motion_choreography = ["push_in", "pan_right", "tilt_up", "pull_out", "hero_drift", "push_in"]

        # Precompute floating atmospheric embers / starlight
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
                        scale = 1.0 + 0.15 * progress
                        pan_x, pan_y = 0, 0
                    elif motion_type == "pan_right":
                        scale = 1.12
                        pan_x = int(32.0 * (2.0 * progress - 1.0))
                        pan_y = 0
                    elif motion_type == "tilt_up":
                        scale = 1.10
                        pan_x = 0
                        pan_y = int(32.0 * (1.0 - 2.0 * progress))
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

        logger.info(f"[COMPOSER] Assembling {len(clips)} distinct scene clips into master montage...")
        dest_video_path.parent.mkdir(parents=True, exist_ok=True)
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            str(dest_video_path),
            fps=fps,
            codec="libx264",
            audio=False,
            logger=None
        )
        logger.info(f"[OK] Multi-Image Storytelling Montage created: {dest_video_path} (Duration: {final_video.duration}s)")
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
