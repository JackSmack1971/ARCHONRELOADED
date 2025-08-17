import pino from 'pino'
import { secureFetch } from '../utils/http'

export const logger = pino()

export class EngineError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'EngineError'
  }
}

export async function runEngineTask(taskId: string): Promise<string> {
  if (!/^[0-9a-fA-F-]{36}$/.test(taskId)) {
    logger.error({ taskId }, 'invalid taskId')
    throw new EngineError('Invalid taskId')
  }
  const url = process.env.ENGINE_URL
  if (!url) {
    logger.error('missing ENGINE_URL')
    throw new EngineError('Missing ENGINE_URL')
  }
  logger.info({ taskId }, 'runEngineTask start')
  try {
    const res = await secureFetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId }),
    })
    logger.info({ taskId }, 'runEngineTask success')
    return await res.text()
  } catch (err) {
    logger.error({ taskId, err: err instanceof Error ? err.message : err }, 'runEngineTask failure')
    throw new EngineError(err instanceof Error ? err.message : 'Unknown error')
  }
}
