import { useCallback, useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import type { SearchResult } from '../services/api';

interface UploadProgress { docId: string; status: string; error?: string }
export interface SearchCompleted { query: string; results: SearchResult[] }
interface ServerToClient { 'document:upload_progress': (d: UploadProgress) => void; 'search:completed': (d: SearchCompleted) => void; 'user:join': (d:{userId:string})=>void; 'user:leave': (d:{userId:string})=>void }
interface ClientToServer { project_join: (d:{projectId:string})=>void; project_leave: (d:{projectId:string})=>void }

const buildSocket = (
  onConnect: () => void,
  onDisconnect: () => void,
  onJoin: (id: string) => void,
  onLeave: (id: string) => void,
): Socket<ServerToClient, ClientToServer> => {
  const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const userId = localStorage.getItem('userId') || 'anonymous';
  const s: Socket<ServerToClient, ClientToServer> = io(url, {
    transports: ['websocket'],
    reconnectionAttempts: 5,
    timeout: 5000,
    query: { user_id: userId },
  });
  s.on('connect', onConnect);
  s.on('disconnect', onDisconnect);
  s.on('user:join', ({ userId }) => onJoin(userId));
  s.on('user:leave', ({ userId }) => onLeave(userId));
  s.io.on('reconnect', onConnect);
  return s;
};

export const useSocket = () => {
  const [socket, setSocket] = useState<Socket<ServerToClient, ClientToServer> | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [users, setUsers] = useState<string[]>([]);
  const projects = useRef<Set<string>>(new Set());

  useEffect(() => {
    const s = buildSocket(
      () => {
        setIsConnected(true);
        projects.current.forEach((p) => s.emit('project_join', { projectId: p }));
      },
      () => setIsConnected(false),
      (id) => setUsers((u) => Array.from(new Set([...u, id]))),
      (id) => setUsers((u) => u.filter((i) => i !== id)),
    );
    setSocket(s);
    return () => {
      s.disconnect();
    };
  }, []);

  const joinProject = useCallback((projectId: string) => {
    if (projectId) {
      projects.current.add(projectId);
      socket?.emit('project_join', { projectId });
    }
  }, [socket]);

  const leaveProject = useCallback((projectId: string) => {
    if (projectId) {
      projects.current.delete(projectId);
      socket?.emit('project_leave', { projectId });
    }
  }, [socket]);

  return { socket, isConnected, users, joinProject, leaveProject };
};
