# G5 expansion — Codex handoff

Date: 2026-10-14 (Asia/Bangkok).
Agent: Codex, GPT-6 assistant. Tool: built-in image_gen (underlying image model not exposed).
Status: requested character concepts and comparison sheets saved; production pixel palette/anatomical cleanup still belongs to the integrator.

## Scope and decisions

Interpreted "two additional melee, remove hammer" as replace the hammer slot with a brawler and add an assassin: 4 melee total. Preserve the round-eared ranged character; replace sling with two alternative weapon loadouts. Revise Noll into a summoner with centre-held upright staff. Old images are retained.

User's attached references informed the mechanical fists, ninja silhouette, small heavy-weapons gunner and woodland summoner. Actual local templates passed to generation are recorded in prompts-v1.json. Franchise references inform roles; this roster keeps its original identities and clothing.

## Exact tool prompts

- prompts-v1.json stores verbatim brawler, assassin, twin guns and summoner prompts plus reference paths.
- laser-prompt-v1.txt stores verbatim heavy-laser edit prompt. Target was ranged-gunner-dual-raw-v1.png.
- All first four images used the existing grey-bodysuit chibi template. Gunner and summoner also used their previously accepted Codex concepts.

## Files and recommended versions

All paths below are relative to design/concepts/characters-g5-expansion-codex-v1/.

- melee-brawler-v1.png — 512x512; recommended.
- melee-assassin-v1.png — 512x512; recommended.
- ranged-gunner-dual-v1.png — 512x512; recommended twin-gun mode.
- ranged-gunner-laser-v1.png — 512x512; recommended heavy mode.
- mage-summoner-v1.png — 512x512; recommended.
- Matching five *-raw-v1.png files — each 1254x1254; every generation attempt retained as original PNG.
- changes-lineup-v1.png — 1536x1024.
- roster-lineup-v1.png — 2048x1536.
- characters.md — names, races, hooks, ramps, weapons and 3 move ideas per character.
- prompts-v1.json, laser-prompt-v1.txt, export-v1.py and verification-v1.json.

## Export and verification

Built-in images arrived as PNG1254x1254. No JPEG conversion. Non-creative export samples to64x64 then enlarges nearest-neighbour8x, normalizes keyed green to#00B140, and aligns lowest foreground row to62. All five already met row62: no vertical shifts. File sizes and bounding boxes are recorded in verification-v1.json. No side clipping; summoner antlers reach row2, laser reaches column60, within side margins.

Inspected all five generated images and the saved changes lineup. Fists, two separate daggers, two guns, one large cannon and upright centre-shaft staff are visible. Existing hammer is omitted from the new roster comparison but never deleted.

## Brief deviations / limitations

- The underlying generator approximates the anatomical template; exact original eye/hand/foot pixels are not protected. Head-to-body proportions remain visually chibi, with hats/hair/ears/antlers extending as permitted.
- Output is on a strict8x8 grid with flat chroma background, but foreground colours still have intermediate shades and the dark outline is not exactly#2e1816 throughout. characters.md supplies intended3-shade material ramps for palette locking.
- Brawler keeps a fuller raspberry bob rather than exposing a pronounced undercut. Both fists are visible.
- Staff is upright and hand wraps its central shaft; complete ornament-to-bottom length is longer than the nominal26-art-pixel target. Including ornamental head it is about35px, still shorter than the character. Centre grip is visually approximate when measured over the full staff ornament rather than just shaft.
- Gunner identity is visually preserved across loadouts, but exact shared pixels may differ. Before animation, integrator can restore common head/body pixels from the chosen gunner template.
- Summon creature concepts are documented as future move ideas, not generated in this task.
- Old hammer/sling pixels and existing game files untouched. No PixelLab, MiniMax, external paid generation CLI or game integration.

## Next handoff

Owner reviews changes-lineup-v1.png and picks/revises designs. Integrator restores exact template anchors, locks palettes, extracts weapon layers if needed, then creates motion frames following design/MOTION_GUIDE.md. Keep new attempts versioned; do not overwrite.
