'use client';

import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  Play,
  Clock,
  ShieldCheck,
  AlertTriangle,
  RefreshCw,
  Terminal,
  Filter,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { actionsService } from '@/services/actions';
import { ActionItem } from '@/types/api';
import { formatRelativeTime } from '@/lib/utils';

export default function ActionsExecutionPage() {
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [loading, setLoading] = useState<boolean>(true);
  const [executingId, setExecutingId] = useState<string | null>(null);

  const fetchActions = async () => {
    setLoading(true);
    try {
      const data = await actionsService.listActions();
      setActions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActions();
  }, []);

  const handleExecute = async (actionId: string) => {
    setExecutingId(actionId);
    try {
      await actionsService.executeAction(actionId, 'lead_sre_operator');
      await fetchActions();
    } catch (err: any) {
      alert(`Execution failed: ${err.message}`);
    } finally {
      setExecutingId(null);
    }
  };

  const filtered = actions.filter((act) => {
    if (filterStatus === 'all') return true;
    if (filterStatus === 'pending') return act.approval_status === 'pending';
    if (filterStatus === 'approved') return act.approval_status === 'approved' && act.execution_status !== 'completed';
    if (filterStatus === 'completed') return act.execution_status === 'completed';
    if (filterStatus === 'rejected') return act.approval_status === 'rejected';
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold">
              Controlled Action Engine
            </span>
            <span className="text-xs text-slate-400 font-mono">Whitelisted Interventions • No Arbitrary Shell</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Action Registry & Safe Execution Console
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Controlled operational mutations with schema validation, permission checks, duplicate prevention, and human authorization verification before execution.
          </p>
        </div>

        <button
          onClick={fetchActions}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Actions</span>
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono">
          {['all', 'approved', 'completed', 'pending', 'rejected'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1.5 rounded-lg capitalize font-medium transition-all ${
                filterStatus === st
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950/50'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
        <div className="text-xs font-mono text-slate-400">
          Total Interventions: <strong className="text-slate-200">{filtered.length}</strong>
        </div>
      </div>

      {/* Actions List */}
      <div className="space-y-4">
        {filtered.length === 0 ? (
          <GlassCard className="py-12 text-center text-xs text-slate-400 font-mono">
            No actions match the selected filter.
          </GlassCard>
        ) : (
          filtered.map((act) => {
            const canExecute = act.approval_status === 'approved' && act.execution_status !== 'completed';
            const isCompleted = act.execution_status === 'completed';

            return (
              <GlassCard key={act.id} className="space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2.5 border-b border-slate-800">
                  <div className="flex items-center gap-2.5">
                    <StatusBadge type="risk" value={act.risk_level} />
                    <span className="text-xs font-mono font-bold text-slate-200 uppercase">
                      {act.action_type}
                    </span>
                    <StatusBadge type="approval" value={act.approval_status} />
                    <StatusBadge type="execution" value={act.execution_status} />
                  </div>
                  <div className="text-[11px] font-mono text-slate-500">
                    ID: {act.id.slice(0, 8)} • {formatRelativeTime(act.created_at)}
                  </div>
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-sm font-bold text-slate-100 font-sans">
                    {act.payload?.title || act.action_type}
                  </h3>
                  <div className="text-xs font-mono text-slate-400 bg-slate-950/80 p-2.5 rounded border border-slate-850">
                    {JSON.stringify(act.payload, null, 2)}
                  </div>
                </div>

                {/* Execution Result */}
                {act.result && (
                  <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-900/40 text-xs font-mono text-emerald-300">
                    <span className="font-bold text-emerald-400 uppercase block mb-1">
                      Execution Result (PostgreSQL Verified):
                    </span>
                    <pre className="whitespace-pre-wrap">{JSON.stringify(act.result, null, 2)}</pre>
                  </div>
                )}

                {/* Execute Button */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs font-mono text-slate-400">
                  <div>
                    Requested by: <strong className="text-slate-200">{act.requested_by || 'agent'}</strong>
                    {act.approved_by && (
                      <span className="ml-3 text-cyan-400">
                        Authorized by: {act.approved_by}
                      </span>
                    )}
                  </div>

                  {canExecute && (
                    <button
                      onClick={() => handleExecute(act.id)}
                      disabled={executingId === act.id}
                      className="px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white font-semibold text-xs font-sans flex items-center gap-1.5 transition-all shadow-md shadow-emerald-950/50"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>{executingId === act.id ? 'EXECUTING SAFE MUTATION...' : 'EXECUTE INTERVENTION'}</span>
                    </button>
                  )}
                </div>
              </GlassCard>
            );
          })
        )}
      </div>
    </div>
  );
}
