import { logger } from '../utils/logger'
import { secureFetch } from '../utils/http'

export class EmbeddingError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'EmbeddingError'
  }
}

export async function generateEmbedding(text: string): Promise<number[]> {
  if (typeof text !== 'string' || !text.trim()) {
    logger.error('invalid text')
    throw new EmbeddingError('Invalid text')
  }
  const url = process.env.EMBEDDINGS_URL
  if (!url) {
    logger.error('missing EMBEDDINGS_URL')
    throw new EmbeddingError('Missing EMBEDDINGS_URL')
  }
  logger.info('generateEmbedding start')
  try {
    const res = await secureFetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    const data = (await res.json()) as { embedding: number[] }
    if (!Array.isArray(data.embedding)) {
      logger.error('bad response')
      throw new EmbeddingError('Bad response')
    }
    logger.info('generateEmbedding success')
    return data.embedding
  } catch (err) {
    logger.error({ err: err instanceof Error ? err.message : err }, 'generateEmbedding failure')
    throw new EmbeddingError(err instanceof Error ? err.message : 'Unknown error')
  }
}
