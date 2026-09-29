'use client';

import React from 'react';
import { Brain, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

interface HindsightEvidenceBadgeProps {
  memoryText?: string;
  outcome?: string;
  confidence?: number;
  relevance?: number;
  timestamp?: string;
  source?: string;
  variant?: 'compact' | 'card';
  lessonsLearned?: string;
}

export const HindsightEvidenceBadge: React.FC<HindsightEvidenceBadgeProps> = ({
  memoryText,
  outcome,
  confidence,
  relevance,
  timestamp,
  source = 'Hindsight Episodic Memory',
  variant = 'compact',
  lessonsLearned,
}) => {
  if (variant === 'compact') {
    return (
      <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-mono">
        <Brain className="w-3.5 h-3.5 text-purple-400 animate-pulse" />
        <span className="font-semibold tracking-wider">HINDSIGHT EVIDENCE</span>
        {confidence !== undefined && (
          <span className="text-purple-200/70 border-l border-purple-500/30 pl-1.5 ml-1">
            {Math.round(confidence * 100)}%
          </span>
        )}
      </div>
    );
  }

  return (
    <div className="p-3.5 rounded-lg bg-gradient-to-r from-purple-950/40 to-slate-900/80 border border-purple-500/40 relative overflow-hidden">
      <div className="absolute top-0 right-0 px-2 py-0.5 bg-purple-600/30 text-purple-300 text-[10px] font-mono rounded-bl border-l border-b border-purple-500/30 flex items-center gap-1">
        <Brain className="w-3 h-3 text-purple-300" />
        HINDSIGHT EVIDENCE
      </div>

      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs font-mono text-purple-400 flex items-center gap-1">
          <Sparkles className="w-3 h-3" />
          {source}
        </span>
        {timestamp && (
          <span className="text-[11px] text-slate-500 font-mono">
            • {timestamp}
          </span>
        )}
      </div>

      {memoryText && (
        <p className="text-sm text-slate-200 leading-relaxed font-sans mb-2">
          {memoryText}
        </p>
      )}

      {outcome && (
        <div className="text-xs bg-slate-950/60 rounded p-2 border border-slate-800 text-slate-300 mb-2">
          <span className="text-purple-400 font-mono font-medium">Historical Outcome: </span>
          {outcome}
        </div>
      )}

      {lessonsLearned && (
        <div className="text-xs bg-emerald-950/30 rounded p-2 border border-emerald-900/40 text-emerald-300 flex items-start gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold font-mono text-emerald-400">Lesson Learned: </span>
            {lessonsLearned}
          </div>
        </div>
      )}

      {(confidence !== undefined || relevance !== undefined) && (
        <div className="flex items-center gap-4 mt-2 pt-2 border-t border-purple-500/20 text-[11px] font-mono text-slate-400">
          {confidence !== undefined && (
            <span>
              Confidence: <strong className="text-purple-300">{Math.round(confidence * 100)}%</strong>
            </span>
          )}
          {relevance !== undefined && (
            <span>
              Relevance: <strong className="text-purple-300">{Math.round(relevance * 100)}%</strong>
            </span>
          )}
        </div>
      )}
    </div>
  );
};
