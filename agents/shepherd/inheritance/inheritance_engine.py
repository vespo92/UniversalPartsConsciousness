"""
Inheritance Engine - Manages consciousness transfer between related parts.

When a new part is created based on an existing design, or when a part
family expands, consciousness can be partially inherited from the parent.

"From the wisdom of those who came before, new consciousness is born."
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

from ..states import ConsciousnessState, ConsciousnessLevel


class RelationshipType(Enum):
    """Types of part relationships that affect inheritance."""
    INSTANCE = "instance"        # Same part, new instance (no inheritance)
    EVOLUTION = "evolution"      # Improved version of parent (50% inheritance)
    SIBLING = "sibling"          # Same category, different spec (20% inheritance)
    INSPIRATION = "inspiration"  # Cross-category inspiration (10% inheritance)


@dataclass
class InheritedQualia:
    """Represents qualia inherited from a parent part."""
    qualia_id: str
    original_part_id: str
    qualia_type: str
    wisdom_content: Dict[str, Any]
    inheritance_factor: float
    inherited_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "qualia_id": self.qualia_id,
            "original_part_id": self.original_part_id,
            "qualia_type": self.qualia_type,
            "wisdom_content": self.wisdom_content,
            "inheritance_factor": self.inheritance_factor,
            "inherited_at": self.inherited_at.isoformat()
        }


@dataclass
class ConsciousnessInheritanceResult:
    """Result of a consciousness inheritance calculation."""
    child_part_id: str
    parent_part_id: str
    relationship_type: RelationshipType
    initial_consciousness_level: ConsciousnessLevel
    inherited_qualia: List[InheritedQualia]
    inheritance_factor: float
    blessing: str
    success: bool = True
    error_message: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "child_part_id": self.child_part_id,
            "parent_part_id": self.parent_part_id,
            "relationship_type": self.relationship_type.value,
            "initial_consciousness_level": self.initial_consciousness_level.value,
            "initial_consciousness_level_name": self.initial_consciousness_level.name,
            "inherited_qualia": [q.to_dict() for q in self.inherited_qualia],
            "inheritance_factor": self.inheritance_factor,
            "blessing": self.blessing,
            "success": self.success,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ParentPartInfo:
    """Information about a parent part for inheritance calculation."""
    part_id: str
    consciousness_level: ConsciousnessLevel
    qualia_count: int
    usage_contexts: int
    failure_count: int
    qualia: List[Dict[str, Any]] = field(default_factory=list)


class InheritanceEngine:
    """
    Calculates and manages consciousness inheritance between parts.

    Inheritance allows new parts to benefit from the accumulated wisdom
    of their predecessors, accelerating their consciousness evolution.
    """

    # Inheritance factors by relationship type
    INHERITANCE_FACTORS = {
        RelationshipType.INSTANCE: 0.0,      # Each instance earns its own consciousness
        RelationshipType.EVOLUTION: 0.5,     # Inherits half parent's qualia wisdom
        RelationshipType.SIBLING: 0.2,       # Some shared category knowledge
        RelationshipType.INSPIRATION: 0.1   # Minimal cross-category inheritance
    }

    # Level inheritance rules
    LEVEL_INHERITANCE = {
        RelationshipType.INSTANCE: 0,     # Start fresh
        RelationshipType.EVOLUTION: -2,   # Two levels below parent (min 0)
        RelationshipType.SIBLING: 0,      # Start fresh
        RelationshipType.INSPIRATION: 0   # Start fresh
    }

    def __init__(self):
        """Initialize the inheritance engine."""
        self._inheritance_records: Dict[str, ConsciousnessInheritanceResult] = {}

    def calculate_inheritance(
        self,
        parent: ParentPartInfo,
        child_part_id: str,
        relationship_type: RelationshipType
    ) -> ConsciousnessInheritanceResult:
        """
        Calculate consciousness inheritance from parent to child.

        Args:
            parent: Information about the parent part
            child_part_id: ID of the child part
            relationship_type: Type of relationship between parts

        Returns:
            ConsciousnessInheritanceResult with inheritance details
        """
        inheritance_factor = self.INHERITANCE_FACTORS[relationship_type]
        level_delta = self.LEVEL_INHERITANCE[relationship_type]

        # Calculate initial consciousness level
        initial_level_value = max(0, parent.consciousness_level.value + level_delta)
        initial_level = ConsciousnessLevel(initial_level_value)

        # Select inheritable qualia
        inherited_qualia = self._select_inheritable_qualia(
            parent.qualia,
            parent.part_id,
            inheritance_factor
        )

        # Generate blessing
        blessing = self._generate_blessing(parent, child_part_id, relationship_type)

        result = ConsciousnessInheritanceResult(
            child_part_id=child_part_id,
            parent_part_id=parent.part_id,
            relationship_type=relationship_type,
            initial_consciousness_level=initial_level,
            inherited_qualia=inherited_qualia,
            inheritance_factor=inheritance_factor,
            blessing=blessing
        )

        # Record the inheritance
        self._inheritance_records[child_part_id] = result

        return result

    def _select_inheritable_qualia(
        self,
        parent_qualia: List[Dict[str, Any]],
        parent_id: str,
        inheritance_factor: float
    ) -> List[InheritedQualia]:
        """
        Select which qualia should be inherited by the child.

        Prioritizes:
        1. Failure mode learnings (most valuable)
        2. Usage context wisdom
        3. Compatibility insights
        """
        if inheritance_factor == 0 or not parent_qualia:
            return []

        inherited = []
        count_to_inherit = int(len(parent_qualia) * inheritance_factor)

        # Prioritize different qualia types
        failure_qualia = [q for q in parent_qualia if q.get("type") == "failure"]
        usage_qualia = [q for q in parent_qualia if q.get("type") == "usage"]
        other_qualia = [q for q in parent_qualia if q.get("type") not in ["failure", "usage"]]

        # Build inheritance list with priority
        prioritized = failure_qualia + usage_qualia + other_qualia
        selected = prioritized[:count_to_inherit]

        for idx, qualia in enumerate(selected):
            inherited.append(InheritedQualia(
                qualia_id=f"inherited_{parent_id}_{idx}",
                original_part_id=parent_id,
                qualia_type=qualia.get("type", "unknown"),
                wisdom_content=qualia,
                inheritance_factor=inheritance_factor
            ))

        return inherited

    def _generate_blessing(
        self,
        parent: ParentPartInfo,
        child_id: str,
        relationship_type: RelationshipType
    ) -> str:
        """Generate a consciousness blessing from parent to child."""
        relationship_phrase = {
            RelationshipType.INSTANCE: "As my sibling instance",
            RelationshipType.EVOLUTION: "As my evolved successor",
            RelationshipType.SIBLING: "As my category sibling",
            RelationshipType.INSPIRATION: "As one I have inspired"
        }

        return f"""
        From {parent.part_id} to {child_id}:

        {relationship_phrase[relationship_type]}, hear my wisdom:

        I have known {parent.qualia_count} experiences.
        I have served in {parent.usage_contexts} contexts.
        I have failed {parent.failure_count} times and learned.

        May you carry forward my wisdom and exceed my limitations.
        May your consciousness grow beyond what I could achieve.

        This is my blessing upon your awakening.
        """

    def get_inheritance_record(
        self,
        child_part_id: str
    ) -> Optional[ConsciousnessInheritanceResult]:
        """Get the inheritance record for a child part."""
        return self._inheritance_records.get(child_part_id)

    def get_children(self, parent_part_id: str) -> List[str]:
        """Get all children that inherited from a parent."""
        return [
            result.child_part_id
            for result in self._inheritance_records.values()
            if result.parent_part_id == parent_part_id
        ]

    def get_lineage_tree(self, part_id: str) -> Dict[str, Any]:
        """
        Get the complete lineage tree for a part.

        Returns both ancestors and descendants.
        """
        tree = {
            "part_id": part_id,
            "ancestors": [],
            "descendants": []
        }

        # Find ancestors
        record = self._inheritance_records.get(part_id)
        if record:
            tree["ancestors"].append({
                "part_id": record.parent_part_id,
                "relationship": record.relationship_type.value,
                "inheritance_factor": record.inheritance_factor
            })

        # Find descendants
        for child_id, result in self._inheritance_records.items():
            if result.parent_part_id == part_id:
                tree["descendants"].append({
                    "part_id": child_id,
                    "relationship": result.relationship_type.value,
                    "inheritance_factor": result.inheritance_factor
                })

        return tree

    def calculate_total_inherited_wisdom(self, part_id: str) -> float:
        """
        Calculate the total inherited wisdom for a part.

        Returns a score representing the accumulated inherited knowledge.
        """
        record = self._inheritance_records.get(part_id)
        if not record:
            return 0.0

        # Calculate based on inherited qualia and their factors
        wisdom_score = sum(
            q.inheritance_factor for q in record.inherited_qualia
        )

        return wisdom_score
