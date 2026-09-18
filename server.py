#!/usr/bin/env python3
"""Production FastAPI Web Server & 24/7 Cloud Scheduler for Render.

Provides:
- 24/7 automated hourly Short creation (24 videos/day)
- REST API (/health, /status, /trigger, /videos)
- Modern dark-mode dashboard for on-demand generation and live monitoring
- Direct YouTube credentials hydration from environment variables
"""

import os
import sys
import time
import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import schedule

from src import config
from src.pipeline import ShortsPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("server")

# Hydrate credentials from environment if provided
def hydrate_credentials_from_env():
    """Write credentials from environment variables if set in cloud (Render/Docker)."""
    secret_env = os.getenv("YOUTUBE_CLIENT_SECRET_JSON")
    secret_path = config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE
    if secret_env and (not secret_path.exists() or len(secret_path.read_text(encoding="utf-8").strip()) == 0):
        logger.info("[AUTH] Hydrating client_secret.json from YOUTUBE_CLIENT_SECRET_JSON...")
        secret_path.write_text(secret_env, encoding="utf-8")

    token_env = os.getenv("YOUTUBE_TOKEN_JSON")
    token_path = config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE
    if token_env and (not token_path.exists() or len(token_path.read_text(encoding="utf-8").strip()) == 0):
        logger.info("[AUTH] Hydrating token.json from YOUTUBE_TOKEN_JSON...")
        token_path.write_text(token_env, encoding="utf-8")

hydrate_credentials_from_env()

# State Tracking
class ServerState:
    def __init__(self):
        self.start_time: float = time.time()
        self.is_busy: bool = False
        self.current_task: Optional[str] = None
        self.total_runs: int = 0
        self.successful_runs: int = 0
        self.failed_runs: int = 0
        self.last_run_time: Optional[str] = None
        self.last_run_result: Optional[Dict[str, Any]] = None
        self.history: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.stop_scheduler_event = threading.Event()
        self.scheduler_thread: Optional[threading.Thread] = None

state = ServerState()

def run_pipeline_task(
    category: Optional[str] = None,
    upload: bool = True,
    privacy_status: Optional[str] = None,
    dry_run: Optional[bool] = None
) -> Dict[str, Any]:
    """Execute pipeline safely with thread lock."""
    if not state.lock.acquire(blocking=False):
        logger.warning("[RUNNER] Job skipped: another pipeline generation is already in progress.")
        return {"status": "busy", "message": "Pipeline is currently busy generating another video."}

    run_start = time.time()
    state.is_busy = True
    state.current_task = f"Generating Short ({category or 'Random Auto-Rotate'})"
    state.total_runs += 1

    try:
        pipeline = ShortsPipeline(dry_run=dry_run)
        result = pipeline.run_single(
            category=category,
            upload=upload,
            privacy_status=privacy_status,
            engine="free"
        )
        duration = round(time.time() - run_start, 2)
        state.successful_runs += 1
        state.last_run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        job_summary = {
            "id": state.total_runs,
            "timestamp": state.last_run_time,
            "category": result.get("concept", {}).get("category", "Auto"),
            "title": result.get("concept", {}).get("concept_title", "Short"),
            "youtube_title": result.get("concept", {}).get("youtube_title", ""),
            "youtube_url": result.get("upload", {}).get("url") if result.get("upload") else None,
            "video_file": Path(result.get("final_video", "")).name,
            "status": "success",
            "duration_seconds": duration
        }
        state.last_run_result = job_summary
        state.history.insert(0, job_summary)
        if len(state.history) > 50:
            state.history.pop()

        return job_summary

    except Exception as e:
        duration = round(time.time() - run_start, 2)
        state.failed_runs += 1
        state.last_run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        err_msg = str(e)
        logger.error(f"[RUNNER] Pipeline error: {err_msg}", exc_info=True)
        job_summary = {
            "id": state.total_runs,
            "timestamp": state.last_run_time,
            "category": category or "Auto",
            "title": "Failed Generation",
            "status": "failed",
            "error": err_msg,
            "duration_seconds": duration
        }
        state.last_run_result = job_summary
        state.history.insert(0, job_summary)
        return job_summary

    finally:
        state.is_busy = False
        state.current_task = None
        state.lock.release()

