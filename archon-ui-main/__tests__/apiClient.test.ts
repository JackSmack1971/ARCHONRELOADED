import { apiGet, ApiError } from '../src/services/apiClient'

process.env.NEXT_PUBLIC_API_BASE_URL = 'http://example.com'

describe('apiGet', () => {
  it('throws on invalid path', async () => {
    await expect(apiGet('')).rejects.toBeInstanceOf(ApiError)
  })

  it('retries and fails', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error('fail'))
    // @ts-ignore: override for test
    global.fetch = fetchMock
    await expect(apiGet('/test', 1, 10)).rejects.toBeInstanceOf(ApiError)
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})
