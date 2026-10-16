import { FPS_OPTIONS, type Settings } from '../../../shared/settings'
import { CLASS_NAMES, countdown, fmt, itemName, RARITY_NAMES, slotName, T, tierLabel, TIERS, W } from '../i18n'
import type { BagItem, GameState, Inventory, Item, Odds, Rarity, Slot } from '../types'
import { h, rarityClass, replace, sprite } from './dom'

// Render functions for the five tabs. Each one rebuilds its panel from the current data; main.ts only calls
// them when their inputs changed. Markup and classes follow design/mockups/window.html.

export type SortKey = 'power' | 'rarity' | 'newest'

export interface Ui {
  sort: SortKey
  slot: Slot | 'all'
  selected: number | null
  /** Which sell button is waiting for a second click. */
  confirm: 'bulk' | 'single' | null
  oddsOpen: boolean
}

export interface App {
  state: GameState | null
  inv: Inventory | null
  odds: Odds | null
  settings: Settings
  ui: Ui
  busy: boolean
  /** Date.now() on the server's clock. */
  now(): number
  setUi(patch: Partial<Ui>): void
  openWood(): void
  openAllWood(): void
  openGold(id: number): void
  equip(id: number): void
  sell(ids: number[], confirm: 'bulk' | 'single'): void
  setAutoSell(rarities: Rarity[]): void
  setSettings(patch: Partial<Settings>): void
}

const SLOTS: Slot[] = ['weapon', 'armor', 'ring']
const OPEN_ALL_LIMIT = 200

const itemIcon = (slot: Slot): HTMLSpanElement => sprite(`icon_${slot}`)

function header(title: string, sub: string): HTMLElement {
  return h('header', { class: 'tb-panel-header' }, h('div', {}, h('h1', {}, title), h('p', {}, sub)))
}

function loading(el: HTMLElement, title: string): void {
  replace(el, header(title, W.loading))
}

// ---------- nav ----------

export function renderNav(el: HTMLElement, app: App): void {
  const s = app.state
  if (!s) return replace(el)
  replace(
    el,
    h('p', { class: 'tb-accent' }, sprite('icon_coin'), ` ${fmt(s.hero.gold)}`),
    h('p', { class: 'tb-muted' }, W.navStage(s.hero.stage, CLASS_NAMES[s.hero.cls] ?? s.hero.cls))
  )
}

// ---------- hero ----------

export function renderHero(el: HTMLElement, app: App): void {
  const s = app.state
  if (!s) return loading(el, W.tabs.hero)

  const equipment = SLOTS.map((slot) => {
    const item = s.equipped[slot]
    if (!item) {
      return h(
        'div',
        { class: 'tb-equipment-item' },
        h('div', { class: 'tb-item-icon' }, itemIcon(slot)),
        h('div', {}, h('small', {}, slotName(slot)), h('strong', { class: 'tb-muted' }, W.emptySlot))
      )
    }
    const rc = rarityClass(item.rarity)
    return h(
      'div',
      { class: 'tb-equipment-item' },
      h('div', { class: `tb-item-icon tb-rarity ${rc}` }, itemIcon(slot)),
      h(
        'div',
        {},
        h('small', {}, slotName(slot)),
        h('strong', {}, itemName(item)),
        h('p', { class: `${rc} tb-tier` }, tierLabel(item.rarity)),
        h('small', {}, W.powerPlus(item.power))
      )
    )
  })

  const skills = [1, 2, 3, 4].map((n) =>
    h('div', { class: 'tb-skill tb-skill--empty' }, h('strong', {}, W.skillSlot(n)), h('span', {}, W.skillSoon))
  )

  replace(
    el,
    header(W.tabs.hero, W.heroSub),
    h(
      'div',
      { class: 'tb-hero-summary' },
      h('div', { class: 'tb-hero-stage' }, sprite(`hero_${s.hero.cls}_idle`, 'large')),
      h(
        'div',
        {},
        h('h2', {}, CLASS_NAMES[s.hero.cls] ?? s.hero.cls),
        h('p', { class: 'tb-power' }, T.power(s.hero.power)),
        h('p', {}, W.heroStage(s.hero.stage, s.hero.totalKills)),
        h('p', { class: 'tb-muted' }, W.heroPace(s.rates.killMs, s.rates.goldPerKill)),
        !s.rates.canAdvance && h('p', { class: 'tb-accent' }, W.heroStuck)
      )
    ),
    h('div', {}, h('h2', { class: 'tb-section-title' }, W.equipment), h('div', { class: 'tb-equipment' }, ...equipment)),
    h('div', {}, h('h2', { class: 'tb-section-title' }, W.skills), h('div', { class: 'tb-skills' }, ...skills)),
    h('p', { class: 'tb-footnote' }, W.heroFoot)
  )
}

