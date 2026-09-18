"""Builds an extensive offline database of 5,000+ unique, high-retention Short concepts."""

import json
import itertools
from pathlib import Path

# High-impact archetypes across popular YouTube Shorts niches
ARCHETYPES = [
    # Warriors & Combatants
    {"name": "Paladin", "category": "Holy Warriors & Crusaders", "weapon": "a radiant dawnbreaker greatsword", "power": "blinding solar celestial wrath"},
    {"name": "Cyber Samurai", "category": "Cyberpunk & Feudal Warriors", "weapon": "a dual plasma-edged katana", "power": "hyper-accelerated nanosecond reflex dash"},
    {"name": "Shadow Assassin", "category": "Shadow Assassins & Rogues", "weapon": "twin shadow-forged daggers", "power": "merging seamlessly into dark abyssal mist"},
    {"name": "Spartan Commander", "category": "Ancient Legions & Warriors", "weapon": "a bronze-tipped spear and hoplite shield", "power": "an unyielding phalanx shockwave"},
    {"name": "Viking Berserker", "category": "Norse Mythology & Raiders", "weapon": "frost-runed dual battleaxes", "power": "unleashing the thunderous roar of Odin"},
    {"name": "Ronin Swordsman", "category": "Feudal Legends & Ronin", "weapon": "a weathered cursed Muramasa blade", "power": "a single blinding cherry-blossom draw strike"},
    {"name": "Blood Knight", "category": "Dark Fantasy & Vampires", "weapon": "a jagged crimson flamberge", "power": "erupting blood-crystal spikes"},
    {"name": "Templar Crusader", "category": "Medieval & Crusades", "weapon": "a sacred steel broadsword and kite shield", "power": "calling down a pillar of golden divine fire"},
    
    # Mythical & Monster Beasts
    {"name": "Obsidian Dragon", "category": "Mythical Dragons & Flying Titans", "weapon": "diamond-sharp obsidian talons", "power": "breathing a helix of cobalt blue plasma lightning"},
    {"name": "Solar Phoenix", "category": "Celestial Beasts & Avian Titans", "weapon": "molten golden feathers", "power": "bursting into a blinding supernova reincarnation"},
    {"name": "Abyssal Leviathan", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "monolithic glowing bioluminescent jaws", "power": "summoning a crushing black-ocean whirlpool"},
    {"name": "Frost Wyrm", "category": "Glacial Legends & Ice Titans", "weapon": "spines of razor-sharp glacier ice", "power": "freezing the entire atmosphere in an instant"},
    {"name": "Colossal Behemoth", "category": "Ancient Titans & Primordials", "weapon": "mountain-sized stone fists", "power": "shattering the continental tectonic plate"},
    {"name": "Celestial Griffin", "category": "Sky Realms & Mythic Beasts", "weapon": "storm-infused razor claws", "power": "hurling tempest cyclone blades"},
    {"name": "Void Hydra", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "seven serpentine shadow heads", "power": "spewing dark matter venom"},
    
    # Sci-Fi, Mecha & Cosmic
    {"name": "Heavy Assault Mech", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "shoulder-mounted railguns", "power": "a devastating 360-degree missile salvo"},
    {"name": "Chrono Weaver", "category": "Time Travel & Paradoxes", "weapon": "a floating temporal hourglass staff", "power": "freezing bullets mid-air and reversing time"},
    {"name": "Cybernetic Shinobi", "category": "Neo-Tokyo & Cyberpunk", "weapon": "high-frequency vibrating kunai", "power": "leaving hologram decoys while teleporting"},
    {"name": "Astral Archon", "category": "Cosmic Entities & Nebula Gods", "weapon": "a spear forged from dead neutron stars", "power": "bending spacetime gravitational waves"},
    {"name": "Dread Necromancer", "category": "Dark Magic & Undead Hordes", "weapon": "a bone-carved soul staff", "power": "raising an army of glowing spectral wraiths"},
    {"name": "Volcanic Golem", "category": "Elemental Titans & Cataclysms", "weapon": "magma-coated volcanic boulders", "power": "triggering a subterranean supervolcano eruption"},
    {"name": "Desert Djinn", "category": "Ancient Sands & Spirits", "weapon": "swirling scimitars of living sand", "power": "swallowing an army in a golden sandstorm"},
    {"name": "Bioluminescent Siren", "category": "Ocean Depths & Mythic Sirens", "weapon": "pulsing oceanic crystal tridents", "power": "hypnotic spectral soundwaves under water"},
    {"name": "Valkyrie Harbinger", "category": "Norse Sky Warriors", "weapon": "a spear of aurora borealis light", "power": "opening the golden gates of Valhalla"},
    {"name": "Ironclad Juggernaut", "category": "Dieselpunk & Steampunk Titans", "weapon": "hydraulic pneumatic warhammers", "power": "steam-powered explosive tremors"}
]

