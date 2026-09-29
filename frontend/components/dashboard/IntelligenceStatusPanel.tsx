'use client';

import React from 'react';
import { GlassCard } from '@/components/common/GlassCard';
import { Database, Brain, Bot, GitBranch, SplitSquareVertical, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';
import { HealthResponse } from '@/types/api';

interface IntelligenceStatusPanelProps {
  health?: HealthResponse | null;
  loading?: boolean;
}

export const IntelligenceStatusPanel: React.FC<IntelligenceStatusPanelProps> = ({ health, loading }) => {
  const isHealthy = health?.status === 'ok';

  const engines = [
    {
      name: 'PostgreSQL State',
      role: 'Relational Ground Truth',
      status: health?.database === 'connected' ? 'ONLINE' : 'DEGRADED',
      icon: Database,
      details: 'Organizations, Customers, Events, Decisions, Causal Tables',
      accent: 'cyan',
    },
    {
      name: 'Hindsight Engine',
      role: 'Episodic Organizational Memory',
      status: health?.hindsight === 'connected' ? 'ONLINE' : 'DEGRADED',
      icon: Brain,
      details: `Bank: ${health?.bank_id || 'nexus-demo'} (Dual-Index Embeddings)`,
      accent: 'purple',
    },
    {
      name: 'Multi-Agent Graph',
      role: '8 Specialized Reasoning Agents',
      status: isHealthy ? 'ONLINE' : 'STANDBY',
      icon: Bot,
      details: 'Planner, Memory, Analyst, Causal, Decision, Sim, Risk, Critic',
      accent: 'emerald',
    },
    {
      name: 'Causal Knowledge Graph',
      role: 'Bayesian Topology & Root Cause',
      status: isHealthy ? 'ONLINE' : 'STANDBY',
      icon: GitBranch,
      details: '13 Relationship Types with Counter-Evidence Tracking',
      accent: 'cyan',
    },
    {
      name: 'Counterfactual Engine',
      role: 'Isolated State Simulations',
      status: isHealthy ? 'ONLINE' : 'STANDBY',
      icon: SplitSquareVertical,
      details: 'Actual vs What-If Worlds (SIMULATION_ONLY)',
      accent: 'amber',
    },
    {
      name: 'Controlled Action Engine',
      role: 'Safe Interventions & HITL Gate',
      status: isHealthy ? 'ONLINE' : 'STANDBY',
      icon: ShieldCheck,
      details: 'Schema Validation, Risk Tiers, Human Approval State Machine',
      accent: 'emerald',
    },
  ];

  return (
    <GlassCard
      glow="cyan"
      header={
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
            <h2 className="text-base font-bold font-mono tracking-wider text-slate-100 uppercase">
              INTELLIGENCE STATUS & ENGINE MESH
            </h2>
          </div>
          <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-700 text-xs font-mono text-cyan-400">
            {loading ? 'PROBING...' : isHealthy ? 'ALL SYSTEMS OPERATIONAL' : 'SYSTEM DEGRADED'}
          </span>
        </div>
      }
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {engines.map((eng, idx) => {
          const Icon = eng.icon;
          const isEngOnline = eng.status === 'ONLINE';

          return (
            <div
              key={idx}
              className="p-3.5 rounded-lg bg-slate-950/70 border border-slate-800/90 hover:border-slate-700 transition-all flex flex-col justify-between"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800 text-cyan-400">
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-100 font-sans">
                      {eng.name}
                    </h3>
                    <div className="text-[11px] font-mono text-slate-400">
                      {eng.role}
                    </div>
                  </div>
                </div>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${
                    isEngOnline
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  }`}
                >
                  {eng.status}
                </span>
              </div>
              <div className="text-xs text-slate-400 font-mono pt-2 border-t border-slate-900 truncate">
                {eng.details}
              </div>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
};