// ---------- bag ----------

let compareEl: HTMLElement | null = null

/** Compare card for a bag item against what is equipped in the same slot. */
function showCompare(anchor: HTMLElement, item: BagItem, equipped: Item | null): void {
  compareEl ??= document.body.appendChild(h('div', { class: 'tb-compare is-floating', role: 'tooltip' }))
  replace(
    compareEl,
    h('strong', {}, itemName(item)),
    h('br'),
    h('span', { class: `tb-tier ${rarityClass(item.rarity)}` }, tierLabel(item.rarity)),
    h('br'),
    `พลัง ${fmt(item.power)}`,
    h('br'),
    compareLine(item, equipped)
  )
  compareEl.hidden = false
  const a = anchor.getBoundingClientRect()
  const c = compareEl.getBoundingClientRect()
  const top = a.bottom + 4 + c.height <= window.innerHeight - 8 ? a.bottom + 4 : a.top - 4 - c.height
  compareEl.style.top = `${Math.max(8, top)}px`
  compareEl.style.left = `${Math.max(8, Math.min(a.left, window.innerWidth - c.width - 8))}px`
}

function hideCompare(): void {
  if (compareEl) compareEl.hidden = true
}

function compareLine(item: Item, equipped: Item | null): HTMLElement {
  if (!equipped) return h('span', { class: 'tb-up' }, W.compareEmpty)
  const diff = item.power - equipped.power
  if (diff > 0) return h('span', { class: 'tb-up' }, W.compareUp(diff))
  if (diff < 0) return h('span', { class: 'tb-muted' }, W.compareDown(-diff))
  return h('span', { class: 'tb-muted' }, W.compareSame)
}

function sortItems(items: BagItem[], sort: SortKey, slot: Slot | 'all'): BagItem[] {
  const list = slot === 'all' ? [...items] : items.filter((i) => i.slot === slot)
  const byPower = (a: BagItem, b: BagItem) => b.power - a.power
  const byRarity = (a: BagItem, b: BagItem) => b.rarity - a.rarity
  if (sort === 'power') return list.sort((a, b) => byPower(a, b) || byRarity(a, b))
  if (sort === 'rarity') return list.sort((a, b) => byRarity(a, b) || byPower(a, b))
  return list.sort((a, b) => b.id - a.id)
}

function select<T extends string>(label: string, value: T, options: Record<T, string>, onChange: (v: T) => void): HTMLElement {
  const sel = h(
    'select',
    { 'aria-label': label, onchange: () => onChange(sel.value as T) },
    ...Object.entries<string>(options).map(([v, text]) => h('option', { value: v, selected: v === value }, text))
  )
  return h('label', {}, `${label} `, sel)
}