def scheduler_worker():
    """Background worker that triggers generation every hour (24 times/day)."""
    logger.info("[SCHEDULER] Background hourly scheduler thread started.")
    
    # Schedule every 1 hour
    schedule.every(1).hours.do(lambda: run_pipeline_task(upload=True))

    # Optional initial run on startup
    run_on_start = os.getenv("RUN_ON_STARTUP", "false").lower() in ("true", "1", "yes")
    if run_on_start:
        logger.info("[SCHEDULER] RUN_ON_STARTUP is true. Executing initial Short generation...")
        time.sleep(3)
        run_pipeline_task(upload=True)

    while not state.stop_scheduler_event.is_set():
        schedule.run_pending()
        time.sleep(10)
    
    logger.info("[SCHEDULER] Background scheduler stopped.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for FastAPI application."""
    hydrate_credentials_from_env()
    
    enable_scheduler = os.getenv("ENABLE_SCHEDULER", "true").lower() in ("true", "1", "yes")
    if enable_scheduler:
        logger.info("[STARTUP] Starting 24/7 Hourly Scheduler (24 videos/day)...")
        state.scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        state.scheduler_thread.start()
    else:
        logger.info("[STARTUP] Scheduler disabled (ENABLE_SCHEDULER=false).")

    yield

    # Shutdown
    state.stop_scheduler_event.set()
    schedule.clear()
    logger.info("[SHUTDOWN] Server stopping...")

app = FastAPI(
    title="Gemini Shorts Automator API",
    version="2.0.0",
    description="Automated 24/7 YouTube Shorts Creation and Cloud Deployment Service",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class TriggerRequest(BaseModel):
    category: Optional[str] = None
    upload: bool = True
    privacy: Optional[str] = None
    dry_run: Optional[bool] = None

# API Endpoints
@app.get("/health")
def health_check():
    """Healthcheck endpoint for Render and external monitoring pings."""
    uptime = round(time.time() - state.start_time, 1)
    secret_exists = (config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE).exists()
    token_exists = (config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE).exists()
    
    return {
        "status": "healthy",
        "service": "gemini-shorts-automator",
        "uptime_seconds": uptime,
        "is_busy": state.is_busy,
        "scheduler_enabled": state.scheduler_thread is not None and state.scheduler_thread.is_alive(),
        "total_runs": state.total_runs,
        "successful_runs": state.successful_runs,
        "auth_ready": secret_exists and token_exists
    }

@app.get("/status")
def get_status():
    """Detailed JSON status including scheduler jobs and recent history."""
    uptime = round(time.time() - state.start_time, 1)
    secret_exists = (config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE).exists()
    token_exists = (config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE).exists()

    next_run = None
    jobs = schedule.get_jobs()
    if jobs:
        next_run = str(jobs[0].next_run)

    return {
        "uptime_seconds": uptime,
        "is_busy": state.is_busy,
        "current_task": state.current_task,
        "total_runs": state.total_runs,
        "successful_runs": state.successful_runs,
        "failed_runs": state.failed_runs,
        "last_run_time": state.last_run_time,
        "last_run_result": state.last_run_result,
        "next_scheduled_run": next_run,
        "auth": {
            "client_secret_present": secret_exists,
            "token_present": token_exists
        },
        "config": {
            "daily_target": config.DAILY_TARGET_SHORTS,
            "scenes_per_video": config.NUM_SCENES,
            "video_engine": config.VIDEO_ENGINE,
            "tts_voice": config.EDGE_TTS_VOICE,
            "privacy": config.YOUTUBE_PRIVACY_STATUS
        },
        "recent_history": state.history[:10]
    }

@app.post("/trigger")
def trigger_generation(req: TriggerRequest, background_tasks: BackgroundTasks):
    """Manually trigger a video generation & upload in the background."""
    if state.is_busy:
        raise HTTPException(status_code=409, detail="Pipeline is currently generating another video. Please wait.")

    background_tasks.add_task(
        run_pipeline_task,
        category=req.category,
        upload=req.upload,
        privacy_status=req.privacy,
        dry_run=req.dry_run
    )

    return {
        "status": "accepted",
        "message": "Video creation pipeline triggered in background.",
        "category": req.category or "Auto-Rotate",
        "upload": req.upload
    }

@app.get("/videos")
def list_videos():
    """List all generated videos currently stored on disk."""
    videos = []
    if config.FINAL_VIDEO_DIR.exists():
        for p in sorted(config.FINAL_VIDEO_DIR.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True):
            stat = p.stat()
            videos.append({
                "filename": p.name,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "preview_url": f"/preview/{p.name}"
            })
    return {"videos": videos, "total": len(videos)}

@app.get("/preview/{filename}")
def preview_video(filename: str):
    """Stream or preview a generated MP4 Short video."""
    video_path = config.FINAL_VIDEO_DIR / filename
    if not video_path.exists() or not video_path.is_file():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(path=str(video_path), media_type="video/mp4", filename=filename)

# Dashboard UI
@app.get("/", response_class=HTMLResponse)
def dashboard():
    """Interactive dark-mode Web Dashboard."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YouTube Shorts Automator Cloud Node</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(18, 24, 38, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-cyan: #06b6d4;
      --accent-purple: #8b5cf6;
      --accent-red: #ef4444;
      --accent-green: #10b981;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --glow: rgba(6, 182, 212, 0.15);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      background-color: var(--bg);
      background-image: 
        radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.12) 0px, transparent 50%);
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .container {
      width: 100%;
      max-width: 1150px;
    }

    /* Header */
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 0 32px 0;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 32px;
      flex-wrap: wrap;
      gap: 16px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-icon {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: linear-gradient(135deg, #ef4444, #8b5cf6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
    }

    h1 {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }

    .subtitle {
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 400;
      margin-top: 2px;
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.12);
      color: var(--accent-green);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .status-badge.busy {
      background: rgba(245, 158, 11, 0.12);
      color: #f59e0b;
      border-color: rgba(245, 158, 11, 0.3);
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
      box-shadow: 0 0 10px currentColor;
    }

    /* Metrics Grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 22px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      position: relative;
      overflow: hidden;
    }

    .card-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
    }

    .card-value {
      font-size: 32px;
      font-weight: 700;
      letter-spacing: -1px;
    }

    .card-subtext {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 6px;
    }

    /* Actions Panel */
    .action-panel {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 26px;
      margin-bottom: 32px;
    }

    .panel-header {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .controls-row {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      align-items: flex-end;
    }

    .form-group {
      flex: 1;
      min-width: 200px;
    }

    label {
      display: block;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }

    select, input {
      width: 100%;
      background: rgba(10, 15, 26, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      color: var(--text-main);
      font-family: inherit;
      font-size: 14px;
      outline: none;
      transition: all 0.2s;
    }

    select:focus, input:focus {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 12px var(--glow);
    }

    .btn {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #fff;
      font-family: inherit;
      font-weight: 600;
      font-size: 14px;
      border: none;
      border-radius: 10px;
      padding: 13px 26px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }

    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
    }

    .btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* History & Videos Table */
    .table-container {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 24px;
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 14px;
    }

    th {
      color: var(--text-muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 12px 16px;
      border-bottom: 1px solid var(--card-border);
    }

    td {
      padding: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    tr:last-child td {
      border-bottom: none;
    }

    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
    }

    .badge-success { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .badge-yt { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
    .badge-dark { background: rgba(255, 255, 255, 0.08); color: #cbd5e1; }

    .link-yt {
      color: #f87171;
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .link-yt:hover { text-decoration: underline; }

    /* Live Toast */
    #toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #1e293b;
      border: 1px solid var(--accent-cyan);
      color: var(--text-main);
      padding: 14px 22px;
      border-radius: 12px;
      font-size: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      display: none;
      z-index: 1000;
    }

    /* Video Modal */
    #videoModal {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.85);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2000;
    }
    .modal-content {
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 20px;
      max-width: 420px;
      width: 90%;
      text-align: center;
      position: relative;
    }
    video {
      width: 100%;
      max-height: 65vh;
      border-radius: 12px;
      outline: none;
    }
    .close-btn {
      position: absolute;
      top: 12px; right: 16px;
      font-size: 24px;
      cursor: pointer;
      color: var(--text-muted);
    }
    .close-btn:hover { color: #fff; }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="brand">
        <div class="brand-icon">⚡</div>
        <div>
          <h1>Shorts Automator Cloud Node</h1>
          <div class="subtitle">Autonomous 24/7 Multi-Scene Storytelling & YouTube Publishing</div>
        </div>
      </div>
      <div id="statusBadge" class="status-badge">
        <div class="status-dot"></div>
        <span id="statusText">System Ready</span>
      </div>
    </header>

    <!-- Metrics Row -->
    <div class="grid">
      <div class="card">
        <div class="card-title">Cloud Schedule</div>
        <div class="card-value" id="scheduleRate">24 / Day</div>
        <div class="card-subtext" id="nextRun">Next run in: ~60 mins</div>
      </div>
      <div class="card">
        <div class="card-title">YouTube Auth Status</div>
        <div class="card-value" id="authStatus" style="font-size: 24px; color: #10b981;">Connected</div>
        <div class="card-subtext">OAuth Token Active</div>
      </div>
      <div class="card">
        <div class="card-title">Total Created</div>
        <div class="card-value" id="totalRuns">0</div>
        <div class="card-subtext" id="successfulUploads">0 Successful Uploads</div>
      </div>
      <div class="card">
        <div class="card-title">Node Uptime</div>
        <div class="card-value" id="nodeUptime">0h 0m</div>
        <div class="card-subtext">Render Container Online</div>
      </div>
    </div>

    <!-- On-Demand Generation Panel -->
    <div class="action-panel">
      <div class="panel-header">
        <span>🎬</span> Trigger Instant Short Generation
      </div>
      <form id="triggerForm" onsubmit="triggerRun(event)">
        <div class="controls-row">
          <div class="form-group" style="flex: 2;">
            <label>Niche / Concept Category</label>
            <select id="categorySelect">
              <option value="">Auto-Rotate Bank (5,000 Unique Concepts)</option>
              <option value="paladin">Holy Warriors & Crusaders</option>
              <option value="cyberpunk">Cyber Samurai & Neo-Tokyo</option>
              <option value="dragons">Elder Dragons & Wyrms</option>
              <option value="dark fantasy">Eldritch & Dark Fantasy</option>
              <option value="cosmic sci-fi">Interstellar Fleet & Sci-Fi</option>
              <option value="valkyrie">Norse Valkyries & Asgard</option>
            </select>
          </div>
          <div class="form-group">
            <label>YouTube Privacy</label>
            <select id="privacySelect">
              <option value="public">Public</option>
              <option value="unlisted">Unlisted</option>
              <option value="private">Private</option>
            </select>
          </div>
          <div class="form-group" style="flex: 0 0 auto;">
            <button type="submit" id="triggerBtn" class="btn">
              <span>🚀 Generate & Upload Now</span>
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Video History Table -->
    <div class="table-container">
      <div class="panel-header" style="margin-bottom: 16px;">
        <span>📹</span> Published YouTube Shorts & Generated Library
      </div>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Category</th>
            <th>Concept / Title</th>
            <th>YouTube Status</th>
            <th>Local Video</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody id="videosBody">
          <tr>
            <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">
              Loading video records...
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div id="toast"></div>

  <!-- Video Preview Modal -->
  <div id="videoModal" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <span class="close-btn" onclick="closeModal()">&times;</span>
      <h3 id="modalTitle" style="font-size: 16px; margin-bottom: 12px;">Video Preview</h3>
      <video id="modalVideo" controls autoplay playsinline></video>
    </div>
  </div>

  <script>
    function showToast(msg) {
      const toast = document.getElementById("toast");
      toast.innerText = msg;
      toast.style.display = "block";
      setTimeout(() => { toast.style.display = "none"; }, 4000);
    }

    function openModal(title, url) {
      document.getElementById("modalTitle").innerText = title;
      const v = document.getElementById("modalVideo");
      v.src = url;
      document.getElementById("videoModal").style.display = "flex";
      v.play();
    }

    function closeModal() {
      const v = document.getElementById("modalVideo");
      v.pause();
      v.src = "";
      document.getElementById("videoModal").style.display = "none";
    }

    async function fetchStatus() {
      try {
        const res = await fetch("/status");
        if (!res.ok) return;
        const data = await res.json();

        // Uptime
        const hrs = Math.floor(data.uptime_seconds / 3600);
        const mins = Math.floor((data.uptime_seconds % 3600) / 60);
        document.getElementById("nodeUptime").innerText = `${hrs}h ${mins}m`;

        // Runs
        document.getElementById("totalRuns").innerText = data.total_runs;
        document.getElementById("successfulUploads").innerText = `${data.successful_runs} Successful Runs`;

        // Auth
        const authEl = document.getElementById("authStatus");
        if (data.auth.token_present) {
          authEl.innerText = "Connected";
          authEl.style.color = "#10b981";
        } else {
          authEl.innerText = "Pending Auth";
          authEl.style.color = "#ef4444";
        }

        // Busy status
        const badge = document.getElementById("statusBadge");
        const statusText = document.getElementById("statusText");
        const triggerBtn = document.getElementById("triggerBtn");

        if (data.is_busy) {
          badge.className = "status-badge busy";
          statusText.innerText = data.current_task || "Generating Short...";
          triggerBtn.disabled = true;
          triggerBtn.innerHTML = "<span>⏳ Rendering Short...</span>";
        } else {
          badge.className = "status-badge";
          statusText.innerText = "24/7 Scheduler Active";
          triggerBtn.disabled = false;
          triggerBtn.innerHTML = "<span>🚀 Generate & Upload Now</span>";
        }

        // Next Run
        if (data.next_scheduled_run) {
          document.getElementById("nextRun").innerText = "Next: " + data.next_scheduled_run.split(".")[0];
        }

        // Table
        renderTable(data.recent_history);
      } catch (err) {
        console.error("Status check failed", err);
      }
    }

    function renderTable(history) {
      const tbody = document.getElementById("videosBody");
      if (!history || history.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">No Shorts created in this session yet. Click 'Generate & Upload Now' or wait for the hourly schedule!</td></tr>`;
        return;
      }

      tbody.innerHTML = history.map(item => {
        const ytCell = item.youtube_url 
          ? `<a class="link-yt" href="${item.youtube_url}" target="_blank"><span>▶</span> View on YouTube</a>` 
          : `<span class="badge badge-dark">${item.status === 'success' ? 'Local Video' : 'Failed'}</span>`;
        
        const previewBtn = item.video_file
          ? `<button class="btn" style="padding: 6px 12px; font-size: 12px;" onclick="openModal('${item.title}', '/preview/${item.video_file}')">Watch 🎬</button>`
          : '-';

        return `
          <tr>
            <td style="color: var(--text-muted); font-size: 12px;">${item.timestamp || '-'}</td>
            <td><span class="badge badge-dark">${item.category || 'Auto'}</span></td>
            <td style="font-weight: 600;">${item.title}</td>
            <td>${ytCell}</td>
            <td>${previewBtn}</td>
            <td style="color: var(--text-muted);">${item.duration_seconds}s</td>
          </tr>
        `;
      }).join('');
    }

    async function triggerRun(e) {
      e.preventDefault();
      const cat = document.getElementById("categorySelect").value;
      const priv = document.getElementById("privacySelect").value;

      try {
        const res = await fetch("/trigger", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category: cat || null, privacy: priv, upload: true })
        });
        const data = await res.json();
        if (res.ok) {
          showToast("⚡ Generation started! Creating 5 cinematic scenes...");
          fetchStatus();
        } else {
          showToast("❌ " + (data.detail || "Error triggering run"));
        }
      } catch (err) {
        showToast("❌ Connection error");
      }
    }

    // Polling loop
    fetchStatus();
    setInterval(fetchStatus, 6000);
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

def main():
    """Run uvicorn server directly."""
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting Gemini Shorts Automator server on {host}:{port}...")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
