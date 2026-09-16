"""Topic and Prompt Engine using Google Gemini to brainstorm dynamic viral concepts."""

import json
import random
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from src import config

logger = logging.getLogger(__name__)

# Default rotating categories for dynamic variety
VIRAL_NICHES = [
    "Mythical Dragons & Flying Titans",
    "Cyberpunk & Feudal Samurai Duels",
    "Ancient Celestial Gods & Beings",
    "Deep Sea Bioluminescent Leviathans",
    "Post-Apocalyptic Mecha Guardians",
    "Surreal Elemental Magic & Portals",
    "Galactic Nebula Explorers",
]

class ShortConcept(BaseModel):
    category: str
    concept_title: str
    video_prompt: str = Field(description="Detailed visual prompt for Veo in 9:16 vertical format")
    voiceover_script: str = Field(description="10-25 word gripping narrative hook")
    youtube_title: str = Field(description="Catchy Short title including #Shorts")
    youtube_description: str
    tags: list[str]


FALLBACK_CONCEPTS = [
    ShortConcept(
        category="Mythical Dragons & Flying Titans",
        concept_title="Obsidian Dragon Breaking The Storm",
        video_prompt=(
            "Cinematic vertical 9:16 shot. A colossal obsidian dragon with glowing molten-gold veins "
            "soars dynamically through thunderous dark storm clouds, breathing a helix of blue lightning into the night sky. "
            "Epic scale, dynamic low-angle tracking camera, hyper-detailed scales, rain droplets reacting to heat, photorealistic 8k render."
        ),
        voiceover_script="Ancient legends spoke of a storm dragon whose roar could ignite the night sky. What if the legends were real?",
        youtube_title="The Storm Dragon Has Awakened! ⚡🐉 #Shorts #Fantasy",
        youtube_description="Witness the awakening of the Obsidian Storm Dragon as it pierces through the celestial tempest. Subscribe for daily mythical encounters!",
        tags=["Shorts", "Dragon", "Fantasy", "AIArt", "Cinematic", "Mythology", "Veo"]
    ),
    ShortConcept(
        category="Cyberpunk & Feudal Samurai Duels",
        concept_title="Neon Rain Duel of Two Master Blades",
        video_prompt=(
            "Cinematic vertical 9:16 framing. Two futuristic cyber-samurai facing each other on a wet skyscraper rooftop under neon rain. "
            "One draws a katana crackling with crimson plasma. Rapid camera arc motion, reflective puddle splashes, holographic billboards in background, hyper-realistic."
        ),
        voiceover_script="In the year 2099, honor is measured in nanoseconds. Only one blade will strike true.",
        youtube_title="Cyber Samurai Showdown in Neon Rain ⚔️🌧️ #Shorts #Cyberpunk",
        youtube_description="A lethal encounter in neo-Tokyo under pouring neon rain. Who survives the duel? Drop your prediction below!",
        tags=["Shorts", "Samurai", "Cyberpunk", "Katana", "Futuristic", "CGI", "Epic"]
    ),
    ShortConcept(
        category="Deep Sea Bioluminescent Leviathans",
        concept_title="The Abyssal Kraken of the Marianas",
        video_prompt=(
            "Cinematic vertical 9:16 framing. A deep-sea glowing bioluminescent kraken emerging from the darkest abyss. "
            "Ethereal cyan and violet tendrils pulsing with light, drifting marine snow, slow motion underwater camera drift, photorealistic BBC planet earth style."
        ),
        voiceover_script="Miles beneath the ocean surface, ancient leviathans lurk where sunlight has never dared to reach.",
        youtube_title="Deepest Leviathan Ever Recorded? 🌊🐙 #Shorts #DeepSea",
        youtube_description="What hides at the bottom of the Mariana Trench? Meet the bioluminescent lord of the abyss.",
        tags=["Shorts", "DeepSea", "Ocean", "Creature", "Bioluminescence", "Mystery"]
    )
]


class TopicEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI client: {e}")

    def generate_concept(self, category: Optional[str] = None) -> ShortConcept:
        """Generates a structured video concept and prompt."""
        chosen_category = category or random.choice(VIRAL_NICHES)

        # Use fallback if client is not configured or in dry-run without key
        if not self.client:
            logger.info("Using curated fallback concept (No GEMINI_API_KEY or offline mode).")
            matched = [c for c in FALLBACK_CONCEPTS if chosen_category.lower() in c.category.lower()]
            return random.choice(matched) if matched else random.choice(FALLBACK_CONCEPTS)

        prompt = f"""
You are a viral YouTube Shorts director specializing in breathtaking CGI, fantasy, and cinematic AI visual storytelling.
Brainstorm an unforgettable, high-retention video concept for the category: "{chosen_category}".

Requirements:
1. Concept: Visually explosive, dynamic, and cinematic (e.g., dynamic flight, intense clash, colossal scale).
2. Video Prompt: Explicitly designed for Google Veo video generation in vertical 9:16 aspect ratio. Describe lighting, camera motion, subject details, atmosphere, dynamic movement, and photorealistic textures. Avoid buzzwords like 'trending on artstation'; use direct cinematic cinematography terms.
3. Voiceover Script: Exactly 15 to 25 words. A hypnotic, mysterious, or high-stakes hook designed for immediate viewer retention.
4. YouTube Title: Must be under 65 characters, high CTR, and include #Shorts.
5. YouTube Description: 2-3 engaging sentences + call to action.
6. Tags: 5-8 relevant tags without hash symbols.

Respond ONLY with valid JSON matching this schema:
{{
  "category": "{chosen_category}",
  "concept_title": "string",
  "video_prompt": "string",
  "voiceover_script": "string",
  "youtube_title": "string",
  "youtube_description": "string",
  "tags": ["string", "string"]
}}
"""
        try:
            from google.genai import types
            chat = self.client.chats.create(
                model=config.GEMINI_TEXT_MODEL,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            response = chat.send_message(prompt)
            raw_text = response.text.strip()
            data = json.loads(raw_text)
            return ShortConcept(**data)
        except Exception as e:
            logger.error(f"Gemini API error during topic generation: {e}. Falling back to template.")
            return random.choice(FALLBACK_CONCEPTS)