export function renderInventory(el: HTMLElement, app: App): void {
  hideCompare()
  const { inv, state, ui } = app
  if (!inv || !state) return loading(el, W.tabs.inventory)

  const items = sortItems(inv.items, ui.sort, ui.slot)
  const full = inv.items.length >= inv.capacity

  const toolbar = h(
    'div',
    { class: 'tb-toolbar' },
    select(W.sortBy, ui.sort, W.sorts, (sort) => app.setUi({ sort, selected: null })),
    select(W.slotFilter, ui.slot, { all: W.allSlots, weapon: slotName('weapon'), armor: slotName('armor'), ring: slotName('ring') }, (slot) =>
      app.setUi({ slot, selected: null })
    )
  )

  // Auto-sell: the same rarities also drive the "sell what's already in the bag" button.
  const autoRarities = Array.from({ length: inv.autoSellMax + 1 }, (_, r) => r as Rarity)
  const matching = inv.items.filter((i) => inv.autoSell.includes(i.rarity))
  const matchingGold = matching.reduce((sum, i) => sum + i.sellValue, 0)
  const autoSell = h(
    'div',
    { class: 'tb-auto-sell', title: W.autoSellHint },
    h('strong', {}, W.autoSell),
    ...autoRarities.map((r) => {
      const box = h('input', {
        type: 'checkbox',
        checked: inv.autoSell.includes(r),
        disabled: app.busy,
        onchange: () => {
          const next = autoRarities.filter((x) => (x === r ? box.checked : inv.autoSell.includes(x)))
          app.setAutoSell(next)
        }
      })
      return h('label', {}, box, ` ${tierLabel(r)}`)
    }),
    h('span', { class: 'tb-grow' }),
    matching.length > 0 &&
      h(
        'button',
        {
          class: ui.confirm === 'bulk' ? 'tb-primary' : '',
          disabled: app.busy,
          onclick: () => app.sell(matching.map((i) => i.id), 'bulk')
        },
        ui.confirm === 'bulk' ? W.confirmSell(matching.length) : W.sellMatching(matching.length, matchingGold)
      )
  )

  const grid =
    items.length === 0
      ? h('div', { class: 'tb-empty' }, sprite('icon_armor'), h('p', {}, W.bagEmpty))
      : h(
          'div',
          { class: 'tb-inventory' },
          ...items.map((item) => {
            const rc = rarityClass(item.rarity)
            const cell = h(
              'button',
              {
                class: `tb-inventory-cell tb-rarity ${rc}${ui.selected === item.id ? ' is-selected' : ''}`,
                'aria-label': `${itemName(item)} ${tierLabel(item.rarity)} พลัง ${item.power}`,
                'aria-pressed': ui.selected === item.id ? 'true' : 'false',
                onclick: () => app.setUi({ selected: ui.selected === item.id ? null : item.id, confirm: null }),
                ondblclick: () => app.equip(item.id),
                onmouseenter: () => showCompare(cell, item, state.equipped[item.slot]),
                onmouseleave: hideCompare,
                onfocus: () => showCompare(cell, item, state.equipped[item.slot]),
                onblur: hideCompare
              },
              h('span', { class: 'tb-marker' }, TIERS[item.rarity]),
              itemIcon(item.slot),
              h('span', { class: 'tb-score' }, fmt(item.power))
            )
            return cell
          })
        )

  const selected = inv.items.find((i) => i.id === ui.selected)
  const actionbar = selected
    ? h(
        'div',
        { class: 'tb-actionbar' },
        h('div', { class: `tb-item-icon tb-rarity ${rarityClass(selected.rarity)}` }, itemIcon(selected.slot)),
        h(
          'div',
          { class: 'tb-grow' },
          h('strong', {}, itemName(selected)),
          h('br'),
          h('span', { class: `tb-tier ${rarityClass(selected.rarity)}` }, tierLabel(selected.rarity)),
          ` · พลัง ${fmt(selected.power)} · `,
          compareLine(selected, state.equipped[selected.slot])
        ),
        h('button', { class: 'tb-primary', disabled: app.busy, onclick: () => app.equip(selected.id) }, W.equip),
        h(
          'button',
          { disabled: app.busy, onclick: () => app.sell([selected.id], 'single') },
          ui.confirm === 'single' ? W.confirmSell(1) : W.sellFor(selected.sellValue)
        )
      )
    : h('p', { class: 'tb-footnote' }, full ? h('span', { class: 'tb-accent' }, W.bagFull) : W.bagFoot)

  replace(el, header(W.tabs.inventory, W.bagSub(inv.items.length, inv.capacity)), toolbar, autoSell, grid, actionbar)
}

