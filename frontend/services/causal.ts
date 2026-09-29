import { apiClient, DEFAULT_ORG_ID } from './api';
import { CausalGraphData, RootCauseResponse, CausalPathResponse, CascadeResponse } from '@/types/causal';

export const causalService = {
  async getGraph(organizationId: string = DEFAULT_ORG_ID): Promise<CausalGraphData> {
    const res = await apiClient.get<CausalGraphData>('/causal/graph', {
      params: { organization_id: organizationId },
    });
    return res.data;
  },

  async analyzeRootCause(
    incidentId: string = 'ACME Transaction Failures',
    organizationId: string = DEFAULT_ORG_ID,
    depth: number = 5
  ): Promise<RootCauseResponse> {
    const res = await apiClient.post<RootCauseResponse>('/causal/root-cause', {
      organization_id: organizationId,
      incident_id: incidentId,
      depth,
    });
    return res.data;
  },

  async getCausalPath(
    source: string,
    target: string,
    organizationId: string = DEFAULT_ORG_ID,
    depth: number = 5
  ): Promise<CausalPathResponse> {
    const res = await apiClient.get<CausalPathResponse>('/causal/path', {
      params: { source, target, organization_id: organizationId, depth },
    });
    return res.data;
  },

  async analyzeCascade(
    trigger: string = 'Payment Gateway Connection Timeout',
    organizationId: string = DEFAULT_ORG_ID,
    depth: number = 5
  ): Promise<CascadeResponse> {
    const res = await apiClient.post<CascadeResponse>('/causal/cascade', {
      organization_id: organizationId,
      trigger,
      depth,
    });
    return res.data;
  },
};
