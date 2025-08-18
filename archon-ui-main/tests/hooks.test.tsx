import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi } from 'vitest';
import { useCreateProject } from '../src/hooks/useCreateProject';
import { useUploadDocument } from '../src/hooks/useUploadDocument';
import { useSearch } from '../src/hooks/useSearch';
import * as api from '../src/services/api';

const joinProject = vi.fn();
const leaveProject = vi.fn();
vi.mock('../src/hooks/useSocket', () => ({
  useSocket: () => ({
    socket: { on: vi.fn(), off: vi.fn(), emit: vi.fn() },
    joinProject,
    leaveProject,
  }),
}));

const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const client = new QueryClient();
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
};

describe('hooks', () => {
  it('useCreateProject calls API', async () => {
    vi.spyOn(api, 'createProject').mockResolvedValue({ id: '1', name: 'a', description: 'b' });
    const { result } = renderHook(() => useCreateProject(), { wrapper });
    await act(async () => {
      await result.current.mutateAsync({ name: 'a', description: 'b' });
    });
    expect(api.createProject).toHaveBeenCalled();
  });

  it('useUploadDocument joins project and calls API', async () => {
    vi.spyOn(api, 'uploadDocument').mockResolvedValue({ id: 'd1', name: 't.txt' });
    const { result } = renderHook(() => useUploadDocument(), { wrapper });
    const file = new File(['data'], 't.txt', { type: 'text/plain' });
    await act(async () => {
      await result.current.mutateAsync({ projectId: 'p1', file });
    });
    expect(joinProject).toHaveBeenCalledWith('p1');
    expect(leaveProject).toHaveBeenCalledWith('p1');
    expect(api.uploadDocument).toHaveBeenCalled();
  });

  it('useSearch calls API', async () => {
    vi.spyOn(api, 'searchDocuments').mockResolvedValue([{ id: '1', title: 't', snippet: 's' }]);
    const { result } = renderHook(() => useSearch('a'), { wrapper });
    await act(async () => {
      await result.current.refetch();
    });
    expect(api.searchDocuments).toHaveBeenCalledWith('a');
  });
});
