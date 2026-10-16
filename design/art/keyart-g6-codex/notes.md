# G6 anime key art — Codex handoff

Date: 2026-10-14 (Asia/Bangkok).
Agent: Codex / GPT-6 assistant.
Image service: built-in image_gen; underlying image model identifier not exposed.
Status: DONE — ten character identities illustrated; three additional framing attempts retained.

## Scope

Read AGENTS.md and Prompt G6, opened all ten source sprites and read both character documents before drawing. Used the updated expansion sprites for Rika, Yara, Noll and Bramble; no hammer/slingshot/old mushroom-hat character. One character corresponds to one class. Anime proportions replace the chibi anatomy as explicitly requested for G6.

All task deliverables are inside design/art/keyart-g6-codex/. The only write outside that folder is the mandated append-only design/AGENT_LOG.md handoff. Existing sprites, manifests and game files untouched.

## Saved files and selected versions

All portraits and source PNGs are 1024x1536, lossless PNG, as returned by the built-in tool. No JPEG conversion or portrait resizing was necessary.

- mara-v1.png — 1024x1536; recommended mara.
- rika-v1.png — 1024x1536; recommended rika.
- sella-v2.png — 1024x1536; recommended sella.
- yara-v1.png — 1024x1536; recommended yara.
- pipra-v1.png — 1024x1536; recommended pipra.
- vessa-v1.png — 1024x1536; recommended vessa.
- noll-v1.png — 1024x1536; recommended noll.
- tavi-v2.png — 1024x1536; recommended tavi.
- ilen-v1.png — 1024x1536; recommended ilen.
- bramble-v2.png — 1024x1536; recommended bramble.

- lineup-v1.png — 1600x960; ten thumbnails, 5 columns x2 rows, each320x480.
- All ten <name>-v1.png are kept, including superseded Sella/Tavi/Bramble V1.
- All ten <name>-raw-v1.png are original tool-output copies, also1024x1536.
- sella-v2.png, tavi-v2.png, bramble-v2.png —1024x1536 framing edits; these are also unresized original tool PNGs.
- prompts-v1.json — exact ten initial prompts and identity-reference paths.
- edit-prompts-v2.json — exact three framing-edit prompts.
- recommended-v1.json — selected filename per character.
- files-v1.json — complete PNG inventory with dimensions, format and byte count.
- build-lineup-v1.py — non-creative thumbnail composition script.
- notes.md — this handoff.

## Lineup reading order

Top row: Mara, Rika, Sella, Yara, Pipra.
Bottom row: Vessa, Noll, Tavi, Ilen, Bramble.

## Three strongest

1. Rika: the paired fists, rose hair and workshop light make the brawler class immediately readable.
2. Noll: stone, bark, leaves, beard and centre-held staff retain a distinctive non-human identity.
3. Bramble V2: warm personality, round ears and two visible drum-magazine guns preserve the selected character while giving a strong class reveal.

## Per-character identity checks, deviations and exact prompts

Small accessories, stitching and material textures were elaborated to meet the request for detailed anime illustrations. Hair/species, core outfit colour family and weapon role were prioritized over inventing a new design. The notes below record where hem lengths, ornament or effects differ; illustrations are recognizably the same roster, not pixel-perfect costume geometry.

### mara

Source sprite: design/concepts/characters-g5/codex/melee-1-v2.png

Selected art: mara-v1.png

Matched: Auburn rounded side-swept bob; fair face; navy brigandine and short shoulder cape; cream sleeves; brass buckle; brown leather boots; single steel short broadsword.

