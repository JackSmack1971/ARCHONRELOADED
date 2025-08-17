import { render, screen } from '@testing-library/react'
import Page from '../src/app/page'
import { apiGet, ApiError } from '../src/services/apiClient'

vi.mock('../src/services/apiClient', async () => {
  const actual = await vi.importActual<typeof import('../src/services/apiClient')>(
    '../src/services/apiClient',
  )
  return { ...actual, apiGet: vi.fn() }
})

process.env.NEXT_PUBLIC_API_BASE_URL = 'http://example.com'

describe('Page', () => {
  it('renders header', async () => {
    ;(apiGet as any).mockResolvedValue({ status: 'ok' })
    render(<Page />)
    expect(await screen.findByText('ARCHON RELOADED')).toBeInTheDocument()
  })

  it('renders error', async () => {
    ;(apiGet as any).mockRejectedValue(new ApiError('fail'))
    render(<Page />)
    expect(await screen.findByRole('alert')).toHaveTextContent('fail')
  })
})
