import '@testing-library/jest-dom';
import { vi } from 'vitest';

vi.mock('socket.io-client', () => {
  const mSocket = {
    on: vi.fn(),
    off: vi.fn(),
    emit: vi.fn(),
    disconnect: vi.fn(),
    io: { on: vi.fn() },
  };
  return { io: () => mSocket };
});
