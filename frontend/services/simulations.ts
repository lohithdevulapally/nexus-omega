import { apiClient, DEFAULT_ORG_ID } from './api';
import {
  CounterfactualResponse,
  MultiScenarioComparison,
  ReconstructResponse,
  ScenarioOptionEvaluation,
} from '@/types/simulation';

export function normalizeMultiScenarioComparison(
  raw: any,
  fallbackContext: string = 'ACME payment gateway timeout resolution'
): MultiScenarioComparison {
  if (!raw || typeof raw !== 'object') {
    return {
      decision_context: fallbackContext,
      options_evaluated: [],
      evaluations: [],
      generated_at: new Date().toISOString(),
    };
  }

  // Handle both evaluations and options_evaluated from backend
  const rawList = Array.isArray(raw.evaluations)
    ? raw.evaluations
    : Array.isArray(raw.options_evaluated)
    ? raw.options_evaluated
    : [];

  const evaluations: ScenarioOptionEvaluation[] = rawList.map((item: any) => {
    if (!item || typeof item !== 'object') {
      const name = String(item || 'Unknown Option');
      return {
        action: name,
        option: name,
        assumptions: [],
        projected_outcome: 'No outcome projected',
        projected_outcomes: [],
        risk_propagation: [],
        risk_severity: 'MEDIUM',
        historical_evidence: [],
        uncertainty: [],
        reversibility: 'medium',
        required_approval: false,
        affected_entities: [],
        confidence: 0.85,
      };
    }

    const action = item.action || item.option || 'Candidate Intervention';
    const option = item.option || item.action || 'Candidate Intervention';

    // Extract projected outcome
    let projected_outcome = 'Projected operational recovery';
    if (typeof item.projected_outcome === 'string' && item.projected_outcome.trim()) {
      projected_outcome = item.projected_outcome;
    } else if (Array.isArray(item.projected_outcomes) && item.projected_outcomes.length > 0) {
      projected_outcome = String(item.projected_outcomes[0]);
    }

    // Extract risk severity
    let risk_severity = 'MEDIUM';
    if (typeof item.risk_severity === 'string' && item.risk_severity.trim()) {
      risk_severity = item.risk_severity.toUpperCase();
    } else if (Array.isArray(item.risk_propagation) && item.risk_propagation.length > 0) {
      const firstRisk = item.risk_propagation[0];
      if (typeof firstRisk === 'object' && firstRisk?.severity) {
        risk_severity = String(firstRisk.severity).toUpperCase();
      } else if (typeof firstRisk === 'string') {
        risk_severity = firstRisk.toUpperCase();
      }
    }

    return {
      action,
      option,
      assumptions: Array.isArray(item.assumptions) ? item.assumptions : [],
      projected_outcome,
      projected_outcomes: Array.isArray(item.projected_outcomes) ? item.projected_outcomes : [projected_outcome],
      risk_propagation: Array.isArray(item.risk_propagation) ? item.risk_propagation : [],
      risk_severity,
      historical_evidence: Array.isArray(item.historical_evidence) ? item.historical_evidence : [],
      uncertainty: Array.isArray(item.uncertainty) ? item.uncertainty : [],
      reversibility: item.reversibility || 'medium',
      required_approval: typeof item.required_approval === 'boolean' ? item.required_approval : false,
      affected_entities: Array.isArray(item.affected_entities) ? item.affected_entities : [],
      confidence: typeof item.confidence === 'number' ? item.confidence : 0.85,
    };
  });

  return {
    comparison_id: raw.comparison_id,
    organization_id: raw.organization_id || DEFAULT_ORG_ID,
    decision_context: raw.decision_context || fallbackContext,
    timestamp: raw.timestamp || new Date().toISOString(),
    options_evaluated: Array.isArray(raw.options_evaluated) ? raw.options_evaluated : evaluations.map(e => e.action),
    evaluations,
    comparative_synthesis: raw.comparative_synthesis,
    recommended_evaluation: raw.recommended_evaluation,
    generated_at: raw.timestamp || new Date().toISOString(),
  };
}

export const simulationService = {
  async runCounterfactual(
    alternativeAction: string = 'Restart Payment Gateway A',
    incidentId?: string,
    baselineAction?: string,
    organizationId: string = DEFAULT_ORG_ID
  ): Promise<CounterfactualResponse> {
    const res = await apiClient.post<CounterfactualResponse>('/simulation/counterfactual', {
      organization_id: organizationId,
      alternative_action: alternativeAction,
      incident_id: incidentId,
      baseline_action: baselineAction,
    });
    return res.data;
  },

  async compareScenarios(
    options: string[],
    decisionContext: string = 'ACME payment gateway timeout resolution',
    organizationId: string = DEFAULT_ORG_ID
  ): Promise<MultiScenarioComparison> {
    const res = await apiClient.post<any>('/simulation/compare', {
      organization_id: organizationId,
      decision_context: decisionContext,
      options,
    });
    return normalizeMultiScenarioComparison(res.data, decisionContext);
  },

  async reconstructState(
    timestamp: string,
    organizationId: string = DEFAULT_ORG_ID
  ): Promise<ReconstructResponse> {
    const res = await apiClient.post<ReconstructResponse>('/simulation/reconstruct', {
      organization_id: organizationId,
      timestamp,
    });
    return res.data;
  },
};
