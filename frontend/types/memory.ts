export interface MemoryItem {
  id?: string;
  source: string;
  timestamp: string;
  relevance: number;
  confidence: number;
  content: string;
  outcome?: string;
  success?: boolean;
  entity_id?: string;
  entity_type?: string;
  evidence?: Record<string, any>;
}

export interface MemoryConflict {
  conflict_id: string;
  description: string;
  hypothesis_a: {
    description: string;
    source: string;
    outcome?: string;
    confidence: number;
  };
  hypothesis_b: {
    description: string;
    source: string;
    outcome?: string;
    confidence: number;
  };
  resolution_status: 'ambiguous' | 'context_dependent' | 'resolved';
}

export interface ExperienceItem {
  id: string;
  organization_id: string;
  experience_type: string;
  description: string;
  action_taken?: string;
  outcome?: string;
  success: boolean;
  hindsight_bank_id?: string;
  hindsight_document_id?: string;
  metadata?: Record<string, any>;
  created_at?: string;
}

export interface MemorySearchResponse {
  bank_id: string;
  query: string;
  count: number;
  memories: any[];
}

export interface MemoryReflectResponse {
  bank_id: string;
  query: string;
  reflection: string;
  based_on: any[];
}
