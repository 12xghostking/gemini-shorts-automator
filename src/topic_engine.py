"""Topic and Prompt Engine using a bank of 5,000+ unique cinematic Short concepts."""

import json
import random
import logging
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field

from src import config

logger = logging.getLogger(__name__)

# Default rotating categories for dynamic variety
VIRAL_NICHES = [
    "Mythical Dragons & Flying Titans",
    "Cyberpunk & Feudal Warriors",
    "Holy Warriors & Crusaders",
    "Deep Sea Bioluminescent Leviathans",
    "Futuristic Mecha & Sci-Fi Warfare",
    "Ancient Titans & Primordials",
    "Cosmic Entities & Nebula Gods",
    "Shadow Assassins & Rogues",
    "Norse Mythology & Raiders",
]

class ShortConcept(BaseModel):
    category: str
    concept_title: str
    video_prompt: str = Field(description="Detailed visual prompt for Veo in 9:16 vertical format")
    voiceover_script: str = Field(description="10-25 word gripping narrative hook")
    youtube_title: str = Field(description="Catchy Short title including #Shorts")
    youtube_description: str
    tags: List[str]


class TopicEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.concepts_bank_path = config.ASSETS_DIR / "concepts_bank.json"
        self.concepts: List[dict] = []
        self._load_bank()

    def _load_bank(self):
        """Loads the 5,000+ concept offline database for instant, zero-failure concept generation."""
        if self.concepts_bank_path.exists():
            try:
                with open(self.concepts_bank_path, "r", encoding="utf-8") as f:
                    self.concepts = json.load(f)
                logger.info(f"[TOPIC ENGINE] Loaded {len(self.concepts)} unique concepts from bank.")
            except Exception as e:
                logger.warning(f"Failed to load concepts_bank.json: {e}")
        else:
            logger.warning("concepts_bank.json not found. Running with fallback generator.")

    def generate_concept(self, category: Optional[str] = None) -> ShortConcept:
        """
        Instantly selects a unique concept from the 5,000+ database,
        guaranteeing zero 503 API downtime and instant response.
        """
        chosen_category = (category or "").strip()

        # If user specified a category (e.g. "paladin", "samurai", "dragon")
        if chosen_category and self.concepts:
            query = chosen_category.lower()
            # Filter concepts matching category, title, prompt, or tags
            matched = [
                c for c in self.concepts
                if query in c.get("category", "").lower()
                or query in c.get("concept_title", "").lower()
                or query in c.get("video_prompt", "").lower()
                or any(query in t.lower() for t in c.get("tags", []))
            ]
            if matched:
                selected = random.choice(matched)
                return ShortConcept(**selected)

        # If no specific category or no match in bank, pick randomly from the 5,000
        if self.concepts:
            selected = random.choice(self.concepts)
            return ShortConcept(**selected)

        # Dynamic algorithmic fallback if bank is not present
        cat_name = chosen_category or random.choice(VIRAL_NICHES)
        return ShortConcept(
            category=cat_name,
            concept_title=f"The Legend of the {cat_name.title()}",
            video_prompt=(
                f"Cinematic vertical 9:16 framing. An epic {cat_name} unleashing radiant celestial energy "
                "amidst swirling storm clouds, shattered stone, and glowing embers. Dynamic low-angle tracking camera, "
                "hyper-detailed armor textures, volumetric god rays, photorealistic 8k render."
            ),
            voiceover_script=f"When shadows consumed the realm, only the legendary {cat_name} could turn the tide.",
            youtube_title=f"The Legendary {cat_name.title()} Has Awakened! #Shorts",
            youtube_description=f"Witness the power of the {cat_name}. Subscribe for daily epic visual encounters!",
            tags=["Shorts", cat_name.lower().replace(" ", ""), "Fantasy", "Cinematic", "AIArt", "Epic", "Veo"]
        )
