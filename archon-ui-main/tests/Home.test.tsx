import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';
import { Home } from '../src/pages/Home';

describe('Home', () => {
  it('renders heading', () => {
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <Home />
      </QueryClientProvider>,
    );
    expect(screen.getByRole('heading', { name: /archon ui/i })).toBeInTheDocument();
  });
});
