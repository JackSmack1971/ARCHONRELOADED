import http from 'http';
import { Server, Socket } from 'socket.io';
import { logger } from '../utils/logger';

const USER_RE = /^[a-zA-Z0-9_-]{1,50}$/;
const PROJ_RE = /^[a-zA-Z0-9_-]{1,50}$/;

export class SocketServerError extends Error {}

const validate = (re: RegExp, val: unknown): val is string =>
  typeof val === 'string' && re.test(val);

function setupMiddleware(io: Server): void {
  io.use((socket, next) => {
    try {
      const id = socket.handshake.query.user_id;
      if (!validate(USER_RE, id)) throw new SocketServerError('Invalid user ID');
      socket.data.userId = id;
      next();
    } catch (err) {
      next(err as Error);
    }
  });
}

function setupConnection(io: Server): void {
  io.on('connection', (socket: Socket) => {
    const userId = socket.data.userId as string;
    io.emit('user:join', { userId });

    socket.on('project_join', ({ projectId }) => {
      if (validate(PROJ_RE, projectId)) socket.join(`project:${projectId}`);
    });

    socket.on('project_leave', ({ projectId }) => {
      if (validate(PROJ_RE, projectId)) socket.leave(`project:${projectId}`);
    });

    socket.on('disconnect', () => io.emit('user:leave', { userId }));
    socket.on('error', (e) => logger.error({ err: e }, 'socket error'));
  });
}

export interface UploadProgress {
  docId: string;
  status: string;
  error?: string;
}

export interface SearchCompleted {
  query: string;
  results: unknown[];
}

export function createSocketServer(port = Number(process.env.SOCKET_PORT) || 7000) {
  const httpServer = http.createServer();
  const io = new Server(httpServer, {
    cors: { origin: process.env.CLIENT_URL || '*' },
  });

  setupMiddleware(io);
  setupConnection(io);
  httpServer.listen(port);

  const emit = (room: string, event: string, data: unknown) => io.to(room).emit(event, data);

  const broadcastUploadProgress = (projectId: string, d: UploadProgress): void => {
    if (validate(PROJ_RE, projectId)) emit(`project:${projectId}`, 'document:upload_progress', d);
  };

  const broadcastSearchCompleted = (projectId: string, d: SearchCompleted): void => {
    if (validate(PROJ_RE, projectId)) emit(`project:${projectId}`, 'search:completed', d);
  };

  const broadcastPresence = (userId: string, joined: boolean): void => {
    if (validate(USER_RE, userId)) io.emit(joined ? 'user:join' : 'user:leave', { userId });
  };

  return { io, httpServer, broadcastUploadProgress, broadcastSearchCompleted, broadcastPresence };
}
