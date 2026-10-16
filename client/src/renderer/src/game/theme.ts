import tokens from '../design/tokens.json'

// World colors come from design/tokens.json (Codex). Do not hard-code new colors here.
// Names follow the action prototype (design/prototypes/action/prototype.js) so ported drawing code reads the same.

const p = tokens.palette

export const C = {
  ink: p.ink,
  outline: p.outline,
  slate: p.slate_dark,
  metal: p.slate_mid,
  silver: p.silver,
  cream: p.cream,
  white: p.white,
  wood: p.wood_dark,
  bark: p.wood_mid,
  gold: p.gold_light,
  brass: p.gold_mid,
  glint: p.gold_glint,
  red: p.red_mid,
  green: p.green_dark,
  leaf: p.green_mid,
  light: p.green_light,
  blue: p.blue_dark
}

export const FONT = [tokens.font.family, ...tokens.font.fallback.map((f) => (f.includes(' ') ? `"${f}"` : f))].join(', ')

export function toColor(hex: string): number {
  return parseInt(hex.slice(1), 16)
}
