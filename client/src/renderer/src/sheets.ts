import manifest from './design/manifest.json'

// Codex's sprite contract (design/sprites/manifest.json): horizontal strips, fixed frame size,
// `events.impact` = 0-based hit frame. Shared by the Phaser strip and the DOM main window.

export interface SheetSpec {
  file: string
  frameWidth: number
  frameHeight: number
  frames: number
  fps: number
  loop: boolean
  events?: { impact?: number }
  /** Pixel that sits on the feet line (default: bottom-center). */
  anchor?: { x: number; y: number }
  /** FX only: anchor position relative to the hero's feet; x is forward. */
  offset?: { x: number; y: number }
}

export const SHEETS = manifest.sheets as Record<string, SheetSpec>
