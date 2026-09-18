"""Builds an extensive offline database of 5,000+ unique, high-retention Short concepts
powered by an expanded universe of 250+ distinct archetypes across all genres.
"""

import json
import itertools
from pathlib import Path

# Expanded universe of 250+ unique archetypes
ARCHETYPES = [
    # --- Holy & Celestial Warriors (1-25) ---
    {"name": "Paladin of the Sun", "category": "Holy Warriors & Crusaders", "weapon": "a radiant dawnbreaker greatsword", "power": "blinding solar celestial wrath"},
    {"name": "Templar Grandmaster", "category": "Holy Warriors & Crusaders", "weapon": "a sacred blessed flamberge and tower shield", "power": "calling down a pillar of golden divine fire"},
    {"name": "Archangel Seraph", "category": "Celestial Entities & Angels", "weapon": "six flaming wings and a spear of pure starlight", "power": "summoning an apocalyptic judgement blast"},
    {"name": "Dawn Valkyrie", "category": "Norse Sky Warriors", "weapon": "a crystalline spear of morning light", "power": "unleashing the radiant gates of Valhalla"},
    {"name": "Solar Inquisitor", "category": "Holy Warriors & Crusaders", "weapon": "a gilded chained flail crackling with holy fire", "power": "purging shadows with an expanding sun-burst"},
    {"name": "Celestial Guardian", "category": "Celestial Entities & Angels", "weapon": "twin halberds forged from solar flares", "power": "erecting an impenetrable dome of solid daylight"},
    {"name": "Lightbringer Cleric", "category": "Holy Warriors & Crusaders", "weapon": "a heavy golden war-mace", "power": "erupting divine healing runes that incinerate monsters"},
    {"name": "Sun-Forged Centurion", "category": "Ancient Legions & Warriors", "weapon": "a solar pilum spear and crested mirror shield", "power": "reflecting deadly laser beams of concentrated sunlight"},
    {"name": "Aegis Sentinel", "category": "Holy Warriors & Crusaders", "weapon": "a towering mirror-polished kite shield", "power": "a concussive kinetic rebound shockwave"},
    {"name": "Aura Knight", "category": "Holy Warriors & Crusaders", "weapon": "an ethereal broadsword woven from pure photons", "power": "a 360-degree crescent wave of blinding energy"},
    {"name": "Radiant Arbiter", "category": "Celestial Entities & Angels", "weapon": "golden executioner scales and a blazing claymore", "power": "severing chaotic entities from reality"},
    {"name": "Daybreak Paladin", "category": "Holy Warriors & Crusaders", "weapon": "a twin-handed golden warhammer", "power": "striking the earth to unleash subterranean geysers of light"},
    {"name": "Solar Pegasus Knight", "category": "Sky Realms & Mythic Beasts", "weapon": "a lance tip glowing with plasma heat", "power": "a hypersonic aerial dive-bomb strike"},
    {"name": "High Seraphim", "category": "Celestial Entities & Angels", "weapon": "a bow strung with strings of blinding light", "power": "raining thousand-arrow meteor volleys"},
    {"name": "Divine Crusader", "category": "Holy Warriors & Crusaders", "weapon": "a blessed longsword engulfed in white flame", "power": "cutting through dimension rifts with pure light"},
    {"name": "Golden Lion Knight", "category": "Holy Warriors & Crusaders", "weapon": "a lion-crested war-axe and buckler", "power": "unleashing a deafening celestial lion roar"},
    {"name": "Sanctified Duelist", "category": "Holy Warriors & Crusaders", "weapon": "an ornate golden rapier", "power": "blinding-speed precision thrusts that pierce darkness"},
    {"name": "Solar Champion", "category": "Holy Warriors & Crusaders", "weapon": "a heavy solar cleaver", "power": "an explosive sun-strike that incinerates miles"},
    {"name": "Elysian Warden", "category": "Celestial Entities & Angels", "weapon": "a pearl-white scythe", "power": "harvesting corruption and transforming it into starlight"},
    {"name": "Star-Forged Crusader", "category": "Holy Warriors & Crusaders", "weapon": "a heavy bastard sword embedded with pulsar gems", "power": "unleashing gravity-crushing light shockwaves"},
    {"name": "Sun-King Vanguard", "category": "Holy Warriors & Crusaders", "weapon": "dual sun-daggers", "power": "leaving trails of white-hot embers during high-speed combat"},
    {"name": "Caelum Sky-Knight", "category": "Sky Realms & Mythic Beasts", "weapon": "an aerodynamic feather-edged blade", "power": "commanding gale-force hurricane winds infused with light"},
    {"name": "Seraphic Executioner", "category": "Celestial Entities & Angels", "weapon": "a massive guillotine blade of holy energy", "power": "an unblockable vertical overhead split"},
    {"name": "Sol Invictus Warmaster", "category": "Holy Warriors & Crusaders", "weapon": "a circular sun-shield with bladed edges", "power": "spinning into a deadly vortex of plasma blades"},
    {"name": "Radiant Battlemage", "category": "Holy Warriors & Crusaders", "weapon": "a crystal spell-blade and holy grimoire", "power": "summoning orbiting solar spheres that barrage enemies"},

    # --- Feudal, Samurai & Ninja Legends (26-55) ---
    {"name": "Cyber Samurai", "category": "Cyberpunk & Feudal Warriors", "weapon": "a dual plasma-edged katana", "power": "hyper-accelerated nanosecond reflex dash"},
    {"name": "Neon Ronin", "category": "Cyberpunk & Feudal Warriors", "weapon": "a weathered cursed Muramasa blade", "power": "a single blinding cherry-blossom draw strike"},
    {"name": "Shadow Shinobi", "category": "Shadow Assassins & Rogues", "weapon": "twin shadow-forged kunai and shuriken", "power": "dissolving into smoke and striking from shadows"},
    {"name": "Kunoichi Phantom", "category": "Shadow Assassins & Rogues", "weapon": "razor-sharp combat fans tipped with poison", "power": "spinning into a lethal whirlwind of flying blades"},
    {"name": "Oni Demon Slayer", "category": "Feudal Legends & Ronin", "weapon": "a spiked iron kanabo club", "power": "shattering demonic skulls with earthquake strikes"},
    {"name": "Shaolin Grandmaster", "category": "Martial Arts & Monks", "weapon": "a dragon-carved wooden bo staff", "power": "deflecting bullets with supersonic spinning strikes"},
    {"name": "Blood Moon Samurai", "category": "Cyberpunk & Feudal Warriors", "weapon": "a crimson odachi two-handed great katana", "power": "releasing crescent shockwaves of blood mist"},
    {"name": "Shogun Warlord", "category": "Feudal Legends & Ronin", "weapon": "a gilded naginata polearm", "power": "commanding ghost armies with a sweep of the blade"},
    {"name": "Wind-Cutter Ronin", "category": "Feudal Legends & Ronin", "weapon": "an ultra-thin chokuto sword", "power": "slicing air into vacuum blades that cut from afar"},
    {"name": "Lightning Shinobi", "category": "Shadow Assassins & Rogues", "weapon": "dual ninjato charged with violet electricity", "power": "teleporting instantly with thunderclaps"},
    {"name": "Onmyoji Master", "category": "Feudal Legends & Ronin", "weapon": "sacred origami shikigami talismans", "power": "summoning nine-tailed phantom foxes to attack"},
    {"name": "Ghost of Tsushima Style Bushi", "category": "Feudal Legends & Ronin", "weapon": "a razor Sakai steel katana", "power": "unleashing the terrifying Ghost Stance assault"},
    {"name": "Cyber Geisha Assassin", "category": "Cyberpunk & Feudal Warriors", "weapon": "concealed wire blades inside silk sleeves", "power": "decapitating multiple targets in one graceful pirouette"},
    {"name": "Iron Monk of Wudang", "category": "Martial Arts & Monks", "weapon": "meteor iron gauntlets", "power": "shattering boulders and steel with pure internal chi"},
    {"name": "Yakuza Cyber-Boss", "category": "Cyberpunk & Feudal Warriors", "weapon": "a high-frequency cyber katana and thermal revolver", "power": "activating military-grade sub-dermal armor"},
    {"name": "Cherry Blossom Blademaster", "category": "Feudal Legends & Ronin", "weapon": "a damascus folded-steel iaito", "power": "a thousand cuts appearing before the blade is even resheathed"},
    {"name": "Demon-Masked Ninja", "category": "Shadow Assassins & Rogues", "weapon": "chain-sickle kusarigama", "power": "wrapping enemies from distance and dragging them into the abyss"},
    {"name": "Sohei Warrior Monk", "category": "Feudal Legends & Ronin", "weapon": "a heavy cross-spear jumonji yari", "power": "holding mountain passes against endless cavalry"},
    {"name": "Frost Katana Master", "category": "Cyberpunk & Feudal Warriors", "weapon": "a blade forged from eternal mountain ice", "power": "freezing blood in enemy veins upon contact"},
    {"name": "Flame-Breathing Bushi", "category": "Feudal Legends & Ronin", "weapon": "a scorching blackened blade", "power": "igniting air into trails of dragon fire with each slash"},
    {"name": "Poison Lotus Kunoichi", "category": "Shadow Assassins & Rogues", "weapon": "venomous senbon needles", "power": "vanishing mid-air in a cloud of intoxicating petals"},
    {"name": "Cybernetic Duelist", "category": "Cyberpunk & Feudal Warriors", "weapon": "a laser-edge wakizashi", "power": "calculating parry trajectories with AI targeting optics"},
    {"name": "Sovereign Shogun", "category": "Feudal Legends & Ronin", "weapon": "an emperor-engraved ceremonial katana", "power": "a shockwave of pure royal conqueror conqueror chi"},
    {"name": "Nightblade Shinobi", "category": "Shadow Assassins & Rogues", "weapon": "a matte-black stealth blade", "power": "moving invisibly under rainy night conditions"},
    {"name": "Thunderclap Samurai", "category": "Cyberpunk & Feudal Warriors", "weapon": "a crackling electro-katana", "power": "breaking the sound barrier with a sonic boom slash"},
    {"name": "Immortal Ronin", "category": "Feudal Legends & Ronin", "weapon": "a chipped blade covered in ancestral charms", "power": "regenerating fatal wounds while pressing forward"},
    {"name": "Cybernetic Ronin Drifter", "category": "Cyberpunk & Feudal Warriors", "weapon": "a thermal-heated longblade", "power": "melting through armored mechs with a single stroke"},
    {"name": "Jade Dragon Monk", "category": "Martial Arts & Monks", "weapon": "a dragon-head jade quarterstaff", "power": "summoning an ethereal emerald dragon around his strikes"},
    {"name": "Silent Assassin", "category": "Shadow Assassins & Rogues", "weapon": "a silent monomolecular garrote wire", "power": "eliminating targets without making a single sound"},
    {"name": "Zen Archery Master", "category": "Feudal Legends & Ronin", "weapon": "a giant yumi asymmetric war-bow", "power": "splitting distant raindrops and piercing armored fortresses"},

    # --- Ancient & Classical Legions (56-80) ---
    {"name": "Spartan Commander", "category": "Ancient Legions & Warriors", "weapon": "a bronze-tipped dory spear and heavy hoplite shield", "power": "an unyielding phalanx shockwave that repels armies"},
    {"name": "Roman Centurion", "category": "Ancient Legions & Warriors", "weapon": "a gladius shortsword and rectangular scutum shield", "power": "disciplined legionnaire formation assault"},
    {"name": "Gladiator Champion", "category": "Ancient Legions & Warriors", "weapon": "a net and trident tipped with serrated steel", "power": "entangling and executing beasts before cheering crowds"},
    {"name": "Aztec Jaguar Warrior", "category": "Ancient Legions & Warriors", "weapon": "an obsidian-toothed macuahuitl war club", "power": "channeling the raw stealth and bloodlust of the jungle predator"},
    {"name": "Mayan Eagle Scout", "category": "Ancient Legions & Warriors", "weapon": "an atlatl dart-thrower and flint dagger", "power": "striking from canopy heights with pinpoint precision"},
    {"name": "Immortals Guard", "category": "Ancient Legions & Warriors", "weapon": "a recurve composite bow and wicker shield", "power": "an endless synchronized hail of black-feathered arrows"},
    {"name": "Egyptian Anubis Guard", "category": "Ancient Legions & Warriors", "weapon": "a ceremonial khopesh sickle-sword", "power": "summoning jackal shadows to devour enemy souls"},
    {"name": "Pharaoh's Charioteer", "category": "Ancient Legions & Warriors", "weapon": "a gilded double-curved war bow", "power": "firing flaming arrows while drifting horse-drawn war chariots"},
    {"name": "Carthaginian War Leader", "category": "Ancient Legions & Warriors", "weapon": "a falcata curved slashing sword", "power": "commanding armored war elephants to trample defenses"},
    {"name": "Greek Hoplite Veteran", "category": "Ancient Legions & Warriors", "weapon": "a leaf-shaped xiphos sword", "power": "locking shields in an unbreakable bronze wall"},
    {"name": "Viking Jarl", "category": "Norse Mythology & Raiders", "weapon": "a damascus bearded axe and round shield", "power": "igniting battlefield morale with a war horn blast"},
    {"name": "Shieldmaiden of Odin", "category": "Norse Mythology & Raiders", "weapon": "a runed short-spear and raven shield", "power": "parrying monstrous beasts with flawless timing"},
    {"name": "Berserker of Fenrir", "category": "Norse Mythology & Raiders", "weapon": "dual heavy battleaxes", "power": "entering an unkillable blood-frenzy immune to pain"},
    {"name": "Celtic Woad Warrior", "category": "Ancient Legions & Warriors", "weapon": "a massive iron broadsword", "power": "channeling ancient forest spirits through blue warpaint"},
    {"name": "Highland Claymore Master", "category": "Ancient Legions & Warriors", "weapon": "a massive six-foot two-handed claymore", "power": "cleaving through ranks of armored soldiers in sweeping arcs"},
    {"name": "Mongol Keshik Archer", "category": "Ancient Legions & Warriors", "weapon": "a high-tension horn bow", "power": "hitting moving targets from galloping horses a mile away"},
    {"name": "Rajput Kshatriya", "category": "Ancient Legions & Warriors", "weapon": "a flexible urumi whip-sword and talwar", "power": "spinning like a lethal metallic storm that deflects arrows"},
    {"name": "Zulu Impi Chieftain", "category": "Ancient Legions & Warriors", "weapon": "an iklwa stabbing spear and cowhide shield", "power": "the swift 'buffalo horns' flanking maneuver"},
    {"name": "Maori Toa Champion", "category": "Ancient Legions & Warriors", "weapon": "a heavy greenstone mere club", "power": "terrifying foes with the primal spirit of the Haka"},
    {"name": "Teutonic Grandmaster", "category": "Ancient Legions & Warriors", "weapon": "a heavy flanged mace", "power": "smashing through plate armor like brittle glass"},
    {"name": "Winged Hussar", "category": "Ancient Legions & Warriors", "weapon": "a 18-foot hollow lance with eagle feather wings", "power": "a thunderous cavalry charge that breaks any infantry wall"},
    {"name": "Mamluk Duelist", "category": "Ancient Legions & Warriors", "weapon": "a curved damascus scimitar", "power": "parrying multiple weapons simultaneously with peerless agility"},
    {"name": "Janissary Musketeer", "category": "Ancient Legions & Warriors", "weapon": "an engraved flintlock musket and yatagan sword", "power": "devastating volley fire followed by close-quarters butchery"},
    {"name": "Landsknecht Mercenary", "category": "Ancient Legions & Warriors", "weapon": "a flame-bladed zweihander greatsword", "power": "shattering enemy spearwalls in one overhead cleave"},
    {"name": "Conquistador Captain", "category": "Ancient Legions & Warriors", "weapon": "a steel rapier and buckler", "power": "tactical counter-ripostes against monstrous wildlife"},

    # --- Mythical & Monster Beasts (81-120) ---
    {"name": "Obsidian Dragon", "category": "Mythical Dragons & Flying Titans", "weapon": "diamond-sharp obsidian talons", "power": "breathing a helix of cobalt blue plasma lightning"},
    {"name": "Solar Phoenix", "category": "Celestial Beasts & Avian Titans", "weapon": "molten golden feathers", "power": "bursting into a blinding supernova reincarnation"},
    {"name": "Abyssal Leviathan", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "monolithic glowing bioluminescent jaws", "power": "summoning a crushing black-ocean whirlpool"},
    {"name": "Frost Wyrm", "category": "Glacial Legends & Ice Titans", "weapon": "spines of razor-sharp glacier ice", "power": "freezing the entire atmosphere in an instant"},
    {"name": "Colossal Behemoth", "category": "Ancient Titans & Primordials", "weapon": "mountain-sized stone fists", "power": "shattering the continental tectonic plate"},
    {"name": "Celestial Griffin", "category": "Sky Realms & Mythic Beasts", "weapon": "storm-infused razor claws", "power": "hurling tempest cyclone blades from the sky"},
    {"name": "Void Hydra", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "seven serpentine shadow heads", "power": "spewing dark matter venom that melts reality"},
    {"name": "Storm Thunderbird", "category": "Celestial Beasts & Avian Titans", "weapon": "wings made of flashing thunderclouds", "power": "discharging million-volt lightning storms"},
    {"name": "Cerberus Hound of Hades", "category": "Ancient Titans & Primordials", "weapon": "three demonic fanged maws and a serpent tail", "power": "spewing underworld hellfire and petrifying roars"},
    {"name": "Nemean Lion", "category": "Ancient Titans & Primordials", "weapon": "golden impenetrable pelt and diamond claws", "power": "a sonic roar that collapses cliff faces"},
    {"name": "Chimera of Epidaurus", "category": "Ancient Titans & Primordials", "weapon": "lion jaws, venomous goat horns, and viper tail", "power": "triple elemental breath of fire, poison, and venom"},
    {"name": "Midgard Serpent Jormungandr", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "planet-circling venomous coils", "power": "drowning continents under toxic tidal waves"},
    {"name": "Fenrir the Giant Wolf", "category": "Norse Mythology & Raiders", "weapon": "jaw that touches earth while upper touches sky", "power": "snapping cosmic chains and swallowing the sun"},
    {"name": "Quetzalcoatl Feathered Serpent", "category": "Celestial Beasts & Avian Titans", "weapon": "emerald rainbow feathers and golden fangs", "power": "commanding solar tempests and revitalizing the land"},
    {"name": "Abyssal Kraken", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "massive barbed suction tentacles", "power": "dragging whole armadas into the dark ocean trench"},
    {"name": "Basilisks King", "category": "Ancient Titans & Primordials", "weapon": "corrosive venomous gaze", "power": "turning flesh into stone and dissolving steel"},
    {"name": "Manticore of the Badlands", "category": "Ancient Titans & Primordials", "weapon": "bat wings and scorpion barbed tail", "power": "firing volleys of toxic crystalline spines"},
    {"name": "Iron Golem Colossus", "category": "Ancient Titans & Primordials", "weapon": "solid forged steel fists and furnace chest", "power": "venting blast-furnace heat and crushing fortifications"},
    {"name": "Ancient Sandworm", "category": "Ancient Titans & Primordials", "weapon": "circular rows of diamond teeth", "power": "erupting from dunes to swallow entire desert cities"},
    {"name": "Bioluminescent Siren Queen", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "pulsing aquatic soundwaves and coral claws", "power": "hypnotizing sailors and summoning sea storms"},
    {"name": "Canyon Wyvern", "category": "Mythical Dragons & Flying Titans", "weapon": "poison-tipped tail and aerodynamic wings", "power": "supersonic canyon dives that slice mountain spires"},
    {"name": "Golden Dragon Sovereign", "category": "Mythical Dragons & Flying Titans", "weapon": "gilded celestial scales and mustache whiskers", "power": "summoning golden rain that purifies evil"},
    {"name": "Crimson Blood Drake", "category": "Mythical Dragons & Flying Titans", "weapon": "serrated crimson fangs and barbed wings", "power": "a flame breath that burns underwater"},
    {"name": "Bone Dragon Necrowyrm", "category": "Dark Magic & Undead Hordes", "weapon": "hollow skeletal ribcage and necrotic miasma", "power": "raising fallen enemies as skeletal thralls"},
    {"name": "Molten Magma Dragon", "category": "Mythical Dragons & Flying Titans", "weapon": "scales made of cooling basalt crust", "power": "vomiting volcanic lava rivers across the land"},
    {"name": "Eldritch Star-Spawn", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "writhing mass of non-Euclidean tentacles", "power": "driving onlookers mad through psychological horror"},
    {"name": "Shadow Behemoth", "category": "Ancient Titans & Primordials", "weapon": "mass of solid midnight mist and glowing purple eyes", "power": "extinguishing all light sources in a ten-mile radius"},
    {"name": "Crystal Roc", "category": "Celestial Beasts & Avian Titans", "weapon": "crystal talons and prism wings", "power": "refracting sun rays into burning laser beams"},
    {"name": "Cave Wyrm", "category": "Mythical Dragons & Flying Titans", "weapon": "blind sensory whiskers and stone-crushing jaws", "power": "burrowing through solid granite in seconds"},
    {"name": "Gorgon Queen", "category": "Ancient Titans & Primordials", "weapon": "nest of living venomous vipers for hair", "power": "a direct stare that instantly petrifies living flesh"},
    {"name": "Minotaur of the Labyrinth", "category": "Ancient Titans & Primordials", "weapon": "a massive double-bitted iron labrys axe", "power": "unstoppable bull charge that shatters stone pillars"},
    {"name": "Harpy Matriarch", "category": "Sky Realms & Mythic Beasts", "weapon": "razor steel talons and piercing screech", "power": "a sonic shriek that shatters glass and eardrums"},
    {"name": "Frost Phoenix", "category": "Glacial Legends & Ice Titans", "weapon": "crystalline azure plumage", "power": "exploding into a sub-zero blizzard nova upon death"},
    {"name": "Spectral Pegasus", "category": "Sky Realms & Mythic Beasts", "weapon": "spectral hooves that walk on cloud tops", "power": "passing through solid enemy armor harmlessly"},
    {"name": "Deep Ocean Leviathan", "category": "Deep Sea Bioluminescent Leviathans", "weapon": "armor plated scales and bioluminescent lure", "power": "generating devastating underwater shockwaves"},
    {"name": "Thunder Horn Behemoth", "category": "Ancient Titans & Primordials", "weapon": "massive twin spiraling lightning horns", "power": "channeling lightning bolts from thunderclouds"},
    {"name": "Blood Hound of the Void", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "phasing teeth that bite through dimensions", "power": "hunting scent across parallel timelines"},
    {"name": "Plague Hydra", "category": "Dark Magic & Undead Hordes", "weapon": "rotting multi-heads and toxic breath", "power": "sprouting two heads whenever one is severed"},
    {"name": "Chimeric Griffin", "category": "Sky Realms & Mythic Beasts", "weapon": "eagle beak and lion forelegs", "power": "tearing through dragon scales with ease"},
    {"name": "Starlight Kirin", "category": "Celestial Beasts & Avian Titans", "weapon": "a single pearl horn that channels holy light", "power": "walking on water and air leaving starry trails"},

    # --- Sci-Fi, Cyberpunk & Mecha Warfare (121-170) ---
    {"name": "Heavy Assault Mech", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "dual shoulder-mounted railguns", "power": "a devastating 360-degree micro-missile barrage"},
    {"name": "Chrono Weaver", "category": "Time Travel & Paradoxes", "weapon": "a floating temporal hourglass staff", "power": "freezing bullets mid-air and rewinding seconds"},
    {"name": "Cybernetic Shinobi", "category": "Neo-Tokyo & Cyberpunk", "weapon": "high-frequency vibrating kunai", "power": "leaving holographic decoys while cloaked in stealth"},
    {"name": "Orbital Drop Shocktrooper", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a rapid-fire gauss assault rifle", "power": "falling from stratosphere pods straight into battle"},
    {"name": "Nanotech Assassin", "category": "Neo-Tokyo & Cyberpunk", "weapon": "swarms of microscopic nanite blades", "power": "disassembling enemy armor on a molecular level"},
    {"name": "Plasma Sniper", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a ten-foot heavy anti-material plasma rifle", "power": "shooting through mountains with pinpoint accuracy"},
    {"name": "Exosuit Brawler", "category": "Neo-Tokyo & Cyberpunk", "weapon": "pneumatic hydraulic power-fists", "power": "punching through solid bank vaults with sonic booms"},
    {"name": "Cyber Valkyrie", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "anti-gravity energy wings and laser lance", "power": "flying at Mach 3 while dropping thermal bombs"},
    {"name": "Drone Swarm Commander", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a wrist holographic command terminal", "power": "orchestrating 500 autonomous kamikaze drones"},
    {"name": "Quantum Hacker", "category": "Neo-Tokyo & Cyberpunk", "weapon": "neural link cyberdeck and EMP pistols", "power": "hijacking enemy mechs and turning them on their allies"},
    {"name": "Titan Mecha Pilot", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a skyscraper-sized thermal sword", "power": "cleaving colossal kaiju in half with one stroke"},
    {"name": "Cyber Inquisitor", "category": "Neo-Tokyo & Cyberpunk", "weapon": "energy whip and thermal suppressors", "power": "frying rogue cyborg brains with electric shocks"},
    {"name": "Void Stalker", "category": "Cosmic Entities & Nebula Gods", "weapon": "a dark matter blade that bends light", "power": "phasing through solid walls and security shields"},
    {"name": "Hoverbike Ronin", "category": "Neo-Tokyo & Cyberpunk", "weapon": "a monomolecular naginata", "power": "high-speed highway dogfights weaving through traffic"},
    {"name": "Android Revolutionary", "category": "Neo-Tokyo & Cyberpunk", "weapon": "overclocked cybernetic limbs", "power": "breaking human limits with zero thermal throttles"},
    {"name": "Tesla Shock Trooper", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a backpack arc-generator lightning gun", "power": "chaining lightning across twenty armored targets"},
    {"name": "Space Marine Dreadnought", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "twin rotary assault cannons and power claw", "power": "unyielding advance through concentrated artillery"},
    {"name": "Bounty Hunter of Mars", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a thermal tracking carbine and jetpack", "power": "hunting targets through zero-gravity space wrecks"},
    {"name": "Cybernetic Berserker", "category": "Neo-Tokyo & Cyberpunk", "weapon": "chainsaw blades built directly into forearms", "power": "pumping combat adrenaline for super speed"},
    {"name": "Nanotech Swarm Host", "category": "Neo-Tokyo & Cyberpunk", "weapon": "liquid metal body that morphs into blades", "power": "regenerating from a single remaining drop of metal"},
    {"name": "Anti-Gravity Duelist", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "twin repulsion rapiers", "power": "fighting on walls and ceilings with zero gravity"},
    {"name": "EMP Vanguard", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "an electromagnetic pulse shotgun", "power": "blacking out entire city sectors with one blast"},
    {"name": "Cyber Medic Guardian", "category": "Neo-Tokyo & Cyberpunk", "weapon": "a heavy riot shield with defibrillator charge", "power": "deploying nano-shields that absorb explosions"},
    {"name": "Orbital Railgunner", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "satellite-linked orbital targeting beacon", "power": "calling down tungsten kinetic rods from orbit"},
    {"name": "Stealth Infiltrator Unit", "category": "Neo-Tokyo & Cyberpunk", "weapon": "suppressed particle beam pistol", "power": "active thermoptic camouflage making him invisible"},
    {"name": "Mech-Hunter Stalker", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "harpoon launcher with high-voltage cables", "power": "grounding 100-ton mechs and short-circuiting their cores"},
    {"name": "Solar Flare Pilot", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "solar-powered fighter thrusters and laser cannons", "power": "blinding dogfight maneuvers near the sun"},
    {"name": "Warp Blade Commando", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "teleportation-linked combat knives", "power": "blinking five times per second while striking"},
    {"name": "Nuclear Golem Mech", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "uranium-tipped fists and core meltdown blast", "power": "sacrificing reactor to incinerate the enemy"},
    {"name": "Cyber Hound Handler", "category": "Neo-Tokyo & Cyberpunk", "weapon": "mechanical war-dogs with titanium jaws", "power": "flanking and pinning armored targets instantly"},
    {"name": "Heavy Siege Automaton", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "twin 500mm siege howitzers", "power": "flattening enemy fortress walls from miles away"},
    {"name": "Laser Aegis Sentinel", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "interlocking laser shield panels", "power": "deflecting incoming missile salvos back to sender"},
    {"name": "Cybernetic Duelist Ace", "category": "Neo-Tokyo & Cyberpunk", "weapon": "curved plasma saber and flashbang grenades", "power": "blinding reflexes that dodge automatic gunfire"},
    {"name": "Zero-G Marine", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "recoilless magnetic carbine", "power": "acrobatic three-dimensional combat inside airlocks"},
    {"name": "Nanotech Plague Doctor", "category": "Neo-Tokyo & Cyberpunk", "weapon": "beak mask aerosol disperser", "power": "dissolving cybernetics into digital rust"},
    {"name": "Cyber Dragoon", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "anti-vehicle energy spear and rocket boots", "power": "leaping 300 feet into the air to impale dropships"},
    {"name": "Sub-Zero Cryo-Mech", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "liquid nitrogen cryo-sprayer", "power": "freezing metal until it shatters from physical impacts"},
    {"name": "Plasma Grenadier", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "rotary drum plasma grenade launcher", "power": "carpet bombing sectors with sticky blue plasma"},
    {"name": "Android Sword-Dancer", "category": "Neo-Tokyo & Cyberpunk", "weapon": "quadruple mechanical arms with lightblades", "power": "spinning into an impenetrable hemisphere of death"},
    {"name": "Void Raider", "category": "Cosmic Entities & Nebula Gods", "weapon": "salvaged alien particle blasters", "power": "breaching starship hulls and surviving hard vacuum"},
    {"name": "Supercarrier Admiral Mech", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "flight deck shoulders launching mini-interceptors", "power": "blanketing the sky with swarming air cover"},
    {"name": "Cybernetic Shadow Monk", "category": "Neo-Tokyo & Cyberpunk", "weapon": "monomolecular clawed gauntlets", "power": "moving so fast cameras only capture static"},
    {"name": "Kinetic Juggernaut", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "heavy kinetic battering ram", "power": "absorbing bullet impacts to supercharge punches"},
    {"name": "Ghost Fleet Captain", "category": "Cosmic Entities & Nebula Gods", "weapon": "plasma cutlass and boarding hook", "power": "cloaking entire battlecruisers inside asteroid fields"},
    {"name": "Cyber Samurai Duelist", "category": "Cyberpunk & Feudal Warriors", "weapon": "an overheated red plasma katana", "power": "shearing through armored mech plating with solar heat"},
    {"name": "Heavy Ordnance Trooper", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "quad-barrel rocket launcher", "power": "leveling enemy sniper perches in seconds"},
    {"name": "Nanite Shield Warden", "category": "Neo-Tokyo & Cyberpunk", "weapon": "expanding honeycomb energy shields", "power": "protecting civilian convoys from airstrikes"},
    {"name": "Bio-Mech Hybrid", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "symbiote cyber-tentacles and acid spray", "power": "infecting enemy machinery and consuming their power"},
    {"name": "Solar Particle Lancer", "category": "Futuristic Mecha & Sci-Fi Warfare", "weapon": "a focused sunbeam particle accelerator", "power": "drilling holes through star destroyer hulls"},
    {"name": "Cyber Ronin Gunslinger", "category": "Cyberpunk & Feudal Warriors", "weapon": "energy revolver and wakizashi", "power": "deadeye ricochet shots that bypass cover"},

    # --- Cosmic, Temporal & Dimensional Entities (171-210) ---
    {"name": "Astral Archon", "category": "Cosmic Entities & Nebula Gods", "weapon": "a spear forged from dead neutron stars", "power": "bending spacetime gravitational waves to crush foes"},
    {"name": "Black Hole Harvester", "category": "Cosmic Entities & Nebula Gods", "weapon": "a siphon scythe of singular density", "power": "creating localized event horizons that swallow light"},
    {"name": "Nebula Weaver", "category": "Cosmic Entities & Nebula Gods", "weapon": "threads of glowing interstellar gas and dust", "power": "weaving cosmic constellations that rain supernovas"},
    {"name": "Supernova Forger", "category": "Cosmic Entities & Nebula Gods", "weapon": "cosmic blacksmith tongs and anvil of dying stars", "power": "forging planets and hurling white-hot sun shards"},
    {"name": "Chrono Lord", "category": "Time Travel & Paradoxes", "weapon": "the Blade of Stolen Moments", "power": "aging enemies by a hundred years with a single touch"},
    {"name": "Void Archmage", "category": "Cosmic Entities & Nebula Gods", "weapon": "an orb containing a captured galaxy", "power": "opening tears in the fabric of the universe"},
    {"name": "Starlight Empress", "category": "Cosmic Entities & Nebula Gods", "weapon": "a crown of orbiting quasars and scepter of light", "power": "illuminating darkness with the radiance of creation"},
    {"name": "Cosmic Voyager", "category": "Cosmic Entities & Nebula Gods", "weapon": "a compass that navigates higher dimensions", "power": "stepping between parallel universes at will"},
    {"name": "Entropy Harbinger", "category": "Cosmic Entities & Nebula Gods", "weapon": "the Ash of Extinguished Stars", "power": "hastening the inevitable heat death of matter"},
    {"name": "Solar Flare Deity", "category": "Cosmic Entities & Nebula Gods", "weapon": "whips of coronal mass ejections", "power": "stripping atmospheres with solar winds"},
    {"name": "Dimensional Ripper", "category": "Time Travel & Paradoxes", "weapon": "scissors that cut space-time coordinates", "power": "folding reality so enemies hit themselves"},
    {"name": "Pulsar Knight", "category": "Cosmic Entities & Nebula Gods", "weapon": "a lance pulsating with gamma-ray bursts", "power": "sweeping beams of lethal cosmic radiation"},
    {"name": "Gravity Manipulator", "category": "Cosmic Entities & Nebula Gods", "weapon": "rings of ultra-dense matter", "power": "increasing enemy weight by 10,000x until bones break"},
    {"name": "Time-Lost Wanderer", "category": "Time Travel & Paradoxes", "weapon": "an antique stopwatch that halts reality", "power": "walking through frozen battlefields untouched"},
    {"name": "Eclipse Sovereign", "category": "Cosmic Entities & Nebula Gods", "weapon": "a disk that blots out celestial bodies", "power": "plunging worlds into eternal freezing dark"},
    {"name": "Dark Matter Entity", "category": "Cosmic Entities & Nebula Gods", "weapon": "invisible gravitational claws", "power": "collapsing stars without being detected by instruments"},
    {"name": "Cosmic Dragon of the Milky Way", "category": "Mythical Dragons & Flying Titans", "weapon": "spiral galaxy arms as dragon wings", "power": "breathing streams of pure hydrogen and plasma"},
    {"name": "Paradox Inquisitor", "category": "Time Travel & Paradoxes", "weapon": "a rapier that erases grandfather paradoxes", "power": "removing historical events from existence"},
    {"name": "Quasar Titan", "category": "Cosmic Entities & Nebula Gods", "weapon": "jets of relativistic matter", "power": "firing energy beams brighter than a trillion suns"},
    {"name": "Stellar Cartographer", "category": "Cosmic Entities & Nebula Gods", "weapon": "a celestial globe projecting hyper-routes", "power": "warping planets into collision courses"},
    {"name": "Void Siren", "category": "Cosmic Entities & Nebula Gods", "weapon": "cosmic radio frequencies echoing in deep space", "power": "luring starships to their doom in black holes"},
    {"name": "Comet Vanguard", "category": "Cosmic Entities & Nebula Gods", "weapon": "a tail of frozen methane and star dust", "power": "crashing into planets at hypersonic velocity"},
    {"name": "Temporal Duelist", "category": "Time Travel & Paradoxes", "weapon": "a sword that hits 3 seconds before being swung", "power": "winning fights before the opponent even draws"},
    {"name": "Celestial Architect", "category": "Cosmic Entities & Nebula Gods", "weapon": "compasses that measure planetary orbits", "power": "rebuilding shattered worlds into Dyson spheres"},
    {"name": "Zero-Point Manipulator", "category": "Cosmic Entities & Nebula Gods", "weapon": "vacuum energy generators", "power": "pulling infinite raw energy from the quantum foam"},
    {"name": "Primordial Void Walker", "category": "Cosmic Entities & Nebula Gods", "weapon": "shadows from before the Big Bang", "power": "returning matter to pure unformed nothingness"},
    {"name": "Supercluster Sovereign", "category": "Cosmic Entities & Nebula Gods", "weapon": "the Great Attractor gravitational pull", "power": "dragging whole galaxies across millions of lightyears"},
    {"name": "Singularity Knight", "category": "Cosmic Entities & Nebula Gods", "weapon": "a blade with infinite mass at its tip", "power": "crushing shields with unstoppable momentum"},
    {"name": "Cosmic Alchemist", "category": "Cosmic Entities & Nebula Gods", "weapon": "a crucible that fuses hydrogen into gold", "power": "transmuting enemy armor into radioactive isotopes"},
    {"name": "Astral Phantasm", "category": "Cosmic Entities & Nebula Gods", "weapon": "starlight projections of previous incarnations", "power": "fighting with fifty spectral copies simultaneously"},
    {"name": "Horizon Sentinel", "category": "Cosmic Entities & Nebula Gods", "weapon": "the edge of the observable universe", "power": "barring extra-dimensional horrors from entering reality"},
    {"name": "Cosmic Seraph", "category": "Celestial Entities & Angels", "weapon": "feathered wings made of solar aurora", "power": "healing entire planetary biospheres with a song"},
    {"name": "Dark Star Warlock", "category": "Dark Magic & Undead Hordes", "weapon": "a staff tipped with a decaying brown dwarf", "power": "draining warmth and life from planets"},
    {"name": "Quantum Entanglement Assassin", "category": "Time Travel & Paradoxes", "weapon": "paired twin daggers linked across distance", "power": "stabbing one dagger to kill a target lightyears away"},
    {"name": "Cosmic Tempest Herald", "category": "Cosmic Entities & Nebula Gods", "weapon": "a horn that channels pulsar radio pulses", "power": "summoning space storms that disable electronics"},
    {"name": "Eldritch Stargazer", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "a telescope that looks beyond sanity", "power": "manifesting the nightmares seen in the deep void"},
    {"name": "Hypernova Berserker", "category": "Cosmic Entities & Nebula Gods", "weapon": "two axes burning with fusion cores", "power": "exploding with the force of dying blue giants"},
    {"name": "Cosmic Judge", "category": "Cosmic Entities & Nebula Gods", "weapon": "the Hammer of Universal Constants", "power": "adjusting the speed of light to paralyze foes"},
    {"name": "Astral Pathfinder", "category": "Cosmic Entities & Nebula Gods", "weapon": "a lantern burning with ancient starlight", "power": "guiding lost souls across the sea of space"},
    {"name": "Omega Entity", "category": "Cosmic Entities & Nebula Gods", "weapon": "the Final Epoch Seal", "power": "bringing an end to all things when the universe expires"},

    # --- Dark Fantasy, Undead & Necromantic (211-250+) ---
    {"name": "Dread Necromancer", "category": "Dark Magic & Undead Hordes", "weapon": "a bone-carved skull staff", "power": "raising legions of glowing spectral wraiths"},
    {"name": "Vampire Lord of Wallachia", "category": "Dark Fantasy & Vampires", "weapon": "blood-forged silver rapier and bat swarm", "power": "dissolving into crimson mist and biting necks"},
    {"name": "Lich King of the Frozen Peak", "category": "Dark Magic & Undead Hordes", "weapon": "a frostmourne runeblade and phylactery", "power": "freezing hearts and commanding undead giants"},
    {"name": "Death Knight of the Apocalypse", "category": "Dark Magic & Undead Hordes", "weapon": "a soul-devouring jagged greatsword", "power": "spreading plagues and summoning skeletal steeds"},
    {"name": "Plague Doctor of the Black Death", "category": "Dark Fantasy & Vampires", "weapon": "a poison cane and alchemical gas grenades", "power": "unleashing virulent black mist that rots flesh"},
    {"name": "Blood Countess", "category": "Dark Fantasy & Vampires", "weapon": "a goblet of maiden blood and silver claws", "power": "commanding blood rivers that impale intruders"},
    {"name": "Cursed Marionette Master", "category": "Dark Magic & Undead Hordes", "weapon": "barbed strings that control living bodies", "power": "turning enemy warriors against their comrades"},
    {"name": "Abyssal Shadow Fiend", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "claws of solidified nightmare darkness", "power": "stealing shadows and devouring human sanity"},
    {"name": "Gothic Gargoyle Patriarch", "category": "Dark Fantasy & Vampires", "weapon": "granite claws and demonic stone wings", "power": "awakening from cathedral rooftops under moonlight"},
    {"name": "Warlock of the Crimson Pact", "category": "Dark Magic & Undead Hordes", "weapon": "a tome bound in demon skin", "power": "summoning hellish horned pit fiends"},
    {"name": "Grave Warden", "category": "Dark Magic & Undead Hordes", "weapon": "a heavy iron shovel and lantern of souls", "power": "keeping restless undead buried deep under soil"},
    {"name": "Bone Colossus", "category": "Dark Magic & Undead Hordes", "weapon": "clubs made of fused skeletal mammoth bones", "power": "crushing battalions and absorbing their skeletons"},
    {"name": "Banshee Queen of Crying Swamps", "category": "Dark Magic & Undead Hordes", "weapon": "spectral tears and rotting crown", "power": "a wail that instantly stops human hearts from beating"},
    {"name": "Werewolf Alpha of Black Forest", "category": "Dark Fantasy & Vampires", "weapon": "nine-inch titanium-strength claws", "power": "leaping sixty feet to rip armored knights to shreds"},
    {"name": "Eldritch Cultist High Priest", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "a dagger carved from alien meteor stone", "power": "opening the deep sunken gates of R'lyeh"},
    {"name": "Specter of the Guillotine", "category": "Dark Magic & Undead Hordes", "weapon": "a flying executioner blade on rusted chains", "power": "hunting monarchs and tyrants across generations"},
    {"name": "Hollow Knight Soul-Vessel", "category": "Dark Fantasy & Vampires", "weapon": "a fractured nail blade and void cloak", "power": "channeling pure abyssal darkness from an empty shell"},
    {"name": "Witch of the Cursed Bog", "category": "Dark Magic & Undead Hordes", "weapon": "a bubbling cauldron and twisted root wand", "power": "turning hunters into beasts and cursing entire bloodlines"},
    {"name": "Hellhound Master", "category": "Dark Magic & Undead Hordes", "weapon": "chains of brimstone and iron collar", "power": "unleashing flaming red-eyed beasts that never sleep"},
    {"name": "Revenant of the Battlefield", "category": "Dark Magic & Undead Hordes", "weapon": "broken spears stuck through his own chest", "power": "cannot be killed until his vengeance is fulfilled"},
    {"name": "Phantom Highwayman", "category": "Dark Fantasy & Vampires", "weapon": "ghostly dual flintlocks that fire spectral balls", "power": "riding a headless horse through storm clouds"},
    {"name": "Blood Berserker", "category": "Dark Fantasy & Vampires", "weapon": "twin serrated meat cleavers", "power": "growing stronger and faster the more blood is shed"},
    {"name": "Nightmare Weaver", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "threads spun from human terrors", "power": "manifesting your deepest fear as a physical monster"},
    {"name": "Crypt Lord Beetle", "category": "Dark Magic & Undead Hordes", "weapon": "chitinous spiky carapace and burrowing claws", "power": "summoning swarms of flesh-eating scarabs"},
    {"name": "Dark Shaman of the Bone Tribe", "category": "Dark Magic & Undead Hordes", "weapon": "a rattle made of human teeth and stag skull", "power": "blighting crops and poisoning river waters with curses"},
    {"name": "Fallen Seraph of Pride", "category": "Celestial Entities & Angels", "weapon": "charred black wings and a broken holy sword", "power": "corrupting sacred temples into burning ruins"},
    {"name": "Abyssal Jester", "category": "Dark Fantasy & Vampires", "weapon": "juggling daggers coated with madness toxins", "power": "laughing hysterically while dodging fatal strikes"},
    {"name": "Vampiric Nightwing", "category": "Dark Fantasy & Vampires", "weapon": "leathery wings with razor bone spurs", "power": "swooping down to snatch sentries in complete silence"},
    {"name": "Spectral Galleon Captain", "category": "Dark Magic & Undead Hordes", "weapon": "a spectral cutlass and barnacle pistol", "power": "sailing through dense fog on green ghost flames"},
    {"name": "Soul-Eater Demon", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "a gaping maw in its stomach lined with teeth", "power": "swallowing souls whole to grow in physical size"},
    {"name": "Gargoyle Assassin", "category": "Dark Fantasy & Vampires", "weapon": "stone daggers and razor tail", "power": "posing as stone for decades before making a single strike"},
    {"name": "Corpse-Stitched Golem", "category": "Dark Magic & Undead Hordes", "weapon": "steel plates bolted directly to rotting flesh", "power": "ignoring sword cuts as if they were mosquito bites"},
    {"name": "Vampire Noble Duelist", "category": "Dark Fantasy & Vampires", "weapon": "a ceremonial dueling sword with ruby pommel", "power": "parrying attacks with a wine glass in the other hand"},
    {"name": "Dread Banshee of the Cliffs", "category": "Dark Magic & Undead Hordes", "weapon": "wailing spectral gusts of wind", "power": "pushing warriors off stormy seaside cliffs"},
    {"name": "Undead Gladiator", "category": "Dark Magic & Undead Hordes", "weapon": "a rusted trident with impaled human skulls", "power": "fighting on with no head or limbs"},
    {"name": "Blood Alchemist", "category": "Dark Fantasy & Vampires", "weapon": "syringes of volatile boiling vampire blood", "power": "injecting himself to gain monstrous giant strength"},
    {"name": "Void Cult Inquisitor", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "a mace with an eyeball embedded in the head", "power": "forcing enemies to see visions of the abyss"},
    {"name": "Shadow Dancer", "category": "Shadow Assassins & Rogues", "weapon": "crescent blades attached to silk cords", "power": "dancing between torch shadows without touching the floor"},
    {"name": "Gothic Vampire Bride", "category": "Dark Fantasy & Vampires", "weapon": "silk lace dress concealing steel needles", "power": "charming castle guards before draining them dry"},
    {"name": "Lord of the Abyssal Throne", "category": "Eldritch Terrors & Abyssal Horrors", "weapon": "a throne carved from the skulls of forgotten gods", "power": "commanding the nightmare realm with a gesture"}
]

ENVIRONMENTS = [
    "on the rain-slicked roof of a neon-drenched Tokyo skyscraper at midnight",
    "at the edge of a crumbling gothic cathedral during a blood-red lunar eclipse",
    "amidst a thunderous stormy mountain peak with lightning striking violently around",
    "inside the dark abyssal depths of the Mariana Trench surrounded by glowing marine snow",
    "inside a burning volcanic caldera with rivers of molten magma flowing below",
    "across a desolate glacier tundra beneath the shimmering green aurora borealis",
    "within an ancient crumbling desert temple being consumed by a violent sandstorm",
    "on floating shattered islands drifting around a colossal dying star in deep space",
    "inside an overgrown cybernetic ruin where nature has reclaimed towering skyscrapers",
    "upon a misty feudal battlefield covered in scattered banners and falling cherry blossoms",
    "inside an alien bioluminescent crystal cavern pulsating with violet and cyan light",
    "at the golden gates of a forgotten celestial fortress towering into the upper atmosphere",
    "within a dark dystopian megacity under pouring neon rain and holographic blimps",
    "atop a stormy ocean sea-cliff as massive 60-foot waves crash against black jagged rocks",
    "in the eye of a cosmic nebula where gravity is shattered and space-time warps",
    "inside an ancient subterranean dwarven forge with roaring blast furnaces",
    "on the deck of a storm-battered pirate galleon navigating treacherous monster-filled seas",
    "within a cursed graveyard surrounded by weeping angel statues and green phantom fog",
    "inside a high-tech orbital space station airlock overlooking planet Earth",
    "on a blood-soaked Roman Colosseum arena floor surrounded by 50,000 roaring spectators"
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
    "surviving a catastrophic blast and standing defiantly amidst rising embers and smoke",
    "charging forward at supersonic speed leaving a trail of shattered shockwaves",
    "executing an acrobatic mid-air spin that cleaves through multiple armored targets",
    "parrying a monstrous blow that creates a 100-foot kinetic pressure wave",
    "releasing a blinding pulse of raw elemental energy that incinerates the shadows",
    "standing atop a mountain of defeated foes as lightning flashes dramatically behind"
]

LIGHTING_AND_STYLE = [
    "Dynamic vertical 9:16 framing, extreme low-angle tracking camera, volumetric god rays, high-contrast chiaroscuro, photorealistic 8k render.",
    "Cinematic vertical 9:16 aspect ratio, dizzying circular camera orbit, glowing neon reflections, rain droplets in slow motion, unreal engine 5 style.",
    "Epic vertical 9:16 shot, rapid tilt-up motion, dramatic rim lighting, embers drifting through dark mist, hyper-detailed textures.",
    "Cinematic vertical 9:16 framing, sweeping macro close-up to wide tracking shot, bioluminescent glow, atmospheric depth haze, 8k cinematic realism.",
    "Vertical 9:16 composition, fast-action camera drift with subtle motion blur, high-contrast backlighting, particle physics, masterwork CGI.",
    "Cinematic 9:16 vertical cinematography, anamorphic lens flares, moody atmospheric fog, extreme slow motion at 120fps, photorealistic textures.",
    "Hyper-realistic 9:16 vertical shot, low-angle hero framing, golden hour solar illumination, floating dust particles, blockbuster movie aesthetic."
]

VOICEOVER_NARRATIVES = [
    "In the forgotten age of warriors, the {name} swore an unbreakable oath. Armed with {weapon}, they stood as the realm's last defense. When shadows struck, they unleashed {power}—reminding the world why some legends must never be challenged.",
    "Ancient prophecies warned of the day the {name} would awaken. With {weapon} drawn, they took their stance. Unleashing {power}, the very foundation of reality trembled. Watch closely before history is rewritten.",
    "In a battle where a single mistake means oblivion, the {name} never hesitates. Gripping {weapon}, they charged headfirst into the storm. Through {power}, victory was claimed in less than a heartbeat.",
    "When all hope was abandoned, one lone warrior refused to bow: the {name}. Standing firm with {weapon}, they met the advancing horde. Channeling {power}, they turned the battlefield into blinding starlight.",
    "They said this battle was already lost. But they forgot who ruled the frontlines: the {name}. Drawing {weapon} in blinding silence, they unleashed {power}. In seconds, centuries of darkness collapsed into dust.",
    "Only once every thousand years does a strike like this occur. The legendary {name} raised {weapon} towards the sky. Channeling {power}, they tore through the enemy lines with godlike fury.",
    "Mortals believed the tales were just myths—until the {name} descended. Wielding {weapon}, they brought divine retribution to the battlefield. One blast of {power}, and the encroaching shadows were banished forever.",
    "Surrounded on all sides, any normal fighter would falter. But the {name} is built for the impossible. Gripping {weapon} with iron resolve, they unleashed {power}. Witness the wrath of an undefeated titan.",
    "From the highest peaks to the deepest shadows, the name of the {name} commands absolute reverence. Empowered by {weapon}, they ignited {power}. Tell us in the comments: who could ever stop them?",
    "When empires crumble, only true legends stand tall. The {name} took their final stance with {weapon}. Channeling {power}, they pushed back the abyss when everyone said it couldn't be done.",
    "The skies turned pitch black as the {name} stepped forward into the fray. With {weapon} crackling in their hands, they unleashed {power}. A strike so pure, it echoed across the mortal realm.",
    "Trained in absolute secrecy, the {name} only emerges when the world teeters on the edge of destruction. With {weapon} at the ready, they channeled {power}. Nothing in their path was left standing.",
    "Destiny called, and the {name} answered without fear. Locking eyes with the enemy, they drew {weapon}. Through {power}, fate itself was severed in a fraction of a second.",
    "Some warriors rely on armor. The {name} relies on pure, unstoppable will. Raising {weapon} high, they ignited {power}, shattering the battlefield into blazing embers.",
    "Long after the clash ends, the legend of the {name} will echo through eternity. Armed with {weapon}, they channeled {power}. Watch until the end to see true supremacy.",
    "Before anyone could even react, the {name} had already struck. Wielding {weapon} with surgical precision, they activated {power}. In the blink of an eye, the duel was over.",
    "A celestial aura engulfed the battlefield as the {name} revealed their true form. Gripping {weapon}, they unleashed {power}. This is what peak power looks like.",
    "Carrying the spirits of all who came before, the {name} stepped into the fray. With {weapon} ignited, they channeled {power}. Honor never dies.",
    "They studied the art of war for centuries, reaching perfection as the {name}. Bearing {weapon}, they unleashed {power}—leaving spectators in absolute awe.",
    "This is the moment everything changed. The {name} unleashed the full might of {weapon}. Channeling {power}, they etched their name into legend forever."
]

TITLE_TEMPLATES = [
    "The {name} Awakens! ⚔️ #Shorts",
    "When The {name} Strikes! ⚡ #Shorts",
    "Legendary {name} Showdown 🔥 #Shorts",
    "The Strike That Made The {name} Legendary #Shorts",
    "No One Could Stop The {name}! #Shorts",
    "The True Power of The {name} #Shorts",
    "The {name}'s Final Clash! 🛡️ #Shorts",
    "Ancient {name} Unleashed! 💥 #Shorts",
    "The Day The {name} Appeared #Shorts",
    "Could You Survive The {name}? #Shorts",
    "The {name} Defies Destiny! #Shorts",
    "Wrath of The {name} Revealed #Shorts",
    "The Strike That Shattered The Realm: {name} #Shorts",
    "Witness The Power of The {name}! #Shorts",
    "When The {name} Enters The Battlefield #Shorts",
    "The Secret Technique of The {name} #Shorts",
    "The Undefeated {name} Strikes Again #Shorts",
    "The {name}'s Legendary Duel #Shorts",
    "Why The {name} Was Feared By Everyone #Shorts",
    "The {name} Unleashes Ancient Wrath #Shorts"
]

def generate_5000_concepts(output_file: Path, concepts_per_archetype: int = 20):
    concepts = []
    seen_prompts = set()
    
    # Generate balanced concepts for EVERY archetype in the universe
    for arch_idx, arch in enumerate(ARCHETYPES):
        name = arch["name"]
        cat = arch["category"]
        weapon = arch["weapon"]
        power = arch["power"]
        clean_name = name.replace(" ", "")

        for i in range(concepts_per_archetype):
            env = ENVIRONMENTS[(arch_idx * 7 + i) % len(ENVIRONMENTS)]
            act = ACTIONS[(arch_idx * 5 + i) % len(ACTIONS)]
            style = LIGHTING_AND_STYLE[(arch_idx * 3 + i) % len(LIGHTING_AND_STYLE)]
            hook = VOICEOVER_NARRATIVES[i % len(VOICEOVER_NARRATIVES)].format(name=name, weapon=weapon, power=power)
            title = TITLE_TEMPLATES[(arch_idx * 3 + i) % len(TITLE_TEMPLATES)].format(name=name)

            prompt = (
                f"Cinematic vertical 9:16 framing. A legendary {name} wielding {weapon} {env}. "
                f"The subject is {act}, channeling {power}. {style}"
            )
            
            if prompt in seen_prompts:
                continue
            seen_prompts.add(prompt)
            
            desc = (
                f"Witness the power of the {name} as ancient legends come alive. "
                f"Created with cinematic AI visual storytelling. Subscribe for daily epic encounters! #Shorts #{clean_name}"
            )
            tags = ["Shorts", clean_name, "Cinematic", "Epic", "AIArt", "Storytelling", "Animation"]

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
        
    print(f"Successfully generated {len(concepts)} unique Short concepts into {output_file}!")
    print(f"Total unique archetypes in bank: {len({c['concept_title'].split(':')[0] for c in concepts})}")

if __name__ == "__main__":
    dest = Path(__file__).resolve().parent / "assets" / "concepts_bank.json"
    generate_5000_concepts(dest, concepts_per_archetype=20)

