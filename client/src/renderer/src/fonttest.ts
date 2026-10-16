// Font test page: shows every candidate Thai font the way the game will draw it.

const SAMPLE = 'น้ำ ปี่ ฟ้า ฝั่ง ญู ฐุ ฎู ผู้ใหญ่ ปั้น ซ้ำ'
const SAMPLE_UI = 'ด่าน 12  พลัง 1,540  กล่องไม้ ×12  ตำนาน  Sword +312'
const SIZES = [8, 10, 11, 12, 13, 14, 16, 20, 24, 32]
const CANVAS_SIZES = [11, 12, 13, 16]
const FILES = ['GameFont.ttf', 'Silver.ttf', 'ThaiThai-Regular.ttf', 'ThaiThai.ttf', 'ThaiThai-Regular.otf']
const SYSTEM_FONTS = ['Leelawadee UI', 'Tahoma']

const results = document.getElementById('results') as HTMLDivElement
const drop = document.getElementById('drop') as HTMLDivElement
let dropped = 0

function section(title: string, family: string | null, note = '', first = false): void {
  const el = document.createElement('section')
  const h2 = document.createElement('h2')
  h2.textContent = family ? title : `${title} — ${note}`
  el.appendChild(h2)
  if (first) results.prepend(el)
  else results.appendChild(el)
  if (!family) {
    el.className = 'missing'
    return
  }

  for (const size of SIZES) {
    const row = document.createElement('div')
    row.className = 'row'
    const label = document.createElement('span')
    label.className = 'size'
    label.textContent = `${size}px`
    const text = document.createElement('span')
    text.style.font = `${size}px "${family}"`
    text.textContent = `${SAMPLE}   ${SAMPLE_UI}`
    row.append(label, text)
    el.appendChild(row)
  }

  // The game draws text on a canvas, then the strip is shown 1:1 — this is the honest preview, zoomed 3x.
  const caption = document.createElement('div')
  caption.className = 'canvas-label'
  caption.textContent = 'แบบที่เกมวาดจริง (canvas, ขยาย 3 เท่า)'
  el.appendChild(caption)
  for (const size of CANVAS_SIZES) el.appendChild(canvasPreview(family, size))
}

function canvasPreview(family: string, size: number): HTMLCanvasElement {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d') as CanvasRenderingContext2D
  const font = `${size}px "${family}"`
  ctx.font = font
  const text = `${size}px  ${SAMPLE}`
  canvas.width = Math.ceil(ctx.measureText(text).width) + 12
  canvas.height = Math.ceil(size * 2.2)
  ctx.fillStyle = '#0c0e18'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.font = font
  ctx.textBaseline = 'middle'
  ctx.lineWidth = 3
  ctx.strokeStyle = '#0b0d17'
  ctx.strokeText(text, 6, canvas.height / 2)
  ctx.fillStyle = '#ffffff'
  ctx.fillText(text, 6, canvas.height / 2)
  canvas.style.width = `${canvas.width * 3}px`
  canvas.style.height = `${canvas.height * 3}px`
  return canvas
}

async function loadFile(name: string): Promise<void> {
  const family = `Test-${name}`
  try {
    const face = new FontFace(family, `url(fonts/${name})`)
    await face.load()
    document.fonts.add(face)
    section(name, family)
  } catch {
    section(name, null, 'ไม่พบไฟล์')
  }
}

async function main(): Promise<void> {
  for (const name of FILES) await loadFile(name)
  for (const name of SYSTEM_FONTS) section(`${name} (ฟอนต์ของ Windows สำหรับเทียบ)`, name)
}

drop.addEventListener('dragover', (e) => {
  e.preventDefault()
  drop.classList.add('over')
})
drop.addEventListener('dragleave', () => drop.classList.remove('over'))
window.addEventListener('dragover', (e) => e.preventDefault())
window.addEventListener('drop', async (e) => {
  e.preventDefault()
  drop.classList.remove('over')
  for (const file of Array.from(e.dataTransfer?.files ?? [])) {
    const family = `Dropped-${++dropped}`
    try {
      const face = new FontFace(family, await file.arrayBuffer())
      await face.load()
      document.fonts.add(face)
      section(`${file.name} (ลากมาวาง)`, family, '', true)
    } catch {
      section(file.name, null, 'อ่านไฟล์ฟอนต์ไม่ได้', true)
    }
  }
})

void main()
