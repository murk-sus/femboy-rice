export type RiceLook = {
  id: string
  name: string
  title: string
  sub: string
  mascot: string
  accent: string
  accent2: string
  dim: string
  thinking: string
  tool: string
  done: string
  error: string
  greet: string
  quotes: string[]
  persona: string
  sounds: string
}

export type RiceTurn = { seconds: number; tools: number; ok: boolean }

declare module 'claude-code' {
  interface PluginState {
    'rice-mood': { look: RiceLook | null; turn: RiceTurn | null; quote: number }
  }
}
