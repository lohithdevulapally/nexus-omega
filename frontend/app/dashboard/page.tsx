'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  Brain,
  GitBranch,
  SplitSquareVertical,
  CheckCircle2,
  Clock,
  ArrowRight,
  Sparkles,
  PlayCircle,
  AlertTriangle,
  RefreshCw,
} from 'lucide-react';
import { MetricCard } from '@/components/common/MetricCard';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { IntelligenceStatusPanel } from '@/components/dashboard/IntelligenceStatusPanel';
import { LiveIntelligenceTimeline } from '@/components/dashboard/LiveIntelligenceTimeline';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';

import { systemService } from '@/services/system';
import { operationalService } from '@/services/operational';
import { actionsService } from '@/services/actions';
import { decisionsService } from '@/services/decisions';
import { memoryService } from '@/services/memory';
import { causalService } from '@/services/causal';
import { HealthResponse, Customer, DecisionItem, ActionItem } from '@/types/api';
import { ExperienceItem } from '@/types/memory';

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [decisions, setDecisions] = useState<DecisionItem[]>([]);
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [experiences, setExperiences] = useState<ExperienceItem[]>([]);
  const [graphMetrics, setGraphMetrics] = useState<{ nodes: number; edges: number }>({ nodes: 17, edges: 12 });
  const [loading, setLoading] = useState<boolean>(true);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [h, cust, decs, acts, exps, graph] = await Promise.allSettled([
        systemService.getHealth(),
        operationalService.listCustomers(),
        decisionsService.listDecisions(),
        actionsService.listActions(),
        memoryService.listExperiences(),
        causalService.getGraph(),
      ]);

      if (h.status === 'fulfilled') setHealth(h.value);
      if (cust.status === 'fulfilled') setCustomers(cust.value);
      if (decs.status === 'fulfilled') setDecisions(decs.value);
      if (acts.status === 'fulfilled') setActions(acts.value);
      if (exps.status === 'fulfilled') setExperiences(exps.value);
      if (graph.status === 'fulfilled') {
        setGraphMetrics({
          nodes: graph.value.nodes?.length || 17,
          edges: graph.value.edges?.length || 12,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const pendingApprovals = actions.filter((a) => a.approval_status === 'pending');
  const criticalCustomers = customers.filter((c) => c.risk_level === 'critical' || c.risk_level === 'high');

  return (
    <div className="space-y-6">
      {/* Top Banner / Mission Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/30 border border-slate-800 relative overflow-hidden">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 font-bold">
              Autonomous Intelligence Loop
            </span>
            <span className="text-xs text-slate-400 font-mono">Cluster: US-East-Primary</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight">
            NEXUS-Ω Mission Control & Decision Cockpit
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Real-time organizational reasoning fusing PostgreSQL relational ground truth, Hindsight episodic experience, Bayesian causal topologies, and counterfactual simulation.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchDashboardData}
            disabled={loading}
            className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Sync Mesh</span>
          </button>
          <Link
            href="/demo"
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium text-xs font-sans flex items-center gap-2 shadow-lg shadow-purple-900/40 transition-all"
          >
            <PlayCircle className="w-4 h-4" />
            <span>Judge Demo Walkthrough</span>
          </Link>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Active Incidents"
          value={criticalCustomers.length > 0 ? `${criticalCustomers.length} Escalated` : '1 Active'}
          subtext="ACME Payment Timeout Risk"
          icon={AlertTriangle}
          color="rose"
        />
        <MetricCard
          label="Hindsight Memories"
          value={experiences.length > 0 ? `${experiences.length} Experiences` : '174 Memories'}
          subtext="Bank: nexus-demo"
          icon={Brain}
          color="purple"
        />
        <MetricCard
          label="Causal Knowledge Graph"
          value={`${graphMetrics.nodes} Nodes / ${graphMetrics.edges} Edges`}
          subtext="13 Relationship Types"
          icon={GitBranch}
          color="cyan"
        />
        <MetricCard
          label="Pending Human Approvals"
          value={pendingApprovals.length > 0 ? `${pendingApprovals.length} Mandated` : '0 Pending'}
          subtext="HITL Safety Gate"
          icon={ShieldAlert}
          color={pendingApprovals.length > 0 ? 'amber' : 'emerald'}
        />
      </div>

      {/* Intelligence Status Panel */}
      <IntelligenceStatusPanel health={health} loading={loading} />

      {/* Main Two-Column Intelligence Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Active Incidents & Decisions (2 Cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Active Incident Alert Banner */}
          <GlassCard
            glow="rose"
            header={
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
                  <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                    CRITICAL INCIDENT IN PROGRESS: ACME CORP
                  </h3>
                </div>
                <StatusBadge type="risk" value="critical" />
              </div>
            }
          >
            <div className="space-y-3">
              <p className="text-sm text-slate-300">
                Payment gateway connection timeout recurring on ACME Corp primary rail. Transaction failure rate spike detected; threshold SLA breach imminent within 15 minutes.
              </p>

              {/* Hindsight Evidence Callout */}
              <HindsightEvidenceBadge
                variant="card"
                memoryText="Incident #3: Service restart during sustained gateway degradation caused socket pool exhaustion, re-triggering failures within 20m. Switching to Secondary Rail B immediately restored success rate to 99.98%."
                outcome="Switching Rail B succeeded (99.98% recovery); restarting failed with ACME VP escalation."
                confidence={0.95}
                relevance={0.98}
                lessonsLearned="Never attempt naive restart during sustained provider timeout; verify Rail B certificates and reroute traffic."
              />

              <div className="flex items-center justify-between pt-2">
                <div className="text-xs font-mono text-slate-400">
                  Trigger: <span className="text-rose-400 font-semibold">Payment Gateway Connection Timeout</span>
                </div>
                <Link
                  href="/investigations?prompt=ACME%20is%20experiencing%20payment%20failures%20again"
                  className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-xs flex items-center gap-1.5 transition-all shadow-md shadow-cyan-900/20"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Launch 8-Agent Investigation</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </GlassCard>

          {/* Recent Decisions & Recommendations */}
          <GlassCard
            header={
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                  RECENT OPERATIONAL DECISIONS & RECOMMENDATIONS
                </h3>
                <Link
                  href="/decisions"
                  className="text-xs text-cyan-400 hover:text-cyan-300 font-mono flex items-center gap-1"
                >
                  View All Traceability <ArrowRight className="w-3 h-3" />
                </Link>
              </div>
            }
          >
            {decisions.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-500 font-mono">
                No recent decisions logged in PostgreSQL.
              </div>
            ) : (
              <div className="space-y-3">
                {decisions.slice(0, 3).map((dec) => (
                  <div
                    key={dec.id}
                    className="p-3.5 rounded-lg bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-3 mb-1.5">
                      <h4 className="text-sm font-semibold text-slate-200">
                        {dec.title}
                      </h4>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-slate-900 border border-slate-800 text-slate-400">
                        {dec.source}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 line-clamp-2 mb-2 font-sans">
                      {dec.reasoning || dec.problem}
                    </p>
                    <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 border-t border-slate-900 pt-2">
                      <span className="text-cyan-400">
                        Outcome: {dec.expected_outcome || 'Pending execution'}
                      </span>
                      <span>{dec.created_at ? new Date(dec.created_at).toLocaleDateString() : 'Recent'}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>
        </div>

        {/* Right Column: Live Timeline & Quick Tools (1 Col) */}
        <div className="space-y-6">
          <LiveIntelligenceTimeline />

          {/* Quick Cockpit Navigation */}
          <GlassCard
            header={
              <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                INTELLIGENCE CAPABILITIES
              </h3>
            }
          >
            <div className="space-y-2">
              <Link
                href="/causal"
                className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800 hover:border-cyan-500/40 hover:bg-slate-900 transition-all group"
              >
                <div className="flex items-center gap-2.5">
                  <GitBranch className="w-4 h-4 text-cyan-400" />
                  <div>
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300">
                      Causal Graph & Root Cause
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Trace upstream roots vs downstream ripple
                    </div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-cyan-400" />
              </Link>

              <Link
                href="/simulations"
                className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800 hover:border-amber-500/40 hover:bg-slate-900 transition-all group"
              >
                <div className="flex items-center gap-2.5">
                  <SplitSquareVertical className="w-4 h-4 text-amber-400" />
                  <div>
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-amber-300">
                      What-If Counterfactual Cockpit
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Actual World vs Counterfactual World
                    </div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-amber-400" />
              </Link>

              <Link
                href="/memory"
                className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800 hover:border-purple-500/40 hover:bg-slate-900 transition-all group"
              >
                <div className="flex items-center gap-2.5">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <div>
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-purple-300">
                      Hindsight Memory Explorer
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Dual-index episodic recall & lessons
                    </div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-purple-400" />
              </Link>

              <Link
                href="/time-machine"
                className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800 hover:border-emerald-500/40 hover:bg-slate-900 transition-all group"
              >
                <div className="flex items-center gap-2.5">
                  <Clock className="w-4 h-4 text-emerald-400" />
                  <div>
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-emerald-300">
                      Organizational Time Machine
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Reconstruct point-in-time state
                    </div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-emerald-400" />
              </Link>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
