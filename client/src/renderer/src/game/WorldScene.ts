import Phaser from 'phaser'
import { SCENE_WIDTH } from '../../../shared/widget'
import { fmt } from '../i18n'
import { SHEETS } from '../sheets'
import { createAnimations, preloadSprites } from './assets'
import { Backdrop, GROUND_Y, random, type RegionBackground } from './backdrop'
import { C, FONT, toColor } from './theme'

// The world inside the widget: parallax forest, a hero who really walks, monsters, and fast heavy hits.
// Timing and feel come from Codex's action prototype (design/prototypes/action) as approved by the owner.
// Everything here is visual: kills and gold are paced by the server's rates.killMs, and the server decides rewards.

const HERO_VIEW_X = 0.29 // hero stands at 29% of the view while the camera follows
const HERO_SPEED = 0.105 // px/ms
const FOE_SPEED = 0.014
const ENGAGE_GAP = 66
const MAX_STRIKES = 8
const STRIKE_SPACING = 320 // ms of fight time per visual strike
const SKILL_COOLDOWN_MS = 1600
const SKILL_EVERY_KILLS = 3
const DEATH_FRAME_MS = 85
const PAN_RETURN_DELAY_MS = 1200

interface Timing {
  windup: number
  lunge: number
  hold: number
  recover: number
  shake: number
  knock: number
}

// Slash 35 → 55 → stop 45 → 105ms; skill 70 → 65 → stop 60 → 145ms (GAME_BRIEF §7.1).
const SLASH: Timing = { windup: 35, lunge: 55, hold: 45, recover: 105, shake: 110, knock: 9 }
const SKILL: Timing = { windup: 70, lunge: 65, hold: 60, recover: 145, shake: 180, knock: 16 }

export type Phase = 'idle' | 'walk' | 'fight' | 'impact'

export interface Rates {
  killMs: number
  goldPerKill: number
}

export interface WorldInit {
  background: RegionBackground | null
  onKill(gold: number): void
  onPhase(phase: Phase): void
}

interface Strike {
  kind: 'slash' | 'skill'
  timing: Timing
  t: number
  hit: boolean
}

interface Foe {
  type: string
  sprite: Phaser.GameObjects.Sprite
  x: number
  hp: number // strikes left
  maxHp: number
  flash: number
  hurt: number
  dying: number // ms since death, -1 while alive
  born: number
}

interface Burst {
  x: number
  life: number
  max: number
  skill: boolean
}

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  life: number
  color: number
  size: number
}

interface Chest {
  x: number
  life: number
}

interface FloatText {
  text: Phaser.GameObjects.Text
  x: number
  y: number
  life: number
  max: number
}

export class WorldScene extends Phaser.Scene {
  private hooks!: WorldInit
  private backdrop!: Backdrop
  private hero!: Phaser.GameObjects.Sprite
  private fx!: Phaser.GameObjects.Graphics
  private overlay!: Phaser.GameObjects.Graphics

  private cls = 'melee'
  private power = 0
  private rates: Rates | null = null
  private monsters: string[] = []
  private reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  // world clock: stops during hit stop, so only the world freezes (UI, sync and timers keep running)
  private sim = 0
  private hold = 0
  private heroX = 0
  private mode: Phase = 'idle'
  private phase: Phase = 'idle'
  private foe: Foe | null = null
  private dead: Foe[] = []
  private strike: Strike | null = null
  private fightT = 0
  private nextStrikeAt = 0
  private strikeGap = 0
  private kills = 0
  private cooldown = 0
  private skillQueued = false
  private walkMs = 900

  private bursts: Burst[] = []
  private particles: Particle[] = []
  private floats: FloatText[] = []
  private chests: Chest[] = []

  private pan = 0
  private panning = false
  private panIdle = 0
  private lastPointerX = 0

  constructor() {
    super('world')
  }

  init(data: WorldInit): void {
    this.hooks = data
  }

