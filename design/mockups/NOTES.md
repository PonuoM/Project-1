# Mockup handoff

## Recommended strip: Variant A

The 94% ink plate is the default: it gives Thai text a stable ground over spreadsheets and saturated wallpaper. Variant B reduces desktop coverage but depends on outlined text and bright sprite interior edges; it is an optional preference. Both keep the upper 156px empty except transient popups. See all 30 combinations in `strip.html` (5 states × 3 backgrounds × 2 variants).

## Exact band allocation

Coordinates are relative to the 64px band; 12px outer padding and 12px gaps. Total strip is 220px; the band begins y=156. Sprite baseline y=55, sprites 32×32. Windows taskbar begins y=220 and is 48px high, outside the game.

| Region | 1920px x / width | 1366px x / width |
|---|---|---|
| HUD | 12 / 300 | 12 / 260 |
| Playfield | 324 / 1048 | 284 / 594 |
| Box tray | 1384 / 480 | 890 / 420 |
| Expand hit target | 1876 / 32 | 1322 / 32 |

The final expand target ends at width−12 (1908 / 1354). Hero starts at 12% of playfield (approximately x450 / x355), leaving room for monsters. Tray controls are right aligned and their widths fit the allocated tray. At ≤1500px viewport width, HUD and tray use the smaller sizes. The preview adds 16px outside padding; measure its inner context width or use the QA capture at exact scene widths.

## Z order and interaction

- Desktop backdrop and fake taskbar: context only, layer 0.
- Band: layer 10; playfield objects and numbers layer 11–12.
- Reward/offline toast: layer 30, bottom y=148, right 16px.
- Tooltips: layer 40, above the target.
- Inventory compare tooltip: layer 50, local to the main window.

The strip container and passive descendants have `pointer-events:none`; only buttons use `pointer-events:auto`, minimum 24px. The game developer must configure native Windows window hit tests separately; CSS does not create OS-level click-through. Do not ship the fake desktop or taskbar.

## Main window

Fixed 960×600 including its 1px border. Title bar 40px; sidebar 156px; content padding 16px. Each of five tabs fits without document scrolling; inventory scrolls internally. Thai body text 12px, headings 24px. The `tb-drag` region marks the native title-bar drag area; title buttons stay outside it. Tabs support mouse, arrows, Home/End and keyboard focus. Other controls are static game-state examples, with native checkbox/select interactions only.

## Open integration questions

Final game name, actual drop rates, gold unlock durations, expedition rewards/slot entitlement, the GameFont font file, native minimize/close handlers and tooltip placement near window edges remain integration decisions. Mockups avoid inventing drop rates or prices.

## Rebuild

`python design/tools/build_sprites.py`

`python design/tools/build_mockups.py`

The second command mirrors tokens into `tokens.css` and produces both mockups. No external network dependencies. Use `sprites/manifest.json` in the game; do not parse mockup CSS as engine data.
