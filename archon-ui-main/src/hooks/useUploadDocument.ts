import { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { uploadDocument, type UploadResponse } from '../services/api';
import { useSocket } from './useSocket';

interface UploadProgress { docId: string; status: string; error?: string }
interface UploadVars { projectId: string; file: File }

export const useUploadDocument = () => {
  const { socket, joinProject, leaveProject } = useSocket();
  const [progress, setProgress] = useState<UploadProgress | null>(null);

  useEffect(() => {
    if (!socket) return;
    const h = (d: UploadProgress) => setProgress(d);
    socket.on('document:upload_progress', h);
    return () => socket.off('document:upload_progress', h);
  }, [socket]);

  const mutation = useMutation<UploadResponse, Error, UploadVars>({
    mutationFn: async ({ projectId, file }) => {
      joinProject(projectId);
      try {
        return await uploadDocument(projectId, file);
      } finally {
        leaveProject(projectId);
      }
    },
  });

  return { ...mutation, progress };
};
