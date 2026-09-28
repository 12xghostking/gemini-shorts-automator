"""Builds an extensive offline database of 10,000+ unique, high-retention Short concepts
targeting proven viral YouTube Shorts niches (2025–2026 research-backed):

  1. Dark Psychology & Human Behavior
  2. Body Science & Medical Curiosities
  3. Historical "What If" Scenarios
  4. Scary Stories & Creepy Facts
  5. Space & Cosmos
  6. Animal Kingdom & Nature's Extremes
  7. Stoicism & Ancient Wisdom
  8. Unsolved Mysteries & Cold Cases
  9. Conspiracy Theories & Hidden History
 10. Mind-Blowing Science & "Did You Know"

Each concept is script-first with a curiosity-gap hook, dramatic narration (30-60 words),
and atmospheric visual prompts designed for faceless AI-generated imagery.
"""

import re
import json
import random
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# ██  NICHE DEFINITIONS — 10 proven viral categories              ██
# ═══════════════════════════════════════════════════════════════════

NICHES = {
    "Dark Psychology": {
        "description": "Hidden manipulation tactics, social power dynamics, and uncomfortable truths about human behavior",
        "visual_mood": "dark moody lighting, dramatic shadows, mysterious atmosphere, noir aesthetic",
        "tags_base": ["DarkPsychology", "Psychology", "HumanBehavior", "MindGames", "Manipulation"],
    },
    "Body Science": {
        "description": "Fascinating and terrifying things your body does, medical curiosities, biological limits",
        "visual_mood": "clinical yet dramatic lighting, 3D visualization feel, neon anatomical glow, dark background",
        "tags_base": ["BodyFacts", "Science", "HumanBody", "Medical", "Biology"],
    },
    "Historical What If": {
        "description": "Alternate history scenarios, modern tech in ancient times, what-if historical pivots",
        "visual_mood": "cinematic historical atmosphere, dramatic golden hour, ancient meets modern contrast",
        "tags_base": ["History", "WhatIf", "AlternateHistory", "HistoryFacts", "TimePeriod"],
    },
    "Scary & Creepy": {
        "description": "True scary stories, urban legends, creepy facts, paranormal encounters, disturbing truths",
        "visual_mood": "horror atmosphere, fog, dim flickering light, abandoned locations, eerie shadows",
        "tags_base": ["Scary", "Creepy", "Horror", "TrueScary", "UrbanLegends"],
    },
    "Space & Cosmos": {
        "description": "Mind-bending space facts, cosmic scale comparisons, what-if cosmic scenarios",
        "visual_mood": "deep space nebula colors, cosmic scale, dramatic planet lighting, star-field backgrounds",
        "tags_base": ["Space", "Cosmos", "Universe", "Astronomy", "SpaceFacts"],
    },
    "Animal Kingdom": {
        "description": "Insane animal abilities, nature's most extreme creatures, biological superpowers",
        "visual_mood": "nature documentary cinematic, dramatic wildlife lighting, close-up intensity",
        "tags_base": ["Animals", "Nature", "Wildlife", "AnimalFacts", "Biology"],
    },
    "Stoicism & Wisdom": {
        "description": "Ancient philosophical wisdom applied to modern life, mental toughness, self-mastery",
        "visual_mood": "marble statue aesthetic, stoic philosophy atmosphere, classical architecture, moody contemplative",
        "tags_base": ["Stoicism", "Philosophy", "Wisdom", "MentalStrength", "SelfImprovement"],
    },
    "Unsolved Mysteries": {
        "description": "Cold cases, disappearances, unexplained phenomena, historical enigmas",
        "visual_mood": "detective noir, case file aesthetic, dim desk lamp, evidence board atmosphere",
        "tags_base": ["Unsolved", "Mystery", "ColdCase", "TrueCrime", "Unexplained"],
    },
    "Conspiracy & Hidden History": {
        "description": "Declassified operations, suppressed history, suspicious coincidences, government secrets",
        "visual_mood": "redacted document aesthetic, surveillance camera feel, shadowy government buildings",
        "tags_base": ["Conspiracy", "HiddenHistory", "Declassified", "GovernmentSecrets", "TruthRevealed"],
    },
    "Mind-Blowing Science": {
        "description": "Counter-intuitive science, impossible-sounding facts, physics paradoxes, future tech",
        "visual_mood": "futuristic lab aesthetic, glowing experiments, particle effects, high-tech atmosphere",
        "tags_base": ["Science", "DidYouKnow", "MindBlown", "Facts", "Physics"],
    },
}

# ═══════════════════════════════════════════════════════════════════
# ██  TOPICS — 100+ unique topics per niche (1000+ total)          ██
# ═══════════════════════════════════════════════════════════════════

