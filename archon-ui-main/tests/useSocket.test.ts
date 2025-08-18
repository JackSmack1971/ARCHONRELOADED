import { renderHook, act } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';

const handlers: Record<string, (arg?: any) => void> = {};
vi.mock('socket.io-client', () => {
  const mSocket = {
    on: vi.fn((e, cb) => { handlers[e] = cb; }),
    emit: vi.fn(),
    disconnect: vi.fn(),
  };
  return { io: () => mSocket };
});

import { useSocket } from '../src/hooks/useSocket';

describe('useSocket', () => {
  it('emits join and leave', () => {
    const { result } = renderHook(() => useSocket());
    act(() => handlers.connect?.());
    act(() => {
      result.current.joinProject('p1');
      result.current.leaveProject('p1');
    });
    expect(result.current.socket?.emit).toHaveBeenCalledWith('project_join', { projectId: 'p1' });
    expect(result.current.socket?.emit).toHaveBeenCalledWith('project_leave', { projectId: 'p1' });
  });
});
