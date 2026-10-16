# Pixel overworld prototype

Open **viewer-v3.html** (recommended) in a browser. It also works through the existing AppServ site:

http://localhost/Projects-1/design/world/worldmap-pixel-g10-codex/viewer-v3.html

No build, installation, API key or internet connection is required. Keep the folder together. The preview reads local PNG/JS assets and has no server writes or game-state changes.

## Try it

- Overview starts with water and clouds moving; pins/routes are initially hidden.
- Choose a region to zoom to it and reveal its20 stage pins. All5 regions have4 zones ×5 stages.
- Click a pin or use the20 stage buttons below. Arrow keys on the focused canvas select adjacent stages. The20th stage of each region is marked as its boss.
- Toggle clouds, pins or routes independently. Stop/start animation using the top button.
- Return to overview with ดูทั้งโลก. All100 pins can also be shown there using the checkbox.
- Reduced-motion preference pauses the preview initially; the user can explicitly enable it. It also pauses movement while the document is hidden.

## Layers and files

| Item | Role | Size |
|---|---|---|
| land-raw-v1.png | Original image_gen PNG, kept | 1448×1086 |
| land-native-v1.png | Transparent continent at native art scale | 256×192 |
| land-v1.png | Exact8× transparent continent | 2048×1536 |
| overview-v1.png | Static composite for review | 2048×1536 |
| motion-preview-v1.png | 16-frame animated PNG excerpt from the actual canvas | 768×576 |
| motion-still-v1.png | Static first frame of the animated excerpt | 768×576 |
| map-data.js | Runtime data for the standalone viewer | — |
| stages.json | 100 independent editable stage anchors | native pixel coordinates |
| zones.json | 20 zone,5 camp/village and5 special anchors | native pixel coordinates |
| map-layout.json | Region cameras, colours and cloud positions | native pixel coordinates |
| viewer-v2.js | Recommended canvas renderer | — |
| viewer-v2.css | Recommended viewer styles | — |

The viewer draws **water → transparent land → clouds → route overlays → stage pins**. Sea wave tiles and near/far cloud shapes are code-native pixel layers, not baked into the continent. Terrain stays fixed. The weather pass is behind pins, so clouds do not hide stage selection.

## Coordinate and stage contract

All JSON coordinates use the256×192 native map, origin top-left, x right, y down. Multiply x/y by8 for positions in the2048×1536 PNG. Scale using the actual displayed map rectangle and camera crop. Do not use the original painted G10 coordinates for this map.

Each stage has id1–100, city1–5, zone1–4, inZone1–5, localStage1–20, x/y, boss, regionName and zoneName. Boss is true only at localStage20. Stage selection here is a preview, not progression or unlocking. Position changes are made in the JSON/data, not by repainting the map. To update this standalone viewer, keep map-data.js in sync with stages.json.

The100 positions are **proposed layout anchors**. Every centre is on opaque terrain; they are not a navigation mesh or collision-checked route. Some connectors cut across scenery or jump between zone clusters. Integrator review should move pins onto final road clearings, widen clearings where necessary, choose stage unlock rules and wire the gameplay screen. This task provides the art/interaction prototype only.

## Animation limits

Sea ripples and clouds move live at10 drawing updates/sec. Rivers, marsh water, waterfalls, lava, windmill blades, beanstalk and the rift remain part of the static land layer in this first prototype. To animate them independently later, provide dedicated masks/sprites or terrain overlays. The APNG is a6-second excerpt and repeats with a cloud-position reset; the live viewer has continuous offscreen wrapping.

The source used too many small painted-style clusters in places despite the low-resolution prompt. Export locks exact8×8 blocks and an80-colour palette; snow/castles and some village details become abstract at native scale. The source also crops a little of the northern ridge/eastern rift, which padding cannot restore. The purple rift haze loses some colour at binary-alpha/palette export. These are art polish items before production.

## Verification

- All100 unique stage anchors inside the map and on non-transparent terrain.
- Five regions each show20 working stage buttons; selecting stage100 shows the final regional boss.
- Actual browser render changed5534 pixels between t0/t3 (water/cloud movement), while pause stopped the animation clock.
- Desktop and390px mobile layouts inspected; no horizontal overflow. Buttons/toggles and region focus checked.
- Two visual passes; v1 retained, v2 reduced marker/route clutter and shows them on region selection. Final HTML v3 only adds the23px mobile title hierarchy correction.
- Mechanical design detector run once: one small mobile heading hierarchy warning, corrected in viewer-v2.css. No claim of a production accessibility/performance certification.

All source prompts, generated attempts and previous preview files are retained. No game-loaded asset, client/server file or manifest was edited.
