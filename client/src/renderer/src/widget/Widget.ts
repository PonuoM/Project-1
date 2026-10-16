import type { Settings } from '../../../shared/settings'
import { api, ApiError } from '../api'
import type { Phase, WorldScene } from '../game/WorldScene'
import { CLASS_NAMES, countdown, fmt, itemName, RARITY_NAMES, SKILL_NAMES, slotName, T } from '../i18n'
import type { GameState, GoldBox, Item, OpenAllResult, Rarity, SyncDelta } from '../types'
import { h, replace, sprite } from '../window/dom'

// The widget's DOM side: server sync, boxes, popups, click-through and dragging. The world scene only animates.

const SYNC_EVERY_MS = 30_000
const MAX_POPUPS = 2
const OPEN_ALL_FROM = 5

const RARITY_VARS: Record<Rarity, string> = {
  0: 'var(--tb-rarity-common)',
  1: 'var(--tb-rarity-uncommon)',
  2: 'var(--tb-rarity-rare)',
  3: 'var(--tb-rarity-epic)',
  4: 'var(--tb-rarity-legendary)'
}

interface Line {
  text: string
  cls?: string
}

const $ = (id: string): HTMLElement => document.getElementById(id) as HTMLElement

export class Widget {
  private state: GameState | null = null
  private clockOffset = 0 // serverTime - Date.now()
  private predictedGold = 0 // animated since the last settle; the server already counts it
  private predictedKills = 0
  private firstSync = true
  private busy = false
  private interactive = false
  private dragging = false
  private notifyGoldReady = true
  private notifiedGold = new Set<number>()
  private goldBaseline = false
  private errorTimer = 0

  private el = {
    region: $('region'),
    stage: $('stage'),
    heroLine: $('hero-line'),
    phase: $('phase'),
    error: $('error'),
    gold: $('gold'),
    wood: $('wood') as HTMLButtonElement,
    openAll: $('openall') as HTMLButtonElement,
    goldBox: $('goldbox') as HTMLButtonElement,
    skill: $('skill') as HTMLButtonElement,
    expand: $('expand') as HTMLButtonElement,
    popups: $('popups'),
    titlebar: $('titlebar')
  }
  private cooldownBar = h('i', { class: 'tw-cooldown' })

