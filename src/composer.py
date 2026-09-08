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
        Assembles video, voiceover, background music, and overlays into a finished 1080x1920 Short.
        """
        timestamp = int(time.time())
        dest_filename = output_name or f"short_{timestamp}.mp4"
        dest_path = config.FINAL_VIDEO_DIR / dest_filename

        logger.info(f"[COMPOSER] Loading raw video: {video_path}")
        video_clip = VideoFileClip(str(video_path))

        # 1. Determine target duration based on voiceover
        audio_duration = 5.0
        vo_clip = None
        if voiceover_path and voiceover_path.exists():
            try:
                vo_clip = AudioFileClip(str(voiceover_path))
                audio_duration = vo_clip.duration + 1.0  # slight breathing room
            except Exception as e:
                logger.warning(f"Failed to load voiceover audio: {e}")

        # Limit to max duration
        final_duration = min(audio_duration, config.MAX_DURATION_SECONDS)

        # 2. Adjust video duration (loop if video is shorter than voiceover)
        if video_clip.duration < final_duration:
            num_loops = int(final_duration // video_clip.duration) + 1
            video_clip = _loop_video(video_clip, num_loops)

        video_clip = _subclip(video_clip, 0, final_duration)

        # 3. Ensure 9:16 vertical resolution (1080x1920)
        vw, vh = video_clip.size
        aspect_ratio = vw / vh
        target_aspect = self.width / self.height

        if abs(aspect_ratio - target_aspect) > 0.05:
            # Scale and crop to fill
            scale_factor = max(self.width / vw, self.height / vh)
            video_clip = _resize(video_clip, scale_factor)
            cw, ch = video_clip.size
            x1 = (cw - self.width) // 2
            y1 = (ch - self.height) // 2
            video_clip = _crop(video_clip, x1=x1, y1=y1, width=self.width, height=self.height)
        else:
            video_clip = _resize(video_clip, (self.width, self.height))

        # 4. Audio Mixing
        audio_layers = []
        if vo_clip:
            audio_layers.append(_scale_volume(vo_clip, 1.0))

        if music_path and music_path.exists():
            try:
                bg_music = AudioFileClip(str(music_path))
                if bg_music.duration < final_duration:
                    bg_music = _loop_audio(bg_music, final_duration)
                else:
                    bg_music = _subclip(bg_music, 0, final_duration)
                # Duck background music to 15% volume
                audio_layers.append(_scale_volume(bg_music, 0.15))
            except Exception as e:
                logger.warning(f"Could not mix background music: {e}")

        if audio_layers:
            final_audio = _subclip(CompositeAudioClip(audio_layers), 0, final_duration)
            video_clip = _set_audio(video_clip, final_audio)

        # 5. Render Final MP4
        logger.info(f"[COMPOSER] Rendering final 9:16 Short to {dest_path}...")
        video_clip.write_videofile(
            str(dest_path),
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            threads=4,
            logger=None
        )

        # Close handles
        video_clip.close()
        if vo_clip:
            vo_clip.close()

        logger.info(f"[OK] Successfully rendered final Short: {dest_path}")
        return dest_path
