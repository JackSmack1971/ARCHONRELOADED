import { useCallback, useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

interface UploadProgress {
  docId: string;
  status: string;
  error?: string;
}

export interface SearchCompleted {
  query: string;
  results: unknown[];
}

interface ServerToClientEvents {
  'document:upload_progress': (data: UploadProgress) => void;
  'search:completed': (data: SearchCompleted) => void;
  'user:join': (data: { userId: string }) => void;
  'user:leave': (data: { userId: string }) => void;
}

interface ClientToServerEvents {
  project_join: (data: { projectId: string }) => void;
  project_leave: (data: { projectId: string }) => void;
}

export const useSocket = () => {
  const [socket, setSocket] = useState<
    Socket<ServerToClientEvents, ClientToServerEvents> | null
  >(null);
  const [isConnected, setIsConnected] = useState(false);
  const [users, setUsers] = useState<string[]>([]);

  useEffect(() => {
    const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const userId = localStorage.getItem('userId') || 'anonymous';
    const s: Socket<ServerToClientEvents, ClientToServerEvents> = io(url, {
      transports: ['websocket'],
      reconnectionAttempts: 5,
      timeout: 5000,
      query: { user_id: userId },
    });

    s.on('connect', () => setIsConnected(true));
    s.on('disconnect', () => setIsConnected(false));
    s.on('connect_error', (err) => console.error('Socket error', err));
    s.on('user:join', ({ userId }) =>
      setUsers((u) => Array.from(new Set([...u, userId])))
    );
    s.on('user:leave', ({ userId }) =>
      setUsers((u) => u.filter((id) => id !== userId))
    );

    setSocket(s);

    return () => {
      s.disconnect();
    };
  }, []);

  const joinProject = useCallback(
    (projectId: string) => {
      if (projectId) {
        socket?.emit('project_join', { projectId });
      }
    },
    [socket]
  );

  const leaveProject = useCallback(
    (projectId: string) => {
      if (projectId) {
        socket?.emit('project_leave', { projectId });
      }
    },
    [socket]
  );

  return { socket, isConnected, users, joinProject, leaveProject };
};
