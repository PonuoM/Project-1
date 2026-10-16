import type { Item, Rarity, Slot } from './types'

// Thai only for the prototype; English goes in a second table with the same keys.

export const RARITY_NAMES: Record<Rarity, string> = {
  0: 'ธรรมดา',
  1: 'ดี',
  2: 'หายาก',
  3: 'มหากาพย์',
  4: 'ตำนาน'
}

/** Roman tier marks next to rarity colors, so rarity never depends on color alone. */
export const TIERS: Record<Rarity, string> = { 0: 'I', 1: 'II', 2: 'III', 3: 'IV', 4: 'V' }

const SLOT_NAMES: Record<Slot, string> = {
  weapon: 'อาวุธ',
  armor: 'เกราะ',
  ring: 'เครื่องประดับ'
}

const ITEM_NAMES: Record<string, string> = {
  sword: 'ดาบ',
  axe: 'ขวาน',
  spear: 'หอก',
  leather: 'เกราะหนัง',
  chain: 'เกราะโซ่',
  plate: 'เกราะเหล็ก',
  ring: 'แหวน',
  amulet: 'สร้อยคอ',
  charm: 'เครื่องราง'
}

export const CLASS_NAMES: Record<string, string> = {
  melee: 'นักรบ',
  mage: 'นักเวท',
  ranged: 'นักธนู'
}

/** Visual skill per class (the button and the big strike). Real skill mechanics are not decided yet. */
export const SKILL_NAMES: Record<string, string> = {
  melee: 'สะบั้นแผ่นดิน',
  mage: 'ลูกไฟระเบิด',
  ranged: 'ศรทะลวง'
}

export const T = {
  regionDefault: 'ป่ามืด',
  stageLine: (stage: number, kills: number, perStage: number) => `ด่าน ${stage} · ${kills}/${perStage}`,
  heroLine: (cls: string, power: number) => `${cls} · พลัง ${fmt(power)}`,
  phases: { idle: 'กำลังโหลด…', walk: 'กำลังเดินทาง', fight: 'ต่อสู้', impact: 'ปะทะ!' } as Record<string, string>,
  openWoodHint: 'คลิกเพื่อเปิดกล่องไม้ 1 ใบ',
  goldBoxHint: 'กล่องทอง: รอปลดล็อกแล้วคลิกเพื่อเปิด',
  noGoldBox: 'ยังไม่มีกล่องทอง',
  skillHint: 'ใช้สกิลกับมอนตัวถัดไป',
  expand: 'เปิดหน้าต่างเกม',
  dragHint: 'ลากเพื่อย้าย',
  stage: (stage: number) => `ด่าน ${stage}`,
  stageProgress: (kills: number, perStage: number) => `${kills}/${perStage}`,
  power: (power: number) => `พลัง ${fmt(power)}`,
  goldLabel: 'ทอง',
  stuck: 'ติดด่าน! เปิดกล่องเพื่อเพิ่มพลัง',
  openAll: 'เปิดทั้งหมด',
  ready: 'เปิดได้!',
  equipped: (gain: number) => `สวมใส่แล้ว ▲ +${fmt(gain)} พลัง`,
  stored: 'เก็บเข้ากระเป๋า (ของเดิมดีกว่า)',
  soldOne: (gold: number) => `ขายอัตโนมัติ +${fmt(gold)} ทอง`,
  soldMany: (n: number, gold: number) => `ขายอัตโนมัติ ${fmt(n)} ชิ้น +${fmt(gold)} ทอง`,
  goldReadyTitle: 'กล่องทองพร้อมเปิดแล้ว',
  goldReadyBody: 'คลิกที่กล่องบนแถบ หรือคลิกตรงนี้เพื่อเปิดหน้ากล่อง',
  openedMany: (n: number) => `เปิดกล่องไม้ ${fmt(n)} ใบ`,
  powerChange: (a: number, b: number) => `พลัง ${fmt(a)} → ${fmt(b)}`,
  best: 'ชิ้นที่ดีที่สุด',
  awayTitle: (ms: number) => `ระหว่างที่คุณไม่อยู่ ${duration(ms)}`,
  awayGold: (gold: number) => `+${fmt(gold)} ทอง`,
  awayBoxes: (wood: number, gold: number) => `กล่องไม้ ×${fmt(wood)}   กล่องทอง ×${fmt(gold)}`,
  awayStage: (from: number, to: number) => (from === to ? `อยู่ด่าน ${to}` : `ผ่านด่าน ${from} → ${to}`),
  awayCapped: 'เก็บได้สูงสุด 8 ชม. กลับมาบ่อยขึ้นจะได้ไม่เสียรางวัล',
  tapToClose: 'คลิกเพื่อปิด',
  errors: {
    network: 'เชื่อมต่อเซิร์ฟเวอร์ไม่ได้ กำลังลองใหม่…',
    not_ready: 'กล่องทองยังปลดล็อกไม่เสร็จ',
    no_box: 'ไม่มีกล่องให้เปิด',
    no_item: 'ไม่พบไอเทมนี้ในกระเป๋าแล้ว',
    default: 'เกิดข้อผิดพลาด'
  } as Record<string, string>
}

