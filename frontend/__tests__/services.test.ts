import { describe, it, expect, vi, beforeEach } from 'vitest';
import { systemService } from '@/services/system';
import { investigationsService } from '@/services/investigations';
import { memoryService } from '@/services/memory';
import { causalService } from '@/services/causal';
import { simulationService, normalizeMultiScenarioComparison } from '@/services/simulations';
import { actionsService } from '@/services/actions';
import { evaluationService } from '@/services/evaluation';
import { apiClient } from '@/services/api';

vi.mock('@/services/api', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
  DEFAULT_ORG_ID: '2d48f08c-0b35-4aea-8941-86e4f855f738',
  DEFAULT_ORG_NAME: 'NEXUS Demo Corporation',
}));

describe('Frontend API Services', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('systemService.getHealth returns backend health payload', async () => {
    const mockHealth = {
      status: 'ok',
      database: 'connected',
      redis: 'connected',
      hindsight: 'connected',
      bank_id: 'nexus-demo',
    };
    (apiClient.get as any).mockResolvedValueOnce({ data: mockHealth });

    const result = await systemService.getHealth();
    expect(result.status).toBe('ok');
    expect(result.database).toBe('connected');
    expect(result.hindsight).toBe('connected');
  });

  it('investigationsService.runInvestigation executes multi-agent graph', async () => {
    const mockInvestigation = {
      request_id: 'req-123',
      status: 'completed',
      final_recommendation: 'Switch to Rail B',
      approval_required: true,
      timeline: [],
    };
    (apiClient.post as any).mockResolvedValueOnce({ data: mockInvestigation });

    const result = await investigationsService.runInvestigation('ACME failure');
    expect(result.status).toBe('completed');
    expect(result.final_recommendation).toContain('Rail B');
    expect(result.approval_required).toBe(true);
  });

  it('memoryService.searchMemories searches Hindsight bank', async () => {
    const mockSearch = {
      bank_id: 'nexus-demo',
      query: 'timeout',
      count: 2,
      memories: [{ content: 'Incident #3 resolved by Rail B' }],
    };
    (apiClient.get as any).mockResolvedValueOnce({ data: mockSearch });

    const result = await memoryService.searchMemories('timeout');
    expect(result.count).toBe(2);
    expect(result.memories[0].content).toContain('Rail B');
  });

  it('causalService.getGraph retrieves persistent graph topology', async () => {
    const mockGraph = {
      nodes: [{ id: 'n1', label: 'Payment Gateway Timeout', entity_type: 'event' }],
      edges: [{ id: 'e1', source_node_id: 'n1', target_node_id: 'n2', relationship: 'CAUSES' }],
    };
    (apiClient.get as any).mockResolvedValueOnce({ data: mockGraph });

    const result = await causalService.getGraph();
    expect(result.nodes.length).toBe(1);
    expect(result.edges[0].relationship).toBe('CAUSES');
  });

  it('simulationService.runCounterfactual simulates dual-world comparison', async () => {
    const mockCounterfactual = {
      scenario_id: 'sc-1',
      actual_world: { action: 'Switch to Rail B', confidence: 0.95 },
      counterfactual_world: { action: 'Restart Gateway', confidence: 0.92 },
      differences: ['Divergence in recovery time'],
    };
    (apiClient.post as any).mockResolvedValueOnce({ data: mockCounterfactual });

    const result = await simulationService.runCounterfactual('Restart Gateway');
    expect(result.actual_world.action).toBe('Switch to Rail B');
    expect(result.counterfactual_world.action).toBe('Restart Gateway');
  });

  it('actionsService handles submit, approve, and execute', async () => {
    const mockAction = {
      id: 'act-1',
      action_type: 'create_internal_event',
      approval_status: 'pending',
      execution_status: 'not_started',
    };
    (apiClient.get as any).mockResolvedValueOnce({ data: [mockAction] });
    const list = await actionsService.listActions();
    expect(list.length).toBe(1);

    (apiClient.post as any).mockResolvedValueOnce({
      data: { ...mockAction, approval_status: 'approved' },
    });
    const approved = await actionsService.approveAction('act-1');
    expect(approved.approval_status).toBe('approved');

    (apiClient.post as any).mockResolvedValueOnce({
      data: { ...mockAction, approval_status: 'approved', execution_status: 'completed' },
    });
    const executed = await actionsService.executeAction('act-1');
    expect(executed.execution_status).toBe('completed');
  });

  it('evaluationService runs memory ablation and benchmark suites', async () => {
    const mockAblation = {
      scenario_id: 'scenario-01-payment-failure',
      without_memory: { recommendation: 'restart_gateway' },
      with_memory: { recommendation: 'switch_secondary_rail_b' },
      memory_influence: { score: 0.85, level: 'DECISIVE' },
      metrics: { mistake_prevented: true },
    };
    (apiClient.post as any).mockResolvedValueOnce({ data: mockAblation });

    const ablation = await evaluationService.runMemoryAblation('scenario-01-payment-failure');
    expect(ablation.without_memory.recommendation).toBe('restart_gateway');
    expect(ablation.with_memory.recommendation).toBe('switch_secondary_rail_b');
    expect(ablation.metrics.mistake_prevented).toBe(true);

    const mockReset = { status: 'reset_successful', message: 'Demo reset' };
    (apiClient.post as any).mockResolvedValueOnce({ data: mockReset });
    const reset = await evaluationService.resetDemo();
    expect(reset.status).toBe('reset_successful');
  });

  it('normalizeMultiScenarioComparison safely handles raw backend response with options_evaluated', () => {
    const rawBackendData = {
      comparison_id: 'cmp-1234',
      decision_context: 'Payment gateway timeout',
      timestamp: '2026-09-28T16:00:00Z',
      options_evaluated: [
        {
          option: 'Switch to Secondary Rail',
          projected_outcomes: ['Restores success rate to 99.98%'],
          risk_propagation: [{ severity: 'low', description: 'Minimal latency' }],
          reversibility: 'medium',
          required_approval: true,
          confidence: 0.95,
        },
        {
          option: 'Restart Service',
          projected_outcomes: ['Fails due to socket exhaustion'],
          risk_propagation: [{ severity: 'high', description: 'Cascading outage' }],
          reversibility: 'low',
          required_approval: true,
          confidence: 0.91,
        },
      ],
      comparative_synthesis: 'Switching rails is optimal.',
    };

    const normalized = normalizeMultiScenarioComparison(rawBackendData);
    expect(Array.isArray(normalized.evaluations)).toBe(true);
    expect(normalized.evaluations.length).toBe(2);
    expect(normalized.evaluations[0].action).toBe('Switch to Secondary Rail');
    expect(normalized.evaluations[0].projected_outcome).toBe('Restores success rate to 99.98%');
    expect(normalized.evaluations[0].risk_severity).toBe('LOW');
    expect(normalized.evaluations[1].risk_severity).toBe('HIGH');
  });

  it('normalizeMultiScenarioComparison gracefully handles null, undefined, or empty objects', () => {
    const fromNull = normalizeMultiScenarioComparison(null);
    expect(Array.isArray(fromNull.evaluations)).toBe(true);
    expect(fromNull.evaluations.length).toBe(0);

    const fromEmpty = normalizeMultiScenarioComparison({});
    expect(Array.isArray(fromEmpty.evaluations)).toBe(true);
    expect(fromEmpty.evaluations.length).toBe(0);

    const fromZeroOptions = normalizeMultiScenarioComparison({ options_evaluated: [] });
    expect(Array.isArray(fromZeroOptions.evaluations)).toBe(true);
    expect(fromZeroOptions.evaluations.length).toBe(0);
  });

  it('simulationService.compareScenarios returns normalized MultiScenarioComparison', async () => {
    const rawBackendData = {
      comparison_id: 'cmp-5678',
      decision_context: 'DB latency spike',
      timestamp: '2026-09-28T16:10:00Z',
      options_evaluated: [
        {
          option: 'Divert Analytics',
          projected_outcomes: ['Latency drops to 18ms'],
          risk_propagation: [{ severity: 'low' }],
          reversibility: 'high',
          confidence: 0.96,
        },
      ],
    };
    (apiClient.post as any).mockResolvedValueOnce({ data: rawBackendData });

    const result = await simulationService.compareScenarios(['Divert Analytics']);
    expect(result.evaluations.length).toBe(1);
    expect(result.evaluations[0].action).toBe('Divert Analytics');
    expect(result.evaluations[0].projected_outcome).toBe('Latency drops to 18ms');
    expect(result.evaluations[0].risk_severity).toBe('LOW');
  });
});
