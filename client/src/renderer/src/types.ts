// Mirrors the JSON returned by server/public/api.php.

export type Slot = 'weapon' | 'armor' | 'ring'
export type Rarity = 0 | 1 | 2 | 3 | 4

export interface Item {
  id: number
  slot: Slot
  rarity: Rarity
  power: number
  nameKey: string
  equipped?: boolean
  replacedPower?: number
  /** Gold it was auto-sold for when it dropped; 0 = kept. */
  soldFor?: number
}

export interface BagItem extends Item {
  sellValue: number
  createdAt: number
}

export interface Inventory {
  items: BagItem[]
  capacity: number
  /** Rarities sold automatically on drop. */
  autoSell: Rarity[]
  /** Highest rarity that may be auto-sold. */
  autoSellMax: Rarity
}

export interface Odds {
  /** Percent per rarity, common → legendary. */
  boxes: { wood: number[]; gold: number[] }
  /** Percent chance per kill. */
  perKill: { wood: number; gold: number }
  goldUnlockMs: number
}

export interface Sold {
  count: number
  gold: number
}

export interface GoldBox {
  id: number
  unlockAt: number
  ready: boolean
}

export interface GameState {
  serverTime: number
  hero: {
    cls: string
    stage: number
    stageKills: number
    killsPerStage: number
    gold: number
    totalKills: number
    power: number
  }
  rates: { killMs: number; goldPerKill: number; canAdvance: boolean }
  equipped: Record<Slot, Item | null>
  boxes: { wood: number; gold: GoldBox[] }
  limits: { offlineCapMs: number }
}

export interface SyncDelta {
  elapsedMs: number
  creditedMs: number
  capped: boolean
  kills: number
  gold: number
  wood: number
  goldBoxes: number
  stageFrom: number
  stageTo: number
}

export interface SyncResult {
  delta: SyncDelta
  state: GameState
}

export interface OpenResult {
  item: Item
  powerBefore: number
  powerAfter: number
  autoSold: Sold
  state: GameState
}

export interface OpenAllResult {
  opened: number
  byRarity: number[]
  best: Item
  powerBefore: number
  powerAfter: number
  autoSold: Sold
  state: GameState
}

export interface InventoryResult {
  state: GameState
  inventory: Inventory
}

export interface SellResult extends InventoryResult {
  sold: Sold
}