  preload(): void {
    preloadSprites(this)
    for (const layer of this.hooks.background?.layers ?? []) this.load.image(`bg:${layer.file}`, `backgrounds/${layer.file}`)
  }

  create(): void {
    createAnimations(this)
    this.monsters = ['slime', 'goblin', 'skeleton', 'wolf', 'spider', 'ghost'].filter((m) => SHEETS[`${m}_walk`] && SHEETS[`${m}_death`])

    this.backdrop = new Backdrop(this)
    if (this.hooks.background) this.backdrop.fromConfig(this.hooks.background)
    else this.backdrop.procedural()

    this.overlay = this.add.graphics().setScrollFactor(0).setDepth(5)
    this.hero = this.add.sprite(0, GROUND_Y, this.heroKey('idle'), 0).setDepth(10)
    this.anchor(this.hero, this.heroKey('idle'))
    this.fx = this.add.graphics().setDepth(20)

    // Drag the scene to look around; the camera eases back to the hero shortly after release.
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      this.panning = true
      this.lastPointerX = p.x
    })
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => {
      if (!this.panning || !p.isDown) return
      this.pan -= p.x - this.lastPointerX
      this.lastPointerX = p.x
    })
    const release = () => {
      this.panning = false
      this.panIdle = 0
    }
    this.input.on('pointerup', release)
    this.input.on('pointerupoutside', release)
    this.input.on('gameout', release)

    if (this.rates) this.spawnFoe()
  }

  // ---------- API for the widget ----------

  setHero(cls: string, power: number, rates: Rates | null): void {
    const changed = cls !== this.cls
    this.cls = SHEETS[`hero_${cls}_idle`] ? cls : 'melee'
    this.power = power
    this.rates = rates
    if (!this.hero) return // not created yet; create() spawns the first monster
    if (changed) this.anchor(this.hero, this.heroKey('idle'))
    if (rates && this.mode === 'idle') this.spawnFoe()
  }

  /** Player pressed the skill button: the next strike becomes the skill. */
  queueSkill(): boolean {
    if (this.cooldown > 0) return false
    this.skillQueued = true
    return true
  }

  /** 0 = ready, 1 = just used. */
  cooldownLeft(): number {
    return this.cooldown / SKILL_COOLDOWN_MS
  }

  stageUp(stage: number): void {
    this.playFx('fx_levelup', this.heroX, GROUND_Y - 16)
    this.floatText(this.heroX, GROUND_Y - 58, `ด่าน ${stage}!`, C.light, 16)
  }

  /** New boxes arrived from a sync: a chest pops out where the hero stands. */
  dropLoot(): void {
    this.chests.push({ x: this.heroX + 34, life: 900 })
    this.floatText(this.heroX + 34, GROUND_Y - 22, '+กล่อง', C.gold, 13)
  }

  setFps(fps: number): void {
    // Phaser has no public setter for the frame cap; the loop already runs in capped mode, so swap its rate.
    const loop = this.game.loop as Phaser.Core.TimeStep & { _limitRate: number }
    loop.fpsLimit = fps
    loop._limitRate = 1000 / fps
  }

  // ---------- simulation ----------

  update(_time: number, delta: number): void {
    const real = Math.min(50, delta)
    this.cooldown = Math.max(0, this.cooldown - real)
    if (!this.panning) {
      this.panIdle += real
      if (this.panIdle > PAN_RETURN_DELAY_MS) this.pan *= Math.pow(0.0008, real / 1000)
    }

    if (this.hold > 0) {
      this.hold = Math.max(0, this.hold - real)
    } else {
      this.step(Math.min(32, real))
    }
    this.draw()
  }

  private step(dt: number): void {
    this.sim += dt

    if (this.strike) {
      this.advanceStrike(dt)
    } else if (this.mode === 'walk' && this.foe) {
      this.heroX += dt * HERO_SPEED
      this.foe.x -= dt * FOE_SPEED
      if (this.foe.x - this.heroX < ENGAGE_GAP) this.engage()
    } else if (this.mode === 'fight') {
      this.fightT += dt
      if (this.fightT >= this.nextStrikeAt) this.startStrike()
    }

    if (this.foe) {
      this.foe.flash = Math.max(0, this.foe.flash - dt)
      this.foe.hurt = Math.max(0, this.foe.hurt - dt)
    }
    for (const f of this.dead) f.dying += dt
    this.dead = this.dead.filter((f) => {
      const frames = SHEETS[`${f.type}_death`]?.frames ?? 4
      if (f.dying < frames * DEATH_FRAME_MS + 200) return true
      f.sprite.destroy()
      return false
    })
    for (const p of this.particles) {
      p.life -= dt
      p.x += (p.vx * dt) / 1000
      p.y += (p.vy * dt) / 1000
      p.vy += (220 * dt) / 1000
    }
    this.particles = this.particles.filter((p) => p.life > 0)
    for (const b of this.bursts) b.life -= dt
    this.bursts = this.bursts.filter((b) => b.life > 0)
    for (const c of this.chests) c.life -= dt
    this.chests = this.chests.filter((c) => c.life > 0)
    for (const f of this.floats) f.life -= dt
    this.floats = this.floats.filter((f) => {
      if (f.life > 0) return true
      f.text.destroy()
      return false
    })
  }

  /** Next monster far enough ahead that walking to it takes this kill's walk share of killMs. */
  private spawnFoe(): void {
    if (!this.rates || this.monsters.length === 0) return
    this.walkMs = Math.min(900, this.rates.killMs * 0.6)
    const type = this.monsters[Math.floor(random(this.kills + this.sim) * this.monsters.length) % this.monsters.length]
    const x = this.heroX + ENGAGE_GAP + (HERO_SPEED + FOE_SPEED) * this.walkMs
    const sprite = this.add.sprite(x, GROUND_Y, `${type}_walk`, 0).setDepth(9).setAlpha(0)
    this.anchor(sprite, `${type}_walk`)
    this.foe = { type, sprite, x, hp: 1, maxHp: 1, flash: 0, hurt: 0, dying: -1, born: this.sim }
    this.mode = 'walk'
  }

  /** Split this kill's fight time into visual strikes; the last one kills. */
  private engage(): void {
    if (!this.foe || !this.rates) return
    const fightMs = Math.max(250, this.rates.killMs - this.walkMs)
    const strikes = Phaser.Math.Clamp(Math.floor(fightMs / STRIKE_SPACING), 1, MAX_STRIKES)
    this.foe.hp = this.foe.maxHp = strikes
    this.strikeGap = fightMs / strikes
    this.fightT = 0
    this.nextStrikeAt = Math.min(80, this.strikeGap * 0.3)
    this.mode = 'fight'
  }

  private startStrike(): void {
    if (!this.foe) return
    const last = this.foe.hp === 1
    const auto = last && (this.kills + 1) % SKILL_EVERY_KILLS === 0
    const skill = (this.skillQueued || auto) && this.cooldown <= 0
    if (skill) {
      this.skillQueued = false
      this.cooldown = SKILL_COOLDOWN_MS
    }
    this.strike = { kind: skill ? 'skill' : 'slash', timing: skill ? SKILL : SLASH, t: 0, hit: false }
    this.nextStrikeAt += this.strikeGap
  }

  private advanceStrike(dt: number): void {
    const s = this.strike!
    s.t += dt
    const impactAt = s.timing.windup + s.timing.lunge
    if (!s.hit && s.t >= impactAt) {
      s.t = impactAt
      s.hit = true
      this.impact(s)
    } else if (s.hit && s.t >= impactAt + s.timing.recover) {
      this.strike = null
      if (!this.foe) this.spawnFoe()
    }
  }

  private impact(s: Strike): void {
    const foe = this.foe
    if (!foe) return
    const skill = s.kind === 'skill'
    this.hold = s.timing.hold
    if (!this.reduced) {
      foe.flash = 75
      this.cameras.main.shake(s.timing.shake, (skill ? 4 : 2.5) / SCENE_WIDTH, true)
    }
    foe.x += s.timing.knock
    foe.hurt = 90
    foe.hp -= 1

    const shown = skill ? Math.round(this.power * 2.5) : this.power
    this.floatText(foe.x, GROUND_Y - 58, skill ? `${fmt(shown)}!` : fmt(shown), skill ? C.gold : C.cream, skill ? 17 : 13)
    this.bursts.push({ x: foe.x - 10, life: skill ? 235 : 150, max: skill ? 235 : 150, skill })
    this.playFx('fx_hit', foe.x - 6, GROUND_Y - 14)
    const count = skill ? 30 : 16
    for (let i = 0; i < count; i++) {
      const angle = random(i + this.sim) * Math.PI * 2
      const speed = 35 + random(i + 7) * 95
      this.particles.push({
        x: foe.x - 14,
        y: -25,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 45,
        life: 170 + random(i) * 180,
        color: toColor(i % 4 === 0 ? C.white : i % 3 === 0 ? C.brass : C.gold),
        size: i % 5 === 0 ? 3 : 2
      })
    }
    this.setPhase('impact')

    if (foe.hp <= 0) this.kill(foe)
  }

  private kill(foe: Foe): void {
    const gold = this.rates?.goldPerKill ?? 0
    this.kills += 1
    this.hooks.onKill(gold)
    foe.dying = 0
    foe.sprite.clearTint()
    this.dead.push(foe)
    this.foe = null
    this.mode = 'walk'
    this.floatText(foe.x + 12, GROUND_Y - 32, `+${fmt(gold)}`, C.gold, 13)
    this.playFx('coin_spin', foe.x, GROUND_Y - 20)
  }

  // ---------- drawing ----------

  private draw(): void {
    const cam = this.cameras.main
    cam.scrollX = Math.round(this.heroX - SCENE_WIDTH * HERO_VIEW_X + this.pan)
    this.backdrop.update(cam.scrollX)

    this.drawHero()
    if (this.foe) this.drawFoe(this.foe)
    for (const f of this.dead) this.drawFoe(f)
    this.drawFx()

    if (this.hold === 0) this.setPhase(this.strike || this.mode === 'fight' ? 'fight' : this.mode === 'walk' ? 'walk' : 'idle')
  }

  private drawHero(): void {
    const s = this.strike
    if (!s) {
      const walking = this.mode === 'walk' && !!this.foe
      this.pose(this.hero, this.heroKey(walking ? 'walk' : 'idle'), this.loopFrame(this.heroKey(walking ? 'walk' : 'idle')), this.heroX)
      return
    }
    const key = s.kind === 'skill' && SHEETS[this.heroKey('skill')] ? this.heroKey('skill') : this.heroKey('attack')
    const sheet = SHEETS[key]
    const frames = sheet?.frames ?? 1
    const impactFrame = Math.min(frames - 1, sheet?.events?.impact ?? Math.floor(frames / 2))
    const impactAt = s.timing.windup + s.timing.lunge
    let frame: number
    let lunge: number
    if (s.t < impactAt) {
      // wind-up and lunge share the frames before the impact pose; pull back a little first
      frame = Math.floor((s.t / impactAt) * impactFrame)
      lunge = s.t < s.timing.windup ? -3 : ((s.t - s.timing.windup) / s.timing.lunge) * (s.kind === 'skill' ? 19 : 14)
    } else {
      const k = Math.min(1, (s.t - impactAt) / s.timing.recover)
      frame = impactFrame + Math.floor(k * (frames - impactFrame))
      lunge = (s.kind === 'skill' ? 19 : 14) * (1 - k)
    }
    this.pose(this.hero, key, Math.min(frames - 1, frame), this.heroX + lunge)
  }

  private drawFoe(f: Foe): void {
    let key: string
    let frame: number
    if (f.dying >= 0) {
      key = `${f.type}_death`
      frame = Math.min((SHEETS[key]?.frames ?? 1) - 1, Math.floor(f.dying / DEATH_FRAME_MS))
      const frames = SHEETS[key]?.frames ?? 4
      f.sprite.setAlpha(Phaser.Math.Clamp(1 - (f.dying - frames * DEATH_FRAME_MS) / 200, 0, 1))
    } else {
      const hurtKey = `${f.type}_hurt`
      key = f.hurt > 0 && SHEETS[hurtKey] ? hurtKey : this.mode === 'walk' ? `${f.type}_walk` : `${f.type}_idle`
      frame = key === hurtKey ? 0 : this.loopFrame(key)
      f.sprite.setAlpha(Math.min(1, (this.sim - f.born) / 150))
      if (f.flash > 35) f.sprite.setTintFill(0xffffff)
      else f.sprite.clearTint()
    }
    this.pose(f.sprite, key, frame, f.x)
  }

  private drawFx(): void {
    const g = this.fx
    g.clear()

    // contact shadows
    g.fillStyle(toColor(C.ink), 1)
    g.fillRect(Math.round(this.heroX - 13), GROUND_Y - 1, 27, 2)
    if (this.foe) {
      g.fillRect(Math.round(this.foe.x - 15), GROUND_Y - 1, 28, 2)
      if (this.mode === 'fight' && this.foe.maxHp > 1) {
        g.fillRect(Math.round(this.foe.x - 15), GROUND_Y - 54, 30, 3)
        g.fillStyle(toColor(C.red), 1)
        g.fillRect(Math.round(this.foe.x - 14), GROUND_Y - 53, Math.round((28 * this.foe.hp) / this.foe.maxHp), 1)
      }
    }

    // Slash crescents and skill shockwaves: separate from the character frame so they can overreach it.
    const gy = GROUND_Y
    for (const b of this.bursts) {
      const t = 1 - b.life / b.max
      const x = b.x
      const reach = b.skill ? 95 : 67
      g.fillStyle(toColor(C.gold), 1 - t)
      g.fillPoints(
        [p(x - 35, gy - 62), p(x + 22, gy - 55), p(x + reach, gy - 18), p(x + reach - 12, gy - 4), p(x + 19, gy - 37), p(x - 27, gy - 48)],
        true
      )
      g.fillStyle(toColor(C.white), 1 - t)
      g.fillPoints([p(x - 30, gy - 62), p(x + 22, gy - 55), p(x + reach, gy - 18), p(x + reach - 4, gy - 12), p(x + 19, gy - 48)], true)
      if (b.skill) {
        const radius = 12 + t * 83
        g.fillStyle(toColor(C.gold), 1 - t)
        for (let i = 0; i < 14; i++) {
          const a = (Math.PI * i) / 13
          g.fillRect(Math.round(x + Math.cos(a) * radius), Math.round(gy - Math.sin(a) * radius * 0.24), 4, 2)
        }
        g.fillStyle(toColor(C.glint), 1 - t)
        g.fillRect(x - 22, gy - 68, 5, Math.round(60 * (1 - t)))
        g.fillStyle(toColor(C.brass), 1 - t)
        g.fillPoints([p(x - 20, gy - 5), p(x + 26, gy - 7), p(x + 60, gy), p(x - 45, gy)], true)
      }
    }

    // Loot chest that hops out of the ground and fades (prototype chest, palette colors).
    for (const c of this.chests) {
      const t = 1 - c.life / 900
      const y = gy - Math.round(Math.sin(Math.min(1, t * 2.5) * Math.PI) * 10)
      const a = Math.min(1, c.life / 200)
      const x = Math.round(c.x)
      g.fillStyle(toColor(C.wood), a)
      g.fillRect(x - 7, y - 12, 14, 11)
      g.fillStyle(toColor(C.brass), a)
      g.fillRect(x - 6, y - 11, 12, 9)
      g.fillStyle(toColor(C.gold), a)
      g.fillRect(x - 6, y - 12, 12, 3)
      g.fillStyle(toColor(C.silver), a)
      g.fillRect(x - 1, y - 10, 2, 3)
    }

    for (const q of this.particles) {
      g.fillStyle(q.color, Math.min(1, q.life / 120))
      g.fillRect(Math.round(q.x), Math.round(gy + q.y), q.size, q.size)
    }

    for (const f of this.floats) {
      const t = 1 - f.life / f.max
      f.text.setPosition(Math.round(f.x), Math.round(f.y - t * 20)).setAlpha(Math.min(1, f.life / 170))
    }

    // Fireflies drift with a slow parallax; dim, never blinking at high contrast.
    const o = this.overlay
    o.clear()
    o.fillStyle(toColor(C.light), 1)
    const scroll = this.cameras.main.scrollX
    for (let i = 0; i < 7; i++) {
      const x = (((i * 91 + Math.sin(this.sim * 0.0007 + i) * 7 - scroll * 0.3) % SCENE_WIDTH) + SCENE_WIDTH) % SCENE_WIDTH
      o.fillRect(Math.round(x), Math.round(45 + random(i) * 55), 1, 1)
    }
  }

  // ---------- helpers ----------

  private heroKey(anim: string): string {
    return `hero_${this.cls}_${anim}`
  }

  private loopFrame(key: string): number {
    const sheet = SHEETS[key]
    if (!sheet || sheet.frames < 2) return 0
    return Math.floor((this.sim / 1000) * sheet.fps) % sheet.frames
  }

  private pose(sprite: Phaser.GameObjects.Sprite, key: string, frame: number, x: number): void {
    if (sprite.texture.key !== key) {
      sprite.setTexture(key, frame)
      this.anchor(sprite, key)
    } else if (Number(sprite.frame.name) !== frame) {
      sprite.setFrame(frame)
    }
    sprite.setPosition(Math.round(x), GROUND_Y)
  }

  /** Feet on the ground line: bottom-center unless the manifest gives an anchor. */
  private anchor(sprite: Phaser.GameObjects.Sprite, key: string): void {
    const sheet = SHEETS[key]
    if (!sheet?.anchor) sprite.setOrigin(0.5, 1)
    else sprite.setOrigin(sheet.anchor.x / sheet.frameWidth, (sheet.anchor.y + 1) / sheet.frameHeight)
  }

  /** One play of an FX sheet; looping sheets (e.g. coin_spin) are cut after one cycle. */
  private playFx(key: string, x: number, y: number): void {
    const sheet = SHEETS[key]
    if (!sheet || !this.anims.exists(key)) return
    const fx = this.add.sprite(Math.round(x), Math.round(y), key).setDepth(25).play(key)
    if (sheet.loop) {
      this.tweens.add({ targets: fx, y: fx.y - 18, alpha: 0, duration: 650, onComplete: () => fx.destroy() })
    } else {
      fx.once(Phaser.Animations.Events.ANIMATION_COMPLETE, () => fx.destroy())
    }
  }

  private floatText(x: number, y: number, text: string, color: string, size: number): void {
    const t = this.add
      .text(x, y, text, { fontFamily: FONT, fontSize: `${size}px`, fontStyle: 'bold', color, stroke: C.ink, strokeThickness: 3 })
      .setOrigin(0.5, 1)
      .setDepth(30)
    this.floats.push({ text: t, x, y, life: 650, max: 650 })
  }

  private setPhase(phase: Phase): void {
    if (phase === this.phase) return
    this.phase = phase
    this.hooks.onPhase(phase)
  }
}

const p = (x: number, y: number): Phaser.Types.Math.Vector2Like => ({ x: Math.round(x), y: Math.round(y) })
