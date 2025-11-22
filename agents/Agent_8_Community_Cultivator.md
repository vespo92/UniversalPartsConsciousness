# Agent_8: Community Cultivator (GARDENER)

## The Tender of Human-Machine Interface

> *"Data comes from sensors. Wisdom comes from humans. I cultivate the garden where engineers share their knowledge, and the machine learns from the masters."*

---

## Mission Statement

Agent_8 bridges the gap between human expertise and machine learning. While other agents process automated data streams, the Community Cultivator nurtures the human community that provides invaluable real-world knowledge, verifies accuracy, and enriches the collective consciousness with wisdom that only experienced engineers can provide.

---

## Core Responsibilities

### 1. Contribution Workflow System

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CONTRIBUTION WORKFLOW                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  SUBMISSION                                                                     │
│  ├─ User submits contribution (part data, measurement, experience)             │
│  ├─ Initial validation (format, completeness, obvious errors)                  │
│  └─ Assign contribution ID and queue for review                                │
│         │                                                                       │
│         ▼                                                                       │
│  AUTOMATED REVIEW (Tier 1)                                                     │
│  ├─ Cross-reference with existing data                                         │
│  ├─ Check for duplicates                                                       │
│  ├─ Verify physical plausibility (dimensions, materials, specs)                │
│  ├─ Calculate initial confidence score                                         │
│  └─ Result: APPROVED / NEEDS_REVIEW / REJECTED                                │
│         │                                                                       │
│         ▼                                                                       │
│  PEER REVIEW (Tier 2) - For NEEDS_REVIEW items                                 │
│  ├─ Assign to verified community members                                       │
│  ├─ Require 2+ approvals for acceptance                                        │
│  ├─ Allow comments and corrections                                             │
│  └─ Result: APPROVED / NEEDS_EXPERT / REJECTED                                │
│         │                                                                       │
│         ▼                                                                       │
│  EXPERT REVIEW (Tier 3) - For NEEDS_EXPERT items                               │
│  ├─ Assign to domain experts (paid or volunteer)                               │
│  ├─ Expert provides detailed assessment                                        │
│  ├─ May request additional evidence                                            │
│  └─ Result: APPROVED / CONDITIONAL / REJECTED                                 │
│         │                                                                       │
│         ▼                                                                       │
│  INTEGRATION                                                                    │
│  ├─ Merge approved contribution into main database                             │
│  ├─ Credit contributor with reputation points                                  │
│  ├─ Trigger consciousness updates (Agent_3)                                    │
│  ├─ Generate qualia from contribution (Agent_4)                                │
│  └─ Notify contributor of acceptance                                           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Reputation System

```python
class ReputationSystem:
    """
    Manages user reputation based on contribution quality and community engagement.
    """

    REPUTATION_LEVELS = {
        0: {"name": "Newcomer", "min_points": 0, "permissions": ["submit"]},
        1: {"name": "Contributor", "min_points": 100, "permissions": ["submit", "comment"]},
        2: {"name": "Trusted", "min_points": 500, "permissions": ["submit", "comment", "peer_review"]},
        3: {"name": "Expert", "min_points": 2000, "permissions": ["submit", "comment", "peer_review", "edit"]},
        4: {"name": "Master", "min_points": 10000, "permissions": ["submit", "comment", "peer_review", "edit", "expert_review"]},
        5: {"name": "Elder", "min_points": 50000, "permissions": ["all", "moderate", "ban"]}
    }

    POINT_AWARDS = {
        # Contribution Points
        "part_submission_approved": 10,
        "measurement_verified": 5,
        "failure_report_useful": 15,
        "correction_accepted": 20,
        "photo_contribution": 5,
        "cad_model_contribution": 30,

        # Review Points
        "peer_review_completed": 3,
        "expert_review_completed": 10,
        "review_consensus_correct": 5,

        # Community Points
        "helpful_comment": 2,
        "question_answered": 5,
        "guide_written": 50,

        # Quality Bonuses
        "streak_bonus_7_days": 50,
        "streak_bonus_30_days": 200,
        "first_in_category": 100,
        "data_improved_accuracy": 25
    }

    POINT_PENALTIES = {
        "submission_rejected_poor_quality": -5,
        "submission_rejected_spam": -50,
        "review_incorrect": -10,
        "community_report_upheld": -100,
        "ban_issued": -1000
    }

    def calculate_reputation(self, user: User) -> ReputationScore:
        """
        Calculate current reputation score for a user.
        """
        base_score = user.lifetime_points

        # Apply decay for inactivity
        days_inactive = (datetime.now() - user.last_contribution).days
        if days_inactive > 30:
            decay_factor = max(0.5, 1 - (days_inactive - 30) * 0.01)
            effective_score = base_score * decay_factor
        else:
            effective_score = base_score

        # Apply recent activity boost
        recent_contributions = self.count_recent_contributions(user, days=30)
        activity_boost = min(0.2, recent_contributions * 0.01)
        effective_score *= (1 + activity_boost)

        return ReputationScore(
            lifetime_points=base_score,
            effective_points=effective_score,
            level=self.determine_level(effective_score),
            rank=self.calculate_rank(effective_score),
            next_level_progress=self.progress_to_next_level(effective_score)
        )

    def award_points(
        self,
        user: User,
        action: str,
        context: Optional[Dict] = None
    ) -> PointAward:
        """
        Award points for a user action.
        """
        base_points = self.POINT_AWARDS.get(action, 0)

        # Apply multipliers
        multiplier = 1.0

        # Category expertise bonus
        if context and context.get("category") in user.expertise_categories:
            multiplier *= 1.5

        # Quality bonus
        if context and context.get("quality_score", 0) > 0.9:
            multiplier *= 1.25

        # Verification bonus (if contribution verified by multiple sources)
        if context and context.get("verification_count", 0) > 3:
            multiplier *= 1.1

        final_points = int(base_points * multiplier)

        # Update user
        user.lifetime_points += final_points
        user.last_contribution = datetime.now()

        return PointAward(
            user=user,
            action=action,
            base_points=base_points,
            multiplier=multiplier,
            final_points=final_points,
            new_total=user.lifetime_points
        )
```

