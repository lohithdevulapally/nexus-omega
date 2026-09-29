export interface CausalNode {
  id: string;
  organization_id: string;
  entity_type: string;
  entity_id?: string;
  label: string;
  description?: string;
  metadata?: Record<string, any>;
  created_at?: string;
}

export interface CausalEdge {
  id: string;
  organization_id: string;
  source_node_id: string;
  target_node_id: string;
  relationship: string;
  confidence: number;
  evidence?: {
    supporting_events?: string[];
    supporting_memories?: string[];
    counter_evidence?: string[];
    rationale?: string;
  };
  source_type: string;
  created_at?: string;
}

export interface CausalGraphData {
  nodes: CausalNode[];
  edges: CausalEdge[];
}

export interface RootCauseFactor {
  node_id: string;
  label: string;
  entity_type: string;
  relationship: string;
  confidence: number;
  evidence: any;
  depth: number;
}

export interface RootCauseResponse {
  incident: string;
  immediate_cause?: string;
  root_causes: RootCauseFactor[];
  contributing_factors: RootCauseFactor[];
  upstream_causes: RootCauseFactor[];
  downstream_effects: RootCauseFactor[];
  symptoms: RootCauseFactor[];
  unresolved_hypotheses: string[];
  confidence: number;
}

export interface CausalPathStep {
  from_node: string;
  to_node: string;
  relationship: string;
  confidence: number;
}

export interface CausalPathResult {
  path: string[];
  relationships: string[];
  length: number;
  cumulative_confidence: number;
  steps: CausalPathStep[];
  supporting_memories: string[];
}

export interface CausalPathResponse {
  source: string;
  target: string;
  paths: CausalPathResult[];
  strongest_path?: CausalPathResult;
}

export interface CascadeStep {
  from_node: string;
  to_node: string;
  relationship: string;
  distance: number;
}

export interface CascadeResponse {
  trigger: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  cascade_paths: CascadeStep[];
  affected_entities: string[];
  total_downstream_entities: number;
  evidence?: Record<string, any>;
}
