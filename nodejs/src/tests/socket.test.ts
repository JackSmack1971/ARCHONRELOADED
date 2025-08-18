import { describe, expect, it, beforeAll, afterAll } from 'vitest';
import { createSocketServer } from '../socket/server';
import { io as Client } from 'socket.io-client';

let port: number;
let server: ReturnType<typeof createSocketServer>;

beforeAll(() => {
  server = createSocketServer(0);
  const address = server.httpServer.address();
  if (typeof address === 'object' && address) port = address.port;
});

afterAll(() => {
  server.io.close();
  server.httpServer.close();
});

describe('socket server', () => {
  it('broadcasts upload progress', async () => {
    const client = Client(`http://localhost:${port}`, {
      query: { user_id: 'u1' },
      transports: ['websocket'],
    });
    await new Promise<void>((res) => client.on('connect', () => res()));
    client.emit('project_join', { projectId: 'p1' });
    await new Promise((r) => setTimeout(r, 50));
    const received = new Promise((res) => client.on('document:upload_progress', res));
    server.broadcastUploadProgress('p1', { docId: 'd1', status: 'done' });
    const data = await received;
    expect(data).toStrictEqual({ docId: 'd1', status: 'done' });
    client.disconnect();
  }, 10000);
});
