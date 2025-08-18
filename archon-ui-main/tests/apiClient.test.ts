import { describe, it, expect, vi, afterEach } from 'vitest';
import {
  request,
  postRequest,
  uploadRequest,
  ApiError,
  client,
  setAuthToken,
} from '../src/services/apiClient';
import type { InternalAxiosRequestConfig } from 'axios';

afterEach(() => {
  vi.restoreAllMocks();
  setAuthToken(null);
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

  it('postRequest sends data', async () => {
    vi.spyOn(client, 'post').mockResolvedValueOnce({ data: { ok: true } });
    const data = await postRequest('/post', { a: 1 });
    expect(data).toEqual({ ok: true });
  });

  it('uploadRequest handles errors', async () => {
    vi.spyOn(client, 'post').mockRejectedValue(new Error('fail'));
    const form = new FormData();
    form.append('f', 'v');
    await expect(uploadRequest('/upload', form, 1)).rejects.toBeInstanceOf(ApiError);
  });

  it('adds Authorization header when token is set', async () => {
    setAuthToken('secureToken');
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) => ({
      data: { ok: true },
      status: 200,
      statusText: 'OK',
      headers: {},
      config,
    }));
    client.defaults.adapter = adapter;
    await request('/auth');
    expect(adapter).toHaveBeenCalled();
    expect(adapter.mock.calls[0][0].headers.Authorization).toBe('Bearer secureToken');
  });
});
