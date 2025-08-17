import { secureFetch } from '../utils/http'

export class MCPError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'MCPError'
  }
}

export async function fetchMCP(resource: string): Promise<string> {
  if (!/^[\w/-]+$/.test(resource)) throw new MCPError('Invalid resource')
  const base = process.env.MCP_BASE_URL
  if (!base) throw new MCPError('Missing MCP_BASE_URL')
  try {
    const res = await secureFetch(`${base}/${resource}`)
    return await res.text()
  } catch (err) {
    throw new MCPError(err instanceof Error ? err.message : 'Unknown error')
  }
}
