"""
Lineage Tracker - Tracks part family trees and consciousness lineage.

Maintains the relationships between parts across generations,
enabling understanding of how consciousness flows through part families.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import json
from pathlib import Path

from .inheritance_engine import RelationshipType


@dataclass
class LineageNode:
    """A node in the consciousness lineage tree."""
    part_id: str
    parent_id: Optional[str] = None
    relationship_to_parent: Optional[RelationshipType] = None
    children: List[str] = field(default_factory=list)
    generation: int = 0  # 0 = root, 1 = first generation, etc.
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "part_id": self.part_id,
            "parent_id": self.parent_id,
            "relationship_to_parent": self.relationship_to_parent.value if self.relationship_to_parent else None,
            "children": self.children,
            "generation": self.generation,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LineageNode":
        """Create from dictionary."""
        return cls(
            part_id=data["part_id"],
            parent_id=data.get("parent_id"),
            relationship_to_parent=RelationshipType(data["relationship_to_parent"]) if data.get("relationship_to_parent") else None,
            children=data.get("children", []),
            generation=data.get("generation", 0),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            metadata=data.get("metadata", {})
        )


@dataclass
class FamilyTree:
    """A complete family tree of related parts."""
    root_id: str
    nodes: Dict[str, LineageNode]
    total_generations: int = 0
    total_members: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "root_id": self.root_id,
            "nodes": {pid: node.to_dict() for pid, node in self.nodes.items()},
            "total_generations": self.total_generations,
            "total_members": self.total_members
        }


class LineageTracker:
    """
    Tracks consciousness lineage across part families.

    Enables:
    - Tracing consciousness ancestry
    - Understanding inheritance patterns
    - Visualizing part family trees
    """

    def __init__(self, persist_path: Optional[str] = None):
        """
        Initialize the lineage tracker.

        Args:
            persist_path: Optional path for persisting lineage data.
        """
        self._nodes: Dict[str, LineageNode] = {}
        self._roots: Set[str] = set()  # Parts with no parent
        self._persist_path = Path(persist_path) if persist_path else None

        if self._persist_path and self._persist_path.exists():
            self._load_lineage()

    def register_part(
        self,
        part_id: str,
        parent_id: Optional[str] = None,
        relationship: Optional[RelationshipType] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LineageNode:
        """
        Register a part in the lineage system.

        Args:
            part_id: The ID of the part to register
            parent_id: Optional parent part ID
            relationship: Relationship type to parent
            metadata: Additional metadata about the part

        Returns:
            The created lineage node
        """
        generation = 0
        if parent_id and parent_id in self._nodes:
            generation = self._nodes[parent_id].generation + 1
            # Add this part as a child of the parent
            self._nodes[parent_id].children.append(part_id)

        node = LineageNode(
            part_id=part_id,
            parent_id=parent_id,
            relationship_to_parent=relationship,
            generation=generation,
            metadata=metadata or {}
        )

        self._nodes[part_id] = node

        # Track roots
        if not parent_id:
            self._roots.add(part_id)
        elif part_id in self._roots:
            self._roots.remove(part_id)

        if self._persist_path:
            self._save_lineage()

        return node

    def get_ancestors(self, part_id: str) -> List[LineageNode]:
        """Get all ancestors of a part, from parent to root."""
        ancestors = []
        current_id = part_id

        while current_id in self._nodes:
            node = self._nodes[current_id]
            if node.parent_id and node.parent_id in self._nodes:
                parent_node = self._nodes[node.parent_id]
                ancestors.append(parent_node)
                current_id = node.parent_id
            else:
                break

        return ancestors

    def get_descendants(self, part_id: str) -> List[LineageNode]:
        """Get all descendants of a part (children, grandchildren, etc.)."""
        descendants = []
        to_visit = [part_id]
        visited = set()

        while to_visit:
            current_id = to_visit.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            if current_id in self._nodes:
                node = self._nodes[current_id]
                for child_id in node.children:
                    if child_id in self._nodes and child_id not in visited:
                        descendants.append(self._nodes[child_id])
                        to_visit.append(child_id)

        return descendants

    def get_siblings(self, part_id: str) -> List[LineageNode]:
        """Get all siblings of a part (same parent)."""
        if part_id not in self._nodes:
            return []

        node = self._nodes[part_id]
        if not node.parent_id or node.parent_id not in self._nodes:
            return []

        parent_node = self._nodes[node.parent_id]
        return [
            self._nodes[child_id]
            for child_id in parent_node.children
            if child_id != part_id and child_id in self._nodes
        ]

    def get_family_tree(self, part_id: str) -> FamilyTree:
        """
        Get the complete family tree containing a part.

        Traverses up to find the root, then builds the complete tree.
        """
        # Find the root
        root_id = part_id
        while root_id in self._nodes:
            node = self._nodes[root_id]
            if node.parent_id and node.parent_id in self._nodes:
                root_id = node.parent_id
            else:
                break

        # Build the tree from the root
        tree_nodes = {}
        to_visit = [root_id]
        max_generation = 0

        while to_visit:
            current_id = to_visit.pop(0)
            if current_id not in self._nodes or current_id in tree_nodes:
                continue

            node = self._nodes[current_id]
            tree_nodes[current_id] = node
            max_generation = max(max_generation, node.generation)

            for child_id in node.children:
                if child_id not in tree_nodes:
                    to_visit.append(child_id)

        return FamilyTree(
            root_id=root_id,
            nodes=tree_nodes,
            total_generations=max_generation + 1,
            total_members=len(tree_nodes)
        )

    def get_generation(self, part_id: str) -> Optional[int]:
        """Get the generation number of a part."""
        if part_id not in self._nodes:
            return None
        return self._nodes[part_id].generation

    def get_lineage_path(self, part_id: str) -> List[str]:
        """Get the path from root to part as a list of part IDs."""
        path = [part_id]
        current_id = part_id

        while current_id in self._nodes:
            node = self._nodes[current_id]
            if node.parent_id and node.parent_id in self._nodes:
                path.insert(0, node.parent_id)
                current_id = node.parent_id
            else:
                break

        return path

    def get_roots(self) -> List[LineageNode]:
        """Get all root nodes (parts with no parent)."""
        return [self._nodes[rid] for rid in self._roots if rid in self._nodes]

    def get_statistics(self) -> Dict[str, Any]:
        """Get lineage statistics."""
        relationships = defaultdict(int)
        generations = defaultdict(int)

        for node in self._nodes.values():
            if node.relationship_to_parent:
                relationships[node.relationship_to_parent.value] += 1
            generations[node.generation] += 1

        return {
            "total_parts": len(self._nodes),
            "total_roots": len(self._roots),
            "relationships": dict(relationships),
            "parts_by_generation": dict(generations),
            "max_generation": max(generations.keys()) if generations else 0
        }

    def find_common_ancestor(
        self,
        part_id_1: str,
        part_id_2: str
    ) -> Optional[str]:
        """Find the most recent common ancestor of two parts."""
        ancestors_1 = set(node.part_id for node in self.get_ancestors(part_id_1))
        ancestors_1.add(part_id_1)

        # Walk up from part_id_2 until we find a common ancestor
        current_id = part_id_2
        while current_id:
            if current_id in ancestors_1:
                return current_id

            if current_id in self._nodes:
                node = self._nodes[current_id]
                current_id = node.parent_id
            else:
                break

        return None

    def _save_lineage(self) -> None:
        """Save lineage data to disk."""
        if not self._persist_path:
            return

        self._persist_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "nodes": {pid: node.to_dict() for pid, node in self._nodes.items()},
            "roots": list(self._roots)
        }
        with open(self._persist_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_lineage(self) -> None:
        """Load lineage data from disk."""
        if not self._persist_path or not self._persist_path.exists():
            return

        try:
            with open(self._persist_path, 'r') as f:
                data = json.load(f)

            for pid, node_data in data.get("nodes", {}).items():
                self._nodes[pid] = LineageNode.from_dict(node_data)

            self._roots = set(data.get("roots", []))
        except Exception as e:
            print(f"Error loading lineage: {e}")
