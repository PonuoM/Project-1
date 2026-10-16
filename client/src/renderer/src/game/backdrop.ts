import Phaser from 'phaser'
import { SCENE_HEIGHT, SCENE_WIDTH } from '../../../shared/widget'
import { C } from './theme'

// Parallax background. Codex's production layers (design/backgrounds/backgrounds.json) are used when present;
// until then the dark-forest scene from Codex's action prototype is painted procedurally into tileable textures.

/** Feet line of every character, in scene pixels. The bottom 28px is the ground strip. */
export const GROUND_Y = SCENE_HEIGHT - 28

export interface LayerSpec {
  file: string
  parallax: number
  y?: number
}

export interface RegionBackground {
  th?: string
  sky?: string
  layers: LayerSpec[]
}

export type BackgroundConfig = Record<string, RegionBackground>

interface Layer {
  tile: Phaser.GameObjects.TileSprite
  parallax: number
}

export class Backdrop {
  private layers: Layer[] = []

  constructor(private scene: Phaser.Scene) {}

  /** Codex PNG layers (already loaded by key `bg:<file>`) — nearest layer last. */
  fromConfig(region: RegionBackground): void {
    this.scene.add.rectangle(0, 0, SCENE_WIDTH, SCENE_HEIGHT, Phaser.Display.Color.HexStringToColor(region.sky ?? C.ink).color).setOrigin(0).setScrollFactor(0)
    for (const spec of region.layers) {
      const key = `bg:${spec.file}`
      const frame = this.scene.textures.getFrame(key)
      if (!frame) continue
      this.add(key, spec.parallax, spec.y ?? 0, frame.height)
    }
  }

  /** Procedural dark forest (prototype art), painted once into tileable canvases. */
  procedural(): void {
    const sky = this.paint('bg:sky', SCENE_WIDTH, (g) => {
      rect(g, 0, 0, SCENE_WIDTH, SCENE_HEIGHT, C.ink)
      rect(g, 0, 0, SCENE_WIDTH, Math.round(SCENE_HEIGHT * 0.53), C.outline)
      // Small moon and a broken cloud: a light anchor that does not fill the desktop.
      const mx = Math.round(SCENE_WIDTH * 0.74)
      rect(g, mx, 24, 18, 18, C.silver)
      rect(g, mx - 3, 29, 24, 8, C.silver)
      rect(g, mx + 8, 22, 12, 12, C.outline)
      rect(g, mx - 14, 43, 64, 4, C.slate)
    })
    this.scene.add.image(0, 0, sky).setOrigin(0).setScrollFactor(0)

    for (const layer of [0, 1]) {
      const step = 130 - layer * 20
      const count = 10
      this.addPainted(`bg:mountains${layer}`, 0.11 + layer * 0.17, step, count, (g, x, i) =>
        poly(g, [[x - 30, GROUND_Y], [x + 50, GROUND_Y - 60 - layer * 22 - random(i + layer) * 25], [x + 140, GROUND_Y]], layer ? C.blue : C.slate)
      )
    }
    this.addPainted('bg:farTrees', 0.5, 80, 16, (g, x, i) => tree(g, x, GROUND_Y - 2, 90 + random(i) * 50, i, false))
    this.addPainted('bg:nearTrees', 0.82, 155, 10, (g, x, i) => tree(g, x + 20, GROUND_Y + 4, 115 + random(i) * 45, i, true))
    // Half-buried stone arches along the route.
    this.addPainted('bg:arches', 1, 380, 4, (g, x) => {
      const gy = GROUND_Y
      rect(g, x + 265, gy - 49, 11, 49, C.slate)
      rect(g, x + 302, gy - 38, 12, 38, C.slate)
      rect(g, x + 263, gy - 52, 17, 5, C.metal)
      rect(g, x + 263, gy - 54, 52, 5, C.slate)
      rect(g, x + 269, gy - 40, 2, 17, C.metal)
      rect(g, x + 266, gy - 4, 15, 4, C.green)
    })
    this.addPainted(
      'bg:ground',
      1,
      32,
      39,
      (g, x, i) => {
        rect(g, x, GROUND_Y + 7, 30, 9, C.slate)
        rect(g, x + 1, GROUND_Y + 7, 26, 1, C.metal)
        rect(g, x + 4, GROUND_Y + 19, 29, 8, C.outline)
        if (i % 3 === 0) {
          rect(g, x + 3, GROUND_Y - 2, 8, 2, C.leaf)
          rect(g, x + 13, GROUND_Y + 3, 2, 3, C.ink)
        }
      },
      (g, width) => {
        rect(g, 0, GROUND_Y, width, SCENE_HEIGHT - GROUND_Y, C.wood)
        rect(g, 0, GROUND_Y, width, 4, C.green)
        rect(g, 0, GROUND_Y + 4, width, 2, C.ink)
      }
    )
  }

