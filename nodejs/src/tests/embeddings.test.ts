import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { generateEmbedding, EmbeddingError } from '../embeddings'

describe('generateEmbedding', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.EMBEDDINGS_URL = 'https://emb.example.com'
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.EMBEDDINGS_URL
  })
  it('rejects invalid text', async () => {
    await expect(generateEmbedding('')).rejects.toBeInstanceOf(EmbeddingError)
  })
  it('fails without env', async () => {
    delete process.env.EMBEDDINGS_URL
    await expect(generateEmbedding('hi')).rejects.toBeInstanceOf(EmbeddingError)
  })
  it('returns embedding array', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ embedding: [1, 2, 3] }),
    })
    await expect(generateEmbedding('hi')).resolves.toEqual([1, 2, 3])
  })
})
