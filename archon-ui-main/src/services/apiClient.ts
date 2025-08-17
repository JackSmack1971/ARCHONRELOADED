import { z } from 'zod'

export class ApiError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

const pathSchema = z.string().min(1)

function getBaseUrl(): string {
  const url = process.env.NEXT_PUBLIC_API_BASE_URL
  if (!url) throw new ApiError('API base URL not configured')
  try {
    return new URL(url).toString()
  } catch {
    throw new ApiError('Invalid API base URL')
  }
}

export async function apiGet<T>(
  path: string,
  retries = 3,
  timeout = 5000,
): Promise<T> {
  const result = pathSchema.safeParse(path)
  if (!result.success) throw new ApiError('Invalid path')
  const urlPath = result.data
  const baseUrl = getBaseUrl()

  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), timeout)
    try {
      const res = await fetch(`${baseUrl}${urlPath}`, {
        signal: controller.signal,
      })
      clearTimeout(timer)
      if (!res.ok) throw new ApiError(`Request failed: ${res.status}`)
      const data: T = await res.json()
      return data
    } catch (err) {
      clearTimeout(timer)
      if (attempt === retries) {
        throw new ApiError((err as Error).message)
      }
    }
  }
  throw new ApiError('Request failed')
}
