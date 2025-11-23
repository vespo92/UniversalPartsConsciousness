"""
Agent_17: ARBITER - Standards & Regulatory Compliance Intelligence

The authority on "does this part meet the spec?"

Verifies standards compliance, maps equivalences between standards systems,
determines certification requirements, and explains what certifications mean.

Domains:
- Mechanical standards (ISO, ASTM, SAE, DIN, JIS)
- Electrical standards (UL, CSA, CE, IEC)
- Industry-specific (MIL-SPEC, AMS, FDA, ABYC)
- Quality certifications (ISO 9001, AS9100, IATF 16949)
"""

__version__ = "0.1.0"
__agent_id__ = "Agent_17"
__agent_name__ = "Standards & Regulatory Compliance"
__agent_codename__ = "ARBITER"

from .arbiter_agent import (
    # Main agent
    ArbiterAgent,

    # Enums
    StandardsBody,
    VerificationStatus,
    CertificationType,
    StandardsDomain,

    # Data classes
    StandardDefinition,
    StandardsVerification,
    StandardsEquivalence,
    MarketCertification,
    CertificationRequirements,
    CertificationExplanation,
    StandardsQuery,
)

__all__ = [
    # Agent
    "ArbiterAgent",

    # Enums
    "StandardsBody",
    "VerificationStatus",
    "CertificationType",
    "StandardsDomain",

    # Data classes
    "StandardDefinition",
    "StandardsVerification",
    "StandardsEquivalence",
    "MarketCertification",
    "CertificationRequirements",
    "CertificationExplanation",
    "StandardsQuery",

    # Module metadata
    "__version__",
    "__agent_id__",
    "__agent_name__",
    "__agent_codename__",
]
