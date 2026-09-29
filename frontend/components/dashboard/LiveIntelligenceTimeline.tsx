'use client';

import React from 'react';
import { GlassCard } from '@/components/common/GlassCard';
import { Activity, Brain, GitBranch, SplitSquareVertical, ShieldAlert, CheckCircle2, Bot, Clock } from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';

export interface TimelineEvent {
  id: string;
  time: string;
  agent: string;
  type: 'memory' | 'causal' | 'simulation' | 'risk' | 'critic' | 'approval' | 'action' | 'reflection';
  summary: string;
  badge?: string;
}

interface LiveIntelligenceTimelineProps {
  events?: TimelineEvent[];
}

export const LiveIntelligenceTimeline: React.FC<LiveIntelligenceTimelineProps> = ({ events }) => {
  // Default live organizational timeline events if none passed
  const defaultEvents: TimelineEvent[] = [
    {
      id: '1',
      time: new Date(Date.now() - 1000 * 20).toISOString(),
      agent: 'ControlledActionEngine',
      type: 'action',
      summary: 'Action ID #177d1fc2 safely executed: Traffic switched to Secondary Gateway Rail B.',
      badge: 'EXECUTED',
    },
    {
      id: '2',
      time: new Date(Date.now() - 1000 * 45).toISOString(),
      agent: 'HumanApprovalGate',
      type: 'approval',
      summary: 'Lead SRE Operator authorized candidate intervention with canary pre-condition.',
      badge: 'APPROVED',
    },
    {
      id: '3',
      time: new Date(Date.now() - 1000 * 60).toISOString(),
      agent: 'CriticAgent',
      type: 'critic',
      summary: 'Intercepted blind restart trap; verified rail switch historical effectiveness (99.98% recovery).',
      badge: 'VERIFIED',
    },
    {
      id: '4',
      time: new Date(Date.now() - 1000 * 85).toISOString(),
      agent: 'CounterfactualEngine',
      type: 'simulation',
      summary: 'Simulated Actual (Rail B recovery) vs Counterfactual (Gateway restart socket exhaustion).',
      badge: 'DUAL-WORLD',
    },
    {
      id: '5',
      time: new Date(Date.now() - 1000 * 110).toISOString(),
      agent: 'CausalAgent',
      type: 'causal',
      summary: 'Isolated root cause: Primary Connection Timeout -> ACME Transaction Failures -> SLA Risk.',
      badge: 'ROOT-CAUSE',
    },
    {
      id: '6',
      time: new Date(Date.now() - 1000 * 140).toISOString(),
      agent: 'MemoryAgent',
      type: 'memory',
      summary: 'Recalled 174 Hindsight episodic experiences for ACME Corp payment timeout pattern.',
      badge: 'HINDSIGHT',
    },
  ];

  const items = events && events.length > 0 ? events : defaultEvents;

  const getIcon = (type: string) => {
    switch (type) {
      case 'memory':
        return <Brain className="w-4 h-4 text-purple-400" />;
      case 'causal':
        return <GitBranch className="w-4 h-4 text-cyan-400" />;
      case 'simulation':
        return <SplitSquareVertical className="w-4 h-4 text-amber-400" />;
      case 'risk':
      case 'critic':
        return <ShieldAlert className="w-4 h-4 text-rose-400" />;
      case 'approval':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      default:
        return <Bot className="w-4 h-4 text-cyan-400" />;
    }
  };

  return (
    <GlassCard
      header={
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              LIVE INTELLIGENCE STREAM & TIMELINE
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500 flex items-center gap-1">
            <Clock className="w-3 h-3" />
            Real-time feed
          </span>
        </div>
      }
    >
      <div className="space-y-4">
        {items.map((ev, idx) => (
          <div key={ev.id || idx} className="flex items-start gap-3 relative group">
            {idx !== items.length - 1 && (
              <div className="absolute left-4 top-8 bottom-0 w-px bg-slate-800" />
            )}
            <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0 z-10 group-hover:border-cyan-500/40 transition-colors">
              {getIcon(ev.type)}
            </div>
            <div className="flex-1 min-w-0 bg-slate-950/60 rounded-lg p-3 border border-slate-900 hover:border-slate-800 transition-colors">
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="text-xs font-mono font-bold text-slate-200">
                  {ev.agent}
                </span>
                <div className="flex items-center gap-2">
                  {ev.badge && (
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                      {ev.badge}
                    </span>
                  )}
                  <span className="text-[10px] font-mono text-slate-500">
                    {formatRelativeTime(ev.time)}
                  </span>
                </div>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed font-sans">
                {ev.summary}
              </p>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};
