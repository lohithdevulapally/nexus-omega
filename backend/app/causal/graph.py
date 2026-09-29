"""In-Memory Causal Knowledge Graph with Persistence Synchronization."""

import uuid
from typing import Dict, List, Optional, Set, Any
from sqlalchemy.orm import Session

from app.causal.nodes import CausalNodeDTO
from app.causal.edges import CausalEdgeDTO
from app.causal.causal_store import causal_store
from app.core.logging import logger


class CausalKnowledgeGraph:
    """Directed causal knowledge graph supporting multi-hop reasoning, path traversal,

    and cascade analysis.
    """

    def __init__(self, organization_id: Optional[str] = None):
        self.organization_id = organization_id
        self.nodes: Dict[str, CausalNodeDTO] = {}
        self.label_to_id: Dict[str, str] = {}
        self.outgoing: Dict[str, List[CausalEdgeDTO]] = {}
        self.incoming: Dict[str, List[CausalEdgeDTO]] = {}

    def clear(self):
        self.nodes.clear()
        self.label_to_id.clear()
        self.outgoing.clear()
        self.incoming.clear()

    def add_node(self, node: CausalNodeDTO) -> CausalNodeDTO:
        self.nodes[node.id] = node
        self.label_to_id[node.label.lower()] = node.id
        if node.id not in self.outgoing:
            self.outgoing[node.id] = []
        if node.id not in self.incoming:
            self.incoming[node.id] = []
        return node

    def add_edge(self, edge: CausalEdgeDTO) -> CausalEdgeDTO:
        if edge.source_node_id not in self.outgoing:
            self.outgoing[edge.source_node_id] = []
        if edge.target_node_id not in self.incoming:
            self.incoming[edge.target_node_id] = []

        # Avoid duplicates in memory
        existing = [
            e for e in self.outgoing[edge.source_node_id]
            if e.target_node_id == edge.target_node_id and e.relationship == edge.relationship
        ]
        if not existing:
            self.outgoing[edge.source_node_id].append(edge)
            self.incoming[edge.target_node_id].append(edge)
        return edge

    def get_node(self, node_id: str) -> Optional[CausalNodeDTO]:
        return self.nodes.get(node_id)

    def find_node(self, identifier: str) -> Optional[CausalNodeDTO]:
        """Looks up a node by id or case-insensitive label match."""
        if identifier in self.nodes:
            return self.nodes[identifier]
        nid = self.label_to_id.get(identifier.lower())
        if nid:
            return self.nodes.get(nid)
        # Substring fuzzy match
        for label, nid in self.label_to_id.items():
            if identifier.lower() in label:
                return self.nodes.get(nid)
        return None

    def sync_from_db(self, db: Session, organization_id: uuid.UUID) -> "CausalKnowledgeGraph":
        """Loads all nodes and edges from PostgreSQL into this graph."""
        self.clear()
        self.organization_id = str(organization_id)
        nodes, edges = causal_store.load_graph_data(db, organization_id)
        for n in nodes:
            self.add_node(n)
        for e in edges:
            self.add_edge(e)
        logger.info(
            f"[CAUSAL_GRAPH_UPDATE] Loaded {len(self.nodes)} nodes and {len(edges)} edges for Org={organization_id}"
        )
        return self

    def find_paths(
        self, source_id: str, target_id: str, max_depth: int = 5
    ) -> List[Dict[str, Any]]:
        """Finds all directed causal paths from source to target up to max_depth."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return []

        results: List[Dict[str, Any]] = []

        def dfs(current_id: str, current_path: List[Dict[str, Any]], visited: Set[str], accumulated_confidence: float):
            if len(current_path) > max_depth:
                return
            if current_id == target_id and current_path:
                path_steps = []
                for step in current_path:
                    src = self.nodes.get(step["source_id"])
                    tgt = self.nodes.get(step["target_id"])
                    path_steps.append({
                        "source": src.label if src else step["source_id"],
                        "relationship": step["relationship"],
                        "target": tgt.label if tgt else step["target_id"],
                        "confidence": step["confidence"],
                        "evidence": step["evidence"],
                    })
                results.append({
                    "path_length": len(current_path),
                    "confidence": round(accumulated_confidence, 3),
                    "steps": path_steps,
                })
                return

            visited.add(current_id)
            for edge in self.outgoing.get(current_id, []):
                next_id = edge.target_node_id
                if next_id not in visited:
                    next_confidence = accumulated_confidence * edge.confidence
                    current_path.append({
                        "source_id": edge.source_node_id,
                        "target_id": edge.target_node_id,
                        "relationship": edge.relationship,
                        "confidence": edge.confidence,
                        "evidence": edge.evidence,
                    })
                    dfs(next_id, current_path, visited, next_confidence)
                    current_path.pop()
            visited.remove(current_id)

        dfs(source_id, [], set(), 1.0)
        # Sort by highest confidence and shortest length
        results.sort(key=lambda p: (-p["confidence"], p["path_length"]))
        return results

    def get_ancestors(self, node_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Finds all upstream causes of a given node."""
        ancestors: List[Dict[str, Any]] = []
        visited: Set[str] = set()
        queue = [(node_id, 0, 1.0)]

        while queue:
            curr_id, depth, conf = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.incoming.get(curr_id, []):
                parent_id = edge.source_node_id
                if parent_id not in visited:
                    visited.add(parent_id)
                    parent_node = self.nodes.get(parent_id)
                    edge_conf = conf * edge.confidence
                    ancestors.append({
                        "node_id": parent_id,
                        "label": parent_node.label if parent_node else parent_id,
                        "entity_type": parent_node.entity_type if parent_node else "Unknown",
                        "relationship": edge.relationship,
                        "distance": depth + 1,
                        "confidence": round(edge_conf, 3),
                        "evidence": edge.evidence,
                    })
                    queue.append((parent_id, depth + 1, edge_conf))

        return ancestors

    def get_descendants(self, node_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Finds all downstream cascading effects of a given node."""
        descendants: List[Dict[str, Any]] = []
        visited: Set[str] = set()
        queue = [(node_id, 0, 1.0)]

        while queue:
            curr_id, depth, conf = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self.outgoing.get(curr_id, []):
                child_id = edge.target_node_id
                if child_id not in visited:
                    visited.add(child_id)
                    child_node = self.nodes.get(child_id)
                    edge_conf = conf * edge.confidence
                    descendants.append({
                        "node_id": child_id,
                        "label": child_node.label if child_node else child_id,
                        "entity_type": child_node.entity_type if child_node else "Unknown",
                        "relationship": edge.relationship,
                        "distance": depth + 1,
                        "confidence": round(edge_conf, 3),
                        "evidence": edge.evidence,
                    })
                    queue.append((child_id, depth + 1, edge_conf))

        return descendants
