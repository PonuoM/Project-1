# G10 illustrated world map

2026-10-15. Agent: Codex (GPT-6). Built-in image_gen; image model ID not exposed.

Status: unfinished, generation in progress. Exact tool prompt: prompt-v1.txt. Planned icon positions: layout-plan-v1.json (not final pin coordinates).

Inputs read: design/world/WORLD-MAP-v1.md and design/world/BESTIARY-v1.md. Opened design/world/style-ref-worldmap.png for genre/rendering style only. No reference layout, names or icons supplied to the image tool; generation uses an original text description. G10 overrides pixel-art/chroma-background rules.

Resume: locate/save generated PNG as worldmap-raw-v1.png, inspect composition and all30 landmarks (5 villages/camps,20 zones,5 specials), export worldmap-v1.png at1536x1024 if needed, record observed icon centres rather than planned coordinates in zones.json, verify saved PNGs, append completion here and in design/AGENT_LOG.md. Preserve every attempt. Write only within this task folder apart from required append-only agent log.

## Completion — 2026-10-15

Status: DONE. Recommended: **worldmap-v1.png**, paired with **zones.json**.

Image generation: one built-in image_gen call with the exact prompt preserved verbatim in prompt-v1.txt, transparent_background=false, no referenced image paths. Agent Codex (GPT-6); exact image-model identifier not exposed. The provided map was opened for broad painted-map style only, and was not passed as an edit target or used for its geography, labels or landmark designs. No external paid generation service, PixelLab or MiniMax used.

Saved PNGs:
- worldmap-raw-v1.png — 1536x1024 PNG, original generated image, preserved.
- worldmap-v1.png — 1536x1024 PNG, recommended map, no resampling required.
- pin-crops-v1.png — 640x768 PNG, separate unlabelled QA contact sheet. Each128x128 tile is centred on a stored pin; rows1-5 are cities1-5 and columns are village/camp then zones1-4. Row6 is beanstalk, tower, sewer gate, rift, harbour. This is an inspection artifact, not a game map.

Data and reproducibility:
- zones.json — flat array of30 manually observed centres on the FINAL image:20 zone landmarks,5 villages/camps,5 specials. Fields city+zone identify city entries; zone0 is the village/camp, zones1-4 are playable zones. Special entries use special IDs. Names are English metadata only and never printed on the map.
- layout-plan-v1.json — initial requested coordinates, retained as generation planning history; DO NOT use it for pins. Generated landmark placement differs from the plan.
- export-v1.py / export-verification-v1.json — non-destructive exact-size PNG export; source and final sizes both1536x1024.
- inspect-pins-v1.py / verification-v1.json — counts, coordinate bounds, unique centres, city-zone coverage and separate crop sheet. All30 points inside image; closest pair65.12px apart.

Coordinate convention: top-left origin(0,0), x increases rightward, y downward, units are pixels in the1536x1024 final PNG. Pins mark the visible icon centre, not a terrain-region centroid or a road footpoint. Tall tower/beanstalk centres are on the vertical icons. Harbour centre includes pier/ship composition. Scale positions using the actual rendered image rectangle; account for any letterboxing or cropping in the game UI. Coordinates are human visual measurements, not semantic segmentation precision.

Visual QA: opened the full saved map and the30-centre crop sheet. Confirmed all5 biomes in their requested relative locations; each has4 distinct landmarks plus1 settlement/camp. All5 special icons are separate and identifiable. The bridge, den, candy road, candy house, desert tombs/lamp, snowy pass/cave/lake/palace, ash fields/crags/gate/castle are visible at their indexed locations. The map has no visible labels, letters, title, legend, compass, pins, border UI or watermark. Main land is coherent with rivers, road bridges and winding roads; daylight is warm outside the dark eastern volcanic region. Teal sea and edge mist allow visual expansion space, though future islands still require new artwork.

Brief interpretations and limits:
- The painted road network has junctions and bends rather than a single arrow-like unbranched line. The desert-to-snow leg reconnects through the central mountain approach. Logical progression1->2->3->4->5 and zone order are supplied by city/zone metadata; the game should place its stage pins along the appropriate road segments.
- Landmark scales are illustrative, not geographical: the beanstalk, lamp shrine and castles are deliberately enlarged for readability. Scarab Dunes uses a monumental beetle-shaped stone/statue; Hellhound Crags uses hound-like rock silhouettes. Troll Bridge has carved troll faces. The witch cottage is eerie candy architecture without an actual boss character.
- Snow peaks reach the upper image edge; open expansion sea is more generous at west/south/east than at the northern ridge. Clouds around the beanstalk/tower and outer edges are painted scenery, not gameplay fog-of-war. No fog covers unreached cities; that remains the integrator's overlay.
- Image-model placement drift is reflected in zones.json. No landmark was moved with code or silently replaced, and no prior file was deleted or overwritten.

Remaining G10 work: none. Next step: owner review, Claude checks pin placement and integrates the map screen and localization overlays. No runtime files, game-loaded assets, manifests, client or server were edited.
