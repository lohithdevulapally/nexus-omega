export interface HealthResponse {
  status: string;
  service?: string;
  database: string;
  redis: string;
  hindsight: string;
  bank_id?: string;
  timestamp?: string;
  latencies?: {
    database_ms?: number | null;
    redis_ms?: number | null;
    hindsight_ms?: number | null;
    total_ms?: number | null;
  };
}

export interface Customer {
  id: string;
  organization_id: string;
  name: string;
  industry?: string;
  status: string;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  metadata?: Record<string, any>;
  created_at: string;
}

export interface EventItem {
  id: string;
  organization_id: string;
  event_type: string;
  entity_type?: string;
  entity_id?: string;
  title: string;
  description?: string;
  timestamp: string;
  source: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface DecisionItem {
  id: string;
  source: 'organization' | 'agent';
  title: string;
  problem: string;
  decision: string;
  reasoning?: string;
  expected_outcome?: string;
  actual_outcome?: string;
  status: string;
  approval_required?: boolean;
  confidence?: number;
  historical_support?: any;
  risks?: any;
  metadata?: Record<string, any>;
  created_at?: string;
}

export interface ActionItem {
  id: string;
  organization_id: string;
  action_type: string;
  payload: Record<string, any>;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  approval_required: boolean;
  approval_status: 'pending' | 'approved' | 'rejected';
  approved_by?: string;
  requested_by?: string;
  status: string;
  execution_status: 'not_started' | 'executing' | 'completed' | 'failed' | 'rejected';
  result?: Record<string, any>;
  created_at?: string;
  completed_at?: string;
}

export interface AgentRunItem {
  id: string;
  agent_name: string;
  task: string;
  status: string;
  duration_ms: number;
  input_data?: any;
  output_data?: any;
  started_at?: string;
  completed_at?: string;
}
