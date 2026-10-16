# Gemini (Google Antigravity) — read AGENTS.md

All shared rules for this repository are in `AGENTS.md` (Codex reads the same file, and the owner switches between
Codex and Gemini when one runs out of tokens). Follow it exactly, including the start/finish handoff through
`design/AGENT_LOG.md`.

Gemini-specific notes:
- Your `image-generator` sub-agent saves `.jpg` files in Antigravity's artifact folder
  (`C:\Users\user\.gemini\antigravity\brain\<conversation id>\`). After every generation, convert to PNG and copy
  it into the task folder in `design/` — this is the step most often missed.
- Report the model in notes.md as it appears in Antigravity (e.g. "Gemini 4 Argon (Medium)").
