import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { secureFetch, HTTPError } from '../utils/http'

describe('secureFetch', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false, status: 500, statusText: 'err' })
  })
  afterEach(() => {
    global.fetch = originalFetch
  })
  it('rejects invalid url', async () => {
    await expect(secureFetch('bad')).rejects.toBeTruthy()
  })
  it('retries and throws HTTPError', async () => {
    await expect(secureFetch('https://example.com')).rejects.toBeInstanceOf(HTTPError)
    expect((global.fetch as any).mock.calls.length).toBe(3)
  })
  it('returns on success', async () => {
    (global.fetch as any).mockResolvedValueOnce({ ok: true })
    const res = await secureFetch('https://example.com')
    expect(res.ok).toBe(true)
  })
})
