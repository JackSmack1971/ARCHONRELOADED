import { secureFetch } from '../utils/http'

export class EngineError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'EngineError'
  }
}

export async function runEngineTask(taskId: string): Promise<string> {
  if (!/^[0-9a-fA-F-]{36}$/.test(taskId)) throw new EngineError('Invalid taskId')
  const url = process.env.ENGINE_URL
  if (!url) throw new EngineError('Missing ENGINE_URL')
  try {
    const res = await secureFetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId }),
    })
    return await res.text()
  } catch (err) {
    throw new EngineError(err instanceof Error ? err.message : 'Unknown error')
  }
}
