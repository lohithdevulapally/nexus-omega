import { apiClient, DEFAULT_ORG_ID } from './api';
import { AgentInvestigateResponse } from '@/types/investigation';

export const investigationsService = {
  async runInvestigation(
    request: string,
    organizationId: string = DEFAULT_ORG_ID,
    userId: string = 'mission-control-operator'
  ): Promise<AgentInvestigateResponse> {
    const res = await apiClient.post<AgentInvestigateResponse>('/agents/investigate', {
      organization_id: organizationId,
      request,
      user_id: userId,
    });
    return res.data;
  },

  async getSimilarIncidents(
    description: string,
    organizationId: string = DEFAULT_ORG_ID,
    limit: number = 5
  ): Promise<any> {
    const res = await apiClient.post('/investigations/similar', {
      organization_id: organizationId,
      description,
      limit,
    });
    return res.data;
  },

  async getAvoidMistakes(
    proposedAction: string,
    context: string,
    organizationId: string = DEFAULT_ORG_ID
  ): Promise<any> {
    const res = await apiClient.post('/investigations/avoid-mistakes', {
      organization_id: organizationId,
      proposed_action: proposedAction,
      context,
    });
    return res.data;
  },
};
