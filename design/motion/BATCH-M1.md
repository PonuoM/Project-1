# Batch M1 — city 1 monsters + Grimfang + Thunderhead (MiniMax Design, H3 768P, 5 s)

Inputs (inside THIS project folder, relative paths only): `inputs/<name>-1280x720.png` (first frame) and `inputs/<name>-1280x720-end.png` (last frame). Never use C:/AppServ paths ("Path traversal detected"). Skip the agent's brief/research/storyboard stages and call the video tool directly.
hurt-death: first frame only. Name each output `<name>-<move>.mp4`. 20 clips ≈ 7,000 credits. Start with kiki-idle-walk as a test and check it before the rest.

## kiki
1. **kiki-idle-walk** — first `kiki-1280x720.png`, last `kiki-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a small fierce blue-grey goblin imp with red glowing eyes holding a rusty orange knife. First it stands in the ready pose breathing for about one and a half seconds. Then it scurries hunched IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
2. **kiki-attack** — first `kiki-1280x720.png`, last `kiki-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a small fierce blue-grey goblin imp with red glowing eyes holding a rusty orange knife. It crouches, then darts a short step forward to the left and stabs the knife twice very fast, then hops back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
3. **kiki-hurt-death** — first `kiki-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a small fierce blue-grey goblin imp with red glowing eyes holding a rusty orange knife. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```

## thornboar
4. **thornboar-idle-walk** — first `thornboar-1280x720.png`, last `thornboar-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a black wild boar with big ivory tusks and bright green thorny vines on its back. First it stands in the ready pose breathing for about one and a half seconds. Then it trots heavily IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
5. **thornboar-attack** — first `thornboar-1280x720.png`, last `thornboar-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a black wild boar with big ivory tusks and bright green thorny vines on its back. It lowers its head and scrapes the ground with a front hoof, holds for a moment, then charges a short distance forward to the left and tosses its tusks upward hard, then backs up into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
6. **thornboar-hurt-death** — first `thornboar-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a black wild boar with big ivory tusks and bright green thorny vines on its back. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```

## hex-scarecrow
7. **hex-scarecrow-idle-walk** — first `hex-scarecrow-1280x720.png`, last `hex-scarecrow-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a thin cursed scarecrow with a straw-yellow body, dark rags, a sack head with one big orange glowing eye, and a purple-black crow perched on its raised arm. First it stands in the ready pose breathing for about one and a half seconds. Then it shambles stiffly IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
8. **hex-scarecrow-attack** — first `hex-scarecrow-1280x720.png`, last `hex-scarecrow-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a thin cursed scarecrow with a straw-yellow body, dark rags, a sack head with one big orange glowing eye, and a purple-black crow perched on its raised arm. It jerks its crow arm forward and points to the left; the crow spreads its wings and caws without leaving the arm, the scarecrow's head twitches, then everything settles into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
9. **hex-scarecrow-hurt-death** — first `hex-scarecrow-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a thin cursed scarecrow with a straw-yellow body, dark rags, a sack head with one big orange glowing eye, and a purple-black crow perched on its raised arm. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```

## bridge-troll
10. **bridge-troll-idle-walk** — first `bridge-troll-1280x720.png`, last `bridge-troll-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a squat moss-green troll with an underbite and white tusks holding a heavy grey stone-and-stump club. First it stands in the ready pose breathing for about one and a half seconds. Then it lumbers heavily IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
11. **bridge-troll-attack** — first `bridge-troll-1280x720.png`, last `bridge-troll-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a squat moss-green troll with an underbite and white tusks holding a heavy grey stone-and-stump club. It slowly raises the club high over its shoulder, holds at the top, then smashes it down hard onto the ground in front of it to the left, the body jolts from the impact, then it lifts the club back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
12. **bridge-troll-hurt-death** — first `bridge-troll-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a squat moss-green troll with an underbite and white tusks holding a heavy grey stone-and-stump club. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```

## grimfang
13. **grimfang-idle-walk** — first `grimfang-1280x720.png`, last `grimfang-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a huge fierce dark-blue werewolf standing on two legs with long white claws and a torn red hooded cloak. First it stands in the ready pose breathing for about one and a half seconds. Then it prowls IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
14. **grimfang-attack** — first `grimfang-1280x720.png`, last `grimfang-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a huge fierce dark-blue werewolf standing on two legs with long white claws and a torn red hooded cloak. It rears back, then slashes forward to the left with one claw and then the other in two fast heavy swipes, then returns into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
15. **grimfang-special** — first `grimfang-1280x720.png`, last `grimfang-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a huge fierce dark-blue werewolf standing on two legs with long white claws and a torn red hooded cloak. It throws its head back and howls at the sky for a moment, then crouches low and leaps forward to the left in a short pounce, slamming both claws down, then springs back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
16. **grimfang-hurt-death** — first `grimfang-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a huge fierce dark-blue werewolf standing on two legs with long white claws and a torn red hooded cloak. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```

## thunderhead
17. **thunderhead-idle-walk** — first `thunderhead-1280x720.png`, last `thunderhead-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a gigantic bearded giant in leather and chains holding a whole green beanstalk as a club. First it stands in the ready pose breathing for about one and a half seconds. Then it stomps slowly IN PLACE like on a treadmill for three steps, legs clearly alternating, never moving across the screen. Then it stops and settles back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
18. **thunderhead-attack** — first `thunderhead-1280x720.png`, last `thunderhead-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a gigantic bearded giant in leather and chains holding a whole green beanstalk as a club. He slowly lifts the beanstalk club high, holds at the top, then swings it down in a huge arc to the ground in front of him to the left, the whole body jolts from the impact, then he lifts it back into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
19. **thunderhead-special** — first `thunderhead-1280x720.png`, last `thunderhead-1280x720-end.png`
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a gigantic bearded giant in leather and chains holding a whole green beanstalk as a club. He raises one huge foot, holds it, then stomps the ground extremely hard so his whole body shakes, then immediately slams the beanstalk club down, then recovers into the exact starting pose. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
20. **thunderhead-hurt-death** — first `thunderhead-1280x720.png`, NO last frame
```text
Static locked-off camera, side view facing LEFT, flat solid green background that never changes. This is a gigantic bearded giant in leather and chains holding a whole green beanstalk as a club. It is hit once from the front and flinches backward, then hit hard again: it staggers, collapses to the ground and lies still for the rest of the clip, staying inside the frame. Same creature, same size, same colours, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no particles, no text.
```
