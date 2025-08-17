import { secureFetch } from '../utils/http'

export class EmbeddingError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'EmbeddingError'
  }
}

export async function generateEmbedding(text: string): Promise<number[]> {
  if (typeof text !== 'string' || !text.trim()) throw new EmbeddingError('Invalid text')
  const url = process.env.EMBEDDINGS_URL
  if (!url) throw new EmbeddingError('Missing EMBEDDINGS_URL')
  try {
    const res = await secureFetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    const data = (await res.json()) as { embedding: number[] }
    if (!Array.isArray(data.embedding)) throw new EmbeddingError('Bad response')
    return data.embedding
  } catch (err) {
    throw new EmbeddingError(err instanceof Error ? err.message : 'Unknown error')
  }
}
