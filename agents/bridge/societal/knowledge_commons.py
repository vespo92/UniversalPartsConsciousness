"""
Knowledge Commons - The Shared Repository of Mechanical Wisdom
================================================================

The Knowledge Commons is the heart of Universal Parts Consciousness
as societal infrastructure. It represents the collective mechanical
wisdom of humanity, freely accessible to all.

This is not a database. This is a living repository of:
- How things work
- Why things fail
- What works together
- The heritage of mechanical innovation
- The wisdom of engineers, mechanics, and makers

Governed by principles of openness, accuracy, and accessibility.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class KnowledgeType(Enum):
    """Types of knowledge in the commons."""
    SPECIFICATION = auto()      # Technical specifications
    PROCEDURE = auto()          # How-to instructions
    PRINCIPLE = auto()          # Engineering principles
    HISTORY = auto()            # Historical context
    EXPERIENCE = auto()         # Real-world experiences
    FAILURE = auto()            # Failure case studies
    INNOVATION = auto()         # Innovation patterns
    WISDOM = auto()             # Collective insights


class ContributionSource(Enum):
    """Sources of knowledge contribution."""
    STANDARDS_BODY = auto()     # ISO, DIN, ANSI, etc.
    MANUFACTURER = auto()       # OEM documentation
    COMMUNITY = auto()          # Community contributions
    PROFESSIONAL = auto()       # Professional engineers
    SENSOR = auto()             # IoT sensor data
    ACADEMIC = auto()           # Research and studies
    HERITAGE = auto()           # Historical preservation


class VerificationLevel(Enum):
    """Level of verification for knowledge."""
    UNVERIFIED = 0
    COMMUNITY_REVIEWED = 1
    EXPERT_VERIFIED = 2
    STANDARD_BODY = 3
    CONSENSUS = 4


@dataclass
class KnowledgeEntry:
    """An entry in the knowledge commons."""
    entry_id: str
    knowledge_type: KnowledgeType
    title: str
    content: str
    source: ContributionSource
    verification_level: VerificationLevel
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    contributors: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    part_ids: List[str] = field(default_factory=list)
    access_count: int = 0
    contribution_score: float = 0.0


@dataclass
class ContributionGuidelines:
    """Guidelines for contributing to the knowledge commons."""
    allowed_types: List[KnowledgeType]
    verification_requirements: Dict[VerificationLevel, List[str]]
    quality_standards: List[str]
    citation_requirements: List[str]
    prohibited_content: List[str]


class KnowledgeCommons:
    """
    The Knowledge Commons - Humanity's Mechanical Wisdom Repository.

    The commons operates on these core principles:

    1. OPENNESS
       - Knowledge is freely accessible
       - Contribution is open to all
       - No artificial barriers to learning

    2. ACCURACY
       - Multi-tier verification
       - Expert review for critical knowledge
       - Community curation for quality

    3. ACCESSIBILITY
       - Available in multiple languages
       - Adaptable to skill levels
       - Searchable by any criteria

    4. PRESERVATION
       - Historical knowledge preserved
       - Heritage maintained
       - Evolution tracked

    5. EVOLUTION
       - Knowledge improves over time
       - New experiences integrate
       - Collective wisdom emerges

    This is infrastructure for society - enabling anyone to learn,
    build, repair, and innovate with mechanical systems.
    """

    def __init__(self):
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.categories: Dict[str, List[str]] = {}
        self.contribution_guidelines = self._create_guidelines()
        self.commons_statistics: Dict[str, Any] = {}

        logger.info("Knowledge Commons initialized")

    def _create_guidelines(self) -> ContributionGuidelines:
        """Create contribution guidelines for the commons."""
        return ContributionGuidelines(
            allowed_types=list(KnowledgeType),
            verification_requirements={
                VerificationLevel.COMMUNITY_REVIEWED: [
                    "Minimum 3 community reviews",
                    "No unresolved disputes"
                ],
                VerificationLevel.EXPERT_VERIFIED: [
                    "Review by verified expert",
                    "Technical accuracy confirmation"
                ],
                VerificationLevel.STANDARD_BODY: [
                    "Reference to published standard",
                    "Standard body confirmation"
                ],
                VerificationLevel.CONSENSUS: [
                    "Multiple expert agreement",
                    "Extended community review",
                    "No contradicting evidence"
                ]
            },
            quality_standards=[
                "Clear and accurate technical content",
                "Proper citations and references",
                "Objective, non-commercial language",
                "Accessible to target skill level",
                "Inclusive of safety considerations"
            ],
            citation_requirements=[
                "Reference original sources",
                "Include measurement methodology",
                "Note applicable conditions",
                "Acknowledge contributors"
            ],
            prohibited_content=[
                "Proprietary or copyrighted material without license",
                "Commercial promotion",
                "Unverified safety-critical claims",
                "Personal attacks or bias",
                "Deliberately misleading information"
            ]
        )

    async def add_entry(self, entry: KnowledgeEntry) -> str:
        """Add a new entry to the knowledge commons."""
        self.entries[entry.entry_id] = entry
        logger.info(f"Added knowledge entry: {entry.title}")
        return entry.entry_id

    async def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Retrieve an entry from the commons."""
        entry = self.entries.get(entry_id)
        if entry:
            entry.access_count += 1
        return entry

    async def search_knowledge(
        self,
        query: str,
        knowledge_type: Optional[KnowledgeType] = None,
        min_verification: VerificationLevel = VerificationLevel.UNVERIFIED
    ) -> List[KnowledgeEntry]:
        """Search the knowledge commons."""
        results = []

        for entry in self.entries.values():
            if knowledge_type and entry.knowledge_type != knowledge_type:
                continue
            if entry.verification_level.value < min_verification.value:
                continue
            # In production, this would do actual text search
            results.append(entry)

        return results

    async def get_knowledge_for_part(self, part_id: str) -> List[KnowledgeEntry]:
        """Get all knowledge entries related to a part."""
        return [e for e in self.entries.values() if part_id in e.part_ids]

    async def get_knowledge_by_type(self, knowledge_type: KnowledgeType) -> List[KnowledgeEntry]:
        """Get all entries of a specific knowledge type."""
        return [e for e in self.entries.values() if e.knowledge_type == knowledge_type]

    def get_commons_charter(self) -> Dict[str, Any]:
        """
        Return the Knowledge Commons Charter.

        This defines the principles and governance of the commons.
        """
        return {
            "name": "Universal Parts Consciousness Knowledge Commons",
            "subtitle": "Humanity's Repository of Mechanical Wisdom",
            "note": "This is NOT a barcode system - it is collective consciousness",
            "charter": {
                "article_1_openness": {
                    "title": "Commitment to Openness",
                    "text": (
                        "The Knowledge Commons exists to serve all of humanity. "
                        "Fundamental mechanical knowledge shall remain freely accessible. "
                        "Safety-critical information shall never be restricted."
                    )
                },
                "article_2_accuracy": {
                    "title": "Dedication to Accuracy",
                    "text": (
                        "Knowledge in the commons must be accurate and verifiable. "
                        "Multiple verification levels ensure quality. "
                        "Errors must be correctable by the community."
                    )
                },
                "article_3_community": {
                    "title": "Community Governance",
                    "text": (
                        "The commons is governed by its community of contributors. "
                        "Decisions are made transparently and democratically. "
                        "Expert guidance informs but does not dictate."
                    )
                },
                "article_4_preservation": {
                    "title": "Preservation of Heritage",
                    "text": (
                        "Historical knowledge is preserved for future generations. "
                        "The evolution of mechanical wisdom is documented. "
                        "No knowledge is discarded without community consent."
                    )
                },
                "article_5_attribution": {
                    "title": "Recognition of Contribution",
                    "text": (
                        "Contributors are acknowledged for their additions. "
                        "Collective wisdom credits its sources. "
                        "Building on others' work is encouraged with attribution."
                    )
                },
            },
            "knowledge_types": [t.name for t in KnowledgeType],
            "contribution_sources": [s.name for s in ContributionSource],
            "verification_levels": [v.name for v in VerificationLevel],
            "vision": (
                "A future where every mechanic, engineer, maker, and curious mind "
                "has access to the collective wisdom of humanity's mechanical heritage - "
                "where learning how things work is a universal right, and where every "
                "contribution improves the whole."
            )
        }

    def get_commons_statistics(self) -> Dict[str, Any]:
        """Get current statistics of the knowledge commons."""
        return {
            "total_entries": len(self.entries),
            "by_type": {
                t.name: sum(1 for e in self.entries.values() if e.knowledge_type == t)
                for t in KnowledgeType
            },
            "by_verification": {
                v.name: sum(1 for e in self.entries.values() if e.verification_level == v)
                for v in VerificationLevel
            },
            "total_access_count": sum(e.access_count for e in self.entries.values()),
            "unique_contributors": len(set(
                c for e in self.entries.values() for c in e.contributors
            ))
        }

    def get_learning_pathways(self) -> Dict[str, Any]:
        """
        Return structured learning pathways through the knowledge commons.

        These pathways enable anyone to learn mechanical knowledge
        from beginner to expert.
        """
        return {
            "pathways": {
                "maker_basics": {
                    "title": "Maker Basics",
                    "level": "beginner",
                    "description": "Foundational knowledge for making and building",
                    "topics": [
                        "Understanding fasteners",
                        "Basic material properties",
                        "Hand tool fundamentals",
                        "Safety essentials",
                        "Your first build"
                    ]
                },
                "mechanical_fundamentals": {
                    "title": "Mechanical Fundamentals",
                    "level": "intermediate",
                    "description": "Core mechanical engineering concepts",
                    "topics": [
                        "Thread mechanics and standards",
                        "Material science basics",
                        "Tolerance and fits",
                        "Stress and strain",
                        "Failure modes"
                    ]
                },
                "automotive_systems": {
                    "title": "Automotive Systems",
                    "level": "intermediate",
                    "description": "Understanding automotive mechanical systems",
                    "topics": [
                        "Engine fundamentals",
                        "Drivetrain systems",
                        "Suspension and steering",
                        "Brake systems",
                        "Common repairs"
                    ]
                },
                "advanced_engineering": {
                    "title": "Advanced Engineering",
                    "level": "advanced",
                    "description": "Professional-level mechanical engineering",
                    "topics": [
                        "Finite element concepts",
                        "Fatigue analysis",
                        "Thermal management",
                        "Design optimization",
                        "Failure investigation"
                    ]
                },
                "heritage_and_history": {
                    "title": "Mechanical Heritage",
                    "level": "all",
                    "description": "The history and culture of mechanical innovation",
                    "topics": [
                        "Evolution of the machine",
                        "Legendary engines",
                        "Manufacturing revolutions",
                        "Pioneers of engineering",
                        "Future of mechanics"
                    ]
                }
            },
            "philosophy": (
                "Learning is a journey through collective wisdom. "
                "Each pathway connects learners to humanity's mechanical heritage "
                "while preparing them for future innovation."
            )
        }
