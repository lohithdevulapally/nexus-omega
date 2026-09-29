'use client';

import React, { useState, useEffect } from 'react';
import {
  Activity,
  Bot,
  Brain,
  Clock,
  CheckCircle2,
  AlertCircle,
  Eye,
  RefreshCw,
  X,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { agentsService } from '@/services/agents';
import { AgentRunItem } from '@/types/api';
import { formatRelativeTime } from '@/lib/utils';

export default function AgentRunsPage() {
  const [runs, setRuns] = useState<AgentRunItem[]>([]);
  const [selectedRun, setSelectedRun] = useState<AgentRunItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchRuns = async () => {
    setLoading(true);
    try {
      const data = await agentsService.listRuns();
      setRuns(data);
      if (data.length > 0 && !selectedRun) {
        setSelectedRun(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRuns();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-cyan-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold">
              Autonomous Agent Telemetry
            </span>
            <span className="text-xs text-slate-400 font-mono">PostgreSQL: agent_runs</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Agent Run Monitor & Latency Telemetry
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Inspect individual specialized agent executions, input tasks, latency breakdown, memory token consumption, and structured outputs.
          </p>
        </div>

        <button
          onClick={fetchRuns}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Agent Runs</span>
        </button>
      </div>

      {/* Visual Agent Pipeline Sequence */}
      <GlassCard
        header={
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              8-AGENT EXECUTION TOPOLOGY
            </h3>
          </div>
        }
      >
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
          {[
            'PlannerAgent',
            'MemoryAgent',
            'AnalystAgent',
            'CausalAgent',
            'DecisionAgent',
            'CounterfactualSim',
            'RiskAgent',
            'CriticAgent',
            'ReflectionAgent',
          ].map((ag, idx) => (
            <div
              key={ag}
              className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 flex items-center gap-1.5"
            >
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              <span>{ag}</span>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* 2-Column: Agent Runs Table + Selected Run Detail */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Runs Table (2 cols) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="text-xs font-mono font-bold uppercase text-slate-400">
            RECORDED AGENT EXECUTIONS ({runs.length})
          </div>

          <GlassCard>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                    <th className="pb-3 font-semibold">Agent</th>
                    <th className="pb-3 font-semibold">Status</th>
                    <th className="pb-3 font-semibold">Duration</th>
                    <th className="pb-3 font-semibold">Started</th>
                    <th className="pb-3 text-right">Inspect</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-sans">
                  {runs.map((r) => {
                    const isSelected = selectedRun?.id === r.id;
                    return (
                      <tr
                        key={r.id}
                        onClick={() => setSelectedRun(r)}
                        className={`cursor-pointer transition-colors ${
                          isSelected ? 'bg-cyan-950/30' : 'hover:bg-slate-900/60'
                        }`}
                      >
                        <td className="py-3 pr-4 font-bold text-slate-200">
                          {r.agent_name}
                        </td>
                        <td className="py-3 pr-4">
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold uppercase">
                            {r.status}
                          </span>
                        </td>
                        <td className="py-3 pr-4 font-mono text-cyan-400">
                          {r.duration_ms ? `${r.duration_ms.toFixed(1)}ms` : '—'}
                        </td>
                        <td className="py-3 pr-4 text-slate-500 font-mono text-[11px]">
                          {formatRelativeTime(r.started_at)}
                        </td>
                        <td className="py-3 text-right">
                          <Eye className="w-4 h-4 text-slate-500 inline-block hover:text-cyan-400" />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </GlassCard>
        </div>

        {/* Selected Run Inspector (1 col) */}
        <div className="space-y-4">
          <div className="text-xs font-mono font-bold uppercase text-slate-400">
            EXECUTION PAYLOAD INSPECTOR
          </div>

          {selectedRun ? (
            <GlassCard glow="cyan" className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-mono font-bold uppercase text-cyan-400">
                    {selectedRun.agent_name}
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    {selectedRun.duration_ms ? `${selectedRun.duration_ms.toFixed(1)}ms` : 'completed'}
                  </span>
                </div>
                <div className="text-xs text-slate-300 font-sans">
                  Task: {selectedRun.task}
                </div>
              </div>

              {/* Output Data */}
              <div className="space-y-1">
                <span className="text-[11px] font-mono text-slate-400 uppercase font-semibold">
                  OUTPUT DATA:
                </span>
                <div className="bg-slate-950 rounded-lg p-3 border border-slate-800 text-xs font-mono text-slate-300 overflow-x-auto max-h-60">
                  <pre>{JSON.stringify(selectedRun.output_data, null, 2)}</pre>
                </div>
              </div>

              {/* Input Data */}
              <div className="space-y-1">
                <span className="text-[11px] font-mono text-slate-400 uppercase font-semibold">
                  INPUT DATA:
                </span>
                <div className="bg-slate-950 rounded-lg p-3 border border-slate-800 text-xs font-mono text-slate-400 overflow-x-auto max-h-40">
                  <pre>{JSON.stringify(selectedRun.input_data, null, 2)}</pre>
                </div>
              </div>
            </GlassCard>
          ) : (
            <div className="p-8 rounded-xl bg-slate-900/50 border border-slate-800 text-center text-xs text-slate-500 font-mono">
              Select an execution to inspect payload.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
