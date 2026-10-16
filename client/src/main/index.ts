import { app, BrowserWindow, ipcMain, Menu, nativeImage, Notification, screen, Tray, type Rectangle } from 'electron'
import { readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { DEFAULT_SETTINGS, sanitizeSettings, type Settings } from '../shared/settings'
import { POPUP_SPACE, WIDGET_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH } from '../shared/widget'

// Codex mockup: fixed 960×600 main window (design/mockups/NOTES.md).
const MAIN_WIDTH = 960
const MAIN_HEIGHT = 600
const EDGE_GAP = 12
const DRAG_TICK_MS = 16

type Page = 'index' | 'window' | 'fonttest'

let widget: BrowserWindow | null = null
let mainWin: BrowserWindow | null = null
let fontTest: BrowserWindow | null = null
let tray: Tray | null = null
let settings: Settings = { ...DEFAULT_SETTINGS }
let drag: { timer: NodeJS.Timeout; dx: number; dy: number } | null = null

const preload = (): string => join(__dirname, '../preload/index.js')

function loadPage(win: BrowserWindow, page: Page, hash = ''): void {
  const devUrl = process.env['ELECTRON_RENDERER_URL']
  if (devUrl) {
    void win.loadURL(`${devUrl}/${page}.html${hash ? `#${hash}` : ''}`)
  } else {
    void win.loadFile(join(__dirname, `../renderer/${page}.html`), { hash })
  }
}

// ---------- widget ----------

/** Keep the framed part of the widget fully inside a work area; the popup space above may stick out. */
function clampWidget(x: number, y: number): { x: number; y: number } {
  const probe: Rectangle = { x, y: y + POPUP_SPACE, width: WINDOW_WIDTH, height: WIDGET_HEIGHT }
  const { workArea } = screen.getDisplayMatching(probe)
  return {
    x: Math.round(Math.min(Math.max(x, workArea.x), workArea.x + workArea.width - WINDOW_WIDTH)),
    y: Math.round(Math.min(Math.max(y, workArea.y - POPUP_SPACE), workArea.y + workArea.height - WINDOW_HEIGHT))
  }
}

/** Saved spot if it is still on a screen, otherwise bottom-right just above the taskbar. */
function widgetPosition(): { x: number; y: number } {
  if (settings.widgetX !== null && settings.widgetY !== null) return clampWidget(settings.widgetX, settings.widgetY)
  const { workArea } = screen.getPrimaryDisplay()
  return {
    x: workArea.x + workArea.width - WINDOW_WIDTH - EDGE_GAP,
    y: workArea.y + workArea.height - WINDOW_HEIGHT
  }
}

function placeWidget(): void {
  if (!widget) return
  const { x, y } = widgetPosition()
  widget.setBounds({ x, y, width: WINDOW_WIDTH, height: WINDOW_HEIGHT })
}

function createWidget(): void {
  const { x, y } = widgetPosition()
  widget = new BrowserWindow({
    x,
    y,
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    show: false,
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    hasShadow: false,
    resizable: false,
    minimizable: false,
    maximizable: false,
    fullscreenable: false,
    skipTaskbar: true,
    alwaysOnTop: true,
    webPreferences: {
      preload: preload(),
      contextIsolation: true,
      nodeIntegration: false,
      backgroundThrottling: false
    }
  })
  widget.setAlwaysOnTop(true, 'floating')
  // Click-through by default; the renderer turns clicks on while the cursor is over the frame or a popup.
  widget.setIgnoreMouseEvents(true, { forward: true })
  loadPage(widget, 'index')
  widget.once('ready-to-show', () => widget?.showInactive())
  widget.on('closed', () => (widget = null))
}

/** Dragging by the title bar: follow the cursor from the main process so the moving window never fights its own events. */
function startDrag(): void {
  if (!widget || drag) return
  const cursor = screen.getCursorScreenPoint()
  const [wx, wy] = widget.getPosition()
  const timer = setInterval(() => {
    if (!widget || !drag) return stopDrag()
    const c = screen.getCursorScreenPoint()
    const p = clampWidget(c.x - drag.dx, c.y - drag.dy)
    widget.setPosition(p.x, p.y)
  }, DRAG_TICK_MS)
  drag = { timer, dx: cursor.x - wx, dy: cursor.y - wy }
}

function stopDrag(): void {
  if (!drag) return
  clearInterval(drag.timer)
  drag = null
  if (!widget) return
  const [x, y] = widget.getPosition()
  saveSettings({ widgetX: x, widgetY: y })
}

// ---------- main window ----------

/** The full game window (hero, bag, boxes, settings), centered on the screen the widget is on. */
function openMain(tab?: string): void {
  if (mainWin) {
    if (tab) mainWin.webContents.send('main:tab', tab)
    if (mainWin.isMinimized()) mainWin.restore()
    bringToFront(mainWin)
    return
  }
  const display = widget ? screen.getDisplayMatching(widget.getBounds()) : screen.getPrimaryDisplay()
  const { workArea } = display
  const win = new BrowserWindow({
    width: MAIN_WIDTH,
    height: MAIN_HEIGHT,
    x: Math.round(workArea.x + (workArea.width - MAIN_WIDTH) / 2),
    y: Math.round(workArea.y + Math.max(0, (workArea.height - MAIN_HEIGHT) / 2)),
    show: false,
    frame: false,
    resizable: false,
    maximizable: false,
    fullscreenable: false,
    backgroundColor: '#171C2C',
    title: 'Idle Loot',
    webPreferences: { preload: preload(), contextIsolation: true, nodeIntegration: false }
  })
  mainWin = win
  loadPage(win, 'window', tab)
  // The page says when its styles and first data are in; show anyway if that never comes.
  const fallback = setTimeout(() => !win.isDestroyed() && bringToFront(win), 4000)
  win.on('show', () => clearTimeout(fallback))
  win.on('closed', () => {
    clearTimeout(fallback)
    mainWin = null
  })
}

/**
 * Windows refuses focus to a process that did not get the last input (tray menu, toast, second launch),
 * which would leave the window behind others. moveTop() raises it anyway.
 */
function bringToFront(win: BrowserWindow): void {
  win.show()
  win.moveTop()
  win.focus()
}

function openFontTest(): void {
  if (fontTest) {
    fontTest.focus()
    return
  }
  fontTest = new BrowserWindow({ width: 1100, height: 760, title: 'ทดสอบฟอนต์ภาษาไทย', autoHideMenuBar: true })
  loadPage(fontTest, 'fonttest')
  fontTest.on('closed', () => (fontTest = null))
}

/** 16x16 gold square with a dark border, built from raw BGRA pixels so no icon file is needed yet. */
function trayIcon(): Electron.NativeImage {
  const size = 16
  const pixels = Buffer.alloc(size * size * 4)
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const edge = x === 0 || y === 0 || x === size - 1 || y === size - 1
      const i = (y * size + x) * 4
      pixels[i] = edge ? 40 : 49 // B
      pixels[i + 1] = edge ? 26 : 182 // G
      pixels[i + 2] = edge ? 20 : 242 // R
      pixels[i + 3] = 255
    }
  }
  return nativeImage.createFromBitmap(pixels, { width: size, height: size })
}

