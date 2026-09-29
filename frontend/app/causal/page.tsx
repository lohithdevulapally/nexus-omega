'use client';

import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  Search,
  Activity,
  AlertTriangle,
  ShieldAlert,
  ArrowRight,
  Layers,
  Sparkles,
  RefreshCw,
  X,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { CausalGraphCanvas } from '@/components/causal/CausalGraphCanvas';
import { causalService } from '@/services/causal';
import { CausalNode, CausalEdge, RootCauseResponse, CascadeResponse } from '@/types/causal';

export default function CausalExplorerPage() {
  const [activeTab, setActiveTab] = useState<'graph' | 'root_cause' | 'cascade'>('graph');
  const [nodes, setNodes] = useState<CausalNode[]>([]);
  const [edges, setEdges] = useState<CausalEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<CausalNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<CausalEdge | null>(null);

  // Root Cause State
  const [rootCauseIncident, setRootCauseIncident] = useState<string>('ACME Transaction Failures');
  const [rootCauseData, setRootCauseData] = useState<RootCauseResponse | null>(null);

  // Cascade State
  const [cascadeTrigger, setCascadeTrigger] = useState<string>('Payment Gateway Connection Timeout');
  const [cascadeData, setCascadeData] = useState<CascadeResponse | null>(null);

  const [loading, setLoading] = useState<boolean>(true);

  const fetchGraph = async () => {
    setLoading(true);
    try {
      const g = await causalService.getGraph();
      setNodes(g.nodes || []);
      setEdges(g.edges || []);
      if (g.nodes && g.nodes.length > 0 && !selectedNode) {
        setSelectedNode(g.nodes[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const runRootCause = async () => {
    try {
      const res = await causalService.analyzeRootCause(rootCauseIncident);
      setRootCauseData(res);
    } catch (err) {
      console.error(err);
    }
  };

  const runCascade = async () => {
    try {
      const res = await causalService.analyzeCascade(cascadeTrigger);
      setCascadeData(res);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchGraph();
    runRootCause();
    runCascade();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-cyan-950/40 to-slate-900 border border-cyan-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold">
              Persistent Knowledge Graph
            </span>
            <span className="text-xs text-slate-400 font-mono">PostgreSQL: causal_nodes & causal_edges</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Organizational Causal Intelligence & Blast Radius
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Never confuse correlation with causation. Inspect Bayesian causal links, empirical root causes, and multi-tier downstream impact propagation.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-950 border border-slate-800 self-start md:self-auto">
          <button
            onClick={() => setActiveTab('graph')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
              activeTab === 'graph'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-950/50'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Full Topology
          </button>
          <button
            onClick={() => setActiveTab('root_cause')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
              activeTab === 'root_cause'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-950/50'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Root Cause View
          </button>
          <button
            onClick={() => setActiveTab('cascade')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
              activeTab === 'cascade'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-950/50'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Cascade Blast Radius
          </button>
        </div>
      </div>

      {/* TAB 1: FULL TOPOLOGY (REACT FLOW) */}
      {activeTab === 'graph' && (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3">
            <CausalGraphCanvas
              nodesData={nodes}
              edgesData={edges}
              onSelectNode={(n) => {
                setSelectedNode(n);
                setSelectedEdge(null);
              }}
              onSelectEdge={(e) => {
                setSelectedEdge(e);
                setSelectedNode(null);
              }}
            />
          </div>

          {/* Inspector Side Panel */}
          <div className="space-y-4">
            <div className="text-xs font-mono font-bold uppercase text-slate-400">
              CAUSAL INSPECTOR
            </div>

            {selectedNode && (
              <GlassCard glow="cyan" className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                    {selectedNode.entity_type}
                  </span>
                  <span className="text-[10px] font-mono text-slate-500">Node ID</span>
                </div>
                <h3 className="text-sm font-bold text-slate-100 font-sans">
                  {selectedNode.label}
                </h3>
                <p className="text-xs text-slate-300 font-sans leading-relaxed">
                  {selectedNode.description || 'Organizational entity in active causal graph.'}
                </p>
                <div className="text-[11px] font-mono text-slate-400 border-t border-slate-800 pt-2 space-y-1">
                  <div>Entity ID: {selectedNode.entity_id || selectedNode.id}</div>
                  <div>Created: {selectedNode.created_at || 'Seeded in PostgreSQL'}</div>
                </div>
              </GlassCard>
            )}

            {selectedEdge && (
              <GlassCard glow="rose" className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-rose-500/10 text-rose-300 border border-rose-500/30">
                    {selectedEdge.relationship}
                  </span>
                  <StatusBadge type="confidence" value={selectedEdge.confidence} />
                </div>
                <div className="text-xs text-slate-300 font-mono">
                  From: <strong className="text-slate-100">{selectedEdge.source_node_id.slice(0, 8)}</strong>
                  <br />
                  To: <strong className="text-slate-100">{selectedEdge.target_node_id.slice(0, 8)}</strong>
                </div>

                {selectedEdge.evidence && (
                  <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300 space-y-1.5 font-sans">
                    <span className="font-mono text-[11px] text-cyan-400 font-bold uppercase block">
                      GROUNDED EVIDENCE
                    </span>
                    <p>{selectedEdge.evidence.rationale || 'Derived from empirical event logs and Hindsight memory.'}</p>
                  </div>
                )}
              </GlassCard>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: ROOT CAUSE VIEW */}
      {activeTab === 'root_cause' && (
        <div className="space-y-6">
          <GlassCard glow="cyan">
            <div className="flex flex-col sm:flex-row items-center gap-3">
              <div className="relative flex-1 w-full">
                <Search className="w-4 h-4 text-cyan-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={rootCauseIncident}
                  onChange={(e) => setRootCauseIncident(e.target.value)}
                  placeholder="Incident title to analyze (e.g., 'ACME Transaction Failures')..."
                  className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-cyan-400 font-sans shadow-inner"
                />
              </div>
              <button
                onClick={runRootCause}
                className="w-full sm:w-auto px-6 py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-all shadow-md shadow-cyan-950/40"
              >
                ANALYZE ROOT CAUSE
              </button>
            </div>
          </GlassCard>

          {rootCauseData && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Column 1: Root Causes */}
              <GlassCard glow="rose" header={<div className="font-mono font-bold text-sm text-rose-400 uppercase">1. IDENTIFIED ROOT CAUSES</div>}>
                <div className="space-y-3">
                  {rootCauseData.root_causes.map((rc, idx) => (
                    <div key={idx} className="p-3.5 rounded-lg bg-slate-950/80 border border-rose-500/30 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-mono text-rose-400 font-bold uppercase">{rc.entity_type}</span>
                        <StatusBadge type="confidence" value={rc.confidence} />
                      </div>
                      <h4 className="text-sm font-bold text-slate-100">{rc.label}</h4>
                      <p className="text-xs text-slate-400 font-mono">Relationship: {rc.relationship}</p>
                    </div>
                  ))}
                </div>
              </GlassCard>

              {/* Column 2: Contributing Factors */}
              <GlassCard glow="amber" header={<div className="font-mono font-bold text-sm text-amber-400 uppercase">2. CONTRIBUTING FACTORS</div>}>
                <div className="space-y-3">
                  {rootCauseData.contributing_factors.map((cf, idx) => (
                    <div key={idx} className="p-3.5 rounded-lg bg-slate-950/80 border border-amber-500/30 space-y-1">
                      <span className="text-[10px] font-mono text-amber-400 font-bold uppercase">{cf.entity_type}</span>
                      <h4 className="text-sm font-bold text-slate-100">{cf.label}</h4>
                      <p className="text-xs text-slate-400 font-mono">Relationship: {cf.relationship}</p>
                    </div>
                  ))}
                </div>
              </GlassCard>

              {/* Column 3: Observable Symptoms */}
              <GlassCard glow="cyan" header={<div className="font-mono font-bold text-sm text-cyan-400 uppercase">3. OBSERVABLE SYMPTOMS</div>}>
                <div className="space-y-3">
                  {rootCauseData.symptoms.map((sy, idx) => (
                    <div key={idx} className="p-3.5 rounded-lg bg-slate-950/80 border border-cyan-500/30 space-y-1">
                      <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase">{sy.entity_type}</span>
                      <h4 className="text-sm font-bold text-slate-100">{sy.label}</h4>
                      <p className="text-xs text-slate-400 font-mono">Relationship: {sy.relationship}</p>
                    </div>
                  ))}
                </div>
              </GlassCard>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: CASCADE / BLAST RADIUS VIEW */}
      {activeTab === 'cascade' && (
        <div className="space-y-6">
          <GlassCard glow="cyan">
            <div className="flex flex-col sm:flex-row items-center gap-3">
              <div className="relative flex-1 w-full">
                <Search className="w-4 h-4 text-cyan-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={cascadeTrigger}
                  onChange={(e) => setCascadeTrigger(e.target.value)}
                  placeholder="Trigger event or action to simulate cascade blast radius..."
                  className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-cyan-400 font-sans shadow-inner"
                />
              </div>
              <button
                onClick={runCascade}
                className="w-full sm:w-auto px-6 py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-all shadow-md shadow-cyan-950/40"
              >
                EVALUATE BLAST RADIUS
              </button>
            </div>
          </GlassCard>

          {cascadeData && (
            <GlassCard
              glow="rose"
              header={
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold font-mono text-slate-100 uppercase">
                      DOWNSTREAM CASCADE BLAST RADIUS: {cascadeData.trigger}
                    </span>
                  </div>
                  <StatusBadge type="risk" value={cascadeData.severity} />
                </div>
              }
            >
              <div className="space-y-4">
                <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 flex items-center justify-between">
                  <span>Total Downstream Entities Threatened: <strong className="text-rose-400 text-sm">{cascadeData.total_downstream_entities}</strong></span>
                  <span className="text-slate-500">Max Depth: 5 Hops</span>
                </div>

                <div className="space-y-2">
                  {cascadeData.cascade_paths.map((step, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-slate-950/70 border border-slate-800 flex items-center justify-between text-xs"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-5 h-5 rounded bg-slate-900 border border-slate-700 flex items-center justify-center font-mono text-[10px] text-cyan-400">
                          {step.distance}
                        </span>
                        <div className="font-mono text-slate-200">{step.from_node}</div>
                        <ArrowRight className="w-3.5 h-3.5 text-rose-400" />
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-rose-500/10 text-rose-300 border border-rose-500/20 font-bold">
                          {step.relationship}
                        </span>
                        <ArrowRight className="w-3.5 h-3.5 text-rose-400" />
                        <div className="font-mono text-rose-300 font-semibold">{step.to_node}</div>
                      </div>
                      <span className="text-[10px] font-mono text-slate-500">Hop Distance: {step.distance}</span>
                    </div>
                  ))}
                </div>
              </div>
            </GlassCard>
          )}
        </div>
      )}
    </div>
  );
}