TOPICS = {
    "Dark Psychology": [
        {"topic": "The Door-in-the-Face Technique", "hook": "Ask for something outrageous first. When they say no, your real request seems tiny. They'll say yes almost every time.", "visual": "a shadowy figure extending a hand through a doorway toward a vulnerable person in dim light"},
        {"topic": "Why Silence Is a Weapon", "hook": "When someone wrongs you, the most powerful thing you can do is go completely silent. It drives them insane because humans are hardwired to fear social rejection.", "visual": "a person sitting alone in silence while another paces anxiously in a dark room, tension visible in the air"},
        {"topic": "The 48 Laws of Power: Law 1", "hook": "Never outshine the master. The moment you make your boss feel inferior, your days are numbered. History is full of brilliant people destroyed by this mistake.", "visual": "a chess board with a pawn standing taller than the king, dramatic side-lighting creating long shadows"},
        {"topic": "Why Narcissists Love-Bomb You", "hook": "That person who seemed perfect in the first two weeks wasn't falling in love with you. They were studying you. Every compliment was a data point.", "visual": "a smiling face with a dark shadow behind it revealing a manipulative expression, split lighting"},
        {"topic": "The Ben Franklin Effect", "hook": "Want someone to like you more? Don't do them a favor. Ask THEM for one. Their brain will rationalize that they must like you, or why would they help?", "visual": "two people exchanging a book, one looking surprised, warm but mysterious amber lighting"},
        {"topic": "Mirroring Body Language", "hook": "Copy someone's posture within 3 seconds and they'll unconsciously trust you 40% more. FBI negotiators use this in every hostage situation.", "visual": "two silhouettes facing each other in identical poses, backlit by cool blue light"},
        {"topic": "The Spotlight Effect", "hook": "You think everyone noticed your embarrassing moment? Studies prove that 90% of people around you didn't even register it happened. Your brain is lying to you.", "visual": "a person standing under a dramatic spotlight on a dark stage, looking self-conscious"},
        {"topic": "Why People Ghost You", "hook": "Ghosting isn't about you. It's a self-preservation instinct from someone too conflict-avoidant to handle the discomfort of honesty. Their silence says everything about them.", "visual": "a phone screen glowing in darkness showing unread messages, fog swirling around it"},
        {"topic": "The Halo Effect", "hook": "Attractive people get shorter prison sentences, higher salaries, and are assumed to be more intelligent. Your brain makes these judgments in under 100 milliseconds.", "visual": "a person's face with a subtle golden glow around their head, courtroom background blurred"},
        {"topic": "Dark Triad Personality", "hook": "Narcissism. Machiavellianism. Psychopathy. People with all three are rare, but they run billion-dollar companies and entire governments. Here is how to spot them.", "visual": "three dark masks arranged in a triangle on a velvet surface, each lit from a different angle"},
        {"topic": "Why Guilt-Tripping Works", "hook": "When someone says 'After everything I've done for you,' they're not reminding you of kindness. They're cashing in emotional debt they've been secretly tracking.", "visual": "a ledger book with emotional transactions listed, lit by a single candle in darkness"},
        {"topic": "The Sunk Cost Fallacy in Relationships", "hook": "You stay in bad relationships because your brain treats the years invested like money spent. But time already gone is never coming back, no matter how much more you give.", "visual": "an hourglass with sand running out, a couple's silhouette visible inside the glass"},
        {"topic": "Weaponized Incompetence", "hook": "They're not bad at doing the dishes. They do them badly on purpose so you'll stop asking. It's a strategy, not stupidity.", "visual": "a stack of poorly washed dishes with a smirking shadow in the background"},
        {"topic": "The Gray Rock Method", "hook": "To defeat a narcissist, become the most boring person alive. No reactions. No emotions. No supply. They'll move on because you're no longer fun to control.", "visual": "a person standing motionless like a gray stone statue while chaotic energy swirls around them"},
        {"topic": "Why Nice Guys Finish Last", "hook": "Being nice isn't the problem. Being nice to get something in return is manipulation disguised as kindness. People sense the transaction and it repels them.", "visual": "a mask of a smiling face being held up, revealing a calculating expression underneath"},
        {"topic": "Intermittent Reinforcement", "hook": "The most addictive relationships aren't consistently good. They alternate between heaven and hell. Your brain gets hooked on the unpredictability like a slot machine.", "visual": "a slot machine with relationship symbols showing mixed results, neon casino glow"},
        {"topic": "The Dunning-Kruger Effect", "hook": "The less you know about something, the more confident you feel about it. True experts are riddled with doubt. That's why the loudest person in the room is usually wrong.", "visual": "a graph showing confidence vs knowledge with a dramatic peak at low knowledge, dark academic setting"},
        {"topic": "Emotional Vampires", "hook": "Some people don't drain your energy on purpose. They genuinely don't realize that every conversation leaves you exhausted. But the result is the same.", "visual": "a person's shadow stretching unnaturally long, draining color from everything it touches"},
        {"topic": "The Foot-in-the-Door Technique", "hook": "First they ask you for a small favor. Then a bigger one. Then bigger. Before you know it, you've agreed to things you never would have said yes to originally.", "visual": "a door opening inch by inch, each crack revealing a larger demand written on the wall behind"},
        {"topic": "Why You Attract Toxic People", "hook": "If you're an empath, you don't attract toxic people by accident. Your compassion is their oxygen. They can smell your willingness to give from across a crowded room.", "visual": "a glowing warm figure surrounded by dark silhouettes reaching toward the light"},
        {"topic": "Cognitive Dissonance in Cults", "hook": "The more you sacrifice for a belief, the harder your brain fights to justify it. This is how cults keep members. The exit cost feels worse than staying.", "visual": "people walking in a circle inside a geometric structure, dramatic overhead lighting"},
        {"topic": "The Pygmalion Effect", "hook": "Teachers who believe their students are gifted produce gifted students, even when the kids were randomly selected. Your expectations literally reshape other people's reality.", "visual": "a teacher's silhouette casting a shadow that transforms into a larger, more powerful figure"},
        {"topic": "Why People Lie About Small Things", "hook": "Someone who lies about what they had for lunch will lie about anything. Casual dishonesty isn't harmless. It's practice for the big betrayals.", "visual": "a tiny lie represented as a small crack in glass that spreads across an entire window"},
        {"topic": "The Bystander Effect", "hook": "If you collapse in a crowd of 50 people, you're LESS likely to get help than if one person walks by. Everyone assumes someone else will act. Nobody does.", "visual": "a person lying on the ground while dozens of blurred figures walk past, each looking away"},
        {"topic": "Trauma Bonding Explained", "hook": "The person who hurts you and then comforts you isn't showing love. They're creating a chemical addiction in your brain. The relief after pain feels identical to love.", "visual": "a chain that transforms from thorns to flowers and back again, dramatic chiaroscuro lighting"},
        {"topic": "The Pratfall Effect", "hook": "Making a small, relatable mistake in public actually makes people like you MORE. Perfection is intimidating. Vulnerability is magnetic.", "visual": "a person tripping slightly and catching themselves while others smile warmly, soft golden light"},
        {"topic": "Gaslighting Red Flags", "hook": "If they say 'that never happened' about something you clearly remember, run. They're not forgetful. They're rewriting your reality to maintain control.", "visual": "a mirror showing a different scene than what's actually happening in the room, distorted edges"},
        {"topic": "Why You Can't Stop Scrolling", "hook": "Every scroll is a slot machine pull. Your brain releases micro-doses of dopamine not from finding content, but from the anticipation of what might be next.", "visual": "a phone screen as a slot machine with infinite scroll, person's face lit by blue screen glow"},
        {"topic": "The Zeigarnik Effect", "hook": "Your brain obsesses over unfinished tasks far more than completed ones. That ex you never got closure with? Your mind is stuck in a loop because the story never ended.", "visual": "an incomplete puzzle piece floating in darkness, the gap glowing with restless energy"},
        {"topic": "Social Proof Manipulation", "hook": "Fake reviews, paid followers, manufactured waitlists. When you see everyone wanting something, your brain shuts off critical thinking and follows the crowd.", "visual": "a crowd of identical silhouettes all pointing in one direction while one figure hesitates"},
        {"topic": "The Contrast Principle", "hook": "A $200 jacket seems expensive until you try on the $2000 one first. Real estate agents show you a terrible house before the one they want you to buy.", "visual": "two price tags side by side, the smaller one glowing as the larger one casts it in favorable shadow"},
        {"topic": "Why You Fear Rejection More Than Failure", "hook": "Your brain processes social rejection in the exact same area that processes physical pain. Being excluded literally hurts the same as being punched.", "visual": "a brain scan highlighting the pain center while a hand reaches out being pushed away"},
        {"topic": "Anchoring Bias", "hook": "The first number you see in a negotiation controls everything. Even if it's absurd, your brain clings to it. This is why car dealers put the sticker price so high.", "visual": "a heavy anchor attached to a number floating in dark water, dragging everything toward it"},
        {"topic": "The Backfire Effect", "hook": "Showing someone evidence against their beliefs doesn't change their mind. It makes them believe even harder. Facts are weapons that strengthen the walls you're trying to break.", "visual": "arrows hitting a shield and bouncing back stronger, the shield growing larger with each impact"},
        {"topic": "Strategic Vulnerability", "hook": "Powerful leaders share one carefully chosen weakness to appear relatable. But they never reveal true vulnerability. It's calculated authenticity, and it works every time.", "visual": "a suit of armor with one deliberate gap revealing warm human skin underneath, dramatic lighting"},
        {"topic": "The Peak-End Rule", "hook": "You don't remember experiences as they were. You remember the peak moment and the ending. This is why bad endings ruin great relationships in your memory.", "visual": "a timeline where only the highest and final points glow while everything else fades to gray"},
        {"topic": "Learned Helplessness", "hook": "If you punish someone no matter what they do, they stop trying entirely. Even when the cage door opens, they won't leave. This happens in jobs, relationships, and schools.", "visual": "an open cage door with a figure sitting inside, light streaming in but the person not moving"},
        {"topic": "The IKEA Effect", "hook": "You overvalue things you built yourself. That terrible shelf you assembled feels priceless because your effort is baked into it. Companies exploit this constantly.", "visual": "a wobbly handmade shelf displayed like museum art with a golden frame around it"},
        {"topic": "Reciprocity as a Trap", "hook": "When someone gives you an unsolicited gift, they're not being generous. They're placing an invisible debt on your shoulders. And they will collect.", "visual": "a gift box with barely visible strings attached, leading to puppet-master hands in the shadows"},
        {"topic": "The Power of the Pause", "hook": "When someone asks you a difficult question, wait 5 full seconds before answering. The silence forces them to fill the gap, often revealing information they didn't intend to share.", "visual": "a clock's second hand frozen mid-tick while two people face each other across a table in dim light"},
        {"topic": "Why You Self-Sabotage", "hook": "Your subconscious believes you deserve exactly the life you have. When something better arrives, it triggers deep anxiety because it doesn't match your internal story.", "visual": "a person reaching for a door labeled 'success' while their own shadow pulls them backward"},
        {"topic": "Cold Reading Techniques", "hook": "Psychics aren't reading your mind. They're reading your shoes, your posture, your wedding ring, and your micro-expressions. Then they feed it back to you as divine insight.", "visual": "a crystal ball reflecting mundane details like shoes and jewelry, not mystical visions"},
        {"topic": "The Paradox of Choice", "hook": "Give someone 24 options and they buy nothing. Give them 3 and they buy immediately. Freedom of choice is paralyzing. Limitation is liberating.", "visual": "a person overwhelmed by hundreds of floating doors while another calmly walks through one of three"},
        {"topic": "Why Complaining Is Addictive", "hook": "Every time you complain, your brain rewires to make future complaining easier. Neural pathways strengthen with repetition. Negativity is literally a habit your brain practices.", "visual": "neural pathways lighting up in a brain scan, growing thicker and brighter with each complaint pulse"},
        {"topic": "Triangulation in Relationships", "hook": "When a narcissist brings a third person into your relationship, they're not being honest. They're manufacturing jealousy to keep you competing for their attention.", "visual": "three figures arranged in a triangle, two in shadow competing while one in the center smirks"},
        {"topic": "The Scarcity Principle", "hook": "Limited time offer. Only 3 left in stock. Exclusive access. These phrases bypass your rational brain and trigger panic buying. You're not choosing. You're reacting.", "visual": "a countdown timer with 'LAST CHANCE' glowing red, hands reaching desperately from all directions"},
        {"topic": "Why You Overshare When Nervous", "hook": "Anxiety makes you talk to fill silence. But every unnecessary word you say gives the other person ammunition. The person who speaks less always holds more power.", "visual": "words floating out of a mouth like visible speech bubbles being caught by listening hands in shadow"},
        {"topic": "Projection as a Defense Mechanism", "hook": "When someone accuses you of being jealous, controlling, or dishonest for no reason, listen carefully. They're describing themselves and don't even know it.", "visual": "a person pointing accusingly at a mirror, but the reflection shows them doing exactly what they accuse"},
        {"topic": "The Decoy Effect", "hook": "Movie theaters sell three popcorn sizes. The medium exists only to make the large look like a deal. You were never supposed to buy the medium.", "visual": "three popcorn buckets with price tags, arrows showing how the medium pushes toward the large"},
        {"topic": "Why You Remember Insults Forever", "hook": "One insult sticks harder than a hundred compliments because your brain treats negative information as survival data. Evolution made forgetting criticism dangerous.", "visual": "a single dark word carved into stone while hundreds of golden compliments fade like dust in the wind"},
        {"topic": "The Chameleon Effect", "hook": "You unconsciously adopt the accent, posture, and mood of whoever you spend the most time with. Your personality isn't as fixed as you think. You're absorbing everyone around you.", "visual": "a figure that shifts colors and shape as different people walk past, like a human chameleon"},
        {"topic": "The 7-38-55 Rule", "hook": "Only 7% of communication is words. 38% is tone. And 55% is body language. You could say 'I love you' and someone would know you didn't mean it.", "visual": "a pie chart made of a human silhouette, with body language dominating and words as a tiny sliver"},
        {"topic": "Emotional Flooding", "hook": "When your heart rate exceeds 100 BPM during an argument, your brain literally shuts down rational thinking. You're not fighting with logic anymore. You're fighting with adrenaline.", "visual": "a heart rate monitor spiking while a brain's frontal lobe dims and darkens in real-time"},
        {"topic": "The Double Bind", "hook": "Manipulators give you two options, both bad. 'If you leave, you're selfish. If you stay, you agree with me.' There's always a third option they don't want you to see.", "visual": "two doors both leading to the same dark room, with a hidden third door barely visible in the wall"},
        {"topic": "Why First Impressions Stick", "hook": "You form a permanent judgment about someone in exactly 7 seconds. And it takes 20 positive interactions to override one bad first impression.", "visual": "a timer counting down from 7, a person's face slowly crystallizing into a permanent expression"},
        {"topic": "The Endowment Effect", "hook": "The moment you own something, you value it more than before you had it. This is why free trials work. Once it's 'yours,' giving it up feels like losing.", "visual": "a person clutching an object that glows gold in their hands but appears ordinary on the shelf"},
        {"topic": "Microexpression Reading", "hook": "A real smile involves the muscles around your eyes. A fake smile only uses the mouth. You can spot a liar in one-fifth of a second if you know where to look.", "visual": "a split-screen face: one side with genuine crinkling eyes, one side with only a mouth curve, forensic lighting"},
        {"topic": "Why People Betray Your Secrets", "hook": "Sharing secrets releases dopamine. The person you trusted didn't betray you out of malice. They betrayed you because keeping quiet was physically uncomfortable.", "visual": "a secret represented as glowing light escaping through cracks in a person's clasped hands"},
        {"topic": "The Barnum Effect", "hook": "Horoscopes work because they're vague enough to apply to anyone. 'You sometimes feel insecure' applies to every human alive. But your brain thinks it's speaking directly to you.", "visual": "a horoscope wheel with generic statements that morph to fit different people simultaneously"},
        {"topic": "Status Anxiety", "hook": "You don't actually want the luxury car. You want what you think other people will think of you when they see you in it. Most purchases are just expensive identity signals.", "visual": "a person looking at a luxury car, but their reflection shows them looking at the reactions of passersby"},
        {"topic": "The Illusion of Transparency", "hook": "You think your emotions are written all over your face. They're not. Studies show people are terrible at reading how you feel. Your inner turmoil is more invisible than you think.", "visual": "a calm exterior face with a turbulent storm visible only through translucent skull, dramatic x-ray effect"},
        {"topic": "Negativity Bias in Relationships", "hook": "It takes five positive interactions to neutralize the damage of one negative one. Every criticism costs you five compliments. Most people are permanently in emotional debt.", "visual": "a balance scale with one dark weight easily outweighing five golden ones, stark dramatic lighting"},
        {"topic": "Why You Hate Your Own Voice", "hook": "When you speak, sound travels through your skull bones, adding bass frequencies. Recordings remove that. You sound different to yourself than to everyone else. Always have.", "visual": "sound waves traveling two paths: one through a skull with rich bass, one through air without, split screen"},
        {"topic": "Dark Empathy", "hook": "Dark empaths are the most dangerous people alive. They understand your emotions perfectly but use that understanding to manipulate rather than comfort. They feel you and exploit it.", "visual": "a person with glowing empathic energy that wraps around another person like chains instead of a hug"},
        {"topic": "The FOMO Trap", "hook": "Fear of missing out isn't about wanting what others have. It's about the pain of imagining a version of your life that's better than the one you're living. The comparison is the poison.", "visual": "a person scrolling a phone while ghostly images of alternate lives float around them in mist"},
        {"topic": "Why Closure Doesn't Exist", "hook": "You'll never get the conversation that makes everything make sense. Closure is a myth your brain invented because it can't accept that some stories end mid-sentence.", "visual": "a book slammed shut mid-paragraph, the final words trailing off into darkness and silence"},
        {"topic": "The Mere Exposure Effect", "hook": "You don't fall in love with someone because they're special. You fall in love because you see them often. Familiarity tricks your brain into confusing recognition with affection.", "visual": "a face appearing repeatedly in a crowd until it starts glowing warmer with each appearance"},
        {"topic": "Reactive Devaluation", "hook": "If your enemy proposes a peace deal, your brain automatically assumes it's a trap, even if it's genuinely good. We reject good ideas just because the wrong person suggested them.", "visual": "a peace offer being examined under suspicious magnifying glass, with rejection stamps piling up"},
        {"topic": "The Illusion of Control", "hook": "You blow on dice before rolling. You press elevator buttons harder. You choose your lottery numbers. None of it changes the outcome. But the illusion keeps you sane.", "visual": "a person pressing an elevator button repeatedly while the floor numbers change randomly regardless"},
        {"topic": "Choice Supportive Bias", "hook": "After making a decision, your brain retroactively makes it seem better than it was. You don't remember your choice honestly. You remember the version that justifies staying committed.", "visual": "a decision tree where the chosen path glows golden while unchosen paths darken and shrink from memory"},
        {"topic": "Why Revenge Feels Empty", "hook": "Brain scans show that planning revenge activates reward centers. But executing it? Nothing. The anticipation was the high. The act itself is always hollow.", "visual": "a glowing brain with the reward center lit up during planning, then going dark at the moment of revenge"},
        {"topic": "The Focusing Illusion", "hook": "Nothing is as important as you think it is while you're thinking about it. Your salary, your breakup, your mistake. The moment you stop focusing on it, it shrinks.", "visual": "a magnifying glass making something appear enormous, but the actual object beneath is tiny"},
        {"topic": "Catastrophizing and Anxiety", "hook": "85% of the things you worry about never happen. And of the 15% that do, 79% were handled better than expected. Your anxiety is a false alarm system stuck on maximum.", "visual": "a fire alarm blaring red while the room behind it is perfectly calm and peaceful"},
        {"topic": "The Peak Performance Paradox", "hook": "Trying harder makes you perform worse under pressure. The best athletes describe peak performance as 'not thinking at all.' Your conscious mind is the bottleneck.", "visual": "an athlete running with a glowing brain that dims as their speed increases, paradox visual"},
        {"topic": "Why You Attract What You Fear", "hook": "Your brain scans for what you're afraid of 24/7. You don't attract negativity through magic. You notice it more because fear makes your attention filter for threats.", "visual": "a radar screen highlighting only red threats while ignoring green opportunities all around it"},
        {"topic": "Emotional Reasoning Fallacy", "hook": "You feel stupid, so you conclude you ARE stupid. You feel unlovable, so you act like it. Emotions aren't evidence. But your brain treats them as absolute truth.", "visual": "feelings in the shape of clouds forming solid walls that block a doorway labeled 'reality'"},
        {"topic": "The Paradox of Tolerance", "hook": "A society that tolerates everything will eventually be destroyed by the intolerant. Unlimited tolerance is self-defeating. Even open-mindedness needs boundaries.", "visual": "an open gate that grows wider until dark figures march through it unopposed"},
        {"topic": "Why People Follow Charismatic Leaders", "hook": "Charisma isn't about what you say. It's about how you make people feel about themselves. The most charismatic people in history made others feel chosen.", "visual": "a leader's shadow falling on followers, each shadow making them stand taller, warm dramatic light"},
        {"topic": "The Availability Heuristic", "hook": "You think plane crashes are common because you remember them. You think shark attacks are likely because they're dramatic. Your brain confuses memorable with frequent.", "visual": "a dramatic plane crash headline overshadowing tiny text reading 'car accident: 100x more likely'"},
        {"topic": "Psychological Reactance", "hook": "Tell someone they CAN'T do something and watch them immediately want to do it. Prohibition doesn't reduce desire. It manufactures obsession.", "visual": "a 'DO NOT ENTER' sign with a crowd pushing toward it, while an open door beside it is ignored"},
        {"topic": "The Uncanny Valley Effect", "hook": "Almost-human faces terrify you more than clearly inhuman ones. Your brain knows something is wrong but can't identify what. That gap between almost-right and right is pure horror.", "visual": "a nearly human face with subtle wrongness in the eyes, sitting in a dimly lit uncanny valley scene"},
        {"topic": "Confirmation Bias Blindspot", "hook": "You don't form opinions and then search for evidence. You search for evidence that supports what you already believe and ignore everything else. You're your own worst echo chamber.", "visual": "a person building a wall with bricks labeled 'agrees with me' while discarding ones labeled 'challenges me'"},
        {"topic": "Why Nostalgia Is a Lie", "hook": "The past wasn't better. Your brain filters out the pain and keeps the highlights. Nostalgia is a greatest-hits album of your life, not the full recording.", "visual": "a photo album where dark, painful pages are torn out and only golden-lit happy moments remain"},
        {"topic": "The Framing Effect", "hook": "90% survival rate and 10% mortality rate are the same statistic. But the first one makes you feel safe and the second terrifies you. Words shape reality.", "visual": "the same data presented in two different frames: one warm and reassuring, one cold and threatening"},
        {"topic": "Moral Licensing", "hook": "After doing something good, your brain gives you permission to do something bad. You donated to charity? Now you 'deserve' that impulse buy. Virtue creates its own loophole.", "visual": "a halo that transforms into devil horns after a good deed checkmark appears, seamless transition"},
        {"topic": "The Broken Window Theory", "hook": "One broken window in a building leads to every window being broken. Small signs of disorder signal that nobody cares, which invites total chaos.", "visual": "a single crack in a window spreading until the entire glass wall shatters in slow-motion sequence"},
        {"topic": "Fundamental Attribution Error", "hook": "When someone cuts you off in traffic, they're a terrible person. When YOU cut someone off, you had a good reason. You judge others by actions but yourself by intentions.", "visual": "a split screen: same driving mistake viewed as evil from one perspective and justified from the other"},
        {"topic": "The Hedonic Treadmill", "hook": "You get the promotion, the car, the house. You feel amazing for exactly 3 months. Then you're back to baseline. Happiness has a thermostat, and it always resets.", "visual": "a person running on a treadmill reaching for floating prizes that dissolve the moment they're touched"},
        {"topic": "Why Boredom Is Dangerous", "hook": "Boredom isn't harmless. Your brain in a bored state is more likely to make impulsive, destructive decisions because it's desperately seeking any stimulation at all.", "visual": "a brain with idle warning lights flickering, hands reaching toward risky choices that glow enticingly"},
        {"topic": "Covert Contracts", "hook": "You do nice things expecting something in return but never say it out loud. When they don't reciprocate, you feel betrayed. The problem? They never agreed to the deal.", "visual": "invisible contract papers floating between two people, one signing, the other completely unaware"},
        {"topic": "The Paradox of Vulnerability", "hook": "You admire vulnerability in others but fear showing it yourself. The trait you find most courageous in other people is the same one your brain labels as dangerous in you.", "visual": "a mirror where the reflection looks brave and open while the person in front wears full armor"},
        {"topic": "Group Polarization", "hook": "Put moderate people in a group and their opinions become extreme. Discussion doesn't create consensus. It amplifies whatever direction the group was already leaning.", "visual": "individual figures in neutral gray gradually turning bright red or blue as they cluster together"},
        {"topic": "The Curse of Knowledge", "hook": "Once you know something, you can't imagine not knowing it. This makes experts terrible teachers. They forget what confusion feels like.", "visual": "a teacher speaking in complex equations while a student sees only question marks floating in the air"},
        {"topic": "Status Quo Bias", "hook": "You don't stay in situations because they're good. You stay because change is terrifying. The familiar prison feels safer than the unknown freedom outside.", "visual": "a comfort zone drawn as a warm circle while a vast beautiful landscape lies just outside its edge"},
        {"topic": "The Isolation Experiment", "hook": "After 48 hours of total isolation, hallucinations begin. After 72 hours, you lose the ability to think clearly. Humans don't just want connection. We REQUIRE it to stay sane.", "visual": "a clock ticking in an empty white room, the walls slowly distorting as hours pass"},
        {"topic": "Normalization of Deviance", "hook": "The first time you skip a safety step and nothing bad happens, your brain files it as acceptable. Each time you skip it, the threshold moves. Until catastrophe arrives.", "visual": "warning signs being gradually ignored and dimming, one by one, until complete darkness"},
        {"topic": "The Affect Heuristic", "hook": "You don't evaluate risks logically. You evaluate them emotionally. Nuclear power feels scarier than coal plants, even though coal kills 400 times more people every year.", "visual": "a nuclear symbol glowing menacingly while a much larger coal smokestacks quietly emit death in the background"},
        {"topic": "Why People Stay in Bad Jobs", "hook": "It's not loyalty. It's identity. After years in a role, your job becomes who you ARE. Leaving feels like dying because you'd have to rebuild yourself from nothing.", "visual": "a person merged with their office desk, roots growing from their chair into the floor"},
        {"topic": "The Doorway Effect", "hook": "You walk into a room and forget why you went there. That's not aging. Walking through doorways literally triggers your brain to reset short-term memory. It happens at every age.", "visual": "a doorway acting as an eraser, wiping a thought bubble clean as a person walks through"},
        {"topic": "Deindividuation in Crowds", "hook": "Put on a mask, join a mob, and your moral compass vanishes. Anonymity doesn't reveal your true self. It removes the self entirely, leaving only impulse.", "visual": "a crowd of masked figures with their individual colors draining away into collective gray"},
        {"topic": "The Planning Fallacy", "hook": "Everything takes longer than you think. Studies show you underestimate task duration by 40% minimum. Even after being told about this bias, you STILL underestimate.", "visual": "a timeline stretching rubber-band style far beyond its original endpoint, calendar pages flying"},
        {"topic": "Why You Talk to Yourself", "hook": "Internal monologue burns 20% of your brain's daily energy. You process up to 70,000 thoughts a day. Your loudest conversation is the one nobody else can hear.", "visual": "a person's head with visible thought streams spiraling outward like galaxy arms, glowing with energy"},
        {"topic": "Moral Disengagement", "hook": "Good people do terrible things by relabeling them. It's not torture, it's 'enhanced interrogation.' It's not stealing, it's 'creative accounting.' Language is the first weapon of atrocity.", "visual": "dark actions being relabeled with clean, professional-sounding names on sticky notes, boardroom setting"},
        {"topic": "The Contrast Effect in Dating", "hook": "You seem more attractive standing next to someone less attractive. Bars, nightclubs, and dating apps all exploit this. You're not being chosen. You're being compared.", "visual": "a person appearing to glow brighter as the surrounding figures become dimmer, nightclub lighting"},
    ],

    "Body Science": [
        {"topic": "What Happens When You Die", "hook": "In the first 3 minutes after your heart stops, your brain releases a massive flood of DMT. Some scientists believe this is what causes near-death experiences.", "visual": "a body on a hospital bed with the brain glowing intensely in the final moments, ethereal light"},
        {"topic": "Your Stomach Acid Could Dissolve Metal", "hook": "Your stomach produces hydrochloric acid strong enough to dissolve a razor blade. The only reason it doesn't eat through you is a mucus lining that replaces itself every 3 days.", "visual": "a cross-section of a stomach with acid bubbling and dissolving a metal blade, dark clinical aesthetic"},
        {"topic": "You're Taller in the Morning", "hook": "Gravity compresses your spine throughout the day. By evening, you're up to 1 inch shorter than when you woke up. Astronauts in space grow up to 2 inches taller.", "visual": "a spine shown at morning height vs evening height, measurement lines visible, space station background"},
        {"topic": "Your Brain Eats Itself When Sleep-Deprived", "hook": "After 72 hours without sleep, your brain begins destroying its own cells. It's called astrocytic phagocytosis. Your brain literally digests itself to survive.", "visual": "a brain with small cells being consumed from the inside, dramatic medical visualization lighting"},
        {"topic": "Your Eyes Can See a Candle 30 Miles Away", "hook": "On a perfectly dark, clear night, the human eye can detect a single candle flame from 30 miles away. Your eyes are more sensitive than any camera ever built.", "visual": "a single candle flame in complete darkness, the glow reaching across an impossibly vast dark landscape"},
        {"topic": "You Produce Enough Saliva to Fill a Pool", "hook": "The average person produces 25,000 quarts of saliva in their lifetime. That's enough to fill two swimming pools. Your mouth is a factory that never stops.", "visual": "a swimming pool slowly filling with glistening liquid, measurement markers on the side, surreal aesthetic"},
        {"topic": "Your Bones Are Stronger Than Steel", "hook": "Pound for pound, human bone is stronger than steel. A cubic inch of bone can bear a load of 19,000 pounds. Your skeleton is an engineering marvel.", "visual": "a bone and a steel beam side by side under extreme pressure, the bone outlasting the steel"},
        {"topic": "What Happens If You Never Sleep Again", "hook": "Fatal familial insomnia is a real condition. Your brain slowly loses the ability to sleep. First hallucinations, then dementia, then death. All because you can't close your eyes.", "visual": "wide-open eyes staring at a clock in a dark room, the clock melting as reality distorts"},
        {"topic": "Your Body Glows in the Dark", "hook": "Human bodies emit visible light. It's 1,000 times weaker than what your eyes can detect, but it's real. You are literally bioluminescent. You just can't see it.", "visual": "a human figure in total darkness emitting a faint ethereal glow, infrared camera aesthetic"},
        {"topic": "What Happens If You Drink Seawater", "hook": "Seawater forces your kidneys to use more water to flush the salt than the water you drank. The more you drink, the faster you dehydrate. The ocean is poison disguised as salvation.", "visual": "a person drinking from the ocean while their cells visibly shrivel and dehydrate, split view"},
        {"topic": "Your Heart Beats 100,000 Times a Day", "hook": "Without rest, without a break, without a single day off, your heart beats approximately 100,000 times every 24 hours. Over a lifetime, that's 2.5 billion beats. It never pauses.", "visual": "a dramatic close-up of a beating heart with a counter ticking rapidly, lifetime number growing"},
        {"topic": "Why You Get Brain Freeze", "hook": "When cold hits the roof of your mouth, blood vessels rapidly constrict then dilate. Your brain interprets this sudden blood flow change as pain. It's a false alarm that genuinely hurts.", "visual": "a cross-section of a head showing blood vessels in the palate constricting and expanding violently"},
        {"topic": "You Shed 1.5 Million Skin Cells Per Hour", "hook": "Right now, as you watch this, you're shedding 30,000 dead skin cells every minute. Most household dust is actually you. You've left pieces of yourself everywhere you've ever been.", "visual": "skin cells floating away from a hand like tiny flakes of light, dust particles in a sunbeam"},
        {"topic": "What Happens When You Hold Your Breath", "hook": "After 2 minutes, CO2 builds up and triggers panic. After 5 minutes, brain cells start dying. After 10 minutes without oxygen, you are irreversibly brain dead.", "visual": "a timer counting up while a brain visualization shows cells dimming region by region"},
        {"topic": "Your DNA Could Stretch to Pluto", "hook": "If you uncoiled all the DNA in your body and laid it end to end, it would stretch from the Earth to Pluto and back. 17 times. All packed into cells smaller than a pinhead.", "visual": "a DNA helix unspooling from a cell and stretching across the solar system toward distant Pluto"},
        {"topic": "What 10G Force Does to Your Body", "hook": "At 10G, your blood pools in your legs. Your vision tunnels, then blacks out. Your organs shift downward. Fighter pilots have 7 seconds before they lose consciousness.", "visual": "a pilot's face distorting under extreme G-force, blood visibly pooling, cockpit instruments blurring"},
        {"topic": "Your Gut Has a Second Brain", "hook": "Your intestines contain 500 million neurons. They can operate completely independently from your brain. When people say 'trust your gut,' there's a literal neural network doing the thinking.", "visual": "the digestive system glowing with neural connections like a second brain, dark anatomical background"},
        {"topic": "Why Paper Cuts Hurt So Much", "hook": "Your fingertips have the highest density of pain receptors in your entire body. Paper cuts don't bleed enough to clot, so the nerve endings stay exposed to air. Maximum pain, minimum damage.", "visual": "a microscopic view of a paper cut with exposed nerve endings firing pain signals, clinical zoom"},
        {"topic": "What Happens If You Swallow a Battery", "hook": "A button battery lodged in your esophagus generates an electrical current that burns through tissue in 2 hours. It can create a hole in your throat. Smaller than a coin, deadlier than a knife.", "visual": "a small battery with electrical arcs emanating from it inside a body cross-section, alarm red glow"},
        {"topic": "Your Nose Can Smell 1 Trillion Scents", "hook": "Not thousands. Not millions. Your nose can distinguish approximately 1 trillion different smells. It's the most sophisticated chemical detection system on Earth.", "visual": "a nose with thousands of scent molecules floating toward it in different colors, dark lab setting"},
        {"topic": "What Happens at Absolute Zero", "hook": "At minus 459.67°F, atoms stop moving entirely. Life, chemistry, and physics as we know them cease to exist. We've gotten to within a billionth of a degree from it in labs.", "visual": "atoms frozen completely still in a crystalline lattice, frost spreading across the frame from a central point"},
        {"topic": "You Have Mites Living on Your Face", "hook": "Right now, microscopic Demodex mites are living inside your hair follicles and pores. They come out at night to mate on your face. Everyone has them. There is no cure.", "visual": "a microscopic view of face mites in hair follicles, horrifying detail with dark background"},
        {"topic": "Your Tears Have Different Compositions", "hook": "Tears of grief, tears of joy, and tears from onions have completely different chemical compositions when viewed under a microscope. Your body knows why you're crying.", "visual": "three tears under microscope showing dramatically different crystal patterns, labeled and backlit"},
        {"topic": "What Happens If You Never Shower", "hook": "After 2 weeks without bathing, bacteria colonies on your skin reach dangerous levels. After a month, infections set in. After a year, your skin begins forming a protective crust.", "visual": "a timeline of skin deterioration stages, clinical photography style with dramatic progression"},
        {"topic": "Your Brain Uses 20% of Your Energy", "hook": "Despite being only 2% of your body weight, your brain consumes 20% of your total energy. It's the most expensive organ to run. Thinking is exhausting because it literally burns calories.", "visual": "a brain glowing hot with energy consumption while the rest of the body is dimmer, thermal view"},
        {"topic": "Humans Can Survive in Space for 90 Seconds", "hook": "Without a suit, you wouldn't freeze or explode. You'd remain conscious for about 15 seconds as oxygen leaves your blood. Full recovery is possible within 90 seconds. After that, you're gone.", "visual": "an astronaut floating in space without a suit, a 90-second countdown overlaid, stars behind"},
        {"topic": "Your Body Replaces Itself Every 7 Years", "hook": "Almost every cell in your body is replaced over a 7-year cycle. The person you were 7 years ago has been entirely rebuilt. You're a ship of Theseus made of flesh.", "visual": "a human figure with cells being swapped out like pixels being replaced, time-lapse transformation"},
        {"topic": "What Happens When Lightning Strikes You", "hook": "Lightning is 5 times hotter than the surface of the sun. Survivors report that time slows down, their clothes explode off, and the entry and exit wounds form fractal burn patterns.", "visual": "Lichtenberg figure burn patterns on skin, branching like tree roots, dramatic medical photography"},
        {"topic": "You Can Survive Without a Stomach", "hook": "Surgeons can remove your entire stomach and connect your esophagus directly to your intestines. You can live a full life. You just have to eat 6 tiny meals a day forever.", "visual": "a medical diagram showing the digestive reroute after gastrectomy, clean clinical aesthetic"},
        {"topic": "Why Your Ears Ring in Silence", "hook": "In a perfectly silent room, you hear a ringing. Those are your hair cells in the inner ear firing spontaneously. Absolute silence doesn't exist. Your ears fill the void with their own signal.", "visual": "an ear cross-section with hair cells firing in a soundproof chamber, sound waves generating from nothing"},
        {"topic": "Your Blood Vessels Could Circle Earth 2.5 Times", "hook": "If laid end to end, your blood vessels would stretch 60,000 miles. That's enough to wrap around Earth two and a half times. All packed inside one human body.", "visual": "blood vessels unspooling from a body and wrapping around a globe, cosmic scale visualization"},
        {"topic": "What Happens During an Adrenaline Rush", "hook": "In a crisis, your adrenal glands flood your body with cortisol and adrenaline. Pain vanishes. Strength doubles. Time appears to slow. For 30 seconds, you become superhuman.", "visual": "a person lifting an impossible weight with glowing adrenal glands highlighted, time-frozen debris around them"},
        {"topic": "Your Liver Can Regenerate Itself", "hook": "Cut away 75% of your liver and it will grow back to full size within weeks. It's the only internal organ that can completely regenerate. The ancient Greeks knew this with the Prometheus myth.", "visual": "a liver growing back in time-lapse stages, regeneration glow, medical imaging aesthetic"},
        {"topic": "Why You Twitch When Falling Asleep", "hook": "As your muscles relax for sleep, your brain misinterprets the sensation as falling. It fires a jolt to 'catch' you. It's called a hypnic jerk, and it happens to 70% of people nightly.", "visual": "a person in bed with a jolt of electrical energy firing through their body, the moment of the jerk frozen"},
        {"topic": "What Would Happen If You Stopped Eating", "hook": "Day 1: hunger. Day 3: your body burns fat. Day 21: it starts consuming muscle. Day 40: organs begin to fail. Day 60: death. Your body has a systematic self-destruction sequence.", "visual": "a body timeline showing progressive deterioration stages, clinical measurement markers at each stage"},
        {"topic": "Your Pineal Gland Is a Tiny Eye", "hook": "Deep inside your brain sits the pineal gland. It detects light, regulates sleep, and in some reptiles, it has a lens and retina. Descartes called it the seat of the soul.", "visual": "a cross-section of a brain highlighting the pineal gland with a subtle eye-like glow emanating from it"},
        {"topic": "Phantom Limb Pain Is Real", "hook": "People who lose arms or legs feel genuine pain in limbs that no longer exist. Their brain still maps the missing limb. The pain is not imagined. It's neurologically real.", "visual": "a glowing outline of a missing limb where pain signals still fire, medical imaging overlay"},
        {"topic": "What Happens If You Eat Only One Food", "hook": "If you eat only chicken, you'll die from scurvy. Only potatoes? You'll survive longer but lose muscle. Only rabbit? 'Rabbit starvation' kills you because the meat has no fat.", "visual": "single food items on plates with deficiency warnings appearing like medical alerts around each"},
        {"topic": "Your Heartbeat Syncs With Music", "hook": "Your heart rate unconsciously adjusts to match the tempo of music you're listening to. Fast music speeds it up. Slow music calms it down. Music literally controls your pulse.", "visual": "a heart beating in sync with musical waveforms, the tempo line and heartbeat merging into one"},
        {"topic": "Why Yawning Is Contagious", "hook": "Contagious yawning is linked to empathy. Psychopaths yawn less when others do. Your brain mirrors the action because it's deeply connected to the emotional state of people around you.", "visual": "a chain reaction of yawning faces, empathy connections drawn as glowing lines between brains"},
        {"topic": "What Happens Inside a Black Hole", "hook": "If you fell into a black hole, gravity would stretch your body into a thin strand of atoms. Scientists call it spaghettification. Your feet would experience time differently than your head.", "visual": "a human figure being stretched toward a singularity, the body elongating into infinite thinness"},
        {"topic": "Your Appendix Isn't Useless", "hook": "Doctors called it vestigial for a century. Now we know your appendix stores beneficial gut bacteria and reboots your digestive system after illness. Evolution kept it for a reason.", "visual": "an appendix highlighted in the digestive system with beneficial bacteria cultures being released"},
        {"topic": "The Lethal Dose of Water", "hook": "Drinking 6 liters of water in 3 hours can kill you. It dilutes sodium in your blood until your brain swells. It's called hyponatremia, and it has killed marathon runners.", "visual": "water molecules flooding cells that swell and burst, medical visualization with warning indicators"},
        {"topic": "Why You Can't Tickle Yourself", "hook": "Your cerebellum predicts the sensation before it happens and cancels the surprise. Tickling requires unpredictability. Your brain is too smart to fall for its own trick.", "visual": "a brain with the cerebellum highlighted, blocking signals from the person's own fingers, schematic view"},
        {"topic": "What Happens After 40 Days Without Food", "hook": "Your body has eaten through all fat reserves. It turns to muscle. Your heart weakens because the heart IS muscle. Most starvation deaths aren't from hunger. They're cardiac arrest.", "visual": "a heart muscle thinning over time with a day counter, medical monitoring equipment in the background"},
        {"topic": "Your Eyes Process 36,000 Pieces of Info Per Hour", "hook": "Every single hour, your eyes send 36,000 bits of information to your brain. You consciously process less than 1%. The other 99% shapes your gut feelings and instincts.", "visual": "eyes with streams of data flowing in, most filtering away into the subconscious, only a tiny stream reaching awareness"},
        {"topic": "Humans Share 60% DNA With Bananas", "hook": "You share 60% of your DNA with a banana, 80% with a cow, and 98.7% with a chimpanzee. The genetic recipe for life reuses the same ingredients across all living things.", "visual": "DNA strands from human, banana, and chimp side by side with matching sections highlighted in color"},
        {"topic": "What Happens When You Drown", "hook": "Drowning is silent. There's no splashing, no screaming. The body enters an involuntary response where the throat locks shut. Victims can be struggling 5 feet away and nobody notices.", "visual": "a person underwater with their throat visibly constricted, surface visible above showing a calm scene"},
        {"topic": "Your Body Has Enough Iron for a Nail", "hook": "The iron in your blood, if extracted and forged, would make a single 3-inch nail. Not enough to build anything, but enough to carry oxygen to every cell keeping you alive.", "visual": "iron atoms being extracted from blood cells and forming into a single nail, forge glow aesthetic"},
        {"topic": "Why Anesthesia Is Still a Mystery", "hook": "We've used anesthesia for over 170 years, but we still don't fully understand HOW it works. We know it makes you unconscious. We just can't explain the mechanism. And we use it millions of times a year.", "visual": "a patient going under anesthesia with the brain's consciousness fading to black, question marks floating"},
    ],

    "Historical What If": [
        {"topic": "What If Rome Never Fell", "hook": "The Roman Empire at its peak controlled 70 million people. If it never collapsed, we might have had the Industrial Revolution 800 years earlier. Modern technology by the year 1000.", "visual": "a Roman city with modern skyscrapers blending into ancient architecture, steam engines next to aqueducts"},
        {"topic": "What If The Library of Alexandria Survived", "hook": "The Library of Alexandria held 400,000 scrolls of ancient knowledge. When it burned, we lost centuries of scientific progress. Some historians believe we lost the cure for diseases we still can't treat.", "visual": "a vast ancient library with scrolls stretching to the ceiling, some scrolls glowing with lost knowledge"},
        {"topic": "What If Smartphones Existed in 1800", "hook": "Napoleon with Google Maps. Abraham Lincoln with Twitter. The entire course of warfare, politics, and revolution rewritten by a device that fits in your pocket.", "visual": "Napoleon looking at a glowing smartphone on a battlefield, maps and strategy overlaid on the screen"},
        {"topic": "What If Dinosaurs Never Went Extinct", "hook": "65 million years more evolution. Some paleontologists theorize that Troodon, with its large brain, was on track to develop human-level intelligence. We might be sharing the planet with raptor people.", "visual": "an evolved intelligent dinosaur-humanoid standing in a modern city, briefcase in hand, surreal mashup"},
        {"topic": "What If Hitler Had Been Accepted to Art School", "hook": "In 1907, the Vienna Academy of Fine Arts rejected a young applicant named Adolf Hitler. Twice. If he'd been accepted, 75 million people might not have died.", "visual": "a painting easel in a Vienna studio with an alternate timeline branching from the rejection letter"},
        {"topic": "What If The Internet Was Invented in 1900", "hook": "Telegraphs could send messages at the speed of light. If someone had built a network 70 years earlier, World War 1 might have been prevented by real-time global communication.", "visual": "Victorian-era people using glowing computer terminals connected by telegraph wires, steampunk internet"},
        {"topic": "What If Humans Had Never Discovered Fire", "hook": "Without fire, we couldn't cook meat. Without cooked meat, our brains couldn't grow. Without bigger brains, no language, no tools, no civilization. Fire didn't help us survive. It made us human.", "visual": "two evolutionary paths splitting: one with fire leading to cities, one without leading to primitive existence"},
        {"topic": "What If The Black Death Killed Everyone", "hook": "The Black Death killed 60% of Europe. If it had killed 100%, the Renaissance never happens. No Columbus, no America, no Industrial Revolution. The modern world simply doesn't exist.", "visual": "an empty European city with nature reclaiming the streets, no human presence, abandoned cathedrals"},
        {"topic": "What If Egypt Discovered Gunpowder First", "hook": "China invented gunpowder in the 9th century. If ancient Egypt had it 3,000 years earlier, the Pharaohs would have been unstoppable. The entire ancient world would have been Egyptian.", "visual": "Egyptian soldiers with primitive cannons laying siege to ancient cities, pyramids with smoke trails"},
        {"topic": "What If Gravity Was Twice as Strong", "hook": "Trees would be half as tall. Humans would be shorter and stockier. Aircraft would be impossible. Mountains would crumble under their own weight. The entire surface of Earth would be flattened.", "visual": "a compressed Earth landscape with short trees, squat buildings, and a heavy atmosphere pressing down"},
        {"topic": "What If Columbus Landed in Japan Instead", "hook": "Columbus thought he was heading to Asia. If the Americas didn't exist, his ships would have reached Japan. The Samurai vs. Spanish Conquistadors. History's greatest culture clash.", "visual": "Spanish galleons arriving at a Japanese port, samurai warriors watching from the shore, dramatic sunset"},
        {"topic": "What If Women Had Always Had Equal Rights", "hook": "Half the world's intellectual talent was suppressed for millennia. If women had always had access to education and power, we might have cured cancer by 1800. We'll never know what we lost.", "visual": "ancient female scholars, generals, and inventors working alongside men, civilization advancing twice as fast"},
        {"topic": "What If The Moon Didn't Exist", "hook": "No moon means no tides. Without tides, life may never have crawled from the oceans. Earth's axis would wobble chaotically, causing extreme climate swings. The moon isn't just pretty. It's essential.", "visual": "Earth without a moon, chaotic weather patterns visible from space, oceans still and lifeless"},
        {"topic": "What If Tesla Had Won the Energy War", "hook": "Nikola Tesla wanted to give the world free wireless electricity. JP Morgan shut him down because you can't meter free power. If Tesla won, every home on Earth would have free energy today.", "visual": "Tesla's Wardenclyffe Tower broadcasting electricity wirelessly to glowing cities, versus dark corporate towers"},
        {"topic": "What If Neanderthals Survived", "hook": "Neanderthals had larger brains than us. They made art, buried their dead, and may have spoken. If they survived, we'd share Earth with another intelligent human species. How would we treat them?", "visual": "a Neanderthal and modern human standing side by side in a contemporary city, both in modern clothes"},
        {"topic": "What If The Titanic Never Sank", "hook": "The Titanic's sinking led to international ice patrol, mandatory lifeboat requirements, and radio distress protocols. Without the disaster, maritime safety laws might have taken decades longer. Thousands more would have died.", "visual": "the Titanic arriving safely in New York harbor, but a shadow showing all the safety laws that never get written"},
        {"topic": "What If Alexander the Great Lived Longer", "hook": "Alexander died at 32 having conquered everything from Greece to India. He was planning to invade Arabia and North Africa. If he'd lived to 60, the entire known world would have been one empire.", "visual": "a map showing Alexander's actual conquests next to a glowing expanded empire covering all continents"},
        {"topic": "What If America Lost the Revolution", "hook": "The United States was one battle away from never existing. If Washington lost at Trenton, America stays British. No Constitution. No Bill of Rights. Democracy delayed by a century.", "visual": "the American flag slowly fading into a British colonial flag, Washington's troops retreating in the snow"},
        {"topic": "What If The Asteroid Missed Earth", "hook": "65 million years ago, a 6-mile asteroid hit the Yucatan Peninsula. If it had arrived 30 minutes earlier or later, it would have hit ocean instead of land. Dinosaurs would still rule.", "visual": "an asteroid streaking past Earth narrowly, dinosaurs looking up unharmed, timeline branching"},
        {"topic": "What If We Never Invented Writing", "hook": "Without writing, there's no recorded law, no contracts, no accumulated knowledge across generations. Every innovation would die with its inventor. Humanity would be permanently stuck in the Bronze Age.", "visual": "a world without written records, knowledge being passed only by voice, ideas dissolving like smoke"},
        {"topic": "What If The Mongols Conquered Europe", "hook": "The Mongol army retreated from Europe in 1242 only because their Khan died. If they'd continued, European feudalism would have been obliterated. The Renaissance might never have happened.", "visual": "Mongol cavalry riding through Paris, Notre Dame in the background, European knights overwhelmed"},
        {"topic": "What If JFK Was Never Assassinated", "hook": "Kennedy was planning to pull troops from Vietnam. If he lived, the Vietnam War may have ended before it began. 58,000 Americans and 2 million Vietnamese might never have died.", "visual": "JFK in the motorcade waving, the timeline splitting: one dark path to war, one bright path to peace"},
        {"topic": "What If Earth Had Rings Like Saturn", "hook": "If Earth had Saturn-like rings, every culture would have worshipped them. Navigation would be different. Satellite launches would be impossible. And every sunset would look like a painting.", "visual": "Earth's rings visible from a city skyline at sunset, casting dramatic shadows across the landscape"},
        {"topic": "What If Penicillin Was Never Discovered", "hook": "Before antibiotics, a scratch could kill you. Pneumonia was a death sentence. Surgery was gambling with your life. Alexander Fleming's accidental discovery saved an estimated 200 million lives.", "visual": "a hospital scene split in two: one side bright with modern medicine, one side dark and desperate without antibiotics"},
        {"topic": "What If The South Won the Civil War", "hook": "Slavery would have persisted well into the 1900s. The Confederate States would be a separate nation. Two Americas, forever divided. The ripple effects would reshape the entire 20th century.", "visual": "a divided map of North America with two separate flags, a wall running through the middle"},
        {"topic": "What If Nuclear Weapons Were Never Invented", "hook": "No Hiroshima. No Cold War. No mutually assured destruction. But also, no nuclear deterrent. Would World War 3 have already happened without the fear of total annihilation keeping us in check?", "visual": "a world map without nuclear weapons, but with conventional war fronts spreading across multiple continents"},
        {"topic": "What If The Plague Never Reached Europe", "hook": "The Black Death killed so many workers that survivors demanded higher wages. This broke feudalism and birthed the middle class. Without the plague, serfdom might have lasted until the 1800s.", "visual": "medieval workers negotiating with lords, the balance of power shifting, coin purses being exchanged"},
        {"topic": "What If Cleopatra Won the Battle of Actium", "hook": "If Cleopatra and Mark Antony had defeated Octavian, Rome would have become an Egyptian-influenced empire. The capital might have moved to Alexandria. Western civilization would look entirely different.", "visual": "Alexandria as the capital of a Rome-Egypt hybrid empire, obelisks next to Roman columns, golden age"},
        {"topic": "What If Oil Was Never Discovered", "hook": "No gasoline, no plastics, no modern agriculture. The world population would be under 2 billion. Cities would run on coal and wood. The 20th century would have looked like the 19th.", "visual": "a modern city reverting to steam power, horse-drawn carriages on highways, a world without petroleum"},
        {"topic": "What If Genghis Khan Was Never Born", "hook": "Genghis Khan killed 40 million people, roughly 10% of the world's population. His empire connected East and West, creating the Silk Road. Without him, globalization might have been delayed by 500 years.", "visual": "the Silk Road vanishing from a map, East and West sitting in isolated darkness without connection"},
        {"topic": "What If We Discovered Aliens in 1950", "hook": "Contact during the Cold War could have united humanity against a common external threat, or it could have triggered nuclear panic. First contact at the wrong time might have ended us.", "visual": "a 1950s radio telescope receiving an alien signal, military and scientists arguing about how to respond"},
        {"topic": "What If Photography Existed in Ancient Times", "hook": "We've never seen the real face of Jesus, Cleopatra, or Julius Caesar. If photography existed 2,000 years ago, every historical debate about appearance and events would be settled forever.", "visual": "ancient photo albums with real portraits of historical figures, sitting in a dusty archaeological dig"},
        {"topic": "What If Electricity Was Discovered in Medieval Times", "hook": "Lightning was seen as divine punishment. If a medieval scientist had harnessed it, the Church would have called it witchcraft. Progress versus persecution. The scientist would have been burned alive.", "visual": "a medieval lab with sparking electrical equipment, monks watching in horror from the doorway"},
        {"topic": "What If The Spanish Flu Had a 50% Death Rate", "hook": "The 1918 flu killed 50 million with a 2.5% death rate. At 50%, it would have killed a BILLION people. World War 1 would have ended not from armistice, but from running out of soldiers.", "visual": "empty trenches and abandoned cities, a world depopulated, factories silent and overgrown"},
        {"topic": "What If Humans Could Photosynthesize", "hook": "If our skin could convert sunlight to energy like plants, we'd never need to farm. No agriculture means no settling, no cities, no civilization as we know it. We'd be nomadic sun-eaters.", "visual": "humans with green-tinged skin standing in sunlight, absorbing energy, no farms or buildings in sight"},
        {"topic": "What If The Cold War Went Hot", "hook": "In 1983, Soviet officer Stanislav Petrov single-handedly prevented nuclear war by ignoring a false alarm. If he'd followed protocol, 100 million people would have died in the first hour.", "visual": "a Soviet missile control room with alarm lights flashing, one hand hovering over the launch button"},
        {"topic": "What If The Printing Press Was Never Invented", "hook": "No mass-produced books means no Protestant Reformation, no Enlightenment, no democracy. Knowledge stays locked in monasteries. The world remains medieval. All because of one machine.", "visual": "a monk hand-copying a book while outside the window, progress stands frozen in a medieval landscape"},
        {"topic": "What If Mars Had Oceans", "hook": "Mars once had liquid water. If it had maintained its atmosphere and kept its oceans, life might have evolved there independently. We could be looking at an alien civilization just next door.", "visual": "Mars with blue oceans and green continents, cities visible on the surface, viewed from Earth orbit"},
        {"topic": "What If The Ottoman Empire Never Fell", "hook": "The Ottoman Empire lasted 600 years. If it survived World War 1, the Middle East would never have been carved up by European powers. No arbitrary borders means no century of conflict.", "visual": "a stable Ottoman map overlaid on the modern Middle East, borders untouched, cities thriving"},
        {"topic": "What If Humans Were Immortal", "hook": "No death means no urgency. No urgency means no progress. If we lived forever, would we innovate faster, or would we procrastinate for eternity?", "visual": "an immortal figure sitting unchanged while the world around them shifts through centuries of change"},
    ],

    "Scary & Creepy": [
        {"topic": "The Russian Sleep Experiment", "hook": "In 1940, Soviet researchers kept 5 prisoners awake for 15 days using gas. By day 9, they were screaming. By day 15, they had torn their own flesh. What they said when the gas stopped will haunt you.", "visual": "a dark Soviet laboratory with five observation windows, dim green gas visible, scratches on glass"},
        {"topic": "Why You Should Never Answer 'Who's There'", "hook": "Home intruders have admitted in interviews that knocking first is a test. If nobody answers, they break in. If someone does, they use a cover story. Either way, they were always coming in.", "visual": "a dark hallway with a door at the end, a shadow visible through the peephole, eerie silence"},
        {"topic": "The Smiling Man", "hook": "A man walking alone at 2 AM sees a figure on the sidewalk. Dancing. Grinning. Getting closer. When their eyes meet, the figure starts sprinting toward him. The grin never changes.", "visual": "a distant figure with an unnaturally wide smile illuminated by a single streetlight on a deserted street"},
        {"topic": "Corpse Flowers Smell Like Death for a Reason", "hook": "The corpse flower evolved to smell like rotting flesh to attract carrion beetles. But here's the disturbing part: it only blooms once every 7-10 years, and it times the bloom perfectly.", "visual": "a massive corpse flower blooming in darkness, flies and beetles swarming, mist rising from the petals"},
        {"topic": "The Last Photo Ever Taken", "hook": "Dozens of missing persons cases have been solved by finding the last photo on the victim's camera. In some cases, someone else is in the background. Watching. And they were never identified.", "visual": "a camera screen showing a selfie with a blurred figure standing in the dark trees behind the subject"},
        {"topic": "The Dyatlov Pass Incident", "hook": "9 experienced hikers died in the Ural Mountains in 1959. They cut their tent open from the inside and ran barefoot into minus 30°C temperatures. One had her tongue removed. No animal did this.", "visual": "a torn tent on a snowy mountain slope at night, barefoot tracks leading away into darkness and storm"},
        {"topic": "Why Do We Check Behind the Shower Curtain", "hook": "The instinct to check behind the shower curtain is hardwired into your brain. It's the same survival mechanism that made our ancestors check caves before entering. Your brain knows something could be hiding.", "visual": "a hand reaching for a shower curtain in a dim bathroom, a shadow barely visible behind it"},
        {"topic": "The Hinterkaifeck Murders", "hook": "In 1922, a German family was murdered one by one with a pickaxe. The killer then lived in their house for 3 days, feeding the livestock and eating their food. They were never caught.", "visual": "an old German farmhouse at twilight, a single window lit from inside, footprints in the snow leading only in"},
        {"topic": "Sleep Paralysis Demons Are Universal", "hook": "Every culture on Earth has independently reported the same experience: waking up unable to move while a dark figure sits on your chest. Same entity. Different names. Across thousands of years.", "visual": "a dark shadowy figure sitting on a paralyzed person's chest in bed, the person's eyes wide with terror"},
        {"topic": "The Elevator Game", "hook": "Press the floors in a specific sequence: 4, 2, 6, 2, 10, 5. On the 5th floor, a woman enters. Don't look at her. Don't speak. If the elevator goes up instead of down, you've crossed over.", "visual": "an elevator interior with floor buttons glowing in a specific sequence, a shadowy female figure entering"},
        {"topic": "Bodies on Mount Everest Are Used as Landmarks", "hook": "Over 300 bodies remain on Everest because they're impossible to retrieve. Climbers use them as waypoints. 'Turn left at Green Boots.' That's a real person who died in 1996. Still there.", "visual": "a frozen body in climbing gear on a snowy ledge, other climbers walking past in the distance"},
        {"topic": "The Uncanny Valley of AI Voices", "hook": "AI voices are getting so close to human that your brain can't tell the difference, but something feels wrong. That discomfort you feel? It's your survival instinct screaming that something isn't real.", "visual": "an AI waveform that looks almost human, with subtle distortions that make it feel deeply unsettling"},
        {"topic": "What Lives at the Bottom of the Ocean", "hook": "We've explored less than 5% of the ocean floor. The deepest point is 36,000 feet. We've found creatures there that can survive pressure that would crush a submarine. What else is down there?", "visual": "a deep ocean trench descending into pitch blackness, bioluminescent creatures at impossible depths"},
        {"topic": "The Cecil Hotel Death", "hook": "Elisa Lam was found dead in a hotel water tank. The elevator footage shows her pressing all buttons, hiding from something invisible, and making gestures to something in the hallway. No one else was there.", "visual": "an elevator camera view showing a woman pressing buttons frantically, the hallway beyond empty and dark"},
        {"topic": "Your House Settles at Night", "hook": "Those creaking sounds at 3 AM? Temperature changes cause wood to contract. But your brain can't tell the difference between settling and footsteps. So it assumes the worst. Every single night.", "visual": "a dark hallway at night with creaking floorboards, the sound waves visualized as moving closer"},
        {"topic": "Cotard's Delusion", "hook": "There's a psychiatric condition where you genuinely believe you're dead. Patients report that they've died and are rotting. They stop eating because dead people don't need food. They can smell their own decay.", "visual": "a person looking in a mirror but seeing a decaying version of themselves staring back, clinical horror"},
        {"topic": "The Disappearance of the Sodder Children", "hook": "On Christmas Eve 1945, the Sodder house caught fire. 5 of 10 children vanished. No bones were found. No remains. Decades later, one child may have been spotted alive. The fire was set.", "visual": "a burning house on Christmas Eve with 5 silhouettes of children fading into the smoke and darkness"},
        {"topic": "Fatal Familial Insomnia", "hook": "There's a hereditary disease where you slowly lose the ability to sleep. First insomnia, then hallucinations, then dementia, then death. There is no treatment. And it's passed through families.", "visual": "a person lying in bed with wide-open eyes, a clock accelerating, their features deteriorating over months"},
        {"topic": "The Number Station Phenomenon", "hook": "Since the Cold War, radio stations have broadcast nothing but sequences of numbers. No one has claimed them. No government acknowledges them. They're still broadcasting today. To someone.", "visual": "an old radio in a dark room picking up number sequences, the numbers floating as visible text in the air"},
        {"topic": "Spontaneous Human Combustion", "hook": "Over 200 cases of people bursting into flames with no external ignition source. The fire is intense enough to reduce bones to ash, but the chair they're sitting in barely scorches.", "visual": "a living room with an unburned chair and a pile of ash where a person sat, forensic photography style"},
        {"topic": "The Bunny Man Legend", "hook": "In 1970, two separate witnesses reported a man in a bunny suit attacking their cars with an axe in Fairfax, Virginia. Police investigated. The man was never found. The reports were filed as genuine.", "visual": "a dark underpass at night with a distant figure in a rabbit costume holding an axe, single streetlight"},
        {"topic": "The Taos Hum", "hook": "Since the 1990s, residents of Taos, New Mexico have reported hearing a persistent low-frequency hum. Equipment can't detect it. Not everyone hears it. Those who do say it never stops.", "visual": "a person covering their ears in a silent desert landscape, sound waves emanating from underground"},
        {"topic": "Capgras Delusion", "hook": "Imagine waking up and being 100% convinced that your spouse has been replaced by an identical impostor. You know it's their face. But your brain screams that it's not them. This is a real condition.", "visual": "a person staring at their partner's face which subtly distorts and shifts, uncanny valley close-up"},
        {"topic": "The Isdal Woman", "hook": "In 1970, a burned body was found in Norway's Ice Valley. All clothing labels were removed. Her fingerprints were sanded off. She had 9 different fake IDs. She has never been identified.", "visual": "scattered fake passports with different names but the same blacked-out face, case file aesthetic"},
        {"topic": "Why Mirrors Are Covered After Death", "hook": "In dozens of cultures worldwide, mirrors are covered when someone dies. The belief? The soul of the deceased might become trapped in the reflection. Some say they've seen faces that weren't there.", "visual": "a covered mirror in a dim room, a faint handprint visible on the fabric from the other side"},
        {"topic": "The Lead Masks Case", "hook": "In 1966, two electrical engineers were found dead on a hilltop in Brazil, wearing crude lead eye masks. A notebook beside them read: 'Ingest capsules at 6:30. Await the agreed signal.'", "visual": "two figures lying on a hilltop wearing lead masks, a notebook between them, twilight sky above"},
        {"topic": "Prions: The Unstoppable Disease", "hook": "Prions aren't bacteria, viruses, or fungi. They're misfolded proteins that convert healthy proteins into copies of themselves. You can't kill them with heat, radiation, or chemicals. There is no cure.", "visual": "a protein folding incorrectly, then converting neighboring proteins in a chain reaction, molecular horror"},
        {"topic": "The Overtoun Bridge Dogs", "hook": "Since the 1950s, hundreds of dogs have leaped from the same spot on Overtoun Bridge in Scotland. Always from the same side. Always in dry weather. Over 50 have died. No one knows why.", "visual": "a misty stone bridge in Scotland, a single dog standing at the edge looking down, foggy atmosphere"},
        {"topic": "The Phantom Barber of Mississippi", "hook": "In 1942, someone broke into homes in Pascagoula, Mississippi. They didn't steal anything. They didn't hurt anyone. They cut locks of hair from sleeping people. And vanished without a trace.", "visual": "a dark bedroom with scissors on the nightstand and a lock of hair missing from a sleeping person"},
        {"topic": "Rat Kings Are Real", "hook": "A rat king is a cluster of rats whose tails have become tangled and fused together with blood and filth. They move as one horrifying mass. They've been documented since the 1500s. They still occur.", "visual": "a dark medieval cellar with a writhing mass of tangled rats, their tails knotted, candlelight flickering"},
        {"topic": "The Wow Signal", "hook": "On August 15, 1977, a radio telescope detected a 72-second signal from deep space that was 30 times louder than background noise. It matched no known natural source. It never repeated. Ever.", "visual": "a printout with 'Wow!' written next to a spike in data, the telescope pointed at empty space, night sky"},
        {"topic": "People Who Disappeared Inside Their Own Homes", "hook": "In 2009, a man vanished from inside his locked apartment. Windows sealed. Door locked from the inside. No signs of a struggle. His coffee was still warm. He was never found.", "visual": "a locked apartment with a warm cup of coffee on the table, the chair pushed back as if someone just stood up"},
        {"topic": "The Curse of the Crying Boy Painting", "hook": "In the 1980s, firefighters across England noticed that after house fires, one painting always survived: The Crying Boy. It happened so many times that a national newspaper organized a mass burning.", "visual": "a charred living room with everything destroyed except a single painting of a crying boy, untouched"},
        {"topic": "Alien Hand Syndrome", "hook": "Your hand moves on its own. It grabs things you didn't reach for. It unbuttons shirts you just buttoned. Your brain has lost control of one limb, and it now has its own agenda.", "visual": "a person's hand moving independently, reaching for objects while the person's face shows confusion and fear"},
        {"topic": "The Toynbee Tiles", "hook": "Since the 1980s, mysterious tiles with the message 'Toynbee Idea: Resurrect Dead on Planet Jupiter' have appeared embedded in asphalt across major US cities. Nobody knows who places them or how.", "visual": "a mysterious tile embedded in street asphalt with cryptic text, urban nighttime setting, rain-slicked roads"},
        {"topic": "Cordyceps: The Zombie Fungus", "hook": "This fungus invades ant brains, controls their behavior, forces them to climb to the perfect height, and then erupts from their skull to spread spores. It's real. Scientists worry it could evolve.", "visual": "an ant with a fungal stalk erupting from its head, climbing a leaf unnaturally, macro horror photography"},
        {"topic": "The Flannan Isles Lighthouse", "hook": "In 1900, three lighthouse keepers vanished from a remote Scottish island. The clock had stopped. A meal was half-eaten. The front door was locked from the outside. No bodies were ever found.", "visual": "a lighthouse beam sweeping across a stormy sea, the interior showing an abandoned half-eaten meal"},
        {"topic": "Why Are We Afraid of the Dark", "hook": "Fear of darkness isn't learned. It's hardwired. For 300,000 years, darkness meant predators you couldn't see. Your ancient brain still operates as if a lion might be lurking three feet away.", "visual": "a pair of predator eyes glowing in absolute darkness, just visible enough to trigger primal fear"},
        {"topic": "The Silence of Space", "hook": "In space, no one can hear you scream. Not because there's no air, but because sound requires molecules to travel through. The universe is the most silent place that will ever exist. Forever.", "visual": "an astronaut opening their mouth to scream in the void of space, sound waves that visibly die instantly"},
        {"topic": "Walking Corpse Syndrome", "hook": "Some brain injury patients wake up and calmly announce they've been dead for years. They describe watching their own funeral. Their conviction is absolute. They'll argue their death is a medical fact.", "visual": "a patient calmly sitting in a hospital bed describing their own death while monitors show normal vitals"},
    ],

    "Space & Cosmos": [
        {"topic": "The Size of the Observable Universe", "hook": "The observable universe is 93 billion light-years across. Light from the edge has been traveling since the beginning of time and still hasn't finished arriving. And beyond that edge? We will never know.", "visual": "a zoom-out from Earth through the solar system, galaxy, and into the observable universe, scale increasing"},
        {"topic": "A Day on Venus Is Longer Than a Year", "hook": "Venus takes 243 Earth days to rotate once, but only 225 days to orbit the sun. A single day on Venus is literally longer than its entire year. Time works differently there.", "visual": "Venus spinning in slow-motion while orbiting the sun faster, day/night cycles dramatically different"},
        {"topic": "The Boötes Void", "hook": "There's a region of space 330 million light-years across that contains almost nothing. 2,000 galaxies should be there. Only 60 exist. It's the largest known void in the universe. Something cleared it out.", "visual": "a vast black void in space surrounded by galaxy clusters, the emptiness dramatically larger than anything around it"},
        {"topic": "Neutron Stars Weigh 1 Billion Tons Per Teaspoon", "hook": "A neutron star is so dense that a single teaspoon of its material weighs 6 billion tons. It spins up to 716 times per second. It's a dead star that refuses to be nothing.", "visual": "a teaspoon next to a neutron star with an absurd weight reading, the star spinning as a blur"},
        {"topic": "The Sun Will Swallow Earth", "hook": "In 5 billion years, our sun will exhaust its hydrogen fuel and expand into a red giant. It will consume Mercury, Venus, and Earth. Our planet will be vaporized inside a dying star.", "visual": "the Sun expanding slowly to engulf Earth, the planet's oceans boiling away as the red giant approaches"},
        {"topic": "There Are More Stars Than Grains of Sand", "hook": "There are roughly 200 billion trillion stars in the observable universe. That's more than every grain of sand on every beach on Earth combined. And each one could have planets.", "visual": "a handful of sand dissolving into a star field, each grain becoming a glowing star, infinite scale"},
        {"topic": "The Coldest Place in the Universe", "hook": "The Boomerang Nebula is minus 458°F, just one degree above absolute zero. It's colder than the background radiation of space itself. Even the vacuum of empty space is warmer.", "visual": "the Boomerang Nebula with frost crystals forming in space, temperature readings showing near-zero values"},
        {"topic": "Saturn Could Float in Water", "hook": "Despite being the second-largest planet in our solar system, Saturn's density is so low that if you could find a bathtub big enough, it would float. A gas giant lighter than water.", "visual": "Saturn floating in an impossibly large bathtub of water, the rings splashing gently, surreal cosmic humor"},
        {"topic": "The Great Attractor", "hook": "Our entire galaxy, along with 100,000 others, is being pulled toward a region of space called the Great Attractor at 1.4 million miles per hour. We can't see what it is because our own galaxy blocks the view.", "visual": "galaxies streaming toward a mysterious hidden region of space, the Milky Way blocking the view, arrows showing motion"},
        {"topic": "A Year on Pluto Is 248 Earth Years", "hook": "If you were born on Pluto, you wouldn't celebrate your first birthday for 248 Earth years. Pluto has only completed one-third of its orbit since it was discovered in 1930.", "visual": "Pluto's orbital path with only a fraction completed since discovery, a birthday cake with one candle waiting"},
        {"topic": "The Diamond Planet", "hook": "55 Cancri e is a planet twice the size of Earth that's made primarily of diamond. Its estimated value? 26.9 nonillion dollars. That's more money than has ever existed in all of human history.", "visual": "a glittering diamond planet reflecting starlight, a price tag with an impossibly long number attached"},
        {"topic": "Voyager 1 Is Still Sending Signals", "hook": "Launched in 1977, Voyager 1 is now 15 billion miles from Earth and still transmitting. Its signal takes 22 hours to reach us. It will drift through interstellar space for billions of years, carrying our message.", "visual": "Voyager 1 as a tiny golden speck against the vast emptiness of interstellar space, a faint signal beam reaching back toward a distant sun"},
        {"topic": "The Fermi Paradox", "hook": "There are 400 billion stars in our galaxy alone. If even 1% have habitable planets, there should be millions of civilizations. So where is everybody? The silence is the most terrifying answer.", "visual": "a radio telescope listening to empty static from space, the Milky Way looming behind in silence"},
        {"topic": "Black Holes Bend Time", "hook": "At the edge of a black hole, time slows to a crawl. One hour near a black hole could equal 7 years on Earth. You'd watch civilizations rise and fall while waiting for your coffee to cool.", "visual": "a person near a black hole watching Earth's timeline accelerate through centuries, split-screen time dilation"},
        {"topic": "The Pillars of Creation Are Already Destroyed", "hook": "The iconic Pillars of Creation in the Eagle Nebula are 7,000 light-years away. Evidence suggests a supernova destroyed them 6,000 years ago. We're looking at a ghost. The light just hasn't caught up.", "visual": "the Pillars of Creation with a shockwave approaching from behind, visible but not yet arrived in our view"},
        {"topic": "Jupiter's Red Spot Is Shrinking", "hook": "Jupiter's Great Red Spot is a storm that's been raging for at least 350 years. It's wider than Earth. But it's shrinking. In 20 years, the longest-running storm in the solar system may vanish.", "visual": "Jupiter's Great Red Spot at different historical sizes, shrinking over time, Earth for scale comparison"},
        {"topic": "Space Smells Like Burnt Steak", "hook": "Astronauts who've done spacewalks report that space has a distinct smell: a mix of seared steak, gunpowder, and welding fumes. It's caused by dying stars releasing polycyclic aromatic hydrocarbons.", "visual": "an astronaut removing their helmet on a space station, scent molecules visualized floating around them"},
        {"topic": "The Moon Is Drifting Away", "hook": "The Moon moves 1.5 inches farther from Earth every year. In 600 million years, total solar eclipses will be impossible. In 50 billion years, the Moon will be gone entirely.", "visual": "the Moon slowly receding from Earth, a timeline showing eclipses becoming impossible as the gap widens"},
        {"topic": "There May Be a Planet 9", "hook": "Something massive is affecting the orbits of objects at the edge of our solar system. Astronomers believe a hidden planet, 5-10 times Earth's mass, is lurking in the darkness. We just can't see it yet.", "visual": "the outer solar system with orbital paths bending around an invisible massive object, dark planet silhouette"},
        {"topic": "The Universe Is Expanding Faster Than Light", "hook": "Distant galaxies are moving away from us faster than the speed of light. Not because they're moving through space, but because space itself is stretching. They will eventually vanish from our view forever.", "visual": "galaxies stretching apart and fading as space expands between them, the observable universe shrinking"},
        {"topic": "Magnetars Can Erase Credit Cards from Half a Solar System Away", "hook": "A magnetar has a magnetic field 1 quadrillion times stronger than Earth's. From halfway across the solar system, it could strip the data from every credit card on the planet.", "visual": "a magnetar pulsing with magnetic energy, magnetic field lines warping everything around it for millions of miles"},
        {"topic": "There Are Rogue Planets Wandering in Darkness", "hook": "Billions of planets drift through space without a star. No sun, no day, no seasons. Just eternal darkness and cold. And some of them might have liquid oceans beneath frozen surfaces.", "visual": "a dark planet drifting alone through interstellar space, no star in sight, a faint glow from subsurface heat"},
        {"topic": "The Speed of Light Is Frustratingly Slow", "hook": "Light travels at 186,000 miles per second. Sounds fast. But it takes 4 years to reach the nearest star. 100,000 years to cross our galaxy. And 2 million years to reach Andromeda.", "visual": "a beam of light crawling across the galaxy at seemingly glacial pace, distance markers showing years"},
        {"topic": "The Pale Blue Dot", "hook": "In 1990, Voyager turned its camera back toward Earth from 3.7 billion miles away. Our entire civilization, every war, every love, every birth and death, was a single pixel. Less than a pixel.", "visual": "the famous Pale Blue Dot image recreated, Earth as a tiny speck in a sunbeam, cosmic perspective"},
        {"topic": "White Holes Might Exist", "hook": "If black holes suck everything in, white holes might push everything out. They're mathematically possible but have never been observed. Some physicists think the Big Bang itself was a white hole.", "visual": "a white hole ejecting matter and light in all directions, the inverse of a black hole, blinding radiance"},
        {"topic": "The Sun Loses 4 Million Tons Per Second", "hook": "Every second, the Sun converts 4 million tons of its own mass into pure energy via nuclear fusion. It's been doing this for 4.6 billion years and hasn't even lost 0.05% of its mass.", "visual": "the Sun with mass visibly streaming away as light and energy, a scale showing how much remains"},
        {"topic": "Galaxies Are Cannibals", "hook": "The Milky Way is currently devouring several smaller galaxies. The Sagittarius Dwarf galaxy is being ripped apart and absorbed as you watch this. In 4 billion years, Andromeda will consume us.", "visual": "the Milky Way pulling apart a smaller galaxy, stellar streams visible, cosmic predator-prey scene"},
        {"topic": "Time Didn't Exist Before the Big Bang", "hook": "The Big Bang didn't happen IN time. It created time itself. Asking what happened 'before' the Big Bang is meaningless because there was no 'before.' Time, space, and physics all started at once.", "visual": "a singularity exploding outward creating spacetime fabric as it expands, no 'before' visible, pure creation"},
        {"topic": "The Multiverse Theory", "hook": "Every decision you make might create a parallel universe where you chose differently. There could be infinite versions of you, living infinite lives. The math supports it. The proof doesn't exist yet.", "visual": "branching timeline paths splitting infinitely, each branch showing a different version of the same life"},
        {"topic": "Earth Is Screaming Into Space", "hook": "Every radio broadcast, TV signal, and phone call ever made is traveling through space at the speed of light. Right now, aliens 80 light-years away could be watching our World War 2 broadcasts.", "visual": "radio waves expanding outward from Earth in concentric spheres, reaching distant star systems"},
        {"topic": "The Cosmic Microwave Background", "hook": "If you tune an old TV to static, 1% of that static is radiation from the Big Bang itself. You're literally seeing the afterglow of the universe's creation every time you see snow on a screen.", "visual": "a TV showing static with the CMB pattern overlaid, zooming out to show the entire observable universe"},
        {"topic": "Andromeda Is Coming", "hook": "The Andromeda galaxy is hurtling toward the Milky Way at 250,000 miles per hour. In 4 billion years, the two galaxies will collide. The night sky will be transformed. Nothing will stop it.", "visual": "Andromeda growing larger in the night sky over centuries, eventually dominating the entire field of view"},
        {"topic": "Dark Matter Holds the Universe Together", "hook": "85% of all matter in the universe is invisible. We can't see it, touch it, or detect it directly. But without it, every galaxy would fly apart. We're held together by something we can't find.", "visual": "a galaxy with visible matter and an overlay showing the dark matter web holding it all together"},
        {"topic": "The Heat Death of the Universe", "hook": "In trillions of years, every star will burn out. Every black hole will evaporate. Every atom will decay. The universe will reach maximum entropy: a cold, dark, eternal nothing. This is how everything ends.", "visual": "a timeline showing the last stars dying, the last black hole evaporating, leaving only cold empty darkness forever"},
        {"topic": "Time Moves Slower on GPS Satellites", "hook": "GPS satellites experience time faster than us on Earth because gravity is weaker up there. Without Einstein's corrections for time dilation, your GPS would be off by 6 miles every day.", "visual": "a GPS satellite with two clocks: one showing satellite time, one showing Earth time, the drift growing"},
        {"topic": "Gamma Ray Bursts Could Sterilize Earth", "hook": "A gamma ray burst from a dying star could strip Earth's ozone layer in seconds from thousands of light-years away. No warning. No defense. It may have already caused one of Earth's mass extinctions.", "visual": "a focused beam of gamma radiation crossing space and hitting Earth's atmosphere, ozone layer dissolving"},
        {"topic": "The Observable Universe Is Just the Beginning", "hook": "What we can see is limited by the age of the universe and the speed of light. The actual universe could be 250 times larger than what we observe. Or infinite. We may never find out.", "visual": "the observable universe shown as a tiny bubble inside a vastly larger, unknowable structure"},
    ],

    "Animal Kingdom": [
        {"topic": "The Immortal Jellyfish", "hook": "Turritopsis dohrnii can reverse its aging process and become young again. It's the only known creature that is biologically immortal. It can theoretically live forever unless something eats it.", "visual": "a glowing jellyfish pulsing with light as it cycles between young and old forms, deep ocean darkness"},
        {"topic": "Octopuses Have Blue Blood and 3 Hearts", "hook": "Two hearts pump blood to the gills. One pumps it to the body. Their blood is blue because it uses copper instead of iron. And they can taste with their tentacles.", "visual": "an octopus with its three hearts visible and glowing blue, tentacles reaching out in deep water"},
        {"topic": "The Pistol Shrimp Creates a Shockwave Hotter Than the Sun", "hook": "When a pistol shrimp snaps its claw, it creates a cavitation bubble that reaches 8,000°F, nearly the temperature of the sun's surface. The shockwave stuns prey instantly. From a 2-inch shrimp.", "visual": "a pistol shrimp snapping its claw with a visible shockwave and flash of light, temperature readings"},
        {"topic": "Crows Hold Grudges and Remember Faces", "hook": "Researchers who wore threatening masks around crows were mobbed years later by crows who had never met them. The original crows taught their children. Grudges are inherited.", "visual": "a crow staring intensely at a person's face, its eye reflecting the person's image, dark atmospheric"},
        {"topic": "The Mantis Shrimp Sees Colors We Can't Imagine", "hook": "Humans see 3 primary colors. The mantis shrimp sees 16. It perceives ultraviolet, infrared, and polarized light. Its vision is so advanced that we literally cannot comprehend what it sees.", "visual": "a mantis shrimp with rainbow-like eyes, surrounded by a spectrum far beyond human visible light"},
        {"topic": "Tardigrades Can Survive Anything", "hook": "Tardigrades survive in space, at absolute zero, at 300°F, under 6,000 atmospheres of pressure, and in radiation 1,000 times lethal to humans. They're essentially indestructible.", "visual": "a microscopic tardigrade floating in space, surviving conditions that would kill everything else"},
        {"topic": "Ants Outnumber Humans 2.5 Million to One", "hook": "For every human on Earth, there are approximately 2.5 million ants. Their combined biomass exceeds all wild mammals combined. If they organized, we wouldn't stand a chance.", "visual": "a massive ant colony stretching across a landscape, the sheer scale dwarfing human structures"},
        {"topic": "Dolphins Have Names for Each Other", "hook": "Each dolphin develops a unique whistle that functions as its name. They call each other by name across distances. They remember names of dolphins they haven't seen in 20 years.", "visual": "dolphins communicating with visible sound waves between them, each wave pattern unique like fingerprints"},
        {"topic": "The Parasite That Controls Minds", "hook": "Toxoplasma gondii infects mice and rewires their brains to be attracted to cat urine. The mouse runs toward the cat, gets eaten, and the parasite completes its life cycle. It also infects humans.", "visual": "a mouse walking fearlessly toward a cat, a parasitic organism visible inside its brain, horror biology"},
        {"topic": "Electric Eels Generate 860 Volts", "hook": "An electric eel can produce an 860-volt shock, enough to knock a horse unconscious. It has specialized organs that work like thousands of tiny batteries stacked in series. Nature built a living taser.", "visual": "an electric eel discharging visible electricity in dark water, the shock illuminating its surroundings"},
        {"topic": "Elephants Mourn Their Dead", "hook": "Elephants return to the bones of dead family members years later. They touch the bones with their trunks, stand in silence, and sometimes stay for hours. They understand death and grieve.", "visual": "an elephant gently touching bones with its trunk, standing alone on a savanna at twilight, emotional weight"},
        {"topic": "The Archerfish Shoots Prey with Water", "hook": "The archerfish spits a jet of water with such precision that it knocks insects off branches from 5 feet away. It compensates for refraction, gravity, and wind. No animal should be this accurate.", "visual": "an archerfish shooting a water jet upward at an insect on a branch, the trajectory precisely calculated"},
        {"topic": "Axolotls Can Regrow Their Brain", "hook": "Cut off an axolotl's limb and it grows back. Damage its spinal cord and it heals. Remove part of its brain and it regenerates functional neural tissue. It's the closest thing to a real-life superhero.", "visual": "an axolotl with a glowing regenerating limb, neural pathways visibly regrowing, aquatic darkness"},
        {"topic": "Honey Never Expires", "hook": "Archaeologists found 3,000-year-old honey in Egyptian tombs that was still perfectly edible. Honey's low moisture, high acidity, and natural hydrogen peroxide make it immortal food.", "visual": "an ancient Egyptian tomb being opened to reveal jars of golden honey still glistening, torchlight"},
        {"topic": "The Bombardier Beetle Has a Chemical Weapon", "hook": "When threatened, the bombardier beetle mixes two chemicals in its abdomen that explode at 212°F, spraying boiling toxic liquid at predators. It's a walking chemical weapons factory.", "visual": "a beetle spraying a boiling chemical jet at an attacker, the spray visible as steam, macro close-up"},
        {"topic": "Whale Songs Travel Across Oceans", "hook": "A blue whale's call can be heard by other whales 1,000 miles away. They communicate across entire ocean basins. But ocean noise pollution is making them shout louder every decade.", "visual": "whale song sound waves spreading across an ocean map, reaching a distant whale thousands of miles away"},
        {"topic": "Sloth Algae Ecosystems", "hook": "Sloths move so slowly that algae grows on their fur. Moths live in the algae. The moths lay eggs in sloth dung. A complete ecosystem exists in the fur of one animal. It IS a habitat.", "visual": "a sloth with visible green algae on its fur, tiny moths and microorganisms visible, a self-contained world"},
        {"topic": "Cats Have a Purring Frequency That Heals Bones", "hook": "Cat purring vibrates between 25-150 Hz, the exact frequency range that promotes bone density and healing. Cats don't just purr when happy. They purr to heal themselves.", "visual": "a cat purring with visible vibration waves radiating outward, the frequency matching bone healing charts"},
        {"topic": "The Lyrebird Can Mimic Chainsaws", "hook": "The superb lyrebird can perfectly mimic any sound it hears: chainsaws, camera shutters, car alarms, other bird species. Its vocal cords are the most versatile sound-producing organ in nature.", "visual": "a lyrebird with sound waves emanating from its throat, each wave transforming into the shape of what it mimics"},
        {"topic": "Crocodiles Haven't Evolved in 200 Million Years", "hook": "Crocodiles are so perfectly designed that evolution essentially stopped improving them 200 million years ago. They watched the dinosaurs come and go. They're still here. Unchanged.", "visual": "a crocodile overlaid with its 200-million-year-old ancestor, virtually identical, dinosaurs fading in the background"},
        {"topic": "Ravens Can Plan for the Future", "hook": "Ravens hide food and remember thousands of cache locations. They'll trade tools for better food. They plan ahead, deceive other ravens, and show levels of intelligence rivaling great apes.", "visual": "a raven hiding an object while looking around suspiciously, intelligence visible in its calculating eye"},
        {"topic": "The Portuguese Man-of-War Isn't One Animal", "hook": "What looks like one jellyfish is actually a colony of thousands of tiny organisms called zooids, each specialized for a different task: floating, stinging, digesting, or reproducing. It's a team pretending to be an individual.", "visual": "a man-of-war with its component organisms visible and labeled, floating on dark ocean surface"},
        {"topic": "Sharks Predate Trees", "hook": "Sharks have existed for 450 million years. Trees have only existed for 350 million. Sharks are 100 million years older than trees. They survived 5 mass extinctions. Trees came and went.", "visual": "a timeline with sharks appearing before the first trees, surviving through extinction events marked in red"},
        {"topic": "Greenland Sharks Live for 500 Years", "hook": "A Greenland shark born today won't reach sexual maturity until the year 2175. The oldest one ever found was estimated at 512 years old. It was alive before Shakespeare wrote his first play.", "visual": "a Greenland shark swimming in dark Arctic waters with historical timeline events overlaid on its body"},
        {"topic": "Leafcutter Ants Farm Fungus", "hook": "Leafcutter ants don't eat the leaves they carry. They use them to grow fungus gardens underground. They've been farming for 50 million years. Humans have only been farming for 10,000.", "visual": "underground ant chambers with fungus gardens glowing, ants tending their crops, cross-section view"},
        {"topic": "Peregrine Falcons Dive at 240 MPH", "hook": "The peregrine falcon is the fastest animal on Earth. In a hunting dive, it reaches 240 miles per hour. At that speed, it has to close a third eyelid to prevent its eyes from being destroyed by wind.", "visual": "a peregrine falcon in a dive with speed lines and a speedometer showing 240 mph, wind distortion"},
        {"topic": "Platypuses Are Venomous Mammals", "hook": "Male platypuses have venomous spurs on their hind legs that deliver pain so excruciating that morphine doesn't help. A mammal that lays eggs, detects electricity, and produces venom. Nature broke every rule.", "visual": "a platypus with its venomous spur highlighted, swimming in dark water, bio-electric sensors glowing"},
        {"topic": "Spiders Could Eat Every Human in a Year", "hook": "The total weight of insects eaten by spiders globally every year exceeds the total weight of all humans on Earth. If they coordinated and switched targets, they could consume us all in 12 months.", "visual": "a massive web spanning a dark landscape with the biomass comparison shown as a terrifying infographic"},
        {"topic": "The Anglerfish Mating Nightmare", "hook": "Male anglerfish bite into the female and permanently fuse to her body. Their organs dissolve until they're nothing but a pair of gonads attached to the female. That's the entire male life cycle.", "visual": "a female anglerfish in the deep ocean with tiny male fused to her body, bioluminescent lure glowing"},
        {"topic": "Wombat Poop Is Cube-Shaped", "hook": "Wombats produce cube-shaped droppings because their intestines have varying elasticity that molds the feces into cubes. They stack them to mark territory. Evolution created building blocks.", "visual": "cube-shaped droppings stacked on a rock, a wombat in the background, Australian bush setting at dusk"},
    ],

    "Stoicism & Wisdom": [
        {"topic": "The Obstacle Is the Way", "hook": "Marcus Aurelius ran the Roman Empire during plague, war, and betrayal. His philosophy? The obstacle isn't blocking the path. The obstacle IS the path. Every hardship is training in disguise.", "visual": "a marble bust of Marcus Aurelius with obstacles transforming into stepping stones, classical architecture"},
        {"topic": "Memento Mori", "hook": "Roman generals celebrating victory had a slave whisper in their ear: 'Remember, you will die.' Not to depress them, but to remind them that glory is temporary. Urgency comes from mortality.", "visual": "a Roman general in a triumph procession with a skull visible in the shadows behind his laurel wreath"},
        {"topic": "You Are Not Your Thoughts", "hook": "Epictetus was a slave who became one of history's greatest philosophers. His teaching? You don't control what happens. You control how you respond. Your thoughts are suggestions, not commands.", "visual": "a chain breaking as a man stands up, thoughts floating away like clouds while he remains solid, stoic"},
        {"topic": "The Dichotomy of Control", "hook": "You can't control the economy, other people's opinions, or tomorrow's weather. You CAN control your effort, your attitude, and your response. Stoics focus only on what's in their hands.", "visual": "two circles: one labeled 'in your control' glowing bright, one labeled 'not in your control' fading to gray"},
        {"topic": "Amor Fati: Love Your Fate", "hook": "Nietzsche borrowed from the Stoics: don't just accept what happens to you. LOVE it. The worst thing that ever happened to you shaped who you are. Wishing it away wishes YOU away.", "visual": "a person embracing a storm instead of running from it, rain transforming into golden light around them"},
        {"topic": "Why Comfort Is Dangerous", "hook": "A ship is safe in harbor, but that's not what ships are built for. Stoics deliberately practiced discomfort because they knew that ease breeds fragility. Hardship builds the only real strength.", "visual": "a ship rotting in a safe harbor while another sails through a magnificent storm, growing stronger"},
        {"topic": "The Practicing Stoic Morning Ritual", "hook": "Every morning, Marcus Aurelius wrote: 'Today I will encounter ungrateful, violent, treacherous people. I am prepared because I understand they act from ignorance, not malice.' Then he governed an empire.", "visual": "a sunrise over ancient Rome with a journal and quill on a marble desk, golden morning light"},
        {"topic": "Seneca on the Shortness of Life", "hook": "Seneca wrote: 'It is not that we have a short time to live, but that we waste much of it.' The average person spends 5 years waiting in lines. 11 years on screens. Life is long if you use it.", "visual": "a life timeline with wasted years highlighted in gray and meaningful moments in gold, the ratio shocking"},
        {"topic": "Premeditatio Malorum", "hook": "Stoics imagined the worst-case scenario every morning. Not pessimism, but preparation. When you've already mentally survived the worst, nothing that actually happens can break you.", "visual": "a person visualizing worst-case scenarios that dissolve into manageable situations, mental rehearsal"},
        {"topic": "The Stoic Response to Insults", "hook": "When someone insulted Cato in the Roman Senate, he replied: 'If that's the worst thing about me, I'm doing well.' An insult only hurts if you agree with it. Your reaction is the weapon, not their words.", "visual": "words bouncing off a calm figure like arrows off marble, the insulter looking frustrated, Senate setting"},
        {"topic": "Why You Should Practice Poverty", "hook": "Once a month, Seneca slept on the floor, ate the cheapest food, and wore rough clothes. He said: 'Set aside a number of days to practice poverty so you'll never fear it.'", "visual": "a wealthy Roman sleeping on a bare floor by choice, his luxurious room visible but unused"},
        {"topic": "The Discipline of Desire", "hook": "You don't suffer because of what happens. You suffer because of what you EXPECTED to happen. Eliminate expectations and suffering disappears. The Stoics called this apatheia: freedom from passion.", "visual": "expectations shattering like glass while the person behind them stands unmoved, serene in chaos"},
        {"topic": "Marcus Aurelius Never Wanted to Be Emperor", "hook": "The most powerful man in the world didn't want the job. He wanted to be a philosopher. But he served anyway, for 19 years, because duty mattered more than desire. Reluctant power is often the best kind.", "visual": "a crown being reluctantly accepted, the person looking at philosophy books with longing, throne room"},
        {"topic": "Epictetus on Freedom", "hook": "Born a slave, leg deliberately broken by his master, Epictetus said: 'You can chain my leg, but not even Zeus can conquer my will.' True freedom is internal. No prison can take it.", "visual": "a chained foot but a free mind visualized as light expanding from the person's head, dungeon setting"},
        {"topic": "The View from Above", "hook": "Marcus Aurelius practiced zooming out: from his palace, to Rome, to the continent, to the Earth, to the cosmos. From up there, your problems are invisible. Perspective is the antidote to anxiety.", "visual": "progressive zoom-out from a person's face to their city to Earth to the galaxy, problems shrinking to nothing"},
        {"topic": "Stoic Acceptance vs. Giving Up", "hook": "Acceptance isn't surrender. It's acknowledging reality without wasting energy fighting what's already happened. A Stoic doesn't give up. They redirect their energy to what they can actually change.", "visual": "a river flowing around an immovable rock, the water finding a new path instead of stopping"},
        {"topic": "Why Anger Punishes Yourself", "hook": "Seneca wrote: 'Anger, if not restrained, is frequently more hurtful to us than the injury that provokes it.' Holding anger is drinking poison expecting the other person to die.", "visual": "a person clenching a glowing hot coal, their own hand burning while the target stands unaffected"},
        {"topic": "The Inner Citadel", "hook": "The Stoics built an untouchable fortress in their minds. External events could destroy their homes, take their money, even their bodies. But the inner citadel of reason remained unbreachable.", "visual": "a glowing fortress inside a person's silhouette, storms and chaos raging outside but unable to enter"},
        {"topic": "Voluntary Hardship", "hook": "Cold showers. Fasting. Sleeping on the floor. The Stoics didn't do these things for punishment. They did them to prove that comfort isn't necessary for happiness. Freedom from need is ultimate power.", "visual": "a person standing calmly under a waterfall of ice-cold water, their expression peaceful, misty mountain"},
        {"topic": "Death Is Not to Be Feared", "hook": "Epicurus said: 'Where death is, I am not. Where I am, death is not.' You will never experience your own death. The thing you fear most is the one thing you'll never actually face.", "visual": "a person and death as a hooded figure standing back to back, never facing each other, philosophical scene"},
        {"topic": "The Stoic on Comparison", "hook": "The person you envy has problems you can't see. The person who seems ahead started with advantages you don't know about. Comparison is theft of joy. Run your own race at your own pace.", "visual": "runners on separate tracks that are different lengths and terrain, each facing unique obstacles, overhead view"},
        {"topic": "Why the Wise Man Is Never Surprised", "hook": "A Stoic anticipates every outcome. Success and failure. Praise and criticism. Life and death. When you've prepared for everything, nothing catches you off guard. Surprise is a failure of imagination.", "visual": "a calm figure standing in a hurricane, having anticipated every possible direction of the wind"},
        {"topic": "Fate and Free Will in Stoicism", "hook": "The Stoics believed fate controls events, but you control responses. Imagine a dog tied to a cart. It can run willingly or be dragged. Either way, the cart moves. Only one way avoids suffering.", "visual": "a dog running joyfully alongside a moving cart vs being dragged behind it, same destination different experience"},
        {"topic": "Seneca on Time", "hook": "People guard their money but squander their time. Seneca said: 'People are frugal in guarding their personal property, but as soon as it comes to squandering time, they are most wasteful.'", "visual": "coins being carefully guarded while clock hands spin freely and unmonitored, Roman treasury setting"},
        {"topic": "The Philosopher King", "hook": "Plato dreamed of philosopher kings. Marcus Aurelius was the only one who actually existed. A ruler who spent his nights writing philosophy and his days governing justly. Power paired with wisdom.", "visual": "Marcus Aurelius writing meditations by candlelight after a day of ruling, exhausted but purposeful"},
        {"topic": "Why Stoics Loved Journaling", "hook": "Marcus Aurelius's 'Meditations' was never meant to be published. It was his private journal, a daily practice of self-examination. The most powerful person in the world held himself accountable on paper.", "visual": "an ancient journal with handwritten philosophical reflections, candlelight, ink well, intimate setting"},
        {"topic": "The Stoic Paradox of Wealth", "hook": "Seneca was one of the richest men in Rome. Critics called him a hypocrite. His answer? A wise man can use wealth without being enslaved by it. The problem isn't having money. It's needing it.", "visual": "a wealthy man walking past his own treasure without looking at it, freedom from attachment visualized"},
        {"topic": "Sympatheia: We Are All Connected", "hook": "The Stoics believed the universe is a single living organism. Your actions ripple outward and affect everything. Marcus Aurelius wrote: 'What injures the hive injures the bee.'", "visual": "ripples spreading from a single action affecting an interconnected web of people and events, cosmic web"},
        {"topic": "How to Handle Criticism", "hook": "If the criticism is true, learn from it. If it's false, ignore it. In either case, it cannot hurt you unless you decide to let it. Your reaction to words determines their power over you.", "visual": "arrows of criticism either being absorbed as lessons or passing through harmlessly, the person unmoved"},
        {"topic": "The Good Life According to Stoics", "hook": "The good life isn't luxury, fame, or comfort. It's living according to virtue: wisdom, justice, courage, and temperance. Everything else, money, health, reputation, is 'preferred but not required.'", "visual": "four pillars labeled with the cardinal virtues holding up a simple, solid, beautiful structure, marble aesthetic"},
    ],

    "Unsolved Mysteries": [
        {"topic": "The Disappearance of DB Cooper", "hook": "In 1971, a man hijacked a plane, collected $200,000 in ransom, and parachuted into a storm over the Pacific Northwest. He was never found. No body. No money. No identity. The only unsolved hijacking in history.", "visual": "a figure parachuting into a dark stormy forest from a plane, money bills scattering in the wind"},
        {"topic": "The Zodiac Killer's Unbroken Cipher", "hook": "The Zodiac Killer sent 4 coded messages to newspapers. Three were solved. The fourth, Z340, took 51 years. But it didn't reveal his identity. He killed at least 5 people. He was never caught.", "visual": "a cipher code on aged paper with a few decoded sections, the rest still encrypted, detective desk"},
        {"topic": "The Bermuda Triangle", "hook": "Since 1945, at least 75 planes and hundreds of ships have vanished in the Bermuda Triangle. Flight 19 disappeared with 14 airmen. The rescue plane sent to find them also vanished. No wreckage. Ever.", "visual": "a map of the Bermuda Triangle with markers showing disappeared vessels, ocean fog, compass spinning"},
        {"topic": "Jack the Ripper's Identity", "hook": "In 1888, someone murdered at least 5 women in London's Whitechapel district with surgical precision. Over 100 suspects have been named. DNA tests have been inconclusive. 136 years later, we still don't know.", "visual": "a foggy Victorian London street with a shadowy figure under a gaslight, case files scattered"},
        {"topic": "The Voynich Manuscript", "hook": "Written in the 15th century in a language no one has ever seen before or since. 240 pages of unknown plants, astronomical diagrams, and naked figures. The world's best cryptographers can't decode a single word.", "visual": "the Voynich manuscript pages open showing strange botanical drawings and alien script, candlelight"},
        {"topic": "Malaysia Airlines Flight 370", "hook": "On March 8, 2014, a Boeing 777 with 239 people vanished. It turned off its transponder, deviated from its route, and flew until it ran out of fuel. Only fragments have been found. The black box is still missing.", "visual": "a plane's radar blip disappearing from a screen, the Indian Ocean vast and dark below, no trace"},
        {"topic": "The Somerton Man", "hook": "In 1948, an unidentified man was found dead on an Australian beach. In his pocket: a scrap torn from a rare Persian poetry book with the words 'it is ended.' His identity remained unknown for 74 years.", "visual": "a body on a beach with a torn page in his hand, the ocean behind, film noir mystery atmosphere"},
        {"topic": "The Wow Signal", "hook": "On August 15, 1977, a radio telescope in Ohio detected a signal 30 times louder than the cosmic background from the direction of Sagittarius. It lasted 72 seconds. It never repeated. Was someone trying to reach us?", "visual": "the Big Ear telescope dish pointing at the night sky, the famous printout with 'Wow!' circled in red"},
        {"topic": "Amelia Earhart's Last Transmission", "hook": "In 1937, Earhart transmitted: 'We are on the line 157-337. We are running on line north and south.' Then silence. Her plane, her navigator, and she were never found. The Pacific Ocean kept the secret.", "visual": "a vintage aircraft disappearing into clouds over open ocean, radio waves fading, Earhart's last words as text"},
        {"topic": "The Taman Shud Case", "hook": "The dead man on the beach had no ID, no labels in his clothes, and a hidden pocket sewn into his trousers containing a tiny scroll. The scroll read 'Tamam Shud,' meaning 'it is ended' in Persian.", "visual": "a tiny scroll being unrolled to reveal mysterious text, the beach and ocean in the background"},
        {"topic": "The Kryptos Sculpture at CIA", "hook": "A sculpture at CIA headquarters contains 4 encrypted messages. Three have been solved. The fourth has defeated every codebreaker in the world for over 30 years. The sculptor says the solution has a deep meaning.", "visual": "a copper sculpture with encrypted text at CIA headquarters, partial solutions glowing while one section remains dark"},
        {"topic": "The Lead Masks of Vintem Hill", "hook": "Two engineers found dead on a Brazilian hilltop in 1966, wearing crude lead eye masks. Beside them: a notebook reading 'Ingest capsules. Await the agreed signal.' What signal? From whom?", "visual": "two figures lying on a hilltop wearing lead masks, a notebook between them, the sky above ominous"},
        {"topic": "The Disappearance of the Beaumont Children", "hook": "Three children vanished from an Australian beach in 1966. They were seen with a man. Despite being one of Australia's largest investigations, neither the children nor the man were ever found.", "visual": "an empty beach with three pairs of small shoes left behind, golden afternoon light, unsettling absence"},
        {"topic": "The Tunguska Event", "hook": "In 1908, something exploded over Siberia with the force of 1,000 Hiroshima bombs. It flattened 80 million trees across 830 square miles. No crater. No fragments. We still don't know exactly what it was.", "visual": "a massive shockwave flattening an endless forest from above, trees falling outward in a radial pattern"},
        {"topic": "Stonehenge's Purpose", "hook": "5,000 years ago, someone transported 25-ton stones 150 miles without wheels. We know how old it is. We know where the stones came from. We still don't know why they built it.", "visual": "Stonehenge at sunset with ancient figures working on construction, the question of purpose hanging in the air"},
        {"topic": "The Mary Celeste", "hook": "In 1872, the ship Mary Celeste was found drifting in the Atlantic. Fully stocked. Cargo intact. Personal belongings untouched. The lifeboat was missing. All 10 people on board were gone. They never returned.", "visual": "an abandoned ship drifting on calm ocean, tables set for dinner, personal items undisturbed, eerie silence"},
        {"topic": "The Circleville Letters", "hook": "Starting in 1976, residents of Circleville, Ohio received anonymous threatening letters revealing intimate personal secrets. Thousands of letters were sent. A man was convicted, but the letters continued from prison.", "visual": "a pile of threatening letters on a desk, each one revealing different secrets, dim desk lamp light"},
        {"topic": "The Flannan Isles Lighthouse Keepers", "hook": "Three lighthouse keepers vanished from a remote Scottish island in 1900. The clock had stopped. A meal was abandoned. An overturned chair. The front door locked from outside. They were never found.", "visual": "an abandoned lighthouse interior with a stopped clock and uneaten food, the storm visible through windows"},
        {"topic": "Who Built the Antikythera Mechanism", "hook": "Found in a 2,000-year-old shipwreck, this device predicted eclipses and planetary positions with the precision of a Swiss watch. Technology this advanced wouldn't appear again for 1,500 years. Who made it?", "visual": "the Antikythera mechanism with its intricate gears exposed, sitting in an ancient Greek workshop"},
        {"topic": "The Springfield Three", "hook": "In 1992, three women vanished from a house in Springfield, Missouri. The door was unlocked. A broken porch light. A phone message that was accidentally deleted by a friend. No bodies. No suspects. Nothing.", "visual": "a house with the front door ajar, a broken porch light, the interior perfectly normal, morning light"},
        {"topic": "The Hessdalen Lights", "hook": "Since the 1980s, mysterious lights have appeared in Norway's Hessdalen Valley. They hover, change color, and move against the wind. Scientists have measured them. They emit radar signals. They remain unexplained.", "visual": "glowing orbs of light floating over a Norwegian valley at night, scientific instruments measuring them"},
        {"topic": "The Black Dahlia", "hook": "In 1947, Elizabeth Short's body was found in a Los Angeles vacant lot, surgically bisected at the waist. Her face was slashed from ear to ear. Over 60 people confessed. None were the killer.", "visual": "a foggy 1940s Los Angeles street with noir detective elements, case files and crime scene photos blurred"},
        {"topic": "The Disappearance of Frederick Valentich", "hook": "In 1978, pilot Frederick Valentich reported a large unknown craft hovering above his plane. His last words: 'It is not an aircraft.' Then metallic scraping. Then silence. His plane was never found.", "visual": "a small aircraft with an enormous dark shape hovering directly above it, radio transcript text overlaid"},
        {"topic": "The Phaistos Disc", "hook": "A 4,000-year-old clay disc from Crete covered in 241 stamped symbols. The symbols don't match any known language. It was mass-produced using movable type 3,000 years before Gutenberg.", "visual": "the Phaistos disc with its mysterious spiral of symbols, backlit, the symbols glowing with unknown meaning"},
        {"topic": "The Roswell Incident", "hook": "In 1947, the US military announced it had recovered a 'flying disc.' Hours later, they retracted it and said it was a weather balloon. Witnesses described non-human bodies. The files remain classified.", "visual": "a crashed metallic object in the desert, military personnel surrounding it, newspaper headlines conflicting"},
        {"topic": "The Max Headroom Broadcast Intrusion", "hook": "In 1987, someone hijacked two Chicago TV stations wearing a Max Headroom mask. They swayed, laughed, and were spanked. The signal piracy required sophisticated equipment. They were never identified.", "visual": "a distorted TV screen showing a figure in a mask with signal interference, 1980s broadcast aesthetic"},
        {"topic": "The Tamam Shud Code", "hook": "Behind the dead man's poetry book page, police found a series of capital letters that appeared to be a code. Despite decades of analysis by military intelligence, the code has never been broken.", "visual": "handwritten capital letters in seemingly random sequence on aged paper, decoder wheels and analysis notes"},
        {"topic": "The Phoenix Lights", "hook": "On March 13, 1997, thousands of people across Arizona saw a mile-wide V-shaped craft silently gliding overhead. The governor initially joked about it. Years later, he admitted he saw it too.", "visual": "a massive V-shaped formation of lights moving silently over a city skyline, thousands of witnesses looking up"},
        {"topic": "Who Was the Man in the Iron Mask", "hook": "From 1669 to 1703, a prisoner in France was forced to wear an iron mask until his death. His identity was never revealed. Only the king knew who he was. Even the guards were forbidden to speak his name.", "visual": "a prisoner in an iron mask sitting in a stone cell, a single shaft of light, the mask reflecting candlelight"},
        {"topic": "The Disappearance of Jimmy Hoffa", "hook": "Union leader Jimmy Hoffa disappeared on July 30, 1975. He was last seen in a restaurant parking lot. His body has never been found. The FBI has searched dozens of locations. Hoffa is still missing.", "visual": "an empty parking lot with a single car, late afternoon sun, the person who should be there simply gone"},
    ],

    "Conspiracy & Hidden History": [
        {"topic": "Operation Mockingbird", "hook": "In the 1950s, the CIA secretly recruited American journalists and media organizations to spread propaganda. Over 25 major news outlets participated. This isn't theory. It was confirmed by the Church Committee.", "visual": "a newsroom with puppet strings visible on typewriters and telephones, CIA seal in the shadows"},
        {"topic": "MKUltra: CIA Mind Control", "hook": "From 1953 to 1973, the CIA ran illegal experiments on American citizens using LSD, sensory deprivation, and psychological torture to develop mind control techniques. Most files were destroyed in 1973. What survived is terrifying.", "visual": "a 1950s laboratory with subjects in chairs, observation windows, redacted documents, clinical horror"},
        {"topic": "Operation Paperclip", "hook": "After World War 2, the US secretly recruited over 1,600 Nazi scientists and engineers. War criminals were given new identities and top-secret clearances. They built NASA's rockets. This is documented history.", "visual": "Nazi scientists in lab coats being escorted into American facilities, identities being changed on documents"},
        {"topic": "The Gulf of Tonkin Incident Was Fabricated", "hook": "The event that started the Vietnam War never happened. Declassified documents prove that the second Gulf of Tonkin attack was fabricated by the US government. 58,000 Americans died for a lie.", "visual": "naval vessels firing at empty ocean, radar screens showing no contacts, government memos marked 'classified'"},
        {"topic": "Project SUNSHINE", "hook": "In the 1950s, the US government secretly collected body parts from deceased children worldwide to measure radioactive fallout from nuclear tests. Parents weren't informed. Consent was never given.", "visual": "radiation testing equipment next to medical files, atomic blast footage in the background, clinical horror"},
        {"topic": "The Tuskegee Syphilis Study", "hook": "For 40 years, the US government let 399 Black men with syphilis go untreated, even after penicillin was available. They were told they were receiving free healthcare. This happened from 1932 to 1972.", "visual": "a government medical facility with 'free treatment' sign, the reality of neglect visible behind closed doors"},
        {"topic": "Operation Northwoods", "hook": "In 1962, the US Joint Chiefs of Staff proposed staging fake terrorist attacks on American cities to justify invading Cuba. The plan included sinking boats of Cuban refugees and bombing Miami. JFK rejected it.", "visual": "a military planning room with maps of American cities, false flag operation diagrams, rejected stamp"},
        {"topic": "The Business Plot of 1933", "hook": "Wealthy American industrialists allegedly plotted to overthrow FDR and install a fascist dictatorship. Marine General Smedley Butler exposed the conspiracy. Congress investigated. No one was ever prosecuted.", "visual": "shadowy corporate figures meeting in a boardroom, blueprints for a coup on the table, 1930s aesthetic"},
        {"topic": "COINTELPRO", "hook": "From 1956 to 1971, the FBI ran illegal operations to infiltrate, discredit, and destroy civil rights organizations. They sent MLK a letter urging him to commit suicide. This was official FBI policy.", "visual": "FBI files labeled COINTELPRO with surveillance photos of civil rights leaders, wiretapping equipment"},
        {"topic": "The Nayirah Testimony Was Fake", "hook": "In 1990, a girl named Nayirah testified to Congress that Iraqi soldiers threw babies out of incubators in Kuwait. It was used to justify the Gulf War. She was actually the Kuwaiti ambassador's daughter, coached by a PR firm.", "visual": "a congressional hearing room with a girl testifying, a PR firm logo visible in shadow, manufactured tears"},
        {"topic": "Operation Gladio", "hook": "After World War 2, NATO secretly funded far-right paramilitary groups across Europe to fight communism. These groups carried out bombings and assassinations that were blamed on left-wing groups. Confirmed by the Italian government.", "visual": "weapons caches hidden in European forests, NATO symbols on crates, newspaper headlines about bombings"},
        {"topic": "The Disappeared Nuclear Weapons", "hook": "The US military has officially lost at least 6 nuclear weapons that have never been recovered. They're called 'Broken Arrows.' One is somewhere off the coast of Savannah, Georgia. It's still there.", "visual": "a nuclear weapon symbol on a map with 'LOST' marked at several locations, ocean depths highlighted"},
        {"topic": "Unit 731", "hook": "Japan's Unit 731 conducted biological warfare experiments on living humans during WW2, including vivisection without anesthesia. After the war, the US granted the researchers immunity in exchange for their data.", "visual": "a dark medical facility with experimental equipment, classified files being exchanged, moral horror"},
        {"topic": "The Rendlesham Forest Incident", "hook": "In 1980, US Air Force personnel at a NATO base in England reported a landed craft in the forest. They touched it. They documented it. The deputy base commander recorded the encounter in real-time audio.", "visual": "a triangular craft in a dark forest clearing, military personnel approaching with flashlights, official recordings"},
        {"topic": "The Panama Papers", "hook": "In 2016, 11.5 million documents were leaked exposing how world leaders, billionaires, and criminals hid money in offshore accounts. The journalist who broke the story was killed by a car bomb in Malta.", "visual": "millions of documents cascading from servers, names of world leaders highlighted, offshore bank buildings"},
        {"topic": "The Philadelphia Experiment", "hook": "In 1943, the US Navy allegedly made a destroyer escort invisible and teleported it 200 miles. Sailors were reportedly found fused into the ship's structure. The Navy denies everything. Witnesses say otherwise.", "visual": "a naval ship flickering between visible and invisible, green energy field surrounding it, harbor setting"},
        {"topic": "Operation Midnight Climax", "hook": "The CIA set up fake brothels in San Francisco to secretly dose unsuspecting men with LSD while agents watched through one-way mirrors. They wanted to study the effects. This ran for over a decade.", "visual": "a San Francisco apartment with one-way mirrors, CIA agents observing from behind, 1950s aesthetic"},
        {"topic": "The Bohemian Grove", "hook": "Every July, the most powerful men in America gather in a California redwood forest for a secretive 2-week retreat. Past attendees include every Republican president since 1923. Rituals include burning an effigy.", "visual": "a massive owl statue in a dark redwood forest, firelight illuminating robed figures, exclusive gathering"},
        {"topic": "The Real Reason Hemp Was Banned", "hook": "In 1937, hemp was banned largely because William Randolph Hearst and DuPont feared it would replace paper and nylon. They funded propaganda campaigns calling it 'marijuana' to associate it with Mexican immigrants.", "visual": "newspaper headlines demonizing hemp alongside corporate profit charts for paper and nylon companies"},
        {"topic": "The Montauk Project", "hook": "Former military personnel claim that at Camp Hero on Long Island, the US government experimented with psychological warfare, time travel, and mind control throughout the 1970s and 80s. The base is now a state park.", "visual": "an abandoned military radar tower on Long Island, strange energy emanating from underground, cold war aesthetic"},
        {"topic": "The Iran-Contra Affair", "hook": "The Reagan administration secretly sold weapons to Iran, a sworn enemy, and used the profits to fund rebel groups in Nicaragua, which Congress had explicitly forbidden. Oliver North shredded the evidence.", "visual": "weapons being loaded onto planes, money flowing through hidden channels, shredded documents falling"},
        {"topic": "The Stargate Program", "hook": "For 20 years, the CIA and DIA spent $20 million on psychic spies. They called it remote viewing. Some results were allegedly accurate enough to locate hostages and military installations. The program was declassified in 1995.", "visual": "a blindfolded person drawing locations they've never visited, military maps matching their sketches"},
        {"topic": "Henrietta Lacks and Stolen Cells", "hook": "In 1951, doctors took cancer cells from Henrietta Lacks without her knowledge or consent. Her cells became the most important in medical history, generating billions in profit. Her family received nothing for decades.", "visual": "HeLa cells dividing under a microscope, a portrait of Henrietta Lacks overlooking them, medical injustice"},
        {"topic": "The Assassination of Fred Hampton", "hook": "In 1969, the FBI provided the floor plan of Black Panther leader Fred Hampton's apartment to Chicago police. He was drugged by an informant and shot while sleeping. 99 shots were fired. Hampton fired zero.", "visual": "a dark apartment with bullet holes in walls, FBI documents showing the floor plan, evidence of premeditation"},
        {"topic": "The Forbidden Archaeology", "hook": "The Antikythera mechanism, the Baghdad Battery, the Nazca Lines. Artifacts that shouldn't exist according to mainstream timelines. Either our ancestors were far more advanced than we think, or someone is hiding something.", "visual": "ancient artifacts that seem impossibly advanced arranged on a timeline that doesn't add up, archaeological dig"},
        {"topic": "The Great Pyramid's Impossible Precision", "hook": "The Great Pyramid of Giza is aligned to true north within 3/60th of a degree. Its base is level to within 2.1 centimeters across 13 acres. We struggle to achieve this precision WITH modern technology.", "visual": "the Great Pyramid with precision measurements overlaid, modern surveying equipment beside ancient stone"},
        {"topic": "Operation Sea-Spray", "hook": "In 1950, the US Navy sprayed biological agents over San Francisco to simulate a germ warfare attack. They tracked how the bacteria spread through the city. At least one person died. Residents weren't told for decades.", "visual": "a naval vessel offshore spraying invisible agents toward a city skyline, wind patterns carrying it inland"},
        {"topic": "The Dulles Brothers' Corporate Coups", "hook": "Allen Dulles ran the CIA while his brother John Foster ran the State Department. Together, they overthrew democratically elected governments in Iran and Guatemala to protect American corporate interests. It's declassified.", "visual": "two men in suits reshaping world maps on a desk, corporate logos visible behind overthrown government seals"},
        {"topic": "The Majestic 12 Documents", "hook": "In 1984, documents surfaced claiming that in 1947, President Truman created a secret committee of 12 scientists, military leaders, and officials to investigate UFO recoveries. The FBI has investigated their authenticity.", "visual": "classified documents with 'Majestic 12' header, presidential seal, flying saucer photographs attached"},
        {"topic": "CIA Drug Trafficking", "hook": "Journalist Gary Webb documented that the CIA facilitated cocaine trafficking into Black neighborhoods to fund the Contras. His newspaper retracted the story under pressure. Webb was found dead with two gunshot wounds to the head. Ruled suicide.", "visual": "cocaine flowing through a map from Central America to US cities, CIA connections highlighted, newspaper headlines"},
    ],

    "Mind-Blowing Science": [
        {"topic": "Quantum Entanglement: Spooky Action", "hook": "Two particles can be connected so that measuring one instantly determines the state of the other, no matter the distance. Einstein called it 'spooky action at a distance.' He thought it proved quantum physics was wrong. He was wrong.", "visual": "two glowing particles separated by galaxies, connected by an invisible thread, one changes and the other responds"},
        {"topic": "The Double Slit Experiment", "hook": "Fire a particle at two slits and it goes through BOTH simultaneously. But observe it, and it goes through only one. Consciousness seems to change physical reality. This is real physics, not philosophy.", "visual": "a particle passing through two slits creating an interference pattern, but changing when an eye observes it"},
        {"topic": "You're Made of Exploded Stars", "hook": "Every atom in your body heavier than hydrogen was forged inside a star that exploded billions of years ago. The iron in your blood, the calcium in your bones, the oxygen you breathe: all stellar corpses.", "visual": "a human body dissolving into stars, each element traced back to a different supernova explosion"},
        {"topic": "Time Slows Down Near Heavy Objects", "hook": "GPS satellites have to account for the fact that time runs faster in orbit than on Earth's surface. Without Einstein's corrections, your GPS would drift by 6 miles every day. Gravity literally bends time.", "visual": "a clock near Earth running slower than an identical clock in space, the difference measurable and growing"},
        {"topic": "The Observer Effect Changes Reality", "hook": "In quantum physics, the act of observing a particle changes its behavior. Not because of instruments. Because observation itself collapses probability into certainty. Reality doesn't exist until you look at it.", "visual": "a wave function collapsing into a particle the moment an eye icon appears, quantum probability clouds"},
        {"topic": "We're Mostly Empty Space", "hook": "If you removed all the empty space from every atom in every human body on Earth, the entire population would fit inside a sugar cube. You're 99.9999999% nothing.", "visual": "all of humanity being compressed into a single sugar cube, the empty space visible at atomic level"},
        {"topic": "Schrödinger's Cat Explained", "hook": "A cat in a box is simultaneously alive AND dead until you open the box. This isn't a thought experiment about cats. It's about the fundamental nature of reality before observation. Everything exists in superposition.", "visual": "a box with a ghostly cat that flickers between alive and dead states, quantum probability fog around it"},
        {"topic": "The Mpemba Effect", "hook": "Hot water can freeze faster than cold water under certain conditions. This has been observed for centuries and was first described by an Aristotle. Modern science still can't fully explain WHY it happens.", "visual": "two containers of water side by side: hot water freezing faster than cold, ice crystals forming first on the hot one"},
        {"topic": "Dark Energy Is 68% of the Universe", "hook": "68% of the universe is dark energy, a mysterious force pushing everything apart at accelerating speed. We have no idea what it is. We only know it exists because the math doesn't work without it.", "visual": "a pie chart of the universe showing dark energy as the dominant slice, expanding space between galaxies"},
        {"topic": "Bananas Are Radioactive", "hook": "Bananas contain potassium-40, a radioactive isotope. You'd need to eat 10 million bananas at once to get a lethal dose of radiation. But technically, every banana you've ever eaten has irradiated you.", "visual": "a banana with a subtle radioactive glow, a Geiger counter clicking softly next to it, dramatic close-up"},
        {"topic": "The Speed of Light Is the Speed Limit", "hook": "Nothing with mass can travel at the speed of light because it would require infinite energy. As you approach light speed, your mass increases toward infinity. The universe has a speed limit, and it cannot be broken.", "visual": "an object accelerating toward light speed, its mass growing exponentially, energy requirements skyrocketing"},
        {"topic": "Quantum Tunneling Makes the Sun Possible", "hook": "The Sun's core isn't hot enough for fusion by classical physics. But quantum tunneling allows particles to 'teleport' through energy barriers. Without this quantum cheat code, the Sun wouldn't shine.", "visual": "particles tunneling through an impossible barrier inside the Sun's core, enabling fusion, quantum visualization"},
        {"topic": "The Butterfly Effect Is Real Physics", "hook": "A butterfly flapping its wings can theoretically cause a hurricane weeks later on the other side of the planet. This isn't metaphor. It's chaos theory. Tiny changes in initial conditions create massive unpredictable outcomes.", "visual": "a butterfly wing flap creating ripples that cascade into larger and larger weather patterns, ending in a hurricane"},
        {"topic": "Water Has Anomalous Properties", "hook": "Water is one of the only substances that expands when it freezes. If it didn't, ice would sink, oceans would freeze solid from the bottom up, and all aquatic life would die. Water breaks physics to save life.", "visual": "ice floating on water with fish swimming safely below, the molecular structure showing expansion on freezing"},
        {"topic": "The Universe Might Be a Hologram", "hook": "The holographic principle suggests that all the information in the 3D universe might actually be encoded on a 2D surface at its boundary. You might be living inside a projection. The math checks out.", "visual": "a 3D world being projected from a 2D surface at the edge of the universe, holographic reality"},
        {"topic": "Tardigrades Survived Space", "hook": "In 2007, tardigrades were exposed to the vacuum of space, cosmic radiation, and extreme UV light. They survived. Some even reproduced afterward. They're the toughest animals in the known universe.", "visual": "a tardigrade floating in the vacuum of space, surviving everything, stars and cosmic radiation all around"},
        {"topic": "Your Brain Uses Quantum Physics", "hook": "Recent research suggests that your brain may use quantum effects in its neural processes. Consciousness itself might be a quantum phenomenon. Your thoughts might operate at the most fundamental level of reality.", "visual": "a brain with quantum probability clouds visible at the synaptic level, neural networks with quantum glow"},
        {"topic": "Antimatter Is the Most Expensive Thing on Earth", "hook": "1 gram of antimatter costs approximately $62.5 trillion to produce. It's the most expensive substance in the universe. And if it touched regular matter, both would annihilate in an explosion of pure energy.", "visual": "a tiny speck of antimatter suspended in a magnetic field, a price tag showing trillions, containment chamber"},
        {"topic": "Pi Is Infinite and Non-Repeating", "hook": "Pi has been calculated to 100 trillion digits. It never repeats. It never ends. Somewhere in its infinite string, your phone number, your birthday, and every book ever written exist as a sequence.", "visual": "an infinite stream of pi digits spiraling outward, specific sequences highlighted as matching real-world data"},
        {"topic": "The Arrow of Time Problem", "hook": "The laws of physics work perfectly in both time directions. Nothing in the equations says time must move forward. Yet it does. Why time flows in one direction is one of physics' deepest unsolved mysteries.", "visual": "an arrow of time flowing forward while the equations are symmetrical in both directions, broken symmetry"},
        {"topic": "Graphene Is Impossibly Strong", "hook": "A single sheet of graphene, one atom thick, is 200 times stronger than steel. You could balance an elephant on a pencil if the pencil tip was covered in graphene. It won the Nobel Prize.", "visual": "a single-atom-thick sheet holding up enormous weight, the molecular structure of hexagonal carbon visible"},
        {"topic": "The Placebo Effect Gets Stronger Every Year", "hook": "Placebos are becoming more effective over time, but only in the US. Sugar pills now reduce pain by 30% in clinical trials. Your brain is getting better at healing itself with belief alone.", "visual": "a sugar pill dissolving into the brain and triggering real healing responses, brain scans showing genuine change"},
        {"topic": "Black Holes Have Temperature", "hook": "Stephen Hawking proved that black holes slowly emit radiation and eventually evaporate. A black hole the mass of the Sun would take 10^67 years to evaporate. Nothing is truly permanent.", "visual": "a black hole slowly shrinking as Hawking radiation escapes, a timer showing impossibly long time scales"},
        {"topic": "CRISPR Can Edit Your DNA", "hook": "CRISPR technology can cut, paste, and edit DNA with precision. We can remove genetic diseases, modify crops, and theoretically design custom organisms. We now have the power to rewrite the code of life.", "visual": "a DNA strand being precisely cut and edited by molecular scissors, gene sequences being swapped like code"},
        {"topic": "Superconductors Levitate", "hook": "Cool certain materials below their critical temperature and they develop zero electrical resistance. They also expel magnetic fields, causing them to levitate above magnets indefinitely. Magic that's really physics.", "visual": "a superconductor levitating above a magnet track, frost visible, the object floating with zero friction"},
        {"topic": "The Universe May Have No Center", "hook": "The Big Bang didn't happen at a single point. It happened everywhere simultaneously. Every point in the universe was the center of the explosion. You are at the center of the universe. So is everyone else.", "visual": "expansion happening uniformly from every point, no center visible, every location equally valid as origin"},
        {"topic": "Neutron Stars Can Spin 716 Times Per Second", "hook": "A dead star the size of a city, spinning 716 times per second. The surface moves at a quarter of the speed of light. If you stood on it, gravity would crush you to a layer one atom thick.", "visual": "a neutron star spinning as a blur, its magnetic field lines whipping around at incredible speed"},
        {"topic": "Sound Can Levitate Objects", "hook": "Acoustic levitation uses standing sound waves to suspend small objects in mid-air. Scientists have levitated water droplets, insects, and electronics. Sound is a physical force, not just vibration.", "visual": "small objects floating between sound emitters, visible sound waves holding them in place, laboratory setting"},
        {"topic": "The Universe Is Flat", "hook": "Despite being three-dimensional, the overall geometry of the universe is flat to within 0.4% accuracy. If it were curved, parallel lines would eventually meet. They don't. The universe is geometrically flat.", "visual": "parallel lines extending to infinity without converging, the flat geometry of the universe demonstrated"},
        {"topic": "Zero Can Exist in Physics", "hook": "Absolute zero is unreachable. A perfect vacuum is impossible. Zero friction doesn't exist in nature. Physics refuses to allow true nothingness. The universe insists that something must always remain.", "visual": "a temperature gauge approaching but never reaching zero, quantum fluctuations preventing true nothingness"},
    ],
}


