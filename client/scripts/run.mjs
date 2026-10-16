// Runs electron-vite with a clean environment.
// VS Code (and tools launched from it) set ELECTRON_RUN_AS_NODE=1, which makes Electron start as plain
// Node, so `require('electron').app` is undefined and the app crashes on launch.
import { spawn } from 'node:child_process'

delete process.env.ELECTRON_RUN_AS_NODE

const command = process.argv[2] ?? 'dev'
const child = spawn('npx', ['electron-vite', command], { stdio: 'inherit', shell: true, env: process.env })
child.on('exit', (code) => process.exit(code ?? 0))
