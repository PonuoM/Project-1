import Phaser from 'phaser'
import './widget/widget.css'
import { DEFAULT_SETTINGS } from '../../shared/settings'
import { SCENE_HEIGHT, SCENE_WIDTH } from '../../shared/widget'
import { loadDesignCss } from './designCss'
import { loadGameFont } from './font'
import type { BackgroundConfig, RegionBackground } from './game/backdrop'
import { C } from './game/theme'
import { WorldScene } from './game/WorldScene'
import { T } from './i18n'
import { Widget } from './widget/Widget'

/** Codex's production parallax layers when present (public/backgrounds/), else the procedural forest. */
async function loadBackground(): Promise<{ name: string; region: RegionBackground | null }> {
  try {
    const res = await fetch('backgrounds/backgrounds.json')
    const config = (await res.json()) as BackgroundConfig
    const [key, region] = Object.entries(config)[0] ?? []
    if (key && region?.layers?.length) return { name: region.th ?? key, region }
  } catch {
    /* not delivered yet */
  }
  return { name: T.regionDefault, region: null }
}

async function boot(): Promise<void> {
  await Promise.all([loadDesignCss(['design/tokens.css'], ['design/widget.css']), loadGameFont()])
  const settings = (await window.desktop?.getSettings()) ?? DEFAULT_SETTINGS
  const background = await loadBackground()

  const game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: 'game',
    width: SCENE_WIDTH,
    height: SCENE_HEIGHT,
    backgroundColor: C.ink,
    pixelArt: true,
    roundPixels: true,
    banner: false,
    fps: { limit: settings.stripFps },
    scale: { mode: Phaser.Scale.NONE }
  })
  await new Promise((resolve) => game.events.once(Phaser.Core.Events.READY, resolve))

  let widget: Widget | null = null
  const world = new WorldScene()
  game.scene.add('world', world, true, {
    background: background.region,
    onKill: (gold: number) => widget?.onKill(gold),
    onPhase: (phase: Parameters<Widget['onPhase']>[0]) => widget?.onPhase(phase)
  })
  await new Promise((resolve) => world.events.once(Phaser.Scenes.Events.CREATE, resolve))

  widget = new Widget(world, background.name)
  widget.applySettings(settings)
}

void boot()