# ═══════════════════════════════════════════════════════════════════
# ██  VISUAL STYLES — atmospheric variety per concept              ██
# ═══════════════════════════════════════════════════════════════════

VISUAL_STYLES = [
    "Hyper-detailed photorealistic 8K render, dramatic chiaroscuro lighting, depth of field bokeh.",
    "Cinematic 4K still frame, anamorphic lens flare, moody color grading with teal and orange tones.",
    "Dark atmospheric digital art, volumetric fog, subtle particle effects, high contrast.",
    "Documentary-style dramatic photography, sharp focus, natural but intense lighting.",
    "Concept art quality, matte painting aesthetic, epic scale composition, dramatic sky.",
    "Medical visualization style, dark background with selective illumination, clinical detail.",
    "Film noir aesthetic, high contrast black and white with selective color, venetian blind shadows.",
    "Futuristic holographic display aesthetic, glowing wireframes, dark background with neon accents.",
    "Oil painting texture with photorealistic detail, Rembrandt lighting, rich deep colors.",
    "Night photography style, available light only, grain texture, authentic darkness.",
    "Space photography aesthetic, long exposure star trails, cosmic color palette.",
    "Forensic photography style, evidence markers, clinical white lighting on dark subject.",
    "Underwater photography aesthetic, bioluminescent lighting, deep ocean darkness.",
    "Ancient manuscript illustration style, aged parchment texture, candlelit warmth.",
    "Infrared photography style, false color thermal imaging, scientific visualization.",
    "Split-screen comparison format, before/after lighting, educational diagram style.",
    "Macro photography, extreme close-up detail, shallow depth of field, studio lighting.",
    "Aerial/satellite photography perspective, bird's eye view, dramatic scale.",
    "Time-lapse photography composite, motion blur showing progression, dynamic energy.",
    "Cross-section diagram style, cutaway view revealing internal structures, educational clarity.",
]

