import { describe, it, expect } from 'vitest'
import { fetchMCP, runEngineTask, generateEmbedding } from '..'

describe('index exports', () => {
  it('exports functions', () => {
    expect(fetchMCP).toBeTypeOf('function')
    expect(runEngineTask).toBeTypeOf('function')
    expect(generateEmbedding).toBeTypeOf('function')
  })
})
