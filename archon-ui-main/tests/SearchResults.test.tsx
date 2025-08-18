import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SearchResults } from '../src/features/search/SearchResults';
import * as hook from '../src/hooks/useSearch';
import { describe, it, expect, vi } from 'vitest';

describe('SearchResults', () => {
  it('shows results', async () => {
    vi.spyOn(hook, 'useSearch').mockImplementation((q: string) => ({
      data: q ? [{ id: '1', title: 't', snippet: 's' }] : [],
      error: null,
      isLoading: false,
    } as ReturnType<typeof hook.useSearch>));
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <SearchResults />
      </QueryClientProvider>,
    );
    fireEvent.change(screen.getByLabelText('search'), { target: { value: 'a' } });
    await waitFor(() => expect(screen.getByText('t')).toBeInTheDocument());
  });
});
