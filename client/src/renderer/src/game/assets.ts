import Phaser from 'phaser'
import { SHEETS } from '../sheets'

// Loads every sprite sheet listed in design/sprites/manifest.json (Codex) and builds one animation per sheet
// with the same key.

export function preloadSprites(scene: Phaser.Scene): void {
  for (const [key, sheet] of Object.entries(SHEETS)) {
    scene.load.spritesheet(key, `sprites/${sheet.file}`, {
      frameWidth: sheet.frameWidth,
      frameHeight: sheet.frameHeight
    })
  }
}

export function createAnimations(scene: Phaser.Scene): void {
  for (const [key, sheet] of Object.entries(SHEETS)) {
    if (sheet.frames < 2 || scene.anims.exists(key)) continue
    scene.anims.create({
      key,
      frames: scene.anims.generateFrameNumbers(key, { start: 0, end: sheet.frames - 1 }),
      frameRate: sheet.fps,
      repeat: sheet.loop ? -1 : 0
    })
  }
}

/** How long one play of a non-looping animation lasts, in ms. */
export function animDuration(key: string): number {
  const sheet = SHEETS[key]
  return sheet ? (sheet.frames / Math.max(1, sheet.fps)) * 1000 : 0
}

/** Delay from animation start until its impact frame, in ms. */
export function impactDelay(key: string): number {
  const sheet = SHEETS[key]
  if (!sheet) return 0
  return ((sheet.events?.impact ?? Math.floor(sheet.frames / 2)) / Math.max(1, sheet.fps)) * 1000
}
