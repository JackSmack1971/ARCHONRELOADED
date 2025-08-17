import pino from 'pino'
import { secureFetch } from '../utils/http'

export const logger = pino()

export class MCPError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'MCPError'
  }
}

export async function fetchMCP(resource: string): Promise<string> {
  if (!/^[\w/-]+$/.test(resource)) {
    logger.error({ resource }, 'invalid resource')
    throw new MCPError('Invalid resource')
  }
  const base = process.env.MCP_BASE_URL
  if (!base) {
    logger.error('missing MCP_BASE_URL')
    throw new MCPError('Missing MCP_BASE_URL')
  }
  logger.info({ resource }, 'fetchMCP start')
  try {
    const res = await secureFetch(`${base}/${resource}`)
    logger.info({ resource }, 'fetchMCP success')
    return await res.text()
  } catch (err) {
    logger.error({ resource, err: err instanceof Error ? err.message : err }, 'fetchMCP failure')
    throw new MCPError(err instanceof Error ? err.message : 'Unknown error')
  }
}
