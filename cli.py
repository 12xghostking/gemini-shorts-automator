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
    table.add_row("Video Engine", "Free 5-Shot Storytelling Montage (0 API Credits)")
    table.add_row("Scenes Per Short", str(config.NUM_SCENES))
    
    secret_exists = (config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE).exists()
    table.add_row("YouTube client_secret.json", "[OK] Found" if secret_exists else "[WARNING] Not Found (Required for live upload)")

    token_exists = (config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE).exists()
    token_status = "[PENDING] First-Time Login (run 'python cli.py auth')"
    if token_exists:
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from src.youtube_engine import SCOPES
            creds = Credentials.from_authorized_user_file(str(config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE), SCOPES)
            if creds.valid:
                token_status = "[OK] Authenticated (Valid)"
            elif creds.refresh_token:
                try:
                    creds.refresh(Request())
                    token_status = "[OK] Authenticated (Refreshed)"
                except Exception:
                    token_status = "[EXPIRED / REVOKED] Run 'python cli.py auth'"
            else:
                token_status = "[EXPIRED] Needs fresh login (run 'python cli.py auth')"
        except Exception:
            token_status = "[INVALID] Corrupt token (run 'python cli.py auth')"
    table.add_row("YouTube token.json", token_status)

    table.add_row("TTS Engine", config.TTS_ENGINE)
    table.add_row("Edge-TTS Voice", config.EDGE_TTS_VOICE)
    table.add_row("Dry Run Mode", str(config.DRY_RUN))
    table.add_row("Daily Target Uploads", str(config.DAILY_TARGET_SHORTS))

    console.print(table)

@cli.command()
@click.option("--category", "-c", default=None, help="Specific niche (e.g. 'dragons', 'samurai')")
def prompt(category):
    """Generate a viral topic, visual prompt, and hook script preview."""
    from src.topic_engine import TopicEngine
    engine = TopicEngine()
    concept = engine.generate_concept(category)

    console.print(Panel.fit(
        f"[bold cyan]Category:[/bold cyan] {concept.category}\n"
        f"[bold cyan]Title:[/bold cyan] {concept.concept_title}\n\n"
        f"[bold yellow]YouTube Title:[/bold yellow] {concept.youtube_title}\n\n"
        f"[bold green]Voiceover Script:[/bold green] \"{concept.voiceover_script}\"\n\n"
        f"[bold magenta]Visual Story Prompt:[/bold magenta]\n{concept.video_prompt}\n\n"
        f"[bold blue]Tags:[/bold blue] {', '.join(concept.tags)}",
        title="Generated Short Concept"
    ))

@cli.command()
@click.option("--category", "-c", default=None, help="Theme category")
@click.option("--dry-run/--live", default=None, help="Run without uploading to YouTube")
@click.option("--upload/--no-upload", default=True, help="Whether to upload to YouTube")
@click.option("--privacy", "-p", default=None, type=click.Choice(["public", "unlisted", "private"]), help="Upload privacy status (defaults to public)")
@click.option("--engine", "-e", default="free", help="Video engine (defaults to free)")
def run_once(category, dry_run, upload, privacy, engine):
    """Run full pipeline once (generate concept, 5-6 distinct images, voiceover, mix, and upload)."""
    from src.pipeline import ShortsPipeline
    pipeline = ShortsPipeline(dry_run=dry_run)
    result = pipeline.run_single(category=category, upload=upload, privacy_status=privacy, engine=engine)
    console.print("[bold green]Pipeline execution completed successfully![/bold green]")

@cli.command()
@click.option("--force", is_flag=True, default=True, help="Force fresh OAuth authorization flow.")
def auth(force):
    """Authenticate with YouTube Data API v3 and generate/refresh token.json."""
    from src.youtube_engine import YouTubeEngine
    from src import config
    import json

    console.print(Panel.fit(
        "[bold cyan]YouTube OAuth Authentication[/bold cyan]\n\n"
        "A browser window will open for you to sign in with your Google Account\n"
        "and grant upload permissions for your YouTube channel.",
        title="YouTube Auth"
    ))

    secret_path = config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE
    if not secret_path.exists():
        console.print(f"[bold red]Error:[/bold red] '{secret_path.name}' not found in project root!")
        console.print("Please place your OAuth client secret JSON from Google Cloud Console as client_secret.json.")
        return

    engine = YouTubeEngine()
    try:
        success = engine.authenticate(force_reauth=force)
        if success and engine.token_path.exists():
            console.print("\n[bold green]✓ Successfully authenticated and created token.json![/bold green]\n")

            with open(engine.token_path, "r", encoding="utf-8") as f:
                token_data = json.load(f)
            minified_token = json.dumps(token_data)

            console.print(Panel(
                f"[bold yellow]1. Local Authentication:[/bold yellow] [green]Saved to token.json[/green]\n\n"
                f"[bold yellow]2. For GitHub Actions / CI Secret:[/bold yellow]\n"
                f"Copy the string below and update your GitHub repository secret named [bold cyan]YOUTUBE_TOKEN_JSON[/bold cyan]:\n\n"
                f"{minified_token}\n\n"
                f"[bold magenta]⚡ How to Prevent 7-Day Token Expiration:[/bold magenta]\n"
                f"If your Google Cloud OAuth consent screen is in '[bold red]Testing[/bold red]' status, tokens expire every 7 days.\n"
                f"To make tokens permanent:\n"
                f"1. Go to Google Cloud Console -> [bold cyan]APIs & Services > OAuth consent screen[/bold cyan]\n"
                f"2. Under Publishing status, click '[bold green]Publish App[/bold green]' (switch to In Production).\n"
                f"3. Your refresh token will now never expire automatically!",
                title="Authentication Complete"
            ))
    except Exception as e:
        console.print(f"[bold red]Authentication failed:[/bold red] {e}")

@cli.command()
@click.option("--file", "-f", default=None, help="Path to video file to upload (defaults to latest final Short)")
@click.option("--title", "-t", default="Cyber Samurai Showdown in Neon Rain ⚔️ #Shorts #Cyberpunk", help="Video title")
@click.option("--description", "-d", default="A lethal cyber samurai duel in neo-Tokyo under pouring neon rain. Created with Free AI Storytelling Generator. #Shorts #Cyberpunk #AIArt", help="Description")
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
        tags=["Shorts", "Cyberpunk", "Samurai", "AIArt", "Cinematic", "Storytelling"],
        privacy_status=privacy,
        dry_run=False
    )
    console.print(f"[bold green]Upload Result: {result}[/bold green]")

@cli.command()
def schedule():
    """Start continuous 24/7 background scheduler (CLI mode)."""
    from src.pipeline import ShortsPipeline
    pipeline = ShortsPipeline()
    console.print("[bold cyan]Starting YouTube Shorts Daily Scheduler...[/bold cyan]")
    pipeline.start_scheduler()

@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind server")
@click.option("--port", default=8080, type=int, help="Port to run server on")
def serve(host, port):
    """Start the 24/7 Web Server & API dashboard (Render / Local production server)."""
    import uvicorn
    from server import app
    console.print(f"[bold green]Starting Web Server on http://{host}:{port}[/bold green]")
    console.print("[bold cyan]Includes 24/7 hourly background scheduler, /health, /status, and live dashboard.[/bold cyan]")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    cli()

