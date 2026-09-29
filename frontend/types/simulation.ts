export interface SimulationWorld {
  action: string;
  projected_outcome: string;
  expected_effects: string[];
  risks: string[];
  downstream_impacts: string[];
  supporting_evidence: string[];
  uncertainty: string[];
  confidence: number;
  simulation_id: string;
}

export interface CounterfactualResponse {
  scenario_id: string;
  actual_world: SimulationWorld;
  counterfactual_world: SimulationWorld;
  differences: string[];
  new_risks: string[];
  mitigated_risks: string[];
  causal_paths: string[];
  historical_evidence: string[];
  assumptions: string[];
  uncertainty: string[];
  confidence: number;
}

export interface ScenarioOptionEvaluation {
  action: string;
  option?: string;
  assumptions: string[];
  projected_outcome: string;
  projected_outcomes?: string[];
  risk_propagation: any[];
  risk_severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  historical_evidence: string[];
  uncertainty: string[];
  reversibility: 'high' | 'medium' | 'low' | string;
  required_approval: boolean;
  affected_entities: string[];
  confidence: number;
}

export interface MultiScenarioComparison {
  comparison_id?: string;
  organization_id?: string;
  decision_context: string;
  timestamp?: string;
  options_evaluated: any[];
  evaluations: ScenarioOptionEvaluation[];
  comparative_synthesis?: string;
  recommended_evaluation?: ScenarioOptionEvaluation;
  generated_at?: string;
}

export interface ReconstructResponse {
  organization_id: string;
  timestamp: string;
  customers: any[];
  events: any[];
  decisions: any[];
  actions: any[];
  experiences: any[];
  known_risks: string[];
  memories: any[];
}
