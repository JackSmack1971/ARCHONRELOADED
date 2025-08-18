import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { searchDocuments, type SearchResult } from '../services/api';
import { useSocket } from './useSocket';

export const useSearch = (query: string) => {
  const { socket } = useSocket();
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!socket) return;
    const handler = (data: { query: string; results: SearchResult[] }) => {
      if (data.query === query) {
        queryClient.setQueryData(['search', query], data.results);
      }
    };
    socket.on('search:completed', handler);
    return () => {
      socket.off('search:completed', handler);
    };
  }, [socket, query, queryClient]);

  return useQuery<SearchResult[], Error>({
    queryKey: ['search', query],
    queryFn: async () => {
      try {
        return await searchDocuments(query);
      } catch (error) {
        if (error instanceof Error) {
          throw error;
        }
        throw new Error('Unknown error');
      }
    },
    enabled: query.length > 0,
    retry: 2,
  });
};
