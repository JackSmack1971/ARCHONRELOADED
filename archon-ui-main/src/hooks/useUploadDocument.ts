import { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { uploadDocument, type UploadResponse } from '../services/api';
import { useSocket } from './useSocket';

interface UploadProgress {
  docId: string;
  status: string;
  error?: string;
}

interface UploadVars {
  projectId: string;
  file: File;
}

export const useUploadDocument = () => {
  const { socket } = useSocket();
  const [progress, setProgress] = useState<UploadProgress | null>(null);

  useEffect(() => {
    if (!socket) return;
    const handler = (data: UploadProgress) => setProgress(data);
    socket.on('document:upload_progress', handler);
    return () => {
      socket.off('document:upload_progress', handler);
    };
  }, [socket]);

  const mutation = useMutation<UploadResponse, Error, UploadVars>({
    mutationFn: async ({ projectId, file }) => {
      try {
        return await uploadDocument(projectId, file);
      } catch (error) {
        if (error instanceof Error) {
          throw error;
        }
        throw new Error('Unknown error');
      }
    },
  });

  return { ...mutation, progress };
};
