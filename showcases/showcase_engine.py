"""
Showcase Engine for Universal Parts Consciousness

This module processes real-world engineering showcase examples and integrates
them into the UPC system, demonstrating practical parts compatibility applications.

Key showcases:
- Tesla/Lotus: Cross-platform vehicle parts sharing
- LS Engine Swaps: Community-driven compatibility knowledge
- Aviation Fasteners: Safety-critical substitution rules
- Agricultural Equipment: Right-to-repair crosswalks
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime


class CompatibilityType(Enum):
    """Types of part compatibility relationships"""
    DIRECT_REPLACEMENT = "direct_replacement"        # Drop-in, no mods
    FUNCTIONAL_EQUIVALENT = "functional_equivalent"  # Same function, minor differences
    UPGRADE = "upgrade"                              # Better performance
    DOWNGRADE = "downgrade"                          # Reduced capability
    REQUIRES_ADAPTER = "requires_adapter"            # Needs adapter kit
    REQUIRES_MODIFICATION = "requires_modification"  # Custom work needed
    EMERGENCY_SUBSTITUTE = "emergency_substitute"    # Get-home-itis only


class VerificationLevel(Enum):
    """Levels of verification for compatibility data"""
    UNVERIFIED = 0           # Just claimed, not tested
    COMMUNITY_TESTED = 1     # Multiple community reports
    EXPERT_VERIFIED = 2      # Professional mechanic/engineer confirmed
    MANUFACTURER_CONFIRMED = 3  # OEM documentation
    STANDARD_COMPLIANT = 4   # ISO/SAE/MIL standard


@dataclass
class FastenerSpec:
    """Detailed fastener specification"""
    designation: str                    # e.g., "M8x1.25-10.9"
    standard: str                       # ISO, DIN, AN, MS, etc.
    thread_diameter_mm: float
    pitch_mm: float
    property_class: str                 # 8.8, 10.9, 12.9, Grade 5, etc.
    head_type: str                      # Hex, Socket, Button, etc.
    length_mm: float
    material: str = "steel"
    finish: str = "zinc"
    torque_nm: Optional[float] = None

    @classmethod
    def from_string(cls, spec_string: str) -> "FastenerSpec":
        """Parse fastener specification from string like 'M8x1.25-10.9 x 30mm'"""
        # This would parse specs like "M8x1.25-10.9" or "5/16-18 Grade 8"
        # Simplified implementation
        parts = spec_string.split()
        thread_spec = parts[0]

        if thread_spec.startswith("M"):
            # Metric
            standard = "ISO"
            diameter_pitch = thread_spec[1:].split("x")
            diameter = float(diameter_pitch[0])
            pitch = float(diameter_pitch[1].split("-")[0]) if len(diameter_pitch) > 1 else 1.0
            prop_class = diameter_pitch[1].split("-")[1] if "-" in diameter_pitch[1] else "8.8"
        else:
            # Imperial (UNC/UNF)
            standard = "ANSI"
            diameter = 0  # Would need lookup table
            pitch = 0
            prop_class = "Grade 5"

        return cls(
            designation=spec_string,
            standard=standard,
            thread_diameter_mm=diameter,
            pitch_mm=pitch,
            property_class=prop_class,
            head_type="hex",
            length_mm=30
        )


@dataclass
class PartQualia:
    """Experiential knowledge about a part from community use"""
    source: str                    # Forum, shop, manufacturer
    date: datetime
    user: str
    content: str
    sentiment: str                 # positive, neutral, negative, warning
    verified: bool = False
    upvotes: int = 0
    application_context: str = ""  # What vehicle/machine

    def reliability_weight(self) -> float:
        """Calculate how much to weight this qualia in decisions"""
        base = 1.0
        if self.verified:
            base *= 2.0
        base *= 1 + (self.upvotes / 100)  # Upvotes add credibility
        if self.sentiment == "warning":
            base *= 1.5  # Warnings are important
        return base


@dataclass
class CrossReference:
    """A compatibility relationship between parts"""
    source_part_number: str
    source_manufacturer: str
    target_part_number: str
    target_manufacturer: str
    compatibility_score: float         # 0-1, 1 = perfect drop-in
    compatibility_type: CompatibilityType
    verification_level: VerificationLevel
    modifications_required: List[str] = field(default_factory=list)
    adapter_parts: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    qualia: List[PartQualia] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate from tracked installs"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total

    @property
    def confidence_score(self) -> float:
        """Overall confidence in this cross-reference"""
        # Start with verification level
        base = (self.verification_level.value + 1) * 0.2

        # Add success rate weight
        if self.success_count + self.failure_count > 10:
            base += self.success_rate * 0.3

        # Add qualia weight
        if self.qualia:
            qualia_score = sum(q.reliability_weight() for q in self.qualia) / len(self.qualia)
            base += min(qualia_score * 0.1, 0.2)

        return min(base, 1.0)


@dataclass
class ShowcaseProject:
    """A real-world engineering project demonstrating UPC value"""
    showcase_id: str
    title: str
    description: str
    platforms: Dict[str, Dict]        # Source and target platforms
    cross_references: List[CrossReference]
    fastener_requirements: List[Dict]
    lessons_learned: List[str]
    economic_analysis: Optional[Dict] = None

    def get_compatibility_summary(self) -> Dict:
        """Generate a summary of compatibility across the project"""
        total_parts = len(self.cross_references)
        direct_fit = sum(1 for x in self.cross_references
                        if x.compatibility_type == CompatibilityType.DIRECT_REPLACEMENT)
        needs_mods = sum(1 for x in self.cross_references
                        if x.modifications_required)

        return {
            "total_parts_analyzed": total_parts,
            "direct_fit_count": direct_fit,
            "direct_fit_percent": direct_fit / total_parts * 100 if total_parts > 0 else 0,
            "needs_modification_count": needs_mods,
            "average_compatibility_score": sum(x.compatibility_score for x in self.cross_references) / total_parts if total_parts > 0 else 0
        }


class ShowcaseEngine:
    """
    Engine for loading, processing, and querying showcase data.

    This demonstrates how UPC would handle real-world parts compatibility
    knowledge extracted from engineering projects.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.showcases: Dict[str, ShowcaseProject] = {}
        self.cross_references: Dict[str, List[CrossReference]] = {}
        self.fastener_specs: Dict[str, FastenerSpec] = {}

    def load_showcase(self, filename: str) -> ShowcaseProject:
        """Load a showcase from JSON file"""
        filepath = self.data_dir / filename
        with open(filepath) as f:
            data = json.load(f)

        # Parse into structured objects
        showcase_id = data.get("showcase_id", filename.replace(".json", ""))

        # Extract cross-references from component groups
        cross_refs = []
        for group in data.get("component_groups", []):
            for component in group.get("components", []):
                if component.get("interchangeable"):
                    donor_pn = component.get("lotus_pn") or component.get("source_pn", "")
                    recipient_pn = component.get("tesla_pn") or component.get("target_pn", "")

                    compat_type = CompatibilityType.DIRECT_REPLACEMENT
                    if component.get("modifications_required"):
                        compat_type = CompatibilityType.REQUIRES_MODIFICATION
                    elif component.get("interchangeable") == "partial":
                        compat_type = CompatibilityType.FUNCTIONAL_EQUIVALENT

                    cross_ref = CrossReference(
                        source_part_number=donor_pn,
                        source_manufacturer=data.get("platforms", {}).get("donor", {}).get("manufacturer", ""),
                        target_part_number=recipient_pn,
                        target_manufacturer=data.get("platforms", {}).get("recipient", {}).get("manufacturer", ""),
                        compatibility_score=group.get("compatibility_score", 0.8),
                        compatibility_type=compat_type,
                        verification_level=VerificationLevel.EXPERT_VERIFIED,
                        modifications_required=component.get("modifications_required", [])
                    )
                    cross_refs.append(cross_ref)

        # Parse qualia
        for qualia_entry in data.get("community_qualia", []):
            # Find matching cross-reference and add qualia
            qualia = PartQualia(
                source=qualia_entry.get("source", ""),
                date=datetime.fromisoformat(qualia_entry.get("date", "2024-01-01")),
                user=qualia_entry.get("user", "anonymous"),
                content=qualia_entry.get("content", ""),
                sentiment="positive" if qualia_entry.get("verified") else "neutral",
                verified=qualia_entry.get("verified", False),
                upvotes=qualia_entry.get("upvotes", 0)
            )
            # Add to first relevant cross-ref for now
            if cross_refs:
                cross_refs[0].qualia.append(qualia)

        showcase = ShowcaseProject(
            showcase_id=showcase_id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            platforms=data.get("platforms", {}),
            cross_references=cross_refs,
            fastener_requirements=self._extract_fasteners(data),
            lessons_learned=data.get("lessons_for_upc", []),
            economic_analysis=data.get("economic_analysis")
        )

        self.showcases[showcase_id] = showcase
        return showcase

    def _extract_fasteners(self, data: Dict) -> List[Dict]:
        """Extract all fastener specifications from showcase data"""
        fasteners = []

        for group in data.get("component_groups", []):
            for component in group.get("components", []):
                for fastener in component.get("fasteners", []):
                    fasteners.append({
                        "component": component.get("part_name", ""),
                        "location": fastener.get("location", ""),
                        "spec": fastener.get("spec", ""),
                        "length_mm": fastener.get("length_mm", 0),
                        "qty": fastener.get("qty", 1),
                        "torque_nm": fastener.get("torque_nm")
                    })

        return fasteners

    def load_all_showcases(self) -> Dict[str, ShowcaseProject]:
        """Load all showcase files from data directory"""
        for filepath in self.data_dir.glob("*.json"):
            if filepath.name != "README.md":
                try:
                    self.load_showcase(filepath.name)
                except Exception as e:
                    print(f"Warning: Could not load {filepath.name}: {e}")

        return self.showcases

    def find_cross_references(
        self,
        part_number: str,
        manufacturer: Optional[str] = None
    ) -> List[CrossReference]:
        """
        Find all cross-references for a given part number.

        This is the core UPC query: "What can I use instead of this part?"
        """
        matches = []

        for showcase in self.showcases.values():
            for xref in showcase.cross_references:
                if part_number.upper() in xref.source_part_number.upper():
                    if manufacturer is None or manufacturer.upper() in xref.source_manufacturer.upper():
                        matches.append(xref)
                elif part_number.upper() in xref.target_part_number.upper():
                    # Also search target parts (bidirectional)
                    if manufacturer is None or manufacturer.upper() in xref.target_manufacturer.upper():
                        # Create reverse cross-reference
                        reverse = CrossReference(
                            source_part_number=xref.target_part_number,
                            source_manufacturer=xref.target_manufacturer,
                            target_part_number=xref.source_part_number,
                            target_manufacturer=xref.source_manufacturer,
                            compatibility_score=xref.compatibility_score,
                            compatibility_type=xref.compatibility_type,
                            verification_level=xref.verification_level,
                            modifications_required=xref.modifications_required
                        )
                        matches.append(reverse)

        # Sort by compatibility score
        matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        return matches

    def get_fastener_requirements(
        self,
        platform: str
    ) -> List[Dict]:
        """Get all fastener requirements for a platform/project"""
        fasteners = []

        for showcase in self.showcases.values():
            if platform.lower() in showcase.title.lower():
                fasteners.extend(showcase.fastener_requirements)

        return fasteners

    def query_compatibility(
        self,
        source_platform: str,
        target_platform: str
    ) -> Dict:
        """
        Query overall compatibility between two platforms.

        Example: "How compatible is a Tesla Roadster with a Lotus Elise?"
        """
        for showcase in self.showcases.values():
            platforms = showcase.platforms
            donor = platforms.get("donor", {})
            recipient = platforms.get("recipient", {})

            if (source_platform.lower() in donor.get("model", "").lower() or
                source_platform.lower() in donor.get("manufacturer", "").lower()):
                if (target_platform.lower() in recipient.get("model", "").lower() or
                    target_platform.lower() in recipient.get("manufacturer", "").lower()):

                    return {
                        "showcase": showcase.title,
                        "summary": showcase.get_compatibility_summary(),
                        "cross_references": len(showcase.cross_references),
                        "fastener_requirements": len(showcase.fastener_requirements),
                        "lessons": showcase.lessons_learned
                    }

        return {"error": f"No compatibility data found for {source_platform} ↔ {target_platform}"}

    def generate_bom_crosswalk(
        self,
        source_parts: List[str],
        source_manufacturer: str
    ) -> List[Dict]:
        """
        Generate a bill of materials crosswalk.

        Given a list of source parts, find all compatible alternatives
        with pricing and availability information.
        """
        crosswalk = []

        for part_number in source_parts:
            alternatives = self.find_cross_references(part_number, source_manufacturer)

            crosswalk.append({
                "source_part": part_number,
                "alternatives": [
                    {
                        "part_number": alt.target_part_number,
                        "manufacturer": alt.target_manufacturer,
                        "compatibility_score": alt.compatibility_score,
                        "compatibility_type": alt.compatibility_type.value,
                        "confidence": alt.confidence_score,
                        "modifications_needed": alt.modifications_required,
                        "warnings": alt.warnings
                    }
                    for alt in alternatives
                ]
            })

        return crosswalk


