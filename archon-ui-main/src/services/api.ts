import { request, postRequest, uploadRequest, ApiError } from './apiClient';

const NAME_REGEX = /^[\w\s-]{1,100}$/;

export interface ProjectPayload {
  name: string;
  description: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
}

export interface UploadResponse {
  id: string;
  name: string;
}

export interface SearchResult {
  id: string;
  title: string;
  snippet: string;
}

export async function createProject(payload: ProjectPayload): Promise<Project> {
  if (!NAME_REGEX.test(payload.name) || !NAME_REGEX.test(payload.description)) {
    throw new ApiError('Invalid project data');
  }
  return postRequest<Project>('/projects', payload);
}

export async function uploadDocument(projectId: string, file: File): Promise<UploadResponse> {
  if (!NAME_REGEX.test(projectId)) {
    throw new ApiError('Invalid project ID');
  }
  if (!file || file.size === 0 || file.size > 5_000_000) {
    throw new ApiError('Invalid file');
  }
  const form = new FormData();
  form.append('file', file);
  return uploadRequest<UploadResponse>(`/projects/${projectId}/documents`, form);
}

export async function searchDocuments(query: string): Promise<SearchResult[]> {
  if (!NAME_REGEX.test(query)) {
    throw new ApiError('Invalid query');
  }
  return request<SearchResult[]>(`/search?query=${encodeURIComponent(query)}`);
}
