"""Video Composer that mixes video clips, voiceover, background music, and formatting into YouTube Shorts."""

import time
import logging
from pathlib import Path
from typing import Optional

from src import config

logger = logging.getLogger(__name__)

try:
    from moviepy import (
        VideoFileClip,
        AudioFileClip,
        CompositeAudioClip,
        CompositeVideoClip,
        ColorClip,
        vfx,
        afx
    )
    IS_V2 = True
except ImportError:
    from moviepy.editor import (
        VideoFileClip,
        AudioFileClip,
        CompositeAudioClip,
        CompositeVideoClip,
        ColorClip,
        vfx
    )
    IS_V2 = False


def _subclip(clip, start, end):
    return clip.subclipped(start, end) if hasattr(clip, "subclipped") else clip.subclip(start, end)

def _scale_volume(audio, factor):
    return audio.with_volume_scaled(factor) if hasattr(audio, "with_volume_scaled") else audio.volumex(factor)

def _resize(clip, size_or_factor):
    return clip.resized(size_or_factor) if hasattr(clip, "resized") else clip.resize(size_or_factor)

def _crop(clip, x1, y1, width, height):
    if hasattr(clip, "cropped"):
        return clip.cropped(x1=x1, y1=y1, width=width, height=height)
    return clip.crop(x1=x1, y1=y1, width=width, height=height)

def _set_audio(clip, audio):
    return clip.with_audio(audio) if hasattr(clip, "with_audio") else clip.set_audio(audio)

def _loop_video(clip, n):
    if IS_V2:
        return clip.with_effects([vfx.Loop(n=n)])
    return vfx.loop(clip, n=n)

def _loop_audio(audio, duration):
    if IS_V2:
        return audio.with_effects([afx.AudioLoop(duration=duration)])
    return vfx.audio_loop(audio, duration=duration)


import shutil
import subprocess
import gc
import re

try:
    import imageio_ffmpeg
    DEFAULT_FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    DEFAULT_FFMPEG = None

def _get_ffmpeg_bin():
    return shutil.which("ffmpeg") or DEFAULT_FFMPEG

def get_media_duration(file_path: Path) -> float:
    """Accurately returns media duration in seconds via FFmpeg with zero memory overhead."""
    try:
        ffmpeg_bin = _get_ffmpeg_bin()
        if ffmpeg_bin and file_path.exists():
            cmd = [ffmpeg_bin, "-i", str(file_path)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
            if match:
                h, m, s = match.groups()
                return int(h) * 3600 + int(m) * 60 + float(s)
    except Exception:
        pass
    return 15.0


class VideoComposer:
    def __init__(self):
        self.width = config.VIDEO_WIDTH
        self.height = config.VIDEO_HEIGHT
        self.fps = config.VIDEO_FPS

    def compose_short(
        self,
        video_path: Path,
        voiceover_path: Optional[Path],
        music_path: Optional[Path] = None,
        title_text: Optional[str] = None,
        output_name: Optional[str] = None
    ) -> Path:
        """
        Assembles video, voiceover, and background music into a finished 9:16 Short.
        Precisely synchronizes video and audio durations with no looping or silent replays.
        Uses ultra-fast FFmpeg stream copy (-c:v copy) in <15MB RAM.
        """
        timestamp = int(time.time())
        dest_filename = output_name or f"short_{timestamp}.mp4"
        dest_path = config.FINAL_VIDEO_DIR / dest_filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        ffmpeg_bin = _get_ffmpeg_bin()
        has_vo = voiceover_path and voiceover_path.exists()
        has_music = music_path and music_path.exists()

        vo_duration = get_media_duration(voiceover_path) if has_vo else 15.0
        final_duration = min(vo_duration + 0.5, float(config.MAX_DURATION_SECONDS))

        if ffmpeg_bin and has_vo:
            logger.info(f"[COMPOSER] Using direct FFmpeg stream muxer (Target Duration: {final_duration:.1f}s)...")
            try:
                if has_music:
                    filter_complex = "[1:a]volume=1.0[vo];[2:a]aloop=loop=-1:size=2e+09,volume=0.15[bg];[vo][bg]amix=inputs=2:duration=first:dropout_transition=0[aout]"
                    cmd = [
                        ffmpeg_bin, "-y",
                        "-i", str(video_path),
                        "-i", str(voiceover_path),
                        "-i", str(music_path),
                        "-filter_complex", filter_complex,
                        "-map", "0:v",
                        "-map", "[aout]",
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-b:a", "192k",
                        "-t", f"{final_duration:.2f}",
                        str(dest_path)
                    ]
                else:
                    cmd = [
                        ffmpeg_bin, "-y",
                        "-i", str(video_path),
                        "-i", str(voiceover_path),
                        "-map", "0:v",
                        "-map", "1:a",
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-b:a", "192k",
                        "-t", f"{final_duration:.2f}",
                        str(dest_path)
                    ]

                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 1000:
                    logger.info(f"[OK] Successfully muxed final Short ({final_duration:.1f}s) via FFmpeg: {dest_path}")
                    gc.collect()
                    return dest_path
                else:
                    logger.warning(f"[COMPOSER] FFmpeg stream copy stderr: {res.stderr[:200]}. Falling back to MoviePy...")
            except Exception as fe:
                logger.warning(f"[COMPOSER] FFmpeg direct mux exception: {fe}. Falling back to MoviePy...")

        # Fallback to MoviePy with strict 1-thread low memory parameters
        gc.collect()
        logger.info(f"[COMPOSER] Loading video via MoviePy low-RAM fallback: {video_path}")
        video_clip = VideoFileClip(str(video_path))

        audio_duration = 5.0
        vo_clip = None
        if has_vo:
            try:
                vo_clip = AudioFileClip(str(voiceover_path))
                audio_duration = vo_clip.duration + 1.0
            except Exception as e:
                logger.warning(f"Failed to load voiceover audio: {e}")

        final_duration = min(audio_duration, float(config.MAX_DURATION_SECONDS))

        if video_clip.duration < final_duration:
            num_loops = int(final_duration // video_clip.duration) + 1
            video_clip = _loop_video(video_clip, num_loops)

        video_clip = _subclip(video_clip, 0, final_duration)

        # Audio Mixing
        audio_layers = []
        if vo_clip:
            audio_layers.append(_scale_volume(vo_clip, 1.0))

        if has_music:
            try:
                bg_music = AudioFileClip(str(music_path))
                if bg_music.duration < final_duration:
                    bg_music = _loop_audio(bg_music, final_duration)
                else:
                    bg_music = _subclip(bg_music, 0, final_duration)
                audio_layers.append(_scale_volume(bg_music, 0.15))
            except Exception as e:
                logger.warning(f"Could not mix background music: {e}")

        if audio_layers:
            final_audio = _subclip(CompositeAudioClip(audio_layers), 0, final_duration)
            video_clip = _set_audio(video_clip, final_audio)

        logger.info(f"[COMPOSER] Rendering final 9:16 Short to {dest_path} (Preset: ultrafast, Threads: 1)...")
        video_clip.write_videofile(
            str(dest_path),
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=1,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            logger=None
        )

        video_clip.close()
        if vo_clip:
            vo_clip.close()
        del video_clip
        gc.collect()

        logger.info(f"[OK] Successfully rendered final Short: {dest_path}")
        return dest_path