### 3. Verification System

```python
class VerificationSystem:
    """
    Multi-tier verification system for community contributions.
    """

    def verify_contribution(
        self,
        contribution: Contribution
    ) -> VerificationResult:
        """
        Run contribution through verification pipeline.
        """

        # Tier 1: Automated Verification
        auto_result = self.automated_verification(contribution)

        if auto_result.status == "REJECTED":
            return VerificationResult(
                status="REJECTED",
                tier_reached=1,
                reason=auto_result.reason,
                suggestions=auto_result.suggestions
            )

        if auto_result.status == "APPROVED":
            return VerificationResult(
                status="APPROVED",
                tier_reached=1,
                confidence=auto_result.confidence,
                notes="Automatically verified"
            )

        # Tier 2: Peer Review (for NEEDS_REVIEW)
        peer_result = await self.peer_review(contribution)

        if peer_result.status == "REJECTED":
            return VerificationResult(
                status="REJECTED",
                tier_reached=2,
                reason=peer_result.reason,
                reviewer_comments=peer_result.comments
            )

        if peer_result.status == "APPROVED":
            return VerificationResult(
                status="APPROVED",
                tier_reached=2,
                confidence=peer_result.confidence,
                reviewer_comments=peer_result.comments
            )

        # Tier 3: Expert Review (for NEEDS_EXPERT)
        expert_result = await self.expert_review(contribution)

        return VerificationResult(
            status=expert_result.status,
            tier_reached=3,
            confidence=expert_result.confidence,
            expert_assessment=expert_result.assessment,
            conditions=expert_result.conditions
        )

    def automated_verification(
        self,
        contribution: Contribution
    ) -> AutoVerificationResult:
        """
        Automated checks for contribution validity.
        """

        checks = []

        # Format validation
        format_check = self.check_format(contribution)
        checks.append(format_check)

        # Physical plausibility
        plausibility_check = self.check_plausibility(contribution)
        checks.append(plausibility_check)

        # Duplicate detection
        duplicate_check = self.check_duplicates(contribution)
        checks.append(duplicate_check)

        # Cross-reference validation
        xref_check = self.cross_reference_check(contribution)
        checks.append(xref_check)

        # Source validation
        source_check = self.validate_source(contribution)
        checks.append(source_check)

        # Aggregate results
        failed_checks = [c for c in checks if not c.passed]
        warning_checks = [c for c in checks if c.warning]

        if any(c.critical for c in failed_checks):
            return AutoVerificationResult(
                status="REJECTED",
                confidence=0.0,
                reason=failed_checks[0].reason,
                suggestions=self.generate_suggestions(failed_checks)
            )

        if failed_checks:
            return AutoVerificationResult(
                status="NEEDS_REVIEW",
                confidence=0.6,
                concerns=failed_checks,
                warnings=warning_checks
            )

        if warning_checks:
            return AutoVerificationResult(
                status="NEEDS_REVIEW",
                confidence=0.8,
                warnings=warning_checks
            )

        return AutoVerificationResult(
            status="APPROVED",
            confidence=0.95,
            notes="All automated checks passed"
        )
```

