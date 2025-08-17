export class HTTPError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'HTTPError'
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
    throw new Error('Invalid URL')
  }
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeout)
  try {
    const res = await fetch(url, { ...options, signal: controller.signal })
    if (!res.ok) throw new HTTPError(res.status, res.statusText)
    return res
  } catch (err) {
    if (retries > 0) return secureFetch(url, options, retries - 1, timeout)
    throw err instanceof Error ? err : new Error('Unknown error')
  } finally {
    clearTimeout(id)
  }
}
