import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Home } from '../src/pages/Home';

describe('Home', () => {
  it('renders heading and button', () => {
    render(<Home />);
    fireEvent.click(screen.getByText(/click me/i));
    expect(screen.getByRole('heading', { name: /archon ui/i })).toBeInTheDocument();
  });
});
