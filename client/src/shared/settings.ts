// Per-device preferences, stored by the main process in userData/settings.json and shared with every window.
// Anything that affects rewards lives on the server instead (e.g. auto-sell).

/** 60 is needed for the 35ms wind-up poses; 30 is the battery saver. */
export const FPS_OPTIONS = [30, 60] as const

export interface Settings {
  stripFps: number
  notifyGoldReady: boolean
  /** Widget window top-left in screen DIPs; null = default spot (bottom-right above the taskbar). */
  widgetX: number | null
  widgetY: number | null
}

export const DEFAULT_SETTINGS: Settings = {
  stripFps: 60,
  notifyGoldReady: true,
  widgetX: null,
  widgetY: null
}

const coord = (v: unknown): number | null => (typeof v === 'number' && Number.isFinite(v) ? Math.round(v) : null)

export function sanitizeSettings(raw: Partial<Settings>): Settings {
  return {
    stripFps: (FPS_OPTIONS as readonly number[]).includes(Number(raw.stripFps)) ? Number(raw.stripFps) : DEFAULT_SETTINGS.stripFps,
    notifyGoldReady: typeof raw.notifyGoldReady === 'boolean' ? raw.notifyGoldReady : DEFAULT_SETTINGS.notifyGoldReady,
    widgetX: coord(raw.widgetX),
    widgetY: coord(raw.widgetY)
  }
}
