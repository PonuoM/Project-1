# Combat feel — decisions approved by the owner (15-16 Oct 2026)

Playtest: `prototypes/combat-feel/index.html` (Mara vs Kiki). These are the rules the real game should copy.

- Attacks fast and hard: hitstop ~80 ms (finisher x1.6), screen shake, enemy turns a full white silhouette, knockback,
  damage numbers (crits big/yellow). Combo hits escalate; hit 3 is the finisher (bigger arc, white screen flash).
- Main attack effect = the weapon SLASH ARC (Codex G11 sheets, white/grey/dark roles recoloured per element), placed
  per hit frame from `motion/mara/anchors.json` (thrust arcs on the blade line, spin arcs as a flat ellipse at
  waist height split behind/in front of the hero, other arcs around the body). Not a big explosion on the enemy.
- Elements: particles along the blade, a SHORT hit accent (~0.3 s), status on the enemy = body tint + a few small
  spots + a short label (ติดไฟ/หนาว/พิษ/ช็อต). No big fire pile on the enemy. Explosion = separate support gem.
- Buff moves (no hit, no arc): warcry (power-up pose) and ground stab (sword planted, aura from the feet; aura FX
  still to design).
- AI battle: skills on cooldowns, otherwise the basic 3-hit combo; no idle standing. After the last hit the recovery is
  played FAST (every 2nd frame, ~20 ms) and the next move starts at its 2nd frame -> continuous, approved.
- Every clip: design the reference first (Codex/Gemini), then H3 Max 480P 16:9 (200 credits).
