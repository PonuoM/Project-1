import { contextBridge, ipcRenderer } from 'electron'
import type { Settings } from '../shared/settings'

type ChangeKind = 'state' | 'items'

contextBridge.exposeInMainWorld('desktop', {
  /** Widget: true = this window takes mouse clicks; false = clicks pass through to the desktop. */
  setInteractive: (on: boolean) => ipcRenderer.send('widget:interactive', on),
  /** Widget title bar: the main process moves the window with the cursor until dragEnd. */
  dragStart: () => ipcRenderer.send('widget:drag-start'),
  dragEnd: () => ipcRenderer.send('widget:drag-end'),

  openMain: (tab?: string) => ipcRenderer.send('main:open', tab),
  closeMain: () => ipcRenderer.send('main:close'),
  /** Main window: styles and first data are rendered, show the window now. */
  mainReady: () => ipcRenderer.send('main:ready'),
  onTab: (cb: (tab: string) => void) => ipcRenderer.on('main:tab', (_e, tab: string) => cb(tab)),

  /** 'items' when gear or bag changed, 'state' for everything else (gold, stage, boxes). */
  gameChanged: (kind: ChangeKind) => ipcRenderer.send('game:changed', kind),
  onGameChanged: (cb: (kind: ChangeKind) => void) => ipcRenderer.on('game:changed', (_e, kind: ChangeKind) => cb(kind)),

  getSettings: (): Promise<Settings> => ipcRenderer.invoke('settings:get'),
  setSettings: (patch: Partial<Settings>): Promise<Settings> => ipcRenderer.invoke('settings:set', patch),
  onSettings: (cb: (s: Settings) => void) => ipcRenderer.on('settings:changed', (_e, s: Settings) => cb(s)),

  /** Windows toast; clicking it opens the main window on `tab`. */
  notify: (title: string, body: string, tab?: string) => ipcRenderer.send('notify', title, body, tab)
})
