'use client';

import React, { useState, useEffect } from 'react';
import {
  History,
  Clock,
  Calendar,
  Layers,
  Sparkles,
  ArrowRight,
  Database,
  Brain,
  ShieldAlert,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { MetricCard } from '@/components/common/MetricCard';
import { simulationService } from '@/services/simulations';
import { ReconstructResponse } from '@/types/simulation';

export default function TimeMachinePage() {
  const timePresets = [
    { label: 'September 1, 2026', iso: '2026-09-01T00:00:00Z' },
    { label: 'September 5, 2026', iso: '2026-09-05T12:00:00Z' },
    { label: 'September 10, 2026', iso: '2026-09-10T12:00:00Z' },
    { label: 'September 15, 2026', iso: '2026-09-15T12:00:00Z' },
    { label: 'September 20, 2026', iso: '2026-09-20T12:00:00Z' },
    { label: 'Live Today', iso: new Date().toISOString() },
  ];

  const [selectedTimeIdx, setSelectedTimeIdx] = useState<number>(3);
  const [reconstructedState, setReconstructedState] = useState<ReconstructResponse | null>(null);
  const [compareWithToday, setCompareWithToday] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchReconstruction = async (iso: string) => {
    setLoading(true);
    try {
      const res = await simulationService.reconstructState(iso);
      setReconstructedState(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReconstruction(timePresets[selectedTimeIdx].iso);
  }, [selectedTimeIdx]);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-bold">
              Temporal State Reconstruction
            </span>
            <span className="text-xs text-slate-400 font-mono">POST /simulation/reconstruct</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Organizational Time Machine & State Diffing
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Rewind organizational state to any historical point in time. Inspect what customers, events, decisions, and Hindsight memories existed as of that exact moment.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start md:self-auto">
          <button
            onClick={() => setCompareWithToday(!compareWithToday)}
            className={`px-3 py-2 rounded-lg text-xs font-mono border transition-all ${
              compareWithToday
                ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-950/50'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            {compareWithToday ? 'Diff with Today: ON' : 'Diff with Today: OFF'}
          </button>
        </div>
      </div>

      {/* Interactive Time Slider */}
      <GlassCard glow="cyan">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-mono font-bold uppercase text-slate-200">
                TEMPORAL CHECKPOINT: {timePresets[selectedTimeIdx].label}
              </span>
            </div>
            <span className="text-[11px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/30">
              {timePresets[selectedTimeIdx].iso}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
            {timePresets.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedTimeIdx(idx)}
                className={`p-3 rounded-lg border text-center transition-all ${
                  selectedTimeIdx === idx
                    ? 'bg-indigo-600/30 border-indigo-400 text-white font-bold shadow-md shadow-indigo-950/50'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                <div className="text-xs font-mono">{preset.label}</div>
                <div className="text-[10px] text-slate-500 font-mono mt-1">
                  {idx === timePresets.length - 1 ? 'Live Present' : `T - ${5 * (timePresets.length - 1 - idx)}d`}
                </div>
              </button>
            ))}
          </div>
        </div>
      </GlassCard>

      {/* Reconstructed State Metrics */}
      {reconstructedState && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              label="Reconstructed Customers"
              value={reconstructedState.customers?.length || 0}
              subtext={compareWithToday ? 'Active on that date' : undefined}
              icon={Database}
              color="cyan"
            />
            <MetricCard
              label="Historical Events"
              value={reconstructedState.events?.length || 0}
              subtext="Occurred prior to checkpoint"
              icon={Layers}
              color="purple"
            />
            <MetricCard
              label="Active Known Risks"
              value={reconstructedState.known_risks?.length || 0}
              subtext="Organizational exposure"
              icon={ShieldAlert}
              color="amber"
            />
            <MetricCard
              label="Hindsight Memories"
              value={reconstructedState.memories?.length || 0}
              subtext="Known to system at T"
              icon={Brain}
              color="emerald"
            />
          </div>

          {/* Temporal State Inspection Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Known Risks as of Checkpoint */}
            <GlassCard
              header={
                <div className="flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-amber-400" />
                  <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                    KNOWN ORGANIZATIONAL RISKS AS OF {timePresets[selectedTimeIdx].label}
                  </h3>
                </div>
              }
            >
              <div className="space-y-2.5">
                {reconstructedState.known_risks?.length === 0 ? (
                  <div className="text-xs font-mono text-slate-500 py-4 text-center">
                    No active risks recorded at this temporal point.
                  </div>
                ) : (
                  reconstructedState.known_risks?.map((risk, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300 flex items-center justify-between"
                    >
                      <span className="font-sans">{risk}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 font-bold uppercase">
                        ACTIVE AT T
                      </span>
                    </div>
                  ))
                )}
              </div>
            </GlassCard>

            {/* Historical Events prior to Checkpoint */}
            <GlassCard
              header={
                <div className="flex items-center gap-2">
                  <Layers className="w-4 h-4 text-cyan-400" />
                  <h3 className="text-sm font-bold font-mono text-slate-100 uppercase tracking-wider">
                    EVENTS LOGGED PRIOR TO CHECKPOINT
                  </h3>
                </div>
              }
            >
              <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                {reconstructedState.events?.length === 0 ? (
                  <div className="text-xs font-mono text-slate-500 py-4 text-center">
                    No historical events recorded before this date.
                  </div>
                ) : (
                  reconstructedState.events?.map((ev, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300 space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[10px] text-cyan-400 uppercase font-bold">
                          {ev.event_type}
                        </span>
                        <span className="text-[10px] font-mono text-slate-500">
                          {new Date(ev.timestamp).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="font-semibold text-slate-100">{ev.title}</div>
                    </div>
                  ))
                )}
              </div>
            </GlassCard>
          </div>
        </div>
      )}
    </div>
  );
}
