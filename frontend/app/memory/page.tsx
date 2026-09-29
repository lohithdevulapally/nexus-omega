'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Brain,
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  Sparkles,
  Clock,
  ArrowRight,
  BookOpen,
  ShieldCheck,
  RefreshCw,
} from 'lucide-react';
import { GlassCard } from '@/components/common/GlassCard';
import { MetricCard } from '@/components/common/MetricCard';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { MemoryEvolutionFlow } from '@/components/memory/MemoryEvolutionFlow';
import { memoryService } from '@/services/memory';
import { ExperienceItem } from '@/types/memory';
import { formatRelativeTime } from '@/lib/utils';

export default function MemoryExplorerPage() {
  const [query, setQuery] = useState<string>('ACME payment gateway timeout');
  const [experiences, setExperiences] = useState<ExperienceItem[]>([]);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [selectedExperience, setSelectedExperience] = useState<ExperienceItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [searching, setSearching] = useState<boolean>(false);
  const [filterType, setFilterType] = useState<string>('all');

  const fetchExperiences = async () => {
    setLoading(true);
    try {
      const data = await memoryService.listExperiences();
      setExperiences(data);
      if (data.length > 0 && !selectedExperience) {
        setSelectedExperience(data[0]);
      }
    } catch {
      // quiet fallback
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) return;
    setSearching(true);
    try {
      const res = await memoryService.searchMemories(query);
      setSearchResults(res.memories || []);
    } catch (err) {
      console.error(err);
    } finally {
      setSearching(false);
    }
  };

  useEffect(() => {
    fetchExperiences();
    handleSearch();
  }, []);

  const filtered = experiences.filter((exp) => {
    if (filterType === 'all') return true;
    if (filterType === 'success') return exp.success === true;
    if (filterType === 'failure') return exp.success === false;
    return exp.experience_type === filterType;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-purple-950/40 to-slate-900 border border-purple-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-widest bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold">
              Persistent Organizational Memory
            </span>
            <span className="text-xs text-slate-400 font-mono">Bank: nexus-demo</span>
          </div>
          <h1 className="text-2xl font-bold font-sans text-slate-100 tracking-tight mt-1">
            Hindsight Memory Explorer & Learned Principles
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Inspect what NEXUS-Ω remembers across past outages, decisions, and reflections. Prevents organizational amnesia and blocks recurring failure traps.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start md:self-auto">
          <Link
            href="/memory/proof"
            className="px-3 py-2 rounded-lg bg-purple-900/60 hover:bg-purple-800 text-purple-200 text-xs font-mono border border-purple-500/40 flex items-center gap-1.5 transition-colors"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
            <span>Decision Lineage Proof</span>
          </Link>
          <button
            onClick={fetchExperiences}
            className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Memory Bank</span>
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="Memories Retained" value="174 Items" subtext="Episodic & Reflective" icon={Brain} color="purple" />
        <MetricCard label="Memories Recalled" value="18 Queries" subtext="Average 0.94 relevance" icon={Sparkles} color="cyan" />
        <MetricCard label="Memories Reflected" value="12 Syntheses" subtext="Lessons in PostgreSQL" icon={BookOpen} color="emerald" />
        <MetricCard label="Failure Traps Intercepted" value="6 Traps" subtext="Zero repeated mistakes" icon={ShieldCheck} color="amber" />
      </div>

      {/* Memory Evolution Flow View */}
      <MemoryEvolutionFlow />

      {/* Search Bar */}
      <GlassCard glow="cyan">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 text-purple-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search Hindsight memory bank by semantic meaning or keywords..."
              className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-purple-400 font-sans shadow-inner"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={searching}
            className="w-full sm:w-auto px-6 py-2.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-purple-950/40"
          >
            <Brain className={`w-4 h-4 ${searching ? 'animate-spin' : ''}`} />
            <span>{searching ? 'QUERYING BANK...' : 'SEARCH HINDSIGHT'}</span>
          </button>
        </div>
      </GlassCard>

      {/* Main 2-Column: Memory List + Selected Memory Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Retained Experiences List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold uppercase text-slate-400">
                RETAINED MEMORIES ({filtered.length})
              </span>
            </div>

            {/* Filter Tabs */}
            <div className="flex items-center gap-1 text-xs font-mono">
              <button
                onClick={() => setFilterType('all')}
                className={`px-2.5 py-1 rounded ${
                  filterType === 'all'
                    ? 'bg-purple-600 text-white font-semibold'
                    : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilterType('success')}
                className={`px-2.5 py-1 rounded ${
                  filterType === 'success'
                    ? 'bg-emerald-600 text-white font-semibold'
                    : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                }`}
              >
                Successes
              </button>
              <button
                onClick={() => setFilterType('failure')}
                className={`px-2.5 py-1 rounded ${
                  filterType === 'failure'
                    ? 'bg-rose-600 text-white font-semibold'
                    : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                }`}
              >
                Failures
              </button>
            </div>
          </div>

          <div className="space-y-3">
            {filtered.map((exp) => {
              const isSelected = selectedExperience?.id === exp.id;
              return (
                <div
                  key={exp.id}
                  onClick={() => setSelectedExperience(exp)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-purple-950/30 border-purple-500/60 shadow-lg shadow-purple-950/30'
                      : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex items-center gap-2">
                      <div
                        className={`p-1 rounded ${
                          exp.success
                            ? 'bg-emerald-500/10 text-emerald-400'
                            : 'bg-rose-500/10 text-rose-400'
                        }`}
                      >
                        {exp.success ? (
                          <CheckCircle2 className="w-4 h-4" />
                        ) : (
                          <XCircle className="w-4 h-4" />
                        )}
                      </div>
                      <span className="text-xs font-mono font-bold text-slate-200 uppercase">
                        {exp.experience_type.replace('_', ' ')}
                      </span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500">
                      {formatRelativeTime(exp.created_at)}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed mb-3">
                    {exp.description}
                  </p>

                  <div className="flex items-center justify-between text-[11px] font-mono pt-2 border-t border-slate-850">
                    <span className="text-purple-400 truncate max-w-md">
                      Action: {exp.action_taken || 'Resolution executed'}
                    </span>
                    <span className="text-slate-500">Bank: {exp.hindsight_bank_id || 'nexus-demo'}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Selected Memory Detail Panel */}
        <div className="space-y-4">
          <div className="text-xs font-mono font-bold uppercase text-slate-400">
            MEMORY INSPECTOR
          </div>

          {selectedExperience ? (
            <GlassCard glow="cyan" className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-purple-500/10 text-purple-300 border border-purple-500/30">
                    {selectedExperience.experience_type}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                      selectedExperience.success
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                    }`}
                  >
                    {selectedExperience.success ? 'POSITIVE OUTCOME' : 'FAILURE TRAP'}
                  </span>
                </div>
                <h3 className="text-sm font-bold text-slate-100 font-sans">
                  {selectedExperience.action_taken || 'Operational Experience'}
                </h3>
              </div>

              {/* What the organization remembers */}
              <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 space-y-1.5">
                <div className="text-[11px] font-mono uppercase text-purple-400 font-semibold">
                  WHAT THE ORGANIZATION REMEMBERS
                </div>
                <p className="text-xs text-slate-300 leading-relaxed font-sans">
                  {selectedExperience.description}
                </p>
              </div>

              {/* What Worked & What Failed */}
              <div className="grid grid-cols-1 gap-2">
                <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-850">
                  <span className="text-[11px] font-mono text-emerald-400 font-semibold">
                    OUTCOME OBSERVED:
                  </span>
                  <div className="text-xs text-slate-300 mt-1">
                    {selectedExperience.outcome || 'Success rate restored.'}
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-850">
                  <span className="text-[11px] font-mono text-cyan-400 font-semibold">
                    HOW THIS MEMORY INFLUENCES SIMULATION:
                  </span>
                  <div className="text-xs text-slate-300 mt-1">
                    Used by CounterfactualEngine to penalize naive restart actions during sustained socket timeouts and promote rail switching.
                  </div>
                </div>
              </div>

              {/* Provenance & ID */}
              <div className="text-[10px] font-mono text-slate-500 pt-2 border-t border-slate-800 space-y-1">
                <div>ID: {selectedExperience.id}</div>
                <div>Document ID: {selectedExperience.hindsight_document_id || 'hindsight_doc_auto'}</div>
                <div>Created: {selectedExperience.created_at || 'Recent'}</div>
              </div>
            </GlassCard>
          ) : (
            <div className="p-8 rounded-xl bg-slate-900/50 border border-slate-800 text-center text-xs text-slate-500 font-mono">
              Select a memory to view organizational context.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
