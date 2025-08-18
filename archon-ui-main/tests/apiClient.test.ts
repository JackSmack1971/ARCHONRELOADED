import { describe, it, expect, vi, afterEach } from 'vitest';
import { request, ApiError, client } from '../src/services/apiClient';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('apiClient', () => {
  it('rejects invalid endpoint', async () => {
    await expect(request('invalid endpoint')).rejects.toBeInstanceOf(ApiError);
  });

  it('returns data on success', async () => {
    vi.spyOn(client, 'get').mockResolvedValueOnce({ data: { ok: true } });
    const data = await request('/test');
    expect(data).toEqual({ ok: true });
  });

  it('retries and throws ApiError on failure', async () => {
    vi.spyOn(client, 'get').mockRejectedValue(new Error('fail'));
    await expect(request('/fail', 2)).rejects.toBeInstanceOf(ApiError);
    expect(client.get).toHaveBeenCalledTimes(2);
  });
});