// ---------- boxes ----------

export function renderBoxes(el: HTMLElement, app: App): void {
  const s = app.state
  if (!s) return loading(el, W.tabs.boxes)
  const wood = s.boxes.wood
  const now = app.now()

  const woodSummary = h(
    'div',
    { class: 'tb-wood-summary' },
    h('div', { class: 'tb-inline' }, sprite('box_wood_idle'), h('div', {}, h('h2', {}, W.woodCount(wood)), h('p', { class: 'tb-muted' }, W.woodHint))),
    h(
      'div',
      { class: 'tb-button-row' },
      h('button', { disabled: app.busy || wood === 0, onclick: () => app.openWood() }, W.openOne),
      h('button', { class: 'tb-primary', disabled: app.busy || wood === 0, onclick: () => app.openAllWood() }, W.openAll(OPEN_ALL_LIMIT))
    )
  )

  const rows = s.boxes.gold.map((box) => {
    const ready = box.unlockAt <= now
    return h(
      'div',
      { class: 'tb-row' },
      h(
        'div',
        { class: 'tb-inline' },
        sprite(ready ? 'box_gold_ready' : 'box_gold_locked'),
        h('div', {}, h('strong', {}, W.goldBox), h('p', { class: 'tb-muted' }, ready ? W.goldReady : W.goldLocked))
      ),
      ready
        ? h('span', { class: 'tb-timer tb-accent' }, W.goldReadyTimer)
        : h('span', { class: 'tb-timer', 'data-unlock': box.unlockAt }, countdown(box.unlockAt - now)),
      ready
        ? h('button', { class: 'tb-primary', disabled: app.busy, onclick: () => app.openGold(box.id) }, W.openBox)
        : h('button', { disabled: true }, W.waitUnlock)
    )
  })

  const odds = app.odds
  const details = h(
    'details',
    { class: 'tb-rates', open: app.ui.oddsOpen, ontoggle: () => (app.ui.oddsOpen = details.open) },
    h('summary', {}, W.odds),
    odds &&
      h(
        'table',
        { class: 'tb-odds' },
        h('thead', {}, h('tr', {}, h('th', {}, W.oddsRarity), h('th', {}, 'กล่องไม้'), h('th', {}, 'กล่องทอง'))),
        h(
          'tbody',
          {},
          ...([0, 1, 2, 3, 4] as Rarity[]).map((r) =>
            h(
              'tr',
              {},
              h('td', {}, h('span', { class: `tb-tier ${rarityClass(r)}` }, tierLabel(r))),
              h('td', {}, `${odds.boxes.wood[r]}%`),
              h('td', {}, `${odds.boxes.gold[r]}%`)
            )
          )
        )
      ),
    odds && h('p', { class: 'tb-muted' }, W.oddsPerKill(odds.perKill.wood, odds.perKill.gold)),
    odds && h('p', { class: 'tb-muted' }, W.oddsUnlock(odds.goldUnlockMs))
  )

  replace(
    el,
    header(W.tabs.boxes, W.boxesSub),
    woodSummary,
    h('h2', {}, W.goldBoxes),
    h('div', { class: 'tb-box-list' }, ...(rows.length ? rows : [h('p', { class: 'tb-muted' }, W.goldEmpty)])),
    details
  )
}