  /** Scroll every layer by its parallax factor; camX is the world camera's left edge. */
  update(camX: number): void {
    for (const l of this.layers) l.tile.tilePositionX = Math.round(camX * l.parallax)
  }

  private add(key: string, parallax: number, y: number, height: number): void {
    const tile = this.scene.add.tileSprite(0, y, SCENE_WIDTH, height, key).setOrigin(0).setScrollFactor(0)
    this.layers.push({ tile, parallax })
  }

  /**
   * One tileable layer: `count` elements every `step` px. Each element is also drawn one texture-width to the
   * left and right, and seeds repeat every `count`, so the seam is invisible.
   */
  private addPainted(
    key: string,
    parallax: number,
    step: number,
    count: number,
    element: (g: CanvasRenderingContext2D, x: number, i: number) => void,
    base?: (g: CanvasRenderingContext2D, width: number) => void
  ): void {
    const width = step * count
    this.paint(key, width, (g) => {
      base?.(g, width)
      for (const shift of [-width, 0, width]) {
        for (let i = 0; i < count; i++) element(g, i * step + shift, i)
      }
    })
    this.add(key, parallax, 0, SCENE_HEIGHT)
  }

  private paint(key: string, width: number, draw: (g: CanvasRenderingContext2D) => void): string {
    const texture = this.scene.textures.createCanvas(key, width, SCENE_HEIGHT)
    if (!texture) throw new Error(`[backdrop] could not create ${key}`)
    draw(texture.getContext())
    texture.refresh()
    return key
  }
}

// ---------- pixel drawing (ported from the prototype; integer rasterization keeps edges crisp) ----------

export function random(n: number): number {
  return Math.abs(Math.sin(n * 127.1 + 311.7) * 43758.5453) % 1
}

function rect(g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, color: string): void {
  g.fillStyle = color
  g.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h))
}

/** Scanline polygon fill without antialiasing. */
function poly(g: CanvasRenderingContext2D, points: number[][], color: string): void {
  g.fillStyle = color
  const lo = Math.ceil(Math.min(...points.map((p) => p[1])))
  const hi = Math.floor(Math.max(...points.map((p) => p[1])))
  for (let y = lo; y <= hi; y++) {
    const xs: number[] = []
    for (let i = 0; i < points.length; i++) {
      const a = points[i]
      const b = points[(i + 1) % points.length]
      if ((a[1] <= y && b[1] > y) || (b[1] <= y && a[1] > y)) xs.push(a[0] + ((y - a[1]) * (b[0] - a[0])) / (b[1] - a[1]))
    }
    xs.sort((m, n) => m - n)
    for (let i = 0; i + 1 < xs.length; i += 2) {
      g.fillRect(Math.ceil(xs[i]), y, Math.max(1, Math.floor(xs[i + 1]) - Math.ceil(xs[i]) + 1), 1)
    }
  }
}

/** Bent trunk, forked branches and an irregular stepped broadleaf crown. */
function tree(g: CanvasRenderingContext2D, x: number, base: number, height: number, seed: number, near: boolean): void {
  const top = base - height
  const trunk = near ? C.wood : C.slate
  const leaf = near ? C.green : C.blue
  poly(g, [[x - 9, base], [x - 4, base - 25], [x - 7, top + 37], [x - 3, top + 22], [x + 4, top + 23], [x + 2, base - 47], [x + 6, base - 16], [x + 13, base]], trunk)
  poly(g, [[x - 4, top + 54], [x - 25, top + 29], [x - 22, top + 20], [x + 1, top + 43], [x + 23, top + 22], [x + 27, top + 27], [x + 4, top + 61]], trunk)
  if (near) {
    rect(g, x - 4, top + 44, 2, height - 51, C.bark)
    rect(g, x + 3, base - 21, 2, 17, C.bark)
    rect(g, x - 12, base - 2, 26, 2, C.green)
  }
  for (let k = 0; k < 4; k++) {
    const cx = x + [-27, 0, 24, -8][k]
    const cy = top + [18, 2, 21, 32][k]
    const w = [27, 32, 29, 25][k]
    const h = [17, 22, 19, 16][k]
    poly(
      g,
      [
        [cx - w + 5, cy], [cx - w + 12, cy - 5], [cx - 9, cy - 7], [cx - 2, cy - 11], [cx + 12, cy - 8], [cx + w - 9, cy - 4],
        [cx + w - 3, cy + 2], [cx + w, cy + 9], [cx + w - 5, cy + h - 3], [cx + 12, cy + h], [cx + 3, cy + h + 4],
        [cx - 8, cy + h], [cx - w + 3, cy + h - 3], [cx - w, cy + 8]
      ],
      leaf
    )
    if (near) {
      for (let j = 0; j < 6; j++) rect(g, cx - w + 8 + j * 7, cy - 2 + Math.round(random(seed * 13 + k * 7 + j) * 5), 5, 2, C.leaf)
      rect(g, cx - w + 8, cy + 7, 7, 2, C.leaf)
    }
  }
}
