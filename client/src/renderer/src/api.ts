import type { GameState, Inventory, InventoryResult, Odds, OpenAllResult, OpenResult, Rarity, SellResult, SyncResult } from './types'

const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost/Projects-1/server/public/api.php'

export class ApiError extends Error {
  constructor(
    public status: number,
    code: string
  ) {
    super(code)
  }
}

let token: string | null = localStorage.getItem('token')

function deviceId(): string {
  let id = localStorage.getItem('deviceId')
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem('deviceId', id)
  }
  return id
}

async function request<T>(action: string, body: object = {}): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${BASE}?a=${action}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(token ? { 'X-Auth-Token': token } : {}) },
      body: JSON.stringify(body)
    })
  } catch {
    throw new ApiError(0, 'network')
  }
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new ApiError(res.status, data.error ?? 'bad_response')
  return data as T
}

let loggingIn: Promise<void> | null = null

/** Parallel calls share one login, so a fresh device never races itself into two guest accounts. */
function login(): Promise<void> {
  loggingIn ??= request<{ token: string }>('auth.guest', { deviceId: deviceId() })
    .then((r) => {
      token = r.token
      localStorage.setItem('token', r.token)
    })
    .finally(() => (loggingIn = null))
  return loggingIn
}

/** Logs in on first use and once more if the server forgot our token (e.g. local DB reset). */
async function call<T>(action: string, body?: object): Promise<T> {
  if (!token) await login()
  try {
    return await request<T>(action, body)
  } catch (e) {
    if (e instanceof ApiError && e.status === 401) {
      token = null
      localStorage.removeItem('token')
      await login()
      return request<T>(action, body)
    }
    throw e
  }
}

export const api = {
  state: () => call<GameState>('state'),
  sync: () => call<SyncResult>('sync'),
  openWood: () => call<OpenResult>('box.open', { type: 'wood' }),
  openGold: (id: number) => call<OpenResult>('box.open', { type: 'gold', id }),
  openAllWood: () => call<OpenAllResult>('box.openAll'),
  odds: () => call<Odds>('box.odds'),
  inventory: () => call<Inventory>('inventory'),
  equip: (id: number) => call<InventoryResult>('item.equip', { id }),
  sell: (ids: number[]) => call<SellResult>('item.sell', { ids }),
  setAutoSell: (rarities: Rarity[]) => call<Inventory>('settings.autoSell', { rarities })
}
