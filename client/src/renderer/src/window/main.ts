import './window.css'
import { DEFAULT_SETTINGS, type Settings } from '../../../shared/settings'
import { api, ApiError } from '../api'
import { loadDesignCss } from '../designCss'
import { loadGameFont } from '../font'
import { itemName, T, W } from '../i18n'
import type { GameState, Item, OpenAllResult, Rarity } from '../types'
import { h, rarityClass, replace, sprite } from './dom'
import {
  type App,
  itemToastLines,
  rarityCounts,
  readyGoldKey,
  renderBoxes,
  renderExpeditions,
  renderHero,
  renderInventory,
  renderNav,
  renderSettings,
  tickTimers,
  type ToastLine,
  type Ui
} from './panels'

type Tab = keyof typeof W.tabs

const TABS: { id: Tab; icon: string }[] = [
  { id: 'hero', icon: 'icon_power' },
  { id: 'inventory', icon: 'icon_armor' },
  { id: 'boxes', icon: 'icon_box_gold' },
  { id: 'expeditions', icon: 'icon_stage' },
  { id: 'settings', icon: 'icon_settings' }
]
const MAX_TOASTS = 3

const $ = (id: string): HTMLElement => document.getElementById(id) as HTMLElement
const desktop = window.desktop
let clockOffset = 0
let confirmTimer = 0

// ---------- app state + actions ----------

const app: App = {
  state: null,
  inv: null,
  odds: null,
  settings: { ...DEFAULT_SETTINGS },
  ui: { sort: 'power', slot: 'all', selected: null, confirm: null, oddsOpen: false },
  busy: false,
  now: () => Date.now() + clockOffset,

  setUi(patch: Partial<Ui>) {
    Object.assign(app.ui, patch)
    render()
  },

  openWood: () =>
    run(
      async () => ({ r: await api.openWood(), inv: await api.inventory() }),
      ({ r, inv }) => {
        applyState(r.state)
        app.inv = inv
        itemToast(r.item, r.powerBefore, r.powerAfter)
        desktop?.gameChanged('items')
      }
    ),

  openAllWood: () =>
    run(
      async () => ({ r: await api.openAllWood(), inv: await api.inventory() }),
      ({ r, inv }) => {
        applyState(r.state)
        app.inv = inv
        openAllToast(r)
        desktop?.gameChanged('items')
      }
    ),

  openGold: (id: number) =>
    run(
      async () => ({ r: await api.openGold(id), inv: await api.inventory() }),
      ({ r, inv }) => {
        applyState(r.state)
        app.inv = inv
        itemToast(r.item, r.powerBefore, r.powerAfter)
        desktop?.gameChanged('items')
      }
    ),

  equip: (id: number) => {
    const item = app.inv?.items.find((i) => i.id === id)
    const before = app.state?.hero.power ?? 0
    run(
      () => api.equip(id),
      (r) => {
        applyState(r.state)
        app.inv = r.inventory
        app.ui.selected = null
        if (item) toast([{ text: W.equippedToast(itemName(item), before, r.state.hero.power) }], item.rarity, `icon_${item.slot}`)
        desktop?.gameChanged('items')
      }
    )
  },

  /** Selling asks for a second click when it is a bulk sell or the item is epic or better. */
  sell: (ids: number[], confirm: 'bulk' | 'single') => {
    const needsConfirm = confirm === 'bulk' || (app.inv?.items.find((i) => i.id === ids[0])?.rarity ?? 0) >= 3
    if (needsConfirm && app.ui.confirm !== confirm) {
      window.clearTimeout(confirmTimer)
      confirmTimer = window.setTimeout(() => app.setUi({ confirm: null }), 4000)
      return app.setUi({ confirm })
    }
    app.ui.confirm = null
    run(
      () => api.sell(ids),
      (r) => {
        applyState(r.state)
        app.inv = r.inventory
        app.ui.selected = null
        toast([{ text: W.soldToast(r.sold.count, r.sold.gold), cls: 'tb-accent' }], undefined, 'icon_coin')
        desktop?.gameChanged('items')
      }
    )
  },

  setAutoSell: (rarities: Rarity[]) =>
    run(
      () => api.setAutoSell(rarities),
      (inv) => (app.inv = inv)
    ),

  setSettings: (patch: Partial<Settings>) => {
    if (desktop) {
      void desktop.setSettings(patch).then((s) => {
        app.settings = s
        render()
      })
    } else {
      app.settings = { ...app.settings, ...patch }
      render()
    }
  }
}

/** One server action at a time; buttons are disabled while it runs. */
async function run<R>(action: () => Promise<R>, done: (r: R) => void): Promise<void> {
  if (app.busy) return
  app.busy = true
  render()
  try {
    done(await action())
  } catch (e) {
    errorToast(e)
  } finally {
    app.busy = false
    render()
  }
}

function applyState(state: GameState): void {
  app.state = state
  clockOffset = state.serverTime - Date.now()
}

/** Pull fresh data after another window (the strip) changed something. */
async function refresh(kind: GameChangeKind): Promise<void> {
  try {
    const [state, inv] = await Promise.all([api.state(), kind === 'items' ? api.inventory() : Promise.resolve(app.inv)])
    applyState(state)
    app.inv = inv
    render()
  } catch (e) {
    errorToast(e)
  }
}

// ---------- rendering ----------

const lastInputs = new Map<string, string>()

/** Rebuild a panel only when its inputs changed, so hover, focus and open dropdowns survive background refreshes. */
function renderIf(key: string, inputs: unknown[], draw: () => void): void {
  const sig = JSON.stringify(inputs)
  if (lastInputs.get(key) === sig) return
  lastInputs.set(key, sig)
  draw()
}

