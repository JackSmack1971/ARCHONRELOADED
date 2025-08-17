export class HTTPError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'HTTPError'
  }
}

const BASE_DELAY = 100

export async function secureFetch(
  url: string,
  options: RequestInit = {},
  retries = 2,
  timeout = 5000,
): Promise<Response> {
  try {
    new URL(url)
  } catch {
    throw new HTTPError(0, 'Invalid URL')
  }
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController()
    const id = setTimeout(() => controller.abort(), timeout)
    try {
      const res = await fetch(url, { ...options, signal: controller.signal })
      if (!res.ok) throw new HTTPError(res.status, res.statusText)
      return res
    } catch (err) {
      if (attempt === retries) {
        const message = err instanceof Error ? err.message : 'Unknown error'
        throw err instanceof HTTPError ? err : new HTTPError(0, message)
      }
      await new Promise((r) => setTimeout(r, BASE_DELAY * 2 ** attempt + Math.random() * BASE_DELAY))
    } finally {
      clearTimeout(id)
    }
  }
  throw new HTTPError(0, 'Failed to fetch')
}