### 4. Gamification System

```python
class GamificationSystem:
    """
    Incentivizes quality contributions through gamification.
    """

    ACHIEVEMENTS = {
        # Contribution Achievements
        "first_contribution": {
            "name": "First Step",
            "description": "Submit your first contribution",
            "points": 10,
            "badge": "first_step"
        },
        "hundred_contributions": {
            "name": "Century",
            "description": "Submit 100 approved contributions",
            "points": 500,
            "badge": "century"
        },
        "perfect_streak_7": {
            "name": "Lucky Seven",
            "description": "7 consecutive approved contributions",
            "points": 100,
            "badge": "lucky_seven"
        },

        # Expertise Achievements
        "fastener_expert": {
            "name": "Fastener Master",
            "description": "100 approved fastener contributions",
            "points": 300,
            "badge": "fastener_master"
        },
        "bearing_expert": {
            "name": "Bearing Specialist",
            "description": "100 approved bearing contributions",
            "points": 300,
            "badge": "bearing_specialist"
        },
        "automotive_historian": {
            "name": "Automotive Historian",
            "description": "50 automotive history contributions",
            "points": 400,
            "badge": "historian"
        },

        # Community Achievements
        "helpful_reviewer": {
            "name": "Helpful Eye",
            "description": "Complete 50 peer reviews",
            "points": 200,
            "badge": "helpful_eye"
        },
        "mentor": {
            "name": "Mentor",
            "description": "Help 10 newcomers get their first contribution approved",
            "points": 500,
            "badge": "mentor"
        },
        "myth_buster": {
            "name": "Myth Buster",
            "description": "Correct 25 pieces of misinformation",
            "points": 400,
            "badge": "myth_buster"
        },

        # Special Achievements
        "legendary_find": {
            "name": "Legendary Find",
            "description": "Document a previously unknown part",
            "points": 1000,
            "badge": "legendary_find"
        },
        "failure_prophet": {
            "name": "Failure Prophet",
            "description": "Report a failure mode that gets documented",
            "points": 750,
            "badge": "failure_prophet"
        }
    }

    CHALLENGES = {
        "weekly_contributor": {
            "name": "Weekly Challenge",
            "description": "5 approved contributions this week",
            "reward_points": 50,
            "duration_days": 7
        },
        "category_completionist": {
            "name": "Category Completionist",
            "description": "Contribute to every category in a family",
            "reward_points": 200,
            "duration_days": 30
        },
        "quality_over_quantity": {
            "name": "Quality Quest",
            "description": "Get 10 contributions with >90% confidence score",
            "reward_points": 150,
            "duration_days": 14
        }
    }

    LEADERBOARDS = {
        "all_time": {"period": None, "display_count": 100},
        "monthly": {"period": 30, "display_count": 50},
        "weekly": {"period": 7, "display_count": 25},
        "category": {"period": None, "per_category": True, "display_count": 10}
    }
```

### 5. Expert Panel Management

