/**
 * Evaluation and Benchmarking API Service.
 */

import { apiClient } from './api';

export interface MemoryAblationResult {
  scenario_id: string;
  scenario_name: string;
  category: string;
  current_incident: string;
  without_memory: {
    mode: string;
    evidence_retrieved_count: number;
    historical_precedents_used: string[];
    repeated_mistake_detected: boolean;
    repeated_mistake_prevented: boolean;
    identified_risks: string[];
    causal_assessment: {
      root_cause_identified: string;
      grounded_in_precedent: boolean;
      confidence: number;
    };
    contradiction_detected: boolean;
    counterfactual_simulation: {
      tested_alternatives: string[];
      projected_recurrence_risk: string;
      grounded_in_history: boolean;
    };
    recommendation: string;
    recommendation_rationale: string;
    critic_objections: string[];
    calibrated_confidence: number;
    unsupported_assumptions: string[];
    lessons_utilized_count: number;
  };
  with_memory: {
    mode: string;
    evidence_retrieved_count: number;
    historical_precedents_used: string[];
    repeated_mistake_detected: boolean;
    repeated_mistake_prevented: boolean;
    identified_risks: string[];
    causal_assessment: {
      root_cause_identified: string;
      grounded_in_precedent: boolean;
      confidence: number;
    };
    contradiction_detected: boolean;
    counterfactual_simulation: {
      tested_alternatives: string[];
      projected_recurrence_risk: string;
      grounded_in_history: boolean;
    };
    recommendation: string;
    recommendation_rationale: string;
    critic_objections: string[];
    calibrated_confidence: number;
    unsupported_assumptions: string[];
    lessons_utilized_count: number;
  };
  differences: Array<{
    dimension: string;
    without_memory: string;
    with_memory: string;
    impact: string;
  }>;
  memory_influence: {
    score: number;
    level: string;
    evidence: Record<string, any>;
    explanation: string;
  };
  metrics: {
    decision_shift: boolean;
    mistake_prevented: boolean;
    confidence_gain_pct: number;
    evidence_coverage_pct: number;
    unsupported_claims_reduction_pct: number;
  };
}

export interface BenchmarkSuiteResult {
  summary: {
    total_scenarios_evaluated: number;
    decision_shifts_with_memory: number;
    historical_mistakes_prevented: number;
    mistake_prevention_rate_pct: number;
    average_memory_influence_score: number;
    contradiction_handling_verified: boolean;
    context_discrimination_verified: boolean;
  };
  scenarios: Array<{
    scenario_id: string;
    name: string;
    category: string;
    decision_without_memory: string;
    decision_with_memory: string;
    mistake_prevented: boolean;
    influence_score: number;
    confidence_gain_pct: number;
    is_contradictory: boolean;
  }>;
  memory_quality: Record<string, any>;
  causal_metrics: Record<string, any>;
  counterfactual_metrics: Record<string, any>;
  safety_metrics: Record<string, any>;
}

export const evaluationService = {
  async runMemoryAblation(scenarioId: string, organizationId?: string): Promise<MemoryAblationResult> {
    const res = await apiClient.post<MemoryAblationResult>('/evaluation/memory-ablation', {
      scenario_id: scenarioId,
      organization_id: organizationId,
    });
    return res.data;
  },

  async runAllBenchmarks(): Promise<BenchmarkSuiteResult> {
    const res = await apiClient.post<BenchmarkSuiteResult>('/evaluation/run-benchmarks');
    return res.data;
  },

  async getPerformanceBenchmarks(): Promise<Record<string, any>> {
    const res = await apiClient.get<Record<string, any>>('/evaluation/performance');
    return res.data;
  },

  async getMemoryMetrics(): Promise<Record<string, any>> {
    const res = await apiClient.get<Record<string, any>>('/evaluation/memory-metrics');
    return res.data;
  },

  async injectChaos(scenarioId: string): Promise<Record<string, any>> {
    const res = await apiClient.post<Record<string, any>>('/evaluation/chaos/inject', {
      scenario_id: scenarioId,
    });
    return res.data;
  },

  async runChaosTest(scenarioId: string): Promise<Record<string, any>> {
    const res = await apiClient.post<Record<string, any>>('/evaluation/chaos/run', {
      scenario_id: scenarioId,
    });
    return res.data;
  },

  async resetDemo(): Promise<Record<string, any>> {
    const res = await apiClient.post<Record<string, any>>('/demo/reset');
    return res.data;
  },

  async getAuditLogs(limit: number = 30): Promise<Array<Record<string, any>>> {
    const res = await apiClient.get<Array<Record<string, any>>>(`/audit?limit=${limit}`);
    return res.data;
  },
};
