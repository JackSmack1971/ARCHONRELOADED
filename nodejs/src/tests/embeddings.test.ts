import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { generateEmbedding, EmbeddingError, logger } from '../embeddings'

describe('generateEmbedding', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.EMBEDDINGS_URL = 'https://emb.example.com'
    vi.spyOn(logger, 'info')
    vi.spyOn(logger, 'error')
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.EMBEDDINGS_URL
    vi.restoreAllMocks()
  })
  it('rejects invalid text', async () => {
    await expect(generateEmbedding('')).rejects.toBeInstanceOf(EmbeddingError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('fails without env', async () => {
    delete process.env.EMBEDDINGS_URL
    await expect(generateEmbedding('hi')).rejects.toBeInstanceOf(EmbeddingError)
    expect(logger.error).toHaveBeenCalled()
  })

  it('handles fetch failure', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('timeout'))
    await expect(generateEmbedding('hi')).rejects.toBeInstanceOf(EmbeddingError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('returns embedding array', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ embedding: [1, 2, 3] }),
    })
    await expect(generateEmbedding('hi')).resolves.toEqual([1, 2, 3])
    expect(logger.info).toHaveBeenCalledTimes(2)
  })
})
