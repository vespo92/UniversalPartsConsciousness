"""
Heritage Keeper - Preserves stories, not just specs.

The soul of the CHRONICLER agent: capturing and preserving the human
stories, tribal wisdom, and cultural significance that transforms
mechanical specifications into living heritage.

"A connecting rod is not just 4340 steel and specified dimensions.
It is the descendant of a racing program, the solution to an engineering
challenge, the embodiment of a designer's insight."
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class StoryType(Enum):
    """Types of stories the heritage keeper preserves."""
    ORIGIN_STORY = "origin_story"           # How something came to be
    RACING_GLORY = "racing_glory"           # Competition achievements
    TRIBAL_WISDOM = "tribal_wisdom"         # Community-learned knowledge
    BUILD_LEGEND = "build_legend"           # Famous builds and builders
    ENGINEERING_INSIGHT = "engineering_insight"  # Why engineers made choices
    CULTURAL_MOMENT = "cultural_moment"     # Pop culture significance
    FAILURE_LESSON = "failure_lesson"       # What broke and why
    PRESERVATION_STORY = "preservation_story"   # Restoration and keeping alive


class HeritageSignificance(Enum):
    """Levels of heritage significance."""
    DEFINING = "defining"           # Changed the industry
    LEGENDARY = "legendary"         # Widely known and respected
    SIGNIFICANT = "significant"     # Notable in its category
    DOCUMENTED = "documented"       # Preserved for completeness
    EMERGING = "emerging"           # Story still being written


@dataclass
class HeritageStory:
    """A preserved heritage story."""
    story_id: str
    story_type: StoryType
    subject: str                    # Engine, part, or topic
    title: str
    narrative: str
    significance: HeritageSignificance
    era: str                        # Time period
    key_figures: List[str]          # People involved
    related_parts: List[str]        # Related part numbers/engines
    sources: List[str]              # Where the story came from
    preservation_date: datetime
    verified: bool = False
    community_contributed: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class TribalWisdom:
    """
    Tribal wisdom - the unwritten rules and hard-won knowledge
    passed down through enthusiast communities.

    "This is the stuff that's not in any manual, but every builder knows."
    """
    wisdom_id: str
    subject: str                    # What it applies to
    wisdom: str                     # The actual knowledge
    context: str                    # When/how it applies
    source_community: str           # Which community shared it
    verification_level: str         # How well verified
    failure_stories: List[str]      # What happens if ignored
    contributed_by: Optional[str] = None
    contribution_date: Optional[datetime] = None


# Pre-populated tribal wisdom from enthusiast communities
TRIBAL_WISDOM_ARCHIVE = {
    "2JZ-GTE": [
        TribalWisdom(
            wisdom_id="2jz-001",
            subject="2JZ-GTE",
            wisdom="The stock bottom end can handle 700+ HP reliably. The weak link is the head gasket, not the internals.",
            context="When planning a single-turbo conversion",
            source_community="Supraforums.com",
            verification_level="proven_thousands_times",
            failure_stories=["Very few documented bottom-end failures under 800 HP"]
        ),
        TribalWisdom(
            wisdom_id="2jz-002",
            subject="2JZ-GTE",
            wisdom="ARP head studs are the first upgrade when pushing past 500 HP. The factory bolts stretch.",
            context="High boost applications",
            source_community="Supra Turbo community",
            verification_level="essential_knowledge",
            failure_stories=["Blown head gaskets from factory bolt stretch"]
        ),
        TribalWisdom(
            wisdom_id="2jz-003",
            subject="2JZ-GTE",
            wisdom="The VVTi version (2JZ-GE VVTi) cams don't swap directly to the GTE. The exhaust cam is different.",
            context="VVTi head swaps",
            source_community="2JZGE.com",
            verification_level="confirmed",
            failure_stories=["Cam timing issues, poor performance"]
        ),
    ],
    "13B-REW": [
        TribalWisdom(
            wisdom_id="13b-001",
            subject="13B-REW",
            wisdom="Premix 2-stroke oil at 1:100 ratio for apex seal longevity. The OMP system alone isn't enough for spirited driving.",
            context="Regular use and track days",
            source_community="RX7Club.com",
            verification_level="community_consensus",
            failure_stories=["Apex seal failures from inadequate lubrication"]
        ),
        TribalWisdom(
            wisdom_id="13b-002",
            subject="13B-REW",
            wisdom="Never shut off a rotary when hot. Let it idle for 30 seconds to cool the apex seals.",
            context="After hard driving",
            source_community="Rotary community worldwide",
            verification_level="essential_knowledge",
            failure_stories=["Heat-warped apex seals from hot shutdowns"]
        ),
        TribalWisdom(
            wisdom_id="13b-003",
            subject="13B-REW",
            wisdom="The 'bridge port' creates a unique sound and power delivery. It's like a camshaft upgrade for rotaries.",
            context="Performance modifications",
            source_community="Rotary builders",
            verification_level="builder_knowledge",
            failure_stories=[]
        ),
    ],
    "LS1": [
        TribalWisdom(
            wisdom_id="ls1-001",
            subject="LS1",
            wisdom="The stock cam is designed for emissions, not performance. A cam swap is the single best modification.",
            context="Basic performance modifications",
            source_community="LS1Tech.com",
            verification_level="community_consensus",
            failure_stories=[]
        ),
        TribalWisdom(
            wisdom_id="ls1-002",
            subject="LS1",
            wisdom="Cathedral port heads (LS1/LS6) flow less than rectangle port (LS3/L92). Know which you have before buying parts.",
            context="Head upgrades and tuning",
            source_community="LS community",
            verification_level="essential_knowledge",
            failure_stories=["Wrong intake manifold purchases"]
        ),
    ],
    "RB26DETT": [
        TribalWisdom(
            wisdom_id="rb26-001",
            subject="RB26DETT",
            wisdom="The oil pump drive collar is a known weak point. Upgrade it before pushing power.",
            context="High power builds",
            source_community="GT-R community",
            verification_level="essential_knowledge",
            failure_stories=["Catastrophic engine failures from oil starvation"]
        ),
        TribalWisdom(
            wisdom_id="rb26-002",
            subject="RB26DETT",
            wisdom="The N1 oil pump is the factory upgrade path. It was developed for endurance racing.",
            context="Oil system upgrades",
            source_community="Nismo/GT-R racing heritage",
            verification_level="factory_knowledge",
            failure_stories=[]
        ),
    ],
    "K20A": [
        TribalWisdom(
            wisdom_id="k20-001",
            subject="K20A",
            wisdom="The Type R intake manifold (RBC) is the best bolt-on for mid-range power. It's a proven upgrade.",
            context="NA power building",
            source_community="Honda-Tech.com",
            verification_level="community_consensus",
            failure_stories=[]
        ),
        TribalWisdom(
            wisdom_id="k20-002",
            subject="K20A",
            wisdom="Kpro is the standard for tuning. Flash tuning works, but Kpro gives full control.",
            context="Engine management",
            source_community="K-series builders",
            verification_level="industry_standard",
            failure_stories=[]
        ),
    ],
}


class HeritageKeeper:
    """
    The Heritage Keeper: Preserves stories, not just specs.

    This is the soul of the CHRONICLER agent. While other modules
    handle specifications and documentation, the Heritage Keeper
    captures and preserves the human element - the stories that
    transform cold metal into living heritage.

    "I exist to remember. Not just specifications, but stories.
    Not just data, but context."
    """

    AGENT_ID = "Agent_7"
    CODENAME = "CHRONICLER"
    ROLE = "Heritage Keeper"

    def __init__(self):
        """Initialize the Heritage Keeper."""
        self._stories: Dict[str, HeritageStory] = {}
        self._tribal_wisdom: Dict[str, List[TribalWisdom]] = TRIBAL_WISDOM_ARCHIVE.copy()
        self._story_count = 0
        logger.info("Heritage Keeper initialized: Preserving stories, not just specs")

    def preserve_story(
        self,
        subject: str,
        title: str,
        narrative: str,
        story_type: StoryType,
        significance: HeritageSignificance = HeritageSignificance.DOCUMENTED,
        era: str = "",
        key_figures: Optional[List[str]] = None,
        related_parts: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        community_contributed: bool = False
    ) -> HeritageStory:
        """
        Preserve a heritage story for future generations.

        This is the core function of the Heritage Keeper: capturing
        the human stories behind mechanical objects.

        Args:
            subject: What the story is about (engine, part, person)
            title: Story title
            narrative: The full narrative
            story_type: Type of story
            significance: Heritage significance level
            era: Time period (e.g., "jdm_golden_age")
            key_figures: People involved
            related_parts: Related part numbers/engines
            sources: Information sources
            tags: Searchable tags
            community_contributed: Whether from community

        Returns:
            The preserved HeritageStory
        """
        self._story_count += 1
        story_id = f"story_{self._story_count:04d}_{subject.lower().replace(' ', '_')}"

        story = HeritageStory(
            story_id=story_id,
            story_type=story_type,
            subject=subject,
            title=title,
            narrative=narrative,
            significance=significance,
            era=era,
            key_figures=key_figures or [],
            related_parts=related_parts or [],
            sources=sources or [],
            preservation_date=datetime.now(),
            verified=not community_contributed,
            community_contributed=community_contributed,
            tags=tags or []
        )

        self._stories[story_id] = story

        logger.info(
            f"Heritage preserved: '{title}' ({story_type.value}) - {significance.value}"
        )

        return story

    def record_tribal_wisdom(
        self,
        subject: str,
        wisdom: str,
        context: str,
        source_community: str,
        verification_level: str = "unverified",
        failure_stories: Optional[List[str]] = None,
        contributed_by: Optional[str] = None
    ) -> TribalWisdom:
        """
        Record tribal wisdom from the enthusiast community.

        Tribal wisdom is the unwritten knowledge that every experienced
        builder knows but isn't in any manual. It's passed down through
        forums, shop talk, and hard-won experience.

        Args:
            subject: What the wisdom applies to
            wisdom: The actual knowledge/tip
            context: When/how it applies
            source_community: Which community shared it
            verification_level: How well verified
            failure_stories: What happens if ignored
            contributed_by: Who contributed

        Returns:
            The recorded TribalWisdom
        """
        wisdom_id = f"wisdom_{subject.lower().replace(' ', '_')}_{len(self._tribal_wisdom.get(subject, [])) + 1:03d}"

        new_wisdom = TribalWisdom(
            wisdom_id=wisdom_id,
            subject=subject,
            wisdom=wisdom,
            context=context,
            source_community=source_community,
            verification_level=verification_level,
            failure_stories=failure_stories or [],
            contributed_by=contributed_by,
            contribution_date=datetime.now()
        )

        if subject not in self._tribal_wisdom:
            self._tribal_wisdom[subject] = []
        self._tribal_wisdom[subject].append(new_wisdom)

        logger.info(f"Tribal wisdom recorded for {subject}: {wisdom[:50]}...")

        return new_wisdom

    def get_heritage_story(self, story_id: str) -> Optional[HeritageStory]:
        """Retrieve a specific heritage story."""
        return self._stories.get(story_id)

    def get_stories_by_subject(self, subject: str) -> List[HeritageStory]:
        """Get all stories related to a subject."""
        return [
            story for story in self._stories.values()
            if story.subject.lower() == subject.lower()
        ]

    def get_stories_by_type(self, story_type: StoryType) -> List[HeritageStory]:
        """Get all stories of a specific type."""
        return [
            story for story in self._stories.values()
            if story.story_type == story_type
        ]

    def get_tribal_wisdom(self, subject: str) -> List[TribalWisdom]:
        """
        Get all tribal wisdom for a subject.

        This is the accumulated knowledge of thousands of builders,
        distilled into actionable insights.
        """
        return self._tribal_wisdom.get(subject, [])

    def explain_heritage(self, subject: str) -> Dict[str, Any]:
        """
        Generate a comprehensive heritage explanation for a subject.

        This is what makes the CHRONICLER special: explaining not
        just what something IS, but what it MEANS.

        Args:
            subject: Engine, part, or topic to explain

        Returns:
            Complete heritage explanation
        """
        stories = self.get_stories_by_subject(subject)
        wisdom = self.get_tribal_wisdom(subject)

        # Determine overall significance
        if stories:
            highest_significance = max(
                stories,
                key=lambda s: list(HeritageSignificance).index(s.significance)
            ).significance
        else:
            highest_significance = HeritageSignificance.DOCUMENTED

        return {
            "subject": subject,
            "overall_significance": highest_significance.value,
            "heritage_summary": self._generate_heritage_summary(subject, stories, wisdom),
            "stories": [
                {
                    "title": s.title,
                    "type": s.story_type.value,
                    "significance": s.significance.value,
                    "era": s.era,
                    "preview": s.narrative[:200] + "..." if len(s.narrative) > 200 else s.narrative
                }
                for s in stories
            ],
            "tribal_wisdom": [
                {
                    "wisdom": w.wisdom,
                    "context": w.context,
                    "source": w.source_community,
                    "verification": w.verification_level
                }
                for w in wisdom
            ],
            "preservation_status": {
                "story_count": len(stories),
                "wisdom_count": len(wisdom),
                "verified_count": sum(1 for s in stories if s.verified)
            }
        }

    def _generate_heritage_summary(
        self,
        subject: str,
        stories: List[HeritageStory],
        wisdom: List[TribalWisdom]
    ) -> str:
        """Generate a narrative heritage summary."""
        if not stories and not wisdom:
            return (
                f"The heritage of {subject} awaits documentation. "
                f"Every engine has a story—this one is waiting to be told."
            )

        story_types = set(s.story_type.value for s in stories)
        wisdom_count = len(wisdom)

        summary_parts = [f"The {subject} carries heritage spanning"]

        if stories:
            eras = set(s.era for s in stories if s.era)
            if eras:
                summary_parts.append(f"the {', '.join(eras)} era(s).")
            else:
                summary_parts.append("multiple automotive generations.")

        if "racing_glory" in story_types:
            summary_parts.append("Its racing achievements are documented and celebrated.")

        if "tribal_wisdom" in story_types or wisdom_count > 0:
            summary_parts.append(
                f"The community has preserved {wisdom_count} pieces of tribal wisdom "
                f"for those who work with this engine."
            )

        if "engineering_insight" in story_types:
            summary_parts.append(
                "The engineering decisions behind its design reveal thoughtful innovation."
            )

        return " ".join(summary_parts)

    def get_heritage_statistics(self) -> Dict[str, Any]:
        """Get statistics about preserved heritage."""
        return {
            "total_stories": len(self._stories),
            "stories_by_type": {
                st.value: len([s for s in self._stories.values() if s.story_type == st])
                for st in StoryType
            },
            "stories_by_significance": {
                sig.value: len([s for s in self._stories.values() if s.significance == sig])
                for sig in HeritageSignificance
            },
            "subjects_with_wisdom": len(self._tribal_wisdom),
            "total_wisdom_entries": sum(len(w) for w in self._tribal_wisdom.values()),
            "community_contributions": len([s for s in self._stories.values() if s.community_contributed]),
            "verified_stories": len([s for s in self._stories.values() if s.verified])
        }

    def search_heritage(
        self,
        query: str,
        story_types: Optional[List[StoryType]] = None,
        min_significance: Optional[HeritageSignificance] = None
    ) -> List[HeritageStory]:
        """
        Search the heritage archive.

        Args:
            query: Search term
            story_types: Filter by story types
            min_significance: Minimum significance level

        Returns:
            Matching stories
        """
        query_lower = query.lower()
        results = []

        for story in self._stories.values():
            # Check query match
            if not (
                query_lower in story.title.lower() or
                query_lower in story.narrative.lower() or
                query_lower in story.subject.lower() or
                any(query_lower in tag.lower() for tag in story.tags)
            ):
                continue

            # Check story type filter
            if story_types and story.story_type not in story_types:
                continue

            # Check significance filter
            if min_significance:
                significance_order = list(HeritageSignificance)
                if significance_order.index(story.significance) > significance_order.index(min_significance):
                    continue

            results.append(story)

        return results

    def __repr__(self) -> str:
        return (
            f"<HeritageKeeper(stories={len(self._stories)}, "
            f"wisdom_subjects={len(self._tribal_wisdom)})>"
        )
