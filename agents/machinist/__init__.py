"""
Agent_13: MACHINIST - Industrial & Manufacturing Equipment Intelligence

The MACHINIST agent provides parts consciousness for industrial machinery,
including CNC machines, PLCs, servo systems, and industrial fasteners.

"Industrial machinery represents billions in capital equipment that must stay running.
When a 1985 CNC needs a part, I know the retrofits, cross-references, and alternatives."

Core Capabilities:
- CNC retrofit solutions (monitors, controls, drives)
- PLC platform migration planning
- Servo drive cross-reference across manufacturers
- Industrial motor compatibility
- Industrial fastener selection for machine applications

Usage:
    from agents.machinist import MachinistAgent

    agent = MachinistAgent()

    # Find CNC retrofit
    retrofits = agent.find_cnc_retrofit("Fanuc", "6M", "CRT Monitor")

    # Cross-reference servo drive
    matches = agent.cross_reference_servo_drives("A06B-6079-H106")

    # Plan PLC migration
    plan = agent.find_plc_migration_path("Allen-Bradley SLC 500")

    # Get industrial fastener recommendation
    fastener = agent.find_industrial_fastener(
        application="CNC spindle mount",
        environment="coolant exposure, vibration",
        load_requirements={"preload_kn": 60}
    )
"""

from .machinist_agent import (
    MachinistAgent,
    EquipmentType,
    ComponentCategory,
    RetrofitType,
    RetrofitSolution,
    ServoDriveMatch,
    PLCMigrationPlan,
    IndustrialMotorSpec,
    IndustrialFastenerRecommendation,
    CNCControllerSpec,
)

# Convenience function
def create_machinist_agent() -> MachinistAgent:
    """Create and configure a MACHINIST Agent instance."""
    return MachinistAgent()


__all__ = [
    # Main agent
    "MachinistAgent",
    "create_machinist_agent",

    # Enums
    "EquipmentType",
    "ComponentCategory",
    "RetrofitType",

    # Data classes
    "RetrofitSolution",
    "ServoDriveMatch",
    "PLCMigrationPlan",
    "IndustrialMotorSpec",
    "IndustrialFastenerRecommendation",
    "CNCControllerSpec",
]

# Agent metadata
__agent_id__ = "AGENT_13"
__agent_name__ = "Industrial Equipment Intelligence"
__agent_alias__ = "MACHINIST"
__version__ = "1.0.0"
