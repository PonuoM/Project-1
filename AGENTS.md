# Rules for the art / design agent (Codex or Gemini) in this repository

Read this file at the start of every task. **Codex reads this file; Google Antigravity (Gemini) reads this file
and `GEMINI.md`.** The owner switches between Codex and Gemini when one runs out of tokens, so both follow the
same rules and hand work to each other through `design/AGENT_LOG.md`.

You are the **art / design agent** for "Idle Loot" (a chibi pixel-art idle ARPG desktop widget). You design pieces
(weapons, outfits, items, concepts) and write files in `design/`. Since 14 Oct 2026 the owner's decision is that
**you (Codex / Gemini) draw the game sprites themselves**, outfit concepts first, animation frames later (follow
`design/MOTION_GUIDE.md` for motion). Claude is the integrator: Claude writes your prompts, checks and cleans your
images onto the exact pixel grid, places weapon layers and wires everything into the game. Follow these rules in
every task, even if a prompt forgets to repeat them.

## Start and finish of every task (handoff between agents)
1. **Start:** read `design/AGENT_LOG.md`. If the task is already listed as unfinished, continue it from its notes
   instead of starting over.
2. **Finish, or stop because you are running out of tokens/time:** append an entry to `design/AGENT_LOG.md`
   (date, agent = Codex or Gemini, task, status done/unfinished, saved files, what is left) and write the task
   folder's `notes.md`. An unfinished task must be resumable by the other agent from those two files alone.
3. End with a short message listing the saved paths.

## Hard rules
1. Write only inside `design/`. Never edit `client/`, `server/`, `design/sprites/manifest.json`, or any file the
   game loads. Never edit `AGENTS.md` or `GEMINI.md` unless the owner asks.
2. Never write API keys, tokens or passwords into any file, log or note.
3. Never delete or overwrite existing files. Put every task in a new folder or a new versioned file (`-v2`, `-v3`).
   If the owner runs Codex and Gemini on the same task at the same time, each agent writes ONLY into its own
   folder with its name in it (e.g. `characters-g5-codex/`, `characters-g5-gemini/`), never into the other's.
4. Do not run paid generation services (PixelLab, MiniMax, etc.) yourself; Claude does that.

## Saving images
- **Every image you generate must end up inside the repo at the exact path the task asks for.** If your image tool
  saves somewhere else (Antigravity's artifact folder, a temp folder), copy the file into the requested repo path.
- **PNG only** (lossless). Never JPEG: JPEG smears pixel edges into the green screen. If your tool only gives
  JPEG/WebP, convert to PNG when copying and say so in notes.md.
- Keep every attempt: `sheet-v1.png`, `sheet-v2.png`, … and name the one you recommend in notes.md.
- Before you report "done", list the folder and show the saved files with their pixel sizes. If a file is not in
  the repo, the task is not done.

## House style for images Claude will convert
- Plain flat chroma-key green background `#00B140` everywhere: no gradient, no shadow, no floor, no text, no
  grid lines, no labels.
- Chunky pixel art, **one art pixel = an 8×8 block** of image pixels, 1-pixel dark warm outline `#2e1816`,
  flat 3-shade ramps, no anti-aliasing, no glow, no blur.
- Reference hero: `design/pixellab/chibi-motion/hero-ref-64.png` (64×64, ~50 art px tall, side view facing
  right). Open it when a task concerns the hero, and match its proportions and palette.
- Reserved colours: the hero's ivory mantle, moss-green tunic and terracotta sash belong to the hero — weapons and
  items must not use them. Saturated violet `#7a3cff` is the **weapon ID colour**; use it only when a task asks.
- Grids: at 1024×1024 a 4×4 grid has 256×256 cells = 32×32 art pixels per cell. Keep a clear green gap around
  each item; nothing touches a cell edge.
- Weapons: handle at the **lower-left**, tip/head toward the upper-right (45° diagonal is the house pose; flat
  pointing right is also fine). Lengths are measured **along** the weapon; on the diagonal a weapon covers only
  ~0.7 of its length in width and height. The hero is ~50 art px tall.
- Image models drift toward equal sizes: when exact sizes matter, put small items and long items in separate
  sheets.

## Every task's notes.md
Agent and model used, the exact prompt you gave the image tool, the files you saved (path + size), your
recommended version, and every point of the brief you could not follow exactly.

## Useful context
- Prompts for this role: `design/CODEX_PROMPTS.md` (older, Codex-era) and `design/GEMINI_PROMPTS.md` (current;
  works for either agent).
- Claude's conversion tools live in `design/tools/` (e.g. `weapons_from_sheet.py` cuts a weapon sheet into
  native sprites); you may run them read-only to check your own output, writing only into your task folder.
- Knowledge from the animation experiments: `design/pixellab/chibi-motion/README.md`; the short version for
  drawing frames is `design/MOTION_GUIDE.md`.
