"""
Cultural Analyzer - Deep cultural significance analysis.

Analyzes the cultural impact, community presence, and
cultural significance of engines and parts.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CommunityPresence:
    """Community presence metrics for an engine."""
    forums: List[str] = field(default_factory=list)
    facebook_groups: List[str] = field(default_factory=list)
    discord_servers: List[str] = field(default_factory=list)
    youtube_channels: List[str] = field(default_factory=list)
    instagram_hashtags: List[str] = field(default_factory=list)
    subreddits: List[str] = field(default_factory=list)
    estimated_community_size: int = 0


@dataclass
class MediaPresence:
    """Media and pop culture presence for an engine."""
    movies: List[str] = field(default_factory=list)
    video_games: List[str] = field(default_factory=list)
    music_references: List[str] = field(default_factory=list)
    television: List[str] = field(default_factory=list)
    notable_builds: List[str] = field(default_factory=list)
    influencer_features: List[str] = field(default_factory=list)


@dataclass
class CulturalAnalysisResult:
    """Complete cultural analysis result."""
    engine_code: str
    analysis_date: str
    community_presence: CommunityPresence
    media_presence: MediaPresence
    cultural_era: str
    primary_community: str
    cultural_narrative: str
    significance_score: float


# Known cultural data for legendary engines
CULTURAL_DATABASE = {
    "2JZ-GTE": {
        "community_presence": {
            "forums": ["Supraforums.com", "Supra.mk4.com", "Club4AG"],
            "youtube_channels": ["Cleetus McFarland", "1320Video", "Papadakis Racing"],
            "estimated_community_size": 500000
        },
        "media_presence": {
            "movies": ["The Fast and the Furious (2001)", "Fast & Furious (2009)"],
            "video_games": ["Gran Turismo Series", "Forza Series", "Need for Speed"],
            "notable_builds": ["Orange Man Bad Supra", "Titan Motorsports 1500HP"]
        },
        "cultural_era": "Golden Age of JDM (1993-2002)",
        "primary_community": "JDM Tuning / Import Scene",
        "cultural_narrative": (
            "The 2JZ-GTE became the stuff of legend through its seemingly "
            "unlimited power potential on the stock bottom end. It democratized "
            "1000+ HP builds and became the heart of countless record-breaking cars."
        )
    },
    "13B-REW": {
        "community_presence": {
            "forums": ["RX7Club.com", "RotaryRevs.com"],
            "youtube_channels": ["Rob Dahm", "Hoonigan"],
            "estimated_community_size": 150000
        },
        "media_presence": {
            "movies": ["The Fast and the Furious: Tokyo Drift (2006)"],
            "video_games": ["Gran Turismo", "Forza", "Initial D Arcade"],
            "notable_builds": ["Mad Mike's RADBUL", "Rob Dahm 4-Rotor"]
        },
        "cultural_era": "Rotary Renaissance (1992-2002)",
        "primary_community": "Rotary Enthusiasts / Drifting",
        "cultural_narrative": (
            "The 13B-REW represents Mazda's defiant commitment to rotary technology. "
            "The '47 Ronin' engineering team's dedication created an engine that "
            "achieves 215HP/liter naturally aspirated - a feat of engineering art."
        )
    },
    "LS1": {
        "community_presence": {
            "forums": ["LS1Tech.com", "CorvetteForums.com", "LS1.com"],
            "youtube_channels": ["Holley", "Late Model Engines", "Texas Speed"],
            "estimated_community_size": 750000
        },
        "media_presence": {
            "video_games": ["Forza", "Gran Turismo"],
            "notable_builds": ["Leroy the Savage", "Sick Week Cars"]
        },
        "cultural_era": "LS Swap Era (1997-Present)",
        "primary_community": "American Performance / LS Swap",
        "cultural_narrative": (
            "The LS1 initiated a revolution in engine swaps. 'LS swap it' became "
            "the universal answer to any underpowered vehicle. The combination of "
            "power, reliability, and compact size made it the ultimate swap engine."
        )
    },
    "K20A": {
        "community_presence": {
            "forums": ["K20a.org", "Honda-Tech.com", "ClubRSX.com"],
            "youtube_channels": ["Honda Pro Jason", "Speed Academy"],
            "estimated_community_size": 400000
        },
        "media_presence": {
            "video_games": ["Gran Turismo", "Forza", "Need for Speed"],
            "notable_builds": ["Spoon Sports NSX", "Toda Racing Integra"]
        },
        "cultural_era": "Modern VTEC Era (2001-2011)",
        "primary_community": "Honda Tuning / Time Attack",
        "cultural_narrative": (
            "The K20A represented Honda's evolution of the VTEC philosophy - "
            "taking the screaming high-rev character of the B-series and adding "
            "modern technology. It became the heart of countless track weapons."
        )
    },
    "RB26DETT": {
        "community_presence": {
            "forums": ["GTRLife.com", "SAU.com.au", "NAGTROC"],
            "youtube_channels": ["Mighty Car Mods", "Speed Academy"],
            "estimated_community_size": 200000
        },
        "media_presence": {
            "movies": ["Fast & Furious Series", "Wangan Midnight"],
            "video_games": ["Gran Turismo", "Forza", "Initial D"],
            "notable_builds": ["Top Secret V12 GT-R", "HKS R35"]
        },
        "cultural_era": "JDM Golden Era (1989-2002)",
        "primary_community": "GT-R / JDM Performance",
        "cultural_narrative": (
            "The RB26DETT was over-engineered from factory with massive power "
            "potential. The 'gentleman's agreement' of 280HP was a joke - tuners "
            "quickly found 500+ HP on stock internals. It defined the GT-R legend."
        )
    }
}


class CulturalAnalyzer:
    """
    Analyzes the cultural significance and impact of engines.

    Goes beyond raw specifications to understand the human stories,
    community presence, and cultural meaning of mechanical engineering.
    """

    def __init__(self):
        """Initialize the cultural analyzer."""
        self._analysis_cache: Dict[str, CulturalAnalysisResult] = {}

    def analyze(
        self,
        engine_code: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive cultural analysis on an engine.

        Args:
            engine_code: Engine code to analyze
            additional_data: Optional additional cultural data

        Returns:
            Cultural analysis result dictionary
        """
        # Check for known cultural data
        if engine_code in CULTURAL_DATABASE:
            known_data = CULTURAL_DATABASE[engine_code]
            return self._build_analysis(engine_code, known_data)

        # Use provided data or create minimal analysis
        if additional_data:
            return self._build_analysis(engine_code, additional_data)

        return {
            "engine_code": engine_code,
            "analysis_date": datetime.now().isoformat(),
            "status": "insufficient_data",
            "message": f"No cultural data available for {engine_code}. "
                       f"Consider contributing community knowledge."
        }

    def _build_analysis(
        self,
        engine_code: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a complete cultural analysis from data."""
        community = data.get("community_presence", {})
        media = data.get("media_presence", {})

        # Calculate significance score from presence metrics
        community_score = self._score_community_presence(community)
        media_score = self._score_media_presence(media)
        significance_score = (community_score * 0.6) + (media_score * 0.4)

        return {
            "engine_code": engine_code,
            "analysis_date": datetime.now().isoformat(),
            "cultural_era": data.get("cultural_era", "Unknown Era"),
            "primary_community": data.get("primary_community", "General Automotive"),
            "cultural_narrative": data.get("cultural_narrative", ""),
            "community_presence": {
                "forums": community.get("forums", []),
                "youtube_channels": community.get("youtube_channels", []),
                "facebook_groups": community.get("facebook_groups", []),
                "discord_servers": community.get("discord_servers", []),
                "estimated_community_size": community.get("estimated_community_size", 0),
                "presence_score": community_score
            },
            "media_presence": {
                "movies": media.get("movies", []),
                "video_games": media.get("video_games", []),
                "music_references": media.get("music_references", []),
                "notable_builds": media.get("notable_builds", []),
                "presence_score": media_score
            },
            "significance_score": round(significance_score, 3),
            "cultural_impact_summary": self._generate_impact_summary(
                engine_code, significance_score, data
            )
        }

    def _score_community_presence(self, community: Dict[str, Any]) -> float:
        """Score the community presence (0-1)."""
        score = 0.0

        # Forums (weight: 0.3)
        forums = len(community.get("forums", []))
        score += min(0.3, forums * 0.1)

        # YouTube channels (weight: 0.3)
        channels = len(community.get("youtube_channels", []))
        score += min(0.3, channels * 0.1)

        # Community size (weight: 0.4)
        size = community.get("estimated_community_size", 0)
        if size >= 500000:
            score += 0.4
        elif size >= 200000:
            score += 0.3
        elif size >= 100000:
            score += 0.2
        elif size >= 50000:
            score += 0.1

        return min(1.0, score)

    def _score_media_presence(self, media: Dict[str, Any]) -> float:
        """Score the media presence (0-1)."""
        score = 0.0

        # Movies (weight: 0.4)
        movies = len(media.get("movies", []))
        score += min(0.4, movies * 0.15)

        # Video games (weight: 0.3)
        games = len(media.get("video_games", []))
        score += min(0.3, games * 0.1)

        # Notable builds (weight: 0.3)
        builds = len(media.get("notable_builds", []))
        score += min(0.3, builds * 0.1)

        return min(1.0, score)

    def _generate_impact_summary(
        self,
        engine_code: str,
        score: float,
        data: Dict[str, Any]
    ) -> str:
        """Generate a narrative impact summary."""
        if score >= 0.8:
            return (
                f"The {engine_code} has achieved iconic status in automotive culture, "
                f"with significant presence in {data.get('primary_community', 'the community')}. "
                f"Its influence extends beyond performance into popular culture."
            )
        elif score >= 0.5:
            return (
                f"The {engine_code} is well-known among enthusiasts with active "
                f"community support and notable achievements. A respected choice "
                f"for serious builds."
            )
        elif score >= 0.3:
            return (
                f"The {engine_code} has a dedicated but smaller following. "
                f"Known to enthusiasts of {data.get('cultural_era', 'its era')}."
            )
        else:
            return (
                f"The {engine_code} has limited cultural presence but is "
                f"documented for historical completeness."
            )

    def get_cultural_era(self, year: int) -> str:
        """Determine the cultural era for a given year."""
        if year < 1970:
            return "Classic Muscle Era"
        elif year < 1980:
            return "Malaise Era"
        elif year < 1990:
            return "Turbo Era / Group B"
        elif year < 2000:
            return "JDM Golden Age"
        elif year < 2010:
            return "Modern Performance Era"
        elif year < 2020:
            return "Turbo Renaissance"
        else:
            return "Electrification Era"

    def map_community_landscape(
        self,
        engine_code: str
    ) -> Dict[str, Any]:
        """Map the complete community landscape for an engine."""
        if engine_code in CULTURAL_DATABASE:
            data = CULTURAL_DATABASE[engine_code]
            community = data.get("community_presence", {})

            return {
                "engine_code": engine_code,
                "online_communities": {
                    "forums": community.get("forums", []),
                    "social_media": {
                        "facebook_groups": community.get("facebook_groups", []),
                        "discord_servers": community.get("discord_servers", []),
                        "subreddits": community.get("subreddits", [])
                    },
                    "video_content": {
                        "youtube_channels": community.get("youtube_channels", []),
                        "instagram_hashtags": community.get("instagram_hashtags", [])
                    }
                },
                "estimated_total_reach": community.get("estimated_community_size", 0),
                "primary_platform": self._identify_primary_platform(community)
            }

        return {
            "engine_code": engine_code,
            "status": "community_data_needed",
            "message": "Contribute community knowledge to map this engine's landscape."
        }

    def _identify_primary_platform(self, community: Dict[str, Any]) -> str:
        """Identify the primary community platform."""
        platforms = {
            "forums": len(community.get("forums", [])),
            "youtube": len(community.get("youtube_channels", [])),
            "facebook": len(community.get("facebook_groups", [])),
            "discord": len(community.get("discord_servers", []))
        }
        return max(platforms, key=platforms.get) if any(platforms.values()) else "unknown"

    def list_known_engines(self) -> List[str]:
        """List all engines with known cultural data."""
        return list(CULTURAL_DATABASE.keys())
