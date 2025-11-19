import apiClient from '@/lib/apiClient';
import type { UserResponse } from '@/types';

export const signup = async (email: string, firstName: string): Promise<UserResponse> => {
  const response = await apiClient.post<UserResponse>('/auth/signup', {
    email,
    first_name: firstName,
  });
  return response.data;
};

export const login = async (email: string): Promise<UserResponse> => {
  const response = await apiClient.post<UserResponse>('/auth/login', { email });
  return response.data;
};