Differences / rationale: Added stitching, ornate brass guard/clasp, bracers and cape edging. Detailed navy shorts/cream underlayer and stockings elaborate the low-resolution clothing blocks. Morning airship docks and blue blade aura are G6 additions.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Mara Bellwake, human young-adult female sky-port dockguard. EXACT sprite identity: auburn rounded side-swept chin-length bob, warm fair face, NAVY short shoulder half-cape swept backward, navy fitted brigandine over CREAM short/puffed sleeves, brass clasp/buckle, broad brown belt, dark navy shorts/leggings and brown tall leather boots. NOT long hair, no crown, no full-length cape. Hold ONE short broad cool-steel sword with brass crossguard in right hand low-forward; sensible short broadsword, not giant blade. Dynamic planted fencing step, cape lifts in breeze, confident gentle half-smile. Soft sky-port docks of terraced stone/brass, mooring ropes, distant brass-ribbed airship in morning mist. Navy-blue aura along blade. Entire feet visible.
```

### rika

Source sprite: design/concepts/characters-g5-expansion-codex-v1/melee-brawler-v1.png

Selected art: rika-v1.png

Matched: Raspberry full asymmetrical bob; rose padded vest over charcoal sleeves; two giant brass-and-petrol fists; dark shorts; brown boots.

Differences / rationale: Exposed a little midriff beneath the cropped vest and added rivets, articulated knuckles and knee plates. These are anime-detail elaborations; sprite does not define every seam. Workshop backdrop and rose fist aura added.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Rika Brassbeat, human young-adult female harbour machine-fitter/brawler. EXACT sprite: raspberry-red asymmetrical full bob with side fringe, warm fair face, rose-red cropped padded vest over charcoal short sleeves, charcoal fitted shorts and knee supports, brown belt and sturdy brass-buckled brown boots. TWO enormous bronze/brass mechanical boxing gauntlets with petrol-blue inserts, block knuckle plates and round wrist collars attached to arms, no hammer or sword. Boxing guard with forward fist thrust toward viewer-right, rear fist ready, athletic weight grounded, delighted defiant grin. Do not copy an existing pink-haired fighter's outfit/tattoos. Soft blurred guild machine workshop opening onto airship harbour, gears, warm brass light. Muted rose aura around both fists.
```

### sella

Source sprite: design/concepts/characters-g5/codex/melee-3-v1.png

Selected art: sella-v2.png

Matched: Copper bob; long cream/pink swept-back hare ears and cream tail puff; wine coat/plum underlayer; leather shoulders and boots; green-bronze leaf spear.

Differences / rationale: Expanded the split coat into moving tails with embroidery and tassels; plum leg wraps are partly reinterpreted as short underlayer/upper-leg bands. V1 spear tip was very close to the right edge; V2 pulls back and shows the complete weapon with margin.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Sella Reedcrest, hare beast-folk young-adult woman. EXACT sprite: copper/auburn rounded bob, LONG CREAM rabbit ears with pink interiors swept BACK, small cream tail puff, warm face with humanoid anime features; no rat muzzle or dragon armour. WINE-RED short split travelling coat with brown shoulder leather, PLUM under-tunic/leg wraps, brown belt/gloves and brown tall boots. ONE ash-shaft spear with broad leaf-shaped PATINA BRONZE-GREEN head, simple tassel. Powerful diagonal forward spear thrust in a light leaping courier pose, alert smile, ears streaming back; all spear fits. Soft misty stone courier bridge near theatre caravan wagons, distant wind-organ towers. Subtle wine-red aura tracing spearhead.
```

### yara

Source sprite: design/concepts/characters-g5-expansion-codex-v1/melee-assassin-v1.png

Selected art: yara-v1.png

Matched: Purple-black high ponytail; red ties; lower-face half-mask; plum wrap tunic/scarf; charcoal leggings/boots; lavender wraps; two separate short curved steel daggers.

Differences / rationale: Added weathering, layered ties and detailed brass guards. Turned the idle stance into a midair twist while retaining both knives. Night rooftop/theatre town and subtle plum blade trails are G6 additions.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Yara Veilstep, human young-adult female ninja assassin. EXACT sprite: purple-black voluminous hair tied in HIGH PONYTAIL with RED cord, visible expressive eye, CHARCOAL cloth lower-face HALF-MASK. Deep-plum sleeveless WRAP tunic with short split tassets, charcoal leggings/soft boots, lavender forearm/shin wraps, short trailing plum scarf and red waist knot. TWO SHORT curved steel daggers with small brass guards, each distinct in separate hand. NO katana, shuriken, copied game costume, extra sword. Dynamic low airborne turn with one dagger forward and one reverse near hip, mysterious focused gaze. Soft night-blue medieval guild rooftops above a theatre courtyard, warm lantern bokeh. Restrained plum aura around blades.
```

### pipra

Source sprite: design/concepts/characters-g5/codex/mage-1-v1.png

Selected art: pipra-v1.png

Matched: Salmon-pink bob; branching coral crown; pale warm pink face; petrol poncho/navy underclothes; circular brass ring wand with cyan lens.

