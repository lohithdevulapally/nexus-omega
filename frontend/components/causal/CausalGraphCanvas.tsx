'use client';

import React, { useMemo } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { CausalNode, CausalEdge } from '@/types/causal';

interface CausalGraphCanvasProps {
  nodesData: CausalNode[];
  edgesData: CausalEdge[];
  onSelectNode?: (node: CausalNode) => void;
  onSelectEdge?: (edge: CausalEdge) => void;
}

export const CausalGraphCanvas: React.FC<CausalGraphCanvasProps> = ({
  nodesData,
  edgesData,
  onSelectNode,
  onSelectEdge,
}) => {
  // Convert CausalNodes to React Flow nodes with layout coordinates
  const initialNodes: Node[] = useMemo(() => {
    // Basic circular or tiered positioning
    const count = nodesData.length;
    return nodesData.map((n, idx) => {
      const angle = (idx / Math.max(count, 1)) * 2 * Math.PI;
      const radius = 280;
      const x = 400 + Math.cos(angle) * radius;
      const y = 300 + Math.sin(angle) * radius;

      const isRoot = n.entity_type === 'incident' || n.entity_type === 'failure';
      const isRisk = n.entity_type === 'risk';
      const isAction = n.entity_type === 'action';

      const borderColor = isRoot
        ? '#f43f5e'
        : isRisk
        ? '#f59e0b'
        : isAction
        ? '#10b981'
        : '#06b6d4';

      return {
        id: n.id,
        data: {
          label: (
            <div className="p-2.5 text-left font-sans">
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
                {n.entity_type}
              </div>
              <div className="text-xs font-semibold text-slate-100 mt-0.5 line-clamp-2">
                {n.label}
              </div>
            </div>
          ),
          raw: n,
        },
        position: { x, y },
        style: {
          background: '#0B1220',
          border: `1.5px solid ${borderColor}`,
          borderRadius: '10px',
          color: '#f1f5f9',
          width: 180,
          boxShadow: `0 4px 20px -5px ${borderColor}33`,
        },
      };
    });
  }, [nodesData]);

  // Convert CausalEdges to React Flow edges with labels and markers
  const initialEdges: Edge[] = useMemo(() => {
    return edgesData.map((e) => {
      const isCauses = e.relationship === 'CAUSES' || e.relationship === 'TRIGGERS';
      const isResolved = e.relationship === 'RESOLVED_BY' || e.relationship === 'RESULTED_IN';
      const strokeColor = isCauses ? '#f43f5e' : isResolved ? '#10b981' : '#06b6d4';

      return {
        id: e.id,
        source: e.source_node_id,
        target: e.target_node_id,
        label: `${e.relationship} (${Math.round(e.confidence * 100)}%)`,
        labelStyle: { fill: strokeColor, fontSize: 10, fontFamily: 'monospace', fontWeight: 600 },
        labelBgStyle: { fill: '#060A12', fillOpacity: 0.85 },
        labelBgPadding: [4, 2] as [number, number],
        labelBgBorderRadius: 4,
        animated: isCauses,
        style: { stroke: strokeColor, strokeWidth: 2 },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: strokeColor,
          width: 16,
          height: 16,
        },
        data: { raw: e },
      };
    });
  }, [edgesData]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden border border-slate-800 bg-[#060A12] relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => onSelectNode?.(node.data.raw as CausalNode)}
        onEdgeClick={(_, edge) => onSelectEdge?.(edge.data?.raw as CausalEdge)}
        fitView
      >
        <Background color="#1E2B45" gap={20} size={1} />
        <Controls />
      </ReactFlow>

      {/* Legend Badge Overlay */}
      <div className="absolute top-4 left-4 p-3 rounded-lg bg-slate-950/80 backdrop-blur-md border border-slate-800 text-xs font-mono space-y-1 z-10">
        <div className="font-bold text-slate-300 text-[11px] mb-1.5 uppercase">RELATIONSHIP LEGEND</div>
        <div className="flex items-center gap-2 text-rose-400">
          <span className="w-2.5 h-0.5 bg-rose-500 inline-block" />
          <span>CAUSES / TRIGGERS (Destructive)</span>
        </div>
        <div className="flex items-center gap-2 text-emerald-400">
          <span className="w-2.5 h-0.5 bg-emerald-500 inline-block" />
          <span>RESOLVED_BY / RESULTED_IN</span>
        </div>
        <div className="flex items-center gap-2 text-cyan-400">
          <span className="w-2.5 h-0.5 bg-cyan-500 inline-block" />
          <span>DEPENDS_ON / CORRELATED_WITH</span>
        </div>
      </div>
    </div>
  );
};
