"""End-to-end pipeline orchestrator for creating and publishing Shorts."""

import time
import logging
from typing import Optional, Dict, Any

from src import config
from src.topic_engine import TopicEngine, ShortConcept
from src.video_engine import VideoEngine
from src.audio_engine import AudioEngine
from src.composer import VideoComposer
from src.youtube_engine import YouTubeEngine

logger = logging.getLogger(__name__)

class ShortsPipeline:
    def __init__(self, dry_run: Optional[bool] = None):
        self.dry_run = config.DRY_RUN if dry_run is None else dry_run
        self.topic_engine = TopicEngine()
        self.video_engine = VideoEngine()
        self.audio_engine = AudioEngine()
        self.composer = VideoComposer()
        self.youtube_engine = YouTubeEngine()

    def run_single(self, category: Optional[str] = None, upload: bool = True, privacy_status: Optional[str] = None) -> Dict[str, Any]:
        """Runs a complete cycle from concept to YouTube upload."""
        logger.info("=" * 60)
        logger.info(f"[START] SHORTS CREATION PIPELINE (Dry-Run: {self.dry_run})")
        logger.info("=" * 60)

        start_time = time.time()

        # Step 1: Brainstorm Topic, Prompts & Metadata
        logger.info("\n[1/5] Brainstorming viral concept with Gemini...")
        concept: ShortConcept = self.topic_engine.generate_concept(category)
        logger.info(f"   Category: {concept.category}")
        logger.info(f"   Title:    {concept.concept_title}")
        logger.info(f"   Hook:     \"{concept.voiceover_script}\"")

        # Step 2: Voiceover Generation
        logger.info("\n[2/5] Synthesizing voiceover audio...")
        audio_path = self.audio_engine.generate_voiceover(concept.voiceover_script)
        music_path = self.audio_engine.get_background_music()

        # Step 3: Video Generation (Google Veo)
        logger.info("\n[3/5] Generating vertical video clip...")
        raw_video_path = self.video_engine.generate_video(
            prompt=concept.video_prompt,
            dry_run=self.dry_run,
            aspect_ratio="9:16"
        )

        # Step 4: Video Composition & Audio Mixing
        logger.info("\n[4/5] Composing final 9:16 Short...")
        final_video_path = self.composer.compose_short(
            video_path=raw_video_path,
            voiceover_path=audio_path,
            music_path=music_path,
            title_text=concept.concept_title
        )

        # Step 5: YouTube Upload
        upload_result = None
        if upload:
            logger.info("\n[5/5] Uploading to YouTube...")
            upload_result = self.youtube_engine.upload_short(
                video_path=final_video_path,
                title=concept.youtube_title,
                description=concept.youtube_description,
                tags=concept.tags,
                privacy_status=privacy_status,
                dry_run=self.dry_run
            )
        else:
            logger.info("\n[5/5] Skipping upload (upload=False requested).")

        elapsed = round(time.time() - start_time, 2)
        logger.info("=" * 60)
        logger.info(f"[DONE] PIPELINE RUN FINISHED in {elapsed}s")
        logger.info(f"   Final Video: {final_video_path}")
        if upload_result:
            logger.info(f"   Upload Status: {upload_result.get('status')}")
            logger.info(f"   Short URL: {upload_result.get('url')}")
        logger.info("=" * 60)

        concept_data = concept.model_dump() if hasattr(concept, "model_dump") else concept.dict()
        return {
            "concept": concept_data,
            "raw_video": str(raw_video_path),
            "final_video": str(final_video_path),
            "upload": upload_result,
            "duration_seconds": elapsed
        }

    def start_scheduler(self):
        """Runs the pipeline on a recurring schedule (e.g. 2-3 times daily)."""
        import schedule

        logger.info(f"[SCHEDULER] Starting automated scheduler ({config.DAILY_TARGET_SHORTS} uploads/day)...")
        # Default distribution: Morning, Afternoon, Evening
        schedule.every().day.at("09:00").do(self.run_single)
        schedule.every().day.at("14:30").do(self.run_single)
        if config.DAILY_TARGET_SHORTS >= 3:
            schedule.every().day.at("19:30").do(self.run_single)

        logger.info("Scheduled upload times:")
        logger.info(" - 09:00 AM")
        logger.info(" - 02:30 PM")
        if config.DAILY_TARGET_SHORTS >= 3:
            logger.info(" - 07:30 PM")
        logger.info("Running scheduler loop (Press Ctrl+C to stop)...")

        while True:
            schedule.run_pending()
            time.sleep(30)
