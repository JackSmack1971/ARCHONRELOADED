import { render, screen, fireEvent } from '@testing-library/react'
import { StoreProvider, useStore } from '../src/store'

function Counter() {
  const { state, dispatch } = useStore()
  return (
    <div>
      <span>{state.count}</span>
      <button onClick={() => dispatch({ type: 'inc' })}>inc</button>
    </div>
  )
}

describe('StoreProvider', () => {
  it('toggles state', () => {
    render(
      <StoreProvider>
        <Counter />
      </StoreProvider>,
    )
    fireEvent.click(screen.getByText('inc'))
    expect(screen.getByText('1')).toBeInTheDocument()
  })
})
