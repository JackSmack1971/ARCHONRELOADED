import axios, { AxiosInstance } from 'axios';

export class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

const API_URL = import.meta.env.VITE_API_URL || '';

export const client: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

export async function request<T>(endpoint: string, retries = 3): Promise<T> {
  if (!/^\/[\w-]+(?:\/[\w-]+)*$/.test(endpoint)) {
    throw new ApiError('Invalid endpoint');
  }

  for (let attempt = 0; attempt < retries; attempt += 1) {
    try {
      const { data } = await client.get<T>(endpoint);
      return data;
    } catch (error) {
      if (attempt === retries - 1) {
        if (axios.isAxiosError(error)) {
          throw new ApiError(error.message, error.response?.status);
        }
        throw new ApiError('Unexpected error');
      }
    }
  }
  throw new ApiError('Request failed');
}
