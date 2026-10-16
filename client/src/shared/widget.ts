// The always-on-top widget (GAME_BRIEF §7.1, Codex prototype variant A). Shared by the main process
// (window size) and the renderer (layout), so the two can never disagree.

/** Game pixels of the world scene inside the frame. Shown at 2x on 200% DPI screens. */
export const SCENE_WIDTH = 560
export const SCENE_HEIGHT = 180

/** The framed widget: 4px border + 32px title bar + scene + 46px action bar. */
export const WIDGET_WIDTH = 568
export const WIDGET_HEIGHT = 266

/** Transparent, click-through space above the widget where reward popups appear. */
export const POPUP_SPACE = 150

export const WINDOW_WIDTH = WIDGET_WIDTH
export const WINDOW_HEIGHT = WIDGET_HEIGHT + POPUP_SPACE
