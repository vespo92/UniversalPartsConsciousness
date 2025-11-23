"""
Sterilization Compatibility Module

Provides material-sterilization compatibility data and guidance for
medical device materials.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class SterilizationMethod(Enum):
    """Medical device sterilization methods"""
    STEAM_121 = "steam_121c"           # Autoclave 121°C
    STEAM_134 = "steam_134c"           # Autoclave 134°C
    ETO = "ethylene_oxide"             # EtO gas
    GAMMA = "gamma_radiation"          # Gamma (Co-60)
    EBEAM = "electron_beam"            # E-beam
    H2O2_PLASMA = "h2o2_plasma"        # Hydrogen peroxide plasma
    DRY_HEAT = "dry_heat"              # Dry heat sterilization
    PERACETIC_ACID = "peracetic_acid"  # Liquid chemical


@dataclass
class SterilizationMethodInfo:
    """Information about a sterilization method"""
    method: SterilizationMethod
    temperature_c: Tuple[float, float]  # Min, max
    validation_standard: str
    typical_cycle_time_min: int
    advantages: List[str]
    disadvantages: List[str]
    material_restrictions: List[str]


# Sterilization method reference data
STERILIZATION_METHODS: Dict[SterilizationMethod, SterilizationMethodInfo] = {
    SterilizationMethod.STEAM_121: SterilizationMethodInfo(
        method=SterilizationMethod.STEAM_121,
        temperature_c=(121, 121),
        validation_standard="ISO 17665",
        typical_cycle_time_min=20,
        advantages=[
            "No toxic residues",
            "Fast cycle time",
            "Well established",
            "Low cost"
        ],
        disadvantages=[
            "Heat and moisture damage",
            "Not for heat-sensitive materials",
            "Requires drying cycle"
        ],
        material_restrictions=[
            "ABS (deforms)",
            "Polycarbonate (stress cracks)",
            "Low-density polyethylene",
            "Some rubber compounds"
        ]
    ),
    SterilizationMethod.STEAM_134: SterilizationMethodInfo(
        method=SterilizationMethod.STEAM_134,
        temperature_c=(134, 134),
        validation_standard="ISO 17665",
        typical_cycle_time_min=5,
        advantages=[
            "Faster than 121°C",
            "Prion inactivation",
            "No toxic residues"
        ],
        disadvantages=[
            "Higher heat damage",
            "More restrictive material compatibility"
        ],
        material_restrictions=[
            "All 121°C restrictions apply",
            "Some high-temperature polymers limited"
        ]
    ),
    SterilizationMethod.ETO: SterilizationMethodInfo(
        method=SterilizationMethod.ETO,
        temperature_c=(37, 55),
        validation_standard="ISO 11135",
        typical_cycle_time_min=720,  # 12+ hours with aeration
        advantages=[
            "Low temperature",
            "Excellent material compatibility",
            "Penetrates packaging"
        ],
        disadvantages=[
            "Toxic residues (require aeration)",
            "Long cycle time",
            "Environmental concerns",
            "Explosive hazard"
        ],
        material_restrictions=[
            "Minimal material restrictions",
            "Residue concerns for some polymers"
        ]
    ),
    SterilizationMethod.GAMMA: SterilizationMethodInfo(
        method=SterilizationMethod.GAMMA,
        temperature_c=(20, 40),
        validation_standard="ISO 11137",
        typical_cycle_time_min=180,
        advantages=[
            "Low temperature",
            "Deep penetration",
            "Precise dosing"
        ],
        disadvantages=[
            "Material degradation",
            "Cannot be used in-house",
            "Some color changes"
        ],
        material_restrictions=[
            "PTFE (degrades)",
            "Acetals (degrades)",
            "Some polypropylenes",
            "UHMWPE (oxidation in air)"
        ]
    ),
    SterilizationMethod.H2O2_PLASMA: SterilizationMethodInfo(
        method=SterilizationMethod.H2O2_PLASMA,
        temperature_c=(45, 55),
        validation_standard="ISO 14937",
        typical_cycle_time_min=75,
        advantages=[
            "Low temperature",
            "No toxic residues",
            "Short cycle time",
            "Good for electronics"
        ],
        disadvantages=[
            "Limited penetration",
            "Not for cellulose",
            "Higher cost"
        ],
        material_restrictions=[
            "Cellulose materials",
            "Nylon (absorbs H2O2)",
            "Some liquids"
        ]
    ),
}


# Material compatibility matrix
# Format: (material, method) -> (compatible, max_cycles, notes)
MATERIAL_COMPATIBILITY: Dict[Tuple[str, SterilizationMethod], Tuple[bool, int, str]] = {
    # PEEK
    ("PEEK", SterilizationMethod.STEAM_121): (True, 3000, "Excellent resistance"),
    ("PEEK", SterilizationMethod.STEAM_134): (True, 3000, "Excellent resistance"),
    ("PEEK", SterilizationMethod.ETO): (True, 1000, "Compatible"),
    ("PEEK", SterilizationMethod.GAMMA): (True, 10, "May affect mechanical properties"),
    ("PEEK", SterilizationMethod.H2O2_PLASMA): (True, 500, "Compatible"),

    # PPSU
    ("PPSU", SterilizationMethod.STEAM_121): (True, 1000, "Excellent steam resistance"),
    ("PPSU", SterilizationMethod.STEAM_134): (True, 1000, "Excellent steam resistance"),
    ("PPSU", SterilizationMethod.ETO): (True, 500, "Compatible"),
    ("PPSU", SterilizationMethod.GAMMA): (True, 5, "Limited - may yellow"),
    ("PPSU", SterilizationMethod.H2O2_PLASMA): (True, 500, "Compatible"),

    # ABS
    ("ABS", SterilizationMethod.STEAM_121): (False, 0, "HDT ~98°C, will deform"),
    ("ABS", SterilizationMethod.STEAM_134): (False, 0, "Will deform and degrade"),
    ("ABS", SterilizationMethod.ETO): (True, 100, "Compatible"),
    ("ABS", SterilizationMethod.GAMMA): (True, 10, "May yellow and embrittle"),
    ("ABS", SterilizationMethod.H2O2_PLASMA): (True, 100, "Compatible"),

    # Polycarbonate
    ("Polycarbonate", SterilizationMethod.STEAM_121): (False, 0, "Stress cracking"),
    ("Polycarbonate", SterilizationMethod.STEAM_134): (False, 0, "Severe degradation"),
    ("Polycarbonate", SterilizationMethod.ETO): (True, 50, "Compatible"),
    ("Polycarbonate", SterilizationMethod.GAMMA): (True, 5, "Yellowing, embrittlement"),
    ("Polycarbonate", SterilizationMethod.H2O2_PLASMA): (True, 50, "Compatible"),

    # Silicone
    ("Silicone", SterilizationMethod.STEAM_121): (True, 500, "Compatible"),
    ("Silicone", SterilizationMethod.STEAM_134): (True, 500, "Compatible"),
    ("Silicone", SterilizationMethod.ETO): (True, 500, "Compatible"),
    ("Silicone", SterilizationMethod.GAMMA): (True, 100, "May affect properties over time"),
    ("Silicone", SterilizationMethod.H2O2_PLASMA): (True, 100, "Compatible"),

    # Stainless Steel 316L
    ("316L", SterilizationMethod.STEAM_121): (True, 10000, "Excellent"),
    ("316L", SterilizationMethod.STEAM_134): (True, 10000, "Excellent"),
    ("316L", SterilizationMethod.ETO): (True, 10000, "Excellent"),
    ("316L", SterilizationMethod.GAMMA): (True, 10000, "Excellent"),
    ("316L", SterilizationMethod.H2O2_PLASMA): (True, 10000, "Excellent"),

    # Titanium
    ("Titanium", SterilizationMethod.STEAM_121): (True, 10000, "Excellent"),
    ("Titanium", SterilizationMethod.STEAM_134): (True, 10000, "Excellent"),
    ("Titanium", SterilizationMethod.ETO): (True, 10000, "Excellent"),
    ("Titanium", SterilizationMethod.GAMMA): (True, 10000, "Excellent"),
    ("Titanium", SterilizationMethod.H2O2_PLASMA): (True, 10000, "Excellent"),

    # UHMWPE
    ("UHMWPE", SterilizationMethod.STEAM_121): (False, 0, "Deforms at elevated temp"),
    ("UHMWPE", SterilizationMethod.STEAM_134): (False, 0, "Will melt/deform"),
    ("UHMWPE", SterilizationMethod.ETO): (True, 100, "Preferred method"),
    ("UHMWPE", SterilizationMethod.GAMMA): (True, 1, "Single use - oxidation in air"),
    ("UHMWPE", SterilizationMethod.H2O2_PLASMA): (True, 50, "Compatible"),

    # Nylon
    ("Nylon", SterilizationMethod.STEAM_121): (True, 50, "May absorb moisture"),
    ("Nylon", SterilizationMethod.STEAM_134): (True, 20, "Limited cycles"),
    ("Nylon", SterilizationMethod.ETO): (True, 100, "Compatible"),
    ("Nylon", SterilizationMethod.GAMMA): (True, 10, "May discolor"),
    ("Nylon", SterilizationMethod.H2O2_PLASMA): (False, 0, "Absorbs H2O2"),
}


def check_compatibility(
    material: str,
    method: SterilizationMethod
) -> Dict:
    """
    Check sterilization compatibility for a material.

    Args:
        material: Material name
        method: Sterilization method

    Returns:
        Dict with compatibility information
    """
    # Normalize material name for lookup
    material_key = material.upper().replace(" ", "").replace("-", "")

    # Try to find in compatibility matrix
    for (mat, meth), (compat, cycles, notes) in MATERIAL_COMPATIBILITY.items():
        if mat.upper().replace(" ", "") in material_key or material_key in mat.upper():
            if meth == method:
                return {
                    "material": material,
                    "method": method.value,
                    "compatible": compat,
                    "max_cycles": cycles if compat else 0,
                    "notes": notes,
                    "method_info": STERILIZATION_METHODS.get(method)
                }

    # Not found in matrix
    return {
        "material": material,
        "method": method.value,
        "compatible": None,  # Unknown
        "max_cycles": None,
        "notes": "Material not in compatibility database - testing required",
        "method_info": STERILIZATION_METHODS.get(method)
    }


def find_compatible_methods(material: str) -> List[Dict]:
    """
    Find all compatible sterilization methods for a material.

    Args:
        material: Material name

    Returns:
        List of compatible methods with details
    """
    compatible_methods = []
    material_key = material.upper().replace(" ", "").replace("-", "")

    for (mat, meth), (compat, cycles, notes) in MATERIAL_COMPATIBILITY.items():
        if mat.upper().replace(" ", "") in material_key or material_key in mat.upper():
            if compat:
                method_info = STERILIZATION_METHODS.get(meth)
                compatible_methods.append({
                    "method": meth.value,
                    "max_cycles": cycles,
                    "notes": notes,
                    "temperature_c": method_info.temperature_c if method_info else None,
                    "cycle_time_min": method_info.typical_cycle_time_min if method_info else None
                })

    return compatible_methods


def recommend_sterilization(
    materials: List[str],
    reusable: bool = True,
    has_electronics: bool = False
) -> Dict:
    """
    Recommend sterilization method for a device with multiple materials.

    Args:
        materials: List of materials in the device
        reusable: Whether device needs multiple sterilization cycles
        has_electronics: Whether device contains electronics

    Returns:
        Dict with recommended sterilization method
    """
    # Find methods compatible with ALL materials
    all_compatible = None

    for material in materials:
        compatible = set()
        for method in SterilizationMethod:
            result = check_compatibility(material, method)
            if result.get("compatible"):
                if not reusable or result.get("max_cycles", 0) > 100:
                    compatible.add(method)

        if all_compatible is None:
            all_compatible = compatible
        else:
            all_compatible = all_compatible.intersection(compatible)

    if not all_compatible:
        return {
            "recommended": None,
            "reason": "No sterilization method compatible with all materials",
            "suggestion": "Consider material substitution or component separation",
            "materials_reviewed": materials
        }

    # Prioritize methods
    priority_order = [
        SterilizationMethod.STEAM_134,  # Fast, no residues
        SterilizationMethod.STEAM_121,  # Standard
        SterilizationMethod.H2O2_PLASMA,  # Low temp, no residues
        SterilizationMethod.ETO,  # Wide compatibility
        SterilizationMethod.GAMMA,  # Single-use
    ]

    # If electronics, avoid steam
    if has_electronics:
        priority_order = [
            SterilizationMethod.H2O2_PLASMA,
            SterilizationMethod.ETO,
            SterilizationMethod.GAMMA,
        ]

    for method in priority_order:
        if method in all_compatible:
            method_info = STERILIZATION_METHODS.get(method)
            return {
                "recommended": method.value,
                "reason": f"Compatible with all materials, {method_info.advantages[0] if method_info else 'suitable'}",
                "all_compatible_methods": [m.value for m in all_compatible],
                "method_info": {
                    "temperature_c": method_info.temperature_c if method_info else None,
                    "cycle_time_min": method_info.typical_cycle_time_min if method_info else None,
                    "validation_standard": method_info.validation_standard if method_info else None
                },
                "materials_reviewed": materials
            }

    # Fallback
    method = list(all_compatible)[0]
    return {
        "recommended": method.value,
        "reason": "Compatible with all materials",
        "all_compatible_methods": [m.value for m in all_compatible],
        "materials_reviewed": materials
    }
