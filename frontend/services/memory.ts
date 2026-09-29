import { apiClient, DEFAULT_ORG_ID } from './api';
import { ExperienceItem, MemorySearchResponse, MemoryReflectResponse } from '@/types/memory';

export const memoryService = {
  async searchMemories(
    query: string,
    organizationId: string = DEFAULT_ORG_ID,
    limit: number = 20
  ): Promise<MemorySearchResponse> {
    const res = await apiClient.get<MemorySearchResponse>('/memory/search', {
      params: { query, organization_id: organizationId, limit },
    });
    return res.data;
  },

  async reflectMemories(
    query: string,
    context?: string
  ): Promise<MemoryReflectResponse> {
    const res = await apiClient.post<MemoryReflectResponse>('/memory/reflect', {
      query,
      context,
    });
    return res.data;
  },

  async listExperiences(
    organizationId: string = DEFAULT_ORG_ID,
    experienceType?: string,
    limit: number = 50
  ): Promise<ExperienceItem[]> {
    const res = await apiClient.get<ExperienceItem[]>('/memory/experiences', {
      params: { organization_id: organizationId, experience_type: experienceType, limit },
    });
    return res.data;
  },

  async retainExperience(
    content: string,
    experienceType: string = 'incident_resolution',
    organizationId: string = DEFAULT_ORG_ID,
    metadata: Record<string, any> = {}
  ): Promise<any> {
    const res = await apiClient.post('/memory/retain', {
      organization_id: organizationId,
      experience_type: experienceType,
      content,
      metadata,
    });
    return res.data;
  },
};