# ═══════════════════════════════════════════════════════════════════
# ██  TITLE TEMPLATES — 35+ high-CTR viral curiosity templates       ██
# ═══════════════════════════════════════════════════════════════════

TITLE_TEMPLATES = [
    "{topic} #Shorts",
    "You Won't Believe {topic} #Shorts",
    "The Truth About {topic} #Shorts",
    "{topic} Will Change How You Think #Shorts",
    "Nobody Talks About {topic} #Shorts",
    "This Is Why {topic} Matters #Shorts",
    "The Dark Side of {topic} #Shorts",
    "What They Don't Tell You About {topic} #Shorts",
    "{topic} Explained in 30 Seconds #Shorts",
    "The Shocking Truth: {topic} #Shorts",
    "Wait Until You Hear About {topic} #Shorts",
    "Scientists Can't Explain {topic} #Shorts",
    "{topic} — This Changes Everything #Shorts",
    "Why {topic} Should Terrify You #Shorts",
    "The Hidden Secret of {topic} #Shorts",
    "{topic}: What Nobody Told You #Shorts",
    "This Fact About {topic} Is Insane #Shorts",
    "You're Not Ready for {topic} #Shorts",
    "The Disturbing Reality of {topic} #Shorts",
    "{topic} — Mind = Blown 🤯 #Shorts",
    "Stop Everything and Learn About {topic} #Shorts",
    "{topic}: The Untold Story #Shorts",
    "Warning: {topic} Will Haunt You #Shorts",
    "If You Knew About {topic}, You'd Never Sleep #Shorts",
    "How {topic} Actually Works Under the Hood #Shorts",
    "The 1 Thing You Must Know About {topic} #Shorts",
    "Why Everyone Gets {topic} Wrong #Shorts",
    "Never Make This Mistake: {topic} #Shorts",
    "The Secret Reason Behind {topic} #Shorts",
    "What Actually Happens During {topic} #Shorts",
    "The Bizarre Science of {topic} #Shorts",
    "{topic} Is Way Crazier Than You Think #Shorts",
    "The Real Story of {topic} #Shorts",
    "Why Doctors Warn About {topic} #Shorts",
    "The FBI Secret Trick: {topic} #Shorts",
]


