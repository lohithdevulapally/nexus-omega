'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Sparkles,
  Search,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ArrowRight,
  Brain,
  Play,
  RotateCcw,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { InvestigationPipelineFlow } from '@/components/investigations/InvestigationPipelineFlow';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { investigationsService } from '@/services/investigations';
import { actionsService } from '@/services/actions';
import { AgentInvestigateResponse } from '@/types/investigation';

function InvestigationContent() {
  const searchParams = useSearchParams();
  const initialPrompt = searchParams.get('prompt') || 'ACME is experiencing payment failures again.';

  const [prompt, setPrompt] = useState<string>(initialPrompt);
  const [loading, setLoading] = useState<boolean>(false);
  const [investigationData, setInvestigationData] = useState<AgentInvestigateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [approving, setApproving] = useState<boolean>(false);
  const [approvedActionId, setApprovedActionId] = useState<string | null>(null);

  const runInvestigation = async (customPrompt?: string) => {
    const text = customPrompt || prompt;
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await investigationsService.runInvestigation(text);
      setInvestigationData(res);
    } catch (err: any) {
      setError(err.message || 'Investigation execution failed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // If prompt is in query, run automatically
    if (searchParams.get('prompt')) {
      runInvestigation(searchParams.get('prompt')!);
    }
  }, []);

  const handleApprove = async () => {
    if (!investigationData?.action_id) return;
    setApproving(true);
    try {
      await actionsService.approveAction(
        investigationData.action_id,
        'lead_sre_operator',
        'Authorized from Investigation Workspace'
      );
      setApprovedActionId(investigationData.action_id);
    } catch (err: any) {
      alert(`Approval notice: ${err.message}`);
    } finally {
      setApproving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Investigation Prompt Bar */}
      <GlassCard
        glow="cyan"
        header={
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
                AUTONOMOUS INVESTIGATION WORKSPACE
              </h2>
            </div>
            <span className="text-xs font-mono text-slate-500">
              8-Agent Reasoning Graph + Hindsight
            </span>
          </div>
        }
      >
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-cyan-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter incident or operational question (e.g., 'ACME is experiencing payment failures again')..."
                className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-slate-950 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 font-sans shadow-inner"
              />
            </div>
            <button
              onClick={() => runInvestigation()}
              disabled={loading}
              className="px-6 py-2.5 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 text-white font-semibold text-sm flex items-center justify-center gap-2 transition-all shadow-lg shadow-cyan-950/40"
            >
              <Sparkles className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>{loading ? 'INVESTIGATING...' : 'INVESTIGATE'}</span>
            </button>
          </div>

          {/* Quick presets */}
          <div className="flex items-center gap-2 pt-1 text-xs text-slate-400 font-mono">
            <span>Presets:</span>
            <button
              onClick={() => {
                setPrompt('ACME is experiencing payment failures again.');
                runInvestigation('ACME is experiencing payment failures again.');
              }}
              className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 transition-colors"
            >
              ACME Payment Timeout
            </button>
            <button
              onClick={() => {
                setPrompt('Why did the previous gateway restart attempt fail?');
                runInvestigation('Why did the previous gateway restart attempt fail?');
              }}
              className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-purple-300 border border-slate-700 transition-colors"
            >
              Restart Failure Analysis
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Error Banner */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-sm font-sans flex items-center gap-3">
          <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Investigation Results */}
      {investigationData && (
        <div className="space-y-6">
          {/* Agent Pipeline Flow */}
          <InvestigationPipelineFlow data={investigationData} />

          {/* Final Recommendation Card */}
          <GlassCard
            glow="emerald"
            header={
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
                    FINAL OPERATIONAL RECOMMENDATION & ACTION GATE
                  </h3>
                </div>
                {investigationData.approval_required && (
                  <span className="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    HUMAN APPROVAL MANDATED
                  </span>
                )}
              </div>
            }
          >
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-slate-950/80 border border-slate-800">
                <pre className="text-sm font-sans text-slate-200 whitespace-pre-wrap leading-relaxed">
                  {investigationData.final_recommendation}
                </pre>
              </div>

              {/* Action Registration Callout */}
              {investigationData.action_id && (
                <div className="p-4 rounded-lg bg-slate-950/70 border border-cyan-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <div className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider">
                      CONTROLLED ACTION REGISTERED
                    </div>
                    <div className="text-xs font-mono text-slate-400 mt-1">
                      Action ID: <strong className="text-slate-200">{investigationData.action_id}</strong>
                    </div>
                    <div className="text-xs text-slate-400 mt-0.5">
                      Status: {approvedActionId ? 'APPROVED by Human Operator' : 'Awaiting Human-in-the-Loop review'}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {approvedActionId ? (
                      <span className="px-4 py-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-semibold flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" />
                        AUTHORIZED
                      </span>
                    ) : (
                      <button
                        onClick={handleApprove}
                        disabled={approving}
                        className="px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs font-sans flex items-center gap-1.5 transition-all shadow-md shadow-emerald-950/40"
                      >
                        <ShieldCheck className="w-4 h-4" />
                        <span>{approving ? 'APPROVING...' : 'APPROVE ACTION NOW'}</span>
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>
          </GlassCard>
        </div>
      )}
    </div>
  );
}

export default function InvestigationsPage() {
  return (
    <React.Suspense fallback={<div className="p-8 text-xs font-mono text-slate-400">Loading Investigation Console...</div>}>
      <InvestigationContent />
    </React.Suspense>
  );
}
