import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../src/App';

describe('App', () => {
  it('renders home page', () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: /archon ui/i })).toBeInTheDocument();
  });
});
