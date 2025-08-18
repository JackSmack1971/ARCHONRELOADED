import axios, { type AxiosInstance } from 'axios';

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const API_URL = import.meta.env.VITE_API_URL || '';

export const client: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 5000,
  withCredentials: true,
});

const ENDPOINT_REGEX = /^\/[\w-]+(?:\/[\w-]+)*(?:\?[\w=&-]*)?$/;

let authToken: string | null = null;

export const setAuthToken = (token: string | null): void => {
  authToken = token;
};

const getAuthToken = (): string | null => authToken;

client.interceptors.request.use(
  (config) => {
    try {
      const token = getAuthToken();
      if (token) {
        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Token retrieval failed', error);
    }
    return config;
  },
  (error) => Promise.reject(error),
);

export async function request<T>(endpoint: string, retries = 3): Promise<T> {
  if (!ENDPOINT_REGEX.test(endpoint)) {
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

export async function postRequest<T>(
  endpoint: string,
  payload: unknown,
  retries = 3,
): Promise<T> {
  if (!ENDPOINT_REGEX.test(endpoint)) {
    throw new ApiError('Invalid endpoint');
  }
  for (let attempt = 0; attempt < retries; attempt += 1) {
    try {
      const { data } = await client.post<T>(endpoint, payload);
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

export async function uploadRequest<T>(
  endpoint: string,
  formData: FormData,
  retries = 3,
): Promise<T> {
  if (!ENDPOINT_REGEX.test(endpoint)) {
    throw new ApiError('Invalid endpoint');
  }
  for (let attempt = 0; attempt < retries; attempt += 1) {
    try {
      const { data } = await client.post<T>(endpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
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
  throw new ApiError('Upload failed');
}
