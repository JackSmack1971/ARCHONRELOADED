import { apiGet, ApiError } from '../src/services/apiClient'
import { logger } from '../src/utils/logger'

describe('apiGet', () => {
  beforeEach(() => {
    process.env.NEXT_PUBLIC_API_BASE_URL = 'http://example.com'
  })

  it('throws on invalid path', async () => {
    await expect(apiGet('')).rejects.toBeInstanceOf(ApiError)
  })

  it('throws on invalid base URL', async () => {
    process.env.NEXT_PUBLIC_API_BASE_URL = 'not-a-url'
    // @ts-ignore: override for test
    global.fetch = vi.fn()
    await expect(apiGet('/test')).rejects.toBeInstanceOf(ApiError)
    expect(global.fetch).not.toHaveBeenCalled()
  })

  it('retries with backoff and logs', async () => {
    vi.useFakeTimers()
    const fetchMock = vi.fn().mockRejectedValue(new Error('fail'))
    // @ts-ignore: override for test
    global.fetch = fetchMock
    const loggerSpy = vi.spyOn(logger, 'info')
    const setTimeoutSpy = vi.spyOn(global, 'setTimeout')
    const promise = apiGet('/test', 2, 10, 50)
    const assertion = expect(promise).rejects.toBeInstanceOf(ApiError)
    await vi.runAllTimersAsync()
    await assertion
    expect(fetchMock).toHaveBeenCalledTimes(3)
    expect(loggerSpy).toHaveBeenCalledTimes(2)
    const delays = setTimeoutSpy.mock.calls.map((c) => c[1])
    expect(delays).toContain(50)
    expect(delays).toContain(100)
  })

  it('returns typed response', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ value: 'ok' }),
    })
    // @ts-ignore: override for test
    global.fetch = fetchMock
    const data = await apiGet<{ value: string }>('/test')
    expect(data.value).toBe('ok')
  })
})
