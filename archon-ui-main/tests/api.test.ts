import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createProject, searchDocuments, uploadDocument } from '../src/services/api';
import { client } from '../src/services/apiClient';

beforeEach(() => {
  vi.restoreAllMocks();
});

describe('api services', () => {
  it('creates project', async () => {
    vi.spyOn(client, 'post').mockResolvedValueOnce({ data: { id: '1', name: 'a', description: 'b' } });
    const res = await createProject({ name: 'a', description: 'b' });
    expect(res.id).toBe('1');
  });

  it('uploads document', async () => {
    const file = new File(['data'], 't.txt', { type: 'text/plain' });
    vi.spyOn(client, 'post').mockResolvedValueOnce({ data: { id: 'd1', name: 't.txt' } });
    const res = await uploadDocument('p1', file);
    expect(res.id).toBe('d1');
  });

  it('searches documents', async () => {
    vi.spyOn(client, 'get').mockResolvedValueOnce({ data: [{ id: '1', title: 'x', snippet: 'y' }] });
    const res = await searchDocuments('test');
    expect(res[0].id).toBe('1');
  });

  it('rejects invalid project name', async () => {
    await expect(createProject({ name: '', description: 'b' })).rejects.toBeInstanceOf(Error);
  });
});
