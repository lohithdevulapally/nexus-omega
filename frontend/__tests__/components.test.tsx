import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { HindsightEvidenceBadge } from '@/components/common/HindsightEvidenceBadge';
import { StatusBadge } from '@/components/common/StatusBadge';
import { MetricCard } from '@/components/common/MetricCard';
import { IntelligenceStatusPanel } from '@/components/dashboard/IntelligenceStatusPanel';

describe('Mission Control UI Components', () => {
  it('renders HindsightEvidenceBadge compact variant', () => {
    render(<HindsightEvidenceBadge confidence={0.95} variant="compact" />);
    expect(screen.getByText('HINDSIGHT EVIDENCE')).toBeInTheDocument();
    expect(screen.getByText('95%')).toBeInTheDocument();
  });

  it('renders HindsightEvidenceBadge card variant with historical outcome', () => {
    render(
      <HindsightEvidenceBadge
        variant="card"
        memoryText="Previous outage: Gateway restart failed due to socket exhaustion."
        outcome="Recurring payment failures."
        lessonsLearned="Differentiate transient deadlocks from sustained outages."
        confidence={0.94}
      />
    );
    expect(screen.getByText(/Previous outage: Gateway restart failed/i)).toBeInTheDocument();
    expect(screen.getByText(/Recurring payment failures/i)).toBeInTheDocument();
    expect(screen.getByText(/Lesson Learned:/i)).toBeInTheDocument();
  });

  it('renders StatusBadge for risk, approval, execution, and confidence', () => {
    const { rerender } = render(<StatusBadge type="risk" value="critical" />);
    expect(screen.getByText(/critical/i)).toBeInTheDocument();

    rerender(<StatusBadge type="approval" value="approved" />);
    expect(screen.getByText('APPROVED')).toBeInTheDocument();

    rerender(<StatusBadge type="execution" value="completed" />);
    expect(screen.getByText('EXECUTED')).toBeInTheDocument();

    rerender(<StatusBadge type="confidence" value={0.92} />);
    expect(screen.getByText('92% CONFIDENCE')).toBeInTheDocument();
  });

  it('renders MetricCard with labels and formatting', () => {
    render(
      <MetricCard
        label="Hindsight Memories"
        value="174 Items"
        subtext="Bank: nexus-demo"
        color="purple"
      />
    );
    expect(screen.getByText('Hindsight Memories')).toBeInTheDocument();
    expect(screen.getByText('174 Items')).toBeInTheDocument();
    expect(screen.getByText('Bank: nexus-demo')).toBeInTheDocument();
  });

  it('renders IntelligenceStatusPanel with live engines', () => {
    const mockHealth = {
      status: 'ok',
      database: 'connected',
      redis: 'connected',
      hindsight: 'connected',
      bank_id: 'nexus-demo',
    };
    render(<IntelligenceStatusPanel health={mockHealth} />);
    expect(screen.getByText('INTELLIGENCE STATUS & ENGINE MESH')).toBeInTheDocument();
    expect(screen.getByText('PostgreSQL State')).toBeInTheDocument();
    expect(screen.getByText('Hindsight Engine')).toBeInTheDocument();
    expect(screen.getByText('Counterfactual Engine')).toBeInTheDocument();
  });
});
