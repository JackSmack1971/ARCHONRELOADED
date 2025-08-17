import { render, screen } from '@testing-library/react'
import Page from '../src/app/page'

vi.mock('../src/services/apiClient', () => ({
  apiGet: vi.fn().mockResolvedValue({ status: 'ok' })
}))

process.env.NEXT_PUBLIC_API_BASE_URL = 'http://example.com'

describe('Page', () => {
  it('renders header', async () => {
    render(<Page />)
    expect(await screen.findByText('ARCHON RELOADED')).toBeInTheDocument()
  })
})
