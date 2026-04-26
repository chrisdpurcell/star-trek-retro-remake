# Game Design Document: Star Trek Retro Remake

## Table of Contents

### Executive Summary

- [1.1 Game Overview](#11-game-overview)
- [1.2 Target Audience](#12-target-audience)
- [1.3 Platform and Technical Requirements](#13-platform-and-technical-requirements)
- [1.4 Competitive Analysis](#14-competitive-analysis)
- [1.5 Key Features](#15-key-features)

### Game Overview

- [2.1 Setting and Theme](#21-setting-and-theme)
- [2.2 Core Player Fantasy](#22-core-player-fantasy)
- [2.3 Player Goals and Motivation](#23-player-goals-and-motivation)
- [2.4 Victory Conditions](#24-victory-conditions)

### Gameplay

- [3.1 Core Gameplay Loop](#31-core-gameplay-loop)
- [3.2 Game Modes](#32-game-modes)
- [3.3 Player Progression](#33-player-progression)
- [3.4 Difficulty and Balance](#34-difficulty-and-balance)

### Game World

- [4.1 World Overview](#41-world-overview)
- [4.2 Galaxy Map](#42-galaxy-map)
- [4.3 Sector Map](#43-sector-map)
- [4.4 Locations and Environments](#44-locations-and-environments)
- [4.5 Factions and NPCs](#45-factions-and-npcs)

### Game Mechanics

- [5.1 Starships](#51-starships)
- [5.2 Combat System](#52-combat-system)
- [5.3 Resource Management](#53-resource-management)
- [5.4 Mission System](#54-mission-system)
- [5.5 Economy and Trading](#55-economy-and-trading)
- [5.6 AI and NPCs](#56-ai-and-npcs)

### User Interface and User Experience

- [6.1 UI Design Philosophy](#61-ui-design-philosophy)
- [6.2 Interface Layout](#62-interface-layout)
- [6.3 Visual Style and Theming](#63-visual-style-and-theming)
- [6.4 Input Controls](#64-input-controls)
- [6.5 Window Behavior](#65-window-behavior)
- [6.6 Accessibility](#66-accessibility)

### Audio and Visual Design

- [7.1 Art Style](#71-art-style)
- [7.2 Asset Pipeline](#72-asset-pipeline)
- [7.3 Audio Design](#73-audio-design)
- [7.4 Visual Effects](#74-visual-effects)

### Narrative and Storytelling

- [8.1 Story Overview](#81-story-overview)
- [8.2 Characters](#82-characters)
- [8.3 Dialogue System](#83-dialogue-system)
- [8.4 Cutscenes and Presentation](#84-cutscenes-and-presentation)

### Technical Requirements

- [9.1 Technical Architecture](#91-technical-architecture)
- [9.2 Library Choices](#92-library-choices)
- [9.3 Platform Requirements](#93-platform-requirements)
- [9.4 Performance Requirements](#94-performance-requirements)
- [9.5 Data Management](#95-data-management)
- [9.6 Localization](#96-localization)

### Production

- [10.1 Development Approach](#101-development-approach)
- [10.2 Team Structure](#102-team-structure)
- [10.3 Testing Strategy](#103-testing-strategy)
- [10.4 Risk Assessment](#104-risk-assessment)
- [10.5 Resource Requirements](#105-resource-requirements)
- [10.6 Coding Standards](#106-coding-standards)
- [10.7 Architecture Decision Records](#107-architecture-decision-records)

### Marketing and Business

- [11.1 Distribution Strategy](#111-distribution-strategy)
- [11.2 Monetization Model](#112-monetization-model)
- [11.3 Community and Support](#113-community-and-support)

### Legal and Compliance

- [12.1 Intellectual Property](#121-intellectual-property)
- [12.2 Privacy and Data Protection](#122-privacy-and-data-protection)
- [12.3 Content Rating Considerations](#123-content-rating-considerations)
- [12.4 Platform Compliance](#124-platform-compliance)

### Future Development

- [13.1 Post-Launch Features (v1.1+)](#131-post-launch-features-v11)
- [13.2 Long-term Vision (v2.0+)](#132-long-term-vision-v20)

### Additional Resources

- [Appendix A: Reference Materials](#appendix-a-reference-materials)
- [Appendix B: Glossary](#appendix-b-glossary)
- [Appendix C: Change Log](#appendix-c-change-log)
- [Appendix D: Credits and Acknowledgments](#appendix-d-credits-and-acknowledgments)

---

## 1. Executive Summary

### 1.1 Game Overview

A turn-based, grid-based strategy game set in the Star Trek universe, inspired by the classic *Star Trek* (1971) and *Super Star Trek* (1973) text games but reimagined with a windowed graphical interface evoking mid-1990s desktop strategy games. The player commands a Federation starship, exploring space, completing missions, and engaging in tactical combat with rival factions across a procedurally varied galaxy.

This is an unofficial, non-commercial fan project — a personal labor of love rather than a product.

### 1.2 Target Audience

Star Trek fans, strategy game enthusiasts, and players who enjoy turn-based tactical combat and space exploration with a retro aesthetic. The game targets players who appreciate dense information panels, deliberate decision-making, and the windowed-application feel of *Master of Orion 2*, *Heroes of Might and Magic 2*, *X-COM: UFO Defense*, and the era of MUD/MUSH desktop clients.

### 1.3 Platform and Technical Requirements

- **Platform:** Linux only (no Windows or macOS support planned).
- **Language:** Python 3.14+.
- **UI and rendering:** PySide6 (Qt 6.5+). All rendering — including the isometric map — uses Qt's `QGraphicsView` and `QGraphicsScene`. No pygame, no SDL embedding, no second event loop.
- **Distribution:** AppImage for end users; `uv` for development.
- **License:** MIT for code. See §12.1 for the Star Trek IP posture.

### 1.4 Competitive Analysis

The game competes loosely with classic Trek games and modern turn-based space strategy titles. Its differentiation comes from three commitments most contemporaries don't make: a faithful 23rd-century Star Trek setting in the original-series era, a deliberately retro 1990s desktop-application UI rather than a modern stylized HUD, and grid-based exploration with z-levels rather than free 3D space.

It is not aiming to compete commercially — it's aiming to scratch a specific itch for the kind of game that doesn't really get made anymore.

### 1.5 Key Features

- Turn-based tactical combat with action points, firing arcs, and shield facings
- Grid-based space exploration with up to seven z-levels (sectors vary; flat 2D layouts are valid for tight spaces)
- Resource management spanning energy, supplies, crew morale, and ship integrity
- Classic Star Trek setting (Kirk-era 23rd century) with Federation, Klingon, Romulan, Gorn, Tholian, and Orion factions
- Three nested gameplay modes: Galaxy Map, Sector Map, and Combat
- Mission system spanning patrol, escort, reconnaissance, combat, rescue, and diplomatic objectives
- Captain progression with crew specializations and reputation effects

---

## 2. Game Overview

### 2.1 Setting and Theme

The game is set in the Kirk-era 23rd century. The player is a Starfleet captain commanding a starship — exploring uncharted space, encountering alien species, upholding the principles of the United Federation of Planets, and defending Federation interests against rival powers. The themes are exploration, diplomacy, and tactical combat in roughly that order of intent and the reverse order of game time.

### 2.2 Core Player Fantasy

You are the captain of a starship. You make strategic decisions about where to go and what to engage with. You manage a crew of named officers with specializations. You weigh resource trade-offs — burn energy now to win this fight, or conserve it to make the next sector? You build a reputation with Starfleet Command that opens better assignments and access to better ships.

The fantasy is the captain's chair, not the helm. Movement and combat are turn-based and deliberate. There is no twitch element.

### 2.3 Player Goals and Motivation

Players are motivated by exploration, tactical mastery, resource optimization, and faction relations.

**Primary motivations:**

- **Exploration**: Discover new sectors, anomalies, and uncharted space.
- **Tactical mastery**: Perfect combat strategies and ship management.
- **Resource optimization**: Efficiently manage energy, supplies, and crew morale.
- **Faction relations**: Build reputation with Federation allies and navigate diplomatic challenges.

**Short-term goals:**

- Complete assigned missions successfully
- Defeat enemy ships in tactical combat
- Maintain ship systems and crew morale
- Explore and chart new sectors
- Gather resources at starbases

**Long-term goals:**

- Unlock advanced ship classes and upgrades
- Build maximum reputation with Federation Command
- Expand the borders of Federation space through diplomacy or conquest
- Defend against major threats to the Federation

### 2.4 Victory Conditions

Star Trek Retro Remake is largely open-ended. There is no strict win condition; players continue exploring and completing missions indefinitely. Success is measured per-mission and per-campaign rather than at the game level. The game feels resolved as the player achieves significant milestones — reaching maximum reputation rank, completing major story arcs, unlocking advanced ship classes — without forcing a credits roll.

Per-mission success metrics:

- **Mission success:** Complete primary objectives, optional secondaries for bonuses, meet casualty/resource thresholds, respect time limits.
- **Combat success:** Defeat or force retreat of enemy ships, protect allied vessels, survive ambushes with minimal damage.
- **Exploration success:** Chart 100% of sector territory, discover all anomalies, establish first contact, gather complete scientific data.

Failure conditions (game-ending — distinct from per-combat losses, which respawn at the last starbase per §5.2):

- Ship destroyed in a no-respawn scenario (Admiral Mode permadeath, or specific mission-locked encounters where respawn is disabled)
- Critical mission failure resulting in court-martial
- "Disgraced" reputation rank
- Desertion during critical missions

---

## 3. Gameplay

### 3.1 Core Gameplay Loop

The game operates on a turn-based system. Each turn, the player issues commands constrained by available action points (AP), then NPCs and the environment resolve in response.

#### Time Scale

A turn represents a different real-world duration depending on the active mode:

- **Combat:** Minutes per turn
- **Sector Map:** Hours per turn
- **Galaxy Map:** Days or weeks per turn

This matters mostly for crew morale calculations and supply consumption. A long galaxy-map traversal eats more supplies than a short sector encounter.

#### Turn Phases

Each mode follows the same three-phase pattern:

1. **Player input:** The player issues commands (movement, attacks, resource changes, dialogue choices).
2. **NPC / event phase:** Hostile and neutral entities act according to their AI, and scheduled or random events fire.
3. **Resolution:** The game applies all consequences, updates game state, and re-renders.

### 3.2 Game Modes

- **Galaxy Map Mode:** Navigate between sectors, manage strategic resources, plan mission routes. No z-levels. Long time scale.
- **Sector Map Mode:** Explore individual sectors at the tactical level — encounter events, interact with starbases and stations, engage in combat. Isometric grid with z-levels.
- **Combat Mode:** Turn-based combat between starships, occurring on the same sector grid rather than transitioning to a separate combat map. Initiative system, action points, firing arcs, shield facings.

### 3.3 Player Progression

#### Captain Experience System

**Experience Points (XP):**

- Earned through combat victories, mission completion, and exploration
- XP requirements scale progressively — each level costs more XP than the last. Exact curve is a balance variable; a reasonable starting point is `XP_required(N) = N × 200` (linear), tunable to a steeper curve if level progression feels too fast in playtest.
- **No level cap.** Captains can progress indefinitely.
- **Level 100 is a reasonable completion target** — the point at which a captain feels mastered and the game's mechanical progression has fully expressed itself, without forcing a stop.

**Captain Levels and Rank Tiers:**

Captain levels are purely mechanical progression — they grant skill bonuses (see below). Rank tiers below are narrative flavor for the level milestones; they have no mechanical effect of their own. Starfleet Rank (the social/promotion system) is separate and reputation-driven (see the Reputation System further down in §3.3).

- Level 1–20: Junior Captain
- Level 21–40: Captain
- Level 41–60: Senior Captain
- Level 61–80: Commodore
- Level 81–100: Distinguished Captain
- Level 101+: Beyond standard career progression — endgame territory

**Captain Skills:**

Five skills, each scaling with captain level. The per-level effects below assume level 100 as the design target — bonuses sized so a level-100 captain is powerful but not game-breaking. Per-level values are proposals subject to a balance pass:

- **Command:** +1% crew efficiency per level (target ~+100% at level 100)
- **Tactical:** +0.5% weapon accuracy per level (target ~+50% at level 100, with hit chance soft-capped well below 100% in practice)
- **Science:** +2% sensor range per level (target ~+200% at level 100)
- **Engineering:** +1% repair speed per level (target ~+100% at level 100)
- **Diplomacy:** +1% reputation gain per level (target ~+100% at level 100)

Skills also unlock special abilities and dialogue options at specific level thresholds (defined per ability).

#### Crew Experience System

Each crew position (First Officer, Chief Engineer, etc.) levels independently. Crew gain XP from successful actions and survived encounters across a 1–10 progression.

**Crew benefits:**

- Level 5: Unlock special ability for that station
- Level 8: Reduce action point cost for station actions
- Level 10: Unlock elite bonus (unique per station)

**Crew specializations:**

- First Officer: +1 AP pool at level 5
- Chief Engineer: Emergency repairs (2 AP) at level 5
- Security Chief: +5% accuracy at level 5
- Science Officer: Enemy ship analysis at level 5
- Helm Officer: −1 AP movement cost at level 8

#### Reputation System

**Starfleet Command Ranks:**

1. Probationary (starting status)
2. Officer in Good Standing
3. Commended Officer
4. Distinguished Service
5. Exemplary Record

**Reputation effects:**

- Higher ranks unlock better missions and additional mission options
- Increased resource allocation from starbases
- Access to advanced ship upgrades
- Improved chance of positive random events during diplomatic encounters

**Reputation gains/losses:**

- Mission success: +10 to +50
- Mission failure: −20 to −100
- Civilian casualties: −50
- Destroying allied ships: −200
- Heroic actions: +100

#### Starship Upgrades

Upgrades fall into four categories:

- **Weapons systems:** Phaser arrays (damage, recharge, range, firing arc); photon torpedoes (damage, range, hit chance)
- **Shield systems:** Capacity, recharge rate
- **Engine systems:** Warp drive (galaxy travel speed); impulse engines (sector movement); reduced AP cost
- **Sensor systems:** Range, accuracy, detection capability

### 3.4 Difficulty and Balance

#### Difficulty Modes

- **Cadet Mode** (new players): Reduced enemy stats (−25% hull/shields), more generous resource regeneration (+50%), extended action point pool (+2 AP per turn), clearer tactical hints.
- **Officer Mode** (standard balanced): Default enemy and resource values, 5 AP per turn for the player.
- **Captain Mode** (challenging): Enhanced enemy stats (+25% hull/shields), standard resources, reduced action points (4 AP per turn).
- **Admiral Mode** (expert): Maximum enemy stats (+50% hull/shields), resource scarcity (−25% regeneration), permadeath for crew members. Player AP unchanged at 5 per turn — Admiral's challenge comes from a harder *world*, not a less-capable player. The penalty bundle (tougher enemies, scarce resources, permanent crew loss) makes every engagement consequential without limiting tactical options.

#### Ship Class Balance

Reference: [Memory Alpha — 23rd-century Federation starship classes](https://memory-alpha.fandom.com/wiki/Starship_classes_of_the_United_Federation_of_Planets).

| Class | Profile |
|-------|---------|
| Constitution | Balanced all-rounder (baseline) |
| Constellation | Heavy weapons platform (+30% hull, −10% speed) |
| Miranda | Hybrid science/scout (−20% hull, +30% speed) |
| Reliant | Versatile support (+10% hull, +20% speed, improved sensors) |
| Excelsior | Heavy cruiser (+40% hull, −20% maneuverability) |
| Federation | Dreadnought (+50% hull, −30% speed, +20% weapons damage) |
| Oberth | Science vessel (−30% hull, +40% sensor range, −10% weapons) |
| Antares | Survey ship (−20% hull, +30% speed, +20% sensor range) |
| Soyuz | Light cruiser (+10% speed, −10% hull, −10% weapons) |

#### Weapon Balance

- **Phasers:** 10–15 damage, 0.5s cooldown, 85% accuracy, 1 AP. Range modifiers: short +15% damage, medium 0%, long −20% damage. High effectiveness vs. shields, lower vs. hull. Firing arc varies by array type (narrow, wide, omni) and mount point.
- **Torpedoes:** 25–35 damage, 1.0s cooldown, 75% accuracy, 2 AP. Range affects hit chance: short +10%, medium 0%, long −15%. High effectiveness vs. hull, lower vs. shields. Carry a speed factor that affects hit chance against fast/maneuverable targets.

#### Resource Economy

- Energy regenerates 10 units/turn (passive)
- Shields regenerate 5 points/turn out of combat
- Phaser banks have buffer capacity (upgradable)
- Torpedo launchers have magazine size (default 10, upgradable)
- Supplies: 1 unit/turn during travel, 3 units/turn in combat
- Crew morale: −2 per week without shore leave

#### Combat Pacing

- Average combat: 5–10 turns
- Elite encounters: 15–25 turns
- Initiative range: 6–10 (prevents excessive turn-swapping)

---

## 4. Game World

### 4.1 World Overview

The galaxy is divided into sectors, each containing star systems, space stations, and points of interest. The player navigates the galaxy map to choose a sector, then drops into the sector map for tactical exploration. Each sector is a grid-based map with z-levels representing 3D space, where ships, anomalies, and other objects coexist.

### 4.2 Galaxy Map

- 10×10 grid of sectors (100 total), procedurally generated at the start of each new game from a seed
- Sector categories (Federation Core, Border, Neutral Zone, Hostile Territory, Unexplored) distributed by placement rules: Federation Core clusters around the player's starting position; hostile territory tends toward the opposite edge; neutral and unexplored sectors fill the space between
- Sector contents (starbases, anomalies, encounter likelihoods, faction presence) are also placed procedurally within rule constraints
- No z-levels at the galaxy level
- Used for navigation between sectors and strategic mission planning
- Time scale: days or weeks per turn
- Travel between sectors may trigger random encounters or scripted events
- Faction territories shown via color overlay; procedurally named landmarks marked with icons
- Each new-game seed produces a different galaxy — no two playthroughs share the same map

### 4.3 Sector Map

- Grid-based map with z-levels representing 3D space
- Maximum 1 to 7 z-levels per sector (varies — flat 2D maps are valid for tight or constrained spaces)
- Maximum 20×20 cells in x/y; sizes vary by sector
- Fixed isometric perspective
- All z-levels visible simultaneously: the active z-level is fully opaque, others are semi-transparent
- Each cell can contain multiple entities: empty space, starships (player or NPC), space stations, anomalies (black holes, nebulae, wormholes), or other objects (asteroids, debris fields)
- Time scale: minutes or hours per turn

The sector map is the central element of the game. Most play time happens here.

### 4.4 Locations and Environments

#### Galaxy Map Sectors

| Sector Type | Security | Facilities | Mission Focus |
|-------------|----------|------------|---------------|
| **Federation Core** | High, frequent patrols | Numerous starbases | Patrol, escort, diplomacy |
| **Border** | Moderate, mixed control | Less frequent starbases | Patrol, reconnaissance, defense |
| **Neutral Zone** | Low, uncharted | Rare | Exploration, first contact, surveys |
| **Hostile Territory** | Enemy-controlled | None (enemy only) | Combat, espionage, rescue |
| **Unexplored** | Unknown | None | Deep-space exploration, discovery |

#### Sector Map Locations

- **Starbases:** Major Federation facilities providing repairs, resupply, crew rest, ship upgrades, and mission briefings. Safe haven with docking mechanics.
- **Star Systems:** Central star with orbiting planets (habitable, gas giants, barren), moons, asteroid belts. Scientific survey opportunities.
- **Space Stations:** Smaller facilities — civilian (trading, research), military (defense, sensors), or neutral (independent, alien). May be damaged, abandoned, or hostile.
- **Anomalies:** Black holes (gravity wells, sensor interference), wormholes (shortcuts, future feature), subspace rifts, temporal anomalies. Scientific value with associated dangers.

#### Environmental Objects

| Environment | Sensor Impact | Movement Impact | Combat Impact |
|-------------|---------------|-----------------|---------------|
| **Open Space** | Standard range | No penalties | Emphasizes maneuver |
| **Nebulae** | −50% detection range | +1 AP per move | −10% accuracy, concealment |
| **Asteroid Fields** | LoS blocked | Increased AP cost | +20% damage reduction (cover) |
| **Debris Fields** | Minor obstruction | Navigation hazards | Partial cover, salvage opportunities |
| **Ion Storms** | Intermittent blackouts | Standard | Comms disruption |

### 4.5 Factions and NPCs

Active factions in the initial release:

- The United Federation of Planets
- Klingon Empire
- Romulan Star Empire
- The Gorn Hegemony
- The Tholian Assembly
- The Orion Syndicate
- Independent traders and explorers

Faction relationships at game start reflect canonical Star Trek lore from the 23rd century. Hostile factions present combat challenges; neutral factions offer trade opportunities and diplomatic missions; allied factions provide support and easier missions. The player can shift these relationships through their actions and Diplomacy skill checks.

NPC starships fall into three behavior categories — friendly, hostile, or neutral — and can be interacted with via combat, diplomacy, trading, random encounters, player-initiated hails, or as mission targets.

---

## 5. Game Mechanics

### 5.1 Starships

#### Visual Representation

Starships appear as sprites on the isometric sector map. Orientation is indicated by a visible arrow or engine glow. Faction-specific color coding distinguishes ships at a glance: Federation cyan, Klingon red, Romulan green, Gorn brown, Orion green-yellow, Tholian magenta. Sprite size is 256×256 pixels at base resolution, resampled by `QPixmap` at runtime for zoom levels. Z-level indicators display vertical position relative to the active layer (vertical dashed line plus `+N`/`−N` numeric badge).

#### Starship Attributes

**Primary Systems:**

- **Hull integrity:** Total structural damage capacity, varies by ship class.
- **Shield systems:** Four directional facings (forward, aft, port, starboard), 25 points each.
- **Weapon systems:** Phaser arrays (270° forward firing arc, 1 AP) and photon torpedoes (270° forward arc, 2 AP).
- **Engine systems:** Impulse drive (sector movement), warp drive (galaxy travel), maneuvering thrusters.
- **Sensor systems:** Short-range (tactical scanning) and long-range (strategic detection).

**Secondary Systems:**

- Deflector dish (environmental protection)
- Transporters (crew/cargo transfer)
- Shuttles (away missions, future)
- Life support (crew capacity)
- Communications array (hailing and diplomacy)

**Crew Attributes:**

- Crew efficiency (affects all system performance)
- Crew morale (influences efficiency and combat effectiveness)
- Individual crew member levels and specializations (see §3.3)

#### Movement System

Movement is vector-based on the grid. Each cell costs 1 AP, with diagonals computed via Pythagorean distance. Z-level transitions cost additional AP. Ship orientation updates automatically based on movement direction.

**Movement modifiers:**

- Engine power allocation (high power = greater movement range)
- Damaged engines reduce range proportionally
- Environmental costs (see §4.4 table)

**Orientation and facing:**

- Facing determines the 270° forward firing arc
- Affects shield coverage (automatic facing detection based on attacker position)
- Influences sensor effectiveness (forward sensors more effective)
- Updates automatically at the end of turn based on the final movement vector

#### Combat Capabilities

- Engage enemy ships within weapon range and firing arc
- Line of sight required for valid targeting
- Range-based accuracy and damage calculations
- Critical hits (10% chance, 1.5× damage)
- Action point costs vary by weapon

#### Docking and Services

Dock at starbases and space stations for 1 AP. Services include repairs, resupply, upgrades, and mission briefings. Federation starbases offer free repairs and full resupply; neutral trading posts charge for services. Docking restores crew morale via shore leave.

### 5.2 Combat System

#### Combat Initiation

Combat occurs on the sector map (no separate combat map) when the player encounters hostile NPCs, mission objectives require engagement, the player initiates a combat action, or an ambush triggers from a random event.

#### Turn Structure and Initiative

- All entities are assigned initiative at combat start
- Player ship: initiative 10
- NPC ships: initiative 6–9 (varies by class and crew)
- Higher initiative acts first; turn order remains fixed throughout combat
- Player ship gets 5 AP per turn (modifiable by upgrades and crew); NPC ships get 3 AP
- AP fully restores at the start of each turn; unused AP does not carry over

#### Combat Actions

**Movement:** 1 AP per cell, including z-level changes. Updates orientation. Environmental modifiers apply.

**Weapons:**

- **Phasers:** 1 AP, 10–15 damage, 85% base accuracy, 270° forward arc. Range: short +15% damage, medium baseline, long −20% damage. Effective against shields.
- **Torpedoes:** 2 AP, 25–35 damage, 75% base accuracy, 270° forward arc. Range: short +10% accuracy, medium baseline, long −15% accuracy. Effective against hull.

**Tactical:**

- **Scan:** 1 AP, reveals enemy ship status and weaknesses.
- **Evasive maneuvers:** 2 AP, +10% dodge chance for the remainder of the turn.
- **Shield redistribution:** 1 AP, reallocate power between facings.
- **Emergency repairs:** 2 AP, requires Chief Engineer at level 5+.

**Special abilities:** Vary by crew skill, ship class, and unlocks. Examples include sensor jamming, emergency power, and tactical analysis. Cost typically 2–3 AP.

#### Combat Resolution

Each attack resolves through this sequence:

1. Check line of sight between attacker and target
2. Verify target within firing arc (270° forward cone)
3. Calculate base accuracy with range modifiers
4. Apply environmental modifiers (e.g., nebulae −10%, asteroid cover +20% defense)
5. Roll for hit/miss; check critical hit (10% chance, 1.5× damage)
6. Determine which shield facing is hit, based on attacker's relative position
7. Apply damage to shields first, then hull
8. Apply system damage at hull thresholds (75%, 50%, 25%)

**Damage details:**

- Shield absorption: 85% for energy weapons, 65% for kinetic
- Critical hits bypass partial shield absorption
- Destroyed systems reduce ship effectiveness proportionally

**Resolution factors:** Weapon stats, shield strength, hull integrity, ship positioning and orientation, crew efficiency and morale, environmental effects, and current system status (damaged weapons, depleted shields, engine malfunctions) all combine into the final outcome.

#### AI Behavior

NPC ships use a three-state machine:

- **PATROL:** Default, follows patrol route, scans for targets. Transitions to ATTACK when a hostile is detected.
- **ATTACK:** Engages targets, uses weapons, maintains optimal range. Target selection based on threat level and distance. Weapon choice based on range and shield status.
- **FLEE:** Triggers when hull drops below 30%. Prioritizes survival over offensive actions. Some factions (Klingons, honor-bound) never flee.

AI processes automatically at end of player turn. Tactical decisions are deterministic for testability. See §5.6 for fuller AI detail.

#### Combat End Conditions

**Victory:** All enemy ships destroyed or fled, mission objectives completed, or enemy surrender (rare, faction-dependent).

**Failure:** Player ship destroyed (mission failure, respawn at starbase), protected target destroyed, or unable to complete time-sensitive objectives.

**Post-combat:** XP awarded based on performance, salvage opportunities from destroyed enemy ships, reputation adjustments, ship damage persists (requires repairs at starbase), crew morale shifts based on outcome.

#### Alternative Resolution

**Diplomatic options:** Hail enemy ship before combat (requires Communications officer), negotiate surrender or retreat (Diplomacy skill check). Available for some factions and mission types.

**Retreat:** Costs 2 AP. Success chance based on relative speed of player and pursuers. May result in reputation loss or mission failure.

### 5.3 Resource Management

#### Energy

- **Capacity:** Varies by ship class and reactor upgrades
- **Regeneration:** 10 units per turn (passive)
- **Allocation:** Shields, weapons, engines, sensors — managed via power-distribution sliders in the Resource Management dialog
- **Depletion:** Zero energy disables systems until regeneration occurs

#### Supplies

Subdivided into fuel (dilithium for warp, deuterium for impulse), medical supplies, spare parts, and food. Consumption is 1 unit/turn during normal travel, 3 units/turn in combat, with extra consumption for repairs and medical treatment. Resupply at starbases is free (Federation) or paid (neutral). Low supplies reduce crew morale and limit repair capability.

#### Crew Morale

Range 0–100. Affected by combat outcomes (success +5, failure −10), casualties (−15), shore leave (+20), time since last starbase visit (−2/week), ship condition (−5 for poor conditions), and mission completion (+10).

Morale effects on gameplay:

- 75–100: +10% crew efficiency bonus
- 50–74: standard performance
- 25–49: −10% crew efficiency penalty
- 0–24: −25% efficiency, risk of crew incidents

#### Ship System Condition

Each system has a condition rating 0–100%. Degrades from combat damage (immediate), normal wear (1% per 10 turns of active use), and environmental damage (nebulae, ion storms).

Effects:

- 75–100%: full functionality
- 50–74%: −15% effectiveness
- 25–49%: −35% effectiveness, increased failure chance
- 0–24%: critical, 50% chance of failure per use
- 0%: offline until repaired

Repair: 5% per turn at starbase (automatic), Chief Engineer emergency repairs (2 AP, +10% immediate), or full repairs at starbase (free at Federation bases).

#### Resource Interdependencies

- **Energy and performance:** Low energy (<25%) disables non-essential systems. Cannot fire weapons without sufficient reserve. Reduced movement range when engine power is low. Shields collapse if energy depletes during combat.
- **Supplies and operations:** Insufficient supplies prevent repairs, block medical treatment, and cannot maintain crew morale.
- **Morale and efficiency:** High morale improves all system performance. Low morale reduces repair speed and combat effectiveness.
- **System condition and combat:** Damaged weapons reduce accuracy and damage. Compromised shields have reduced capacity and regeneration. Engine damage limits movement and evasion. Sensor damage reduces detection and targeting.

#### Resource Strategy

Optimal play balances energy allocation between offense and defense, maintains supply reserves for extended missions, returns to starbases regularly to restore crew morale, prioritizes critical-system repairs over non-essential ones, and plans mission routes around resource availability.

Emergency situations call for specific responses: energy crises mean disabling non-essential systems and retreating; supply shortages mean trading or salvaging; morale collapse means immediate shore leave; system failures call for emergency repairs and tactical retreat.

### 5.4 Mission System

#### Mission Types

- **Patrol:** Travel to designated waypoints. 3–5 turns. Easy. 30% chance of hostile contact.
- **Escort:** Protect civilian or diplomatic vessel to destination. 5–8 turns. Medium. Ambushes and equipment malfunctions are common complications.
- **Reconnaissance:** Scan anomalies or enemy positions without engagement. 4–6 turns. Medium. Stealth approach and sensor management required.
- **Combat:** Engage and destroy enemy forces. 2–4 turns plus combat time. Hard. Variants include ship destruction, base assault, and ambush scenarios.
- **Rescue:** Respond to distress calls. 3–5 turns. Variable difficulty. Time pressure — penalty for late arrival.
- **Diplomatic:** Establish or maintain relations with alien species. 2–3 turns plus dialogue. Variable. Command skill checks involved.

#### Mission Generation

Procedurally generated based on sector characteristics. Federation sectors lean toward patrol and escort; neutral zones toward exploration and reconnaissance; hostile zones toward combat and rescue. Difficulty scales with player level and reputation. 1–2 missions per sector visit; the mission board refreshes when the sector is revisited. Story-driven priority missions appear at narrative beats.

#### Mission Structure

**Briefing:** Clear objective statement, expected duration and difficulty rating, reward preview, optional crew recommendations.

**Execution:** Waypoint navigation on sector map, encounter resolution (combat, dialogue, scanning), resource management during the mission, decision points with branching outcomes.

**Completion:** Success/failure evaluation, reward distribution, after-action report, reputation adjustment.

**Failure consequences:** No XP or resource rewards, reputation loss (severity-dependent), possible court-martial for critical failures, mission may become unavailable.

#### Chain Missions

Multi-part story arcs that span several sectors. Each mission builds on previous outcomes; the final mission provides exceptional rewards. Example: a five-part "Klingon Incursion" campaign. Chain mission benefits include bonus XP for completing the full chain, unique ship upgrades or equipment, major reputation improvements, and unlocking special crew or abilities.

### 5.5 Economy and Trading

The economy and trading systems are deliberately basic in the initial release. Players can trade resources at space stations. Future plans may include supply-and-demand dynamics and a more developed merchant ecosystem.

### 5.6 AI and NPCs

#### NPC Starship AI

The three-state machine (PATROL / ATTACK / FLEE) described in §5.2 governs all NPC ships. State details:

- **PATROL:** Default behavior when no threats are detected. Follows predefined patrol routes within the sector. Periodic sensor scans for targets. Transitions to ATTACK on hostile detection. Low energy consumption, standard movement.
- **ATTACK:** Actively engages detected hostiles. Target selection considers threat assessment (distance, ship class, hull), mission objectives (protect specific targets), and tactical advantage (positioning, shield status). Weapon selection is range-aware: phasers at short-medium range, torpedoes at medium-long range when shields are detected. Movement tactics include closing to optimal weapon range, maintaining firing arc, using environmental cover. Transitions to FLEE when hull drops below 30%.
- **FLEE:** Maximizes distance from threats, moves toward friendly starbases when present, uses environmental hazards to block pursuit. Energy conservation (minimal weapon use). Returns to PATROL if threats are eliminated or escape is successful.

#### AI Decision Making

Target acquisition uses a priority scoring system: distance (closer = higher), hull integrity (weaker = higher), ship class (player ship = highest), faction relations (hostile = higher). AI switches targets if the current target is destroyed or a higher-priority target appears.

#### Faction-Specific AI Behavior

| Faction | Aggression | Tactics | Flee Threshold | Special Behavior |
|---------|-----------|---------|----------------|------------------|
| Klingon | High | Frontal assault, overwhelming firepower | Never (honor) | Aggressive engagement |
| Romulan | Medium | Cloaking ambushes, flanking | 30% hull | Strategic withdrawal |
| Gorn | Medium | Defensive, heavy weapons | 20% hull | Holds position, focus on durability |
| Orion | Low | Opportunistic, hit-and-run | 50% hull | Targets weak ships, flees early |
| Tholian | Medium | Precision strikes, exotic weapons | 30% hull | Alien logic, unpredictable patterns |

#### NPC Interaction Types

- **Combat encounters:** Hostile NPCs attack on sight; neutrals may defend if provoked; friendlies assist.
- **Diplomatic:** Hailing enemy ships (Communications officer required), negotiation attempts (Diplomacy skill check), surrender offers when overwhelmed, distress calls.
- **Random encounters:** Patrol ships requesting identification, traders offering goods, distressed vessels requiring assistance, exploration vessels sharing information.
- **Mission-specific:** Escort targets following the player ship, enemy commanders with scripted behaviors, civilian vessels with fixed routes, special encounter ships with unique AI.

#### AI Limitations and Future Enhancements

The initial AI is intentionally simple. Planned future expansions include advanced tactical planning (flanking, formations), group coordination for multiple enemy ships, dynamic difficulty adjustment, personality systems for named enemy commanders, learning AI that adapts to player tactics, and richer environmental utilization (nebula hiding, asteroid navigation).

Pathfinding and line-of-sight calculations use the `tcod` library (see §9.2) rather than hand-rolled algorithms.

---

## 6. User Interface and User Experience

### 6.1 UI Design Philosophy

The UI evokes mid-1990s desktop strategy games — *Master of Orion 2*, *Heroes of Might and Magic 2*, *X-COM: UFO Defense* — and the era of MUD/MUSH desktop clients like zMUD and MUSHclient. The visual identifiers of that era:

- A resizable application window with full chrome — menu bar, toolbar, status bar, and dockable side panels.
- Chunky 3D-bevel buttons with clearly visible raised and pressed states.
- Panel borders with raised/sunken framing.
- Limited per-panel color palettes.
- Monospace fonts in info-dense panels (comm log, status panels).
- Pixel-style or simple geometric icons in toolbars.
- A tile-based map with visible grid lines.
- Dialog-heavy interaction. No floating overlay HUDs; the chrome holds the controls.

The interaction model is entirely mouse-driven with keyboard shortcuts for common actions. There is no command-line input; the MUD/MUSH influence is purely aesthetic.

### 6.2 Interface Layout

The application uses a single PySide6 main window with the following structure:

```text
+---------------------------------------------------------+
|  Menu Bar: File | View | Game | Help                    |
+---------------------------------------------------------+
|  Toolbar: [Galaxy] [Sector] [Combat] | [Z+] [Z-] | [+][-] |
+---------------------------------------------------------+
|                                |                        |
|       CENTRAL MAP              |    RIGHT DOCK PANEL    |
|     (QGraphicsView)            |                        |
|   (fills available space)      |    [Status Tab]        |
|     Isometric grid             |    [Actions Tab]       |
|     with z-level display       |    [Map Tab]           |
|                                |                        |
|                                |    Ship: USS Enterprise|
|                                |    Hull:    [====] 100%|
|                                |    Shields: [====] 100%|
|                                |    Energy:  [====] 100%|
|                                |    Position: (10,10,2) |
|                                |                        |
+--------------------------------+------------------------+
|  Comm Log (bottom dock — collapsible)                   |
|  [16:30:41] Federation channel: Patrol report received  |
|  [16:30:52] Sensor contact: Klingon D7, bearing 045     |
+---------------------------------------------------------+
|  Turn Bar: Turn: 1 | Phase: Input | AP: 5 | [End Turn]  |
+---------------------------------------------------------+
```

#### Component Breakdown

**Main window (`QMainWindow`):** Hosts the menu bar, toolbar, dock widgets, and central widget. Dock arrangement is saved and restored across sessions.

**Menu bar:**

- **File:** New Game, Save Game, Load Game, Exit
- **View:** Toggle dock visibility, zoom controls, z-level display options, theme variant
- **Game:** End Turn, Mission Log, Crew Roster, Settings
- **Help:** Controls reference, About

**Toolbar (`QToolBar`):** Mode-switcher buttons (Galaxy / Sector / Combat), zoom controls (in / out / reset), z-level navigation (visible in Sector and Combat modes). Icons sourced from QtAwesome (see §9.2).

**Central map (`QGraphicsView` + `QGraphicsScene`):** The isometric grid with all entities. One scene per game mode; the active scene is swapped on mode change without tearing down inactive scenes. Mouse wheel zooms; middle-mouse drag pans; left-click selects/moves; PageUp/PageDown changes active z-level.

**Right dock (`QDockWidget` with `QTabWidget`):**

- **Status tab:** Ship name, hull integrity (`QProgressBar`), four shield-facing bars, energy level, position, sector name.
- **Actions tab:** Movement group (Move Ship, Cancel Move), Combat group (Fire Weapons, Scan Target, Evasive Maneuvers), Utilities group (Dock, Hail).
- **Map tab:** Mini-map (sector overview), legend with sector information.

**Bottom dock — Communication Log (`QDockWidget`):** Collapsible scrollback panel showing timestamped messages: Federation channel chatter, sensor reports, mission updates, system alerts. ANSI-style color coding via HTML in `QTextEdit`. Borrowed wholesale from the MUD-client aesthetic — and genuinely useful for tracking what just happened during a busy turn.

**Turn bar:** Fixed-height bar at the bottom showing turn number, current phase, action points remaining, and the End Turn button.

#### Resizing Behavior

- Central map view expands and contracts with the window
- Minimum window size: 1600×1000
- Right dock: minimum 300px width, resizable
- Bottom comm log: collapsible to a single-line title bar
- Toolbars and turn bar stay fixed
- Layout state (dock positions, sizes, visibility) persists across sessions

### 6.3 Visual Style and Theming

#### Color Palette

The palette is stored as Python constants in `view/theme/palette.py` and referenced by name in stylesheet preprocessing — never inline.

| Token | Hex | Usage |
|-------|-----|-------|
| `bg.deep` | `#0A0E1A` | Outer window background, scene background |
| `bg.panel` | `#1A1F2E` | Dock panel backgrounds |
| `bg.raised` | `#2A3142` | Button face (default) |
| `bg.sunken` | `#0F1320` | Pressed button, input field background |
| `border.bright` | `#4A5878` | Top/left bevel highlight |
| `border.dark` | `#0A0E1A` | Bottom/right bevel shadow |
| `accent.federation` | `#4DD0E1` | Federation cyan — primary accent |
| `accent.amber` | `#FFAA00` | LCARS-adjacent amber — secondary accent, warnings |
| `text.primary` | `#D4DCE8` | Default panel text |
| `text.dim` | `#7A8499` | Secondary labels, disabled text |
| `status.shield` | `#4DD0E1` | Shield bars |
| `status.hull` | `#7CFC00` | Hull integrity (green→yellow→red gradient by %) |
| `status.energy` | `#FFEE00` | Energy bars |
| `alert.red` | `#FF3030` | Red alert, hull critical |
| `faction.klingon` | `#CC2020` | |
| `faction.romulan` | `#208030` | |
| `faction.gorn` | `#A06030` | |
| `faction.orion` | `#90D000` | |
| `faction.tholian` | `#E040E0` | |

#### Typography

- **Primary monospace:** JetBrains Mono — bundled in `assets/fonts/`. Readable, retro feel, full Unicode coverage including box-drawing characters.
- **CRT/pixel accent:** VT323 (or Perfect DOS VGA 437) — for splash screen, mission briefing headers, and other "old terminal" moments.
- **UI fallback:** System sans-serif for menu text and dialog buttons.

Fonts are registered via `QFontDatabase.addApplicationFont()` at startup. Bundled fonts ensure consistent appearance across distros — no relying on system-installed fonts.

#### Stylesheet Strategy

A single root stylesheet at `view/theme/retro.qss` is applied via `QApplication.setStyleSheet()` after force-setting the Qt style to `Fusion` (`QApplication.setStyle("Fusion")`). Fusion is the most QSS-receptive built-in style and ignores OS theming, which keeps the retro aesthetic consistent across distros.

Per-widget overrides use `setObjectName()` plus ID selectors rather than inline styles.

Key selectors authored:

- `QMainWindow`, `QDockWidget`, `QDockWidget::title` — panel title bars with faction-colored stripe
- `QPushButton`, `QPushButton:pressed`, `QPushButton:disabled` — 3D bevel via `border-style: outset/inset`
- `QProgressBar`, `QProgressBar::chunk` — segmented chunk look
- `QTabWidget::pane`, `QTabBar::tab`, `QTabBar::tab:selected` — flat tabs with selected highlight
- `QMenuBar`, `QMenu`, `QMenu::item:selected`
- `QToolBar`, `QToolButton`
- `QStatusBar`
- `QGraphicsView` — scene background color

### 6.4 Input Controls

#### Mouse

Primary interaction method.

**Map interaction:**

- Left click on grid cell: select cell or move ship (when in move mode)
- Left click on ship: select ship for status display
- Right click on ship: context menu for ship actions (future)
- Mouse wheel: zoom in/out on map view
- Middle-mouse drag: pan camera

**UI interaction:**

- Left click on buttons, menu items, toolbar buttons, and tabs: standard activation
- Drag-and-drop on dock title bars: reposition panels

#### Keyboard

**Movement and z-levels:**

- Arrow keys: pan camera
- Page Up / Page Down: change active z-level
- `+` / `-`: zoom in/out
- Home: reset zoom and recenter on player ship

**Actions:**

- Space: end turn
- M: toggle move mode
- F: fire weapons (opens target dialog)
- S: scan target
- D: dock (when adjacent to a station)
- Esc: cancel current action / close dialog

**Modes:**

- F1: Galaxy Map
- F2: Sector Map
- F3: Combat Mode (when applicable)
- F11: toggle fullscreen
- F12: toggle FPS counter (development)

All keybindings are configurable in Settings → Key Bindings, persisted to `keybindings.toml`.

### 6.5 Window Behavior

- **Default:** windowed, resizable, 1600×1000 minimum.
- **Fullscreen:** opt-in toggle via View menu (F11). Borderless fullscreen, not exclusive.
- **No native window decoration override:** the window manager draws the title bar. The retro feel comes from the *interior* chrome (menu bar, dock title bars, button bevels), not from custom-painted window borders. This keeps the application well-behaved on all Linux desktop environments.
- **Dock arrangement and window geometry:** persisted via `QSettings` to an INI file at `~/.config/star_trek_retro_remake/window_state.ini`. `QSettings` handles `QMainWindow.saveState()` (a binary `QByteArray`) and `QMainWindow.saveGeometry()` natively without base64 encoding. Game settings, key bindings, and save data stay in TOML (per §9.5); window-layout state is the one place where TOML would require ugly binary encoding, so it lives separately.

### 6.6 Accessibility

- High contrast between text and backgrounds throughout the palette
- Colorblind-friendly: information is never conveyed by color alone (status icons accompany color-coded bars, ship outlines distinguish factions in addition to color)
- Scalable UI elements: zoom levels of 1×, 1.5×, and 2× available
- Bundled fonts ensure readability at all UI scales
- All actions are mouse-accessible; all critical actions also have keyboard shortcuts
- No reliance on rapid input; turn-based gameplay is inherently accessible to players with mobility limitations

---

## 7. Audio and Visual Design

### 7.1 Art Style

The visual style is "abstract retro Trek" — pixel-tile-influenced sprites at modern resolutions, suggesting Star Trek imagery rather than reproducing it. Ships read as Federation / Klingon / Romulan / Gorn etc. through silhouette and color, not through copyrighted detail. The overall aesthetic complements the 1990s desktop chrome (§6.1) without being kitsch.

#### Color Application

- **Deep space:** Near-black with subtle blue tint (`#0A0E14`)
- **Nebulae:** Purple, pink, and blue gradients
- **Stars:** White with varying brightness
- **Grid lines:** Semi-transparent white (30% opacity)
- **Faction colors:** Per the palette in §6.3

#### Ship Design Principles

- Top-down isometric view (2.5D perspective)
- Sprites at 256×256 base resolution
- Clear orientation indicator (engine glow or facing arrow)
- Faction silhouettes recognizable at a distance
- Hull damage shown through sprite-state variants (clean → battle-damaged → critical)

Specific ship designs intentionally *evoke* canonical Trek classes (Constitution-style saucer-and-engineering, Klingon raptor, Romulan warbird) without reproducing exact copyrighted designs. See §12.1.

#### Icon Design

UI iconography comes from QtAwesome's bundled icon fonts (Font Awesome 6, Material Design Icons, Phosphor) rather than AI generation. Icons are colorized at runtime to match the palette and stay sharp at every zoom.

**Status icons (rendered):** Hull silhouette, hexagonal shields, lightning-bolt energy, crosshair weapons, nacelle engines, humanoid crew.

**Action icons:** Directional arrows for movement, targeting reticle for attack, radar sweep for scan, station silhouette for dock, wrench for repair.

### 7.2 Asset Pipeline

All visual assets are AI-generated using OpenAI's ChatGPT Images 2.0. This is a deliberate choice — the project is solo, and hand-drawing or licensing the asset volume needed isn't realistic. The pipeline is structured to make generation reproducible, IP-defensible, and consistent.

#### Directory Layout

```text
assets/
├── sprites/
│   ├── ships/          # Faction ship sprites with facing variants
│   ├── stations/       # Starbases and civilian stations
│   ├── anomalies/      # Black holes, nebulae, wormholes
│   └── environment/    # Asteroids, debris, ion storms
├── icons/              # Custom toolbar and UI icons not covered by QtAwesome
├── ui/                 # UI chrome elements (panel borders, button textures)
├── backgrounds/        # Splash screen, sector starfields, mission backdrops
├── fonts/              # Bundled fonts (JetBrains Mono, VT323)
└── prompts/            # One markdown file per asset family with the prompt used
```

#### Format and Sizing

- **Format:** PNG, RGBA, sRGB color space
- **Ship sprites:** 256×256 base, resampled at runtime
- **Environmental tiles:** 128×128
- **Custom UI icons:** 32×32 (small) and 64×64 (large), pixel-aligned
- **Backgrounds:** 1920×1080 base
- **All sprites:** transparent background, single subject centered, no baked-in drop shadow

#### Facing Variants

Ships need orientation variants for isometric rendering. The DESIGN spec calls for 45° increments (eight facings: N, NE, E, SE, S, SW, W, NW). Two paths considered:

- Generate eight sprites per ship class — accurate isometric perspective per facing, ~80 sprites for 10 ship classes.
- Generate one sprite per ship class and rotate at runtime via `QTransform` — fewer assets but isometric perspective distorts under rotation, visually compromised.

**For v0.1, four facings (NE, SE, SW, NW — the visible isometric quadrants).** Acceptable visual fidelity, manageable asset count. Expand to eight in a later version if four-facing reads poorly during playtest.

#### Prompt Archival

Every generated asset has a corresponding `assets/prompts/{asset_name}.md` containing the exact prompt, generation date, tool version, any reference images used, and notes on which variant was selected and why. This is non-optional. Three reasons:

1. Regeneration requires the prompt.
2. IP defensibility (per §12.1) requires provenance.
3. Future contributors need the lineage.

Template:

```markdown
# {asset_name}

**Tool:** ChatGPT Images 2.0
**Date:** YYYY-MM-DD
**Reference images:** none | path/to/ref.png

## Prompt

{exact prompt text}

## Notes

{which variant chosen, what was tried and rejected, post-processing if any}
```

#### Naming Convention

`{category}_{name}_{variant}.png`, lowercase snake_case, no spaces. Examples:

- `ship_federation_cruiser_facing_ne.png`
- `ship_klingon_raptor_facing_se.png`
- `anomaly_black_hole.png`
- `bg_splash_main.png`

#### Loading

A single `view/theme/asset_loader.py` module provides a `QPixmap` cache keyed by relative path. Lazy-load on first request, cache for session lifetime. `QGraphicsItem` instances reference the cached pixmap rather than reloading from disk per frame.

#### v0.1 Minimum Asset List

| Asset | Variants | Size |
|-------|----------|------|
| Federation cruiser (player ship) | 4 facings | 256×256 |
| Klingon-style ship | 4 facings | 256×256 |
| Romulan-style ship | 4 facings | 256×256 |
| Asteroid | 1 | 128×128 |
| Debris field | 1 | 128×128 |
| Nebula | 1 | 256×256 |
| Black hole | 1 | 256×256 |
| Starbase | 1 | 256×256 |
| App icon | 1 | 256×256 |
| Splash background | 1 | 1920×1080 |

Approximately 19 generated assets for v0.1. Additional UI iconography is sourced from QtAwesome at no generation cost.

### 7.3 Audio Design

Deferred to a future release. The initial release ships silent. Audio is a non-trivial scope and not on the critical path for the gameplay vision.

When audio is added, it will use Qt's `QMediaPlayer` and `QSoundEffect` (already part of PySide6). PulseAudio and PipeWire are both supported on modern Linux. ALSA fallback is available for older systems.

### 7.4 Visual Effects

Effects use Qt's animation framework — `QPropertyAnimation`, `QGraphicsItemAnimation`, and timeline-based property changes — rather than per-frame drawing. The turn-based pace doesn't demand particle systems or shaders.

**Weapon effects:**

- Phasers: animated beam line with glow, drawn via custom `QGraphicsItem` with `QPen` width animation
- Torpedoes: animated `QGraphicsPixmapItem` traversing path with trail
- Explosions: frame-based animated pixmap (4–6 frames)
- Impact flashes: brief opacity pulse on the hit ship

**Environmental effects:**

- Nebula clouds: subtle sinusoidal opacity animation
- Asteroid rotation: slow rotation property animation
- Warp travel: streak overlay during sector transitions
- Shield impacts: hexagonal grid flash at the hit location

**UI animations:**

- Button press: subtle scale and brightness via QSS pseudo-states
- Panel transitions: smooth slide or fade, 0.2s duration
- Progress bars: smooth fill animation
- Alert pulses: gentle opacity oscillation (red-alert mode)

---

## 8. Narrative and Storytelling

### 8.1 Story Overview

Narrative content is minimal in the initial release. The player is a Starfleet captain in the 23rd century; the game focuses on exploration, tactical combat, and resource management rather than scripted plot. Story comes through mission briefings, NPC encounters, and emergent events on the sector map. A heavier narrative layer is a candidate for post-launch content.

### 8.2 Characters

#### Player Character

**Captain [Player Name]** — commanding officer of the player's starship. Customizable name and basic background at game start. Experience level affects ship performance and mission availability. Reputation with Starfleet Command influences assignments and promotions.

**Captain skills (five):** Command, Tactical, Science, Engineering, Diplomacy. These are tracked via captain level — see §3.3 for the leveling curve and per-level effects. Captain levels are uncapped, with approximately level 100 representing a reasonable late-game completion state.

**Background options (story flavor):**

- Academy Graduate (standard Starfleet training)
- Field Promoted (rose through ranks during crisis)
- Explorer (focused on discovery and scientific missions)
- Tactical Officer (combat-focused background)

#### Key Crew Members

| Position | Role | Special Ability (Level 5+) | Skills |
|----------|------|---------------------------|---------|
| **First Officer** | Executive officer, tactical advisor | +1 AP pool; can assume command | Command, Tactics, Leadership |
| **Chief Engineer** | Ship systems, power distribution | Emergency repairs (2 AP) | Engineering, Warp Theory, Systems |
| **Security Chief** | Weapons systems, ship security | +5% weapon accuracy | Tactics, Weapons, Security |
| **Science Officer** | Anomaly analysis, enemy identification | Identify ship weaknesses | Science, Sensors, Xenobiology |
| **Helm Officer** | Ship movement, navigation | −1 AP movement cost (Level 8) | Piloting, Navigation, Cartography |
| **Communications** | Ship comms, diplomatic contacts | Better hailing success | Communications, Diplomacy, Translation |
| **Medical Officer** | Crew health, casualty treatment | Emergency medical treatment | Medicine, Xenobiology, Psychology |

#### NPC Characters

**Starfleet Command — Admiral [Procedurally Generated Name]:**

- Issues mission assignments, communicates strategic directives
- Personality types: By-the-book, Maverick, Diplomatic, Tactical
- Relationship affected by player reputation and mission outcomes

**Starbase Commanders — Commander [Procedurally Generated Name]:**

- Manages starbase operations and local sector defense
- Provides repair/resupply services, local intelligence, sector missions
- Reputation affects service priority and pricing

Procedural names use `tcod.namegen` with custom rule files for sci-fi-flavored output (see §9.2).

#### Enemy Commanders

| Faction | Personality | Tactics | Ship Classes |
|---------|-------------|---------|--------------|
| **Klingon** | Aggressive, honor-focused | Frontal assault, never retreats | D7 Cruiser, Bird-of-Prey |
| **Romulan** | Tactical, deceptive | Cloaking ambushes, flanking | Bird-of-Prey, Warbird |
| **Gorn** | Methodical, powerful | Defensive positioning, heavy weapons | Heavy Cruiser |
| **Orion** | Opportunistic | Targets weak ships, flees when outmatched | Raider, Corsair |
| **Tholian** | Alien logic, territorial | Web weapons, precision strikes | Web-Spinner |

#### Neutral Characters

| Character | Role | Benefits |
|-----------|------|----------|
| **Merchant Captain** | Trading opportunities, rumors | Access to rare supplies and equipment |
| **Independent Explorer** | Sector information | Sector maps, anomaly locations |
| **Civilian Transport** | Escort opportunities | Reputation gains, emergency assistance |

### 8.3 Dialogue System

To be defined in a future phase. The initial release uses static mission-briefing text and limited multiple-choice dialogue at decision points.

### 8.4 Cutscenes and Presentation

No cutscenes planned. Major story beats are conveyed through static dialog screens with character portraits and text — appropriate to the retro aesthetic and lower-cost than animated cinematics.

---

## 9. Technical Requirements

### 9.1 Technical Architecture

#### Pattern: State Machine + Game Object + Component + MVC

The architecture is a hybrid optimized for turn-based strategy: a state machine for mode transitions, the Game Object pattern with component composition for entities, and Model-View-Controller separation for testability.

#### Layer Boundaries

The strict layering rule is: **the model layer has zero Qt imports.** This guarantees the entire game simulation can run headless under pytest, with no `QApplication` required.

```text
src/stmrr/
├── model/          # Pure Python. No Qt, no PySide6. Headless-testable.
│   ├── state/      # GameStateManager, GameState subclasses
│   ├── entities/   # GameObject, Starship, Station, Anomaly, Projectile
│   ├── systems/    # WeaponSystems, ShieldSystems, EngineSystems, SensorSystems
│   ├── world/      # GalaxyMap, SectorMap, GridPosition
│   ├── combat/     # TurnManager, CombatResolver, AI state machines
│   ├── missions/   # Mission, MissionManager, MissionTemplate (TOML loader)
│   ├── resources/  # ResourceManager (energy, supplies, morale)
│   └── events.py   # Pure-Python observer/event bus (blinker)
│
├── view/           # PySide6-only. Subscribes to model events, renders state.
│   ├── main_window.py
│   ├── docks/                # QDockWidget panels
│   ├── dialogs/              # QDialog subclasses
│   ├── scene/                # QGraphicsScene + custom QGraphicsItem classes
│   │   ├── map_view.py       # QGraphicsView with isometric projection
│   │   ├── grid_scene.py     # Scene managing items per active mode
│   │   ├── items/            # CellItem, StarshipItem, AnomalyItem, etc.
│   │   └── projection.py     # Iso math: world (x,y,z) ↔ scene (sx, sy)
│   ├── widgets/              # Custom QWidgets (status bar, progress meters)
│   └── theme/                # QSS, font registration, palette, asset_loader
│
├── controller/     # Translates Qt input → model calls; bridges model events → Qt signals.
│   ├── input_router.py
│   ├── model_bridge.py       # QObject that emits Qt signals when model events fire
│   └── action_handlers.py    # End Turn, Fire Weapons, Move, Dock, etc.
│
├── config/         # Pydantic models for ships, missions, factions, settings
├── persistence/    # Save/load via pydantic + TOML
└── app.py          # Entry: build QApplication, wire MVC, show MainWindow

tests/
├── unit/           # Model-only tests, no QApplication
├── integration/    # pytest-qt tests for view + controller
└── fixtures/
```

#### Layer Enforcement

The "model has zero Qt imports" rule is enforced by `import-linter`, run in CI alongside ruff and mypy. A declarative contract in `.importlinter` at the repo root specifies the forbidden dependency:

```ini
[importlinter]
root_package = stmrr
include_external_packages = True

[importlinter:contract:model-is-qt-free]
name = Model layer must not import Qt or PySide6
type = forbidden
source_modules =
    stmrr.model
forbidden_modules =
    PySide6
    shiboken6
```

CI fails on any violation. This is the single most important architectural rule in the project — convention is not enough; mechanical enforcement keeps the layer pure even under time pressure or refactor churn.

`include_external_packages = True` is required at the top-level `[importlinter]` section because `PySide6` and `shiboken6` sit outside the `stmrr` root package. Without it, import-linter 2.11+ refuses to evaluate forbidden contracts that reference external modules.

A secondary contract enforces controller-as-seam:

```ini
[importlinter:contract:view-does-not-import-model-events]
name = View must not subscribe to model events directly
type = forbidden
source_modules =
    stmrr.view
forbidden_modules =
    stmrr.model.events
```

This forces all model→view communication through `controller/model_bridge.py`, which is the only module permitted to import both `model.events` and `PySide6`.

#### Game State Management

The state machine is hand-rolled rather than using `QStateMachine`. With ~7 states (MainMenu, GalaxyMap, SectorMap, Combat, MissionBriefing, Settings, SaveLoad), a generic FSM library adds more complexity than it removes.

State transitions emit Python events on the blinker event bus; the model bridge translates them to Qt signals that the view consumes — swapping the active `QGraphicsScene`, updating dock visibility, etc.

#### Game Object and Component Pattern

```python
class GameObject:
    """Base class for all game entities."""
    def __init__(self, position: GridPosition):
        self.id = generate_id()
        self.position = position
        self.active = True

class Starship(GameObject):
    def __init__(self, position: GridPosition, ship_class: str):
        super().__init__(position)
        self.systems = {
            'weapons': WeaponSystems(),
            'shields': ShieldSystems(),
            'engines': EngineSystems(),
            'sensors': SensorSystems(),
        }
        self.crew = CrewRoster()
        self.resources = ResourceManager()
```

Components are simple objects with their own state and behavior, composed onto entities rather than inherited. This is the simplification of a full ECS — appropriate for a turn-based game with modest entity counts.

#### Map Rendering: QGraphicsView + QGraphicsScene

The map is the central game element and gets the most architectural weight.

- **One `QGraphicsScene` per game mode** (Galaxy / Sector / Combat). The active scene is set on a single shared `QGraphicsView` when modes change. Inactive scenes remain in memory with state intact for fast switching.
- **Logical coordinates are cartesian `(x, y, z)`** stored on items. Scene coordinates are isometric-projected pixels. All conversion lives in `view/scene/projection.py` and is fully unit-tested.
- **Z-levels** rendered as `QGraphicsItem.zValue` (Qt's painter ordering) plus per-level opacity. Active level: opacity 1.0; non-active: 0.35. Configurable in settings.

Custom `QGraphicsItem` subclasses. All items receive state updates via the model bridge — never by subscribing to model events directly. See *MVC Wiring and Event Flow* below for the mechanism.

| Item | Role |
|------|------|
| `GridCellItem` | One per grid cell, manages hover/select highlight. Pooled. |
| `GridLineItem` | Iso grid lines per z-level. Dashed pattern denotes z-distance from active layer. |
| `StarshipItem` | Ship sprite + faction color + facing arrow. Reflects hull, shield, and position state. |
| `AnomalyItem` | Black holes, nebulae, wormholes. Optional animated glow. |
| `EnvironmentItem` | Asteroids, debris, ion storms. Static. |
| `ProjectileItem` | Phaser beams, torpedoes during combat. Pooled (~100 pre-allocated). Animated via `QPropertyAnimation` along path. |
| `ZLevelMarkerItem` | Vertical dashed line + numeric `+N` / `−N` indicator. |

The `MapView` (a `QGraphicsView` subclass) handles input:

- Mouse wheel: zoom via `scale()`, clamped 0.25× to 4.0×
- Middle-mouse drag: pan via `setDragMode(ScrollHandDrag)` toggle
- Left click: hit-test via `itemAt()`, dispatch to controller
- Page Up / Page Down: change active z-level
- Arrow keys: pan camera
- Render hints: `QPainter.Antialiasing | QPainter.SmoothPixmapTransform`
- `QGraphicsItem.setCacheMode(DeviceCoordinateCache)` for static items (asteroids, grid lines) to avoid redraw cost

#### MVC Wiring and Event Flow

```text
User clicks grid cell
    ↓
QGraphicsView.mousePressEvent
    ↓
controller/input_router.py — translates QMouseEvent → ModelAction(MoveShip, dest)
    ↓
GameModel.execute_move() — pure Python, validates, mutates state
    ↓
model/events.py — emits ShipMoved(ship_id, new_position) on blinker bus
    ↓
controller/model_bridge.py — observer callback, emits Qt Signal ship_moved
    ↓
view/scene/items/StarshipItem — connected slot updates QGraphicsItem position
                                 with QPropertyAnimation
```

The two-layer event system (Python observer in the model + Qt signals in the bridge) is what keeps the model Qt-free. The bridge in `controller/model_bridge.py` is the single seam where both worlds meet.

#### Object Pooling

Object pooling matters more for `QGraphicsItem` subclasses than the model entities themselves; creating and destroying graphics items has measurable cost in tight loops (especially projectiles).

- Starship pool: 20 pre-allocated entities
- Projectile pool: 100 pre-allocated entities
- Visual effect pool: 50 pre-allocated entities

Pool expansion: 25% growth when exhausted.

### 9.2 Library Choices

The runtime stack was deliberately chosen to minimize hand-rolling. Each library replaces specific code that would otherwise need to be written, tested, and maintained.

| Library | Replaces | Why |
|---------|----------|-----|
| **PySide6** | UI + rendering | Single framework, single event loop. `QGraphicsView` covers map rendering without pygame. |
| **pydantic** v2 | Hand-rolled validation | Schema validation for ships, missions, factions, settings, save game state. Fast, type-safe, integrates with TOML cleanly. |
| **tcod** (python-tcod) | Custom LoS, FOV, A* | Mature roguelike algorithm library. NumPy-based `compute_fov`, `tcod.path.Pathfinder`, `tcod.los`, plus `tcod.namegen` for procedural names. Skip its console rendering. |
| **blinker** | Custom observer pattern | Pure-Python signal/slot library used by Flask. ~400 lines, two decades stable. |
| **loguru** | stdlib `logging` boilerplate | Sane defaults, structured logging, pretty tracebacks, file rotation built in. |
| **qtawesome** | AI-generated UI icons | Vector icons via Font Awesome 6, Material Design, Phosphor, etc. Themeable via QColor, sharp at any zoom, eliminates several AI generations. |
| **tomli-w** | Custom TOML writer | `tomllib` (stdlib) reads; this writes. Used for save files and settings persistence. |

#### Saved-State Security

Save files are pydantic models serialized to TOML. **`pickle` and `dill` are banned** — both expose remote-code-execution risk on load. Even a single-user game can be tricked into loading a malicious save file from an untrusted source. TOML round-tripping via pydantic is inspectable, safe, and human-editable for debugging.

#### Deferred Libraries

- **hypothesis** — property-based testing for game-state invariants. High value once the model layer stabilizes (v0.2+).
- **superqt** — extra Qt widgets (range sliders, collapsibles). Adopt only when a specific need arises.
- **rich + typer** — for a future debug/admin CLI. Easy to add later.

#### Skipped Libraries

| Library | Reason |
|---------|--------|
| `transitions` / `python-statemachine` | Hand-rolled state manager is simpler at this state count. |
| `numpy` (direct) | Pulled in via tcod transitively. Don't add as direct dep unless needed elsewhere. |
| Behavior-tree libraries | Premature for the current AI scope. Revisit at v0.3+. |
| `pickle`, `dill` | RCE risk on save load. Hard rule. |
| `dynaconf`, full `pydantic-settings` | Overkill for single-user desktop config. |
| `qt-material`, `pyqtdarktheme` | Pre-built themes fight bespoke QSS. |
| `arcade`, `pygame`, `pyglet`, `kivy` | Rejected by the pure-Qt decision. |

### 9.3 Platform Requirements

#### Target Platform

Linux only. All development and testing happens on Linux. Code uses Linux-specific paths, system calls, and conventions. POSIX-compliant environment is assumed. No Windows or macOS support is planned.

#### System Requirements

**Minimum:**

- OS: Debian 13 / Ubuntu 24.04 LTS or equivalent modern distribution
- Python: 3.14 or higher
- RAM: 4 GB
- Storage: 500 MB
- Display: 1600×1000 minimum
- Graphics: OpenGL 2.0+ capable GPU

**Recommended:**

- OS: Latest stable Linux distribution
- Python: Latest 3.14+ release
- RAM: 8 GB or more
- Storage: 1 GB
- Display: 1920×1080 or higher
- Graphics: Modern GPU with OpenGL 3.0+

#### Linux-Specific Considerations

**File system:**

- Forward-slash paths
- Case-sensitive file names
- Configuration: `~/.config/star_trek_retro_remake/`
- Save data: `~/.local/share/star_trek_retro_remake/`

**Display:**

- X11 supported directly
- Wayland supported natively (PySide6 6.5+)

#### Distribution

- **Development:** `uv` for venv and lockfile management; `uv run python -m stmrr` to launch.
- **Release:** AppImage via `python-appimage` or `briefcase`. Bundles the Python interpreter and all dependencies.
- **Future:** Flatpak for sandboxed distribution; native `.deb` package for Debian/Ubuntu.

#### Toolchain Bootstrap

Python 3.14 is not yet available in Debian 13 / Ubuntu 24.04 default repositories. The project bootstraps its own interpreter via `uv` rather than depending on system Python:

```bash
# One-time per machine
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.14

# Per repo clone
cd star-trek-retro-remake
uv sync --all-extras
uv run python -m stmrr
```

`pyproject.toml` declares `requires-python = ">=3.14"`. CI uses the same `uv python install 3.14` step. This avoids deadends caused by distro Python lag and keeps the project pinned to a known-good interpreter version across all dev machines and CI runners.

### 9.4 Performance Requirements

#### Frame Rate Targets

- UI and menus: 60 FPS target, 30 FPS minimum
- Map rendering: 60 FPS target, 30 FPS minimum during animation
- Combat animations: 30+ FPS

The turn-based nature of the game tolerates lower frame rates without gameplay impact. Priority is consistency over peak performance. Input response is the harder constraint: <16ms from click to visible feedback.

#### Load Time Targets

- Application startup: <3 seconds to main menu
- Sector map load: <2 seconds
- Combat initialization: <1 second
- Galaxy map render: <1 second
- Save/load: <2 seconds

#### Memory Usage

No hard memory ceiling. A 2D turn-based game on modern desktop hardware operates with plenty of headroom; engineering for tight memory budgets is premature optimization. The one rule that matters: **no memory leaks.** Long sessions, repeated mode switches, and many save/load cycles must not grow memory unboundedly. Validate via long-running test sessions during v1.0 polish.

If memory use ever climbs unreasonably (multi-GB for a turn-based game), it's a bug worth investigating — likely an unbounded cache or an entity pool that grows but never shrinks.

#### CPU Usage

- Player turn processing: <50ms
- AI turn processing: <200ms per NPC ship
- 10 simultaneous AI ships: <1 second
- Turn advancement: <100ms

#### Threading

The Qt event loop drives everything. AI computation is synchronous on the main thread for v0.1 — turn budgets are well within frame time. If per-turn AI processing exceeds 1 second in later versions (e.g., advanced tactical planning), heavy computation moves to `QThreadPool` with results delivered via Qt signals.

#### Performance Monitoring

- F12 toggles an FPS counter and frame-time graph during development
- Performance warnings logged via loguru for slow operations (>100ms)
- AI processing time tracked per ship
- Render time breakdown by component

### 9.5 Data Management

#### Configuration Format

User-facing configuration uses **TOML** — human-readable, comment-friendly, type-safe, well-supported by `tomllib` (stdlib reader) and `tomli-w` (writer). Schemas are defined as pydantic models so loading validates structure and types up front rather than crashing deep in turn logic.

The single exception is **window-layout state** (dock positions, geometry), which lives in a `QSettings` INI file because `QMainWindow.saveState()` returns a binary `QByteArray` that doesn't fit cleanly into TOML. See §6.5.

#### Configuration Files

User config root: `~/.config/star_trek_retro_remake/`

```text
~/.config/star_trek_retro_remake/
├── game_settings.toml    # Display, audio, controls, graphics
├── keybindings.toml      # Keyboard mappings
└── window_state.ini      # QSettings: window geometry, dock layout

src/stmrr/data/                 # Bundled with code, read-only at runtime
├── ships.toml                  # Ship class definitions
├── factions.toml               # Faction relationships, behavior, territory placement rules
├── missions.toml               # Mission templates
├── galaxy_generation.toml      # Galaxy-level procedural rules
└── sector_templates.toml       # Sector-content templates (starbase, anomaly, etc. spawn rules)
```

#### Examples

**Game settings:**

```toml
[display]
window_width = 1024
fullscreen = false

[grid_size]
galaxy = [10, 10]
sector = [20, 20, 5]
```

**Ship class:**

```toml
[ship_classes.constitution]
name = "Constitution Class"
hull_integrity = 100

[ship_classes.constitution.systems.weapons]
phaser_arrays = 4
torpedo_capacity = 12
```

**Galaxy generation rule:**

```toml
[galaxy.zone_distribution]
federation_core_radius = 2     # cells from player start
hostile_edge_buffer = 3         # cells from the opposite edge
neutral_zone_density = 0.3      # fraction of remaining sectors

[sector_template.starbase]
type = "starbase"
services = ["repair", "resupply", "missions"]
spawn_chance_in_federation_core = 0.6
spawn_chance_in_border = 0.2
```

#### Save Game Management

Save files are pydantic models of the full game state, serialized to TOML. Multiple save slots (5 manual + 1 auto-save) plus metadata (timestamp, turn count, sector, mission status).

**Auto-save triggers (hybrid):**

- **Mode transitions:** auto-save fires when entering or leaving combat, on docking at a starbase, on entering or leaving the galaxy map. These are natural "checkpoint" moments — the kind a player would manually save at — and they bracket the highest-stakes events in the game (a combat win/loss, a successful dock, a long traversal).
- **Fallback interval:** every N turns of continuous play in the same mode without a transition, to catch extended sessions (a long galaxy traversal, an extended sector survey). Default N = 10; configurable. The fallback is a safety net rather than the primary mechanism — most auto-saves should land on transitions.

This pattern matches turn-based-strategy convention (XCOM, FTL) where saves cluster at meaningful moments rather than ticking on a fixed clock.

### 9.6 Localization

The game ships in English. No localization plans for the initial release.

---

## 10. Production

### 10.1 Development Approach

This is a solo project with Claude Code as the primary implementer. The development model is project-management-led: I make architectural and design decisions; Claude Code handles execution.

#### Phased Roadmap

**v0.1 — Vertical slice and core loop**

- Project scaffold, MVC layering, theming
- Empty windowed grid with zoom, pan, z-level switch
- One ship rendered, click-to-select, click-to-move
- Turn manager with AP system
- One starbase placed on the test sector. Player can move adjacent to it and trigger the **Dock** action (1 AP cost). Exercises the full action pipeline — button click → AP debit → state change → UI update — end-to-end. v0.2's combat actions ride on top of this same pipeline; proving it works in v0.1 means v0.2 can focus on combat math rather than rebuilding action plumbing.
- Minimum asset set (per §7.2)

**v0.1 Definition of Done.** v0.1 is complete when *all* of the following pass:

1. `uv run python -m stmrr` launches the main window on a clean Debian 13 / Ubuntu 24.04 box with no errors in the loguru log.
2. Window opens at 1600×1000 minimum, all docks visible, retro QSS applied (no native Fusion grey bleeds through).
3. The active sector renders an isometric grid with z-level switching via PageUp/PageDown. Active z-level opacity 1.0; non-active 0.35.
4. Mouse wheel zoom (0.25×–4.0× clamped) and middle-mouse drag pan both work without selection or focus loss.
5. The player ship renders at a starting cell. Left-click selects; clicking another reachable cell moves the ship one cell, debits 1 AP, emits `ShipMoved` from the model, and the `StarshipItem` animates to the new position via `QPropertyAnimation`.
6. A starbase is placed adjacent-reachable. Moving adjacent to it enables the Dock action button. Clicking Dock debits 1 AP, emits a `Docked` event, and writes a comm log entry timestamped via loguru.
7. End Turn button advances the turn counter, restores AP to 5, and emits `TurnAdvanced`.
8. Window geometry and dock layout persist across restarts via `QSettings` to `~/.config/star_trek_retro_remake/window_state.ini`.
9. CI is green: ruff, mypy, `import-linter`, and pytest all pass. Coverage on `model/` is at or above 80%.
10. `import-linter` enforces "model has zero Qt imports" — verifiable by adding a test `PySide6` import to a model file and watching CI fail.

If any of the above fails, v0.1 is not done. Don't move on to v0.2 work until the checklist clears.

**v0.2 — Combat foundation**

- Phaser and torpedo weapons
- Shield facings and damage resolution
- Basic AI state machine (PATROL / ATTACK / FLEE)
- Mission system foundation with TOML templates
- Save/load via pydantic round-trip

**v0.3 — Resource management, missions, and difficulty modes**

- Energy allocation, supplies, crew morale
- Six mission types fully implemented
- Mission briefing and tracking dialogs
- Reputation system
- Difficulty modes (Cadet / Officer / Captain / Admiral) — all four dimensions difficulty touches (combat scaling, resource scarcity, AP modifiers, and the permadeath flag) exist by this point. Permadeath enforcement lands here as a flag; the crew system that makes it consequential lands in v0.5.

**v0.4 — Procedural galaxy and sector navigation**

- Galaxy map mode with sector navigation
- Procedural galaxy generation: rule-based placement of sector types, faction territories, starbases, and anomalies from a seed
- Procedural sector contents (within sector templates from §9.5)
- Travel time and warp consumption
- Random encounters during travel

**v0.5 — Crew and progression**

- Captain XP and skills (with the uncapped curve from §3.3)
- Crew member specializations and leveling
- Ship upgrade paths

**v1.0 — Polish and ship**

- Full audio pass
- Bug fixes and balance tuning
- Distribution as AppImage
- Documentation completeness

#### Vertical Build Order

When scaffolding, build vertically through the stack rather than completing each layer before starting the next. This surfaces MVC seam issues in week one rather than week ten.

1. `pyproject.toml` + `uv` lockfile + repo skeleton, including `.importlinter` contract and `pre-commit` config
2. `docs/adr/` directory seeded with ADR-0001 through ADR-0012 capturing the locked decisions (one ADR per locked decision; see §10.7)
3. `model/world/grid_position.py` + `model/entities/game_object.py` — pure Python, fully unit-tested
4. `view/scene/projection.py` — isometric math, fully unit-tested
5. `view/main_window.py` — empty `QMainWindow` shell with menu bar and dock placeholders
6. `view/scene/map_view.py` + `view/scene/grid_scene.py` — render an empty grid with z-levels
7. `view/scene/items/grid_cell_item.py` + `starship_item.py` — render one ship on the grid, verify selection
8. `model/state/game_state_manager.py` + `controller/model_bridge.py` — hook up state transitions with the signal bridge
9. Resume feature work from §10.1

Build vertically through the stack early (steps 1–8) rather than building each layer to completion. Catches MVC seam issues in week 1, not week 10.

### 10.2 Team Structure

Solo developer. No outside contributors anticipated for v0.1. Public open-source repository may attract community contributions over time; if so, see §11.3.

### 10.3 Testing Strategy

| Layer | Framework | Notes |
|-------|-----------|-------|
| Model (pure Python) | `pytest` | Headless, no `QApplication`. Fast. Run on every commit. |
| Controller bridges | `pytest` + mocks | Mock the Qt signal layer; verify model events translate correctly. |
| View widgets | `pytest-qt` | `qtbot` fixture for widget interaction. |
| `QGraphicsScene` rendering | `pytest-qt` + `QImage` snapshot | Render scene to `QImage`, hash, compare to golden. Catches projection regressions. |
| AI behavior | `pytest` | Deterministic seeds; assert state-machine transitions and target selection. |
| TOML round-trip | `pytest` | Save → load → assert deep equality. Catches schema drift. |

**Coverage targets:** 80%+ on `model/`, 60%+ on `view/`, 70%+ on `controller/`. Don't chase 100% — diminishing returns past these levels.

#### Test Categories

- **Game logic:** Movement, combat, resources, turn management
- **State machine:** Transitions, mode switching, validation
- **Ship systems:** Weapons, shields, engines, sensors
- **AI behavior:** Decision-making, targeting, tactical states
- **Data management:** Configuration loading, save/load operations

#### Tools

- `pytest` — core framework
- `pytest-qt` — Qt widget testing
- `pytest-cov` — coverage reporting
- `pytest-mock` — mocking and fixtures
- `pytest-env` — environment variable management for headless Qt
- `ruff` — linting and formatting
- `mypy` — static type checking
- `import-linter` — architectural layer enforcement (see §9.1)
- `cProfile` — performance investigation when needed

#### CI

GitHub Actions workflow runs ruff, mypy, `import-linter`, and pytest on every push. Branch protection on `main` requires passing CI before merge.

CI installs Python 3.14 via `uv python install 3.14`, runs `uv sync --all-extras`, then executes the lint/type/test pipeline. Headless Qt is enabled via `QT_QPA_PLATFORM=offscreen` in the workflow env (see "Headless Qt" below); `xvfb-run` is available as a fallback for any test that genuinely needs a display server.

#### Headless Qt

`pytest-qt` and the `QImage` snapshot tests in the rendering layer require a Qt platform plugin. CI and local headless test runs use Qt's offscreen platform plugin, set via the `QT_QPA_PLATFORM` environment variable.

Configured in `pyproject.toml` under `[tool.pytest.ini_options]`:

```toml
[tool.pytest.ini_options]
env = [
    "QT_QPA_PLATFORM=offscreen",
]
```

This requires `pytest-env`. For developers running tests locally on a machine with a display, the offscreen plugin still works correctly — it just doesn't open windows.

If a specific test needs a real display server (extremely rare for this project), `xvfb-run pytest tests/that_specific_test.py` is the escape hatch. The CI runner has `xvfb` installed for this case but defaults to offscreen.

### 10.4 Risk Assessment

The biggest risks for a solo project of this scope are scope creep, asset pipeline overhead, and burnout. Mitigations:

- **Scope creep:** Phased roadmap (§10.1) with explicit cut lines. v0.1 ships before v0.2 starts.
- **Asset overhead:** Asset list per release is fixed up front. AI generation keeps art-pipeline cost low; QtAwesome handles iconography.
- **Burnout:** This is a personal project, not a deliverable. No deadlines. Pause is acceptable.

Smaller technical risks:

- **PySide6 version drift:** Qt 6 is well-supported but PySide6 binding occasionally lags Qt itself. Pin major version in `pyproject.toml`.
- **AppImage portability:** Python applications in AppImage occasionally have library-loading edge cases. Test on at least Debian, Ubuntu LTS, and one rolling distro before declaring v1.0.
- **AI asset consistency:** Multiple ChatGPT generations of the same prompt produce different outputs. Mitigated by archiving prompts and selecting variants deliberately rather than using first-generation output.

### 10.5 Resource Requirements

Solo developer time. Asset generation uses an existing ChatGPT Plus subscription — no per-asset cost beyond tooling already in place. No third-party tooling licenses.

### 10.6 Coding Standards

A short, mechanically-enforced standard. Documented in full in `CONTRIBUTING.md`; the canonical decisions live here.

**Formatting and linting (ruff):**

- Line length: 100 characters.
- Quote style: double quotes.
- Import sorting: ruff's isort-compatible rules (`I` rule set enabled).
- Rule sets enabled: `E`, `F`, `W`, `I`, `B`, `UP`, `SIM`, `RUF`. Add `D` (pydocstyle) only if docstring discipline becomes a problem.
- `ruff format` is the formatter. No black, no separate isort.

**Typing (mypy):**

- `model/` runs under `strict = true`. The model layer is the testable core; type rigor pays for itself.
- `controller/` and `config/` run under `strict = true`. Same reason.
- `view/` runs under a relaxed profile — `disallow_untyped_defs = true` but not full strict, because Qt's stub coverage has rough edges and fighting them is not worth the time.
- `tests/` runs unchecked except for `disallow_incomplete_defs = true` to keep test fixtures honest.

Configuration lives in `pyproject.toml` under `[tool.mypy]` with per-module overrides.

**Type hints:**

- All public APIs (anything not prefixed with `_`) require complete type hints on parameters and return values. Enforced by mypy strict mode in `model/`, `controller/`, `config/`.
- Internal helpers may omit hints where mypy can infer cleanly.
- Use `from __future__ import annotations` at the top of every module for forward-reference ergonomics.

**Docstrings:**

- Public model classes, public functions, and any non-obvious algorithm: Google-style docstrings.
- Private helpers: a single-line summary or no docstring at all.
- View widgets and Qt-specific glue: docstring optional; the Qt class hierarchy and method names usually carry intent.
- Don't write docstrings that just restate the function name. "Returns the ship" is not useful.

**Module-level conventions:**

- One class per module is *not* required. Group closely-related classes (e.g., all weapon-system components).
- `__all__` declared in modules with public APIs.
- Avoid circular imports by routing through `events.py` in the model and `model_bridge.py` in the controller — both are explicitly designed as decoupling seams.

**Naming:**

- Classes: `PascalCase`.
- Functions, methods, variables: `snake_case`.
- Module-level constants: `UPPER_SNAKE_CASE`.
- Qt signals: `snake_case` past tense (`ship_moved`, `turn_advanced`) to match Qt convention.
- Model events (blinker): same convention as Qt signals so the bridge translation is mechanical.

**Pre-commit hooks:**

- ruff format
- ruff check --fix
- mypy (cached)
- import-linter

`pre-commit install` is run after `uv sync`. CI re-runs all checks; pre-commit is a local convenience that catches issues before push.

### 10.7 Architecture Decision Records

Locked architectural and design decisions live in `docs/adr/` as one-page Markdown files following the lightweight ADR format (Context / Decision / Consequences / Status). The purpose is to anchor decisions in the repo so future Claude Code sessions — which may not have the project-instruction context — don't relitigate settled questions.

ADRs are not living documents. Once an ADR is marked `Accepted`, the decision is settled. Reversing it requires a new ADR that supersedes the old one explicitly (`Status: Superseded by ADR-NNNN`).

**Initial ADR set (seeded at scaffold time):**

| ADR | Title | Status |
|-----|-------|--------|
| 0001 | Pure-Qt rendering, no pygame or SDL | Accepted |
| 0002 | Linux-only, no Windows or macOS support | Accepted |
| 0003 | Model layer has zero Qt imports, enforced by import-linter | Accepted |
| 0004 | TOML for save/config, never pickle or dill | Accepted |
| 0005 | Hand-rolled state machine, not QStateMachine or transitions library | Accepted |
| 0006 | Procedural galaxy from v1.0, no hand-crafted maps | Accepted |
| 0007 | Captain progression is uncapped, level 100 is target not cap | Accepted |
| 0008 | Combat happens on the sector grid, not a separate combat scene | Accepted |
| 0009 | No audio in v0.1, full audio pass deferred to v1.0 | Accepted |
| 0010 | Hybrid auto-save: mode transitions plus N-turn fallback | Accepted |
| 0011 | v0.1 scope includes the starbase Dock action target | Accepted |
| 0012 | AI-generated visual assets via ChatGPT Images 2.0, prompts archived per-asset | Accepted |
| 0013 | Branch protection via ruleset with admin bypass, not classic protection | Accepted |

Each ADR is short — half a page typically, one page maximum. The `docs/adr/template.md` provides the format. New ADRs are added when a non-trivial architectural choice is made; trivial implementation choices stay out of the ADR log.

The README links to `docs/adr/` so contributors discover it without needing project context.

---

## 11. Marketing and Business

### 11.1 Distribution Strategy

Open source, public repo, free download. The repo is hosted at `github.com/chrisdpurcell/star-trek-retro-remake`. AppImage releases attached to GitHub releases. No app-store distribution.

### 11.2 Monetization Model

None. The project is non-commercial by design and by Star Trek IP requirement (see §12.1). No donations solicited at launch — though that may be revisited if hosting or distribution costs become non-trivial.

### 11.3 Community and Support

The repository is public and accepts issues and PRs. The v0.1 scaffold includes a CONTRIBUTING.md and basic issue templates so any drive-by contributors have a starting point. No formal community infrastructure (Discord, forums, etc.) is planned for the initial release; lightweight community channels can be added later if interest develops.

---

## 12. Legal and Compliance

### 12.1 Intellectual Property

This is an unofficial, non-commercial fan project. The legal posture has the following layers.

**Code:** MIT license, copyright Chris Purcell. The MIT license covers all original code in the repository.

**Star Trek IP:** Names, ships, factions, characters, and visual designs are intellectual property of CBS Studios Inc. / Paramount Global, including trademarks and copyrights. The MIT license **does not** cover this material. Non-commercial fan projects in the Trek space are generally tolerated under fair-use and unofficial-fan-work principles, but the boundary is real and explicit.

**Bundled fonts:** JetBrains Mono and VT323 are licensed under the SIL Open Font License 1.1. License text is included in `NOTICE.md` and travels with the fonts when redistributed; OFL permits bundling and use without per-asset cost.

**Required posture:**

- README disclaimer near the top:
  > This is an unofficial, non-commercial fan project. *Star Trek* and all related marks, characters, ships, and concepts are intellectual property of CBS Studios Inc. / Paramount Global, including trademarks and copyrights. This project is not affiliated with, endorsed by, or sponsored by CBS Studios or Paramount.
- No commercial monetization of any kind. Donations for hosting are a grey area; paid features or sale are not.
- No copied assets — sprites, audio, screenshots, or text from official Trek media are not committed to the repo.
- AI-generated **visual assets** must avoid reproducing canonical Trek designs. Prompts describe styling and silhouette — *"Klingon-style raptor cruiser"* rather than *"D7"* — to keep the AI from outputting direct copies of copyrighted artwork. The risk lives at the prompt layer; see §7.2 for the prompt archival workflow.
- Naming canonical classes, ships, characters, and concepts **in text** (UI labels, mission briefings, dialogue, comm log entries, NPC ship names) is acceptable under nominative fair use, as standard practice in non-commercial Trek fan works. The README disclaimer covers attribution; no obfuscation or rewording is needed in text content.
- README discloses that visual assets are AI-generated.
- `NOTICE.md` at the repo root documents the IP boundary for contributors and includes licenses for bundled assets (font licenses, any other third-party content).

### 12.2 Privacy and Data Protection

The game is a single-user desktop application. It does not collect, transmit, or store personal data. No telemetry, no analytics, no network calls beyond user-initiated actions (which are none in v1.0). All save data lives on the user's local machine.

### 12.3 Content Rating Considerations

The game is unrated. Content is roughly equivalent to an E10+ or T rating: tactical space combat without graphic violence, no profanity, no sexual content, no drug references. The retro aesthetic naturally avoids the kind of detailed violence that drives higher ratings.

### 12.4 Platform Compliance

No app-store distribution means no platform-specific compliance requirements. AppImage and direct GitHub releases sidestep the Microsoft Store, Mac App Store, and Steam Direct review processes entirely.

---

## 13. Future Development

### 13.1 Post-Launch Features (v1.1+)

- Audio pass: ambient music per mode, weapon and engine sound effects, UI feedback sounds
- Galaxy expansion beyond the initial 10×10 grid
- Additional ship classes (Excelsior, Federation dreadnought, Oberth science vessel)
- Mission variety expansion: archeology, first contact protocols, scientific surveys
- Diplomacy depth: dialogue trees, faction alliance shifts, treaty mechanics
- Crew event system: shore leave incidents, character development arcs
- Modding support: external TOML files for ships, missions, factions

### 13.2 Long-term Vision (v2.0+)

- Admiral rank and fleet command (multi-ship missions)
- Persistent galaxy state with faction-driven world events
- Advanced AI: tactical planning, formation flying, learning from player tactics
- Localization

These are aspirations, not commitments. Some may never happen. The v1.0 game is meant to be complete on its own.

---

## Appendix A: Reference Materials

### Classic Trek Games (inspiration)

- *Star Trek* (1971) — Mike Mayfield's original mainframe game
- *Super Star Trek* (1973) — David Ahl's BASIC port
- *Star Trek: 25th Anniversary* (1992) — adventure / strategy hybrid
- *Star Trek: Starfleet Command* series — tactical ship combat

### Star Trek Universe

- *Star Trek: The Original Series* (1966–1969) — primary era inspiration
- Key episodes: "Balance of Terror", "Space Seed", "The Doomsday Machine"

**Technical manuals:**

- *Star Trek: The Original Series Sketchbook*
- *Star Trek Starship Recognition Manual*
- *Star Fleet Technical Manual* by Franz Joseph
- *Mr. Scott's Guide to the Enterprise*

**Online:**

- Memory Alpha: <https://memory-alpha.fandom.com>
- Ex Astris Scientia: <http://www.ex-astris-scientia.org>

### Game Design References

- *XCOM* series — turn-based tactical mechanics
- *FTL: Faster Than Light* — ship system management and events
- *Into the Breach* — grid-based tactical gameplay
- *Master of Orion* series — 4X space strategy
- *Star Traders: Frontiers* — space RPG/strategy hybrid

### Technical Documentation

- Python 3.14+: <https://docs.python.org/3.14/>
- PySide6: <https://doc.qt.io/qtforpython-6/>
- pydantic v2: <https://docs.pydantic.dev/>
- python-tcod: <https://python-tcod.readthedocs.io/>
- blinker: <https://blinker.readthedocs.io/>
- loguru: <https://loguru.readthedocs.io/>
- qtawesome: <https://github.com/spyder-ide/qtawesome>
- pytest: <https://docs.pytest.org/>

### Books

- *Game Programming Patterns* — Robert Nystrom
- *Design Patterns* — Gamma, Helm, Johnson, Vlissides
- *The Art of Game Design* — Jesse Schell

### Linux Development

- `uv` package manager: <https://docs.astral.sh/uv/>
- `ruff` linter/formatter: <https://docs.astral.sh/ruff/>

### Asset Creation

- ChatGPT Images 2.0 (OpenAI) — sprite, anomaly, and background generation
- QtAwesome — UI iconography (no asset generation needed)
- GIMP — pixel cleanup and PNG export when needed

---

## Appendix B: Glossary

### Game Terms

**Action Points (AP):** Resource spent per turn for actions. Player ships have 5 AP/turn baseline. Movement: 1 AP/cell. Phasers: 1 AP. Torpedoes: 2 AP.

**Combat Mode:** Tactical turn-based ship combat on the sector grid with z-levels.

**Component:** Modular ship subsystem (weapons, shields, engines, sensors) that can be damaged, upgraded, or replaced.

**Difficulty Modes:** Four challenge tiers selected at new-game start — Cadet (forgiving, +2 AP, weaker enemies), Officer (default, balanced), Captain (harder, fewer AP, stronger enemies), and Admiral (expert, permadeath, scarce resources, maximum enemy stats). See §3.4.

**Facing:** Ship orientation in 45° increments. Affects firing arcs, shield coverage, and movement direction.

**Firing Arc:** 270° forward cone where weapons can target. Ships cannot fire behind themselves.

**Galaxy Map:** 10×10 grid showing all sectors for strategic navigation.

**Initiative:** Determines turn order. Higher acts first. Player: 10. NPCs: 6–9.

**Line of Sight (LoS):** Unobstructed path between grid positions. Required for targeting and detection. Computed via `tcod.los`.

**Mission:** Discrete objective-driven task assigned to the player, with primary objectives, optional secondary objectives, time/resource constraints, and rewards. Six types: Patrol, Escort, Reconnaissance, Combat, Rescue, Diplomatic. Procedurally generated from templates per sector. See §5.4.

**Object Pool:** Optimization that reuses game objects instead of creating and destroying them.

**Procedural Generation:** Algorithmic creation of game content from rule-based templates rather than hand-authoring. Used at v1.0 for galaxy layout (zone distribution, faction territories, starbase placement) and mission content. Each new game uses a different seed, producing a different galaxy per playthrough.

**Reputation:** Player standing with Starfleet Command, tracked separately from Captain Level (which is XP-based). Five ranks (Probationary → Officer in Good Standing → Commended Officer → Distinguished Service → Exemplary Record). Affects mission availability, starbase services, and random-event outcomes. See §3.3.

**Sector Map:** Up to 20×20×7 grid representing a single sector.

**Shield Facing:** Four directional shield zones (forward, aft, port, starboard) absorbing damage independently.

**State Machine:** Pattern managing transitions between game modes.

**Turn:** Complete cycle where entities execute actions in initiative order.

**Z-Level:** Vertical layer representing altitude/depth in space. Sectors have between 1 and 7 z-levels (varies by sector — flat 2D maps are valid for tight or constrained spaces). Ships can move between levels.

### Star Trek Terms

**Constitution Class:** Main Federation starship in the Kirk era. Balanced cruiser.

**Deflector Shields:** Energy barrier protecting ships. Four directional facings.

**Dilithium:** Rare element regulating matter/antimatter reactions in warp cores.

**Federation:** United Federation of Planets, democratic alliance of Earth and member worlds.

**Gorn Hegemony:** Reptilian species. Strong, territorial, slow but powerful ships.

**Impulse Drive:** Sublight propulsion using fusion reactors. Used for in-system travel and combat.

**Klingon Empire:** Warrior empire, often hostile to Federation. Values honor and combat.

**LCARS:** Library Computer Access/Retrieval System — Federation UI style (loose design inspiration).

**Nacelle:** Warp engine component with warp coils. Vulnerable, critical for FTL.

**Orion Syndicate:** Criminal organization. Known for piracy and smuggling.

**Phaser:** Phased Array by Stimulated Emission of Radiation. Primary Federation energy weapon.

**Photon Torpedo:** Antimatter warhead. High damage, limited ammunition.

**Romulan Star Empire:** Secretive empire from Vulcan exiles. Masters of cloaking and tactics.

**Starbase:** Large orbital or deep-space station. Repairs, supplies, mission briefings, command.

**Starfleet:** Military, exploration, and diplomatic service of the Federation.

**Tholian Assembly:** Crystalline beings with exotic energy tech. Territorial, use web weapons.

**Warp Drive:** FTL propulsion via subspace field. Warp factors 1–9.

### Technical Terms

**AAA Pattern:** Testing pattern: Arrange, Act, Assert.

**Component Pattern:** Complex objects composed of smaller, reusable components rather than via inheritance.

**ECS (Entity Component System):** Architecture where entities are containers for components and systems process components. Simplified to the Component Pattern in this game.

**GameObject:** Base class for interactive entities (ships, stations, projectiles) with position and state.

**Isometric View:** 2.5D projection showing 3D space at an angle with width, depth, and height.

**MVC (Model-View-Controller):** Architecture separating game logic (Model), rendering (View), and input handling (Controller).

**Object Pooling:** Memory pattern reusing inactive objects instead of allocating and deallocating repeatedly.

**State Machine:** Model managing discrete states and transitions based on events or conditions.

**TOML:** Tom's Obvious Minimal Language. Configuration file format. Human-readable, type-safe.

**Turn-Based:** Time advances in discrete turns rather than real-time, allowing strategic planning.

### Abbreviations

- **AI:** Artificial Intelligence (NPC behavior)
- **AP:** Action Points
- **FOV:** Field of View
- **FPS:** Frames Per Second
- **FTL:** Faster Than Light
- **HP:** Hull Points
- **LoS:** Line of Sight
- **NPC:** Non-Player Character
- **TOS:** *The Original Series*
- **UI:** User Interface
- **UX:** User Experience
- **XP:** Experience Points

---

## Appendix C: Change Log

See `/CHANGELOG.md` for complete version history. The current implementation begins at v0.1.0 with the pure-Qt scaffold; this is a fresh start in a new repository (`chrisdpurcell/star-trek-retro-remake`). The prior pygame-ce prototype (versions 0.0.1 through 0.0.25, in the deleted `L3DigitalNet/Star-Trek-Retro-Remake` repo) is no longer maintained. A local bare-repo mirror of the prototype is kept as a personal design-reference archive but is not part of the public project.

---

## Appendix D: Credits and Acknowledgments

- The Star Trek community, for decades of inspiration.
- The libtcod / python-tcod authors, for high-quality roguelike algorithms applicable far beyond their original domain.
- The PySide6 / Qt team.
- The pydantic, blinker, and loguru maintainers, and the Spyder team for QtAwesome.
- The Astral team (`uv`, `ruff`).
- All contributors listed in `CHANGELOG.md` once contributions exist.
