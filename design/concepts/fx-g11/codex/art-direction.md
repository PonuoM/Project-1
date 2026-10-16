# G11 slash arcs — integration handoff

Use the six `arc-*-v3.png` sheets, all1024x256, four256x256 cells; native64x64 at4x. Rows in lineup-v3.png: down, sweep-rl, sweep-lr, up, thrust, spin. Exact24-cell bounds/colour counts and nominal anchor positions are in verification-v3.json.

Content palette is semantic, not lit greyscale: #FFFFFF = bright core; #9A9A9A = element body; #3C3C3C = darker element edge; #000000 = empty. Remap these exact RGB values before additive blending. Nearest-neighbour sampling only. Do not multiply the whole image by one tint if that loses the white core. No green keying needed.

Proposed timing: start25ms, full40ms, breakup35ms, last30ms (130ms total). Preview APNGs add600ms black; do not include that delay in attack playback. Trigger on swing/weapon motion, then hold full pose during hitstop. Contact bursts from G10 belong on the monster; G11 arcs belong at the weapon hand. Keep these layers separate. Avoid full-screen white flashes that erase the crescent.

Nominal origin native(8,32) is the imaginary hand on the left side. Spin instead uses(32,32), centred on hero torso. Draw origin = hand position minus scaled nominal origin. These are design anchors, not traced per-frame blade positions: integrator should adjust to each move's hand path and angle rather than centre arcs on the monster. Backhand is right-to-left; do not accidentally mirror it to the finisher's direction.

At the hero reference's50px body height, recommend peak spans: down75px, backhand65px, finisher90px, up75px, thrust75px along its long axis, spin75px diameter. Divide by actual peak span in verification-v3.json to get a native draw scale. The native sheets have55-58px maximum peak spans, so they need approximately1.1-1.6x world scale to read as1.2-1.8 hero heights. The64px cell cannot itself hold a90px effect; leave the source64px and enlarge the rendered quad, never crop to hero bounds. Thrust intentionally stays thin vertically, and horizontal sweeps are judged by longest span rather than literal vertical height. Finisher should be the largest rendered sweep.

These are four designed key poses per action, as requested, not extra interpolated frames. Spin's final key has a small lower-right curved remnant rather than fully disappearing; hide the effect after130ms. Directionality and one-frame breakup trajectories require final review during real attack playback. This task does not modify combat-feel, motion assets, production files or manifests.
