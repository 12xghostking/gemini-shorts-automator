#!/usr/bin/env python3
"""CLI interface for Gemini Faceless YouTube Shorts Automator."""

import sys
import logging
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Configure Windows UTF-8 stdout if needed
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

console = Console(force_terminal=True, highlight=False)

@click.group()
def cli():
    """Gemini Faceless YouTube Shorts Automator CLI"""
    pass

@cli.command()
def check_env():
    """Verify system setup, API keys, and credential status."""
    from src import config
    table = Table(title="Configuration Status")
    table.add_column("Setting / Credential", style="cyan")
    table.add_column("Value / Status", style="green")

    table.add_row("GEMINI_API_KEY", "[OK] Configured" if config.GEMINI_API_KEY else "[MISSING] (Set in .env)")
    table.add_row("GEMINI_TEXT_MODEL", config.GEMINI_TEXT_MODEL)
    table.add_row("GEMINI_VIDEO_MODEL", config.GEMINI_VIDEO_MODEL)
    
    secret_exists = (config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE).exists()
    table.add_row("YouTube client_secret.json", "[OK] Found" if secret_exists else "[WARNING] Not Found (Required for live upload)")

    token_exists = (config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE).exists()
    table.add_row("YouTube token.json", "[OK] Authenticated" if token_exists else "[PENDING] First-Time Login")

    table.add_row("TTS Engine", config.TTS_ENGINE)
    table.add_row("Edge-TTS Voice", config.EDGE_TTS_VOICE)
    table.add_row("Dry Run Mode", str(config.DRY_RUN))
    table.add_row("Daily Target Uploads", str(config.DAILY_TARGET_SHORTS))

    console.print(table)

@cli.command()
@click.option("--category", "-c", default=None, help="Specific niche (e.g. 'dragons', 'samurai')")
def prompt(category):
    """Generate a viral topic, Veo video prompt, and hook script preview."""
    from src.topic_engine import TopicEngine
    engine = TopicEngine()
    concept = engine.generate_concept(category)

    console.print(Panel.fit(
        f"[bold cyan]Category:[/bold cyan] {concept.category}\n"
        f"[bold cyan]Title:[/bold cyan] {concept.concept_title}\n\n"
        f"[bold yellow]YouTube Title:[/bold yellow] {concept.youtube_title}\n\n"
        f"[bold green]Voiceover Script:[/bold green] \"{concept.voiceover_script}\"\n\n"
        f"[bold magenta]Veo Video Prompt:[/bold magenta]\n{concept.video_prompt}\n\n"
        f"[bold blue]Tags:[/bold blue] {', '.join(concept.tags)}",
        title="Generated Short Concept"
    ))

@cli.command()
@click.option("--category", "-c", default=None, help="Theme category")
@click.option("--dry-run/--live", default=None, help="Run without burning Veo / YouTube API credits")
@click.option("--upload/--no-upload", default=True, help="Whether to upload to YouTube")
def run_once(category, dry_run, upload):
    """Run full pipeline once (generate concept, video, voiceover, mix, and upload)."""
    from src.pipeline import ShortsPipeline
    pipeline = ShortsPipeline(dry_run=dry_run)
    result = pipeline.run_single(category=category, upload=upload)
    console.print("[bold green]Pipeline execution completed successfully![/bold green]")

@cli.command()
@click.option("--file", "-f", default=None, help="Path to video file to upload (defaults to latest final Short)")
@click.option("--title", "-t", default="Cyber Samurai Showdown in Neon Rain ⚔️ #Shorts #Cyberpunk", help="Video title")
@click.option("--description", "-d", default="A lethal cyber samurai duel in neo-Tokyo under pouring neon rain. Created with Google Veo and Gemini. #Shorts #Cyberpunk #Veo", help="Description")
@click.option("--privacy", "-p", default=None, type=click.Choice(["public", "unlisted", "private"]), help="Upload privacy status (defaults to .env setting)")
def upload(file, title, description, privacy):
    """Upload a specific video file directly to YouTube using YouTube Data API v3."""
    from src.youtube_engine import YouTubeEngine
    from src import config
    from pathlib import Path

    privacy = privacy or config.YOUTUBE_PRIVACY_STATUS

    if not file:
        candidates = sorted(config.FINAL_VIDEO_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            console.print("[bold red]No video files found in output/final/ to upload![/bold red]")
            return
        target_file = candidates[0]
    else:
        target_file = Path(file)

    if not target_file.exists():
        console.print(f"[bold red]File not found: {target_file}[/bold red]")
        return

    console.print(f"[bold cyan]Selected video for upload:[/bold cyan] {target_file.name}")
    engine = YouTubeEngine()
    result = engine.upload_short(
        video_path=target_file,
        title=title,
        description=description,
        tags=["Shorts", "Cyberpunk", "Samurai", "Veo", "AIArt", "Cinematic"],
        privacy_status=privacy,
        dry_run=False
    )
    console.print(f"[bold green]Upload Result: {result}[/bold green]")

@cli.command()
def schedule():
    """Start continuous 2-3x daily background scheduler."""
    from src.pipeline import ShortsPipeline
    pipeline = ShortsPipeline()
    console.print("[bold cyan]Starting YouTube Shorts Daily Scheduler...[/bold cyan]")
    pipeline.start_scheduler()

if __name__ == "__main__":
    cli()
