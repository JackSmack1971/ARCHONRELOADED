import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { fetchMCP, MCPError } from '../mcp'

describe('fetchMCP', () => {
  const originalFetch = global.fetch
  beforeEach(() => {
    process.env.MCP_BASE_URL = 'https://api.example.com'
  })
  afterEach(() => {
    global.fetch = originalFetch
    delete process.env.MCP_BASE_URL
  })
  it('rejects invalid resource', async () => {
    await expect(fetchMCP('bad resource')).rejects.toBeInstanceOf(MCPError)
  })
  it('fails without env', async () => {
    delete process.env.MCP_BASE_URL
    await expect(fetchMCP('good')).rejects.toBeInstanceOf(MCPError)
  })
  it('fetches valid resource', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => 'ok' })
    await expect(fetchMCP('good')).resolves.toBe('ok')
  })
})