ENVIRONMENTS = [
    "on the rain-slicked roof of a neon-drenched Tokyo skyscraper at midnight",
    "at the edge of a crumbling gothic cathedral during a blood-red lunar eclipse",
    "amidst a thunderous stormy mountain peak with lightning striking around",
    "inside the dark abyssal depths of the Mariana Trench surrounded by glowing marine snow",
    "inside a burning volcanic caldera with rivers of molten magma flowing below",
    "across a desolate glacier tundra beneath the shimmering green aurora borealis",
    "within an ancient crumbling desert temple being consumed by a violent sandstorm",
    "on floating shattered islands drifting around a colossal dying star",
    "inside an overgrown cybernetic ruin where nature has reclaimed towering skyscrapers",
    "upon a misty feudal battlefield covered in scattered banners and falling cherry blossoms",
    "inside an alien bioluminescent crystal cavern pulsating with violet light",
    "at the gates of a forgotten celestial fortress towering into the upper atmosphere",
    "within a dark dystopian megacity under pouring neon rain and holographic blimps",
    "atop a stormy ocean sea-cliff as massive 50-foot waves crash against black jagged rocks",
    "in the eye of a cosmic nebula where gravity is shattered and space-time warps"
]

ACTIONS = [
    "unleashing a devastating ultimate strike that shatters the ground into floating debris",
    "clashing against a shadowy monstrous entity in an intense, high-speed lethal duel",
    "ascending into the stormy heavens surrounded by an explosive shockwave of light",
    "slowly drawing their legendary weapon as glowing runes awaken along its blade",
    "defending against an overwhelming horde of nightmarish shadow beasts",
    "plunging their weapon into an ancient seal to awaken dormant apocalyptic power",
    "dodging a deadly barrage in extreme slow motion with sparks and raindrops reflecting light",
    "channeling an ancient celestial spell that splits the dark clouds wide open",
    "stepping through a swirling portal of raw cosmic energy onto the battlefield",
    "surviving a catastrophic blast and standing defiantly amidst rising embers and smoke"
]

LIGHTING_AND_STYLE = [
    "Dynamic vertical 9:16 framing, extreme low-angle tracking camera, volumetric god rays, high-contrast chiaroscuro, photorealistic 8k render.",
    "Cinematic vertical 9:16 aspect ratio, dizzying circular camera orbit, glowing neon reflections, rain droplets in slow motion, unreal engine 5 style.",
    "Epic vertical 9:16 shot, rapid tilt-up motion, dramatic rim lighting, embers drifting through dark mist, hyper-detailed textures.",
    "Cinematic vertical 9:16 framing, sweeping macro close-up to wide tracking shot, bioluminescent glow, atmospheric depth haze, 8k cinematic realism.",
    "Vertical 9:16 composition, fast-action camera drift with subtle motion blur, high-contrast backlighting, particle physics, masterwork CGI."
]

HOOK_TEMPLATES = [
    "When darkness consumed the mortal realm, only the {name} dared to defy fate.",
    "Ancient scrolls warned of this exact day. Watch what happens when the {name} awakens.",
    "In a battle where a single mistake means oblivion, honor is measured in nanoseconds.",
    "They believed the legends were just myths. Until the skies turned dark and the {name} appeared.",
    "Deep beyond where sunlight dares to reach, ancient power waits for those worthy enough to wield it.",
    "They said this titan could never be stopped. But they forgot who was standing in their way.",
    "When the heavens shattered, one warrior stood alone against the encroaching abyss.",
    "Legends said one strike could sever destiny itself. Watch closely before it happens.",
    "Only once every thousand years does this power awaken. Witness the true wrath of the {name}.",
    "When all hope was lost, the shadows parted to reveal something far more terrifying."
]

TITLE_TEMPLATES = [
    "The {name} Awakens! #Shorts",
    "When The {name} Strikes! #Shorts",
    "Legendary {name} Showdown #Shorts",
    "The Strike That Shattered Fate #Shorts",
    "No One Saw This Coming! #Shorts",
    "The Power of the {name} #Shorts",
    "The Final Duel Begins #Shorts",
    "Ancient {name} Unleashed #Shorts"
]

def generate_5000_concepts(output_file: Path):
    concepts = []
    seen_prompts = set()
    
    # Generate all combinatorial possibilities
    combinations = itertools.product(ARCHETYPES, ENVIRONMENTS, ACTIONS, LIGHTING_AND_STYLE)
    
    for idx, (arch, env, act, style) in enumerate(combinations):
        if len(concepts) >= 5000:
            break
            
        name = arch["name"]
        cat = arch["category"]
        weapon = arch["weapon"]
        power = arch["power"]
        
        prompt = (
            f"Cinematic vertical 9:16 framing. A legendary {name} wielding {weapon} {env}. "
            f"The subject is {act}, channeling {power}. {style}"
        )
        
        if prompt in seen_prompts:
            continue
        seen_prompts.add(prompt)
        
        hook = HOOK_TEMPLATES[idx % len(HOOK_TEMPLATES)].format(name=name)
        title = TITLE_TEMPLATES[idx % len(TITLE_TEMPLATES)].format(name=name)
        desc = (
            f"Witness the power of the {name} as ancient legends come alive. "
            f"Created with cinematic AI visual storytelling. Subscribe for daily epic encounters! #Shorts #{name.replace(' ', '')}"
        )
        tags = ["Shorts", name.replace(" ", ""), "Cinematic", "Fantasy", "Epic", "AIArt", "Veo", "Animation"]
        
        concepts.append({
            "category": cat,
            "concept_title": f"{name}: {act.split()[0].title()} of Destiny",
            "video_prompt": prompt,
            "voiceover_script": hook,
            "youtube_title": title,
            "youtube_description": desc,
            "tags": tags
        })
        
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2)
        
    print(f"Generated {len(concepts)} unique Short concepts into {output_file}!")

if __name__ == "__main__":
    dest = Path(__file__).resolve().parent / "assets" / "concepts_bank.json"
    generate_5000_concepts(dest)