/** Once a second: tick the visible countdowns without rebuilding the panel. */
export function tickTimers(root: HTMLElement, now: number): void {
  for (const el of root.querySelectorAll<HTMLElement>('[data-unlock]')) {
    el.textContent = countdown(Number(el.dataset.unlock) - now)
  }
}

/** Ids of gold boxes that are ready right now; the boxes panel re-renders when this changes. */
export function readyGoldKey(app: App): string {
  const now = app.now()
  return (app.state?.boxes.gold ?? []).map((b) => `${b.id}:${b.unlockAt <= now ? 1 : 0}`).join(',')
}

// ---------- expeditions ----------

export function renderExpeditions(el: HTMLElement): void {
  replace(
    el,
    header(W.tabs.expeditions, W.expeditionsSub),
    h('div', { class: 'tb-empty' }, sprite('hero_ranged_idle', 'large'), h('h2', {}, W.expeditionsSoon), h('p', {}, W.expeditionsSoonHint))
  )
}

// ---------- settings ----------

export function renderSettings(el: HTMLElement, app: App): void {
  const s = app.settings
  const fps = h(
    'select',
    { id: 'fps', onchange: () => app.setSettings({ stripFps: Number(fps.value) }) },
    ...FPS_OPTIONS.map((n) => h('option', { value: n, selected: n === s.stripFps }, `${n} FPS`))
  )
  const notifyGold = h('input', {
    type: 'checkbox',
    checked: s.notifyGoldReady,
    onchange: () => app.setSettings({ notifyGoldReady: notifyGold.checked })
  })

  replace(
    el,
    header(W.tabs.settings, W.settingsSub),
    h(
      'div',
      { class: 'tb-settings' },
      h('div', { class: 'tb-setting-row' }, h('div', {}, h('label', { for: 'fps' }, W.fps), h('p', { class: 'tb-muted' }, W.fpsHint)), fps),
      h(
        'div',
        { class: 'tb-setting-row' },
        h('strong', {}, W.notifications),
        h('div', { class: 'tb-notifications' }, h('label', {}, notifyGold, ` ${W.notifyGoldReady}`))
      ),
      h(
        'div',
        { class: 'tb-setting-row' },
        h('div', {}, h('strong', {}, W.fullscreen), h('p', { class: 'tb-muted' }, W.soon)),
        h(
          'div',
          { class: 'tb-setting-options' },
          h('label', {}, h('input', { type: 'radio', name: 'fullscreen', checked: true, disabled: true }), ` ${W.fullscreenHide}`),
          h('label', {}, h('input', { type: 'radio', name: 'fullscreen', disabled: true }), ` ${W.fullscreenKeep}`)
        )
      ),
      h(
        'div',
        { class: 'tb-setting-row' },
        h('label', { for: 'language' }, W.language),
        h('select', { id: 'language', disabled: true }, h('option', { selected: true }, 'ไทย'), h('option', {}, `English ${W.soon}`))
      )
    ),
    h('p', { class: 'tb-footnote' }, W.settingsFoot)
  )
}

// ---------- toasts ----------

export interface ToastLine {
  text: string
  cls?: string
}

export function itemToastLines(item: Item, before: number, after: number): ToastLine[] {
  return [
    { text: itemName(item) },
    { text: `${tierLabel(item.rarity)} · ${slotName(item.slot)} · พลัง ${fmt(item.power)}`, cls: `tb-tier ${rarityClass(item.rarity)}` },
    item.equipped
      ? { text: T.equipped(after - before), cls: 'tb-up' }
      : item.soldFor
        ? { text: T.soldOne(item.soldFor), cls: 'tb-muted' }
        : { text: T.stored, cls: 'tb-muted' }
  ]
}

export function rarityCounts(byRarity: number[]): string {
  return byRarity
    .map((n, i) => (n > 0 ? `${RARITY_NAMES[i as Rarity]} ${fmt(n)}` : ''))
    .filter(Boolean)
    .join(' · ')
}
