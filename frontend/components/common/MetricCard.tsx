'use client';

import React from 'react';
import { GlassCard } from './GlassCard';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon?: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendText?: string;
  color?: 'cyan' | 'emerald' | 'rose' | 'amber' | 'purple' | 'slate';
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  subtext,
  icon: Icon,
  trendText,
  color = 'cyan',
  className,
}) => {
  const iconColor =
    color === 'cyan'
      ? 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20'
      : color === 'emerald'
      ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
      : color === 'rose'
      ? 'text-rose-400 bg-rose-500/10 border-rose-500/20'
      : color === 'amber'
      ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
      : color === 'purple'
      ? 'text-purple-400 bg-purple-500/10 border-purple-500/20'
      : 'text-slate-400 bg-slate-800 border-slate-700';

  return (
    <GlassCard className={cn('p-4', className)}>
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-mono uppercase tracking-wider text-slate-400">
            {label}
          </span>
          <div className="text-2xl font-bold font-mono tracking-tight text-slate-100 mt-1">
            {value}
          </div>
          {(subtext || trendText) && (
            <div className="flex items-center gap-2 mt-1 text-xs text-slate-400">
              {trendText && (
                <span className="font-mono text-cyan-400">{trendText}</span>
              )}
              {subtext && <span>{subtext}</span>}
            </div>
          )}
        </div>
        {Icon && (
          <div className={cn('p-2.5 rounded-lg border', iconColor)}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </GlassCard>
  );
};
