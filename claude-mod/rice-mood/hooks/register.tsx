import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { RiceLook, RiceTurn } from '../types'

// Claude Code в стиле активной темы райса (~/.local/share/rice/current):
// шапка над вводом, статус, звуки темы, характер в ответах и /rice для смены темы.

const look = atom({ plugin: 'rice-mood', key: 'look' } as const, null)
const turn = atom({ plugin: 'rice-mood', key: 'turn' } as const, null)
const quote = atom({ plugin: 'rice-mood', key: 'quote' } as const, 0)

let home = ''

function riceDir() {
  return `${home}/.local/share/rice`
}

async function loadLook($: any): Promise<RiceLook | null> {
  try {
    if (!home) home = (await $.process.run(['printenv', 'HOME'])).stdout.trim()
    const theme = JSON.parse(await $.fs.read(`${riceDir()}/current/theme.json`))
    const extra = JSON.parse(await $.fs.read(`${riceDir()}/current/claude.json`))
    const next: RiceLook = { id: theme.id, name: theme.name, sounds: theme.sounds, ...extra }
    await update($, look, () => next)
    return next
  } catch {
    return null
  }
}

// $.audio молчит в Linux-терминале — играем сами через PipeWire
async function sound($: any, ev: string) {
  const l = await read($, look)
  if (!l) return
  const f = `${home}/.local/share/sounds/${l.sounds}/stereo/${ev}.oga`
  if (await $.fs.exists(f)) void $.process.run(['pw-play', '--volume', '0.6', f], { timeoutMs: 8000 }).catch(() => {})
}

export const register: Register = on => {
  let startedAt = 0
  let tools = 0

  on('session.start', async ($, e, next) => {
    const started = await next(e)
    const l = await loadLook($)
    await $.command.register({ name: 'rice', description: 'Тема райса: /rice — список, /rice <id> — сменить тему' })
    if (l && e.isInteractive) {
      $.ui.toast(`${l.mascot ? l.mascot + ' ' : ''}${l.greet}`)
      void sound($, 'desktop-login')
    }
    return started
  })

  on('prompt.compose', async ($, e, next) => {
    const out = await next(e)
    const l = await read($, look)
    if (!l?.persona) return out
    return {
      sections: [...out.sections, { id: 'rice-mood:persona', text: `# Persona (${l.name})\n${l.persona}`, scope: 'session' as const }],
    }
  })

  on('prompt.submit', async ($, e, next) => {
    startedAt = await $.clock.now()
    tools = 0
    const l = await read($, look)
    if (l) $.ui.status(l.thinking)
    return next(e)
  }).catch(($, e, next) => next(e))

  on('tool.call', async ($, e, next) => {
    tools += 1
    const l = await read($, look)
    if (l) $.ui.status(l.tool.replace('{tool}', e.tool))
    return next(e)
  }).catch(($, e, next) => next(e))

  on('turn.complete', async ($, e, next) => {
    const l = await read($, look)
    const ok = e.reason === 'answer'
    const t: RiceTurn = { seconds: Math.round(((await $.clock.now()) - startedAt) / 1000), tools, ok }
    await update($, turn, () => t)
    await update($, quote, q => q + 1)
    if (l) {
      $.ui.status(ok ? l.done : l.error)
      if (e.reason !== 'aborted') void sound($, ok ? 'complete' : 'dialog-error')
    }
    return next(e)
  })

  on('command.run', { command: 'rice' }, async ($, e) => {
    if (!home) await loadLook($)
    const rice = `${riceDir()}/rice.py`
    const id = e.args.trim()
    if (!id) {
      const r = await $.process.run(['python3', rice, 'list'])
      return { text: `Темы райса (* — активная):\n${r.stdout}\nСменить: /rice <id> (рабочий стол; загрузку меняет «Темы райса» в Параметрах)` }
    }
    if (!/^[a-z0-9_-]+$/.test(id)) return { text: 'Некорректный id темы.' }
    const r = await $.process.run(['python3', rice, 'apply', id], { timeoutMs: 300000 })
    const l = await loadLook($)
    if (l) $.ui.toast(`${l.mascot ? l.mascot + ' ' : ''}${l.greet}`)
    void sound($, 'desktop-login')
    return { text: r.exitCode === 0 ? `Тема → ${l?.name ?? id}. Профиль Konsole подхватят новые окна (rclaude).` : `Ошибка:\n${r.stdout}${r.stderr}` }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const l = await read($, look)
    if (!l || e.props.hasSurvey) return next(e)
    const t = await read($, turn)
    const q = l.quotes.length ? l.quotes[(await read($, quote)) % l.quotes.length] : ''
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="row">
        <Text color={l.accent} bold>
          {l.title}{' '}
        </Text>
        <Text color={l.dim}>// </Text>
        <Text color={l.accent2}>{l.sub}</Text>
        {t && (
          <Text color={l.dim}>
            {'  ·  '}
            {t.ok ? l.done : l.error} {t.seconds}s, {t.tools} tools
          </Text>
        )}
        {q && <Text color={l.dim} italic>{'  ·  '}{q}</Text>}
      </Box>
    )
  })
}
