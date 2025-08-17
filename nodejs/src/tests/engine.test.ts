import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { runEngineTask, EngineError } from '../engine'

describe('runEngineTask', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.ENGINE_URL = 'https://engine.example.com'
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.ENGINE_URL
  })
  it('rejects invalid id', async () => {
    await expect(runEngineTask('bad')).rejects.toBeInstanceOf(EngineError)
  })
  it('fails without env', async () => {
    delete process.env.ENGINE_URL
    await expect(runEngineTask('123e4567-e89b-12d3-a456-426614174000')).rejects.toBeInstanceOf(EngineError)
  })
  it('posts task', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => 'done' })
    await expect(runEngineTask('123e4567-e89b-12d3-a456-426614174000')).resolves.toBe('done')
  })
})
