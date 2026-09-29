'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Search,
  Bell,
  PlayCircle,
  Command,
  Activity,
  ShieldCheck,
  CheckCircle,
} from 'lucide-react';
import { CommandPalette } from '@/components/common/CommandPalette';
import { systemService } from '@/services/system';
import { actionsService } from '@/services/actions';

export const TopBar: React.FC = () => {
  const pathname = usePathname();
  const [isCommandOpen, setIsCommandOpen] = useState(false);
  const [healthStatus, setHealthStatus] = useState<string>('checking');
  const [pendingApprovalsCount, setPendingApprovalsCount] = useState<number>(0);

  useEffect(() => {
    // Check health & approvals count
    const loadTelemetry = async () => {
      try {
        const health = await systemService.getHealth();
        setHealthStatus(health.status === 'ok' ? 'healthy' : 'degraded');
      } catch {
        setHealthStatus('unreachable');
      }

      try {
        const pending = await actionsService.listActions(undefined, undefined, 'pending');
        setPendingApprovalsCount(pending.length);
      } catch {
        // Quiet fallback
      }
    };

    loadTelemetry();
    const interval = setInterval(loadTelemetry, 15000);
    return () => clearInterval(interval);
  }, []);

  const getBreadcrumb = () => {
    if (pathname === '/dashboard' || pathname === '/') return 'Mission Overview';
    const clean = pathname.replace('/', '').replace('-', ' ');
    return clean.charAt(0).toUpperCase() + clean.slice(1);
  };

  return (
    <>
      <header className="h-16 px-6 border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md flex items-center justify-between sticky top-0 z-20">
        {/* Left: Breadcrumbs & Mode Indicator */}
        <div className="flex items-center gap-3">
          <div className="text-xs font-mono uppercase tracking-wider text-slate-400">
            NEXUS-Ω
          </div>
          <span className="text-slate-600">/</span>
          <h1 className="text-sm font-semibold tracking-tight text-slate-100 font-sans">
            {getBreadcrumb()}
          </h1>
        </div>

        {/* Center: Global Search Bar */}
        <div className="flex-1 max-w-md mx-6">
          <button
            onClick={() => setIsCommandOpen(true)}
            className="w-full flex items-center justify-between px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-slate-400 hover:border-slate-700 hover:text-slate-300 transition-all shadow-inner"
          >
            <div className="flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-cyan-400" />
              <span>Search decisions, memories, causal graph, or actions...</span>
            </div>
            <div className="flex items-center gap-1 font-mono text-[10px] bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700 text-slate-300">
              <Command className="w-3 h-3" />
              <span>K</span>
            </div>
          </button>
        </div>

        {/* Right: Telemetry & Actions */}
        <div className="flex items-center gap-3">
          {/* Health Pill */}
          <Link
            href="/system"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors"
          >
            <span
              className={`w-2 h-2 rounded-full ${
                healthStatus === 'healthy'
                  ? 'bg-emerald-400 shadow-sm shadow-emerald-400'
                  : 'bg-amber-400 animate-pulse'
              }`}
            />
            <span className="text-slate-300 text-[11px] uppercase tracking-wider font-semibold">
              {healthStatus}
            </span>
          </Link>

          {/* Pending Approvals Badge */}
          <Link
            href="/approvals"
            className="relative p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition-colors"
            title="Human Approval Queue"
          >
            <ShieldCheck className="w-4 h-4 text-amber-400" />
            {pendingApprovalsCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-amber-500 text-slate-950 font-bold font-mono text-[10px] flex items-center justify-center animate-bounce">
                {pendingApprovalsCount}
              </span>
            )}
          </Link>

          {/* Live Demo Button */}
          <Link
            href="/demo"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium text-xs shadow-md shadow-purple-900/30 transition-all font-sans"
          >
            <PlayCircle className="w-3.5 h-3.5" />
            <span>Launch Live Demo</span>
          </Link>
        </div>
      </header>

      <CommandPalette isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} />
    </>
  );
};
