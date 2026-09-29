'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  glow?: 'cyan' | 'rose' | 'emerald' | 'amber' | 'purple' | 'none';
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className,
  header,
  footer,
  glow = 'none',
  onClick,
}) => {
  const glowClass =
    glow === 'cyan'
      ? 'tech-glow-cyan border-cyan-500/30'
      : glow === 'rose'
      ? 'tech-glow-rose border-rose-500/30'
      : glow === 'emerald'
      ? 'tech-glow-emerald border-emerald-500/30'
      : glow === 'amber'
      ? 'border-amber-500/30 shadow-md shadow-amber-950/30'
      : glow === 'purple'
      ? 'border-purple-500/30 shadow-md shadow-purple-950/30'
      : 'border-slate-800/80 hover:border-slate-700/90';

  return (
    <div
      onClick={onClick}
      className={cn(
        'glass-panel rounded-xl p-5 transition-all duration-200 relative overflow-hidden',
        glowClass,
        onClick && 'cursor-pointer hover:bg-slate-900/80',
        className
      )}
    >
      {header && <div className="mb-4 pb-3 border-b border-slate-800/80">{header}</div>}
      <div className="space-y-4">{children}</div>
      {footer && <div className="mt-4 pt-3 border-t border-slate-800/80">{footer}</div>}
    </div>
  );
};
