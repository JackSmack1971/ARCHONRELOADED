import pino from 'pino'

export const logger = pino()

export class HTTPError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'HTTPError'
  }
}

const BASE_DELAY = 100
const wait = (ms: number) => new Promise((r) => setTimeout(r, ms))

async function fetchOnce(url: string, options: RequestInit, timeout: number): Promise<Response> {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeout)
  try {
    return await fetch(url, { ...options, signal: controller.signal })
  } finally {
    clearTimeout(id)
  }
}

export async function secureFetch(
  url: string,
  options: RequestInit = {},
  retries = 2,
  timeout = 5000,
): Promise<Response> {
  try {
    new URL(url)
  } catch {
    logger.error({ url }, 'invalid url')
    throw new HTTPError(0, 'Invalid URL')
  }
  for (let attempt = 0; ; attempt++) {
    logger.info({ url, attempt }, 'request start')
    try {
      const res = await fetchOnce(url, options, timeout)
      if (!res.ok) throw new HTTPError(res.status, res.statusText)
      logger.info({ url, status: res.status, attempt }, 'request success')
      return res
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Unknown error'
      if (attempt >= retries) {
        logger.error({ url, message: msg, attempt }, 'request failure')
        throw err instanceof HTTPError ? err : new HTTPError(0, msg)
      }
      logger.warn({ url, attempt, err: msg }, 'request retry')
      await wait(BASE_DELAY * 2 ** attempt + Math.random() * BASE_DELAY)
    }
  }
}
