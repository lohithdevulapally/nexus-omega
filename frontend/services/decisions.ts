import { apiClient, DEFAULT_ORG_ID } from './api';
import { DecisionItem } from '@/types/api';

export const decisionsService = {
  async listDecisions(
    organizationId: string = DEFAULT_ORG_ID,
    limit: number = 50
  ): Promise<DecisionItem[]> {
    const res = await apiClient.get<DecisionItem[]>('/decisions', {
      params: { organization_id: organizationId, limit },
    });
    return res.data;
  },
};
