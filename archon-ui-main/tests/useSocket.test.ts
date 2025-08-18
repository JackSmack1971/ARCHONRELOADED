import { renderHook, act } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';

vi.mock('socket.io-client', () => {
  const mSocket = {
    on: vi.fn(),
    emit: vi.fn(),
    disconnect: vi.fn(),
  };
  return { io: () => mSocket };
});

import { useSocket } from '../src/hooks/useSocket';

describe('useSocket', () => {
  it('provides join and leave helpers', () => {
    const { result } = renderHook(() => useSocket());
    act(() => {
      result.current.joinProject('p1');
      result.current.leaveProject('p1');
    });
    expect(result.current.socket).toBeTruthy();
  });
});
