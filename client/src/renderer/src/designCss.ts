/**
 * Codex's CSS is copied to public/design/ by scripts/sync-design.mjs and loaded at runtime, so its
 * url(../sprites/...) paths keep working. `base` files go before our own CSS (tokens we build on);
 * `overrides` go after it (Codex's production styling wins). Missing files are skipped.
 */
export function loadDesignCss(base: string[], overrides: string[] = []): Promise<void> {
  const first = document.head.firstChild
  const load = (href: string, before: Node | null): Promise<void> =>
    new Promise((resolve) => {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = href
      link.onload = () => resolve()
      link.onerror = () => {
        link.remove()
        resolve()
      }
      document.head.insertBefore(link, before)
    })
  return Promise.all([...base.map((href) => load(href, first)), ...overrides.map((href) => load(href, null))]).then(() => undefined)
}