# ═══════════════════════════════════════════════════════════════════
# ██  DESCRIPTION TEMPLATES — YouTube descriptions                 ██
# ═══════════════════════════════════════════════════════════════════

DESCRIPTION_TEMPLATES = [
    "{hook_short} Subscribe for daily mind-blowing facts! #Shorts #{niche_tag}",
    "Did you know this about {topic}? Hit subscribe for more. #{niche_tag} #Facts #Shorts",
    "{hook_short} Follow for content that makes you think differently. #{niche_tag} #Shorts",
    "The truth about {topic} that nobody talks about. Like & Subscribe! #{niche_tag} #Shorts",
    "{topic} — one of the most fascinating things you'll learn today. #{niche_tag} #Shorts",
]


# ═══════════════════════════════════════════════════════════════════
# ██  HIGH-RETENTION NARRATION BUILDER — 55 to 80 words per script   ██
# ═══════════════════════════════════════════════════════════════════

def build_high_retention_narration(niche: str, topic: str, hook: str, variant: int) -> str:
    """Constructs a rich, high-retention narration script (55-80 words, ~25-35s)
    with a scroll-stopping hook, core mechanism breakdown, and mind-blowing payoff.
    """
    clean_hook = hook.strip().rstrip('.')
    angle = variant % 5

    if niche == "Dark Psychology":
        openings = [
            f"If someone ever tries to pull this on you, recognize it immediately. {clean_hook}.",
            f"Here is a hidden psychological tactic that manipulators and negotiators use every day. {clean_hook}.",
            f"Have you ever felt like someone was subtly steering your decisions without your knowledge? {clean_hook}.",
            f"This psychological reality will completely change how you observe human behavior. {clean_hook}.",
            f"Your subconscious mind is constantly vulnerable to this exact social trap. {clean_hook}.",
        ]
        closings = [
            "Recognizing this psychological pattern is your only real defense. Pay attention to who uses it.",
            "Once you understand how this mechanism operates, nobody can use it against you again.",
            "The person who understands this dynamic will always control the room. Think about that.",
            "Studies confirm that 90% of people fall for this without ever realizing it happened.",
            "Remember this next time you enter a negotiation or heated conversation. It works every time."
        ]
    elif niche == "Body Science":
        openings = [
            f"Your body is doing something insane right now that you have zero idea about. {clean_hook}.",
            f"Medical science uncovered a terrifying biological fact about the human body. {clean_hook}.",
            f"What actually happens inside your cells during this process will shock you. {clean_hook}.",
            f"Doctors and biologists warn that your body reacts in ways you would never expect. {clean_hook}.",
            f"Have you ever wondered what pushes the human body past its absolute biological limits? {clean_hook}.",
        ]
        closings = [
            "Your body is a biological machine fighting to keep you alive against impossible odds.",
            "Even modern surgeons are amazed by how resilient and strange human biology truly is.",
            "If you ever experience these symptoms, listen to your body before it is too late.",
            "Evolution designed this bizarre reflex over millions of years to guarantee your survival.",
            "It proves that inside your own skin lies one of the most complex mysteries in the universe."
        ]
    elif niche in ("Scary & Creepy", "Unsolved Mysteries"):
        openings = [
            f"This is one of the most disturbing real-life cases ever documented in history. {clean_hook}.",
            f"If you are watching this alone at night, prepare yourself for this reality. {clean_hook}.",
            f"Investigators spent decades trying to explain what happened here, with zero answers. {clean_hook}.",
            f"The official reports on this incident were kept classified for years, and for good reason. {clean_hook}.",
            f"What detectives found at the scene still terrifies anyone who reads the case files. {clean_hook}.",
        ]
        closings = [
            "To this day, not a single piece of evidence has ever surfaced to explain it. Sleep well tonight.",
            "The deepest mystery is not what happened, but why every single trace vanished completely.",
            "Some questions in history were never meant to be answered. This remains one of them.",
            "When authorities closed the case, they quietly admitted they had no logical explanation.",
            "The terrifying truth is that whatever caused this could easily happen again without warning."
        ]
    elif niche in ("Space & Cosmos", "Mind-Blowing Science"):
        openings = [
            f"Physics proves that reality is vastly stranger than anything you could ever imagine. {clean_hook}.",
            f"Scientists recently confirmed a discovery that completely breaks our understanding of physics. {clean_hook}.",
            f"What would happen if you were actually exposed to this cosmic phenomenon? {clean_hook}.",
            f"Astrophysicists were baffled when they calculated the actual numbers behind this event. {clean_hook}.",
            f"Here is a mind-bending truth about the universe that will make you feel completely insignificant. {clean_hook}.",
        ]
        closings = [
            "It proves that the laws of physics are far weirder than our minds were evolved to comprehend.",
            "When you realize the sheer scale of the cosmos, everything on Earth seems impossibly small.",
            "Theoretical physicists still argue whether our universe can survive this inevitable fate.",
            "This single equation rewrote everything we thought we knew about space, time, and existence.",
            "The next time you look up at the night sky, remember that this is happening right now."
        ]
    elif niche == "Historical What If":
        openings = [
            f"History was one tiny decision away from turning out completely differently. {clean_hook}.",
            f"What if the most famous event in human history had gone the other way? {clean_hook}.",
            f"Historians agree that our modern world exists purely because of one bizarre coincidence. {clean_hook}.",
            f"Imagine waking up in a reality where this single historical turning point never occurred. {clean_hook}.",
            f"If you could travel back in time and change just one detail, this is what happens. {clean_hook}.",
        ]
        closings = [
            "A single stroke of luck shaped the entire modern world you are living in today.",
            "It proves that world superpowers and human empires rise and fall on pure chance.",
            "The ripple effects of this moment still dictate the laws, borders, and technology we use.",
            "If that day had gone differently, none of us would be here right now. History is fragile.",
            "Never underestimate how close humanity came to a completely unrecognizable timeline."
        ]
    elif niche == "Animal Kingdom":
        openings = [
            f"Nature created a creature with abilities that make comic book superheroes look weak. {clean_hook}.",
            f"Never underestimate this animal if you encounter it in the wild. {clean_hook}.",
            f"Biologists spent years studying this bizarre superpower and still cannot replicate it. {clean_hook}.",
            f"Evolution broke every established biological rule when it designed this predator. {clean_hook}.",
            f"Here is an unbelievable creature that survived multiple mass extinctions without changing. {clean_hook}.",
        ]
        closings = [
            "It proves that millions of years of natural selection produce weapons deadlier than human technology.",
            "If you ever see one in real life, keep your distance. Nature does not show mercy.",
            "Scientists are still trying to harvest these biological superpowers for human medicine.",
            "Nature designed the ultimate survivor, and humanity has only scratched the surface of its secrets.",
            "Respect the wild, because nature always finds a way to outsmart human engineering."
        ]
    elif niche == "Stoicism & Wisdom":
        openings = [
            f"Ancient Roman emperors used this exact mental rule to conquer anxiety and betrayal. {clean_hook}.",
            f"If you are going through hardship right now, remember what Marcus Aurelius wrote. {clean_hook}.",
            f"The greatest philosophers in history all agreed on one brutal truth about human life. {clean_hook}.",
            f"When life pushes you to your breaking point, this ancient principle will save your sanity. {clean_hook}.",
            f"Most people spend their entire lives wasting energy on things they can never control. {clean_hook}.",
        ]
        closings = [
            "Master your mind, and external events lose all power over your peace. Practice this daily.",
            "The pain you feel is not from the obstacle itself, but from your judgment of it. Choose freedom.",
            "You cannot control what happens to you, but your response is 100% in your hands. Never forget that.",
            "True strength is not loud. It is the quiet discipline to remain unbroken in chaos.",
            "Remember that life is short, time is fleeting, and your character is the only thing you own."
        ]
    else:  # Conspiracy & Hidden History and others
        openings = [
            f"Declassified government files revealed an operation that was officially denied for decades. {clean_hook}.",
            f"The real story behind this event was erased from standard history textbooks. {clean_hook}.",
            f"When journalists finally uncovered the classified documents, what they found was chilling. {clean_hook}.",
            f"This is not a conspiracy theory. This was documented, funded, and executed in total secrecy. {clean_hook}.",
            f"Here is a hidden chapter of history that governments spent millions trying to cover up. {clean_hook}.",
        ]
        closings = [
            "The documents are public record today, yet 99% of people still have no idea it happened.",
            "It proves that reality behind closed doors is far darker than the official press releases.",
            "When the truth was finally declassified, nobody was held accountable. History repeats itself.",
            "Ask yourself: if this was approved decades ago, what is being kept classified right now?",
            "Knowledge is power. Share this truth before history is rewritten once again."
        ]

    intro = openings[angle]
    closing = closings[variant % len(closings)]
    return f"{intro} {closing}"