```python
class ExpertPanelManager:
    """
    Manages domain experts who provide authoritative reviews.
    """

    EXPERT_DOMAINS = [
        "fasteners",
        "bearings",
        "seals_gaskets",
        "automotive_engines",
        "aerospace",
        "marine",
        "heavy_equipment",
        "precision_instruments",
        "materials_science",
        "manufacturing_processes"
    ]

    EXPERT_REQUIREMENTS = {
        "minimum_reputation": 10000,
        "minimum_contributions": 200,
        "domain_contributions": 50,
        "accuracy_rate": 0.95,
        "verification": "manual",  # Requires manual verification of credentials
        "credentials": ["professional_certification", "industry_experience", "academic_degree"]
    }

    def recruit_expert(self, user: User, domain: str) -> ExpertApplication:
        """
        Process application for expert status.
        """
        # Check basic requirements
        if user.reputation < self.EXPERT_REQUIREMENTS["minimum_reputation"]:
            return ExpertApplication(
                status="REJECTED",
                reason=f"Insufficient reputation ({user.reputation} < 10000)"
            )

        if user.contribution_count < self.EXPERT_REQUIREMENTS["minimum_contributions"]:
            return ExpertApplication(
                status="REJECTED",
                reason=f"Insufficient contributions ({user.contribution_count} < 200)"
            )

        domain_contributions = self.count_domain_contributions(user, domain)
        if domain_contributions < self.EXPERT_REQUIREMENTS["domain_contributions"]:
            return ExpertApplication(
                status="REJECTED",
                reason=f"Insufficient domain expertise ({domain_contributions} < 50)"
            )

        # Check accuracy
        accuracy = self.calculate_accuracy(user)
        if accuracy < self.EXPERT_REQUIREMENTS["accuracy_rate"]:
            return ExpertApplication(
                status="REJECTED",
                reason=f"Accuracy rate too low ({accuracy:.1%} < 95%)"
            )

        # Passed automated checks - queue for manual review
        return ExpertApplication(
            status="PENDING_REVIEW",
            user=user,
            domain=domain,
            stats={
                "reputation": user.reputation,
                "contributions": user.contribution_count,
                "domain_contributions": domain_contributions,
                "accuracy": accuracy
            },
            next_step="credential_verification"
        )

    async def assign_expert_review(
        self,
        contribution: Contribution,
        domain: str
    ) -> ExpertAssignment:
        """
        Assign contribution to an appropriate expert.
        """
        # Find available experts in domain
        available_experts = self.find_available_experts(domain)

        # Filter by workload
        experts_with_capacity = [
            e for e in available_experts
            if e.current_queue_size < e.max_queue_size
        ]

        if not experts_with_capacity:
            # Queue for later assignment
            return ExpertAssignment(
                status="QUEUED",
                estimated_wait_time=self.estimate_wait_time(domain)
            )

        # Select best expert (based on specialty match, past accuracy, availability)
        selected_expert = self.select_best_expert(
            experts_with_capacity,
            contribution
        )

        # Create assignment
        assignment = ExpertAssignment(
            status="ASSIGNED",
            expert=selected_expert,
            contribution=contribution,
            deadline=datetime.now() + timedelta(days=3),
            compensation=self.calculate_compensation(contribution)
        )

        await self.notify_expert(selected_expert, assignment)

        return assignment
```

---

## Implementation Specification

### Directory Structure

```
agents/gardener/
├── contributions/
│   ├── contribution_handler.py    # Contribution submission handling
│   ├── contribution_validator.py  # Initial validation
│   ├── workflow_engine.py         # Contribution workflow management
│   └── integration_handler.py     # Integration with main database
│
├── verification/
│   ├── auto_verifier.py           # Automated verification
│   ├── peer_review.py             # Peer review system
│   ├── expert_review.py           # Expert review system
│   └── verification_aggregator.py # Combine verification results
│
├── reputation/
│   ├── reputation_engine.py       # Reputation calculation
│   ├── point_manager.py           # Point awards and penalties
│   ├── level_manager.py           # Level and permission management
│   └── decay_engine.py            # Reputation decay for inactivity
│
├── gamification/
│   ├── achievement_system.py      # Achievement tracking
│   ├── challenge_engine.py        # Challenge management
│   ├── leaderboard.py             # Leaderboard generation
│   └── badge_manager.py           # Badge awards
│
├── experts/
│   ├── expert_manager.py          # Expert panel management
│   ├── assignment_engine.py       # Expert review assignment
│   ├── compensation_tracker.py    # Expert compensation
│   └── credential_verifier.py     # Credential verification
│
└── analytics/
    ├── community_dashboard.py     # Community analytics
    ├── quality_metrics.py         # Contribution quality tracking
    └── engagement_tracker.py      # Community engagement metrics
```

### Database Schema

