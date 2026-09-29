export interface AgentTimelineStep {
  step: number;
  agent: string;
  status: 'completed' | 'running' | 'failed' | 'pending';
  duration_ms: number;
  summary?: string;
  memories_used?: number;
}

export interface DecisionCandidate {
  action: string;
  rationale_summary: string;
  expected_outcome: string;
  historical_support: string[];
  risks: string[];
  confidence: number;
  approval_required: boolean;
}

export interface AgentInvestigateResponse {
  request_id: string;
  status: string;
  plan: Record<string, any>;
  memories: any[];
  findings: string[];
  causal_analysis: Record<string, any>;
  risks: Record<string, any>;
  decision_candidates: DecisionCandidate[];
  critique: Record<string, any>;
  final_recommendation: string;
  approval_required: boolean;
  provenance: Record<string, any>;
  simulation?: Record<string, any>;
  action_id?: string;
  action_request?: Record<string, any>;
  timeline: AgentTimelineStep[];
}