Differences / rationale: Coral branches include small shell-like crown detailing. Astrolabe is drawn as an articulated ring assembly around a glass lens, with wave trim and water casting arcs. Boots are lighter cream-tan under coastal lighting. Small-folk proportions are non-chibi; artwork does not establish scale beside a human.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Pipra Tideglass, petite coral sprite-folk mage young adult, small but NOT chibi. EXACT sprite: salmon-pink side-swept rounded bob, branching PINK-CORAL crown organically growing through hair (not deer antlers), pale warm pink skin, clear curious face/eyes, PETROL-TEAL scalloped poncho, deep-navy fitted short tunic/sleeves, tan/brass-buckled boots and belt. ONE circular BRASS ASTROLABE RING WAND with solid cyan tide-glass lens and short handle. Gentle casting step, wand extended in hand, other hand guides small elegant water arc, excited knowing smile. Whole face visible, no wizard hat, shadow face or floating detached orb. Soft coral shore below misty cliff kingdom, tide pools, distant airship route. Gentle cyan aura at ring lens.
```

### vessa

Source sprite: design/concepts/characters-g5/codex/mage-2-v1.png

Selected art: vessa-v1.png

Matched: Warm brown skin; asymmetrical ivory-white bob; mulberry coat/trousers with marigold trim; charcoal footwear; open burgundy book with three tabs.

Differences / rationale: Coat tails and boots extend farther than in the sprite, with embroidery, belt ornament and earrings added for detailed key art. Paper-light ribbons reinforce theatre spellcasting. No readable text was requested; some decorative page texture resembles tiny script and is not legible.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Vessa Foldlight, human adult female theatre dramaturge/spellbook mage. EXACT sprite: warm BROWN skin, ivory-WHITE asymmetrical FAN-SHAPED bob, MULBERRY-PLUM short high-collared theatre coat with MARIGOLD-gold lining/trim, matching plum trousers, charcoal ankle boots, burgundy leather open PROMPT-BOOK with THREE stiff paper tabs, cream pages. No pale skin or long hair. Dramatic elegant casting gesture with open book clearly supported by one hand, other hand tracing a subtle luminous paper-ribbon spell; amused confident expression. Soft travelling THEATRE wagons and velvet awnings in warm cobblestone guild square at dusk. Gentle mulberry aura around book/pages; no legible writing or symbols from a franchise.
```

### noll

Source sprite: design/concepts/characters-g5-expansion-codex-v1/mage-summoner-v1.png

Selected art: noll-v1.png

Matched: Pale cracked stone face/hands; broad russet wooden crown with twig antlers/leaves; moss-blue beard; leafy olive mantle; bark tunic; gold acorns; root boots; turquoise fork staff visibly held mid-shaft.

Differences / rationale: Additional bark grain, moss and trailing leaves, layered belt/robe and crystal facets. Anime face is friendly and relatively youthful beneath the beard rather than deeply wrinkled; stone cracks express age/species. Free-hand root-shaped casting light expresses summoner role without adding a companion.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Noll Brackenbell, elder PLANT-AND-STONE forest SUMMONER. EXACT updated sprite: pale weathered STONE face and hands, clear warm eyes, broad russet WOODEN hair/crown volume with two branching twig ANTLERS and green leaves, short MOSS-BLUE BEARD, moss-olive leafy shoulder mantle, dark russet BARK tunic, belt gold ACORN charms, root-like green/brown boots. Not a human druid or old mushroom hat. Organic proportioned small elder, not chibi. ONE UPRIGHT wood fork STAFF around turquoise seed crystal, dangling gold acorn, visibly gripped at MID-SHAFT near waist with equal substantial shaft above/below hand. Calm inviting stance, free hand summons a restrained turquoise root-shaped sigil; no separate familiar needed. Soft ancient mossy forest, tiny spirit lights and root bridge in mist. Gentle teal aura at staff crystal.
```

### tavi

Source sprite: design/concepts/characters-g5/codex/archer-1-v1.png

Selected art: tavi-v2.png

Matched: Sandy-orange fox ears/hair; cream cheek tufts and curled cream-tipped tail; saffron hood-down jacket; sand trousers; brown bracers/boots; dark recurve bow.

Differences / rationale: Added bow wrappings, visible nocked arrow, quiver/pouches and clothing patches. Anime facial treatment is humanoid with fox cheek fur rather than a long animal muzzle, consistent with the sprite. V1 tail touched the left edge and bow was near the top; V2 gives them room. Buried giant ribs establish the desert home.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Tavi Saffronwind, petite FOX beast-folk young-adult male archer. EXACT sprite: SANDY-ORANGE messy hair/fur, triangular FOX ears, short cream muzzle/cheeks, enormous curled fluffy orange tail with CREAM tip behind body. SAFFRON-YELLOW hood-DOWN short jacket, sand-colour trousers, brown leather belt/bracers and boots. ONE dark desert-ironwood RECURVE shortbow, visible curved limbs and string, one arrow nocked. Dynamic half-turn drawn-bow stance, bright cheerful focused face, tail balances pose. Do not make raccoon, wolf, monkey or human without tail. Soft Salt-Reach desert of buried stone GIANTS, huge weathered ribs far behind, wind-shelter courier settlement at sunset. Gentle gold aura along arrow.
```

