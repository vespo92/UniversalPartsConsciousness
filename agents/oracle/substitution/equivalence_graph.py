"""
ORACLE Equivalence Graph
Graph database for managing part equivalence relationships.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
from datetime import datetime
import json


class EquivalenceType(Enum):
    """Type of equivalence relationship."""
    IDENTICAL = "IDENTICAL"              # Same part, different manufacturer
    INTERCHANGEABLE = "INTERCHANGEABLE"  # Direct replacement
    FUNCTIONAL = "FUNCTIONAL"            # Same function, minor differences
    SUPERSEDES = "SUPERSEDES"            # New part replaces old
    SUPERSEDED_BY = "SUPERSEDED_BY"      # Old part replaced by new
    SIMILAR = "SIMILAR"                  # Similar but not interchangeable
    CROSS_REFERENCE = "CROSS_REFERENCE"  # Manufacturer cross-reference


@dataclass
class EquivalenceRelation:
    """A relationship between two parts."""
    source_id: str
    target_id: str
    relation_type: EquivalenceType
    confidence: float  # 0.0 to 1.0
    bidirectional: bool

    # Metadata
    source_data: str  # "manufacturer", "community", "calculated"
    verified: bool
    verification_count: int
    created_at: datetime
    updated_at: datetime

    # Differences
    differences: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PartNode:
    """A part node in the equivalence graph."""
    part_id: str
    manufacturer: str
    part_number: str
    category: str

    # Relationships
    equivalents: List[str] = field(default_factory=list)
    supersedes: List[str] = field(default_factory=list)
    superseded_by: List[str] = field(default_factory=list)
    similar: List[str] = field(default_factory=list)

    # Metadata
    consciousness_level: int = 0
    verification_score: float = 0.0


class EquivalenceGraph:
    """
    Graph database for part equivalence relationships.

    Manages:
    - Direct equivalences between parts
    - Cross-manufacturer mappings
    - Supersession chains
    - Similarity relationships
    """

    def __init__(self):
        self.nodes: Dict[str, PartNode] = {}
        self.relations: Dict[Tuple[str, str], EquivalenceRelation] = {}

        # Manufacturer cross-reference tables
        self.manufacturer_xref: Dict[str, Dict[str, str]] = {}

        # Quick lookup indices
        self.by_manufacturer: Dict[str, Set[str]] = {}
        self.by_category: Dict[str, Set[str]] = {}

    def add_part(
        self,
        part_id: str,
        manufacturer: str,
        part_number: str,
        category: str
    ) -> PartNode:
        """Add a part node to the graph."""
        if part_id in self.nodes:
            return self.nodes[part_id]

        node = PartNode(
            part_id=part_id,
            manufacturer=manufacturer,
            part_number=part_number,
            category=category
        )
        self.nodes[part_id] = node

        # Update indices
        if manufacturer not in self.by_manufacturer:
            self.by_manufacturer[manufacturer] = set()
        self.by_manufacturer[manufacturer].add(part_id)

        if category not in self.by_category:
            self.by_category[category] = set()
        self.by_category[category].add(part_id)

        return node

    def add_equivalence(
        self,
        source_id: str,
        target_id: str,
        relation_type: EquivalenceType,
        confidence: float = 0.9,
        source_data: str = "calculated",
        differences: List[str] = None,
        bidirectional: bool = True
    ) -> EquivalenceRelation:
        """Add an equivalence relationship."""
        now = datetime.now()

        relation = EquivalenceRelation(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            confidence=confidence,
            bidirectional=bidirectional,
            source_data=source_data,
            verified=False,
            verification_count=0,
            created_at=now,
            updated_at=now,
            differences=differences or []
        )

        # Store relation
        self.relations[(source_id, target_id)] = relation

        # Update node connections
        if source_id in self.nodes:
            self._update_node_relations(self.nodes[source_id], target_id, relation_type)

        if bidirectional and target_id in self.nodes:
            reverse_type = self._get_reverse_type(relation_type)
            self._update_node_relations(self.nodes[target_id], source_id, reverse_type)

        return relation

    def get_equivalents(
        self,
        part_id: str,
        relation_types: List[EquivalenceType] = None,
        min_confidence: float = 0.7
    ) -> List[Tuple[str, EquivalenceRelation]]:
        """
        Get all equivalent parts.

        Args:
            part_id: Source part ID
            relation_types: Filter by relation types (None = all)
            min_confidence: Minimum confidence threshold

        Returns:
            List of (part_id, relation) tuples
        """
        results = []

        for (source, target), relation in self.relations.items():
            if source == part_id or (relation.bidirectional and target == part_id):
                if relation.confidence < min_confidence:
                    continue

                if relation_types and relation.relation_type not in relation_types:
                    continue

                other_id = target if source == part_id else source
                results.append((other_id, relation))

        # Sort by confidence
        results.sort(key=lambda x: x[1].confidence, reverse=True)

        return results

    def get_interchangeable(
        self,
        part_id: str,
        min_confidence: float = 0.8
    ) -> List[str]:
        """Get all directly interchangeable parts."""
        equivalents = self.get_equivalents(
            part_id,
            relation_types=[
                EquivalenceType.IDENTICAL,
                EquivalenceType.INTERCHANGEABLE
            ],
            min_confidence=min_confidence
        )
        return [pid for pid, _ in equivalents]

    def get_supersession_chain(
        self,
        part_id: str,
        direction: str = "forward"
    ) -> List[str]:
        """
        Get the supersession chain for a part.

        Args:
            part_id: Starting part ID
            direction: "forward" (what supersedes this) or "backward" (what this supersedes)

        Returns:
            Ordered list of part IDs in supersession chain
        """
        chain = []
        visited = set()
        current = part_id

        while current and current not in visited:
            visited.add(current)

            if current != part_id:
                chain.append(current)

            # Find next in chain
            next_part = None
            for (source, target), relation in self.relations.items():
                if direction == "forward":
                    if source == current and relation.relation_type == EquivalenceType.SUPERSEDED_BY:
                        next_part = target
                        break
                else:
                    if source == current and relation.relation_type == EquivalenceType.SUPERSEDES:
                        next_part = target
                        break

            current = next_part

        return chain

    def find_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> Optional[List[Tuple[str, EquivalenceType]]]:
        """
        Find the shortest equivalence path between two parts.

        Returns:
            List of (part_id, relation_type) representing the path,
            or None if no path exists
        """
        if source_id == target_id:
            return [(source_id, None)]

        # BFS search
        queue = [(source_id, [(source_id, None)])]
        visited = {source_id}

        while queue:
            current, path = queue.pop(0)

            if len(path) > max_depth:
                continue

            # Get neighbors
            for other_id, relation in self.get_equivalents(current):
                if other_id == target_id:
                    return path + [(other_id, relation.relation_type)]

                if other_id not in visited:
                    visited.add(other_id)
                    queue.append((other_id, path + [(other_id, relation.relation_type)]))

        return None

    def get_manufacturer_crossref(
        self,
        part_number: str,
        source_manufacturer: str,
        target_manufacturer: str
    ) -> Optional[str]:
        """Get cross-reference part number for different manufacturer."""
        key = (source_manufacturer, target_manufacturer)

        if key not in self.manufacturer_xref:
            return None

        return self.manufacturer_xref[key].get(part_number)

    def add_manufacturer_crossref(
        self,
        source_manufacturer: str,
        source_part_number: str,
        target_manufacturer: str,
        target_part_number: str
    ):
        """Add a manufacturer cross-reference."""
        key = (source_manufacturer, target_manufacturer)

        if key not in self.manufacturer_xref:
            self.manufacturer_xref[key] = {}

        self.manufacturer_xref[key][source_part_number] = target_part_number

        # Also add reverse
        reverse_key = (target_manufacturer, source_manufacturer)
        if reverse_key not in self.manufacturer_xref:
            self.manufacturer_xref[reverse_key] = {}
        self.manufacturer_xref[reverse_key][target_part_number] = source_part_number

    def verify_equivalence(
        self,
        source_id: str,
        target_id: str,
        is_valid: bool,
        verifier: str = "system"
    ):
        """Verify or invalidate an equivalence relationship."""
        key = (source_id, target_id)

        if key not in self.relations:
            # Try reverse
            key = (target_id, source_id)
            if key not in self.relations:
                return

        relation = self.relations[key]
        relation.verification_count += 1
        relation.updated_at = datetime.now()

        if is_valid:
            # Increase confidence
            relation.confidence = min(1.0, relation.confidence + 0.05)
            relation.verified = True
        else:
            # Decrease confidence
            relation.confidence = max(0.0, relation.confidence - 0.1)
            if relation.confidence < 0.3:
                # Remove low-confidence relation
                del self.relations[key]

    def get_cluster(
        self,
        part_id: str,
        max_depth: int = 2
    ) -> Dict[str, Dict]:
        """
        Get the equivalence cluster around a part.

        Returns:
            Dictionary of part_id -> {distance, relations}
        """
        cluster = {part_id: {"distance": 0, "relations": []}}
        queue = [(part_id, 0)]
        visited = {part_id}

        while queue:
            current, depth = queue.pop(0)

            if depth >= max_depth:
                continue

            for other_id, relation in self.get_equivalents(current):
                if other_id not in visited:
                    visited.add(other_id)
                    cluster[other_id] = {
                        "distance": depth + 1,
                        "relations": [relation.relation_type.value]
                    }
                    queue.append((other_id, depth + 1))
                elif other_id in cluster:
                    # Add additional relation
                    cluster[other_id]["relations"].append(relation.relation_type.value)

        return cluster

    def export_graph(self) -> Dict:
        """Export graph to JSON-serializable format."""
        return {
            "nodes": {
                pid: {
                    "manufacturer": node.manufacturer,
                    "part_number": node.part_number,
                    "category": node.category,
                    "equivalents": node.equivalents,
                }
                for pid, node in self.nodes.items()
            },
            "relations": [
                {
                    "source": rel.source_id,
                    "target": rel.target_id,
                    "type": rel.relation_type.value,
                    "confidence": rel.confidence,
                    "bidirectional": rel.bidirectional,
                    "verified": rel.verified,
                }
                for rel in self.relations.values()
            ],
            "manufacturer_xref": {
                f"{k[0]}|{k[1]}": v
                for k, v in self.manufacturer_xref.items()
            }
        }

    def import_graph(self, data: Dict):
        """Import graph from JSON data."""
        # Import nodes
        for pid, node_data in data.get("nodes", {}).items():
            self.add_part(
                part_id=pid,
                manufacturer=node_data["manufacturer"],
                part_number=node_data["part_number"],
                category=node_data["category"]
            )

        # Import relations
        for rel_data in data.get("relations", []):
            self.add_equivalence(
                source_id=rel_data["source"],
                target_id=rel_data["target"],
                relation_type=EquivalenceType(rel_data["type"]),
                confidence=rel_data["confidence"],
                bidirectional=rel_data["bidirectional"]
            )

    def _update_node_relations(
        self,
        node: PartNode,
        other_id: str,
        relation_type: EquivalenceType
    ):
        """Update a node's relation lists."""
        if relation_type in [EquivalenceType.IDENTICAL, EquivalenceType.INTERCHANGEABLE]:
            if other_id not in node.equivalents:
                node.equivalents.append(other_id)
        elif relation_type == EquivalenceType.SUPERSEDES:
            if other_id not in node.supersedes:
                node.supersedes.append(other_id)
        elif relation_type == EquivalenceType.SUPERSEDED_BY:
            if other_id not in node.superseded_by:
                node.superseded_by.append(other_id)
        elif relation_type == EquivalenceType.SIMILAR:
            if other_id not in node.similar:
                node.similar.append(other_id)

    def _get_reverse_type(self, relation_type: EquivalenceType) -> EquivalenceType:
        """Get the reverse relation type."""
        reverse_map = {
            EquivalenceType.SUPERSEDES: EquivalenceType.SUPERSEDED_BY,
            EquivalenceType.SUPERSEDED_BY: EquivalenceType.SUPERSEDES,
        }
        return reverse_map.get(relation_type, relation_type)
