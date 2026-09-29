'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Search,
  Brain,
  ShieldAlert,
  GitBranch,
  Play,
  CheckCircle,
  Clock,
  Sparkles,
  Command,
  X,
} from 'lucide-react';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose }) => {
  const router = useRouter();
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) {
          onClose();
        } else {
          // Open
        }
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const quickNav = [
    { label: 'Run Live ACME Investigation', path: '/demo', icon: Play, category: 'Scenarios' },
    { label: 'Autonomous Investigation Console', path: '/investigations', icon: Sparkles, category: 'Intelligence' },
    { label: 'Causal Knowledge Graph', path: '/causal', icon: GitBranch, category: 'Intelligence' },
    { label: 'What-If Counterfactual Cockpit', path: '/simulations', icon: Sparkles, category: 'Intelligence' },
    { label: 'Organizational Memory Explorer', path: '/memory', icon: Brain, category: 'Memory' },
    { label: 'Human Approval Queue', path: '/approvals', icon: Clock, category: 'Operations' },
    { label: 'Controlled Action Log', path: '/actions', icon: CheckCircle, category: 'Operations' },
    { label: 'Decisions Intelligence Trace', path: '/decisions', icon: ShieldAlert, category: 'Decisions' },
    { label: 'Organizational Time Machine', path: '/time-machine', icon: Clock, category: 'Simulation' },
    { label: 'System Health & Probes', path: '/system', icon: ShieldAlert, category: 'System' },
  ];

  const filtered = query.trim()
    ? quickNav.filter((item) => item.label.toLowerCase().includes(query.toLowerCase()) || item.category.toLowerCase().includes(query.toLowerCase()))
    : quickNav;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-150">
      <div className="w-full max-w-2xl rounded-xl bg-slate-900 border border-slate-700 shadow-2xl overflow-hidden glass-panel-elevated">
        <div className="flex items-center px-4 py-3.5 border-b border-slate-800">
          <Search className="w-5 h-5 text-cyan-400 mr-3" />
          <input
            autoFocus
            type="text"
            placeholder="Search decisions, memories, causal paths, actions, or jump to route... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 focus:outline-none text-sm font-sans"
          />
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="max-h-96 overflow-y-auto p-2">
          {filtered.length === 0 ? (
            <div className="py-8 text-center text-sm text-slate-500">
              No matching intelligence entities or navigation actions found.
            </div>
          ) : (
            <div className="space-y-1">
              {filtered.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      router.push(item.path);
                      onClose();
                    }}
                    className="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left text-sm text-slate-300 hover:text-white hover:bg-slate-800/90 transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-1.5 rounded bg-slate-800 border border-slate-700 text-cyan-400 group-hover:border-cyan-500/40">
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="font-medium">{item.label}</span>
                    </div>
                    <span className="text-xs font-mono text-slate-500 group-hover:text-slate-400">
                      {item.category}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="px-4 py-2 bg-slate-950/70 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500 font-mono">
          <div className="flex items-center gap-2">
            <span className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px]">
              ↑↓
            </span>
            <span>Navigate</span>
            <span className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px]">
              ENTER
            </span>
            <span>Select</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Command className="w-3 h-3 text-cyan-400" />
            <span>NEXUS-Ω Enterprise Cockpit</span>
          </div>
        </div>
      </div>
    </div>
  );
};
