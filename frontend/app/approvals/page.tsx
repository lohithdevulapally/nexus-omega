'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  Clock,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  UserCheck,
  History,
  RefreshCw,
  X,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { actionsService } from '@/services/actions';
import { ActionItem } from '@/types/api';
import { formatRelativeTime } from '@/lib/utils';

export default function ApprovalsPage() {
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [processingId, setProcessingId] = useState<string | null>(null);

  // Rejection modal
  const [rejectModalOpen, setRejectModalOpen] = useState<boolean>(false);
  const [rejectingAction, setRejectingAction] = useState<ActionItem | null>(null);
  const [rejectReason, setRejectReason] = useState<string>('Operational risk threshold exceeded');

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

  const handleApprove = async (action: ActionItem) => {
    setProcessingId(action.id);
    try {
      await actionsService.approveAction(action.id, 'lead_sre_operator', 'Authorized via Mission Control');
      await fetchActions();
    } catch (err: any) {
      alert(`Approval notice: ${err.message}`);
    } finally {
      setProcessingId(null);
    }
  };

  const handleRejectConfirm = async () => {
    if (!rejectingAction || !rejectReason.trim()) return;
    setProcessingId(rejectingAction.id);
    try {
      await actionsService.rejectAction(rejectingAction.id, 'lead_sre_operator', rejectReason);
      setRejectModalOpen(false);
      setRejectingAction(null);
      await fetchActions();
    } catch (err: any) {
      alert(`Rejection error: ${err.message}`);
    } finally {
      setProcessingId(null);
    }
  };

  const pending = actions.filter((a) => a.approval_status === 'pending');
  const audited = actions.filter((a) => a.approval_status !== 'pending');

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-amber-950/40 to-slate-900 border border-amber-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">
              Human-in-the-Loop Governance
            </span>
            <span className="text-xs text-slate-400 font-mono">Zero Unverified Actions</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Human Approval Gate & Authorization Queue
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Autonomous agents cannot execute high-consequence operational mutations without audited human sign-off. Review simulation evidence and authorize interventions safely.
          </p>
        </div>

        <button
          onClick={fetchActions}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Queue</span>
        </button>
      </div>

      {/* PENDING APPROVALS QUEUE */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
            <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              PENDING AUTHORIZATION QUEUE ({pending.length})
            </h2>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Mandatory Human Review Threshold
          </span>
        </div>

        {pending.length === 0 ? (
          <GlassCard className="py-12 text-center text-xs text-slate-400 font-mono">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            No pending action approvals. All systems operating within autonomous boundaries.
          </GlassCard>
        ) : (
          <div className="space-y-4">
            {pending.map((act) => (
              <GlassCard key={act.id} glow="amber" className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-3">
                    <StatusBadge type="risk" value={act.risk_level} />
                    <span className="text-xs font-mono font-bold text-slate-300 uppercase">
                      Action Type: {act.action_type}
                    </span>
                  </div>
                  <div className="text-xs font-mono text-slate-500">
                    Requested {formatRelativeTime(act.created_at)} by <strong className="text-slate-300">{act.requested_by}</strong>
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="text-base font-bold text-slate-100 font-sans">
                    {act.payload?.title || act.action_type}
                  </h3>
                  <div className="text-xs text-slate-300 bg-slate-950/80 rounded-lg p-3 border border-slate-850 font-mono">
                    <span className="text-cyan-400 font-semibold uppercase block mb-1">Payload Parameters:</span>
                    {JSON.stringify(act.payload, null, 2)}
                  </div>
                </div>

                {/* Evidence Context */}
                <HindsightEvidenceBadge
                  variant="card"
                  memoryText="Grounding: Secondary Rail B has verified SSL certificates and 99.98% historical success rate during Incident #3. Restarting gateway primary node triggered 20-minute outage escalation."
                  confidence={0.95}
                />

                {/* Approve / Reject Buttons */}
                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    onClick={() => {
                      setRejectingAction(act);
                      setRejectModalOpen(true);
                    }}
                    disabled={processingId === act.id}
                    className="px-4 py-2 rounded-lg bg-rose-600/10 hover:bg-rose-600/20 text-rose-400 border border-rose-500/30 text-xs font-semibold font-mono transition-colors"
                  >
                    REJECT ACTION
                  </button>
                  <button
                    onClick={() => handleApprove(act)}
                    disabled={processingId === act.id}
                    className="px-6 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs font-sans flex items-center gap-1.5 shadow-md shadow-emerald-950/50 transition-all"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{processingId === act.id ? 'AUTHORIZING...' : 'APPROVE ACTION'}</span>
                  </button>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>

      {/* AUDITED ACTION HISTORY */}
      <div className="space-y-4 pt-4">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-slate-400" />
          <h2 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
            AUDITED HUMAN APPROVAL HISTORY ({audited.length})
          </h2>
        </div>

        <GlassCard>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-sans">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                  <th className="pb-3 font-semibold">Action</th>
                  <th className="pb-3 font-semibold">Risk Tier</th>
                  <th className="pb-3 font-semibold">Approval Status</th>
                  <th className="pb-3 font-semibold">Audited Reviewer</th>
                  <th className="pb-3 font-semibold">Execution Status</th>
                  <th className="pb-3 font-semibold">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {audited.map((act) => (
                  <tr key={act.id} className="hover:bg-slate-900/60 transition-colors">
                    <td className="py-3 pr-4 font-bold text-slate-200">
                      {act.payload?.title || act.action_type}
                    </td>
                    <td className="py-3 pr-4">
                      <StatusBadge type="risk" value={act.risk_level} />
                    </td>
                    <td className="py-3 pr-4">
                      <StatusBadge type="approval" value={act.approval_status} />
                    </td>
                    <td className="py-3 pr-4 font-mono text-slate-300">
                      {act.approved_by || 'system_audit'}
                    </td>
                    <td className="py-3 pr-4">
                      <StatusBadge type="execution" value={act.execution_status} />
                    </td>
                    <td className="py-3 text-slate-500 font-mono text-[11px]">
                      {formatRelativeTime(act.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>

      {/* REJECTION REASON MODAL */}
      {rejectModalOpen && rejectingAction && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
          <div className="w-full max-w-lg rounded-xl bg-slate-900 border border-rose-500/40 p-5 space-y-4 glass-panel-elevated">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono uppercase text-rose-400 font-bold">
                  MANDATORY AUDITED JUSTIFICATION
                </span>
                <h3 className="text-base font-bold text-slate-100 font-sans mt-0.5">
                  Reject Action: {rejectingAction.payload?.title || rejectingAction.action_type}
                </h3>
              </div>
              <button
                onClick={() => setRejectModalOpen(false)}
                className="p-1 rounded text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-300">
              Provide an explicit operational reason for permanently rejecting this intervention. This justification will be audited in PostgreSQL and retained for agent learning.
            </p>

            <textarea
              rows={3}
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              className="w-full p-3 rounded-lg bg-slate-950 border border-slate-700 text-xs font-sans text-slate-100 focus:outline-none focus:border-rose-400"
              placeholder="Explain why this action cannot be authorized..."
            />

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setRejectModalOpen(false)}
                className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-mono hover:bg-slate-700"
              >
                CANCEL
              </button>
              <button
                onClick={handleRejectConfirm}
                className="px-5 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs font-sans"
              >
                CONFIRM REJECTION
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
