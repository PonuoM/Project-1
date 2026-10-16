# Mara — 3-hit combo (owner, 15 Oct)

Hit 1 = the existing slash (`../S01-slash-h3`). Hit 2 = horizontal sweep right→left. Hit 3 = horizontal sweep
left→right. Hit 2 only plays after hit 1, hit 3 only after hit 2.

## How the chain stays seamless
Each hit = **strike part** (wind-up → strike → follow-through) + **recovery part** (back to the ready pose).
- Next hit pressed in time → cut at the end of the strike part and start the next hit there.
- Not pressed → play the recovery part.
The first video frame of hit N+1 is the exact follow-through frame of hit N (its pixels upscaled ×8 onto the
canvas), so the cut point is the same picture. Every clip still ends on the ready pose, so its tail is the recovery.

| Hit | First frame | Last frame | Cut (strike→recovery) |
|---|---|---|---|
| 1 | ready (`../input/mara-violet-1280x720.png`) | ready | after source frame 40 (follow) |
| 2 | hit-1 frame 40 (`hit2-first-1280x720.png`) | ready | its follow frame (pick after generation) |
| 3 | hit-2 follow frame (`hit3-first-1280x720.png`, made after hit 2) | ready | its follow frame |

## Prompt hit 2 (MiniMax Design, H3 768P, 16:9, 5 s, first = hit2-first, last = ready)
Static locked-off camera, side view, flat solid green background that never changes. A chibi pixel-art swordswoman
with an auburn bob and a navy coat starts low after a downward slash, her short violet sword low in front. She
immediately whips the sword in one fast, heavy HORIZONTAL sweep from the front (right side of the screen) back
across her body to behind her (left side), at chest height, twisting her shoulders and stepping forward, holds the
follow-through for a beat with the blade behind her, then returns to her standing ready pose. Only one sweep. The
sword keeps exactly the same short length and violet colour. Same character, same size, chunky pixel art, no
camera movement, no zoom, no motion blur, no effects, no new objects, no text.

## Prompt hit 3 (after hit 2 exists; first = hit3-first, last = ready)
Same opening lines, then: starting with the sword held behind her after a backhand sweep, she swings it in one
fast, powerful HORIZONTAL sweep from behind (left) forward across her body to the front (right side of the
screen) at chest height, leaning into a big forward step as the finishing blow, holds the follow-through, then
returns to her standing ready pose.

## Result (15 Oct) — all three hits generated in MiniMax Design (H3 768P, 350 credits each)
| Hit | Strike part (source frames → ms) | Link / cut | Recovery (only if the combo stops) |
|---|---|---|---|
| 1 `../S01-slash-h3` | 0,14,15,16,17,20(hold),29,30,31(HIT),40 | f40 = hit-2 f0 | 51,53,55 |
| 2 `hit2/` | 2,3,4(smear),5(HIT),10 | f10 = hit-3 f0 | 40,41,43,45,47 |
| 3 `hit3/` | 23,24,25(smear),26(HIT),28 | — | 48,49,51,53,55 |
Previews: `chain-1.png` (0.77 s), `chain-1-2.png` (1.16 s), `chain-1-2-3.png` (1.45 s) + matching .json (frame ms).
Hit 3's video opens with ~1 s of standing still in the start pose; those frames are skipped.
