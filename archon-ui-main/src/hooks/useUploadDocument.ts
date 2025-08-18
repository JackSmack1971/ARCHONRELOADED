import { useMutation } from '@tanstack/react-query';
import { uploadDocument, type UploadResponse } from '../services/api';

interface UploadVars {
  projectId: string;
  file: File;
}

export const useUploadDocument = () =>
  useMutation<UploadResponse, Error, UploadVars>({
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
