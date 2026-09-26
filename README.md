# 🎬 Autonomous Faceless YouTube Shorts Automator

An autonomous AI pipeline that generates, composes, and publishes viral vertical 9:16 Shorts (e.g. samurai duels, cyberpunk warriors, celestial titans, dark fantasy legends) directly to YouTube 2–3 times a day.

Generates **5–6 distinct AI scenes** per Short with dynamic camera panning, zoom choreography, atmospheric particle effects, and high-fidelity neural voiceover — **100% free with zero API costs**.

---

## 🌟 Key Features

- **10,000+ Concept Engine**: Pre-generated bank of 5,000+ unique, high-retention Short concepts across 250+ distinct archetypes. Zero downtime, zero 503 errors, and instant execution.
- **Free Multi-Scene AI Video Synthesis**: Synthesizes 5–6 distinct visuals for every Short using distributed free AI generation clusters with automated retry fallbacks. Zero paid API keys or external credits.
- **Cinematic Multi-Angle Camera Choreography**: Animates each distinct scene using dynamic push-in, pan-right, tilt-up, pull-out, and hero-drift camera motions with subtle atmospheric embers.
- **Free Neural Voiceover**: High-fidelity narration generated through Microsoft Edge Neural TTS with zero subscription fees (or optional ElevenLabs).
- **Automated Video Composer**: Scales, loops, and mixes clips with ducked background music into YouTube Shorts-compliant 1080x1920 MP4s using MoviePy and FFmpeg.
- **Autonomous YouTube Uploading**: Automatically publishes or schedules Shorts with optimized titles, `#Shorts` tags, and descriptions using YouTube Data API v3.
- **Zero-Cost Dry-Run Mode**: Test the entire pipeline locally without spending any quota.

---

## 📂 Project Structure

```
gemini-shorts-automator/
├── .env.example                # Template for environment variables and API keys
├── .env                        # Local credentials (gitignored)
├── client_secret.json          # Your YouTube OAuth credentials from Google Cloud
├── requirements.txt            # Python dependencies
├── cli.py                      # Main Command Line Interface
├── build_concepts_bank.py      # Generator for 5,000+ concept bank
├── assets/
│   ├── concepts_bank.json      # 5,000+ offline concepts database
│   ├── music/                  # Add royalty-free .mp3 / .wav tracks here
│   └── fonts/                  # Custom fonts for overlays
├── output/
│   ├── images/                 # Downloaded distinct AI scene images
│   ├── raw/                    # Raw multi-scene video clips
│   ├── audio/                  # Synthesized voiceovers
│   └── final/                  # Ready-to-upload 1080x1920 MP4 Shorts
└── src/
    ├── config.py               # Path & environment settings
    ├── topic_engine.py         # 5,000+ concept selector & script generator
    ├── video_engine.py         # Free 5-scene AI visual & camera engine
    ├── audio_engine.py         # Voiceover synthesis & audio loader
    ├── composer.py             # 9:16 video assembly & audio ducking
    ├── youtube_engine.py       # YouTube OAuth & upload client
    └── pipeline.py             # Full end-to-end orchestration & scheduler
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies

In your terminal:

```bash
cd c:\Users\sirki\projects\gemini-shorts-automator
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
YOUTUBE_PRIVACY_STATUS=unlisted
DRY_RUN=false
```

---

## 🔑 How to Get Your Credentials

### 1. YouTube Data API v3 (`client_secret.json`)
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g. `YT-Shorts-Automator`).
3. Enable the **YouTube Data API v3** in **APIs & Services > Library**.
4. Go to **APIs & Services > OAuth consent screen**:
   - Choose **External**, fill in app name and your email.
   - Add your Google account as a **Test user**.
5. Go to **APIs & Services > Credentials**:
   - Click **Create Credentials > OAuth Client ID**.
   - Application type: **Desktop app**.
   - Name: `Shorts Uploader`.
6. Click **Download JSON**, rename the downloaded file to `client_secret.json`, and place it in the root folder of this project (`gemini-shorts-automator/`).

### 2. Generate YouTube Token (`token.json`)
Run the authentication helper:
```bash
python cli.py auth
```
A browser window will open for you to sign in with your Google account and authorize permissions. Once authorized, `token.json` is automatically generated.

> [!TIP]
> **How to Prevent 7-Day Token Expiration in GitHub Actions / Production:**
> If your Google Cloud OAuth Consent Screen is left in **"Testing"** status, Google will automatically expire refresh tokens every **7 days** with `invalid_grant: Token has been expired or revoked`.
> To make your token permanent:
> 1. In [Google Cloud Console](https://console.cloud.google.com/), go to **APIs & Services > OAuth consent screen**.
> 2. Under **Publishing status**, click **Publish App** (switch to **In Production**).
> 3. Run `python cli.py auth` to generate a permanent refresh token.
> 4. If using GitHub Actions, copy the printed minified JSON string and update your repository secret `YOUTUBE_TOKEN_JSON`.

---

## 🧪 Testing & Usage

### 1. Check Configuration
Verify whether all environment variables and secrets are detected:
```bash
python cli.py check-env
```

### 2. Test Concept & Prompt Generation
Preview the dynamic viral topics, visual prompts, and voiceover scripts:
```bash
python cli.py prompt
# Or specify a category:
python cli.py prompt --category "samurai"
```

### 3. Run a Dry-Run Test (Zero Cost)
Generate 5 distinct AI scenes and assemble a full test Short:
```bash
python cli.py run-once --dry-run
```
The resulting video will be saved in `output/final/` for your review!

### 4. Run Live Generation & Upload
When your keys are configured:
```bash
python cli.py run-once --live
```
*(On your first live run, a browser window will open asking you to sign into YouTube once. After that, it generates `token.json` and runs headlessly without prompts!)*

---

## ⏰ Automating 24 Daily Uploads (1 Video Per Hour)

### Option A: Deploy to Render (24/7 Cloud Web Service & Dashboard)

Run as an autonomous cloud service on [Render.com](https://render.com). This gives you:
- **Continuous 24/7 autonomous uploads** (1 video every hour = 24 uploads daily)
- **Live Dark-Mode Web Dashboard**: Trigger on-demand generation, monitor queue, inspect upload stats, and stream previews directly from your browser.
- **Health check & REST API**: Endpoints at `/health`, `/status`, `/trigger`, and `/videos`.

#### Step-by-Step Render Deployment:

1. **Push your repository to GitHub**:
   Ensure all changes including `Dockerfile`, `render.yaml`, and `server.py` are committed and pushed.

2. **Create a New Web Service on Render**:
   - Log into [dashboard.render.com](https://dashboard.render.com/).
   - Click **New +** > **Web Service**.
   - Connect your GitHub repository (`gemini-shorts-automator`).
   - Choose **Docker** as the runtime (Render will automatically detect the included `Dockerfile` with system `ffmpeg`).
   - Choose your plan (Free or Starter).

3. **Add Environment Variables in Render Dashboard**:
   Under the **Environment** tab in your Render service, add:
   | Key | Value / Instructions |
   |---|---|
   | `PORT` | `8080` (or leave default `$PORT`) |
   | `ENABLE_SCHEDULER` | `true` (Runs automated upload every hour) |
   | `YOUTUBE_PRIVACY_STATUS` | `public` (or `unlisted`) |
   | `DAILY_TARGET_SHORTS` | `24` |
   | `YOUTUBE_CLIENT_SECRET_JSON` | Open your local `client_secret.json`, copy the entire text, and paste it here |
   | `YOUTUBE_TOKEN_JSON` | Open your local `token.json`, copy the entire text, and paste it here |
   | `AI_HORDE_API_KEY` | *(Optional)* Your AI Horde API Key |

4. **Keep Render Free Tier Awake 24/7**:
   Render's free tier spins down after 15 minutes of inactivity. To keep your hourly scheduler running 24/7 for free:
   - Create a free account at [UptimeRobot.com](https://uptimerobot.com).
   - Add a new HTTP Monitor targeting: `https://your-service-name.onrender.com/health`
   - Set the monitoring interval to **every 10 minutes**.
   - *Alternative*: Upgrade to Render's **Starter** instance ($7/month) which stays running continuously without sleeping.

