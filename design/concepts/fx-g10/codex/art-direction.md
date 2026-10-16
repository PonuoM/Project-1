# Elemental hits — G10 handoff

Recommended sheets: fire-v2.png, ice-v2.png, poison-v2.png, lightning-v2.png, explosion-v2.png. Each1024×256, four256×256 cells, native64×64 at4×. Full comparison: lineup-v2.png1024×1280. Native comparison: lineup-1x-v2.png256×320.

The original prototype uses very similar round burst silhouettes for several elements. Sparse coloured weapon/status particles then add movement without defining the material. These designs give each element a distinct primary gesture, not merely a recolour.

| Effect | Primary shape | Break-up | Proposed four-key timing, ms |
|---|---|---|---|
| Fire | Narrow curling tongues rising from the hit | Ribbons separate into ascending embers | 35 / 65 / 90 / 120 |
| Ice | A spear-shaped faceted crystal | Straight triangular shards leave a dark central gap | 35 / 45 / 80 / 90 |
| Poison | Low puddle with thick asymmetric liquid arcs | Large drops fall back into the puddle | 45 / 60 / 100 / 160 |
| Lightning | Narrow down-striking stepped bolt | Broken segments and short ground arcs | 20 / 30 / 25 / 45 |
| Explosion support | Radial star plus a separated shock ring | Broken arcs, debris and grey smoke | 20 / 45 / 75 / 110 |

Timing is a proposed animation direction, not an existing approved video. These are four designed KEY poses, not a production smooth animation. Claude should use them to guide H3 Max only after owner approval. No video generation performed here.

## Placement

One cell's target footpoint is native(32,52), image(128,208). At1× draw origin should be targetX−32,targetGroundY−52. Keep the peak within roughly one hero-height. Fire/ice/lightning peak height reaches49px; poison40px, explosion37px including debris. The actual feature centre can vary a few pixels across keys; preserve a fixed anchor in final motion extraction.

Black is intentional, for additive blending. Start with normal/lighten comparison before choosing the final compositor. Avoid scaling a full burst by1.6 on top of these dimensions automatically: set final effect size against the48px enemy first. Avoid simultaneous full-white enemy flash plus full-screen flash plus multiple additive peaks; they can erase the shape this art is designed to communicate.

During a three-hit combo, use reduced/simpler first two hits and reserve the full peak for the finisher. A support explosion should occur on impact or a short delayed beat and use the same target anchor; do not stack its full bright core over every element at every hit. The new sheets do not change hit-stop, shake, damage or combat ownership.

## Distinct element behavior

- Fire carries energy upward. Status burning should continue with just2–3 short upward licks or embers, not another full peak burst.
- Ice strikes angularly and leaves separated shards; status freezing belongs on the enemy silhouette, not a repeated circular explosion.
- Poison is a liquid splash, with gravitational return and a small puddle. Avoid upward smoke particles as the primary poison cue.
- Lightning arrives vertically in a very short flash. Avoid continuous random sparks on every frame; that reduces the contrast of the strike.
- Explosion alone owns the round ring. Keep the ring's black interior legible and debris subordinate to it.

## Limitations and review

Sources were generated at different wide aspect ratios instead of1024×256. Export v2 independently extracts the four source cells and applies ONE uniform source-to-native scale per sheet, so circles/shards retain their proportions. Palette is locked to4 content colours plus black. Cell borders have3 black native pixels. Exact4× grid checked. Small one-pixel particles can disappear during source sampling; retained sources allow later cleanup.

The generator does not provide exact temporal pixel correspondence. Fire still reconnects near the base in its breakup key, poison retains a puddle throughout, and explosion smoke/debris occupies more area in the final key than the very sparse fire/ice remains. Lightning source touches its upper boundary; the exported strike starts at nativey4 with a clear margin. Muted violet#6741a4 is allowed here; weapon-ID violet#7a3cff is never used. Source brightness can look softer than final pixel export.

No changes were made to combat-feel/index.html, motion strips, game runtime, client/server or manifests. Integrator must approve placement and motion in the actual combat preview before replacing assets.
