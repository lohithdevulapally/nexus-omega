'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Brain,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Sparkles,
  GitBranch,
  Database,
  RotateCcw,
  Scale,
  Activity,
  FileText,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';

export default function MemoryProofPage() {
  const [selectedIncident, setSelectedIncident] = useState<'acme-payment' | 'db-deadlock'>('acme-payment');

  const proofData = {
    'acme-payment': {
      title: 'ACME Payment Gateway 504 Timeout & Socket Starvation',
      timestamp: '2026-09-28 09:30:00 UTC',
      beforeIncident: {
        hindsightBank: 'nexus-demo',
        storedExperiencesCount: 14,
        keyPrecedent: {
          id: 'exp-2025-10-outage',
          date: '2025-10-14',
          summary: 'Restarting Gateway A during upstream provider outage dumped 4,000 in-flight requests and triggered cascading thundering herd failure.',
          actionTaken: 'RESTART_SERVICE',
          observedOutcome: 'FAILED (Extended outage by 20m, 4,000 lost orders)',
        },
      },
      recalledMemories: [
        {
          id: 'mem-001',
          source: 'Hindsight (bank: nexus-demo)',
          relevance: 0.97,
          confidence: 0.95,
          text: 'Incident #3: ACME transaction failure. Primary gateway connection timeout. Naive service restart failed repeatedly due to sustained provider socket pool exhaustion.',
          contextMatch: 'High (Matching upstream provider error code HTTP 504)',
        },
        {
          id: 'mem-002',
          source: 'Hindsight (bank: nexus-demo)',
          relevance: 0.92,
          confidence: 0.98,
          text: 'Switching traffic to secondary payment rail B bypassed provider socket starvation with zero lost orders.',
          contextMatch: 'High (Valid alternative mitigation pathway)',
        },
      ],
      memoryConflict: {
        hasConflict: true,
        divergence: 'Dec 2024 Memory suggested Restart resolved connection pool deadlock; Oct 2025 Memory proved Restart caused total collapse during sustained provider outage.',
        resolution: 'Contextual Nuance: Telemetry shows current incident matches Oct 2025 provider-level socket starvation. Restart option blocked.',
      },
      memoryInfluence: {
        score: 0.85,
        rating: 'DECISIVE',
        points: [
          { factor: 'Candidate Intervention Formulation', weight: '+20%', detail: 'Memory supplied Secondary Rail B as candidate' },
          { factor: 'Failure Trap Prevention', weight: '+30%', detail: 'Prevented repeating Oct 2025 naive restart trap' },
          { factor: 'Simulation Recurrence Risk Weighting', weight: '+15%', detail: 'Adjusted restart recurrence risk from 10% to 88%' },
          { factor: 'Counterfactual World Divergence', weight: '+15%', detail: 'Grounded Rail B recovery projection in past 99.98% outcome' },
          { factor: 'CriticAgent Adversarial Challenge', weight: '+15%', detail: 'Critic cited past failure to object to operator consensus' },
        ],
      },
      decision: {
        candidateProposed: 'SWITCH_PAYMENT_RAIL',
        rationale: 'Memory-directed bypass of degraded primary processor rail to secondary rail B.',
        criticVerdict: 'APPROVED (Cites Oct 2025 precedent; mandates pre-flight check)',
      },
      action: {
        actionType: 'SWITCH_PAYMENT_RAIL',
        parameters: { target_rail: 'adyen-backup', canary_percentage: 5 },
        approvedBy: 'lead_sre_operator',
        executionResult: 'SUCCESS (Exit Code 0)',
      },
      outcome: {
        recoveryDuration: '2.8 minutes (Projected: 3.0 minutes)',
        primaryMetric: 'Restored Throughput: 99.98%',
        secondaryMetric: 'Lost Transactions: 0',
        customerEscalationAvoided: true,
      },
      newMemory: {
        lessonSynthesized: 'Switching to Secondary Rail B during upstream provider timeouts restored 99.98% transaction throughput in 2.8m with zero lost orders.',
        retainedBank: 'nexus-demo',
        retentionStatus: 'CONFIRMED_IN_HINDSIGHT',
        timestamp: '2026-09-28 09:35:12 UTC',
      },
    },
    'db-deadlock': {
      title: 'Database Read Replica Lock Contention & Latency Spike',
      timestamp: '2026-09-28 11:15:00 UTC',
      beforeIncident: {
        hindsightBank: 'nexus-demo',
        storedExperiencesCount: 15,
        keyPrecedent: {
          id: 'exp-2024-06-db',
          date: '2024-06-22',
          summary: 'Rebuilding indexes under peak traffic caused connection pool saturation and cascaded to write-leader starvation.',
          actionTaken: 'REBUILD_INDEXES',
          observedOutcome: 'FAILED (Cascaded to primary leader crash)',
        },
      },
      recalledMemories: [
        {
          id: 'mem-db-01',
          source: 'Hindsight (bank: nexus-demo)',
          relevance: 0.94,
          confidence: 0.91,
          text: 'Analytical query spikes caused lock queues. Rebuilding indexes under peak load exhausted database connections.',
          contextMatch: 'High (Query latency > 12,000ms on replicas)',
        },
      ],
      memoryConflict: {
        hasConflict: false,
        divergence: 'None. Past precedent consistently advises load-shedding and analytical traffic isolation.',
        resolution: 'Apply analytical traffic shedding; postpone index operations until off-peak.',
      },
      memoryInfluence: {
        score: 0.75,
        rating: 'HIGH',
        points: [
          { factor: 'Candidate Intervention Formulation', weight: '+20%', detail: 'Supplied workload diversion as option' },
          { factor: 'Failure Trap Prevention', weight: '+30%', detail: 'Blocked online index rebuild under peak load' },
          { factor: 'Simulation Recurrence Risk', weight: '+15%', detail: 'Elevated lock contention risk in simulation' },
          { factor: 'CriticAgent Challenge', weight: '+10%', detail: 'Critic challenged aggressive cache flush' },
        ],
      },
      decision: {
        candidateProposed: 'DIVERT_ANALYTICS_TRAFFIC',
        rationale: 'Shed analytical query volume from read replicas to dedicated warehouse.',
        criticVerdict: 'APPROVED (Zero lock contention risk)',
      },
      action: {
        actionType: 'UPDATE_RATE_LIMIT',
        parameters: { route: '/api/v1/analytics', max_concurrent: 10 },
        approvedBy: 'database_admin',
        executionResult: 'SUCCESS (Exit Code 0)',
      },
      outcome: {
        recoveryDuration: '1.4 minutes',
        primaryMetric: 'Replica Latency: Reduced from 12,400ms to 18ms',
        secondaryMetric: 'Lock Queue Depth: 0 locks',
        customerEscalationAvoided: true,
      },
      newMemory: {
        lessonSynthesized: 'Diverting analytical queries during replica lock spikes restored read performance to 18ms without index rebuilds.',
        retainedBank: 'nexus-demo',
        retentionStatus: 'CONFIRMED_IN_HINDSIGHT',
        timestamp: '2026-09-28 11:18:44 UTC',
      },
    },
  };

  const current = proofData[selectedIncident];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-purple-950 via-slate-900 to-indigo-950 border border-purple-500/40 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold">
              Cognitive Lineage & Evidence Audit
            </span>
            <span className="text-xs text-slate-400 font-mono">Core Hackathon Differentiator</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Explicit Memory Proof: End-to-End Decision Lineage
          </h1>
          <p className="text-xs text-slate-300 max-w-2xl mt-1">
            Trace how persistent memory in Hindsight directly informs multi-agent reasoning, alters counterfactual projections, avoids documented failure traps, and synthesizes permanent organizational knowledge.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center p-1 rounded-lg bg-slate-900 border border-slate-700">
            <button
              onClick={() => setSelectedIncident('acme-payment')}
              className={`px-3 py-1.5 rounded text-xs font-mono font-bold transition-all ${
                selectedIncident === 'acme-payment' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Payment Outage
            </button>
            <button
              onClick={() => setSelectedIncident('db-deadlock')}
              className={`px-3 py-1.5 rounded text-xs font-mono font-bold transition-all ${
                selectedIncident === 'db-deadlock' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              DB Deadlock
            </button>
          </div>

          <Link
            href="/demo"
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono border border-slate-700 flex items-center gap-1.5"
          >
            <span>Live Demo</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* The 6-Stage Memory Lineage Flowchart */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-center font-mono">
        <div className="p-3 rounded-lg bg-purple-950/40 border border-purple-500/40">
          <span className="text-[10px] text-purple-400 block font-bold">STAGE 1</span>
          <span className="text-xs text-white font-bold">1. MEMORY</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Precedent in Hindsight</span>
        </div>
        <div className="p-3 rounded-lg bg-cyan-950/40 border border-cyan-500/40">
          <span className="text-[10px] text-cyan-400 block font-bold">STAGE 2</span>
          <span className="text-xs text-white font-bold">2. REASONING</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Context & Conflict</span>
        </div>
        <div className="p-3 rounded-lg bg-indigo-950/40 border border-indigo-500/40">
          <span className="text-[10px] text-indigo-400 block font-bold">STAGE 3</span>
          <span className="text-xs text-white font-bold">3. DECISION</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Candidate & Critic</span>
        </div>
        <div className="p-3 rounded-lg bg-amber-950/40 border border-amber-500/40">
          <span className="text-[10px] text-amber-400 block font-bold">STAGE 4</span>
          <span className="text-xs text-white font-bold">4. ACTION</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Human Approval & Exec</span>
        </div>
        <div className="p-3 rounded-lg bg-blue-950/40 border border-blue-500/40">
          <span className="text-[10px] text-blue-400 block font-bold">STAGE 5</span>
          <span className="text-xs text-white font-bold">5. OUTCOME</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Observed Telemetry</span>
        </div>
        <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/40">
          <span className="text-[10px] text-emerald-400 block font-bold">STAGE 6</span>
          <span className="text-xs text-white font-bold">6. NEW MEMORY</span>
          <span className="text-[10px] text-slate-400 block mt-0.5">Reflection Retained</span>
        </div>
      </div>

      {/* LINEAGE AUDIT DETAILS */}
      <div className="space-y-4">
        {/* Stage 1: Memory Before Incident */}
        <GlassCard glow="purple" header={
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-bold text-purple-400 uppercase">1. MEMORY STATE BEFORE INCIDENT</span>
            <span className="text-slate-400">Bank: {current.beforeIncident.hindsightBank} ({current.beforeIncident.storedExperiencesCount} Experiences)</span>
          </div>
        }>
          <div className="p-3.5 rounded bg-slate-950 border border-purple-500/30 text-xs font-mono space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-purple-300 font-bold">Historical Precedent: {current.beforeIncident.keyPrecedent.id}</span>
              <span className="text-slate-400">{current.beforeIncident.keyPrecedent.date}</span>
            </div>
            <p className="text-slate-200">{current.beforeIncident.keyPrecedent.summary}</p>
            <div className="text-[11px] text-rose-300">Historical Result: {current.beforeIncident.keyPrecedent.observedOutcome}</div>
          </div>
        </GlassCard>

        {/* Stage 2: Recalled Memories & Conflict Detection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <GlassCard glow="cyan" header={<div className="font-mono font-bold text-xs text-cyan-400 uppercase">2A. RECALLED EPISODIC MEMORIES & PROVENANCE</div>}>
            <div className="space-y-2.5">
              {current.recalledMemories.map(mem => (
                <div key={mem.id} className="p-3 rounded bg-slate-950 border border-cyan-500/30 text-xs font-mono space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-cyan-300 font-bold">{mem.id} • {mem.source}</span>
                    <span className="text-emerald-400 font-bold">Relevance: {Math.round(mem.relevance * 100)}%</span>
                  </div>
                  <p className="text-slate-200">{mem.text}</p>
                  <div className="text-[10px] text-slate-400">Context: {mem.contextMatch}</div>
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard glow="rose" header={<div className="font-mono font-bold text-xs text-rose-400 uppercase">2B. CONFLICT DETECTION & CONTEXT NUANCE</div>}>
            <div className="space-y-2 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  current.memoryConflict.hasConflict ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-slate-800 text-slate-300'
                }`}>
                  {current.memoryConflict.hasConflict ? 'CONFLICT DETECTED' : 'UNANIMOUS PRECEDENT'}
                </span>
              </div>
              <p className="text-slate-300 bg-slate-950 p-2.5 rounded border border-slate-800">
                <strong className="text-amber-300 block mb-1">Divergence:</strong>
                {current.memoryConflict.divergence}
              </p>
              <p className="text-emerald-300 bg-emerald-950/20 p-2.5 rounded border border-emerald-900/40">
                <strong className="text-emerald-400 block mb-1">Autonomous Resolution:</strong>
                {current.memoryConflict.resolution}
              </p>
            </div>
          </GlassCard>
        </div>

        {/* Stage 3: Evidence-Based Memory Influence Score */}
        <GlassCard glow="purple" header={
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-bold text-indigo-400 uppercase">3. EVIDENCE-BASED MEMORY INFLUENCE SCORE</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">
              {current.memoryInfluence.rating}: {Math.round(current.memoryInfluence.score * 100)}%
            </span>
          </div>
        }>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-2 text-xs font-mono">
            {current.memoryInfluence.points.map((pt, idx) => (
              <div key={idx} className="p-2.5 rounded bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-[10px] font-bold text-indigo-400 block">{pt.weight}</span>
                <div className="text-[11px] font-bold text-slate-200">{pt.factor}</div>
                <div className="text-[10px] text-slate-400">{pt.detail}</div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Stage 4 & 5: Decision, Action & Outcome */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <GlassCard glow="cyan" header={<div className="font-mono font-bold text-xs text-cyan-400 uppercase">4. FINAL DECISION & CRITIC</div>}>
            <div className="space-y-2 text-xs font-mono">
              <div className="p-2.5 rounded bg-slate-950 border border-cyan-500/30">
                <span className="text-[10px] text-cyan-400 uppercase font-bold block">Selected Intervention</span>
                <span className="text-sm font-bold text-slate-100">{current.decision.candidateProposed}</span>
              </div>
              <p className="text-slate-300 text-[11px]">{current.decision.rationale}</p>
              <div className="p-2 rounded bg-indigo-950/30 border border-indigo-500/30 text-[10px] text-indigo-300">
                <strong>CriticAgent:</strong> {current.decision.criticVerdict}
              </div>
            </div>
          </GlassCard>

          <GlassCard glow="amber" header={<div className="font-mono font-bold text-xs text-amber-400 uppercase">5. CONTROLLED ACTION</div>}>
            <div className="space-y-2 text-xs font-mono">
              <div className="p-2.5 rounded bg-slate-950 border border-amber-500/30">
                <span className="text-[10px] text-amber-400 uppercase font-bold block">Execution State</span>
                <span className="text-xs font-bold text-emerald-300">{current.action.executionResult}</span>
              </div>
              <div className="text-[11px] text-slate-300">
                Authorized by: <strong className="text-slate-100">{current.action.approvedBy}</strong>
              </div>
              <div className="p-2 rounded bg-slate-950 text-[10px] text-slate-400">
                Parameters: {JSON.stringify(current.action.parameters)}
              </div>
            </div>
          </GlassCard>

          <GlassCard glow="emerald" header={<div className="font-mono font-bold text-xs text-emerald-400 uppercase">6. OBSERVED OUTCOME</div>}>
            <div className="space-y-2 text-xs font-mono">
              <div className="p-2.5 rounded bg-slate-950 border border-emerald-500/30">
                <span className="text-[10px] text-emerald-400 uppercase font-bold block">Actual Recovery Duration</span>
                <span className="text-sm font-bold text-emerald-300">{current.outcome.recoveryDuration}</span>
              </div>
              <div className="text-[11px] text-slate-300">
                {current.outcome.primaryMetric}
              </div>
              <div className="text-[10px] text-emerald-400 font-semibold">
                {current.outcome.secondaryMetric}
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Stage 6: Reflection & New Memory Retention */}
        <GlassCard glow="purple" header={
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="font-bold text-purple-400 uppercase">7. POST-INCIDENT REFLECTION & HINDSIGHT RETENTION</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">
              {current.newMemory.retentionStatus}
            </span>
          </div>
        }>
          <div className="p-3.5 rounded bg-slate-950 border border-purple-500/40 text-xs font-mono space-y-2">
            <div className="text-purple-300 font-bold">Synthesized Lesson for Future Incidents:</div>
            <p className="text-slate-200 text-sm italic">&quot;{current.newMemory.lessonSynthesized}&quot;</p>
            <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
              <span>Retained into Bank: <strong>{current.newMemory.retainedBank}</strong></span>
              <span>Timestamp: {current.newMemory.timestamp}</span>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
