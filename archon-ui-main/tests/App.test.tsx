import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';
import App from '../src/App';

describe('App', () => {
  it('renders home page', () => {
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <App />
      </QueryClientProvider>,
    );
    expect(screen.getByRole('heading', { name: /archon ui/i })).toBeInTheDocument();
  });
});
