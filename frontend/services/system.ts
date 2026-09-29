import { apiClient } from './api';
import { HealthResponse } from '@/types/api';

export const systemService = {
  async getHealth(): Promise<HealthResponse> {
    const res = await apiClient.get<HealthResponse>('/health');
    return res.data;
  },

  async getEngineMetadata(): Promise<any> {
    const res = await apiClient.get('/');
    return res.data;
  },
};
