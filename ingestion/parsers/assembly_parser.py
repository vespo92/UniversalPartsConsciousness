"""
Assembly & Engine BOM Parser
==============================
"An engine is not a list of parts. It is a hierarchy of systems,
each system a constellation of components, each component a universe
of specifications. The assembly parser respects this truth."

Handles deeply nested automotive/mechanical assembly data:
  - Engine master specs (variants, base specs, heritage)
  - Parts catalogs (system → component hierarchies)
  - Interchangeability matrices (cross-reference networks)
  - Aftermarket ecosystems (OEM + aftermarket mappings)
  - Tools & service requirements

This is what the flat CSV importer cannot do.

Data model output:
  - BOM assembly with recursive item tree
  - Individual parts with full specs
  - Part relationships (interchanges, compatibility, replaces)
  - Vehicle application mappings
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("UPC.Ingestion.Assembly")


@dataclass
class AssemblyPart:
    """A part extracted from an assembly structure."""
    part_id: str
    name: str
    description: str = ""
    system: str = ""                       # e.g., "short_block", "cylinder_head"
    assembly_path: str = ""                # e.g., "Ford FE V8 > Short Block > Crankshaft"

    oem_part_numbers: List[str] = field(default_factory=list)
    casting_numbers: List[str] = field(default_factory=list)
    manufacturer: str = ""
    material: str = ""

    # Quantity in parent assembly
    quantity: int = 1

    # All specifications from source (preserved as-is)
    specifications: Dict[str, Any] = field(default_factory=dict)

    # Relationships discovered during parsing
    interchanges_with: List[str] = field(default_factory=list)
    compatible_with: List[str] = field(default_factory=list)
    replaces: List[str] = field(default_factory=list)

    # Vehicle applications
    applications: List[str] = field(default_factory=list)

    notes: str = ""
    source_file: str = ""

    def to_dict(self) -> Dict[str, Any]:
        identity = f"{self.part_id}|{self.name}|{self.manufacturer}"
        upc_id = f"UPC-{hashlib.sha256(identity.encode()).hexdigest()[:12].upper()}"
        return {
            "upc_id": upc_id,
            "part_id": self.part_id,
            "name": self.name,
            "description": self.description,
            "system": self.system,
            "assembly_path": self.assembly_path,
            "oem_part_numbers": self.oem_part_numbers,
            "casting_numbers": self.casting_numbers,
            "manufacturer": self.manufacturer,
            "material": self.material,
            "quantity": self.quantity,
            "specifications": self.specifications,
            "interchanges_with": self.interchanges_with,
            "compatible_with": self.compatible_with,
            "replaces": self.replaces,
            "applications": self.applications,
            "notes": self.notes,
            "source_file": self.source_file,
        }


@dataclass
class Relationship:
    """A relationship between two parts discovered during parsing."""
    part_a_id: str
    part_b_id: str
    relationship_type: str      # interchanges, compatible_with, replaces, variant_of,
                                # mates_with, requires, assembly_child
    confidence: float = 1.0
    bidirectional: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_a_id": self.part_a_id,
            "part_b_id": self.part_b_id,
            "relationship_type": self.relationship_type,
            "confidence": self.confidence,
            "bidirectional": self.bidirectional,
            "metadata": self.metadata,
            "source": self.source,
        }


@dataclass
class BOMItem:
    """An item in a Bill of Materials tree."""
    item_number: str                       # e.g., "1", "1.1", "1.1.3"
    level: int
    part_id: Optional[str] = None
    description: str = ""
    quantity: float = 1
    unit: str = "each"
    children: List["BOMItem"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_number": self.item_number,
            "level": self.level,
            "part_id": self.part_id,
            "description": self.description,
            "quantity": self.quantity,
            "unit": self.unit,
            "children": [c.to_dict() for c in self.children],
        }


@dataclass
class AssemblyIngestResult:
    """Complete result of parsing an assembly data set."""
    assembly_name: str
    assembly_id: str

    # Master spec data
    master_spec: Dict[str, Any] = field(default_factory=dict)
    variants: List[Dict[str, Any]] = field(default_factory=list)

    # Extracted parts
    parts: List[AssemblyPart] = field(default_factory=list)

    # BOM tree
    bom_tree: List[BOMItem] = field(default_factory=list)

    # Relationships (interchangeability, compatibility, etc.)
    relationships: List[Relationship] = field(default_factory=list)

    # Vehicle applications
    vehicle_applications: List[Dict[str, Any]] = field(default_factory=list)

    # Transmission compatibility
    transmission_compatibility: List[Dict[str, Any]] = field(default_factory=list)

    # Stats
    total_parts: int = 0
    total_relationships: int = 0
    total_systems: int = 0
    total_variants: int = 0
    files_parsed: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"Assembly: {self.assembly_name} ({self.assembly_id})",
            f"  Variants:      {self.total_variants}",
            f"  Systems:       {self.total_systems}",
            f"  Parts:         {self.total_parts}",
            f"  Relationships: {self.total_relationships}",
            f"  Vehicles:      {len(self.vehicle_applications)}",
            f"  Files parsed:  {len(self.files_parsed)}",
        ]
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assembly_name": self.assembly_name,
            "assembly_id": self.assembly_id,
            "master_spec": self.master_spec,
            "variants": self.variants,
            "parts": [p.to_dict() for p in self.parts],
            "bom_tree": [b.to_dict() for b in self.bom_tree],
            "relationships": [r.to_dict() for r in self.relationships],
            "vehicle_applications": self.vehicle_applications,
            "transmission_compatibility": self.transmission_compatibility,
            "stats": {
                "total_parts": self.total_parts,
                "total_relationships": self.total_relationships,
                "total_systems": self.total_systems,
                "total_variants": self.total_variants,
            },
        }


class AssemblyParser:
    """
    Parses deeply nested assembly data — engine specs, parts catalogs,
    interchangeability matrices — into structured UPC data.

    Usage:
        parser = AssemblyParser()

        # Parse a full engine directory (all JSON files)
        result = parser.parse_engine_directory(
            "Automotive/Engines/Manufacturers/Ford/Ford-FE-V8/"
        )

        # Parse individual files
        result = parser.parse_parts_catalog("parts-catalog.json")
        result = parser.parse_interchangeability("interchangeability-matrix.json")

        # Parse all engines
        results = parser.parse_all_engines("Automotive/Engines/Manufacturers/")
    """

    def parse_engine_directory(self, dir_path: str | Path) -> AssemblyIngestResult:
        """
        Parse all JSON files in an engine directory.

        Expects the standard UPC engine directory layout:
          - *-master.json          (engine specs)
          - parts-catalog.json     (component BOM)
          - interchangeability-matrix.json  (cross-references)
          - aftermarket-ecosystem.json      (aftermarket parts)
          - tools-and-service.json          (service data)
        """
        path = Path(dir_path)
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        # Detect engine name from directory
        engine_name = path.name.replace("-", " ").replace("_", " ")

        result = AssemblyIngestResult(
            assembly_name=engine_name,
            assembly_id=path.name,
        )

        # Parse each file type
        for json_file in sorted(path.glob("*.json")):
            try:
                with open(json_file) as f:
                    data = json.load(f)

                filename = json_file.name.lower()
                result.files_parsed.append(str(json_file))

                if "master" in filename:
                    self._parse_master(data, result, str(json_file))
                elif "parts-catalog" in filename or "parts_catalog" in filename:
                    self._parse_parts_catalog(data, result, str(json_file))
                elif "interchangeability" in filename:
                    self._parse_interchangeability(data, result, str(json_file))
                elif "aftermarket" in filename:
                    self._parse_aftermarket(data, result, str(json_file))
                elif "tools" in filename or "service" in filename:
                    self._parse_tools_service(data, result, str(json_file))

                logger.info(f"Parsed: {json_file.name}")

            except Exception as e:
                logger.error(f"Failed to parse {json_file.name}: {e}")

        # Update stats
        result.total_parts = len(result.parts)
        result.total_relationships = len(result.relationships)

        return result

    def parse_all_engines(self, manufacturers_dir: str | Path) -> List[AssemblyIngestResult]:
        """Parse all engine directories under a manufacturers root."""
        path = Path(manufacturers_dir)
        results = []

        # Walk manufacturer/engine-family directories
        for mfr_dir in sorted(path.iterdir()):
            if not mfr_dir.is_dir():
                continue
            for engine_dir in sorted(mfr_dir.iterdir()):
                if not engine_dir.is_dir():
                    continue
                # Skip non-engine directories
                if engine_dir.name.startswith("Shared"):
                    continue

                json_files = list(engine_dir.glob("*.json"))
                if json_files:
                    try:
                        result = self.parse_engine_directory(engine_dir)
                        results.append(result)
                        logger.info(
                            f"Parsed engine: {result.assembly_name} "
                            f"({result.total_parts} parts, "
                            f"{result.total_relationships} relationships)"
                        )
                    except Exception as e:
                        logger.error(f"Failed to parse {engine_dir}: {e}")

        return results

    # -------------------------------------------------------------------
    # Master Spec Parser
    # -------------------------------------------------------------------

    def _parse_master(
        self,
        data: Dict[str, Any],
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse engine master specification file."""
        result.assembly_id = data.get("engine_id", result.assembly_id)
        result.assembly_name = data.get("engine_family", result.assembly_name)
        result.master_spec = {
            "engine_id": data.get("engine_id"),
            "manufacturer": data.get("manufacturer"),
            "engine_family": data.get("engine_family"),
            "common_names": data.get("common_names", []),
            "production_years": data.get("production_years"),
            "description": data.get("description"),
            "heritage": data.get("heritage", {}),
            "base_specifications": data.get("base_specifications", {}),
        }

        # Parse variants
        for variant in data.get("variants", []):
            result.variants.append(variant)
            result.total_variants += 1

            # Create variant-to-variant relationships within a family
            variant_id = variant.get("variant_id", "")
            for other_variant in data.get("variants", []):
                other_id = other_variant.get("variant_id", "")
                if variant_id and other_id and variant_id != other_id:
                    result.relationships.append(Relationship(
                        part_a_id=variant_id,
                        part_b_id=other_id,
                        relationship_type="variant_of",
                        confidence=1.0,
                        bidirectional=True,
                        metadata={
                            "family": data.get("engine_family"),
                            "a_displacement": variant.get("displacement_ci"),
                            "b_displacement": other_variant.get("displacement_ci"),
                        },
                        source=source_file,
                    ))

        # Parse vehicle applications
        for app in data.get("vehicle_applications", []):
            result.vehicle_applications.append(app)

    # -------------------------------------------------------------------
    # Parts Catalog Parser — the core BOM extraction
    # -------------------------------------------------------------------

    def _parse_parts_catalog(
        self,
        data: Dict[str, Any],
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """
        Parse a parts catalog into individual parts + BOM tree.

        Handles the nested structure:
          catalog → systems → components → specifications
        """
        engine_family = data.get("engine_family", result.assembly_name)
        catalog_id = data.get("catalog_id", result.assembly_id)

        systems = data.get("systems", {})
        system_index = 0

        for system_name, system_data in systems.items():
            system_index += 1
            result.total_systems += 1

            system_desc = system_data.get("description", system_name.replace("_", " ").title())

            # Create BOM node for this system
            system_bom = BOMItem(
                item_number=str(system_index),
                level=0,
                description=system_desc,
            )

            # Parse components within this system
            components = system_data.get("components", [])
            for comp_index, component in enumerate(components, start=1):
                part = self._extract_component(
                    component,
                    system_name=system_name,
                    engine_family=engine_family,
                    source_file=source_file,
                )
                result.parts.append(part)

                # Add to BOM tree
                comp_bom = BOMItem(
                    item_number=f"{system_index}.{comp_index}",
                    level=1,
                    part_id=part.part_id,
                    description=part.name,
                    quantity=part.quantity,
                )
                system_bom.children.append(comp_bom)

                # Create assembly relationship: system contains component
                result.relationships.append(Relationship(
                    part_a_id=f"{catalog_id}:{system_name}",
                    part_b_id=part.part_id,
                    relationship_type="assembly_child",
                    confidence=1.0,
                    bidirectional=False,
                    metadata={"system": system_name, "quantity": part.quantity},
                    source=source_file,
                ))

            result.bom_tree.append(system_bom)

    def _extract_component(
        self,
        component: Dict[str, Any],
        system_name: str,
        engine_family: str,
        source_file: str,
    ) -> AssemblyPart:
        """Extract a single component from the parts catalog structure."""
        # Pull specifications out of nested object
        specs = component.get("specifications", {})

        # Detect material from specs or top-level
        material = (
            specs.get("material", "") or
            component.get("material", "") or
            specs.get("composition", "")
        )

        part = AssemblyPart(
            part_id=component.get("part_id", ""),
            name=component.get("name", ""),
            description=component.get("description", ""),
            system=system_name,
            assembly_path=f"{engine_family} > {system_name.replace('_', ' ').title()} > {component.get('name', '')}",
            oem_part_numbers=component.get("oem_part_numbers", []),
            casting_numbers=component.get("casting_numbers", []),
            manufacturer=component.get("manufacturer", "Ford Motor Company"),
            material=material,
            quantity=component.get("quantity", 1),
            specifications=specs,
            applications=component.get("applications", []),
            notes=component.get("notes", ""),
            source_file=source_file,
        )

        return part

    # -------------------------------------------------------------------
    # Interchangeability Matrix Parser
    # -------------------------------------------------------------------

    def _parse_interchangeability(
        self,
        data: Dict[str, Any],
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """
        Parse interchangeability matrix into part relationships.

        This converts the nested cross-reference data into flat
        relationship records that can be stored in part_relationships.
        """
        engine_family = data.get("engine_family", result.assembly_name)

        # 1. Parse vehicle platforms → application mappings
        for platform_id, platform_data in data.get("vehicle_platforms", {}).items():
            for model_info in platform_data.get("models", []):
                result.vehicle_applications.append({
                    "platform": platform_id,
                    "model": model_info.get("model"),
                    "years": model_info.get("years"),
                    "engines": model_info.get("engines", []),
                    "notes": platform_data.get("notes", ""),
                })

        # 2. Parse interchangeability groups → relationships
        groups = data.get("interchangeability_groups", {})
        self._parse_interchange_groups(groups, engine_family, result, source_file)

        # 3. Parse component interchangeability → direct part relationships
        comp_interchange = data.get("component_interchangeability", {})
        self._parse_component_interchange(comp_interchange, engine_family, result, source_file)

        # 4. Parse transmission compatibility
        trans_compat = data.get("transmission_compatibility", {})
        if trans_compat:
            result.transmission_compatibility.append({
                "engine_family": engine_family,
                "bellhousing_pattern": trans_compat.get("bellhousing_pattern"),
                "compatible_transmissions": trans_compat.get("compatible_transmissions", []),
                "adapter_availability": trans_compat.get("adapter_availability", {}),
            })

        # 5. Parse swap compatibility
        swap_compat = data.get("swap_compatibility", {})
        if swap_compat:
            for direction, swaps in swap_compat.items():
                if isinstance(swaps, dict):
                    for target, swap_info in swaps.items():
                        if isinstance(swap_info, dict):
                            result.relationships.append(Relationship(
                                part_a_id=engine_family,
                                part_b_id=target,
                                relationship_type="swap_compatible",
                                confidence=0.8,
                                bidirectional=False,
                                metadata={
                                    "direction": direction,
                                    "difficulty": swap_info.get("difficulty"),
                                    "requirements": swap_info.get("requirements", []),
                                    "common_swaps": swap_info.get("common_swaps", []),
                                    "notes": swap_info.get("notes", ""),
                                },
                                source=source_file,
                            ))

        # 6. Parse OEM cross-reference
        xref = data.get("oem_part_number_cross_reference", {})
        if xref:
            for category, castings in xref.get("common_casting_numbers", {}).items():
                if isinstance(castings, dict):
                    for casting_num, casting_desc in castings.items():
                        result.relationships.append(Relationship(
                            part_a_id=casting_num,
                            part_b_id=casting_desc,
                            relationship_type="casting_number_identifies",
                            confidence=1.0,
                            bidirectional=False,
                            metadata={
                                "category": category,
                                "engine_family": engine_family,
                            },
                            source=source_file,
                        ))

    def _parse_interchange_groups(
        self,
        groups: Dict[str, Any],
        engine_family: str,
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse interchangeability groups (bore families, stroke families, etc.)."""
        for group_type, group_data in groups.items():
            if not isinstance(group_data, dict):
                continue

            for group_name, group_info in group_data.items():
                if not isinstance(group_info, dict):
                    continue

                engines = group_info.get("engines", [])

                # Every engine in the same group is interchangeable
                # for this specific attribute
                for i, engine_a in enumerate(engines):
                    for engine_b in engines[i + 1:]:
                        result.relationships.append(Relationship(
                            part_a_id=f"{engine_family}:{engine_a}",
                            part_b_id=f"{engine_family}:{engine_b}",
                            relationship_type="interchanges_within_group",
                            confidence=0.9,
                            bidirectional=True,
                            metadata={
                                "group_type": group_type,
                                "group_name": group_name,
                                "notes": group_info.get("notes", ""),
                                **{k: v for k, v in group_info.items()
                                   if k not in ("engines", "notes")},
                            },
                            source=source_file,
                        ))

    def _parse_component_interchange(
        self,
        comp_data: Dict[str, Any],
        engine_family: str,
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse component-level interchangeability (heads, cranks, rods, etc.)."""
        for component_type, interchange_info in comp_data.items():
            if not isinstance(interchange_info, dict):
                continue

            # Handle "interchangeable_within" — marks all engines as sharing this component
            within = interchange_info.get("interchangeable_within")
            if isinstance(within, list):
                for note in within:
                    result.relationships.append(Relationship(
                        part_a_id=f"{engine_family}:{component_type}",
                        part_b_id="all_variants",
                        relationship_type="universally_interchangeable",
                        confidence=0.95,
                        metadata={
                            "component": component_type,
                            "note": note,
                        },
                        source=source_file,
                    ))
            elif isinstance(within, dict):
                # Grouped interchangeability (e.g., crankshafts by stroke family)
                for group_name, group_engines in within.items():
                    if isinstance(group_engines, list):
                        engines = group_engines
                    elif isinstance(group_engines, str):
                        engines = [e.strip() for e in group_engines.split(",")]
                    else:
                        continue

                    for i, eng_a in enumerate(engines):
                        for eng_b in engines[i + 1:]:
                            result.relationships.append(Relationship(
                                part_a_id=f"{engine_family}:{component_type}:{eng_a}",
                                part_b_id=f"{engine_family}:{component_type}:{eng_b}",
                                relationship_type="component_interchangeable",
                                confidence=0.9,
                                bidirectional=True,
                                metadata={
                                    "component": component_type,
                                    "group": group_name,
                                },
                                source=source_file,
                            ))

            # Handle typed variants (e.g., cylinder head types: low_riser, medium_riser)
            for sub_key, sub_data in interchange_info.items():
                if sub_key in ("interchangeable_within", "notes", "upgrades",
                               "cautions", "exceptions"):
                    continue
                if isinstance(sub_data, dict):
                    self._parse_typed_variants(
                        component_type, sub_key, sub_data,
                        engine_family, result, source_file,
                    )

            # Handle upgrades as relationships
            upgrades = interchange_info.get("upgrades")
            if isinstance(upgrades, dict):
                for upgrade_name, upgrade_desc in upgrades.items():
                    result.relationships.append(Relationship(
                        part_a_id=f"{engine_family}:{component_type}:stock",
                        part_b_id=f"{engine_family}:{component_type}:{upgrade_name}",
                        relationship_type="upgrade_path",
                        confidence=0.85,
                        bidirectional=False,
                        metadata={
                            "component": component_type,
                            "upgrade": upgrade_name,
                            "description": upgrade_desc if isinstance(upgrade_desc, str) else str(upgrade_desc),
                        },
                        source=source_file,
                    ))

    def _parse_typed_variants(
        self,
        component_type: str,
        variant_group: str,
        variant_data: Dict[str, Any],
        engine_family: str,
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse typed component variants (e.g., head_types with sub-entries)."""
        if not isinstance(variant_data, dict):
            return

        # Each entry under the group is a variant
        variant_ids = []
        for variant_name, variant_info in variant_data.items():
            if not isinstance(variant_info, dict):
                continue

            variant_id = f"{engine_family}:{component_type}:{variant_name}"
            variant_ids.append(variant_id)

            # Create a part entry for this variant
            casting_nums = variant_info.get("casting_numbers", [])
            applications = variant_info.get("applications", [])

            part = AssemblyPart(
                part_id=variant_id,
                name=f"{engine_family} {component_type.replace('_', ' ').title()} - {variant_name.replace('_', ' ').title()}",
                description=variant_info.get("notes", ""),
                system=component_type,
                assembly_path=f"{engine_family} > {component_type} > {variant_name}",
                casting_numbers=casting_nums if isinstance(casting_nums, list) else [],
                manufacturer="Ford Motor Company",
                specifications={
                    k: v for k, v in variant_info.items()
                    if k not in ("notes", "casting_numbers", "applications")
                },
                applications=applications if isinstance(applications, list) else [applications] if isinstance(applications, str) else [],
                notes=variant_info.get("notes", ""),
                source_file=source_file,
            )
            result.parts.append(part)

            # Create compatibility relationships from "compatible_intakes" etc.
            for key, value in variant_info.items():
                if key.startswith("compatible_") and isinstance(value, list):
                    for compat_item in value:
                        result.relationships.append(Relationship(
                            part_a_id=variant_id,
                            part_b_id=str(compat_item),
                            relationship_type="compatible_with",
                            confidence=0.9,
                            metadata={
                                "compatibility_type": key,
                                "component": component_type,
                            },
                            source=source_file,
                        ))

        # Create variant_of relationships between all entries in this group
        for i, va in enumerate(variant_ids):
            for vb in variant_ids[i + 1:]:
                result.relationships.append(Relationship(
                    part_a_id=va,
                    part_b_id=vb,
                    relationship_type="variant_of",
                    confidence=1.0,
                    bidirectional=True,
                    metadata={
                        "component": component_type,
                        "variant_group": variant_group,
                    },
                    source=source_file,
                ))

    # -------------------------------------------------------------------
    # Aftermarket Ecosystem Parser
    # -------------------------------------------------------------------

    def _parse_aftermarket(
        self,
        data: Dict[str, Any],
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse aftermarket ecosystem data (aftermarket parts and suppliers)."""
        engine_family = data.get("engine_family", result.assembly_name)

        # Aftermarket manufacturers
        for mfr_name, mfr_data in data.get("aftermarket_manufacturers", {}).items():
            if not isinstance(mfr_data, dict):
                continue

            for product_cat, products in mfr_data.get("products", {}).items():
                if isinstance(products, list):
                    for product in products:
                        if isinstance(product, dict):
                            part = AssemblyPart(
                                part_id=product.get("part_number", f"{mfr_name}:{product_cat}"),
                                name=product.get("name", product.get("description", "")),
                                description=product.get("description", ""),
                                system=product_cat,
                                manufacturer=mfr_name,
                                specifications=product.get("specifications", {}),
                                notes=product.get("notes", ""),
                                source_file=source_file,
                            )
                            result.parts.append(part)

                            # Link aftermarket to OEM
                            oem_replacement = product.get("replaces", product.get("oem_equivalent"))
                            if oem_replacement:
                                result.relationships.append(Relationship(
                                    part_a_id=part.part_id,
                                    part_b_id=str(oem_replacement),
                                    relationship_type="replaces",
                                    confidence=0.85,
                                    metadata={
                                        "aftermarket_manufacturer": mfr_name,
                                        "category": product_cat,
                                    },
                                    source=source_file,
                                ))

        # Performance tiers
        for tier_name, tier_data in data.get("performance_tiers", {}).items():
            if isinstance(tier_data, dict):
                for component, options in tier_data.items():
                    if isinstance(options, list):
                        for option in options:
                            if isinstance(option, str):
                                result.relationships.append(Relationship(
                                    part_a_id=f"{engine_family}:{component}:stock",
                                    part_b_id=f"{engine_family}:{component}:{option}",
                                    relationship_type="upgrade_path",
                                    confidence=0.7,
                                    metadata={
                                        "tier": tier_name,
                                        "component": component,
                                    },
                                    source=source_file,
                                ))

    # -------------------------------------------------------------------
    # Tools & Service Parser
    # -------------------------------------------------------------------

    def _parse_tools_service(
        self,
        data: Dict[str, Any],
        result: AssemblyIngestResult,
        source_file: str,
    ) -> None:
        """Parse tools and service requirements."""
        engine_family = data.get("engine_family", result.assembly_name)

        # Extract tool requirements as parts
        for tool_cat, tools in data.get("tools", data.get("required_tools", {})).items():
            if isinstance(tools, list):
                for tool in tools:
                    if isinstance(tool, dict):
                        part = AssemblyPart(
                            part_id=tool.get("tool_id", tool.get("name", "")),
                            name=tool.get("name", ""),
                            description=tool.get("description", ""),
                            system="tooling",
                            manufacturer=tool.get("manufacturer", ""),
                            specifications=tool.get("specifications", {}),
                            notes=tool.get("notes", ""),
                            source_file=source_file,
                        )
                        result.parts.append(part)

                        # Link tool to engine
                        result.relationships.append(Relationship(
                            part_a_id=engine_family,
                            part_b_id=part.part_id,
                            relationship_type="requires_tool",
                            confidence=1.0,
                            bidirectional=False,
                            metadata={"tool_category": tool_cat},
                            source=source_file,
                        ))

        # Extract torque specs as metadata on relationships
        for torque_cat, torque_specs in data.get("torque_specifications", {}).items():
            if isinstance(torque_specs, dict):
                for fastener, spec in torque_specs.items():
                    result.relationships.append(Relationship(
                        part_a_id=f"{engine_family}:{torque_cat}",
                        part_b_id=fastener,
                        relationship_type="torque_specification",
                        confidence=1.0,
                        bidirectional=False,
                        metadata={
                            "category": torque_cat,
                            "specification": spec if isinstance(spec, dict) else {"value": spec},
                        },
                        source=source_file,
                    ))
