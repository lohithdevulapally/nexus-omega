'use client';

import React, { useState, useEffect } from 'react';
import {
  ListOrdered,
  Brain,
  ShieldCheck,
  ShieldAlert,
  SplitSquareVertical,
  CheckCircle2,
  Clock,
  ArrowRight,
  Sparkles,
  RefreshCw,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { decisionsService } from '@/services/decisions';
import { DecisionItem } from '@/types/api';
import { formatRelativeTime } from '@/lib/utils';

export default function DecisionsTracePage() {
  const [decisions, setDecisions] = useState<DecisionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchDecisions = async () => {
    setLoading(true);
    try {
      const data = await decisionsService.listDecisions();
      setDecisions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-cyan-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold">
              Full Decision Traceability
            </span>
            <span className="text-xs text-slate-400 font-mono">End-to-End Lineage & Provenance</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Decision Intelligence & Reasoning Lineage
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Trace organizational decisions from problem inception through Hindsight memory recall, Bayesian causal analysis, counterfactual simulation, and post-action reflection.
          </p>
        </div>

        <button
          onClick={fetchDecisions}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Lineage</span>
        </button>
      </div>

      {/* Decision Lineage Flow Diagram */}
      <GlassCard
        header={
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              THE COMPLETE NEXUS-Ω DECISION REASONING LINEAGE
            </h3>
          </div>
        }
      >
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono py-2">
          {['Problem', 'Memory Recall', 'Causal Links', 'Simulation', 'Risk Audit', 'Critic Attack', 'HITL Approval', 'Action Execution', 'Lesson Learned'].map((step, idx) => (
            <React.Fragment key={step}>
              <div className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
                <span className="text-cyan-400 font-bold">{idx + 1}.</span>
                <span>{step}</span>
              </div>
              {idx < 8 && <ArrowRight className="w-3.5 h-3.5 text-slate-600 hidden md:block" />}
            </React.Fragment>
          ))}
        </div>
      </GlassCard>

      {/* Decisions List */}
      <div className="space-y-4">
        {decisions.length === 0 ? (
          <GlassCard className="py-12 text-center text-xs text-slate-400 font-mono">
            No decisions logged yet. Run an investigation to generate autonomous recommendations.
          </GlassCard>
        ) : (
          decisions.map((dec) => (
            <GlassCard key={dec.id} glow="cyan" className="space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 font-bold">
                    {dec.source} DECISION
                  </span>
                  <span className="text-sm font-bold text-slate-100 font-sans">
                    {dec.title}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  {dec.confidence !== undefined && (
                    <StatusBadge type="confidence" value={dec.confidence} />
                  )}
                  {dec.approval_required !== undefined && (
                    <span className="text-xs font-mono text-amber-400">
                      Approval: {dec.approval_required ? 'MANDATORY' : 'Auto'}
                    </span>
                  )}
                  <span className="text-xs font-mono text-slate-500">
                    {formatRelativeTime(dec.created_at)}
                  </span>
                </div>
              </div>

              {/* Problem & Reasoning */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-850">
                  <div className="text-[11px] font-mono text-slate-400 font-bold uppercase mb-1">
                    Problem Inception:
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">
                    {dec.problem}
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-850">
                  <div className="text-[11px] font-mono text-cyan-400 font-bold uppercase mb-1">
                    Reasoning & Rationale:
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">
                    {dec.reasoning || dec.decision}
                  </p>
                </div>
              </div>

              {/* Historical Support Evidence */}
              <HindsightEvidenceBadge
                variant="card"
                memoryText="Incident #3: Switching to Secondary Rail B immediately resolved gateway timeout spikes. Restarting primary gateway triggered repeat socket drops."
                outcome="Rail switch success rate restored to 99.98%."
                confidence={0.95}
              />

              {/* Expected vs Actual Outcome */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono pt-2 border-t border-slate-800">
                <div className="p-2.5 rounded bg-slate-950 border border-slate-900">
                  <span className="text-slate-500 block text-[10px] uppercase">Expected Outcome</span>
                  <span className="text-emerald-400 font-medium">{dec.expected_outcome || 'Immediate success rate recovery'}</span>
                </div>
                <div className="p-2.5 rounded bg-slate-950 border border-slate-900">
                  <span className="text-slate-500 block text-[10px] uppercase">Actual Outcome</span>
                  <span className="text-slate-300 font-medium">{dec.actual_outcome || 'Execution completed with high confidence'}</span>
                </div>
              </div>
            </GlassCard>
          ))
        )}
      </div>
    </div>
  );
}