function createTray(): void {
  tray = new Tray(trayIcon())
  tray.setToolTip('Idle Loot (ต้นแบบ)')
  tray.on('click', () => openMain())
  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: 'เปิดหน้าต่างเกม', click: () => openMain() },
      {
        label: 'ย้าย widget กลับมุมขวาล่าง',
        click: () => {
          saveSettings({ widgetX: null, widgetY: null })
          placeWidget()
        }
      },
      { label: 'ทดสอบฟอนต์ภาษาไทย', click: openFontTest },
      { label: 'โหลดเกมใหม่', click: () => widget?.webContents.reload() },
      { label: 'เปิด DevTools', click: () => widget?.webContents.openDevTools({ mode: 'detach' }) },
      { type: 'separator' },
      { label: 'ออกจากเกม', click: () => app.quit() }
    ])
  )
}

// ---------- settings ----------

const settingsFile = (): string => join(app.getPath('userData'), 'settings.json')

function loadSettings(): void {
  try {
    settings = sanitizeSettings(JSON.parse(readFileSync(settingsFile(), 'utf8')))
  } catch {
    settings = { ...DEFAULT_SETTINGS }
  }
}

function saveSettings(patch: Partial<Settings>): Settings {
  settings = sanitizeSettings({ ...settings, ...patch })
  try {
    writeFileSync(settingsFile(), JSON.stringify(settings, null, 2))
  } catch (e) {
    console.error('[settings] save failed', e)
  }
  for (const w of BrowserWindow.getAllWindows()) w.webContents.send('settings:changed', settings)
  return settings
}

// ---------- IPC ----------

function registerIpc(): void {
  ipcMain.on('widget:interactive', (_event, on: boolean) => {
    widget?.setIgnoreMouseEvents(!on, { forward: true })
  })
  ipcMain.on('widget:drag-start', startDrag)
  ipcMain.on('widget:drag-end', stopDrag)

  ipcMain.on('main:open', (_event, tab?: string) => openMain(tab))
  ipcMain.on('main:close', () => mainWin?.close())
  ipcMain.on('main:ready', (event) => {
    const win = BrowserWindow.fromWebContents(event.sender)
    if (win) bringToFront(win)
  })

  // One window changed game data on the server; tell the others to refresh.
  ipcMain.on('game:changed', (event, kind: string) => {
    for (const w of BrowserWindow.getAllWindows()) {
      if (w.webContents !== event.sender) w.webContents.send('game:changed', kind)
    }
  })

  ipcMain.handle('settings:get', () => settings)
  ipcMain.handle('settings:set', (_event, patch: Partial<Settings>) => saveSettings(patch))

  ipcMain.on('notify', (_event, title: string, body: string, tab?: string) => {
    if (!Notification.isSupported()) return
    const n = new Notification({ title, body })
    n.on('click', () => openMain(tab))
    n.on('failed', (_e, error) => console.error('[notify] failed', error))
    n.show()
  })
}

if (!app.requestSingleInstanceLock()) {
  app.quit()
} else {
  // Windows toasts need an app id; in dev it must be the exe path.
  app.setAppUserModelId(app.isPackaged ? 'com.idleloot.prototype' : process.execPath)

  app.whenReady().then(() => {
    loadSettings()
    registerIpc()
    createWidget()
    createTray()
    // Screens added/removed or rescaled: pull the widget back onto a screen if it fell off.
    screen.on('display-metrics-changed', placeWidget)
    screen.on('display-added', placeWidget)
    screen.on('display-removed', placeWidget)
  })

  app.on('second-instance', () => openMain())

  // The game keeps running from the tray; quitting is explicit.
  app.on('window-all-closed', () => {})
}
