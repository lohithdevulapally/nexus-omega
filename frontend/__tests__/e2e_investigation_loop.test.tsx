import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { InvestigationPipelineFlow } from '@/components/investigations/InvestigationPipelineFlow';
import { AgentInvestigateResponse } from '@/types/investigation';

describe('End-to-End Decision & Reasoning Loop Component', () => {
  it('renders complete 8-agent reasoning pipeline with Hindsight evidence and structured inspectors', async () => {
    const mockInvestigationData: AgentInvestigateResponse = {
      request_id: 'req-acme-8899',
      status: 'completed',
      plan: {
        steps: ['Recall memories', 'Analyze causal links', 'Simulate actions', 'Verify critique'],
      },
      memories: [
        {
          content: 'Incident #3: Switching to Secondary Rail B resolved gateway timeout spikes. Naive restart failed.',
          confidence: 0.95,
        },
      ],
      findings: ["Customer 'ACME Corp' payment failure rate reached 100% threshold."],
      causal_analysis: {
        root_causes: ['Payment Gateway Connection Timeout'],
        symptoms: ['ACME Executive Escalation'],
      },
      risks: {
        severity: 'high',
        threatened_entities: 4,
      },
      decision_candidates: [
        {
          action: 'Switch ACME transaction traffic to Secondary Payment Gateway Rail B',
          rationale_summary: 'Historical evidence demonstrates that once connection retry limit is reached, switching gateway immediately restores payments.',
          expected_outcome: 'Immediate restoration of transaction success rate to >99.9%.',
          historical_support: ['Incident #3 memory'],
          risks: ['Minor transaction fee variance'],
          confidence: 0.96,
          approval_required: true,
        },
      ],
      critique: {
        objections: [],
        verified_safety_guards: ['Verify Secondary Rail B health and certificate validity prior to traffic rerouting'],
      },
      final_recommendation: 'RECOMMENDED ACTION: Switch ACME transaction traffic to Secondary Payment Gateway Rail B.',
      approval_required: true,
      provenance: {
        retained_in_hindsight: true,
      },
      action_id: 'act-998877',
      timeline: [
        { step: 1, agent: 'PlannerAgent', status: 'completed', duration_ms: 11.2 },
        { step: 2, agent: 'MemoryAgent', status: 'completed', duration_ms: 2167.1 },
        { step: 3, agent: 'AnalystAgent', status: 'completed', duration_ms: 4.9 },
        { step: 4, agent: 'CausalAgent', status: 'completed', duration_ms: 9.3 },
        { step: 5, agent: 'DecisionAgent', status: 'completed', duration_ms: 1895.0 },
        { step: 6, agent: 'RiskAgent', status: 'completed', duration_ms: 4.8 },
        { step: 7, agent: 'CriticAgent', status: 'completed', duration_ms: 7.2 },
        { step: 8, agent: 'ReflectionAgent', status: 'completed', duration_ms: 263.3 },
      ],
    };

    render(<InvestigationPipelineFlow data={mockInvestigationData} />);

    // 1. Pipeline Header renders with request ID
    expect(screen.getByText('AUTONOMOUS MULTI-AGENT REASONING PIPELINE')).toBeInTheDocument();
    expect(screen.getByText('req-acme')).toBeInTheDocument();

    // 2. All 8 Specialized Agents are visible in execution topology
    expect(screen.getByText('Planner')).toBeInTheDocument();
    expect(screen.getByText('Memory')).toBeInTheDocument();
    expect(screen.getByText('Analyst')).toBeInTheDocument();
    expect(screen.getByText('Causal')).toBeInTheDocument();
    expect(screen.getByText('Decision')).toBeInTheDocument();
    expect(screen.getByText('Risk')).toBeInTheDocument();
    expect(screen.getByText('Critic')).toBeInTheDocument();
    expect(screen.getByText('Reflection')).toBeInTheDocument();

    // 3. Decision Agent Inspector is initially selected
    expect(screen.getByText(/AGENT INSPECTOR: DecisionAgent/i)).toBeInTheDocument();
    expect(screen.getByText(/Candidate Actions & Counterfactual Simulation Requests/i)).toBeInTheDocument();

    // 4. Click Memory Agent to verify Hindsight evidence inspection
    fireEvent.click(screen.getByText('Memory'));

    await waitFor(() => {
      expect(screen.getByText(/AGENT INSPECTOR: MemoryAgent/i)).toBeInTheDocument();
      expect(screen.getByText(/Hindsight Episodic Memory Recall/i)).toBeInTheDocument();
      expect(screen.getByText(/HINDSIGHT EVIDENCE/i)).toBeInTheDocument();
    });

    // 5. Click Critic Agent to verify adversarial critique & pre-conditions
    fireEvent.click(screen.getByText('Critic'));

    await waitFor(() => {
      expect(screen.getByText(/AGENT INSPECTOR: CriticAgent/i)).toBeInTheDocument();
      expect(screen.getByText(/Adversarial Critique & Pre-condition Verification/i)).toBeInTheDocument();
    });
  });
});