5. **Access Your Live Dashboard**:
   Open `https://your-service-name.onrender.com` in your browser to view your control panel!

---

### Option B: Run Local Web Server

You can also run the web server and dashboard locally on your machine:

```bash
python cli.py serve --port 8080
```
Then navigate to `http://localhost:8080` in your web browser.

---

### Option C: GitHub Actions (Cloud Cron Alternative)
A pre-configured GitHub Actions workflow is included at `.github/workflows/daily_shorts.yml`. It runs automatically in the cloud **every hour (`0 * * * *`)** to create, compose, and upload 24 Shorts a day!

#### Setting Up GitHub Secrets:
1. Push this repository to your GitHub account.
2. In your GitHub repository, navigate to **Settings > Secrets and variables > Actions**.
3. Under **Repository secrets**, click **New repository secret** and add:
   - `YOUTUBE_CLIENT_SECRET_JSON`: The entire raw contents of your `client_secret.json` file.
   - `YOUTUBE_TOKEN_JSON`: The entire raw contents of your `token.json` file.
   - `GEMINI_API_KEY` *(Optional)*: If generating online concepts.
   - `ELEVENLABS_API_KEY` *(Optional)*: If using ElevenLabs instead of free Edge-TTS.
4. **Test in GitHub**:
   - Go to the **Actions** tab in your repository.
   - Select **Hourly YouTube Shorts Generator & Uploader (24x Daily)**.
   - Click **Run workflow**.

---

### Option D: Built-in Python Scheduler (Local Machine)
Run the continuous background runner that uploads 1 video every hour:
```bash
python cli.py schedule
```

---

### Option E: Windows Task Scheduler (For Always-On PC)
1. Open Windows **Task Scheduler** (`taskschd.msc`).
2. Click **Create Basic Task** -> Name: `YT-Shorts-Hourly`.
3. Trigger: **Daily**, repeat task every **1 hour** for a duration of **indefinitely**.
4. Action: **Start a program**:
   - Program: `python.exe`
   - Arguments: `cli.py run-once --live`
   - Start in: `gemini-shorts-automator`

