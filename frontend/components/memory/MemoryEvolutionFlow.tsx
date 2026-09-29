'use client';

import React from 'react';
import { GlassCard } from '@/components/common/GlassCard';
import { ArrowRight, Brain, Sparkles, CheckCircle2, History, ShieldAlert } from 'lucide-react';

export const MemoryEvolutionFlow: React.FC = () => {
  const steps = [
    {
      stage: '1. OPERATIONAL EXPERIENCE',
      title: 'Real Incident Occurs',
      desc: 'Gateway timeout causes payment failure spikes on primary ACME rail.',
      icon: ShieldAlert,
      color: 'border-rose-500/40 text-rose-400 bg-rose-500/10',
    },
    {
      stage: '2. REFLECTION & RETENTION',
      title: 'Multi-Agent Critique',
      desc: 'Critique & Reflection agents isolate why naive restart failed vs rail switch recovery.',
      icon: Sparkles,
      color: 'border-cyan-500/40 text-cyan-400 bg-cyan-500/10',
    },
    {
      stage: '3. LESSON SYNTHESIS',
      title: 'Contextual Rule Extraction',
      desc: 'Never restart during sustained socket exhaustion; verify Rail B and reroute.',
      icon: CheckCircle2,
      color: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10',
    },
    {
      stage: '4. HINDSIGHT EMBEDDING',
      title: 'Permanent Organizational Memory',
      desc: 'Dual-index semantic memory stored in bank nexus-demo with provenance.',
      icon: Brain,
      color: 'border-purple-500/40 text-purple-400 bg-purple-500/10',
    },
    {
      stage: '5. FUTURE DECISION REASONING',
      title: 'Anti-Failure Protection',
      desc: 'Subsequent incidents recall historical failure analogue before committing action.',
      icon: History,
      color: 'border-amber-500/40 text-amber-400 bg-amber-500/10',
    },
  ];

  return (
    <GlassCard
      header={
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-slate-100 uppercase">
              ORGANIZATIONAL MEMORY EVOLUTION & CONTINUOUS LEARNING LOOP
            </h3>
          </div>
          <span className="text-[11px] font-mono text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
            Hindsight Integration
          </span>
        </div>
      }
    >
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
        {steps.map((st, idx) => {
          const Icon = st.icon;
          return (
            <div
              key={idx}
              className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 flex flex-col justify-between relative group hover:border-purple-500/40 transition-colors"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-1.5 rounded ${st.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  {idx < steps.length - 1 && (
                    <ArrowRight className="w-4 h-4 text-slate-600 hidden md:block" />
                  )}
                </div>
                <div className="text-[10px] font-mono text-purple-400 font-bold uppercase tracking-wider mb-1">
                  {st.stage}
                </div>
                <h4 className="text-xs font-bold text-slate-100 mb-1">
                  {st.title}
                </h4>
                <p className="text-[11px] text-slate-400 leading-relaxed font-sans">
                  {st.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
};
