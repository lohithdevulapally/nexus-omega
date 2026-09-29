'use client';

import React from 'react';
import { getRiskColor, cn } from '@/lib/utils';
import { ShieldAlert, ShieldCheck, Clock, CheckCircle, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  type: 'risk' | 'approval' | 'execution' | 'confidence';
  value: string | number;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ type, value, className }) => {
  if (type === 'risk') {
    const risk = String(value).toLowerCase();
    const style = getRiskColor(risk);
    return (
      <span
        className={cn(
          'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-xs font-mono font-medium border uppercase tracking-wider',
          style.badge,
          className
        )}
      >
        <span className={cn('w-1.5 h-1.5 rounded-full', style.dot)} />
        {risk}
      </span>
    );
  }

  if (type === 'approval') {
    const status = String(value).toLowerCase();
    if (status === 'approved') {
      return (
        <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30', className)}>
          <ShieldCheck className="w-3.5 h-3.5" />
          APPROVED
        </span>
      );
    }
    if (status === 'rejected') {
      return (
        <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-rose-500/10 text-rose-400 border border-rose-500/30', className)}>
          <XCircle className="w-3.5 h-3.5" />
          REJECTED
        </span>
      );
    }
    return (
      <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-amber-500/10 text-amber-400 border border-amber-500/30 animate-pulse', className)}>
        <Clock className="w-3.5 h-3.5" />
        PENDING REVIEW
      </span>
    );
  }

  if (type === 'execution') {
    const status = String(value).toLowerCase();
    if (status === 'completed' || status === 'executed') {
      return (
        <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30', className)}>
          <CheckCircle className="w-3.5 h-3.5" />
          EXECUTED
        </span>
      );
    }
    if (status === 'executing') {
      return (
        <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 animate-pulse', className)}>
          <Clock className="w-3.5 h-3.5" />
          EXECUTING
        </span>
      );
    }
    return (
      <span className={cn('inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-mono bg-slate-500/10 text-slate-400 border border-slate-700', className)}>
        {status}
      </span>
    );
  }

  // Confidence
  const num = typeof value === 'number' ? Math.round(value * 100) : parseInt(String(value), 10);
  const color = num >= 85 ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' : num >= 70 ? 'text-cyan-400 border-cyan-500/30 bg-cyan-500/10' : 'text-amber-400 border-amber-500/30 bg-amber-500/10';

  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded text-xs font-mono border font-semibold', color, className)}>
      {num}% CONFIDENCE
    </span>
  );
};