def format_viral_title(template: str, topic: str) -> str:
    """Formats title and eliminates stutter words like 'Why Why' or 'What What'."""
    res = template.format(topic=topic)
    res = re.sub(r'\bWhy Why\b', 'Why', res, flags=re.IGNORECASE)
    res = re.sub(r'\bWhat What\b', 'What', res, flags=re.IGNORECASE)
    res = re.sub(r'\bThe The\b', 'The', res, flags=re.IGNORECASE)
    res = re.sub(r'\bDuring What Happens When\b', 'When', res, flags=re.IGNORECASE)
    res = re.sub(r'\bDuring What Happens\b', 'During', res, flags=re.IGNORECASE)
    return res


# ═══════════════════════════════════════════════════════════════════
# ██  GENERATOR — builds 10,000+ concepts across all niches        ██
# ═══════════════════════════════════════════════════════════════════

def generate_10000_concepts(output_file: Path, concepts_per_topic: int = 25):
    """Generates 10,000+ unique, high-retention Short concepts across all viral niches."""
    concepts = []
    seen_titles = set()

    num_styles = len(VISUAL_STYLES)
    num_titles = len(TITLE_TEMPLATES)
    num_descs = len(DESCRIPTION_TEMPLATES)

    total_topics = sum(len(topics) for topics in TOPICS.values())

    print(f"\n{'='*60}")
    print(f"  VIRAL CONCEPT BANK GENERATOR (10,000+ TARGET)")
    print(f"{'='*60}")
    print(f"  Niches:          {len(NICHES)}")
    print(f"  Total topics:    {total_topics}")
    print(f"  Variants/topic:  {concepts_per_topic}")
    print(f"  Styles:          {num_styles}")
    print(f"  Title templates: {num_titles}")
    print(f"  Target:          ~{total_topics * concepts_per_topic} concepts")
    print(f"{'='*60}\n")

    for niche_name, niche_config in NICHES.items():
        niche_topics = TOPICS.get(niche_name, [])
        niche_mood = niche_config["visual_mood"]
        niche_tags = niche_config["tags_base"]
        niche_tag = niche_tags[0] if niche_tags else niche_name.replace(" ", "")

        print(f"  [{niche_name}] Generating from {len(niche_topics)} topics...")

        for topic_idx, topic_data in enumerate(niche_topics):
            topic = topic_data["topic"]
            raw_hook = topic_data["hook"]
            base_visual = topic_data["visual"]

            for variant in range(concepts_per_topic):
                # Rotate visual styles, titles, descriptions
                style = VISUAL_STYLES[(topic_idx * 7 + variant * 13) % num_styles]
                title_template = TITLE_TEMPLATES[(topic_idx * 11 + variant * 17) % num_titles]
                desc_template = DESCRIPTION_TEMPLATES[(topic_idx * 3 + variant * 5) % num_descs]

                # Build full visual prompt (curated for 9:16 vertical framing)
                video_prompt = (
                    f"Vertical 9:16 composition. {base_visual}. "
                    f"{niche_mood}. {style}"
                )

                # Build guaranteed unique YouTube title
                base_title = format_viral_title(title_template, topic)
                youtube_title = base_title
                if youtube_title in seen_titles:
                    for alt_tpl in TITLE_TEMPLATES:
                        cand = format_viral_title(alt_tpl, topic)
                        if cand not in seen_titles:
                            youtube_title = cand
                            break
                    else:
                        youtube_title = f"{base_title.replace(' #Shorts', '')} (Pt. {variant + 1}) #Shorts"
                seen_titles.add(youtube_title)

                # Build concept title (unique internal identifier)
                concept_title = f"{topic}: Variant {variant + 1}"

                # Build rich, 55-80 word high-retention narration script
                narration_script = build_high_retention_narration(niche_name, topic, raw_hook, variant)

                # Build description
                hook_short = raw_hook[:120] + "..." if len(raw_hook) > 120 else raw_hook
                youtube_description = desc_template.format(
                    topic=topic,
                    hook_short=hook_short,
                    niche_tag=niche_tag
                )

                # Build tags
                clean_topic = topic.replace(" ", "").replace("'", "")[:30]
                tags = ["Shorts"] + niche_tags + [clean_topic, "Facts", "Viral", "MindBlown"]

                concepts.append({
                    "category": niche_name,
                    "concept_title": concept_title,
                    "video_prompt": video_prompt,
                    "voiceover_script": narration_script,
                    "youtube_title": youtube_title,
                    "youtube_description": youtube_description,
                    "tags": tags
                })

    # Shuffle to prevent niche clustering in sequential runs
    random.shuffle(concepts)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2)

    # Stats
    niche_counts = {}
    for c in concepts:
        niche_counts[c["category"]] = niche_counts.get(c["category"], 0) + 1

    print(f"\n{'='*60}")
    print(f"  [OK] Generated {len(concepts)} unique Short concepts!")
    print(f"{'='*60}")
    for niche, count in sorted(niche_counts.items()):
        print(f"    {niche:30s} -> {count:5d} concepts")
    print(f"{'='*60}")
    print(f"  Output: {output_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    dest = Path(__file__).resolve().parent / "assets" / "concepts_bank.json"
    generate_10000_concepts(dest, concepts_per_topic=25)