function render(): void {
  const { state: s, inv, ui, busy } = app
  renderIf('nav', [s?.hero.gold, s?.hero.stage, s?.hero.cls], () => renderNav($('nav-bottom'), app))
  renderIf('hero', [s?.hero, s?.rates, s?.equipped], () => renderHero($('panel-hero'), app))
  renderIf('inventory', [inv, s?.equipped, ui.sort, ui.slot, ui.selected, ui.confirm, busy], () =>
    renderInventory($('panel-inventory'), app)
  )
  renderIf('boxes', [s?.boxes.wood, readyGoldKey(app), app.odds, busy], () => renderBoxes($('panel-boxes'), app))
  renderIf('settings', [app.settings], () => renderSettings($('panel-settings'), app))
  renderIf('expeditions', [], () => renderExpeditions($('panel-expeditions')))
}

function buildChrome(): void {
  replace($('title'), sprite('icon_weapon'), h('strong', {}, W.title))
  const close = () => (desktop ? desktop.closeMain() : window.close())
  replace(
    $('window-actions'),
    h('button', { 'aria-label': W.collapse, title: W.collapse, onclick: close }, sprite('icon_expand')),
    h('button', { 'aria-label': W.close, title: W.close, onclick: close }, sprite('icon_close'))
  )

  const tabs = TABS.map(({ id, icon }) =>
    h(
      'button',
      { class: 'tb-tab', role: 'tab', id: `tab-${id}`, 'aria-controls': `panel-${id}`, 'data-tab': id, onclick: () => activate(id) },
      sprite(icon),
      W.tabs[id]
    )
  )
  replace($('tabs'), ...tabs)

  // Keyboard: arrows / Home / End move between tabs (same as the mockup), Esc closes the window.
  $('tabs').addEventListener('keydown', (e) => {
    const i = TABS.findIndex((t) => t.id === (document.activeElement as HTMLElement | null)?.dataset.tab)
    if (i < 0) return
    let j = i
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') j = (i + 1) % TABS.length
    else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') j = (i + TABS.length - 1) % TABS.length
    else if (e.key === 'Home') j = 0
    else if (e.key === 'End') j = TABS.length - 1
    else return
    e.preventDefault()
    activate(TABS[j].id)
    tabs[j].focus()
  })
  window.addEventListener('keydown', (e) => e.key === 'Escape' && close())
}

function activate(tab: string): void {
  const id = TABS.some((t) => t.id === tab) ? tab : 'hero'
  for (const t of TABS) {
    const on = t.id === id
    const button = $(`tab-${t.id}`)
    button.setAttribute('aria-selected', String(on))
    button.tabIndex = on ? 0 : -1
    $(`panel-${t.id}`).hidden = !on
  }
}

// ---------- toasts ----------

function toast(lines: ToastLine[], rarity?: Rarity, iconKey?: string, error = false): void {
  const box = $('toasts')
  const el = h(
    'div',
    { class: `toast${rarity !== undefined ? ` ${rarityClass(rarity)}` : ''}${error ? ' is-error' : ''}`, onclick: () => el.remove() },
    iconKey && h('div', { class: `tb-item-icon${rarity !== undefined ? ` tb-rarity ${rarityClass(rarity)}` : ''}` }, sprite(iconKey)),
    h('div', {}, ...lines.flatMap((l, i) => [i > 0 && h('br'), h('span', { class: l.cls ?? '' }, l.text)]))
  )
  box.append(el)
  while (box.children.length > MAX_TOASTS) box.firstElementChild?.remove()
  window.setTimeout(() => el.remove(), rarity !== undefined && rarity >= 3 ? 7000 : 4500)
}

function itemToast(item: Item, before: number, after: number): void {
  toast(itemToastLines(item, before, after), item.rarity, `icon_${item.slot}`)
}

function openAllToast(r: OpenAllResult): void {
  const lines: ToastLine[] = [
    { text: T.openedMany(r.opened) },
    { text: rarityCounts(r.byRarity), cls: 'tb-muted' },
    { text: `${T.best}: ${itemName(r.best)}`, cls: `tb-tier ${rarityClass(r.best.rarity)}` },
    { text: T.powerChange(r.powerBefore, r.powerAfter), cls: r.powerAfter > r.powerBefore ? 'tb-up' : 'tb-muted' }
  ]
  if (r.autoSold.count > 0) lines.push({ text: T.soldMany(r.autoSold.count, r.autoSold.gold), cls: 'tb-muted' })
  toast(lines, r.best.rarity, `icon_${r.best.slot}`)
}

function errorToast(e: unknown): void {
  const code = e instanceof ApiError ? e.message : 'default'
  toast([{ text: T.errors[code] ?? T.errors.default }], undefined, undefined, true)
  if (!(e instanceof ApiError)) console.error(e)
}

// ---------- boot ----------

async function boot(): Promise<void> {
  await Promise.all([loadDesignCss(['design/tokens.css', 'design/window.css']), loadGameFont()])
  if (desktop) app.settings = await desktop.getSettings()

  buildChrome()
  activate(location.hash.slice(1))
  render()
  $('app').hidden = false

  try {
    // Sync first so gold and boxes are current; the strip then re-syncs and resets its animated counters.
    const [{ state }, inv, odds] = await Promise.all([api.sync(), api.inventory(), api.odds()])
    applyState(state)
    app.inv = inv
    app.odds = odds
    render()
    desktop?.gameChanged('state')
  } catch (e) {
    errorToast(e)
  }
  desktop?.mainReady()

  desktop?.onGameChanged((kind) => void refresh(kind))
  desktop?.onSettings((s) => {
    app.settings = s
    render()
  })
  desktop?.onTab(activate)

  window.setInterval(() => {
    tickTimers($('panel-boxes'), app.now())
    render()
  }, 1000)
}

void boot()
