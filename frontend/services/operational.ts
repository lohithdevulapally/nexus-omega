import { apiClient, DEFAULT_ORG_ID } from './api';
import { Customer, EventItem } from '@/types/api';

export const operationalService = {
  async listCustomers(organizationId: string = DEFAULT_ORG_ID): Promise<Customer[]> {
    const res = await apiClient.get<Customer[]>('/customers', {
      params: { organization_id: organizationId },
    });
    return res.data;
  },

  async listEvents(organizationId: string = DEFAULT_ORG_ID, limit: number = 50): Promise<EventItem[]> {
    const res = await apiClient.get<EventItem[]>('/events', {
      params: { organization_id: organizationId, limit },
    });
    return res.data;
  },
};