  constructor(
    private world: WorldScene,
    regionName: string
  ) {
    this.el.region.textContent = regionName
    this.el.expand.append(sprite('icon_expand'))
    this.el.expand.title = T.expand
    this.el.expand.setAttribute('aria-label', T.expand)
    this.el.wood.title = T.openWoodHint
    this.el.goldBox.title = T.goldBoxHint
    this.el.skill.title = T.skillHint
    this.el.openAll.textContent = T.openAll

    this.el.wood.addEventListener('click', () => void this.openWood())
    this.el.openAll.addEventListener('click', () => void this.openAllWood())
    this.el.goldBox.addEventListener('click', () => void this.openGold())
    this.el.expand.addEventListener('click', () => window.desktop?.openMain())
    this.el.skill.addEventListener('click', () => this.world.queueSkill())
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') {
        e.preventDefault()
        this.world.queueSkill()
      }
    })

    this.setupClickThrough()
    this.setupDrag()

    window.desktop?.onGameChanged(() => void this.sync(false))
    window.desktop?.onSettings((s) => this.applySettings(s))

    window.setInterval(() => this.tick(), 250)
    window.setInterval(() => void this.sync(), SYNC_EVERY_MS)
    this.render()
    void this.sync()
  }

  // ---------- hooks from the world ----------

  onKill(gold: number): void {
    this.predictedGold += gold
    this.predictedKills += 1
    this.render()
  }

  onPhase(phase: Phase): void {
    this.renderPhase(phase)
  }

  applySettings(s: Settings): void {
    this.notifyGoldReady = s.notifyGoldReady
    this.world.setFps(s.stripFps)
  }

  // ---------- click-through and dragging ----------

  /** Take clicks only over the frame or a popup; everywhere else (the transparent popup space) clicks reach the desktop. */
  private setupClickThrough(): void {
    document.addEventListener('mousemove', (e) => {
      if (this.dragging) return
      this.setInteractive(!!(e.target as Element | null)?.closest?.('.tw-widget, .tw-popup'))
    })
    document.addEventListener('mouseout', (e) => {
      if (!e.relatedTarget && !this.dragging) this.setInteractive(false)
    })
  }

  private setInteractive(on: boolean): void {
    if (on === this.interactive) return
    this.interactive = on
    window.desktop?.setInteractive(on)
  }

  private setupDrag(): void {
    const bar = this.el.titlebar
    bar.title = T.dragHint
    bar.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return
      bar.setPointerCapture(e.pointerId)
      this.dragging = true
      bar.classList.add('is-dragging')
      window.desktop?.dragStart()
    })
    const end = () => {
      if (!this.dragging) return
      this.dragging = false
      bar.classList.remove('is-dragging')
      window.desktop?.dragEnd()
    }
    bar.addEventListener('pointerup', end)
    bar.addEventListener('pointercancel', end)
    bar.addEventListener('lostpointercapture', end)
  }

  // ---------- server ----------

  /** @param announce tell the main window; false when the main window asked for this sync. */
  private async sync(announce = true): Promise<void> {
    try {
      const { delta, state } = await api.sync()
      const first = this.firstSync
      this.firstSync = false
      this.applyState(state)
      if (first) {
        if (delta.creditedMs >= 60_000) this.showAwaySummary(delta)
      } else {
        if (delta.wood + delta.goldBoxes > 0) {
          this.world.dropLoot()
          this.bump(delta.goldBoxes > 0 ? this.el.goldBox : this.el.wood)
        }
        if (delta.stageTo > delta.stageFrom) this.world.stageUp(delta.stageTo)
      }
      this.hideError()
      if (announce) window.desktop?.gameChanged('state')
    } catch (e) {
      this.showError(e)
    }
  }

  /** Every state the widget gets comes from a call that settles progress up to now, so the animated extras reset. */
  private applyState(state: GameState): void {
    this.state = state
    this.clockOffset = state.serverTime - Date.now()
    this.predictedGold = 0
    this.predictedKills = 0
    this.world.setHero(state.hero.cls, state.hero.power, state.rates)
    this.render()
  }

  private async run<R>(action: () => Promise<R>, done: (r: R) => void): Promise<void> {
    if (this.busy) return
    this.busy = true
    this.render()
    try {
      done(await action())
    } catch (e) {
      this.showError(e)
    } finally {
      this.busy = false
      this.render()
    }
  }

  private openWood(): Promise<void> {
    if (!this.state || this.state.boxes.wood <= 0) return Promise.resolve()
    return this.run(api.openWood, (r) => {
      this.applyState(r.state)
      this.showItem(r.item, r.powerBefore, r.powerAfter)
      window.desktop?.gameChanged('items')
    })
  }

  private openAllWood(): Promise<void> {
    if (!this.state || this.state.boxes.wood <= 0) return Promise.resolve()
    return this.run(api.openAllWood, (r) => {
      this.applyState(r.state)
      this.showOpenAll(r)
      window.desktop?.gameChanged('items')
    })
  }

  /** Opens the first ready gold box; tells the player to wait when none is ready yet. */
  private openGold(): Promise<void> {
    const box = this.readyGold()[0]
    if (!box) {
      this.showError(new ApiError(409, this.state?.boxes.gold.length ? 'not_ready' : 'no_box'))
      return Promise.resolve()
    }
    return this.run(
      () => api.openGold(box.id),
      (r) => {
        this.applyState(r.state)
        this.showItem(r.item, r.powerBefore, r.powerAfter)
        window.desktop?.gameChanged('items')
      }
    )
  }

  // ---------- rendering ----------

  private now(): number {
    return Date.now() + this.clockOffset
  }

  private readyGold(): GoldBox[] {
    const now = this.now()
    return (this.state?.boxes.gold ?? []).filter((b) => b.unlockAt <= now)
  }

  private render(): void {
    const s = this.state
    const cls = s ? (CLASS_NAMES[s.hero.cls] ?? s.hero.cls) : ''
    const kills = s ? Math.min(s.hero.killsPerStage, s.hero.stageKills + this.predictedKills) : 0
    this.el.stage.textContent = s ? T.stageLine(s.hero.stage, kills, s.hero.killsPerStage) : ''
    this.el.heroLine.textContent = s ? T.heroLine(cls, s.hero.power) : ''
    replace(this.el.gold, sprite('icon_coin'), s ? fmt(s.hero.gold + this.predictedGold) : '–')

    const wood = s?.boxes.wood ?? 0
    replace(this.el.wood, sprite('icon_box_wood'), `×${fmt(wood)}`)
    this.el.wood.disabled = this.busy || wood === 0
    this.el.openAll.hidden = wood < OPEN_ALL_FROM
    this.el.openAll.disabled = this.busy

    replace(this.el.skill, SKILL_NAMES[s?.hero.cls ?? 'melee'] ?? SKILL_NAMES.melee, this.cooldownBar)
    this.renderGoldBox()
    this.renderPhase()
  }

  /** One card for all gold boxes: the soonest one's countdown, "เปิดได้!" when any is ready, and how many there are. */
  private renderGoldBox(): void {
    const boxes = [...(this.state?.boxes.gold ?? [])].sort((a, b) => a.unlockAt - b.unlockAt)
    const btn = this.el.goldBox
    btn.hidden = boxes.length === 0
    if (!boxes.length) return
    const ready = boxes[0].unlockAt <= this.now()
    const label = ready ? T.ready : countdown(boxes[0].unlockAt - this.now())
    replace(btn, sprite('icon_box_gold'), label, boxes.length > 1 && ` ×${boxes.length}`)
    btn.classList.toggle('is-ready', ready)
    btn.disabled = this.busy
  }

  private renderPhase(phase?: Phase): void {
    const s = this.state
    const stuck = !!s && !s.rates.canAdvance && s.hero.stageKills + this.predictedKills >= s.hero.killsPerStage
    if (phase) this.el.phase.dataset.phase = phase
    const current = this.el.phase.dataset.phase ?? 'idle'
    this.el.phase.textContent = stuck ? T.stuck : (T.phases[current] ?? '')
    this.el.phase.classList.toggle('is-stuck', stuck)
  }

  private tick(): void {
    this.renderGoldBox()
    this.cooldownBar.style.width = `${Math.round((1 - this.world.cooldownLeft()) * 100)}%`
    this.announceReadyGold()
  }

  /** Windows toast when a gold box finishes unlocking. Boxes already ready at start are not announced. */
  private announceReadyGold(): void {
    if (!this.state) return
    for (const box of this.readyGold()) {
      if (this.notifiedGold.has(box.id)) continue
      this.notifiedGold.add(box.id)
      if (this.goldBaseline && this.notifyGoldReady) window.desktop?.notify(T.goldReadyTitle, T.goldReadyBody, 'boxes')
      if (this.goldBaseline) this.bump(this.el.goldBox)
    }
    this.goldBaseline = true
  }

  private bump(el: HTMLElement): void {
    el.classList.remove('is-bump')
    void el.offsetWidth // restart the animation
    el.classList.add('is-bump')
  }

  // ---------- popups ----------

  private showItem(item: Item, before: number, after: number): void {
    this.popup(
      [
        { text: itemName(item), cls: 'is-title' },
        { text: `${RARITY_NAMES[item.rarity]} · ${slotName(item.slot)} · พลัง ${fmt(item.power)}`, cls: 'is-tier' },
        item.equipped
          ? { text: T.equipped(after - before), cls: 'is-up' }
          : { text: item.soldFor ? T.soldOne(item.soldFor) : T.stored, cls: 'is-muted' }
      ],
      item.rarity,
      `icon_${item.slot}`,
      item.rarity >= 3 ? 6000 : 3500
    )
  }

  private showOpenAll(r: OpenAllResult): void {
    const counts = r.byRarity
      .map((n, i) => (n > 0 ? `${RARITY_NAMES[i as Rarity]} ${n}` : ''))
      .filter(Boolean)
      .join(' · ')
    const lines: Line[] = [
      { text: T.openedMany(r.opened), cls: 'is-title' },
      { text: counts, cls: 'is-muted' },
      { text: `${T.best}: ${itemName(r.best)} (${RARITY_NAMES[r.best.rarity]})`, cls: 'is-tier' },
      { text: T.powerChange(r.powerBefore, r.powerAfter), cls: r.powerAfter > r.powerBefore ? 'is-up' : 'is-muted' }
    ]
    if (r.autoSold.count > 0) lines.push({ text: T.soldMany(r.autoSold.count, r.autoSold.gold), cls: 'is-muted' })
    this.popup(lines, r.best.rarity, `icon_${r.best.slot}`, 6000)
  }

  private showAwaySummary(d: SyncDelta): void {
    const lines: Line[] = [
      { text: T.awayTitle(d.creditedMs), cls: 'is-title' },
      { text: T.awayGold(d.gold), cls: 'is-accent' },
      { text: T.awayBoxes(d.wood, d.goldBoxes) },
      { text: T.awayStage(d.stageFrom, d.stageTo), cls: 'is-muted' }
    ]
    if (d.capped) lines.push({ text: T.awayCapped, cls: 'is-accent is-small' })
    lines.push({ text: T.tapToClose, cls: 'is-muted is-small' })
    this.popup(lines, 4, 'icon_box_gold', 12_000)
  }

  private popup(lines: Line[], rarity: Rarity, iconKey: string, lifeMs: number): void {
    const el = h(
      'div',
      { class: 'tw-popup', style: `--tw-tier: ${RARITY_VARS[rarity]}`, onclick: () => this.dismiss(el) },
      h('div', { class: 'tw-popup-icon' }, sprite(iconKey)),
      h('div', { class: 'tw-popup-lines' }, ...lines.map((l) => h('span', { class: l.cls ?? '' }, l.text)))
    )
    this.el.popups.append(el)
    const live = [...this.el.popups.querySelectorAll('.tw-popup:not(.is-leaving)')]
    for (const old of live.slice(0, Math.max(0, live.length - MAX_POPUPS))) this.dismiss(old as HTMLElement)
    window.setTimeout(() => this.dismiss(el), lifeMs)
  }

  private dismiss(el: HTMLElement): void {
    if (el.classList.contains('is-leaving')) return
    el.classList.add('is-leaving')
    window.setTimeout(() => el.remove(), 200)
  }

  // ---------- errors ----------

  private showError(e: unknown): void {
    const code = e instanceof ApiError ? e.message : 'default'
    this.el.error.textContent = T.errors[code] ?? T.errors.default
    this.el.error.hidden = false
    window.clearTimeout(this.errorTimer)
    this.errorTimer = window.setTimeout(() => this.hideError(), 5000)
    if (!(e instanceof ApiError)) console.error(e)
  }

  private hideError(): void {
    this.el.error.hidden = true
  }
}
