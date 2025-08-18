import { useQuery } from '@tanstack/react-query';
import { searchDocuments, type SearchResult } from '../services/api';

export const useSearch = (query: string) =>
  useQuery<SearchResult[], Error>({
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
