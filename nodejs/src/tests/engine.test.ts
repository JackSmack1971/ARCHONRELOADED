import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { runEngineTask, EngineError, logger } from '../engine'

describe('runEngineTask', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.ENGINE_URL = 'https://engine.example.com'
    vi.spyOn(logger, 'info')
    vi.spyOn(logger, 'error')
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.ENGINE_URL
    vi.restoreAllMocks()
  })
  it('rejects invalid id', async () => {
    await expect(runEngineTask('bad')).rejects.toBeInstanceOf(EngineError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('fails without env', async () => {
    delete process.env.ENGINE_URL
    await expect(runEngineTask('123e4567-e89b-12d3-a456-426614174000')).rejects.toBeInstanceOf(EngineError)
    expect(logger.error).toHaveBeenCalled()
  })

  it('fails with invalid ENGINE_URL', async () => {
    process.env.ENGINE_URL = 'bad'
    await expect(
      runEngineTask('123e4567-e89b-12d3-a456-426614174000'),
    ).rejects.toBeInstanceOf(EngineError)
    expect(logger.error).toHaveBeenCalled()
  })

  it('handles fetch failure', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('timeout'))
    await expect(
      runEngineTask('123e4567-e89b-12d3-a456-426614174000'),
    ).rejects.toBeInstanceOf(EngineError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('posts task', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => 'done' })
    await expect(runEngineTask('123e4567-e89b-12d3-a456-426614174000')).resolves.toBe('done')
    expect(logger.info).toHaveBeenCalledTimes(2)
  })
})
