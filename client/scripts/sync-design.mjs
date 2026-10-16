// Copies Codex's design output (../design) into the game. design/ stays the single source of truth;
// the copies are git-ignored and refreshed before every dev run and build.
import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const client = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const design = resolve(client, '../design')
const spritesOut = resolve(client, 'src/renderer/public/sprites')
const dataOut = resolve(client, 'src/renderer/src/design')
// Main-window CSS stays a runtime file next to the sprites so its url(../sprites/...) paths keep working.
const cssOut = resolve(client, 'src/renderer/public/design')

for (const required of ['tokens.json', 'sprites/manifest.json', 'mockups/tokens.css', 'mockups/window.css']) {
  if (!existsSync(resolve(design, required))) {
    console.error(`[sync-design] missing design/${required}`)
    process.exit(1)
  }
}

rmSync(spritesOut, { recursive: true, force: true })
mkdirSync(spritesOut, { recursive: true })
cpSync(resolve(design, 'sprites'), spritesOut, { recursive: true, filter: (src) => !src.endsWith('.html') })

mkdirSync(dataOut, { recursive: true })
cpSync(resolve(design, 'tokens.json'), resolve(dataOut, 'tokens.json'))
cpSync(resolve(design, 'sprites/manifest.json'), resolve(dataOut, 'manifest.json'))

rmSync(cssOut, { recursive: true, force: true })
mkdirSync(cssOut, { recursive: true })
cpSync(resolve(design, 'mockups/tokens.css'), resolve(cssOut, 'tokens.css'))
cpSync(resolve(design, 'mockups/window.css'), resolve(cssOut, 'window.css'))

// Optional until Codex delivers them (Prompt 7): production widget frame and parallax background layers.
const optional = []
if (existsSync(resolve(design, 'mockups/widget.css'))) {
  cpSync(resolve(design, 'mockups/widget.css'), resolve(cssOut, 'widget.css'))
  optional.push('widget.css')
}
const backgroundsOut = resolve(client, 'src/renderer/public/backgrounds')
rmSync(backgroundsOut, { recursive: true, force: true })
if (existsSync(resolve(design, 'backgrounds/backgrounds.json'))) {
  cpSync(resolve(design, 'backgrounds'), backgroundsOut, { recursive: true, filter: (src) => !src.endsWith('.html') })
  optional.push('backgrounds')
}

console.log(`[sync-design] sprites, tokens and window CSS copied from design/${optional.length ? ` (+ ${optional.join(', ')})` : ''}`)
