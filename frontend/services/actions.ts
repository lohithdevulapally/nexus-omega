import { apiClient, DEFAULT_ORG_ID } from './api';
import { ActionItem } from '@/types/api';

export const actionsService = {
  async listActions(
    organizationId: string = DEFAULT_ORG_ID,
    status?: string,
    approvalStatus?: string,
    limit: number = 50
  ): Promise<ActionItem[]> {
    const res = await apiClient.get<ActionItem[]>('/actions', {
      params: {
        organization_id: organizationId,
        status,
        approval_status: approvalStatus,
        limit,
      },
    });
    return res.data;
  },

  async getAction(actionId: string): Promise<ActionItem> {
    const res = await apiClient.get<ActionItem>(`/actions/${actionId}`);
    return res.data;
  },

  async submitAction(
    actionType: string,
    parameters: Record<string, any>,
    requestedBy: string = 'operator',
    agentId?: string,
    decisionId?: string,
    autoExecuteLowRisk: boolean = false,
    organizationId: string = DEFAULT_ORG_ID
  ): Promise<ActionItem> {
    const res = await apiClient.post<ActionItem>('/actions', {
      organization_id: organizationId,
      action_type: actionType,
      parameters,
      requested_by: requestedBy,
      agent_id: agentId,
      decision_id: decisionId,
      auto_execute_low_risk: autoExecuteLowRisk,
    });
    return res.data;
  },

  async approveAction(
    actionId: string,
    approvedBy: string = 'human_reviewer',
    comment?: string
  ): Promise<ActionItem> {
    const res = await apiClient.post<ActionItem>(`/actions/${actionId}/approve`, {
      approved_by: approvedBy,
      comment,
    });
    return res.data;
  },

  async rejectAction(
    actionId: string,
    rejectedBy: string = 'human_reviewer',
    reason: string = 'Operational risk threshold exceeded'
  ): Promise<ActionItem> {
    const res = await apiClient.post<ActionItem>(`/actions/${actionId}/reject`, {
      rejected_by: rejectedBy,
      reason,
    });
    return res.data;
  },

  async executeAction(
    actionId: string,
    executedBy: string = 'human_reviewer'
  ): Promise<ActionItem> {
    const res = await apiClient.post<ActionItem>(`/actions/${actionId}/execute`, {
      executed_by: executedBy,
    });
    return res.data;
  },
};
