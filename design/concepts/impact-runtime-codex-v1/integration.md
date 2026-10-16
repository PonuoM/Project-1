# Integrating the impact prototype into Idle Loot

Recommended files: attack-driver.mjs + phaser-impact-v2.mjs. This is a working Phaser 3.90.0 presentation prototype, not a drop-in WorldScene patch.

## Evidence from the actual client
- client/src/renderer/src/game/WorldScene.ts: startStrike / advanceStrike / impact / drawHero / drawFoe / drawFx.
- The existing scene already uses a local hold clock, visual foe.hp, server rates.killMs, and hooks.onKill(gold). Normal timing is 35 + 55 + 45 + 105 ms; skill timing 70 + 65 + 60 + 145 ms.
- client/src/renderer/src/game/assets.ts preloads sheets and creates fixed-FPS animation keys. This prototype instead selects frames by attack phase so the burst is fast while anticipation and recovery remain readable.
- Hero and weapon frames are already composed. The weapon is not independently swappable in these exported strips; true equipment swapping requires the existing body + weapon-hand pose pipeline.

## Ownership and hooks
1. Keep authoritative kills, rewards, sync, and cooldowns in the existing host. Do not call hooks.onKill or reward APIs for each of the three contact accents.
2. Choose one source of attack timing. Replace the local visual strike driver OR translate this profile into the host; do not advance both WorldScene.strike.t and AttackDriver.t for the same attack.
3. Load assets/slash.png and assets/chop.png as 80x80 sprite sheets (15 frames each). Origin .5,1; snap feet to ground. Adapter uses this demo's ground=112 and contact=91: parameterize these coordinates to GROUND_Y before integration.
4. Resolve the current target at the actual contact boundary, using world coordinates and the weapon reach. The demo uses a simple horizontal interval (+/-18px target bounds), not a production physics hitbox. Remove/retarget dead enemies safely.
5. In onVisualContact(event), trigger only the visual damage accent and target reaction appropriate to the existing strike. A combo can have three visual contacts but one authorized kill payout. Finisher must not create extra rewards.
6. Tick AttackDriver with elapsed milliseconds; it internally splits at contact and hit-stop boundaries. Freeze only actor presentation; cooldown/UI/network time continues. Do not set scene.time.timeScale=0. Do not add WorldScene.hold on top of this driver's stop.
7. Call cancel() on target replacement, region change, hero/equipment changes or interruption; call destroy() on scene shutdown. Main-camera scroll is owned by WorldScene, so apply the adapter's shake as a transient offset after the host's camera-follow calculation instead of using setScroll(0,0).
8. The adapter currently mutates sprite scale/tint for recoil and clears its own Graphics each frame. Give it dedicated FX Graphics; preserve/restore the game's existing scales/tints when absorbing it. Ghost sprites are three reused objects in demo-v2.mjs, not created each frame.

## Suggested use
Normal attacks should stay short and readable. Heavy profile totals 353ms on contact (95 anticipation + 28 burst + 65 stop + 165 recovery); miss totals 288ms. Finisher totals 505ms; three-hit combo totals 1211ms with contacts. Do not insert a 1211ms combo into every 240ms normal strike: reserve it for a skill/rare finisher and budget it within rates.killMs. A shorter ordinary attack can retain 35ms windup, about 25ms burst, 45ms stop, and 105ms recovery; validate against the actual attack cadence before shipping.

## What remains before shipping
- Integrator modifies WorldScene and its loader under their permissions, maps ground/camera coordinates, and prevents duplicate kill callbacks.
- Test widget dimensions, different attack speeds, boss resistance/death, changed equipment and region switches.
- Tune the source hero's hand/weapon pose and add authored smear frames if matching the reference's extremely fluid flurry is required. Runtime transforms alone cannot invent those poses.
- Sound here is a quiet synthesized placeholder, opt-in. Replace with authored hit/whoosh audio.
- Demo clamps UI delta to 100ms; pause/resume/visibility behavior and performance must be profiled in Electron. The pure driver handles long deltas without duplicate events, but that does not establish live hardware FPS or final gameplay throughput.
