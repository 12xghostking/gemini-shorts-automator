"""YouTube Data API v3 client for uploading and scheduling YouTube Shorts."""

import os
import time
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from src import config

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

class YouTubeEngine:
    def __init__(self, client_secret_path: Optional[Path] = None, token_path: Optional[Path] = None):
        self.client_secret_path = Path(client_secret_path or (config.PROJECT_ROOT / config.YOUTUBE_CLIENT_SECRET_FILE))
        self.token_path = Path(token_path or (config.PROJECT_ROOT / config.YOUTUBE_TOKEN_FILE))
        self.youtube_service = None

        # Automatically hydrate files from environment variables if present (e.g. in GitHub Actions)
        client_secret_env = os.getenv("YOUTUBE_CLIENT_SECRET_JSON")
        if client_secret_env and not self.client_secret_path.exists():
            with open(self.client_secret_path, "w", encoding="utf-8") as f:
                f.write(client_secret_env)

        token_env = os.getenv("YOUTUBE_TOKEN_JSON")
        if token_env and not self.token_path.exists():
            with open(self.token_path, "w", encoding="utf-8") as f:
                f.write(token_env)

    def authenticate(self) -> bool:
        """Authenticates with YouTube Data API v3 using OAuth 2.0."""
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = None
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            except Exception as e:
                logger.warning(f"Existing token is invalid: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.warning(f"Could not refresh token: {e}. Need fresh login.")
                    creds = None

            if not creds:
                if not self.client_secret_path.exists():
                    logger.warning(f"YouTube credentials '{self.client_secret_path}' not found.")
                    return False
                flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secret_path), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, "w") as token_file:
                token_file.write(creds.to_json())

        self.youtube_service = build("youtube", "v3", credentials=creds)
        logger.info("Successfully authenticated with YouTube Data API v3.")
        return True

    def upload_short(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Uploads a video to YouTube as a Short."""
        privacy = privacy_status or config.YOUTUBE_PRIVACY_STATUS
        tags = tags or ["Shorts", "AI"]

        # Ensure #Shorts is present in title for algorithm indexing
        if "#Shorts" not in title and "#shorts" not in title:
            title = f"{title} #Shorts"

        if dry_run or not self.client_secret_path.exists():
            logger.info("[UPLOAD - DRY RUN / MOCK] Video upload simulated:")
            logger.info(f"   Title:       {title}")
            logger.info(f"   Privacy:     {privacy}")
            logger.info(f"   Tags:        {tags}")
            logger.info(f"   File:        {video_path}")
            return {
                "id": "mock_short_id_12345",
                "url": "https://youtube.com/shorts/mock_short_id_12345",
                "status": "simulated"
            }

        if not self.youtube_service:
            if not self.authenticate():
                raise RuntimeError("Could not authenticate with YouTube. Please ensure client_secret.json is configured.")

        from googleapiclient.http import MediaFileUpload

        body = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": tags,
                "categoryId": "24"  # Entertainment
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(
            str(video_path),
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 2
        )

        logger.info(f"[UPLOAD] Uploading '{title}' to YouTube ({privacy})...")
        request = self.youtube_service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"   Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://youtube.com/shorts/{video_id}"
        logger.info(f"[OK] Short published successfully! URL: {video_url}")
        return {
            "id": video_id,
            "url": video_url,
            "status": "published"
        }