// Main window (hero / bag / boxes / expeditions / settings). Layout and copy follow design/mockups/window.html.
export const W = {
  title: 'Idle Loot · ต้นแบบ',
  collapse: 'ย่อกลับไปที่แถบ',
  close: 'ปิด',
  tabs: { hero: 'ฮีโร่', inventory: 'กระเป๋า', boxes: 'กล่อง', expeditions: 'สำรวจ', settings: 'ตั้งค่า' },
  navStage: (stage: number, cls: string) => `ด่าน ${stage} · ${cls}`,
  loading: 'กำลังโหลด…',

  heroSub: 'อุปกรณ์ที่สวมอยู่และความเร็วในการล่า',
  heroStage: (stage: number, kills: number) => `ด่าน ${stage} · ล่าไปแล้ว ${fmt(kills)} ตัว`,
  heroPace: (killMs: number, gold: number) => `ล่า 1 ตัวทุก ${(killMs / 1000).toFixed(1)} วิ · ได้ ${fmt(gold)} ทองต่อตัว`,
  heroStuck: 'ติดด่าน! เปิดกล่องหรือเปลี่ยนอุปกรณ์เพื่อเพิ่มพลัง',
  equipment: 'อุปกรณ์ที่สวมใส่',
  emptySlot: 'ว่าง · เปิดกล่องเพื่อหาของ',
  powerPlus: (n: number) => `พลัง +${fmt(n)}`,
  skills: 'ช่องสกิล',
  skillSlot: (n: number) => `ช่องสกิล ${n}`,
  skillSoon: 'เร็ว ๆ นี้ · ได้หินสกิลจากกล่อง',
  heroFoot: 'เปิดกล่องแล้วได้ของที่พลังสูงกว่า ระบบสวมให้อัตโนมัติ · เปลี่ยนเองได้ที่กระเป๋า',

  bagSub: (n: number, cap: number) => `${fmt(n)} / ${fmt(cap)} ช่อง · ชี้ที่ไอเทมเพื่อเทียบกับของที่สวมอยู่`,
  sortBy: 'เรียงตาม',
  sorts: { power: 'พลัง', rarity: 'ความหายาก', newest: 'ใหม่สุด' },
  slotFilter: 'ช่องอุปกรณ์',
  allSlots: 'ทั้งหมด',
  autoSell: 'ขายอัตโนมัติ',
  autoSellHint: 'ของที่ดรอปมาแล้วไม่ได้สวม จะขายทันที',
  sellMatching: (n: number, gold: number) => `ขายในกระเป๋าตามนี้ ${fmt(n)} ชิ้น (+${fmt(gold)} ทอง)`,
  confirmSell: (n: number) => `ยืนยันขาย ${fmt(n)} ชิ้น?`,
  bagEmpty: 'กระเป๋าว่าง · ของที่ไม่ได้สวมจะมาอยู่ที่นี่',
  bagFull: 'กระเป๋าเต็ม ของใหม่ที่ไม่ได้สวมจะถูกขายอัตโนมัติ',
  bagFoot: 'คลิกไอเทมเพื่อสวมใส่หรือขาย · ขอบสีและเลข I–V บอกความหายาก',
  compareUp: (n: number) => `▲ +${fmt(n)} เทียบกับที่สวม`,
  compareDown: (n: number) => `▼ −${fmt(n)} เทียบกับที่สวม`,
  compareSame: 'เท่ากับที่สวมอยู่',
  compareEmpty: 'ช่องนี้ยังว่าง',
  equip: 'สวมใส่',
  sellFor: (gold: number) => `ขาย +${fmt(gold)} ทอง`,
  equippedToast: (name: string, before: number, after: number) => `สวม${name}แล้ว · พลัง ${fmt(before)} → ${fmt(after)}`,
  soldToast: (n: number, gold: number) => `ขาย ${fmt(n)} ชิ้น +${fmt(gold)} ทอง`,

  boxesSub: 'เปิดกล่องไม้ได้ทันที · กล่องทองต้องรอปลดล็อก',
  woodCount: (n: number) => `กล่องไม้ ×${fmt(n)}`,
  woodHint: 'เปิดได้ทันที',
  openOne: 'เปิด 1 ใบ',
  openAll: (limit: number) => `เปิดทั้งหมด (สูงสุด ${limit})`,
  goldBoxes: 'กล่องทอง',
  goldBox: 'กล่องทอง',
  goldReady: 'พร้อมเปิด',
  goldLocked: 'กำลังปลดล็อก',
  goldReadyTimer: 'เปิดได้แล้ว',
  openBox: 'เปิดกล่อง',
  waitUnlock: 'รอปลดล็อก',
  goldEmpty: 'ยังไม่มีกล่องทอง · ดรอปจากมอนสเตอร์ระหว่างล่า',
  odds: 'อัตราการดรอป',
  oddsRarity: 'ความหายาก',
  oddsPerKill: (wood: number, gold: number) => `โอกาสดรอปต่อมอนสเตอร์ 1 ตัว: กล่องไม้ ${wood}% · กล่องทอง ${gold}%`,
  oddsUnlock: (ms: number) => `กล่องทองปลดล็อกใน ${duration(ms)} · อัตรานี้มาจากเซิร์ฟเวอร์โดยตรง`,

  expeditionsSub: 'ส่งผู้ช่วยไปหาของระหว่างที่คุณทำงาน',
  expeditionsSoon: 'ระบบสำรวจกำลังสร้าง',
  expeditionsSoonHint: 'จะมาพร้อมผู้ช่วย (Minion) ในอัปเดตถัดไป',

  settingsSub: 'ปรับให้เกมอยู่ร่วมกับพื้นที่ทำงานของคุณ',
  fps: 'FPS ของ widget',
  fpsHint: '60 = ท่าโจมตีลื่นและหนักแน่น · 30 = ประหยัดเครื่อง',
  notifications: 'แจ้งเตือนของ Windows',
  notifyGoldReady: 'กล่องทองพร้อมเปิด',
  fullscreen: 'เมื่อแอปอื่นเต็มหน้าจอ',
  fullscreenHide: 'ซ่อนอัตโนมัติ',
  fullscreenKeep: 'อยู่บนสุดเสมอ',
  language: 'ภาษา / Language',
  soon: '(เร็ว ๆ นี้)',
  settingsFoot: 'การตั้งค่าในหน้านี้บันทึกไว้ในเครื่องนี้ ส่วนขายอัตโนมัติบันทึกที่บัญชี'
}

export function tierLabel(rarity: Rarity): string {
  return `${TIERS[rarity]} ${RARITY_NAMES[rarity]}`
}

export function itemName(item: Item): string {
  return ITEM_NAMES[item.nameKey] ?? item.nameKey
}

export function itemSubtitle(item: Item): string {
  return `${RARITY_NAMES[item.rarity]} · ${SLOT_NAMES[item.slot]} · พลัง ${fmt(item.power)}`
}

export function slotName(slot: Slot): string {
  return SLOT_NAMES[slot]
}

export function fmt(n: number): string {
  return Math.floor(n).toLocaleString('en-US')
}

export function duration(ms: number): string {
  const totalMin = Math.floor(ms / 60000)
  const h = Math.floor(totalMin / 60)
  const m = totalMin % 60
  return h > 0 ? `${h} ชม. ${m} นาที` : `${m} นาที`
}

export function countdown(ms: number): string {
  const s = Math.max(0, Math.ceil(ms / 1000))
  const mm = Math.floor(s / 60)
  const ss = s % 60
  return `${mm}:${ss.toString().padStart(2, '0')}`
}
