# 🎬 Autonomous Faceless YouTube Shorts Automator

An autonomous AI pipeline that generates, composes, and publishes viral vertical 9:16 Shorts (e.g. samurai duels, cyberpunk warriors, celestial titans, dark fantasy legends) directly to YouTube 2–3 times a day.

Generates **5–6 distinct AI scenes** per Short with dynamic camera panning, zoom choreography, atmospheric particle effects, and high-fidelity neural voiceover — **100% free with zero API costs**.

---

## 🌟 Key Features

- **5,000+ Concept Engine**: Pre-generated bank of 5,000+ unique, high-retention Short concepts across 250+ distinct archetypes. Zero downtime, zero 503 errors, and instant execution.
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
GEMINI_API_KEY=your_actual_gemini_api_key_here  # Optional: only if generating fresh concepts online
GEMINI_TEXT_MODEL=gemini-2.5-flash
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

## ⏰ Automating 2–3 Daily Uploads

### Option A: GitHub Actions (Recommended — 100% Cloud, No PC Needed!)
A pre-configured GitHub Actions workflow is included at `.github/workflows/daily_shorts.yml`. It runs in the cloud on a 3x daily schedule (approx 8:30 AM, 2:30 PM, and 7:30 PM IST) and uploads the generated videos as downloadable artifacts!

#### Setting Up GitHub Secrets:
1. Push this repository to your GitHub account.
2. In your GitHub repository, navigate to **Settings > Secrets and variables > Actions**.
3. Under **Repository secrets**, click **New repository secret** and add:
   - `GEMINI_API_KEY`: Your Google AI Studio API key.
   - `YOUTUBE_CLIENT_SECRET_JSON`: The entire raw contents of your `client_secret.json` file.
   - `YOUTUBE_TOKEN_JSON`: The entire raw contents of your `token.json` file (generated after your one-time local authentication via `python cli.py run-once --live`).
   - `ELEVENLABS_API_KEY` *(Optional)*: If using ElevenLabs instead of free Edge-TTS.
4. **Test in GitHub**:
   - Go to the **Actions** tab in your repository.
   - Select **Daily YouTube Shorts Generator & Uploader**.
   - Click **Run workflow** (you can toggle dry-run or pick a custom niche like `dragons` or `samurai`).

---

### Option B: Built-in Python Scheduler (Local Machine)
Run the continuous background runner:
```bash
python cli.py schedule
```
By default, this posts at:
- **09:00 AM**
- **02:30 PM**
- **07:30 PM**

---

### Option C: Windows Task Scheduler (For Always-On PC)
1. Open Windows **Task Scheduler** (`taskschd.msc`).
2. Click **Create Basic Task** -> Name: `YT-Shorts-Morning`.
3. Trigger: **Daily at 9:00 AM**.
4. Action: **Start a program**:
   - Program: `python.exe`
   - Arguments: `cli.py run-once --live`
   - Start in: `c:\Users\sirki\projects\gemini-shorts-automator`
5. Repeat for afternoon and evening slots!
