'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Sparkles,
  Brain,
  GitBranch,
  SplitSquareVertical,
  ShieldCheck,
  CheckCircle2,
  ListOrdered,
  History,
  Activity,
  HeartPulse,
  PlayCircle,
  Building2,
  UserCheck,
  Zap,
  Scale,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { DEFAULT_ORG_NAME } from '@/services/api';

const NAV_ITEMS = [
  { name: 'Mission Overview', path: '/dashboard', icon: LayoutDashboard, badge: 'Live' },
  { name: 'Live ACME Demo', path: '/demo', icon: PlayCircle, badge: 'Judge View', highlight: true },
  { name: 'Evaluation & A/B', path: '/evaluation', icon: Scale, badge: 'Proof', highlight: true },
  { name: 'Investigations', path: '/investigations', icon: Sparkles },
  { name: 'Memory Explorer', path: '/memory', icon: Brain, badge: 'Hindsight' },
  { name: 'Memory Proof', path: '/memory/proof', icon: ShieldCheck, badge: 'Lineage' },
  { name: 'Causal Graph', path: '/causal', icon: GitBranch },
  { name: 'Simulations', path: '/simulations', icon: SplitSquareVertical, badge: 'What-If' },
  { name: 'Decisions', path: '/decisions', icon: ListOrdered },
  { name: 'Approvals', path: '/approvals', icon: ShieldCheck, badge: 'HITL Gate' },
  { name: 'Actions', path: '/actions', icon: CheckCircle2 },
  { name: 'Time Machine', path: '/time-machine', icon: History },
  { name: 'Agent Runs', path: '/agents', icon: Activity },
  { name: 'System Health', path: '/system', icon: HeartPulse },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 shrink-0 h-screen sticky top-0 flex flex-col bg-slate-950/95 border-r border-slate-800/80 select-none z-30">
      {/* Brand Header */}
      <div className="h-16 px-5 flex items-center justify-between border-b border-slate-800/80 bg-slate-950">
        <Link href="/dashboard" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center font-mono font-bold text-white shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40 transition-all">
            Ω
          </div>
          <div>
            <div className="font-mono font-bold text-sm tracking-widest text-slate-100 flex items-center gap-1.5">
              NEXUS-Ω
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
            </div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
              Intelligence Cockpit
            </div>
          </div>
        </Link>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.path || (item.path === '/dashboard' && pathname === '/');

          return (
            <Link
              key={item.path}
              href={item.path}
              className={cn(
                'flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all group',
                isActive
                  ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                  : item.highlight
                  ? 'bg-purple-950/40 text-purple-300 border border-purple-800/60 hover:bg-purple-900/50 hover:text-white'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80 border border-transparent'
              )}
            >
              <div className="flex items-center gap-2.5">
                <Icon
                  className={cn(
                    'w-4 h-4 transition-colors',
                    isActive
                      ? 'text-cyan-400'
                      : item.highlight
                      ? 'text-purple-400'
                      : 'text-slate-400 group-hover:text-slate-300'
                  )}
                />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span
                  className={cn(
                    'px-1.5 py-0.5 rounded text-[10px] font-mono tracking-tight font-semibold',
                    isActive
                      ? 'bg-cyan-500/20 text-cyan-300'
                      : item.highlight
                      ? 'bg-purple-500/20 text-purple-300'
                      : 'bg-slate-800 text-slate-400'
                  )}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Organization & Operator Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/60 space-y-2">
        <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 truncate">
            <Building2 className="w-4 h-4 text-cyan-400 shrink-0" />
            <div className="truncate">
              <div className="text-xs font-medium text-slate-200 truncate">
                {DEFAULT_ORG_NAME}
              </div>
              <div className="text-[10px] font-mono text-slate-500 truncate">
                Production Cluster
              </div>
            </div>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-400" title="Org active" />
        </div>

        <div className="flex items-center justify-between px-2 pt-1 text-xs text-slate-400 font-mono">
          <div className="flex items-center gap-1.5">
            <UserCheck className="w-3.5 h-3.5 text-slate-400" />
            <span>Operator: Lead SRE</span>
          </div>
          <div className="flex items-center gap-1 text-[11px] text-emerald-400">
            <Zap className="w-3 h-3" />
            <span>HITL Ready</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
