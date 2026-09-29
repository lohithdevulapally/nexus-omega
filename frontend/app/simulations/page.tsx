'use client';

import React, { useState, useEffect } from 'react';
import {
  SplitSquareVertical,
  ArrowRight,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Brain,
  HelpCircle,
  Clock,
  Sparkles,
  Layers,
  RefreshCw,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { simulationService } from '@/services/simulations';
import { CounterfactualResponse, MultiScenarioComparison, ScenarioOptionEvaluation } from '@/types/simulation';

export default function SimulationsCockpitPage() {
  const [alternativeAction, setAlternativeAction] = useState<string>('Restart Payment Gateway A');
  const [counterfactualData, setCounterfactualData] = useState<CounterfactualResponse | null>(null);
  const [multiScenarioData, setMultiScenarioData] = useState<MultiScenarioComparison | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const runSimulation = async () => {
    setLoading(true);
    setError(null);
    try {
      const [cf, comp] = await Promise.allSettled([
        simulationService.runCounterfactual(alternativeAction),
        simulationService.compareScenarios([
          'Switch to Secondary Payment Gateway Rail B',
          'Restart Payment Gateway Service',
          'Wait and Monitor for Organic Recovery',
        ]),
      ]);

      let hasSuccess = false;
      if (cf.status === 'fulfilled') {
        setCounterfactualData(cf.value);
        hasSuccess = true;
      }
      if (comp.status === 'fulfilled') {
        setMultiScenarioData(comp.value);
        hasSuccess = true;
      }

      if (!hasSuccess) {
        const errorReason = cf.status === 'rejected' ? (cf.reason?.message || 'Counterfactual failed') : 'Simulation failed';
        setError(errorReason);
      }
    } catch (err: any) {
      console.error('Simulation execution error:', err);
      setError(err?.message || 'Unexpected simulation engine failure.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, []);

  const evaluations = multiScenarioData?.evaluations || [];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-amber-950/40 to-slate-900 border border-amber-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">
              Isolated Counterfactual Engine
            </span>
            <span className="text-xs text-slate-400 font-mono">SIMULATION_ONLY • Non-Destructive State</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            What-If Counterfactual Cockpit & Multi-Scenario Comparison
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Compare the Actual World against simulated alternative interventions. Fuses historical Hindsight analogues with causal graph propagation.
          </p>
        </div>

        <button
          onClick={runSimulation}
          disabled={loading}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'Simulating...' : 'Rerun Simulation'}</span>
        </button>
      </div>

      {/* Epistemological Distinction Badges */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold">
            OBSERVED
          </span>
          <span className="text-slate-400 text-[11px]">Empirical telemetry facts</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30 font-bold">
            HISTORICAL
          </span>
          <span className="text-slate-400 text-[11px]">Hindsight past analogues</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 font-bold">
            ASSUMPTION
          </span>
          <span className="text-slate-400 text-[11px]">Explicit model conditions</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-bold">
            PROJECTED
          </span>
          <span className="text-slate-400 text-[11px]">Simulated outcome space</span>
        </div>
      </div>

      {/* ERROR STATE */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 text-xs font-mono space-y-2">
          <div className="flex items-center gap-2 text-rose-300 font-bold text-sm">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            SIMULATION ENGINE NOTICE
          </div>
          <div className="text-slate-300">
            <strong className="text-rose-400">Error:</strong> {error}
          </div>
          <div className="text-slate-400">
            Ensure backend service is running at <code>http://localhost:8000</code>.
          </div>
          <button
            onClick={runSimulation}
            className="mt-2 px-3 py-1.5 rounded bg-rose-900/60 hover:bg-rose-800 text-white font-bold text-xs"
          >
            Retry Simulation
          </button>
        </div>
      )}

      {/* LOADING INDICATOR */}
      {loading && !counterfactualData && (
        <GlassCard className="py-12 text-center space-y-3">
          <RefreshCw className="w-8 h-8 text-amber-400 mx-auto animate-spin" />
          <h3 className="text-sm font-mono font-bold text-slate-200">
            Evaluating Counterfactual Worlds in Isolated Sandbox...
          </h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Forking state snapshot, loading Hindsight analogues, and projecting recovery curves across alternative interventions.
          </p>
        </GlassCard>
      )}

      {/* DUAL-WORLD SPLIT VIEW */}
      {counterfactualData && (
        <div className="space-y-4">
          <div className="text-xs font-mono font-bold uppercase text-slate-400 tracking-wider">
            DUAL-WORLD WHAT-IF COMPARISON
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* ACTUAL WORLD */}
            <GlassCard
              glow="emerald"
              header={
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                    <h3 className="text-sm font-bold font-mono text-emerald-400 uppercase tracking-wider">
                      ACTUAL WORLD (BASELINE INTERVENTION)
                    </h3>
                  </div>
                  <StatusBadge type="confidence" value={counterfactualData.actual_world.confidence} />
                </div>
              }
            >
              <div className="space-y-3">
                <div className="p-3.5 rounded-lg bg-slate-950/80 border border-emerald-500/30">
                  <div className="text-[11px] font-mono text-slate-400 font-bold uppercase mb-1">
                    ACTION SELECTED:
                  </div>
                  <h4 className="text-sm font-bold text-slate-100 font-sans">
                    {counterfactualData.actual_world.action}
                  </h4>
                </div>

                <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-900/30 text-xs text-emerald-300">
                  <span className="font-mono font-bold text-emerald-400 uppercase block mb-1">
                    [PROJECTED OUTCOME]:
                  </span>
                  {counterfactualData.actual_world.projected_outcome}
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <div className="font-mono text-slate-400 text-[11px] font-bold uppercase">
                    Expected Effects:
                  </div>
                  <ul className="list-disc pl-4 text-slate-300 space-y-1">
                    {counterfactualData.actual_world.expected_effects?.map((eff, i) => (
                      <li key={i}>{eff}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </GlassCard>

            {/* COUNTERFACTUAL WORLD */}
            <GlassCard
              glow="rose"
              header={
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-rose-400 animate-pulse" />
                    <h3 className="text-sm font-bold font-mono text-rose-400 uppercase tracking-wider">
                      COUNTERFACTUAL WORLD (WHAT-IF ALTERNATIVE)
                    </h3>
                  </div>
                  <StatusBadge type="confidence" value={counterfactualData.counterfactual_world.confidence} />
                </div>
              }
            >
              <div className="space-y-3">
                <div className="p-3.5 rounded-lg bg-slate-950/80 border border-rose-500/30">
                  <div className="text-[11px] font-mono text-slate-400 font-bold uppercase mb-1">
                    HYPOTHETICAL ALTERNATIVE:
                  </div>
                  <h4 className="text-sm font-bold text-slate-100 font-sans">
                    {counterfactualData.counterfactual_world.action}
                  </h4>
                </div>

                <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/30 text-xs text-rose-300">
                  <span className="font-mono font-bold text-rose-400 uppercase block mb-1">
                    [PROJECTED FAILURE/OUTCOME]:
                  </span>
                  {counterfactualData.counterfactual_world.projected_outcome}
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
                  <div className="font-mono text-rose-400 text-[11px] font-bold uppercase">
                    New Risks Introduced in Counterfactual:
                  </div>
                  <ul className="list-disc pl-4 text-rose-300/90 space-y-1">
                    {counterfactualData.new_risks?.map((r, i) => (
                      <li key={i}>{r.replace('_', ' ')}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </GlassCard>
          </div>

          {/* Contextual Historical Analogue Callout */}
          <HindsightEvidenceBadge
            variant="card"
            memoryText="HINDSIGHT HISTORICAL ANALOGUE: Service restart historically succeeded during isolated thread deadlocks, but FAILED during sustained socket exhaustion / provider-level outages (incident recurred within 20m)."
            outcome="Divergence grounds why restarting is dangerous in sustained outages."
            confidence={0.94}
            lessonsLearned="Simulation outcomes depend on contextual failure state rather than static rules."
          />
        </div>
      )}

      {/* MULTI-SCENARIO COMPARISON TABLE */}
      {multiScenarioData && (
        <GlassCard
          header={
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                  MULTI-SCENARIO DECISION MATRIX
                </h3>
              </div>
              <span className="text-xs font-mono text-slate-400">
                {evaluations.length} Options Evaluated Independently
              </span>
            </div>
          }
        >
          {evaluations.length === 0 ? (
            <div className="py-8 text-center text-xs font-mono text-slate-400">
              No candidate option evaluations recorded for this decision context.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                    <th className="pb-3 font-semibold">Candidate Action</th>
                    <th className="pb-3 font-semibold">Projected Outcome</th>
                    <th className="pb-3 font-semibold">Risk Severity</th>
                    <th className="pb-3 font-semibold">Reversibility</th>
                    <th className="pb-3 font-semibold">Human Approval</th>
                    <th className="pb-3 font-semibold">Confidence</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-sans">
                  {evaluations.map((ev, idx) => (
                    <tr key={idx} className="hover:bg-slate-900/60 transition-colors">
                      <td className="py-3.5 pr-4 font-bold text-slate-200">
                        {ev.action || ev.option || 'Candidate Intervention'}
                      </td>
                      <td className="py-3.5 pr-4 text-slate-300 max-w-xs">
                        {ev.projected_outcome || (ev.projected_outcomes && ev.projected_outcomes[0]) || 'Projected recovery'}
                      </td>
                      <td className="py-3.5 pr-4">
                        <StatusBadge type="risk" value={ev.risk_severity || 'medium'} />
                      </td>
                      <td className="py-3.5 pr-4 font-mono uppercase text-slate-300">
                        {ev.reversibility || 'medium'}
                      </td>
                      <td className="py-3.5 pr-4 font-mono">
                        {ev.required_approval ? (
                          <span className="text-amber-400 font-semibold">MANDATORY</span>
                        ) : (
                          <span className="text-slate-500">Auto</span>
                        )}
                      </td>
                      <td className="py-3.5">
                        <StatusBadge type="confidence" value={typeof ev.confidence === 'number' ? ev.confidence : 0.85} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </GlassCard>
      )}
    </div>
  );
}
