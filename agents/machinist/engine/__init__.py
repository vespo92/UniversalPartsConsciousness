"""
MACHINIST Agent Engine Modules

Industrial equipment intelligence engines for:
- CNC retrofit solutions
- PLC platform migration
- Servo drive cross-reference
"""

from .cnc_retrofit import (
    CNCRetrofitEngine,
    RetrofitComplexity,
    ControlGeneration,
    RetrofitVendor,
    MonitorRetrofitSpec,
    ControlRetrofitSpec,
)

from .plc_migration import (
    PLCMigrationEngine,
    PLCStatus,
    MigrationRisk,
    PLCPlatform,
    IOModule,
    MigrationMapping,
    CodeConversionResult,
)

from .servo_crossref import (
    ServoCrossReferenceEngine,
    DriveType,
    EncoderInterface,
    CommunicationProtocol,
    ServoDriveSpec,
    CrossReferenceMatch,
)

__all__ = [
    # CNC Retrofit
    "CNCRetrofitEngine",
    "RetrofitComplexity",
    "ControlGeneration",
    "RetrofitVendor",
    "MonitorRetrofitSpec",
    "ControlRetrofitSpec",

    # PLC Migration
    "PLCMigrationEngine",
    "PLCStatus",
    "MigrationRisk",
    "PLCPlatform",
    "IOModule",
    "MigrationMapping",
    "CodeConversionResult",

    # Servo Cross-Reference
    "ServoCrossReferenceEngine",
    "DriveType",
    "EncoderInterface",
    "CommunicationProtocol",
    "ServoDriveSpec",
    "CrossReferenceMatch",
]
