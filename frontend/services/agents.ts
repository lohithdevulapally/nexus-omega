import { apiClient, DEFAULT_ORG_ID } from './api';
import { AgentRunItem } from '@/types/api';

export const agentsService = {
  async listRuns(
    organizationId: string = DEFAULT_ORG_ID,
    limit: number = 50
  ): Promise<AgentRunItem[]> {
    const res = await apiClient.get<AgentRunItem[]>('/agents/runs', {
      params: { organization_id: organizationId, limit },
    });
    return res.data;
  },
};
