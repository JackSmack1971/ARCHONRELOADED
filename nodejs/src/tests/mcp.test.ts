import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
vi.mock('../utils/logger', () => ({
  logger: {
    info: vi.fn(),
    error: vi.fn(),
    warn: vi.fn(),
  },
}))
import { fetchMCP, MCPError } from '../mcp'
import { logger } from '../utils/logger'

describe('fetchMCP', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.MCP_BASE_URL = 'https://api.example.com'
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.MCP_BASE_URL
    vi.clearAllMocks()
  })
  it('rejects invalid resource', async () => {
    await expect(fetchMCP('bad resource')).rejects.toBeInstanceOf(MCPError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('fails without env', async () => {
    delete process.env.MCP_BASE_URL
    await expect(fetchMCP('good')).rejects.toBeInstanceOf(MCPError)
    expect(logger.error).toHaveBeenCalled()
  })

  it('handles fetch failure', async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValue({ ok: false, status: 500, statusText: 'err' })
    await expect(fetchMCP('good')).rejects.toBeInstanceOf(MCPError)
    expect(logger.error).toHaveBeenCalled()
  })
  it('fetches valid resource', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => 'ok' })
    await expect(fetchMCP('good')).resolves.toBe('ok')
    expect(logger.info).toHaveBeenCalledTimes(2)
  })
})