### ilen

Source sprite: design/concepts/characters-g5/codex/archer-2-v1.png

Selected art: ilen-v1.png

Matched: Angular black bob; cyan quilted coat; two turquoise scarf ribbons; charcoal trousers/boots; brass-and-steel crossbow with transverse limbs/string.

Differences / rationale: Coat tails are longer and leather harness/armour and a small sight are added. The mechanism is more detailed and larger than its pixel counterpart, while retaining the unmistakable bow limbs/bolt rail. Rigging docks and turquoise bolt aura added.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Ilen Rivetwing, human young-adult female airship mechanic/crossbow scout. EXACT sprite: JET-BLACK angular chin-length bob, warm fair face, COOL CYAN short quilted coat, TURQUOISE scarf with exactly TWO backward-streaming ribbons, charcoal trousers and boots, leather belt, brass buckles. ONE compact BRASS-AND-STEEL CROSSBOW, visible transverse bow limbs, taut string, bolt rail and shoulder stock, not pistol or rifle. Heroic braced crouching-ready stance with crossbow aimed diagonally right, sharp dryly amused eyes. Soft airship rigging sky-port roofs, timber scaffolds/brass lift towers, misty skies. Gentle turquoise aura around loaded bolt. Whole feet and bow within canvas.
```

### bramble

Source sprite: design/concepts/characters-g5-expansion-codex-v1/ranged-gunner-dual-v1.png

Selected art: bramble-v2.png

Matched: Shaggy golden-brown hair/fur; large round pink-inner ears; cream face; apple-red vest/cream sleeves; grey trousers; brown boots/backpack; two brass-drum machine guns.

Differences / rationale: Added backpack stitching/pockets, gun barrel perforations and brass mechanisms. Aura at muzzle tips is brighter than a purely idle gun; no heavy laser is included because G6 makes it optional. V1 right barrel was tight to the edge; V2 shows both complete guns. Still dormouse folk, no raccoon mask or superhero armour.

Exact initial image_gen prompt (transparent_background=false; referenced_image_paths contains the absolute source-sprite path above):

```text
Use case: stylized-concept / character-select key art. Create ONE premium 2D ANIME game character illustration, portrait 1024x1536 PNG (2:3 aspect). Attached PIXEL SPRITE is IDENTITY REFERENCE ONLY: translate the SAME person, species features, hairstyle silhouette and colours, outfit shapes/palette and exact signature weapon into detailed ANIME ART. NOT pixel art, NOT chibi, NOT tracing sprite proportions. Humans ~6.5 heads tall; small folk petite ~5 heads, not giant-headed. Full body, entire footwear and weapon within canvas, generous breathing room, dynamic heroic pose in three-quarter view, expressive eyes, clean confident fine line art, cel shading with subtle painterly light, premium fabric/leather/metal/fur detail, cohesive warm storybook high fantasy. Character sharp and dominant; soft slightly blurred home scene behind. Gentle restrained signature-colour magical aura ONLY around weapon/hands, never obscuring weapon design. No text, logos, UI, frames or watermarks. Original established Idle Loot character, no copied franchise costume, insignia or weapons. Avoid adding unrelated characters or extra weapons. Bramble Kettlehop, small DORMOUSE beast-folk young-adult male gunner, petite roughly5-head proportions NOT chibi. EXACT sprite: shaggy golden-BROWN hair/fur, TWO LARGE ROUND tan ears with PINK interiors, CREAM face/cheeks and little nose, warm expressive eyes, APPLE-RED vest over CREAM short sleeves, SLATE-GREY trousers, chunky BROWN boots, oversized round BROWN leather BACKPACK. Preserve lovable round-eared identity; NOT a raccoon, bear or copied superhero. TWO brass-and-steel compact MACHINE GUNS, one per hand, wooden grips and BRASS DRUM magazines, barrels aimed in two clear forward directions. No sling or knife; no extra arms. Brave mischievous ready step, ears alert, tiny tinkerer with outsized firepower. Soft cosy guild-town orchard workshop and distant clockwork stone turrets. Gentle amber/cyan aura around barrel tips. Heavy laser optional, prefer omit to keep silhouette clear.
```

## Exact framing retries

### sella V2

Edit target: design/art/keyart-g6-codex/sella-v1.png. transparent_background=false. No other reference passed.

```text
Edit the attached sella anime key-art image. Change ONLY framing: pull camera back about15% so the ENTIRE existing character, both feet, all hair/ears/tail, clothing and complete weapon(s) fit with at least50px breathing room from every canvas edge. Keep the SAME face, hairstyle, species, outfit, colours, pose, anatomy, materials, lighting, subtle aura and home background composition. Continue the existing background naturally around the smaller subject. Do not add text, border, frame, logo, new weapons or characters. Keep the full patina bronze-green leaf spear tip and rear shaft inside frame. Premium clean-lined cel-shaded/painterly2D anime style unchanged. Portrait1024x1536 PNG.
```

### tavi V2

Edit target: design/art/keyart-g6-codex/tavi-v1.png. transparent_background=false. No other reference passed.

```text
Edit the attached tavi anime key-art image. Change ONLY framing: pull camera back about15% so the ENTIRE existing character, both feet, all hair/ears/tail, clothing and complete weapon(s) fit with at least50px breathing room from every canvas edge. Keep the SAME face, hairstyle, species, outfit, colours, pose, anatomy, materials, lighting, subtle aura and home background composition. Continue the existing background naturally around the smaller subject. Do not add text, border, frame, logo, new weapons or characters. Show the full curled orange/cream FOX tail on left, full recurve bow including upper tip, and the arrow tip on right. Premium clean-lined cel-shaded/painterly2D anime style unchanged. Portrait1024x1536 PNG.
```

### bramble V2

Edit target: design/art/keyart-g6-codex/bramble-v1.png. transparent_background=false. No other reference passed.

```text
Edit the attached bramble anime key-art image. Change ONLY framing: pull camera back about15% so the ENTIRE existing character, both feet, all hair/ears/tail, clothing and complete weapon(s) fit with at least50px breathing room from every canvas edge. Keep the SAME face, hairstyle, species, outfit, colours, pose, anatomy, materials, lighting, subtle aura and home background composition. Continue the existing background naturally around the smaller subject. Do not add text, border, frame, logo, new weapons or characters. Show both complete MACHINE GUNS including full muzzle rims on left AND right, both brass drum magazines and round brown backpack. Premium clean-lined cel-shaded/painterly2D anime style unchanged. Portrait1024x1536 PNG.
```

## Verification and limitations

- Verified every saved portrait/source is PNG1024x1536 and the lineup is1600x960; listing is in files-v1.json.
- Inspected all ten initial images, all three retries and the final saved lineup. Selected versions show full footwear and complete core weapons; V2 gives tail/spear/gun silhouettes more space.
- All10 have distinct home scenes and weapon/hand aura. Background structures sometimes remain detailed rather than strongly blurred; tonal separation and foreground sharpness keep character emphasis.
- Sella, Tavi and Bramble V2 are frame refinements, but generative editing can also subtly change fine facial/texture pixels; no exact pixel-lock claim.
- Normal/petite anime proportions were requested and visually reviewed; exact numerical6–7/5-head ratios were not mathematically certified.
- Some environment banners contain invented ornamental motifs, and book pages have decorative marks. No readable names, UI, watermark or recognizable franchise logo was requested or observed.
- Vessa's coat tails, Ilen's coat, Sella's garment layers and some accessories are expanded compared to the sprite as explicitly recorded above. If strict costume construction matters, future revisions can shorten them while retaining identity.
- No PixelLab, MiniMax, external paid API runner or game integration performed.

## Next handoff

Owner reviews lineup-v1.png and the selected full portraits. Integrator can use portraits for character select/profile/store displays. Do not overwrite these outputs: any further edits use V2/V3 as available. All exact prompts and inputs are sufficient to resume.
