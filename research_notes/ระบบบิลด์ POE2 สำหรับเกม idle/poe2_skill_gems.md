# Path of Exile 2: Skill & Gem Build System (state as of Oct 14, 2026, live patch 0.5.5)

Scope note: notes on how skills are obtained, levelled, linked to supports and gated by resources in POE2, plus the patch-by-patch history from Early Access 0.1 to the current 0.5.5. The research ran with a limited tool budget. poe2wiki.net blocked automated fetches (Anubis bot wall), and maxroll and mobalytics returned 403/404 on several pages. As a result, primary-source coverage is strongest for the official 0.3.0 and 0.5.0 patch notes, with poe2db.tw for item and mod data. Labels: **[CURRENT]** = verified for 0.5.x. **[HIST x.y]** = changed in patch x.y. **[OLD]** = superseded.

---

## 1. What is the current version, and what changed in the gem system in each patch?

### Takeaway
As of October 2026, POE2 is still in Early Access. The live content patch is **0.5.0 "Return of the Ancients"** (league "Runes of Aldur", launched May 29, 2026), updated by **0.5.5 "Forbidden Rites"** (event patch, Sept 4, 2026, with no balance changes). **1.0 full release is set for December 11, 2026**: it adds the Duelist, swords and the remaining Acts, and the game becomes free-to-play. The biggest gem-system milestones were:
- **0.2.0**: Jeweller's Orbs changed from "add a socket" to "set the socket count".
- **0.3.0**: the one-copy support rule was removed, support tiers I/II/III were added (5 uncut-support levels), and 40 Lineage supports arrived.
- **0.4.0**: Druid/Primal category, 35+ new supports.
- **0.5.0**: 23 new Lineage supports, Kalguuran supports, Jeweller's Orbs on item skills, "+level" mods nerfed.

