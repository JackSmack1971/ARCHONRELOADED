import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { secureFetch, HTTPError } from '../utils/http'

describe('secureFetch', () => {
  const originalFetch = global.fetch

  beforeEach(() => {
    global.fetch = vi
      .fn()
      .mockResolvedValue({ ok: false, status: 500, statusText: 'err' })
  })

  afterEach(() => {
    global.fetch = originalFetch
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('rejects invalid url', async () => {
    await expect(secureFetch('bad')).rejects.toBeInstanceOf(HTTPError)
  })

  it('honors max retries and throws HTTPError', async () => {
    vi.useFakeTimers()
    const p = secureFetch('https://example.com', {}, 2, 1)
    p.catch(() => {})
    await vi.runAllTimersAsync()
    await expect(p).rejects.toBeInstanceOf(HTTPError)
    expect((global.fetch as any).mock.calls.length).toBe(3)
  })

  it('uses exponential backoff with jitter', async () => {
    vi.useFakeTimers()
    const spy = vi.spyOn(global, 'setTimeout')
    vi.spyOn(Math, 'random').mockReturnValue(0)
    const p = secureFetch('https://example.com', {}, 2, 1)
    p.catch(() => {})
    await vi.runAllTimersAsync()
    await expect(p).rejects.toBeInstanceOf(HTTPError)
    const base = spy.mock.calls
      .map((c) => c[1] as number)
      .filter((d) => d !== 1)
    expect(base[1]).toBeGreaterThanOrEqual(base[0] * 2)
    spy.mockClear()
    ;(global.fetch as any).mockClear()
    vi.spyOn(Math, 'random').mockReturnValue(0.5)
    const p2 = secureFetch('https://example.com', {}, 1, 1)
    p2.catch(() => {})
    await vi.runAllTimersAsync()
    await expect(p2).rejects.toBeInstanceOf(HTTPError)
    const jitter = spy.mock.calls
      .map((c) => c[1] as number)
      .filter((d) => d !== 1)
    expect(jitter[0]).toBeGreaterThan(base[0])
  })

  it('returns on success', async () => {
    ;(global.fetch as any).mockResolvedValueOnce({ ok: true })
    const res = await secureFetch('https://example.com')
    expect(res.ok).toBe(true)
  })
})

