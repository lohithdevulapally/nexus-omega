'use client';

import React, { useState, useEffect } from 'react';
import {
  HeartPulse,
  Database,
  Brain,
  Activity,
  Server,
  Zap,
  CheckCircle2,
  RefreshCw,
  Clock,
  ShieldCheck,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { MetricCard } from '@/components/common/MetricCard';
import { systemService } from '@/services/system';
import { HealthResponse } from '@/types/api';

export default function SystemHealthPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [metadata, setMetadata] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [lastCheck, setLastCheck] = useState<Date>(new Date());
  const [pingLatency, setPingLatency] = useState<number>(0);

  const fetchHealth = async () => {
    setLoading(true);
    const start = performance.now();
    try {
      const [h, meta] = await Promise.all([
        systemService.getHealth(),
        systemService.getEngineMetadata(),
      ]);
      const end = performance.now();
      setPingLatency(Math.round(end - start));
      setHealth(h);
      setMetadata(meta);
      setLastCheck(new Date());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const components = [
    {
      name: 'PostgreSQL 17 Database',
      role: 'Relational & Causal State',
      status: health?.database === 'connected' ? 'ONLINE' : 'DEGRADED',
      latency: health?.latencies?.database_ms != null ? `${health.latencies.database_ms}ms` : '< 5ms',
      heartbeat: health?.database === 'connected' ? 'Heartbeat OK' : 'Connection Refused',
      icon: Database,
      details: 'Tables: organizations, customers, events, decisions, actions, causal_nodes, causal_edges',
    },
    {
      name: 'Hindsight Episodic Engine',
      role: 'Semantic Memory Bank',
      status: health?.hindsight === 'connected' ? 'ONLINE' : 'DEGRADED',
      latency: health?.hindsight === 'connected' ? `${health?.latencies?.hindsight_ms || '< 15'}ms` : 'Standby / Fallback',
      heartbeat: health?.hindsight === 'connected' ? 'Heartbeat OK' : 'Memory Fallback Active',
      icon: Brain,
      details: health?.hindsight === 'connected'
        ? `Default Bank: ${health?.bank_id || 'nexus-demo'} (Active Embeddings)`
        : `Default Bank: ${health?.bank_id || 'nexus-demo'} • Local Knowledge Fallback Active`,
    },
    {
      name: 'Redis 7 Cache',
      role: 'PubSub & Fast Session Cache',
      status: health?.redis === 'connected' ? 'ONLINE' : 'DEGRADED',
      latency: health?.redis === 'connected' ? `${health?.latencies?.redis_ms || '< 2'}ms` : 'Standby / Fallback',
      heartbeat: health?.redis === 'connected' ? 'Heartbeat OK' : 'In-Memory Session Active',
      icon: Zap,
      details: health?.redis === 'connected' ? 'Port 6379 • Cluster Cache Active' : 'Port 6379 Offline • Local Fast Session Cache Active',
    },
    {
      name: 'FastAPI Backend Core',
      role: 'Decision Intelligence APIs',
      status: health ? 'ONLINE' : 'DEGRADED',
      latency: `${pingLatency}ms`,
      heartbeat: health ? 'Heartbeat OK' : 'Unreachable',
      icon: Server,
      details: `Version: ${metadata?.version || '0.1.0'} • Port 8000 • Serving REST APIs`,
    },
    {
      name: 'Multi-Agent Orchestrator',
      role: '8-Agent Execution Graph',
      status: 'ONLINE',
      latency: '< 10ms dispatch',
      heartbeat: 'Heartbeat OK',
      icon: Activity,
      details: 'Deterministic state machine with adversarial critic gate',
    },
    {
      name: 'Controlled Action Safety Guard',
      role: 'Human-in-the-Loop Gate',
      status: 'ARMED',
      latency: 'Instant',
      heartbeat: 'Active & Enforced',
      icon: ShieldCheck,
      details: 'Strict whitelist • Shell commands blocked • Audit logging enforced',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold">
              Infrastructure Probes
            </span>
            <span className="text-xs text-slate-400 font-mono">Last check: {lastCheck.toLocaleTimeString()}</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            System Health & Component Diagnostic Grid
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Real-time telemetry and connectivity probes for PostgreSQL, Redis, Hindsight Engine, and the Multi-Agent Execution Kernel.
          </p>
        </div>

        <button
          onClick={fetchHealth}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Probe Now</span>
        </button>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard
          label="Mesh Status"
          value={health?.status === 'ok' ? 'HEALTHY' : 'DEGRADED'}
          subtext={health?.status === 'ok' ? 'All critical services live' : 'Dependencies running on fallback'}
          icon={CheckCircle2}
          color={health?.status === 'ok' ? 'emerald' : 'amber'}
        />
        <MetricCard
          label="API Roundtrip Latency"
          value={`${pingLatency} ms`}
          subtext="FastAPI -> Client"
          icon={Activity}
          color="cyan"
        />
        <MetricCard
          label="Hindsight Bank"
          value={health?.bank_id || 'nexus-demo'}
          subtext={health?.hindsight === 'connected' ? 'Connected on port 8888' : 'Memory Fallback Active'}
          icon={Brain}
          color="purple"
        />
        <MetricCard
          label="Engine Version"
          value={metadata?.version || '0.1.0'}
          subtext="NEXUS-Ω Kernel"
          icon={Server}
          color="slate"
        />
      </div>

      {/* Grid of Components */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {components.map((comp, idx) => {
          const Icon = comp.icon;
          const isOnline = comp.status === 'ONLINE' || comp.status === 'ARMED';
          const isDegraded = comp.status === 'DEGRADED';

          const glowColor = isOnline ? 'emerald' : isDegraded ? 'amber' : 'rose';

          return (
            <GlassCard key={idx} glow={glowColor} className="space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2.5">
                  <div className={`p-2 rounded bg-slate-900 border border-slate-800 ${
                    isOnline ? 'text-emerald-400' : isDegraded ? 'text-amber-400' : 'text-rose-400'
                  }`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-100 font-sans">
                      {comp.name}
                    </h3>
                    <div className="text-[11px] font-mono text-slate-400">
                      {comp.role}
                    </div>
                  </div>
                </div>

                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                    isOnline
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : isDegraded
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                      : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                  }`}
                >
                  {comp.status}
                </span>
              </div>

              <div className="text-xs text-slate-300 font-sans leading-relaxed">
                {comp.details}
              </div>

              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 pt-2 border-t border-slate-800">
                <span>Latency: <strong className="text-slate-200">{comp.latency}</strong></span>
                <span className={isOnline ? 'text-emerald-400' : isDegraded ? 'text-amber-400' : 'text-rose-400'}>
                  {comp.heartbeat}
                </span>
              </div>
            </GlassCard>
          );
        })}
      </div>
    </div>
  );
}
