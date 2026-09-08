# 🎬 Gemini Faceless YouTube Shorts Automator

An autonomous AI pipeline that uses **Google Gemini & Veo** to generate, compose, and publish viral vertical 9:16 Shorts (e.g. flying dragons, samurai duels, surreal fantasy, sci-fi titans) directly to YouTube 2–3 times a day.

---

## 🌟 Key Features

- **Dynamic Concept & Script Engine**: Uses Gemini 2.5/1.5 Flash to rotate viral niches, generate hook scripts, and craft optimized Veo video prompts.
- **Google Veo Video Generation**: Direct 9:16 vertical video synthesis via `google-genai` SDK.
- **Free Neural Voiceover**: High-fidelity narration generated through Microsoft Edge Neural TTS with zero subscription fees (or optional ElevenLabs).
- **Automated Video Composer**: Scales, loops, and mixes clips with ducked background music into YouTube Shorts-compliant 1080x1920 MP4s using MoviePy and FFmpeg.
- **Autonomous YouTube Uploading**: Automatically publishes or schedules Shorts with optimized titles, `#Shorts` tags, and descriptions using YouTube Data API v3.
- **Zero-Cost Dry-Run Mode**: Test the entire pipeline locally without spending API credits or YouTube quota.

---

## 📂 Project Structure

```
gemini-shorts-automator/
├── .env.example                # Template for environment variables and API keys
├── .env                        # Local credentials (gitignored)
├── client_secret.json          # Your YouTube OAuth credentials from Google Cloud
├── requirements.txt            # Python dependencies
├── cli.py                      # Main Command Line Interface
├── assets/
│   ├── music/                  # Add royalty-free .mp3 / .wav tracks here
│   └── fonts/                  # Custom fonts for overlays
├── output/
│   ├── raw/                    # Raw Veo video clips
│   ├── audio/                  # Synthesized voiceovers
│   └── final/                  # Ready-to-upload 1080x1920 MP4 Shorts
└── src/
    ├── config.py               # Path & environment settings
    ├── topic_engine.py         # Gemini prompt & script generator
    ├── video_engine.py         # Google Veo video generation & mock mode
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
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
GEMINI_VIDEO_MODEL=veo-2.0-generate-001
YOUTUBE_PRIVACY_STATUS=unlisted
DRY_RUN=false
```

---

## 🔑 How to Get Your Credentials

### 1. Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key** and create a key in your project.
3. Paste the key into `GEMINI_API_KEY` in `.env`.

### 2. YouTube Data API v3 (`client_secret.json`)
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
Preview the dynamic viral topics, Veo prompts, and voiceover scripts:
```bash
python cli.py prompt
# Or specify a category:
python cli.py prompt --category "samurai"
```

### 3. Run a Dry-Run Test (Zero Cost)
Generate and assemble a test Short without consuming Gemini Veo credits:
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

### Option A: Built-in Python Scheduler
Run the continuous background runner:
```bash
python cli.py schedule
```
By default, this posts at:
- **09:00 AM**
- **02:30 PM**
- **07:30 PM**

### Option B: Windows Task Scheduler (Recommended for 24/7 PC)
1. Open Windows **Task Scheduler** (`taskschd.msc`).
2. Click **Create Basic Task** -> Name: `YT-Shorts-Morning`.
3. Trigger: **Daily at 9:00 AM**.
4. Action: **Start a program**:
   - Program: `python.exe`
   - Arguments: `cli.py run-once --live`
   - Start in: `c:\Users\sirki\projects\gemini-shorts-automator`
5. Repeat for your afternoon and evening time slots!
