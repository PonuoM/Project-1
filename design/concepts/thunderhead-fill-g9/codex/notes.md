# G9 — Thunderhead cut-edge fill

2026-10-15. Codex (GPT-6); built-in image_gen, exact image model ID not exposed. Status: unfinished, generation underway.

Inputs read/opened: ../input/sheet-a.png and sheet-b.png (edit targets), sheet-a-cutlines.png and sheet-b-cutlines.png (boundary guides only), layout.json. merge_fill.py read for coordinate semantics; not run against game assets. G9 overrides the general8x grid with exact2x2 art pixels.

Exact image-tool prompts: prompts-v1.json. Each edit references its plain sheet first, guide second. Preserve all original rectangles; paint only top/right padding. Sheet A1608x816 (3x2), cell536x408, cut localy56/x480. Sheet B1664x832 (4x2), cell416x416, cut localy56/x360. All pad regions56px, native28px.

Resume: save tool PNGs as sheet-a-raw-v1.png / sheet-b-raw-v1.png, inspect. Mechanically align whole sheets/cells to original sizes if necessary, normalize ONLY added padding to2x2 grid/background/palette, paste the FULL original rectangles back unchanged, export sheet-a-v1.png and sheet-b-v1.png. Verify every protected RGB pixel equals its input, no red guide pixels, additions only in allowed padding, and inspect seams and consistency. Keep every attempt, append final inventory/deviations and AGENT_LOG.md.

## Completion — 2026-10-15

Status: DONE for G9 outpainting test. Recommended: **sheet-a-v2.png** (1608x816 PNG), **sheet-b-v2.png** (1664x832 PNG). Requested v1 exports retained alongside v2 retries. Both recommended sheets keep exact input canvas sizes and frame positions, all original rectangles pixel-identical, background #00B140, exact2x2 art blocks, original21-colour palette only, and no red guides.

Agent Codex (GPT-6); built-in image_gen, model ID not exposed. Two tool calls, one per sheet. Exact prompts verbatim in prompts-v1.json; referenced images ordered plain target then corresponding red-guide sheet. transparent_background=false. All four input/guide images visually opened before editing. No paid generation API, PixelLab or MiniMax run.

Generated source PNGs retained: sheet-a-raw-v1.png1760x894, sheet-b-raw-v1.png1774x887. They are image-model edit results and drift in resolution, background and existing sprite detail, so they are NOT recommended merge inputs. No JPEG/WebP conversion. Export normalizes ONLY generated padding to native2x grid and nearest original palette, registers generated fill strips to input cut edges, discards unattached additions, and pastes the FULL original frame rectangles back over the protected area at original RGB resolution. No existing source pixels are repainted. The output keeps the input background too, including green inside the protected rectangles.

Export history:
- export-v1.py: resizes generated cells to their original layout, registers each to its original silhouette/cut edge, takes only connected fill in allowed top/right strips. Saved both v1 sheets. First review found sheet-b final two frames had no attached fill at the right cut because one global alignment was insufficient.
- export-v2.py: same original preservation, separately registers the right strip against the original shoulder/arm region; restores attached right-edge fill in special26/34. All prior exports retained. This is geometric registration/palette cleanup of imagegen output, not replacement artwork drawn by code.
- verify-final-v2.py: independent full-resolution comparison of protected RGB pixels; records matching hashes, exact2x2 blocks, palette subset and adds separate padding-only inspection plates. verification-v1.json, verification-v2.json, verification-final-v2.json and files-v2.json retained.

Final verification:
- Sheet A:14628 changed image pixels, all in allowed padding; protected changed0.
- Sheet B:15644 changed image pixels, all in allowed padding; protected changed0.
- All6 sheet-A cells have attached top fill. Sheet-B cells1-5 have attached top fill; cell6 has no original top-cut foreground (club actually touches right cut there), so top stays green. Right-cut fill attaches in cells3-8; cells1-2 have no original right-cut foreground, so right stays green.
- Source and original protected RGB hashes match for each entire sheet. No red/high-saturation guide pixels. Only original21 colours used. Inputs unchanged.
- Full final sheets visually inspected; right-edge-review-v2.png inspected for shoulder/forearm contours. The sheet-A v2 export matches its v1 art because the right-edge registration change only applies where foreground touches that edge.

Saved images:
- sheet-a-v1.png / sheet-a-v2.png —1608x816 each; recommended v2.
- sheet-b-v1.png / sheet-b-v2.png —1664x832 each; recommended v2.
- sheet-a-raw-v1.png —1760x894; unaltered generated source.
- sheet-b-raw-v1.png —1774x887; unaltered generated source.
- sheet-a-additions-v2.png —1608x816; generated fill only on green for review.
- sheet-b-additions-v2.png —1664x832; generated fill only on green for review.
- right-edge-review-v2.png —832x832; isolated right-edge crops with2x horizontal stretch, QA only, not a sprite sheet.

Limitations: generated additions are plausible contour reconstructions; the missing original video pixels cannot be recovered exactly. Leaf-tip arrangements vary slightly between frames, and some cut joins retain small changes of slope/colour. Full one-to-one cut-row overlap is not expected when a contour narrows just outside the old image: e.g. sheet-A attack12 joins38/40 top pixels; sheet-B special11 joins12/14 right pixels, special25 joins56/59. No detached additions are retained. Special26/34 need only6/8 native added pixels at the clipped elbow tip. Sheet-B special25 right-edge continuation is the least certain anatomical join and should be inspected in playback. This test is not a guarantee of perfect temporal coherence or an animation approval. Only top/right pad regions were available; nothing can extend beyond the existing padded canvas.

Claude handoff: use ../input/layout.json with sheet-a-v2.png / sheet-b-v2.png and design/tools/merge_fill.py; keep source frame ownership with the integrator. No merge into runtime frames was performed. Final originals are already protected in these sheets, but merge_fill.py must still let original frame pixels win. No client/server, manifest, original input, approved boss sprite or game-loaded frame edited. Remaining G9 generation/export work: none; next is Claude's merge/playback review.
