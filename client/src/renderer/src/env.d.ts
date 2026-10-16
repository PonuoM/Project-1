type GameChangeKind = 'state' | 'items'
type DesktopSettings = import('../../shared/settings').Settings

interface Window {
  /** Exposed by the Electron preload; undefined when the page runs in a normal browser. */
  desktop?: {
    setInteractive(on: boolean): void
    dragStart(): void
    dragEnd(): void
    openMain(tab?: string): void
    closeMain(): void
    mainReady(): void
    onTab(cb: (tab: string) => void): void
    gameChanged(kind: GameChangeKind): void
    onGameChanged(cb: (kind: GameChangeKind) => void): void
    getSettings(): Promise<DesktopSettings>
    setSettings(patch: Partial<DesktopSettings>): Promise<DesktopSettings>
    onSettings(cb: (s: DesktopSettings) => void): void
    notify(title: string, body: string, tab?: string): void
  }
}

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
}
