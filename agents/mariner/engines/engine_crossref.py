"""
Marine Engine Cross-Reference Database

Marine engines are often marinized automotive engines. This module reveals
the base automotive engine for parts sourcing, identifying what's shared
versus what's marine-specific (and dangerous to interchange).

CRITICAL SAFETY NOTE:
Certain marine components are IGNITION PROTECTED - automotive equivalents
can cause FIRE or EXPLOSION in the bilge. Never interchange:
- Starters
- Alternators
- Distributors
- Fuel pumps
- Any electrical component in engine compartment
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class EnginePartCategory(Enum):
    """Categories for marine engine parts interchangeability"""
    SHARED = "shared"           # Identical to automotive - safe to interchange
    MARINE_SPECIFIC = "marine"  # Marine-only parts - do not interchange
    NEVER_INTERCHANGE = "never" # SAFETY CRITICAL - automotive = fire/explosion
    MODIFIED = "modified"       # Based on automotive but marine-modified


@dataclass
class MarineEngineXref:
    """Cross-reference between marine and automotive engines"""
    marine_engine: str
    marine_manufacturer: str
    automotive_base: str
    automotive_years: str
    displacement_liters: float

    # Part interchangeability
    shared_parts: Dict[str, str]           # part: notes
    marine_specific_parts: Dict[str, str]  # part: why marine
    never_interchange: Dict[str, str]      # part: danger explanation
    modified_parts: Dict[str, str]         # part: modification details

    # Additional info
    notes: List[str]
    oem_part_numbers: Dict[str, str]
    common_failures: List[str]
    rebuild_tips: List[str]


@dataclass
class PartInterchangeResult:
    """Result of checking part interchangeability"""
    part_name: str
    category: EnginePartCategory
    automotive_part: Optional[str]
    marine_part: Optional[str]
    interchangeable: bool
    danger_level: str  # "NONE", "LOW", "MODERATE", "HIGH", "CRITICAL"
    explanation: str
    cost_savings_percent: Optional[int]
    warnings: List[str]


class MarineEngineCrossReference:
    """
    Marine to automotive engine cross-reference database.

    Covers major marinizers:
    - Mercruiser (GM-based)
    - Volvo Penta (GM and Volvo)
    - Crusader (Ford-based)
    - Indmar (GM-based, ski boats)
    - PCM (GM-based, wake boats)
    - Yamaha Marine
    - Honda Marine
    """

    def __init__(self):
        self.engines: Dict[str, MarineEngineXref] = self._build_database()
        self._part_warnings = self._build_part_warnings()

    def _build_database(self) -> Dict[str, MarineEngineXref]:
        """Build the comprehensive engine cross-reference database"""
        return {
            # Mercruiser GM-Based
            "mercruiser_5.7_mpi": MarineEngineXref(
                marine_engine="Mercruiser 5.7L MPI (350 MAG)",
                marine_manufacturer="Mercury Marine",
                automotive_base="GM Vortec 5700 (L31)",
                automotive_years="1996-2002 Chevy/GMC Truck",
                displacement_liters=5.7,
                shared_parts={
                    "Pistons": "Identical to truck - standard bore 4.00\"",
                    "Connecting rods": "Identical - pressed pin",
                    "Crankshaft": "Same casting, marine balanced",
                    "Cylinder heads": "Vortec castings, same cores",
                    "Block": "Same GM Gen I casting #10243880",
                    "Timing chain/gears": "Standard GM small block",
                    "Oil pump": "Standard volume, same as truck",
                    "Lifters": "Hydraulic, identical",
                    "Camshaft": "Different grind - marine is milder",
                    "Valves": "Same size, marine may be sodium-filled exhaust",
                    "Rocker arms": "Identical 1.5:1 ratio",
                    "Pushrods": "Same length and diameter",
                },
                marine_specific_parts={
                    "Intake manifold": "Cast for marine coolant passages",
                    "Exhaust manifolds": "Water-cooled, CRITICAL - no automotive",
                    "Water pump": "Raw water pump, different from auto",
                    "Thermostat housing": "Marine-specific with water passages",
                    "Oil pan": "Low profile for boat transmission",
                    "Flywheel": "Marine adapter pattern",
                    "Harmonic balancer": "May have sensor ring difference",
                    "Throttle body": "Marine calibration, ignition protected",
                    "ECM/PCM": "Marine calibration, ignition protected",
                },
                never_interchange={
                    "Starter": "Marine is IGNITION PROTECTED - automotive can spark and EXPLODE fuel vapors",
                    "Alternator": "Marine is sealed and ignition protected - auto will corrode AND can cause fire",
                    "Distributor": "Marine cap is ignition protected - auto can arc and ignite vapors",
                    "Fuel pump": "Marine is sealed - automotive can leak vapors",
                    "Carburetor/TBI": "Marine has flame arrestor - automotive = FIRE HAZARD",
                    "Exhaust manifolds": "Automotive will OVERHEAT and burn through - water cooling required",
                    "Ignition coil": "Marine is sealed and ignition protected",
                },
                modified_parts={
                    "Camshaft": "Marine grind is milder for continuous operation",
                    "Head gaskets": "Marine may have different coolant passages",
                    "Valve covers": "May have marine breather system",
                },
                notes=[
                    "5.7L MPI uses same block and heads as Vortec truck engine",
                    "Internal engine parts (pistons, rods, crank) are IDENTICAL",
                    "Save significant money on internal rebuild parts",
                    "NEVER use automotive electrical or exhaust components",
                    "Truck crate engines can be marinized with correct parts",
                ],
                oem_part_numbers={
                    "Block": "GM 10243880 / Mercury 863432A4",
                    "Pistons": "GM 12551388 / Mercury 812863A1",
                    "Intake manifold": "Mercury 806256A2 (NO automotive equivalent)",
                },
                common_failures=[
                    "Exhaust manifold/riser corrosion (water intrusion)",
                    "Raw water pump impeller failure",
                    "Distributor cap cracking from heat/humidity",
                    "Thermostat stuck closed causing overheat",
                ],
                rebuild_tips=[
                    "Use truck pistons - 1/3 the price of marine",
                    "ALWAYS replace exhaust manifold gaskets with OEM",
                    "Use marine thermostat - 143F vs 195F automotive",
                    "Never reuse exhaust manifold bolts - replace with 316SS",
                ],
            ),

            "mercruiser_4.3_vortec": MarineEngineXref(
                marine_engine="Mercruiser 4.3L MPI",
                marine_manufacturer="Mercury Marine",
                automotive_base="GM Vortec 4300 (L35/LF6)",
                automotive_years="1996-2007 S10/Blazer/Astro",
                displacement_liters=4.3,
                shared_parts={
                    "Pistons": "Same as truck 4.3",
                    "Connecting rods": "Identical",
                    "Crankshaft": "Same 90-degree V6",
                    "Cylinder heads": "Vortec castings",
                    "Block": "GM 10238181 and others",
                    "Timing chain": "Standard GM",
                },
                marine_specific_parts={
                    "Intake manifold": "Marine water passages",
                    "Exhaust manifolds": "Water-cooled",
                    "All cooling system": "Raw water",
                },
                never_interchange={
                    "Starter": "IGNITION PROTECTED required",
                    "Alternator": "Marine sealed and ignition protected",
                    "Distributor": "Ignition protected cap",
                    "Exhaust manifolds": "Must be water-cooled",
                },
                modified_parts={
                    "Camshaft": "Marine grind",
                },
                notes=[
                    "Most popular sterndrive engine",
                    "Shares most internal parts with truck 4.3",
                    "Common swap from carbureted to MPI",
                ],
                oem_part_numbers={},
                common_failures=[
                    "Spider injector failure on older units",
                    "Intake manifold gasket leaks",
                    "Distributor gear wear",
                ],
                rebuild_tips=[
                    "Use truck rebuild kit for internals",
                    "Replace spider injector with MPI upgrade kit",
                ],
            ),

            "volvo_penta_5.0_gxi": MarineEngineXref(
                marine_engine="Volvo Penta 5.0L GXi",
                marine_manufacturer="Volvo Penta",
                automotive_base="GM Vortec 5000 (L30)",
                automotive_years="1999-2007 Chevy/GMC Truck",
                displacement_liters=5.0,
                shared_parts={
                    "Block": "GM casting",
                    "Crankshaft": "Identical to truck",
                    "Pistons": "Same bore/stroke as truck",
                    "Cylinder heads": "Vortec design",
                },
                marine_specific_parts={
                    "Complete fuel system": "Volvo EFI system",
                    "Cooling system": "Volvo closed-cooling option",
                    "Drive adapter": "Volvo SX/DP drive specific",
                    "Electrical system": "Volvo harness and ECU",
                },
                never_interchange={
                    "Any electrical": "Volvo proprietary system",
                    "Fuel system": "Marine ignition protected",
                    "Exhaust": "Water-cooled required",
                },
                modified_parts={
                    "Flywheel": "Volvo drive pattern",
                },
                notes=[
                    "Internal engine is GM - external is Volvo",
                    "Volvo EFI uses proprietary calibration",
                    "Drive coupling is Volvo-specific",
                ],
                oem_part_numbers={},
                common_failures=[
                    "Drive bellows failure",
                    "U-joint corrosion",
                ],
                rebuild_tips=[
                    "Use GM internal parts",
                    "MUST use Volvo fuel and electrical",
                ],
            ),

            "mercruiser_8.2_mag": MarineEngineXref(
                marine_engine="Mercruiser 8.2L MAG (502)",
                marine_manufacturer="Mercury Marine",
                automotive_base="GM 502 Big Block (L19)",
                automotive_years="1996-2000 GM Performance",
                displacement_liters=8.2,
                shared_parts={
                    "Block": "GM Mark VI big block",
                    "Crankshaft": "Forged 4340",
                    "Pistons": "Forged, identical specs",
                    "Connecting rods": "Forged, identical",
                    "Cylinder heads": "Oval port castings",
                },
                marine_specific_parts={
                    "Intake manifold": "Marine coolant routing",
                    "Exhaust": "Water-cooled mandatory",
                    "Fuel system": "High-capacity marine",
                },
                never_interchange={
                    "Starter": "High-torque marine, ignition protected",
                    "Alternator": "High-output marine",
                    "Exhaust manifolds": "MUST be water-cooled",
                },
                modified_parts={
                    "Oil pan": "Marine sump design",
                },
                notes=[
                    "Big block GM - internal parts interchange",
                    "Popular in larger cruisers and performance boats",
                    "Truck 454/502 internals are cheaper",
                ],
                oem_part_numbers={},
                common_failures=[
                    "Exhaust manifold cracking",
                    "Raw water pump wear",
                ],
                rebuild_tips=[
                    "Use GM performance rebuild kits",
                    "Check riser condition - replace if any doubt",
                ],
            ),

            "crusader_5.7_ford": MarineEngineXref(
                marine_engine="Crusader 350 (5.7L)",
                marine_manufacturer="Crusader Engines (!"
                " Pleasurecraft)",
                automotive_base="Ford 351W Windsor",
                automotive_years="1969-1997 Ford Truck/Bronco",
                displacement_liters=5.8,
                shared_parts={
                    "Block": "Ford 351W casting",
                    "Pistons": "Ford spec",
                    "Crankshaft": "Ford 351W",
                    "Cylinder heads": "Ford GT40 or similar",
                },
                marine_specific_parts={
                    "Intake": "Marine-specific",
                    "Exhaust": "Water-cooled",
                    "Cooling": "Raw water system",
                },
                never_interchange={
                    "Electrical": "Marine ignition protected",
                    "Exhaust": "Water-cooled only",
                },
                modified_parts={
                    "Flywheel": "Crusader pattern",
                },
                notes=[
                    "Ford-based unlike most marine (GM)",
                    "351W truck parts work for internals",
                    "Different than Crusader GM-based engines",
                ],
                oem_part_numbers={},
                common_failures=[
                    "Timing cover leaks",
                ],
                rebuild_tips=[
                    "Use Ford Motorsport parts",
                ],
            ),

            "indmar_6.0_assault": MarineEngineXref(
                marine_engine="Indmar 6.0L Assault (Monsoon)",
                marine_manufacturer="Indmar Products",
                automotive_base="GM Vortec 6000 (LQ4/LQ9)",
                automotive_years="1999-2007 GM Truck LS-based",
                displacement_liters=6.0,
                shared_parts={
                    "Block": "LS architecture, Gen III/IV",
                    "Pistons": "LS truck spec",
                    "Crankshaft": "LS design",
                    "Cylinder heads": "LS cathedral port",
                    "Camshaft": "Different grind but compatible",
                },
                marine_specific_parts={
                    "ECM": "Marine calibration",
                    "Exhaust manifolds": "Water-cooled",
                    "Intake": "Marine throttle body",
                },
                never_interchange={
                    "Electrical": "Marine ignition protection",
                    "Exhaust": "Water-cooled only",
                },
                modified_parts={
                    "Oil pan": "Ski boat sump",
                    "Accessory drive": "Marine layout",
                },
                notes=[
                    "LS-based engine - modern architecture",
                    "Popular in Mastercraft, Malibu wake boats",
                    "Truck LS parts widely available",
                ],
                oem_part_numbers={},
                common_failures=[
                    "Timing cover seal",
                    "Knock sensor issues",
                ],
                rebuild_tips=[
                    "Use LS truck rebuild kits",
                    "Cathedral port heads are common",
                ],
            ),
        }

    def _build_part_warnings(self) -> Dict[str, str]:
        """Build universal part interchange warnings"""
        return {
            "starter": "NEVER use automotive starter - not ignition protected. Marine starters are sealed to prevent sparks that can ignite fuel vapors in the bilge. Using automotive starter = FIRE/EXPLOSION RISK.",
            "alternator": "NEVER use automotive alternator. Marine alternators are ignition protected (no sparking) and corrosion resistant. Automotive will fail quickly and may cause fire.",
            "distributor": "Marine distributor caps are ignition protected. Automotive caps can arc and ignite vapors. Always use marine.",
            "carburetor": "Marine carburetors have flame arrestors. Automotive carburetors on a boat = FIRE HAZARD. Coast Guard requirement.",
            "fuel_pump": "Marine fuel pumps are sealed and ignition protected. Automotive can leak vapors. Fire risk.",
            "exhaust_manifold": "Automotive exhaust manifolds will OVERHEAT and burn through. Marine manifolds are water-cooled. Non-negotiable.",
            "coil": "Marine ignition coils are sealed. Automotive can arc externally. Fire risk.",
        }

    def find_engine(
        self,
        manufacturer: str,
        model: str
    ) -> Optional[MarineEngineXref]:
        """
        Find engine cross-reference by manufacturer and model.

        Args:
            manufacturer: Engine brand (Mercruiser, Volvo Penta, etc.)
            model: Engine model or displacement

        Returns:
            MarineEngineXref if found, None otherwise
        """
        search_key = f"{manufacturer.lower()}_{model.lower().replace(' ', '_').replace('.', '_')}"

        # Direct match
        for key, engine in self.engines.items():
            if search_key in key:
                return engine

        # Partial match on displacement
        for key, engine in self.engines.items():
            if manufacturer.lower() in key:
                if model.replace("L", "").replace("l", "") in str(engine.displacement_liters):
                    return engine

        return None

    def check_part_interchange(
        self,
        engine_key: str,
        part_name: str
    ) -> PartInterchangeResult:
        """
        Check if a specific part can be interchanged with automotive.

        Args:
            engine_key: Engine identifier
            part_name: Part to check

        Returns:
            Detailed interchange assessment
        """
        engine = self.engines.get(engine_key)
        if not engine:
            return PartInterchangeResult(
                part_name=part_name,
                category=EnginePartCategory.MARINE_SPECIFIC,
                automotive_part=None,
                marine_part=None,
                interchangeable=False,
                danger_level="UNKNOWN",
                explanation="Engine not found in database",
                cost_savings_percent=None,
                warnings=["Verify engine identification"],
            )

        part_lower = part_name.lower()

        # Check NEVER interchange first
        for never_part, danger in engine.never_interchange.items():
            if part_lower in never_part.lower() or never_part.lower() in part_lower:
                return PartInterchangeResult(
                    part_name=part_name,
                    category=EnginePartCategory.NEVER_INTERCHANGE,
                    automotive_part="DO NOT USE",
                    marine_part=f"Marine {part_name}",
                    interchangeable=False,
                    danger_level="CRITICAL",
                    explanation=danger,
                    cost_savings_percent=None,
                    warnings=[
                        "FIRE/EXPLOSION HAZARD",
                        "Coast Guard requirement",
                        "Never use automotive for this part",
                    ],
                )

        # Check shared parts
        for shared_part, notes in engine.shared_parts.items():
            if part_lower in shared_part.lower() or shared_part.lower() in part_lower:
                return PartInterchangeResult(
                    part_name=part_name,
                    category=EnginePartCategory.SHARED,
                    automotive_part=f"{engine.automotive_base} {shared_part}",
                    marine_part=f"{engine.marine_engine} {shared_part}",
                    interchangeable=True,
                    danger_level="NONE",
                    explanation=notes,
                    cost_savings_percent=50,  # Typical automotive savings
                    warnings=[],
                )

        # Check marine-specific
        for marine_part, reason in engine.marine_specific_parts.items():
            if part_lower in marine_part.lower() or marine_part.lower() in part_lower:
                return PartInterchangeResult(
                    part_name=part_name,
                    category=EnginePartCategory.MARINE_SPECIFIC,
                    automotive_part=None,
                    marine_part=f"Marine {part_name}",
                    interchangeable=False,
                    danger_level="MODERATE",
                    explanation=reason,
                    cost_savings_percent=None,
                    warnings=["Must use marine-specific part"],
                )

        # Default - unknown
        return PartInterchangeResult(
            part_name=part_name,
            category=EnginePartCategory.MARINE_SPECIFIC,
            automotive_part=None,
            marine_part=None,
            interchangeable=False,
            danger_level="UNKNOWN",
            explanation="Part not specifically categorized - assume marine-specific for safety",
            cost_savings_percent=None,
            warnings=["Verify with manufacturer before interchanging"],
        )

    def get_parts_list(
        self,
        engine_key: str,
        category: Optional[EnginePartCategory] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        Get all parts for an engine, optionally filtered by category.

        Returns:
            Dictionary of part categories with parts and notes
        """
        engine = self.engines.get(engine_key)
        if not engine:
            return {}

        if category == EnginePartCategory.SHARED:
            return {"shared": engine.shared_parts}
        elif category == EnginePartCategory.MARINE_SPECIFIC:
            return {"marine_specific": engine.marine_specific_parts}
        elif category == EnginePartCategory.NEVER_INTERCHANGE:
            return {"never_interchange": engine.never_interchange}
        elif category == EnginePartCategory.MODIFIED:
            return {"modified": engine.modified_parts}
        else:
            return {
                "shared": engine.shared_parts,
                "marine_specific": engine.marine_specific_parts,
                "never_interchange": engine.never_interchange,
                "modified": engine.modified_parts,
            }

    def get_safety_critical_parts(self) -> List[str]:
        """Get list of parts that must NEVER be automotive"""
        return list(self._part_warnings.keys())

    def get_part_warning(self, part_name: str) -> Optional[str]:
        """Get safety warning for a part type"""
        for key, warning in self._part_warnings.items():
            if key in part_name.lower():
                return warning
        return None
