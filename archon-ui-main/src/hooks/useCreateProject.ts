import { useMutation } from '@tanstack/react-query';
import { createProject, type ProjectPayload, type Project } from '../services/api';

export const useCreateProject = () =>
  useMutation<Project, Error, ProjectPayload>({
    mutationFn: async (payload) => {
      try {
        return await createProject(payload);
      } catch (error) {
        if (error instanceof Error) {
          throw error;
        }
        throw new Error('Unknown error');
      }
    },
  });