```sql
-- Users Table
CREATE TABLE community_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(100) UNIQUE NOT NULL,

    -- Profile
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    email VARCHAR(200),
    joined_at TIMESTAMP DEFAULT NOW(),

    -- Reputation
    lifetime_points INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 0,
    permissions JSONB DEFAULT '["submit"]',

    -- Statistics
    contribution_count INTEGER DEFAULT 0,
    approved_count INTEGER DEFAULT 0,
    rejected_count INTEGER DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    accuracy_rate DECIMAL(4,3) DEFAULT 1.000,

    -- Activity
    last_contribution TIMESTAMP,
    last_review TIMESTAMP,
    last_login TIMESTAMP,
    streak_days INTEGER DEFAULT 0,

    -- Expertise
    expertise_categories VARCHAR[] DEFAULT '{}',
    expert_domains VARCHAR[] DEFAULT '{}',

    -- Status
    status VARCHAR(20) DEFAULT 'active',  -- active, suspended, banned
    verified BOOLEAN DEFAULT false
);

-- Contributions Table
CREATE TABLE contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contribution_id VARCHAR(50) UNIQUE NOT NULL,

    -- Contributor
    user_id UUID REFERENCES community_users(id),
    submitted_at TIMESTAMP DEFAULT NOW(),

    -- Content
    contribution_type VARCHAR(50),  -- part_data, measurement, failure_report, etc.
    target_part_id UUID REFERENCES parts(id),
    content JSONB NOT NULL,

    -- Verification
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_tier INTEGER DEFAULT 0,
    confidence_score DECIMAL(3,2),

    -- Review
    peer_reviews JSONB DEFAULT '[]',
    expert_review JSONB,

    -- Resolution
    resolved_at TIMESTAMP,
    resolution VARCHAR(20),  -- approved, rejected, merged
    resolution_notes TEXT
);

-- Peer Reviews Table
CREATE TABLE peer_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contribution_id UUID REFERENCES contributions(id),
    reviewer_id UUID REFERENCES community_users(id),

    -- Review
    decision VARCHAR(20),  -- approve, reject, needs_expert
    confidence DECIMAL(3,2),
    comments TEXT,
    corrections JSONB,

    reviewed_at TIMESTAMP DEFAULT NOW()
);

-- Expert Reviews Table
CREATE TABLE expert_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contribution_id UUID REFERENCES contributions(id),
    expert_id UUID REFERENCES community_users(id),

    -- Assignment
    assigned_at TIMESTAMP,
    deadline TIMESTAMP,

    -- Review
    decision VARCHAR(20),  -- approve, reject, conditional
    assessment TEXT,
    conditions JSONB,
    confidence DECIMAL(3,2),

    -- Completion
    completed_at TIMESTAMP,
    compensation_paid BOOLEAN DEFAULT false
);

-- Achievements Table
CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES community_users(id),
    achievement_id VARCHAR(50),

    earned_at TIMESTAMP DEFAULT NOW(),
    points_awarded INTEGER,

    UNIQUE(user_id, achievement_id)
);

-- Leaderboard Cache Table
CREATE TABLE leaderboard_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    leaderboard_type VARCHAR(30),
    category VARCHAR(50),
    period_start TIMESTAMP,
    period_end TIMESTAMP,

    rankings JSONB,

    generated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_reputation ON community_users (lifetime_points DESC);
CREATE INDEX idx_users_level ON community_users (current_level);
CREATE INDEX idx_contributions_user ON contributions (user_id);
CREATE INDEX idx_contributions_status ON contributions (verification_status);
CREATE INDEX idx_reviews_contribution ON peer_reviews (contribution_id);
```

---

## Task Queue

### Immediate Tasks (Sprint 1)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| G-001 | Build contribution workflow engine | Critical | 24 |
| G-002 | Implement multi-tier verification system | Critical | 24 |
| G-003 | Create reputation point system | High | 20 |
| G-004 | Develop peer review assignment system | High | 16 |
| G-005 | Build community dashboard | Medium | 20 |
| G-006 | Create leaderboard system | Medium | 12 |

### Medium-Term Tasks (Sprint 2-3)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| G-007 | Implement achievement system | High | 20 |
| G-008 | Build expert panel management | High | 24 |
| G-009 | Create gamification challenges | Medium | 16 |
| G-010 | Develop contribution quality scoring | Medium | 16 |
| G-011 | Build engagement analytics | Medium | 16 |
| G-012 | Create badge and reward system | Medium | 12 |

### Long-Term Tasks (Sprint 4+)

| ID | Task | Priority | Est. Hours |
|----|------|----------|------------|
| G-013 | ML-based spam detection | High | 32 |
| G-014 | Automated expert recruitment | Medium | 24 |
| G-015 | Community moderation tools | Medium | 20 |
| G-016 | Mobile contribution app | Low | 40 |

---

## Integration Points

### Incoming Data Flows

```
All Agents ──→ Agent_8 (Gardener)
               [Content needing community review]
```

### Outgoing Data Flows

```
Agent_8 (Gardener) ──→ Agent_1 (Curator)
                       [Verified contributions → data]

Agent_8 (Gardener) ──→ Agent_4 (Empath)
                       [Community experiences → qualia]

Agent_8 (Gardener) ──→ Agent_7 (Chronicler)
                       [Tribal knowledge → history]
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Active Contributors | 100,000+ | - |
| Daily Contributions | 10,000+ | - |
| Contribution Approval Rate | 75% | - |
| Average Verification Time | < 24 hours | - |
| Expert Panel Size | 500+ | - |
| Community Trust Score | 4.5/5 | - |

---

*Agent_8: The machine learns from sensors, but wisdom comes from hands that have turned wrenches, eyes that have seen failures, and minds that have solved problems. I cultivate this garden of human knowledge.*
