import { SHEETS } from '../sheets'
import type { Rarity } from '../types'

type Child = Node | string | number | null | undefined | false
type Attrs = Record<string, string | number | boolean | null | undefined | EventListener>

/** Tiny element builder: h('button', { class: 'tb-primary', onclick: fn }, 'เปิด'). */
export function h<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Attrs = {}, ...children: Child[]): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag)
  for (const [key, value] of Object.entries(attrs)) {
    if (value === null || value === undefined || value === false) continue
    if (key.startsWith('on') && typeof value === 'function') {
      el.addEventListener(key.slice(2), value)
    } else if (value === true) {
      el.setAttribute(key, '')
    } else {
      el.setAttribute(key, String(value))
    }
  }
  append(el, children)
  return el
}

export function append(el: Element, children: Child[]): void {
  for (const child of children) {
    if (child === null || child === undefined || child === false) continue
    el.append(child instanceof Node ? child : String(child))
  }
}

export function replace(el: Element, ...children: Child[]): void {
  el.replaceChildren()
  append(el, children)
}

/**
 * A Codex sprite as a CSS background (classes from design/mockups/tokens.css). Looping sheets animate with a
 * stepped background-position, using the frame count and fps from the manifest.
 */
export function sprite(key: string, size: 'icon' | 'frame' | 'large' = key.startsWith('icon_') ? 'icon' : 'frame'): HTMLSpanElement {
  const cls = ['tb-sprite', `tb-s-${key}`]
  if (size === 'icon') cls.push('tb-icon')
  if (size === 'large') cls.push('tb-large')
  const el = h('span', { class: cls.join(' '), 'aria-hidden': 'true' })
  const sheet = SHEETS[key]
  if (sheet && sheet.loop && sheet.frames > 1) {
    el.classList.add('tb-anim')
    el.style.setProperty('--frames', String(sheet.frames))
    el.style.setProperty('--dur', `${sheet.frames / Math.max(1, sheet.fps)}s`)
  }
  return el
}

const RARITY_CLASSES: Record<Rarity, string> = {
  0: 'tb-common',
  1: 'tb-uncommon',
  2: 'tb-rare',
  3: 'tb-epic',
  4: 'tb-legendary'
}

export function rarityClass(rarity: Rarity): string {
  return RARITY_CLASSES[rarity]
}