class SwapGuide:
    """
    Generate comprehensive swap guides from showcase data.

    This demonstrates UPC's ability to create actionable documentation
    from community knowledge and verified compatibility data.
    """

    def __init__(self, engine: ShowcaseEngine):
        self.engine = engine

    def generate_swap_guide(
        self,
        source_platform: str,
        target_platform: str
    ) -> str:
        """Generate a markdown swap guide"""
        compatibility = self.engine.query_compatibility(source_platform, target_platform)

        if "error" in compatibility:
            return f"# No Guide Available\n\n{compatibility['error']}"

        guide = f"""# {source_platform} → {target_platform} Swap Guide

## Overview

{compatibility.get('showcase', 'Cross-platform compatibility guide')}

## Compatibility Summary

| Metric | Value |
|--------|-------|
| Total Parts Analyzed | {compatibility['summary']['total_parts_analyzed']} |
| Direct Fit Parts | {compatibility['summary']['direct_fit_count']} ({compatibility['summary']['direct_fit_percent']:.0f}%) |
| Needs Modification | {compatibility['summary']['needs_modification_count']} |
| Average Compatibility | {compatibility['summary']['average_compatibility_score']:.2f} |

## Key Lessons

"""

        for lesson in compatibility.get('lessons', []):
            guide += f"- {lesson}\n"

        return guide


