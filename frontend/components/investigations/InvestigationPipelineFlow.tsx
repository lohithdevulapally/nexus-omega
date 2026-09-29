'use client';

import React, { useState } from 'react';
import {
  Brain,
  Bot,
  GitBranch,
  SplitSquareVertical,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Sparkles,
  ArrowRight,
  Eye,
  X,
} from 'lucide-react';
import { AgentInvestigateResponse, AgentTimelineStep } from '@/types/investigation';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';

interface InvestigationPipelineFlowProps {
  data: AgentInvestigateResponse;
}

export const InvestigationPipelineFlow: React.FC<InvestigationPipelineFlowProps> = ({ data }) => {
  const [selectedAgent, setSelectedAgent] = useState<string | null>('DecisionAgent');

  const agentConfig: Record<string, { label: string; icon: any; color: string; description: string }> = {
    PlannerAgent: {
      label: 'Planner',
      icon: Bot,
      color: 'border-blue-500/40 text-blue-400 bg-blue-500/10',
      description: 'Deconstructs objective into subtasks and identifies required agent capabilities.',
    },
    MemoryAgent: {
      label: 'Memory',
      icon: Brain,
      color: 'border-purple-500/40 text-purple-400 bg-purple-500/10',
      description: 'Recalls episodic memories from Hindsight bank and detects contradictions.',
    },
    AnalystAgent: {
      label: 'Analyst',
      icon: Sparkles,
      color: 'border-cyan-500/40 text-cyan-400 bg-cyan-500/10',
      description: 'Correlates relational facts with memory patterns and identifies anomalies.',
    },
    CausalAgent: {
      label: 'Causal',
      icon: GitBranch,
      color: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10',
      description: 'Isolates empirical root causes vs symptoms vs contributing factors.',
    },
    DecisionAgent: {
      label: 'Decision',
      icon: CheckCircle2,
      color: 'border-cyan-500/40 text-cyan-300 bg-cyan-500/10',
      description: 'Formulates candidate actions and initiates counterfactual simulations.',
    },
    RiskAgent: {
      label: 'Risk',
      icon: ShieldAlert,
      color: 'border-rose-500/40 text-rose-400 bg-rose-500/10',
      description: 'Evaluates cascade blast radius, contractual SLA risk, and failure traps.',
    },
    CriticAgent: {
      label: 'Critic',
      icon: ShieldCheck,
      color: 'border-amber-500/40 text-amber-400 bg-amber-500/10',
      description: 'Adversarially attacks proposals against historical failure traps.',
    },
    ReflectionAgent: {
      label: 'Reflection',
      icon: Brain,
      color: 'border-purple-500/40 text-purple-300 bg-purple-500/10',
      description: 'Synthesizes lessons learned and retains experiences back into Hindsight.',
    },
  };

  const getAgentDetails = (agentName: string) => {
    switch (agentName) {
      case 'PlannerAgent':
        return {
          title: 'Execution Plan Formulation',
          content: data.plan,
          summary: 'Formulated multi-step execution plan across specialized agents.',
        };
      case 'MemoryAgent':
        return {
          title: 'Hindsight Episodic Memory Recall',
          content: {
            memory_count: data.memories?.length || 0,
            memories: data.memories || [],
          },
          summary: `Retrieved ${data.memories?.length || 0} contextual memories from Hindsight bank 'nexus-demo'.`,
        };
      case 'AnalystAgent':
        return {
          title: 'Relational Correlation & Pattern Synthesis',
          content: data.findings,
          summary: `Identified ${data.findings?.length || 0} relational anomalies and recurrence indicators.`,
        };
      case 'CausalAgent':
        return {
          title: 'Persistent Causal Topology & Root Cause Analysis',
          content: data.causal_analysis,
          summary: 'Grounded causality with Bayesian confidence and counter-evidence weighting.',
        };
      case 'DecisionAgent':
        return {
          title: 'Candidate Actions & Counterfactual Simulation Requests',
          content: data.decision_candidates,
          summary: `Generated ${data.decision_candidates?.length || 0} candidate interventions; flagged approval required.`,
        };
      case 'RiskAgent':
        return {
          title: 'Cascade Threat & SLA Penalty Assessment',
          content: data.risks,
          summary: 'Assessed cascade paths and downstream customer relationship impacts.',
        };
      case 'CriticAgent':
        return {
          title: 'Adversarial Critique & Pre-condition Verification',
          content: data.critique,
          summary: 'Challenged naive restart assumption; verified historical analogue.',
        };
      case 'ReflectionAgent':
        return {
          title: 'Post-Action Synthesis & Hindsight Memory Retention',
          content: data.provenance,
          summary: 'Retained learned principles into Hindsight for future decision guidance.',
        };
      default:
        return { title: agentName, content: {}, summary: '' };
    }
  };

  const timelineMap = (data.timeline || []).reduce<Record<string, AgentTimelineStep>>((acc, step) => {
    acc[step.agent] = step;
    return acc;
  }, {});

  const currentDetails = selectedAgent ? getAgentDetails(selectedAgent) : null;

  return (
    <div className="space-y-6">
      {/* Visual Pipeline Flow Header */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              AUTONOMOUS MULTI-AGENT REASONING PIPELINE
            </h3>
          </div>
          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="text-slate-400">
              Request: <strong className="text-slate-200">{data.request_id.slice(0, 8)}</strong>
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              {data.status.toUpperCase()}
            </span>
          </div>
        </div>

        {/* Pipeline Step Nodes */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {Object.entries(agentConfig).map(([agentName, cfg]) => {
            const Icon = cfg.icon;
            const stepInfo = timelineMap[agentName];
            const isSelected = selectedAgent === agentName;
            const isCompleted = stepInfo?.status === 'completed';

            return (
              <button
                key={agentName}
                onClick={() => setSelectedAgent(agentName)}
                className={`p-3 rounded-lg border text-left transition-all relative flex flex-col justify-between ${
                  isSelected
                    ? 'border-cyan-400 bg-cyan-950/30 shadow-md shadow-cyan-950/50'
                    : 'border-slate-800 bg-slate-950/60 hover:border-slate-700'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <div className={`p-1.5 rounded ${cfg.color}`}>
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    {isCompleted && (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    )}
                  </div>
                  <div className="text-xs font-bold font-sans text-slate-200">
                    {cfg.label}
                  </div>
                </div>

                <div className="mt-2 pt-2 border-t border-slate-900/90 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                  <span>{stepInfo?.duration_ms ? `${stepInfo.duration_ms.toFixed(1)}ms` : 'done'}</span>
                  <Eye className="w-3 h-3 text-slate-500" />
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Structured Agent Output Inspector */}
      {selectedAgent && currentDetails && (
        <div className="p-5 rounded-xl bg-slate-900/95 border border-cyan-500/30 shadow-xl space-y-4">
          <div className="flex items-start justify-between border-b border-slate-800 pb-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono uppercase tracking-wider text-cyan-400 font-semibold">
                  AGENT INSPECTOR: {selectedAgent}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300">
                  {timelineMap[selectedAgent]?.duration_ms?.toFixed(1) || 0}ms execution
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-100 font-sans mt-0.5">
                {currentDetails.title}
              </h4>
            </div>
            <button
              onClick={() => setSelectedAgent(null)}
              className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <p className="text-xs text-slate-300 font-sans">
            {currentDetails.summary}
          </p>

          {/* If MemoryAgent is selected, render Hindsight callouts */}
          {selectedAgent === 'MemoryAgent' && (
            <div className="space-y-3">
              <HindsightEvidenceBadge
                variant="card"
                memoryText="Incident #3: ACME transaction gateway sustained outage. Service restart failed due to socket pool exhaustion. Switching to Secondary Rail B restored payments to 99.98%."
                outcome="Rail B switch succeeded immediately; restart led to customer escalation."
                confidence={0.95}
                relevance={0.96}
                lessonsLearned="Differentiate transient deadlocks from sustained provider degradation."
              />
            </div>
          )}

          {/* Structured Output Viewer */}
          <div className="bg-slate-950 rounded-lg p-4 border border-slate-800 overflow-x-auto max-h-80">
            <pre className="text-xs font-mono text-cyan-300 whitespace-pre-wrap leading-relaxed">
              {JSON.stringify(currentDetails.content, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
