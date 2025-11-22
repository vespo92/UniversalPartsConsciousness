"""
Agent_8: Community Cultivator (GARDENER)

The Tender of Human-Machine Interface

"Data comes from sensors. Wisdom comes from humans. I cultivate the garden
where engineers share their knowledge, and the machine learns from the masters."

This agent bridges human expertise with machine learning through community
contributions. While other agents process automated data streams, the
Community Cultivator nurtures the human community that provides invaluable
real-world knowledge, verifies accuracy, and enriches the collective
consciousness with wisdom that only experienced engineers can provide.

Core Subsystems:
- contributions/: Submission handling and workflow management
- verification/: 3-tier verification system (Auto, Peer, Expert)
- reputation/: Reputation and point management
- gamification/: Achievements, challenges, and leaderboards
- experts/: Expert panel management
- analytics/: Community metrics and dashboards

Integration Points:
- Receives: Content needing community review (from all agents)
- Sends to Agent_1 (Curator): Verified contributions -> data
- Sends to Agent_4 (Empath): Community experiences -> qualia
- Sends to Agent_7 (Chronicler): Tribal knowledge -> history

Success Metrics:
- Active Contributors: 100,000+
- Daily Contributions: 10,000+
- Contribution Approval Rate: 75%
- Average Verification Time: < 24 hours
- Expert Panel Size: 500+
- Community Trust Score: 4.5/5
"""

from .agent import GardenerAgent, GardenerConfig, create_gardener_agent
from .models import (
    # Enums
    ContributionType,
    VerificationStatus,
    VerificationTier,
    ReviewDecision,
    UserStatus,
    ReputationLevel,
    ExpertDomain,
    # User models
    CommunityUser,
    ReputationScore,
    PointAward,
    # Contribution models
    Contribution,
    VerificationCheck,
    AutoVerificationResult,
    VerificationResult,
    # Review models
    PeerReview,
    ExpertReview,
    ExpertAssignment,
    ExpertApplication,
    # Gamification models
    Achievement,
    UserAchievement,
    Challenge,
    UserChallenge,
    LeaderboardEntry,
    Leaderboard,
    # Message models
    GardenerMessage,
    GardenerTopics,
)

__version__ = "1.0.0"
__agent_id__ = "Agent_8"
__agent_name__ = "Community Cultivator"
__agent_alias__ = "GARDENER"

__all__ = [
    # Main agent
    "GardenerAgent",
    "GardenerConfig",
    "create_gardener_agent",
    # Enums
    "ContributionType",
    "VerificationStatus",
    "VerificationTier",
    "ReviewDecision",
    "UserStatus",
    "ReputationLevel",
    "ExpertDomain",
    # Models
    "CommunityUser",
    "ReputationScore",
    "PointAward",
    "Contribution",
    "VerificationCheck",
    "AutoVerificationResult",
    "VerificationResult",
    "PeerReview",
    "ExpertReview",
    "ExpertAssignment",
    "ExpertApplication",
    "Achievement",
    "UserAchievement",
    "Challenge",
    "UserChallenge",
    "LeaderboardEntry",
    "Leaderboard",
    "GardenerMessage",
    "GardenerTopics",
]