# Example usage and demonstration
def demo():
    """Demonstrate the showcase engine capabilities"""

    print("=" * 60)
    print("Universal Parts Consciousness - Showcase Engine Demo")
    print("=" * 60)

    # Initialize engine
    engine = ShowcaseEngine()

    # Load showcases
    print("\nLoading showcase data...")
    showcases = engine.load_all_showcases()
    print(f"Loaded {len(showcases)} showcases")

    # Demo: Tesla/Lotus compatibility query
    print("\n" + "-" * 40)
    print("Query: Tesla Roadster ↔ Lotus Elise Compatibility")
    print("-" * 40)

    compatibility = engine.query_compatibility("Elise", "Roadster")
    if "error" not in compatibility:
        print(f"Showcase: {compatibility['showcase']}")
        print(f"Cross-references found: {compatibility['cross_references']}")
        print(f"Direct fit parts: {compatibility['summary']['direct_fit_percent']:.0f}%")
        print("\nKey lessons:")
        for lesson in compatibility.get('lessons', [])[:3]:
            print(f"  • {lesson}")

    # Demo: Part cross-reference lookup
    print("\n" + "-" * 40)
    print("Query: Find alternatives for Lotus part A117C0035F")
    print("-" * 40)

    alternatives = engine.find_cross_references("A117C0035F")
    for alt in alternatives[:3]:
        print(f"  → {alt.target_part_number} ({alt.target_manufacturer})")
        print(f"    Compatibility: {alt.compatibility_score:.0%}")
        print(f"    Type: {alt.compatibility_type.value}")

    # Demo: BOM crosswalk
    print("\n" + "-" * 40)
    print("Query: BOM Crosswalk for Lotus suspension parts")
    print("-" * 40)

    parts = ["A117C0035F", "A117C0034F", "A117D0049F"]
    crosswalk = engine.generate_bom_crosswalk(parts, "Lotus")
    for item in crosswalk:
        print(f"\n{item['source_part']}:")
        for alt in item['alternatives'][:2]:
            print(f"  → {alt['part_number']} (score: {alt['compatibility_score']:.0%})")

    # Generate swap guide
    print("\n" + "-" * 40)
    print("Generated Swap Guide Preview")
    print("-" * 40)

    guide_generator = SwapGuide(engine)
    guide = guide_generator.generate_swap_guide("Lotus", "Tesla")
    print(guide[:500] + "...")

    print("\n" + "=" * 60)
    print("Demo complete. This is how UPC transforms tribal knowledge")
    print("into queryable, verified parts compatibility data.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
