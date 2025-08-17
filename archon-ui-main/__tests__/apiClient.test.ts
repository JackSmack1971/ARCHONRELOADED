import { apiGet, ApiError } from '../src/services/apiClient'

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

  it('retries and fails', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error('fail'))
    // @ts-ignore: override for test
    global.fetch = fetchMock
    await expect(apiGet('/test', 1, 10)).rejects.toBeInstanceOf(ApiError)
    expect(fetchMock).toHaveBeenCalledTimes(2)
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