### Cited Findings
**Release timeline**
- 0.5.0 "Return of the Ancients" was scheduled for May 29, 2026, and was still the active league in late August 2026 — [Mobalytics 0.5.5 release-date guide](https://mobalytics.gg/poe-2/guides/0-5-5-release-date). The official patch notes thread is "Content Update 0.5.0 — Return of the Ancients", league "The Runes of Aldur" — [Official 0.5.0 patch notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Patch 0.5.4 was live by June 29, 2026 — [timesaver.gg Perfect Jeweller's guide (0.5.4)](https://timesaver.gg/blog/poe2-perfect-jewellers-orb-guide). Another 0.5.4 guide was updated 2026-08-09 — [stratlore charges guide](https://poe2.stratlore.com/en/guides/power-frenzy-endurance-charges/).
- 0.5.5 "Forbidden Rites" launched September 4, 2026 at 1 PM PDT — [Path of Exile on X](https://x.com/pathofexile/status/2095640480264433878). Official notes: [0.5.5 Patch Notes forum](https://www.pathofexile.com/forum/view-thread/4000864).
- 0.5.5 shipped with **no balance changes**, "citing a lack of development time". The latest hotfix found is 0.5.5c. Forbidden Rites runs alongside Runes of Aldur until 1.0 — [maxroll 0.5.5 notes](https://maxroll.gg/poe2/news/0-5-5-forbidden-rites-patch-notes); [patchbot 0.5.5c](https://patchbot.io/games/path-of-exile-2/articles/1477-055c-patch-notes).
- 1.0 was announced at gamescom ONL (article dated Aug 25, 2026). Release date is **December 11, 2026**. It adds the Duelist (sword-focused melee, sword-and-shield) and "the remaining campaign Acts", and the game goes fully free-to-play — [CGM gamescom ONL 2026](https://www.cgmagonline.com/news/gamescom-onl-2026-path-of-exile-2-official/); [Push Square](https://www.pushsquare.com/news/2026/08/path-of-exile-2-reaches-1-0-on-11th-december-goes-free-to-play-on-ps5); [RPGamer](https://rpgamer.com/2026/08/path-of-exile-2-fully-releasing-in-december/).
- 0.5 was described as the last major Early Access update before 1.0. The game has been in Early Access since December 2024 — [search summary of 1.0 coverage, frvr](https://frvr.com/blog/path-of-exile-2-1-0-releases-at-the-end-of-2026/).
- 0.4.0 "The Last of the Druids" released December 12, 2025 — [poe-vault](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids); [game8 0.4.0 notes](https://game8.co/games/Path-of-Exile-2/archives/569539). Official: [0.4.0 patch notes](https://www.pathofexile.com/forum/view-thread/3883495).

**Gem-system changes, patch by patch**
- **0.1.0 (Dec 2024)** [OLD rules]
  - Each support gem could be used only once per character. Players complained about this ("every support gem can only be used once").
  - Cast on Critical energy was hotfixed in 0.1.0 so that energy gain accounts for hit damage. This stopped low-level, high-crit skills from dominating.
  - Sources: [Official forum feedback threads](https://pathofexile.com/forum/view-thread/3410466); [CoC search summary / poe2wiki](https://poe2wiki.net/wiki/Cast_on_Critical).
- **0.2.0 "Dawn of the Hunt"**
  - Jeweller's Orbs now **set** a gem's support-socket count to a specified number instead of adding a socket.
  - Grim Feast was removed from Gemcutting for a rework. Skeletal Warrior was removed (existing gems became Skeletal Sniper).
  - Hammer of the Gods lost its cooldown and now requires 20 Glory.
  - Grenade cooldowns were lowered to 5 s in a hotfix.
  - Sources: [maxroll 0.2.0 notes](https://maxroll.gg/poe2/news/0-2-0-dawn-of-the-hunt-patch-notes); [official 0.2.0 notes](https://www.pathofexile.com/forum/view-thread/3740562).
- **0.3.0 "The Third Edict"**, from the official notes ([0.3.0 patch notes](https://www.pathofexile.com/forum/view-thread/3826682)):
  - "We've removed the restriction of having one of each support gem per character."
  - "You can no longer socket multiple copies of the same Skill Gem into your main skill sockets." Item-granted skills and Persistent Buff gems are exempt.
  - "Many Supports now have multiple tiers"; existing gems became tier 1.
  - "40 Lineage Supports … only available in Endgame."
  - Uncut Skill/Support/Reservation gems became tradeable on the Currency Exchange.
  - Unmet attribute requirements on a support now disable only that support, not the whole skill. Skill-gem attribute requirements were lowered.
  - Weapon swapping became instant.
  - Cast on Freeze/Shock/Ignite were merged into **Cast on Elemental Ailment** (100 Spirit, minimum level 14).
  - Flammability, Conductivity and Hypothermia were merged into **Elemental Weakness**.
  - "Infusion" supports were renamed "Attunement".
  - Gems sell to vendors for gold based on level and quality.
- **0.3.0 per Maxroll**: support gems went to **5 tiers instead of 3**, and all attribute requirements were cut by 25% — [maxroll 0.3.0 reveal summary](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- **0.4.0** ([poe-vault](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids)):
  - 35+ new support gems; Lineage supports expanded for all classes, and world-drop Lineage supports became less common.
  - Several supports changed attribute: Crescendo and Gambleshot moved to Int; Mark for Death and Brambleslam moved to Str.
  - Font of Rage and Ricochet III were disabled.
  - New meta gem **Spell Totem**.
  - 0.4.0d: spirit-reserving skills now display their final, modified reservation — [fextralife 0.4.0 notes](https://pathofexile2.wiki.fextralife.com/Patch_Notes_040).
- **0.5.0** ([official 0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540)):
  - **23 new Lineage supports**; **7 Kalguuran supports crafted from remnants** (e.g., Concussive Runes, Healing Runes, Scouring Flame); Minion Splash I/II.
  - Jeweller's Orbs can now add sockets to **skills granted by items**.
  - Skills with no cost (default attacks, item skills, triggered skills, crossbow ammo) now show **0 Mana cost** and can gain added costs.
  - "+X to Level" weapon mods nerfed: two-handed T1 +5 (was +7), one-handed T1 +4 (was +5); quiver "+2 Projectile skills" is now +1.
  - Seal mechanics unified.
  - Infernal Legion III, Shock Conduction II and Overextend were removed from drops.
  - One roundup counts **33 new support gems** in 0.5 — [rpgstash](https://www.rpgstash.com/blog/poe-2-return-of-the-ancients-new-support-gems).
- **1.0 gem changes**: no specific gem/support/spirit changes were described in the 1.0 announcement coverage — [CGM](https://www.cgmagonline.com/news/gamescom-onl-2026-path-of-exile-2-official/).

### Inferences
- The rules have been stable since 0.3.0: tiered supports, duplicates allowed, Lineage supports as an endgame chase. 0.4 and 0.5 mostly added content (more supports and Lineages) and tuned numbers. A designer should copy the 0.3+ ruleset, not the 0.1 one.
- GGG's direction has been to **remove friction**: duplicates allowed, instant weapon swap, uncut gems tradeable, supports disabled individually rather than killing the skill. They keep power gates in currency (Jeweller's Orbs) and chase items (Lineage supports).

### Gaps
- Exact release dates for 0.2.0 (believed April 4, 2025) and 0.3.0 (believed Aug 29, 2025) were not verified this session.
- The official 0.5.0 notes were read only up to about 100k of 165k characters, so later sections (unique items, bug fixes) were not checked.
- 1.0 patch notes are not yet published (release is Dec 11, 2026), so gem changes for 1.0 are unknown.

---

## 2. Uncut gems: drops, choosing a skill, gem level and tier, levelling, max level

### Takeaway
All skills come from **"Uncut" currency gems**, which come in three kinds: **Uncut Skill Gem**, **Uncut Support Gem** and **Uncut Spirit Gem**. An uncut gem's level is set by where it dropped. Right-clicking one opens a **Gemcutting menu**, where the player engraves ANY skill whose tier is at or below the uncut gem's level, or uses it to raise an existing gem to that level. Skill gems cap at **level 20 (21 via corruption)** and **20% quality**. Supports have **5 uncut levels**, which unlock tiers I to V of each support.

### Cited Findings
**Types and drops**
- Uncut gem types:
  - Uncut Skill Gem: creates or levels a gem; a quest variant creates a level-1 gem.
  - Uncut Spirit Gem: used for Persistent Buff gems.
  - Uncut Support Gem.
  - Spirit gems "can only be created using an Uncut Spirit Gem".
  - Source: [poe2wiki Uncut gem (search summary)](https://poe2wiki.net/wiki/Uncut_gem).
- The Uncut Skill Gem "can be used to engrave a skill gem or level up an existing skill gem to the level of the Uncut Skill Gem". It "can drop anywhere", has base drop level 4 (quest version 1) and max quality 20 — [poe2db Uncut Skill Gem](https://poe2db.tw/us/Uncut_Skill_Gem).
- The Uncut Support Gem is used to "engrave a Support Gem". It can drop anywhere and has drop level 4 — [poe2db Uncut Support Gem](https://poe2db.tw/us/Uncut_Support_Gem).
- Gem level depends on drop level. Wiki example: an Uncut Skill Gem from a normal monster in a level-40 area is always a level-10 gem. From drop level 62+, several tiers of uncut gems can drop on a weighting system — [poe2wiki Uncut gem (search summary)](https://poe2wiki.net/wiki/Uncut_gem). Caveat: two copies of the wiki page list different breakpoints.

**Engraving and levelling**
- An engraved gem takes the uncut gem's level. Gems are levelled further with uncut gems up to **level 20 (21 if corrupted)** — [poe2wiki Skill gem (search summary)](https://poe2wiki.net/wiki/Skill_gem).
- The uncut gem must be at least the skill's level, e.g., a level-7 skill needs a level-7+ uncut gem. The same rule applies to upgrading, and engraving consumes the uncut gem — [poe-vault gems guide](https://dev.poe-vault.com/poe2/guides/gems-guide).
- Skills are unlocked in **odd tiers 1, 3, 5, 7, 9, 11, 13** per weapon category in the Gemcutting menu — [poe2db Uncut Skill Gem](https://poe2db.tw/us/Uncut_Skill_Gem); [poe-vault](https://dev.poe-vault.com/poe2/guides/gems-guide).
- poe2db "Tier Level" table (labelled "Used for Item Implicit and Ascendancy Skill"):

  | Gem level | Required character level |
  |---|---|
  | 1 | 2 |
  | 2 | 3 |
  | 3 | 6 |
  | 4 | 10 |
  | 5 | 14 |
  | 6 | 18 |
  | 7 | 22 |
  | 8 | 26 |
  | 9 | 31 |
  | 10 | 36 |
  | 11 | 41 |
  | 12 | 46 |
  | 13 | 52 |
  | 14 | 58 |
  | 15 | 64 |
  | 16 | 66 |
  | 17 | 72 |
  | 18 | 78 |
  | 19 | 84 |
  | 20 | 90 |

  The table also gives support-socket counts for item/ascendancy skills: **3 at level 10, 4 at level 15, 5 at level 20** — [poe2db](https://poe2db.tw/us/Uncut_Skill_Gem).
- 0.3.0 changed some minimum gem levels, e.g., Blink "now has a minimum Gem level of 8 (previously 14)" — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).

**Support tiers**
- Support gems use Roman-numeral tiers. The number in parentheses is the uncut support level needed:
  - Armour Break I (2), II (3), III (4)
  - Brutality I (1), II (2), III (5)
  - Fist of War I (1), II (3), III (5)
  - Bleed I (1), II (3), III (5), IV (5)
  - Source: [poe2db Support Gems](https://poe2db.tw/us/Support_Gems).
- Higher tiers come from higher-level Uncut Support Gems, and tiers can add new effects. Example: Rapid Casting I gives 15% increased cast speed; II gives 20%; III gives "10% increased Cast Speed for each different Spell you've cast in the last eight seconds" — [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- 0.5.0 example: "Brink I: Can be Cut at level 1 (previously level 2)" — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).

**Trading, quality and level bonuses**
- Uncut gems are tradeable on the Currency Exchange (since 0.3.0) — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).
- Gem quality max is 20 — [poe2db](https://poe2db.tw/us/Uncut_Skill_Gem). Gemling Legionnaire (0.5.0): "Gem Quality now gives socketed skills an additional effect, and all gems gain an additional quality stat" — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Item modifiers add effective gem level above 20 (0.5.0 values):
  - Two-handed melee/projectile "+ to Level" T1: +5 (was +7)
  - One-handed T1: +4 (was +5)
  - Quiver: +1 Projectile skills (was +2)
  - Perfect Essence of Battle: +3 Attack skills on two-handed/crossbows (was +5), +2 on one-handed/bows (was +3)
  - Lineage Uhtred's Augury/Omen: +2 level to the supported skill under conditions
  - Source: [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- A Vaal Orb on a gem can add a socket (see §4), lower its level, change its quality, or do nothing — [timesaver.gg](https://timesaver.gg/blog/poe2-perfect-jewellers-orb-guide).

### Inferences
- **Core loop to copy:** skills are a "choose from a menu" unlock, not a random drop. The random part is the **level of the uncut currency**, which gates **which tier of skill** you can pick and **how high** you can level it. Levelling consumes a whole higher-level uncut gem, so there is no XP on gems. This decouples "what skill I want" (player choice) from "how strong it is" (loot progression). That is a strong fit for an idle game.
- The character-level requirement curve (level 20 gem needs character level 90) makes gem level a soft cap tied to player level.

### Gaps
- Gemcutter's Prism details (quality per use, current recipe) were not verified this session.
- The exact current area-level to uncut-gem-level mapping table could not be fetched (poe2wiki blocked).
- Exactly how Lineage and Kalguuran supports interact with the 5 uncut levels is unclear.
- How Uncut Spirit Gem levels are distributed was not found.

---

## 3. Skill gems: weapons, item-granted skills, attributes, weapon sets

### Takeaway
Skills are grouped into **weapon/archetype categories** in the Gemcutting menu. Most attacks **require the matching weapon** (bow skill needs a bow, and so on). Players have **9 skill-gem slots** by default. Some weapons (wands, sceptres, staves, spears, shields) **grant a built-in skill**. Each skill belongs to weapon set 1 and/or 2, and swapping between sets has been instant since 0.3.0.

### Cited Findings
**Gemcutting categories (8 listed, tiers 1–13)** — all from [poe2db Uncut Skill Gem](https://poe2db.tw/us/Uncut_Skill_Gem):

| Category | Tier-1 skills | Tier-13 skills |
|---|---|---|
| **Occult** (Witch) | Unearth, Contagion, Skeletal Sniper | Skeletal Brute, Skeletal Cleric, Soul Offering |
| **Bow** (Ranger) | Lightning Arrow, Escape Shot, Poisonburst Arrow, Lightning Rod | Magnetic Salvo, Spiral Volley, Toxic Domain |
| **Mace** (Warrior) | Rolling Slam, Boneshatter, Earthquake | Ancestral Cry, Hammer of the Gods, Ancestral Warrior Totem |
| **Elemental** (Sorceress) | Spark, Ice Nova, Flame Wall, Frost Bomb | Flameblast, Eye of Winter, Lightning Conduit |
| **Spear** (Huntress) | Disengage, Whirling Slash, Twister, Explosive Spear | Spear of Solaris, Wind Serpent's Fury |
| **Crossbow** (Mercenary) | Explosive Grenade, Permafrost Bolts, Fragmentation Rounds, Armour Piercing Rounds | Siege Cascade, Plasma Blast, Cluster Grenade |
| **Quarterstaff** (Monk) | Falling Thunder, Frozen Locus, Killing Palm, Glacial Cascade | Flicker Strike, Gathering Storm |
| **Primal** (Druid, added 0.4) | Lunar Assault, Entangle, Volcano, Furious Slam | Flame Breath, Lunar Blessing, Walking Calamity |

- Each category has about 20–27 skills spread across tiers 1/3/5/7/9/11/13. Notable mid-tier examples:
  - Bow: Tornado Shot at tier 11.
  - Elemental: Comet at tier 11; Incinerate at tier 9.
  - Quarterstaff: Charged Staff at tier 9.
  - Crossbow: Siege Ballista at tier 9.
  - Mace: Armour Breaker at tier 3; Earthshatter at tier 7.
  - Source: [poe2db](https://poe2db.tw/us/Uncut_Skill_Gem).
- No Sword category appears yet. Swords arrive with the Duelist in 1.0 — [CGM](https://www.cgmagonline.com/news/gamescom-onl-2026-path-of-exile-2-official/).

**Skill slots and item-granted skills**
- You start with **9 skill-gem slots**. The Gemling Legionnaire ascendancy (Mercenary) adds **3**. Some weapons, Unset Rings and uniques add more — [poe-vault gems guide](https://dev.poe-vault.com/poe2/guides/gems-guide).
- Wands, sceptres, staves, spears and shields **come with an attached active skill**. It counts toward your skills and can take supports, but disappears when the item is unequipped. Weapon basic skills cost no mana — [poe-vault](https://dev.poe-vault.com/poe2/guides/gems-guide).
- Since 0.5.0, skills granted by items can be socketed via Jeweller's Orbs. If an item grants several skills, the orb affects all of them — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540); [timesaver.gg](https://timesaver.gg/blog/poe2-perfect-jewellers-orb-guide).
- 0.3.0: you cannot socket multiple copies of the same skill gem in main skill slots — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).

**Attributes and colours**
- Support gems are grouped as Strength, Dexterity or Intelligence; some Spirit gems have attribute requirements — [poe-vault](https://dev.poe-vault.com/poe2/guides/gems-guide).
- Attribute requirements were cut ~25% in 0.3.0 — [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- Unmet requirements on a support now disable only that support — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).
- Supports move between attributes in patches, e.g., Crescendo changed from Dex to Int in 0.4.0 — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).

**Weapon sets**
- "Swapping weapons is now instant" (0.3.0). Blink, Convalescence and Sacrifice "are now required to be active in both weapon sets" — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).
- 0.5.0: Eternal Rage must be active in both weapon sets. When minions are removed due to weapon swapping or resource changes, newer minions are removed first — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Available Spirit can differ between weapon sets (because of sceptres and weapon-set passives) — [poe2db Spirit](https://poe2db.tw/us/Spirit). Reservations adjust dynamically when you swap, so a build can fail if one set has less Spirit — [maxroll spirit guide (search summary)](https://maxroll.gg/poe2/guides/spirit-guide).

### Inferences
- Weapon categories act as **"skill trees by weapon"**: about 8 pools of ~25 skills, each unlocked progressively by tier. For an idle game, this suggests "weapon type = skill pool" plus a "tier unlock by uncut level" ladder.
- The weapon-swap design lets one character hold two loadouts. Example: a sceptre in set 2 for extra Spirit, or a second weapon type for utility skills.

### Gaps
- The exact per-gem attribute requirement formula was not retrieved.
- The red/green/blue colour terminology for POE2 gems was not confirmed. Gems are described by attribute (Str/Dex/Int) in the sources found.
- The full list of base weapon-implicit skills per base type was not retrieved.
- Talisman/shapeshift skill details (Druid) were only seen as the "Primal" category.

---

## 4. Support gems: sockets, Jeweller's Orbs, duplicate rule, tiers, Lineage supports

### Takeaway
Supports live **inside the skill gem**, not in gear. Every skill gem starts with **2 support sockets**. Three currencies **set** it to 3/4/5 sockets (max 5):
- **Lesser Jeweller's Orb**: sets 3 sockets (item level 25)
- **Greater Jeweller's Orb**: sets 4 sockets (item level 45)
- **Perfect Jeweller's Orb**: sets 5 sockets (item level 65)

Since 0.3.0, the same support can be used on any number of skills. Supports come in tiers I to V, and **Lineage supports** are drop-only, unique-like endgame supports. There are 40 from 0.3, more in 0.4, and 23 new in 0.5.

### Cited Findings
**Sockets and Jeweller's Orbs**
- Each skill gem starts with 2 support sockets; maximum is 5. Lesser sets 3, Greater sets 4, Perfect sets 5. Item levels are Lesser 25, Greater 45, Perfect 65. Perfect orbs stack to 20 — [timesaver.gg (0.5.4)](https://timesaver.gg/blog/poe2-perfect-jewellers-orb-guide).
- Greater Jeweller's Orb text: "Sets a Skill Gem to have 4 Support Gem Sockets." It only applies to gems with fewer than 4 sockets. Drop level is 45 — [poe2db Greater Jeweller's Orb](https://poe2db.tw/us/Greater_Jewellers_Orb).
- Each active skill can have up to 5 support gems — [poe-vault](https://dev.poe-vault.com/poe2/guides/gems-guide).
- Perfect orb sources:
  - Monster drops at item level 65+.
  - Zarokh, the Temporal (Trial of the Sekhemas).
  - The Currency Exchange.
  - A Vaal Orb on a 4-socket gem has a small chance to add a 5th socket.
  - There is no recipe that combines lower orbs into a Perfect one.
  - Source: [timesaver.gg](https://timesaver.gg/blog/poe2-perfect-jewellers-orb-guide).
- **[OLD]** Before 0.2.0, orbs added one socket to a gem with exactly N sockets. 0.2.0 changed them to "set to N" — [maxroll 0.2.0 (search summary)](https://maxroll.gg/poe2/news/0-2-0-dawn-of-the-hunt-patch-notes).
- Player complaint: unlocking the next support row is tied to Jeweller's Orb drops — [forum "Feedback: Jeweler's Orb System"](https://www.pathofexile.com/forum/view-thread/3648000).

**Duplicate rule**
- **[OLD 0.1–0.2]** Only one copy of each support per character.
- **[CURRENT since 0.3.0]** "We've removed the restriction of having one of each support gem per character" — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682). Example: Martial Tempo on every attack — [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- No source found says 0.4 or 0.5 re-introduced a limit — [search summary of 0.4 coverage](https://www.itemd2r.com/blog/poe-2/big-buff-for-all-builds-in-path-of-exile-2-support-gem-rule-change-in-update-03).

**Tiers and counts**
- 5 uncut tiers since 0.3.0 (previously 3). Supports are named I/II/III (some IV/V). Higher tiers can add new effects — [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary); [poe2db Support Gems](https://poe2db.tw/us/Support_Gems).
- poe2db's support list header shows "/557". This likely counts all tiers plus Lineage and disabled entries, and is not a count of unique choices — [poe2db](https://poe2db.tw/us/Support_Gems).

**Lineage supports**
- Introduced in 0.3.0, with 40+ at launch. They are endgame-only, "treated as Unique support gems", and cannot be cut from uncut supports; they must drop. Some drop only from specific bosses, others from regular monsters — [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary); [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682). They are mostly found in Abyssal domains — [sportskeeda lineage list (search summary)](https://www.sportskeeda.com/mmo/path-exile-2-lineage-support-gems-poe2).
- Lineage supports in 0.5 roundups are usable from level 65 — [rpgstash](https://www.rpgstash.com/blog/poe-2-return-of-the-ancients-new-support-gems).
- 0.5.0 added 23 new Lineage supports: Arbiter's Reach, Breachlord's Amalgam, Catha's Brilliance, Eonyr's Thunder, Esh's Prowess, Helbrym's Hide, Her Declaration, Olroth's Conviction, Olroth's Hubris, Medved's Felling, Mórrigan's Insight, Prototype Seventeen, Seraph's Heart, Styrn's Ferocity, Styrn's Mountain, Tangmazu's Thurible, Trickster's Shard, Tul's Avalanche, Uhtred's Constellation, Uhtred's Rite, Vorana's Siege, Vruun's Inevitability, Vruun's Aftermath — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Example Lineage effects (0.5.0 values), from [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540) unless noted:
  - **Uhtred's Augury**: +2 level to the supported skill if it has exactly two other supports. **Uhtred's Omen**: +2 if exactly one other support. Both were +3 before. These are "fewer links, more power" trade-offs.
  - **Dialla's Desire**: +5% quality to the supported skill (was +10%).
  - **Paquate's Pact**: supported skills cost 10% of max Life for each recent use, up to 30%.
  - **Bhatair's Vengeance**: 1% of damage as Cold per 2 Rage for 15 s.
  - **Ratha's Assault**: loads 4 bolts on dodge.
  - **Xoph's Pyre**: 40% of Fire as extra Chaos (0.4.0) — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).
- 0.4.0 made world-drop Lineage supports less common — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).
- **Kalguuran supports (0.5.0)**: 7 supports crafted from league "remnants", e.g., Concussive Runes, Healing Runes, Scouring Flame — [0.5.0 search summary](https://www.pathofexile.com/forum/view-thread/3932540).

**Examples of normal supports and recent tuning**
- Rapid Casting I/II/III (above).
- **Martial Tempo** (attack speed; usable on every attack since 0.3).
- **Culmination II** (Combo). 0.5.0: max 10 combo (was 20), 4% more damage per combo (was 2%), lost after 6 s.
- **Salvo**: 1 seal per 1 s, up to 6 (was 2 s, up to 3).
- **Rage I–III** can support minions.
- **Mark of Siphoning**: 8% physical attack damage leeched as mana.
- **Elemental Weakness**: merged curse.
- **Efficiency I/II** cannot support Spirit-reserving skills.
- **Hulking Minions** significantly raises minion Spirit cost.
- Sources: [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540); [poe2db Spirit](https://poe2db.tw/us/Spirit); [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- 0.4.0 new supports include: Accelerated Growth, Tectonic Slam, Fan the Flames (spreads fire between ignited enemies), Advancing Storm, Echoing Cry (repeats warcries), and Grounding Shocks (shocked enemies pulse arcs) — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).

### Inferences
- The depth comes from **three layers of support progression**:
  1. **Socket count**: a currency chase, 2 to 5.
  2. **Support tier**: I to V, from uncut level.
  3. **Lineage**: unique chase supports with conditional, build-warping effects, e.g., "+2 levels if exactly 1 other support".
- An idle game could map these to: slots unlocked by a rare currency; tier upgrades via level-gated tokens; and rare "legendary" supports with conditions that create trade-offs.
- Removing the one-copy rule made builds easier and stronger. The old rule forced trade-offs between skills. An idle designer could choose either. "Each support once" adds puzzle depth but frustrates players (see §8).

### Gaps
- Exact Lesser Jeweller's Orb text wasn't fetched directly; "sets 3" is from secondary sources.
- The current count of unique support gems (excluding tiers) was not reliably found.
- Mana-cost multipliers of individual supports were not retrieved.

---

## 5. Spirit and Spirit gems

### Takeaway
**Spirit** is a separate resource, starting at **0**, that is **reserved** by persistent skills: auras, heralds, permanent minions, companions, totems (under Ancestral Bond), and meta gems like Cast on Critical. Reservations don't drop on death. Sources:
- **About 100 from campaign boss rewards**
- **Sceptres** (100 base per wiki; % Spirit mods)
- **Flat Spirit on body armour, amulets and helmets**
- Passives and uniques

Typical costs:
- Herald of Ice: 30
- Blink: 60
- Cast on Critical / Cast on Elemental Ailment: 100
- Ancestral Bond totems: 75 each

### Cited Findings
**What Spirit is**
- Spirit activates and maintains permanent-effect skills, managed in the Skills Panel. Reservations do not deactivate on death. Characters start with 0 Spirit — [poe2db Spirit](https://poe2db.tw/us/Spirit).

**Campaign rewards**
- Campaign totals still +100 Spirit, after the removal of Cruel difficulty — [poe-vault "Does POE2 campaign still grant 100 Spirit?"](https://www.poe-vault.com/poe2/news/does-path-of-exile-2-campaign-still-grant-100-spirit).
- Breakdown: +30 from **The King in the Mists** (Act 1, Freythorn), +30 from **Ignagduk, the Bog Witch** (Act 3, Azak Bog). The +40 source is listed inconsistently: Act 6 / Cruel Act 3 Ignagduk (Gemcrust Skull) or Interlude boss Lythara — [game8 spirit quests](https://game8.co/games/Path-of-Exile-2/archives/489761); [mobalytics 0.5 campaign checklist](https://mobalytics.gg/poe-2/guides/0-5-campaign-checklist-stats-rewards-skillpoints-and-more).
- Quest items: Gembloom Skull +30, Gemrot Skull +30, Gemcrust Skull +40, Uhtred's Boon +10 — [poe2db Spirit](https://poe2db.tw/us/Spirit).

**Item and passive sources**
- **Sceptres** grant 100 Spirit (per community wiki). %Spirit prefixes on sceptres:
  - (10–14)% up to (35–38)% combined with mana
  - Pure % tiers from Lord's (20–26)% to King's (61–65)%
  - Source: [poe2db Spirit](https://poe2db.tw/us/Spirit).
- Body Armour flat Spirit prefixes: +(30–33) at level 16 up to **+(57–61)** at level 78.
- Amulets roll the same flat ranges; Solar Amulet base +(10–15).
- Helmets: corrupted +(20–30), unique +(40–50).
- Rune of the Blossom (body) +50 Spirit, −1 per 2 levels.
- Passive nodes 4% increased Spirit.
- Ascendancy sources: Infernalist Beidat's Will (+1 Spirit per 25 max Life); Shaman Sacred Flow (+40 Spirit per empty Charm slot); Smith of Kitava's Tribute to Utula (30% increased Spirit from body armour).
- Source for the items above: [poe2db Spirit](https://poe2db.tw/us/Spirit).
- 0.5.0: Rabbit Idol (sceptre) 15% increased Spirit (was 10%); Soul Mantle (unique body) now **+75 Spirit**. Spirit system otherwise mostly unchanged in 0.5 — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540); [rpgstash spirit guide (search summary)](https://www.rpgstash.com/blog/path-of-exile-2-how-to-get-more-spirit-poe2).

**Costs**
- **Herald of Ice**: 30 Spirit, from an Uncut Spirit Gem — [poe2wiki Herald of Ice (search summary)](https://www.poe2wiki.net/wiki/Herald_of_Ice).
- **Blink**: 60 Spirit — [poe2wiki Blink (search summary)](https://www.poe2wiki.net/wiki/Blink).
- **Cast on Critical**: 100 Spirit, from an Uncut Spirit Gem — [poe2wiki CoC (search summary)](https://poe2wiki.net/wiki/Cast_on_Critical).
- **Cast on Elemental Ailment**: 100 Spirit, minimum level 14 (0.3.0). The older separate Cast on Freeze/Shock/Ignite gems cost 60 each — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682); [search summary](https://www.rpgstash.com/blog/path-of-exile-2-how-to-get-more-spirit-poe2).
- **Ancestral Bond** keystone: totem limit doubled, totems reserve 75 Spirit each (100 before 0.3.0); placing totems needs no charge (0.5) — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682); [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- **Spectres**: high-Spirit spectres were made generally cheaper in 0.3.0 — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).

**Reservation modifiers**
- Matsya: skills reserve 50% less.
- Lord of the Wilds: 50% less Spirit; non-minion skills get 50% less efficiency.
- Self Sacrificing: −20% efficiency, +40% for minions.
- **Kaom's Heart: "You have no Spirit"**.
- Atziri's Communion support: persistent skills reserve Life instead.
- Source: [poe2db Spirit](https://poe2db.tw/us/Spirit).
- 0.5.0 Trusted Kinship keystone: companions 30% more reservation efficiency, non-companions 20% less. Bear Idol: 12% companion efficiency — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Tame Beast (0.5.0): newly tamed beasts summon immediately if you have enough Spirit — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).

**Spirit-reserving gem types**
- Minion gems: Spectre, Skeletal Warrior, Azmerian Wolf, Raging Spirits, Ancestral Spirits.
- Persistent buffs: Blasphemy, Lingering Illusion, Eternal Rage, Profane Commander.
- Source: [poe2db Spirit](https://poe2db.tw/us/Spirit).

### Inferences
- Spirit is a **second budget axis** next to mana. It's a fixed pool (~100 campaign + 100 sceptre + ~60 body + ~50 amulet ≈ 250–350 typical) that you "spend" on always-on effects. Costs come in chunks (30/60/100), which makes it a **knapsack choice**, e.g., 3 heralds vs 1 meta gem.
- For an idle game: a "Spirit = passive-slot budget" works very well. Persistent buffs and minions cost a fixed share, and gear pieces trade damage stats for Spirit.

### Gaps
- Costs for Archmage, Grim Feast (reworked), Wind Dancer, other heralds and minion gems (per minion) were not verified. maxroll's spirit guide 404'd and mobalytics returned 403.
- The exact Act/boss for the +40 Spirit in the current 0.5 campaign is inconsistent across sources.

---

## 6. Meta gems, Energy, invocations, charges, combo, and synergies

### Takeaway
**Meta gems** are Spirit-reserving containers that **trigger socketed spells** when they reach max **Energy**:
- Cast on Critical
- Cast on Elemental Ailment
- Cast on Dodge
- Spell Totem
- Invocations

Energy is gained from game events (crits, ailments, dodges) and scaled by hit size. Build identity is reinforced by **charges** (Power/Frenzy/Endurance, usually max 3, consumed by skills for empowered versions), **Monk Combo**, **Rage** and **Glory**. **Ailment and debuff interactions** also shape builds: freeze buildup leads to shatter, armour break leads to fully broken, and there are electrocute, heavy stun and ignite.

### Cited Findings
**Meta gems and Energy**
- Cast on Critical:
  - Reserves 100 Spirit.
  - Gains 1 energy per point of enemy Power you crit, adjusted by how much of the enemy's ailment threshold the hit dealt (0.1.0 hotfix added hit damage).
  - Max energy = 10 per 0.1 s of the socketed spell's base cast time.
  - Spark and Comet are common payloads.
  - Source: [poe2wiki CoC (search summary)](https://poe2wiki.net/wiki/Cast_on_Critical); [official forum CoC thread](https://web.poecdn.com/forum/view-thread/3927079).
- 0.3.0: Cast on Freeze/Shock/Ignite merged into Cast on Elemental Ailment (100 Spirit). Ritual Cadence makes Invocations fire every 2 s, and "triggered skills consume less Energy" — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682).
- 0.4.0: Spell Totem meta gem added; totems cast socketed spells using Power or Endurance charges — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).
- 0.5.0 changes — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540):
  - Spell Totem can be used while moving.
  - Feral Invocation no longer bypasses the cooldown of socketed skills.
  - Flame Breath gains an Energy-gain penalty like Incinerate.
  - Mirage Archer can be used with channelled skills.
  - Triggered skills now show a 0 mana cost that can gain added costs.

**Charges**
- Charges commonly default to max 3, gained 1 per trigger, and give no passive bonus while held; they exist to be spent — [stratlore charges guide (0.5.4)](https://poe2.stratlore.com/en/guides/power-frenzy-endurance-charges/).
- Generators and consumers ([stratlore](https://poe2.stratlore.com/en/guides/power-frenzy-endurance-charges/)):

  | Charge | Generated by | Consumed by |
  |---|---|---|
  | **Power** | Killing Palm (on kill) | Falling Thunder (extra projectiles), Charge Infusion |
  | **Frenzy** | Combat Frenzy (on Freeze/Electrocute/Pin), Cull the Weak, Parry + Disengage, Sniper's Mark | Barrage (extra repeats) |
  | **Endurance** | Magma Barrier (block), Break Endurance (full armour break), Cranial Impact (heavy stun on rare/unique) | Infernal Cry, Seismic Cry, Rally |

- **Resonance** keystone rotates charge types: Power replaces Frenzy, Frenzy replaces Endurance, Endurance replaces Power. Sources conflict on the exact mapping — [stratlore](https://poe2.stratlore.com/en/guides/power-frenzy-endurance-charges/).
- Oil Barrage (0.5.0): Empowered version consumes a Power Charge every 1.5 s (was 2) — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).

**Combo, Rage, Glory**
- Combo (Monk/quarterstaff): Culmination II, 0.5.0 values — lose combo after 6 s without generating, max 10 combo, 4% more damage per combo — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).
- Rage: Rage I–III can support minions (0.5); Enraged Warcry and Rageforged count as spending Rage (0.4) — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540); [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).
- Glory: Hammer of the Gods requires 20 Glory (0.2) — [maxroll 0.2.0](https://maxroll.gg/poe2/news/0-2-0-dawn-of-the-hunt-patch-notes).

**Ailments and debuffs**
- **Freeze**: hits below the ailment threshold add Freeze Buildup; at 100%, a fixed-duration freeze applies. Killing a frozen monster **shatters** it (no corpse); unique bosses cannot shatter.
- **Electrocute**: interrupts for 5 s by default; only specific skills' lightning hits build it.
- **Heavy Stun**: from a filled stun bar; physical and player melee damage cause 50% more buildup; cold hits build freeze, not heavy stun.
- **Fully Armour Broken**: e.g., a Warpick that breaks armour by 40% of damage and makes "Fully Armour Broken enemies you kill" shatter. Breachlord's Rift breaks armour on freeze/electrocute.
- Sources: [poe2wiki Freezing / Shatter / Electrocute (search summary)](https://www.poe2wiki.net/wiki/Freezing); [mobalytics freeze](https://mobalytics.gg/poe-2/guides/freeze).
- Support example: Armour Break I/II/III (tiers 2/3/4) — [poe2db](https://poe2db.tw/us/Support_Gems).
- Ignite synergy: Fan the Flames spreads fire between ignited enemies (0.4) — [poe-vault 0.4](https://www.poe-vault.com/poe2/news/poe2-adds-35-new-support-gems-in-the-last-of-the-druids).

### Inferences
- The signature POE2 pattern is **"setup → payoff"**: one skill applies a state (freeze buildup, armour break, mark, charges, combo), and another skill or support consumes it for a big effect (shatter, empowered skill, extra projectiles). Meta gems automate the payoff via Energy.
- This maps well to an idle game as **status stacks + finisher triggers**: "skill A builds X; at threshold, skill B fires automatically".
- Charges giving no passive stat bonus (only spent) makes them pure combo resources, which is easy to simulate.

### Gaps
- Cast on Dodge, Cast on Minion Death and other meta gems' exact costs and energy rules were not verified this session.
- The full Invocation list and their energy sources were not verified.
- Detonate Dead/corpse interactions were not researched.
- The exact ignite formula (damage % per second) was not retrieved.

---

## 7. How mana costs, cooldowns and limits shape builds

### Takeaway
Mana costs scale up with gem level, so higher levels cost more. Several skills use **cooldowns** affected by "cooldown recovery rate". Others use alternative gates: **Glory**, **charges**, **seals**, and **max active counts** (bells, pustules, totems, minions). Many basic and item skills are free. Supports (Efficiency, Paquate's Pact life cost) and keystones (Ancestral Bond) let players trade one gate for another.

### Cited Findings
**Mana costs** — all from [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540)
- Cull the Weak: 8–42 mana at gem level 3–20 (was 9–46); attack speed 75% of base.
- Oil Barrage: mana cost −18%.
- 0.5.0: default weapon attacks, item-inherent and triggered skills and crossbow ammo skills now have a **0** base mana cost that can gain added costs.
- Paquate's Pact (Lineage): supported skills cost 10% of max Life per recent use, up to 30%.

**Cooldowns** — all from [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540) unless noted
- Pounce: 6–5.1 s at gem level 3–20 (was 4.9–4).
- Ghost Dance: every 11.7–10.1 s, now affected by cooldown recovery.
- Time of Need: 9.3–8.1 s.
- Grim Resurrection: 1 s cooldown.
- Inevitable Agony (Chronomancer): 2 s cooldown.
- Ravenous Swarm, Align Fate and Mirror of Refraction: spawn frequency now scales with cooldown recovery rate.
- Grenade cooldowns: 5 s (0.2 hotfix) — [maxroll 0.2.0](https://maxroll.gg/poe2/news/0-2-0-dawn-of-the-hunt-patch-notes).

**Seals**
- Salvo: gains 1 seal/s up to 6. Unleash/Expand/Salvo/Freezing Salvo share one Seal system — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).

**Limits** — all from [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540) unless noted
- Tempest Bell: max 3 active (was 1).
- Toxic Growth: 5 pustules, limit 5 (was 12).
- Ancestral Bond: totem limit doubled, 75 Spirit each.
- Living Lightning no longer replaces minions when at max.
- Command skills: movement penalty 50% (was 70%).
- Efficiency I/II cannot support Spirit-reserving skills — [poe2db Spirit](https://poe2db.tw/us/Spirit).

### Inferences
- POE2 uses **many different gating currencies**: mana, cooldown, charges, combo, Glory, seals, energy, and Spirit for persistents. Each archetype "feels" different because its rhythm is defined by a different gate.
- For an idle game, a simplification is to give each skill **one gate type** (cooldown, stack/charge, or Spirit reservation). Supports or keystones then convert between gates, e.g., "pay life instead of mana" or "no cooldown but needs 20 Glory".

### Gaps
- Default totem and minion limits (base number of totems, per-gem minion caps) were not retrieved.
- A comprehensive mana-cost-per-level table was not retrieved.

---

## 8. What makes the system feel deep (strengths and complaints)

### Takeaway
Players praise the freedom: any character can cut any skill, test supports, and swap loadouts. They also like the progressive support tiers and Lineage chase items. Commonly cited complaints include:
- The old **one-copy support rule** (removed in 0.3).
- **Support rows locked behind Jeweller's Orb drops.**
- A fixed **9 skill slots** with sockets moved off gear, which some feel lost POE1's gear–skill tie and progression.
- Uncut gems feeling like "another layer of grind".
- Supports being mostly damage-only ("purely offensive").

### Cited Findings
- **Positive**: "the new skill gem system feels great: I can try out all these different skills, fool around with the supports, and it's awesome" — [official forum feedback thread](https://pathofexile.com/forum/view-thread/3410466).
- **Gems vs gear**: removing sockets from items gives every character the same fixed number of skill sockets, with no progression via gear base types. "Exactly 9 skill sockets feels very arbitrary." The changes "go too far in reducing variance" — [official forum](https://www.pathofexile.com/forum/view-thread/3632170).
- **Jeweller's Orbs**: players were frustrated that unlocking the next support row was tied to the Jeweller's Orb system — [forum "Feedback: Jeweler's Orb System"](https://www.pathofexile.com/forum/view-thread/3648000).
- **One-copy rule [OLD]**: players complained that "every support gem can only be used once". GGG removed it in 0.3.0, and coverage called it "a big buff to all builds" — [forum](https://www.pathofexile.com/forum/view-thread/3410466); [sportskeeda](https://www.sportskeeda.com/mmo/path-exile-2-support-gem-rule-change-0-3-poe2-third-edict).
- **Uncut gems** are criticised as "just another layer of grind"; supports "solve only how to kill things faster"; "utility skills are gone" — [forum threads](https://www.pathofexile.com/forum/view-thread/3590389).
- **GGG friction-reduction** responses in 0.3.0: tradeable uncut gems, instant weapon swap, supports disabled individually on unmet attributes, 25% lower attribute requirements — [0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682); [maxroll 0.3.0](https://maxroll.gg/poe2/news/patch-0-3-0-the-third-edict-reveal-summary).
- **Balance churn on chase items**: Lineage supports get frequent numeric nerfs, e.g., Uhtred's +3 to +2 and Dialla's +10% to +5% in 0.5.0 — [0.5.0 notes](https://www.pathofexile.com/forum/view-thread/3932540).

### Inferences
Depth drivers worth recreating:
1. **Choice-from-menu skill unlocks** gated by a randomly-levelled currency.
2. **Per-skill support slots (2→5)** as a long-term currency chase.
3. **Tiered supports** with new effects at higher tiers.
4. **Conditional "Lineage" supports** that warp build rules.
5. **Spirit as a separate reservation budget** for always-on effects.
6. **Setup→payoff ailments and charges** plus Energy-based auto-triggers.
7. **Two weapon sets** for dual loadouts.

Pitfalls to avoid, per player complaints:
- Global uniqueness limits on supports.
- Hard currency gates on basic slot counts too early.
- An overly fixed skill-slot count without progression.
- A gem economy that feels like grind.

### Gaps
- No 2026 (0.5-era) sentiment surveys or reviews specific to the gem system were found. Most complaint sources date from 0.1–0.2 (2024–2025).
- No reliable sources were found on gem respec costs. Gems are not consumed on unsocketing per general knowledge, but this was not verified this session.
