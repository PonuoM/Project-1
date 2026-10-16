# Combat Feel — expanded sprite integration

2026-10-15 · Codex / GPT-6 · done.

The owner explicitly requested updating `design/prototypes/combat-feel/index.html`. That instruction authorizes editing this existing design prototype; the complete prior page is preserved in `index-before.html`. No client/server, manifests, motion source assets or production game files changed.

Default effect set is now **ใหม่ · Sprite**, with **เดิม** available for comparison. Expanded explosion16/fire12/ice-shatter12/poison-slash12 frames load directly from `design/concepts/fx-g10/codex/impact-expanded-v1/` using `effects-v2.json`. Lightning uses the previously approved four-key `design/concepts/fx-g10/codex/lightning-v2.png`. Exact image prompts and generated-image dimensions remain in the source task's prompts-v1.json and notes.md; no new images generated for this task.

Rendering: row-major sheet cells, nearest-neighbour native64px output, additive blending, authored variable durations. Bursts are created by existing HIT/IMPACT frames (slash8; combo8/13/18). Expanded effects pivot at the torso, follow early recoil for140ms, then detach as debris. Lightning retains its footpoint anchor. Combo hit scale is bounded to avoid covering the entire enemy. Elemental explosion support starts45ms later and is smaller. White body/screen flashes are reduced in the new mode to preserve the artwork. Existing hitstop still freezes effect age along with combat.

Reduced-motion mode starts with auto attack off and suppresses screen shake/body and screen flashes; manual attack feedback remains. Hidden-tab ticks skip animation updates. Image loading errors surface in the page note. No libraries added. Existing blade/status particles and damage controls remain.

Validation: browser loaded every new sheet; all56 cells (52 expanded plus4 lightning keys) rendered without exceptions. All four elemental impacts and explosion support spawned at torso contact; authored12/12/12/4 and16 frame counts checked. Original draw path still renders. Real UI click test verified a single poison slash and repeated combo impacts with explosion support; Space triggered attack. Mobile390px had358px canvas and no horizontal overflow. Reduced-motion emulation started auto=false. Browser console:0 errors/0 warnings. Impeccable mechanical detector:[] (no findings). Inspected desktop and mobile PNG screenshots.

Saved files:
- `../index.html`: updated live prototype.
- `index-before.html`: full pre-change backup (restore to parent index to revert).
- `integrate.py`: one-time implementation recipe; do not rerun against the changed page.
- `desktop-v1.png`:1280x900 browser QA capture.
- `mobile-v1.png`:390x844 browser QA capture.
- `notes.md`: this handoff.

The screenshots use a deliberately frozen fire impact for visual inspection, so selected controls in those QA images can differ from the staged effect. The live page uses actual selected elements. Drawn particle progression still inherits source-sheet trajectory limitations; this task integrates those designs without regenerating or claiming production interpolation.

Preview: http://localhost/Projects-1/design/prototypes/combat-feel/index.html
