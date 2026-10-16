import { resolve } from 'node:path'
import { defineConfig } from 'electron-vite'

export default defineConfig({
  main: {},
  preload: {},
  renderer: {
    build: {
      rollupOptions: {
        input: {
          index: resolve('src/renderer/index.html'),
          window: resolve('src/renderer/window.html'),
          fonttest: resolve('src/renderer/fonttest.html')
        }
      }
    }
  }
})
