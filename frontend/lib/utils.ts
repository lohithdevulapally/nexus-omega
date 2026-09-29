import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString?: string): string {
  if (!dateString) return '—';
  try {
    const d = new Date(dateString);
    return d.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  } catch {
    return dateString;
  }
}

export function formatRelativeTime(dateString?: string): string {
  if (!dateString) return '—';
  try {
    const now = new Date();
    const past = new Date(dateString);
    const diffMs = now.getTime() - past.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    if (diffSec < 60) return `${diffSec}s ago`;
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHr = Math.floor(diffMin / 60);
    if (diffHr < 24) return `${diffHr}h ago`;
    return `${Math.floor(diffHr / 24)}d ago`;
  } catch {
    return dateString;
  }
}

export function getRiskColor(level?: string) {
  switch (level?.toLowerCase()) {
    case 'critical':
      return {
        badge: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
        text: 'text-rose-400',
        border: 'border-rose-500/40',
        dot: 'bg-rose-500',
      };
    case 'high':
      return {
        badge: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
        text: 'text-amber-400',
        border: 'border-amber-500/40',
        dot: 'bg-amber-500',
      };
    case 'medium':
      return {
        badge: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
        text: 'text-cyan-400',
        border: 'border-cyan-500/40',
        dot: 'bg-cyan-500',
      };
    default:
      return {
        badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
        text: 'text-emerald-400',
        border: 'border-emerald-500/40',
        dot: 'bg-emerald-500',
      };
  }
}
