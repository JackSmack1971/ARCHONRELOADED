import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi, describe, it, expect } from 'vitest';
import { useSearch } from '../src/hooks/useSearch';
import * as api from '../src/services/api';
import type { SearchCompleted } from '../src/hooks/useSocket';

const handlers: Record<string, (data: SearchCompleted) => void> = {};

vi.mock('../src/hooks/useSocket', () => ({
  useSocket: () => ({
    socket: {
      on: (event: string, handler: (data: SearchCompleted) => void) => {
        handlers[event] = handler;
      },
      off: (event: string) => {
        delete handlers[event];
      },
    },
  }),
}));

describe('useSearch socket integration', () => {
  it('updates cache when search:completed fires', async () => {
    const client = new QueryClient();
    vi.spyOn(api, 'searchDocuments').mockResolvedValue([]);
    const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    );
    renderHook(() => useSearch('hello'), { wrapper });
    await waitFor(() => expect(api.searchDocuments).toHaveBeenCalledWith('hello'));
    const results = [{ id: '1', title: 't', snippet: 's' }];
    handlers['search:completed']?.({ query: 'hello', results });
    expect(client.getQueryData(['search', 'hello'])).toEqual(results);
  });
});
