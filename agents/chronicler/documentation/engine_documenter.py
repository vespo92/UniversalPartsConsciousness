"""
Engine Documenter - Core documentation engine for the Chronicler agent.

Responsible for creating, updating, and maintaining comprehensive
engine documentation following the standardized format.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .standard_templates import (
    REQUIRED_FILES,
    OPTIONAL_FILES,
    EngineDocumentationTemplate,
)

logger = logging.getLogger(__name__)


class EngineDocumenter:
    """
    Creates and maintains comprehensive engine documentation.

    Follows the 5-file standard:
    - {engine}-master.json: Specifications, history, overview
    - {engine}-parts-catalog.json: Complete parts list
    - {engine}-interchangeability.json: What fits what
    - {engine}-tools-procedures.json: Service procedures
    - {engine}-aftermarket.json: Aftermarket ecosystem
    """

    def __init__(self, engines_base_path: Path):
        """
        Initialize the engine documenter.

        Args:
            engines_base_path: Base path to Engines/Manufacturers/ directory
        """
        self.base_path = engines_base_path
        self.documentation_version = "1.0"

    def document(
        self,
        manufacturer: str,
        engine_code: str,
        specifications: Dict[str, Any],
        history: Optional[Dict[str, Any]] = None,
        parts_catalog: Optional[Dict[str, Any]] = None,
        interchangeability: Optional[Dict[str, Any]] = None,
        tools_procedures: Optional[Dict[str, Any]] = None,
        aftermarket: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create comprehensive documentation for an engine.

        Args:
            manufacturer: Manufacturer name
            engine_code: Engine code/designation
            specifications: Technical specifications
            history: Historical context (optional)
            parts_catalog: Parts catalog data (optional)
            interchangeability: Compatibility data (optional)
            tools_procedures: Service procedures (optional)
            aftermarket: Aftermarket ecosystem (optional)

        Returns:
            Result dictionary with paths and status
        """
        # Create engine directory
        engine_dir = self._get_engine_directory(manufacturer, engine_code)
        engine_dir.mkdir(parents=True, exist_ok=True)

        created_files = []
        errors = []

        # Generate engine code slug for filenames
        engine_slug = self._generate_slug(engine_code)

        # 1. Master file (always created)
        master_path = engine_dir / REQUIRED_FILES["master"].format(engine=engine_slug)
        try:
            master_data = self._build_master_document(
                manufacturer, engine_code, specifications, history
            )
            self._write_json(master_path, master_data)
            created_files.append(str(master_path))
            logger.info(f"Created master document: {master_path}")
        except Exception as e:
            errors.append(f"Master file error: {e}")

        # 2. Parts catalog
        if parts_catalog:
            catalog_path = engine_dir / REQUIRED_FILES["catalog"].format(engine=engine_slug)
            try:
                catalog_data = self._build_parts_catalog(engine_code, parts_catalog)
                self._write_json(catalog_path, catalog_data)
                created_files.append(str(catalog_path))
            except Exception as e:
                errors.append(f"Parts catalog error: {e}")

        # 3. Interchangeability matrix
        if interchangeability:
            inter_path = engine_dir / REQUIRED_FILES["interchange"].format(engine=engine_slug)
            try:
                inter_data = self._build_interchangeability(engine_code, interchangeability)
                self._write_json(inter_path, inter_data)
                created_files.append(str(inter_path))
            except Exception as e:
                errors.append(f"Interchangeability error: {e}")

        # 4. Tools and procedures
        if tools_procedures:
            tools_path = engine_dir / REQUIRED_FILES["tools"].format(engine=engine_slug)
            try:
                tools_data = self._build_tools_procedures(engine_code, tools_procedures)
                self._write_json(tools_path, tools_data)
                created_files.append(str(tools_path))
            except Exception as e:
                errors.append(f"Tools/procedures error: {e}")

        # 5. Aftermarket ecosystem
        if aftermarket:
            after_path = engine_dir / REQUIRED_FILES["aftermarket"].format(engine=engine_slug)
            try:
                after_data = self._build_aftermarket(engine_code, aftermarket)
                self._write_json(after_path, after_data)
                created_files.append(str(after_path))
            except Exception as e:
                errors.append(f"Aftermarket error: {e}")

        return {
            "success": len(errors) == 0,
            "engine_code": engine_code,
            "manufacturer": manufacturer,
            "directory": str(engine_dir),
            "paths": created_files,
            "files_created": len(created_files),
            "errors": errors
        }

    def _get_engine_directory(self, manufacturer: str, engine_code: str) -> Path:
        """Get or create the engine documentation directory."""
        # Format: Manufacturers/MANUFACTURER/MANUFACTURER-ENGINE-DISPLACEMENT
        engine_slug = self._generate_directory_name(manufacturer, engine_code)
        return self.base_path / manufacturer / engine_slug

    def _generate_slug(self, engine_code: str) -> str:
        """Generate a filename-safe slug from engine code."""
        return engine_code.lower().replace(" ", "-").replace("/", "-")

    def _generate_directory_name(self, manufacturer: str, engine_code: str) -> str:
        """Generate directory name in standard format."""
        return f"{manufacturer.upper()}-{engine_code.upper().replace(' ', '-')}"

    def _build_master_document(
        self,
        manufacturer: str,
        engine_code: str,
        specifications: Dict[str, Any],
        history: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build the master documentation JSON."""
        doc = {
            "engine_family": specifications.get("engine_family", engine_code),
            "manufacturer": manufacturer,
            "engine_code": engine_code,
            "production_years": specifications.get("production_years", ""),
            "vehicles_used": specifications.get("vehicles_used", []),
            "documentation": {
                "version": self.documentation_version,
                "last_updated": datetime.now().isoformat(),
                "documented_by": "Agent_7:CHRONICLER"
            },
            "specifications": {
                "displacement_cc": specifications.get("displacement_cc", 0),
                "configuration": specifications.get("configuration", ""),
                "aspiration": specifications.get("aspiration", "NA"),
                "compression_ratio": specifications.get("compression_ratio", 0.0),
                "power": {
                    "hp": specifications.get("power_hp", 0),
                    "kw": specifications.get("power_kw", 0),
                    "at_rpm": specifications.get("power_rpm", 0)
                },
                "torque": {
                    "nm": specifications.get("torque_nm", 0),
                    "lb_ft": specifications.get("torque_lb_ft", 0),
                    "at_rpm": specifications.get("torque_rpm", 0)
                },
                "redline_rpm": specifications.get("redline_rpm", 0),
                "bore_mm": specifications.get("bore_mm", 0.0),
                "stroke_mm": specifications.get("stroke_mm", 0.0),
                "block_material": specifications.get("block_material", ""),
                "head_material": specifications.get("head_material", ""),
                "valvetrain": specifications.get("valvetrain", ""),
                "valves_per_cylinder": specifications.get("valves_per_cylinder", 0),
                "fuel_system": specifications.get("fuel_system", ""),
                "vvt_system": specifications.get("vvt_system")
            }
        }

        # Add variants if provided
        if "variants" in specifications:
            doc["variants"] = specifications["variants"]

        # Add history if provided
        if history:
            doc["history"] = {
                "development_story": history.get("development_story", ""),
                "engineering_team": history.get("engineering_team", []),
                "design_philosophy": history.get("design_philosophy", ""),
                "notable_innovations": history.get("notable_innovations", []),
                "racing_achievements": history.get("racing_achievements", []),
                "cultural_impact": history.get("cultural_impact", ""),
                "production_start_year": history.get("production_start_year"),
                "production_end_year": history.get("production_end_year")
            }

        # Add legacy if provided
        if "legacy" in specifications:
            doc["legacy"] = specifications["legacy"]

        return doc

    def _build_parts_catalog(
        self,
        engine_code: str,
        parts_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build the parts catalog JSON."""
        return {
            "engine_code": engine_code,
            "catalog_version": self.documentation_version,
            "last_updated": datetime.now().isoformat(),
            "parts": {
                "block": parts_data.get("block", []),
                "head": parts_data.get("head", []),
                "valvetrain": parts_data.get("valvetrain", []),
                "internals": parts_data.get("internals", []),
                "fuel_system": parts_data.get("fuel_system", []),
                "cooling": parts_data.get("cooling", []),
                "oiling": parts_data.get("oiling", []),
                "ignition": parts_data.get("ignition", []),
                "intake": parts_data.get("intake", []),
                "exhaust": parts_data.get("exhaust", []),
                "accessories": parts_data.get("accessories", [])
            },
            "oem_part_numbers": parts_data.get("oem_part_numbers", {}),
            "critical_torque_specs": parts_data.get("torque_specs", {})
        }

    def _build_interchangeability(
        self,
        engine_code: str,
        inter_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build the interchangeability matrix JSON."""
        return {
            "engine_code": engine_code,
            "matrix_version": self.documentation_version,
            "last_updated": datetime.now().isoformat(),
            "compatibility_matrix": inter_data.get("matrix", []),
            "cross_reference": {
                "same_family": inter_data.get("same_family", []),
                "different_family_compatible": inter_data.get("cross_compatible", []),
                "common_swaps": inter_data.get("common_swaps", [])
            },
            "warnings": inter_data.get("warnings", []),
            "notes": inter_data.get("notes", "")
        }

    def _build_tools_procedures(
        self,
        engine_code: str,
        tools_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build the tools and procedures JSON."""
        return {
            "engine_code": engine_code,
            "procedures_version": self.documentation_version,
            "last_updated": datetime.now().isoformat(),
            "special_tools": tools_data.get("special_tools", []),
            "common_tools": tools_data.get("common_tools", []),
            "procedures": {
                "timing": tools_data.get("timing_procedure", {}),
                "valve_adjustment": tools_data.get("valve_adjustment", {}),
                "oil_change": tools_data.get("oil_change", {}),
                "head_removal": tools_data.get("head_removal", {}),
                "rebuild": tools_data.get("rebuild_procedure", {})
            },
            "torque_specifications": tools_data.get("torque_specs", {}),
            "fluid_capacities": tools_data.get("fluid_capacities", {}),
            "service_intervals": tools_data.get("service_intervals", {})
        }

    def _build_aftermarket(
        self,
        engine_code: str,
        aftermarket_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build the aftermarket ecosystem JSON."""
        return {
            "engine_code": engine_code,
            "ecosystem_version": self.documentation_version,
            "last_updated": datetime.now().isoformat(),
            "vendors": {
                "performance": aftermarket_data.get("performance_vendors", []),
                "oem_replacement": aftermarket_data.get("oem_vendors", []),
                "budget": aftermarket_data.get("budget_vendors", []),
                "specialty": aftermarket_data.get("specialty_vendors", []),
                "machine_shops": aftermarket_data.get("machine_shops", [])
            },
            "build_levels": {
                "stage_1": aftermarket_data.get("stage_1", {}),
                "stage_2": aftermarket_data.get("stage_2", {}),
                "stage_3": aftermarket_data.get("stage_3", {}),
                "race_build": aftermarket_data.get("race_build", {})
            },
            "popular_modifications": aftermarket_data.get("popular_mods", []),
            "community_resources": {
                "forums": aftermarket_data.get("forums", []),
                "facebook_groups": aftermarket_data.get("facebook_groups", []),
                "discord_servers": aftermarket_data.get("discord_servers", []),
                "youtube_channels": aftermarket_data.get("youtube_channels", []),
                "notable_build_threads": aftermarket_data.get("build_threads", [])
            },
            "power_potential": aftermarket_data.get("power_potential", {})
        }

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        """Write JSON data to file with proper formatting."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def read_engine_documentation(
        self,
        manufacturer: str,
        engine_code: str
    ) -> Optional[Dict[str, Any]]:
        """Read existing engine documentation."""
        engine_dir = self._get_engine_directory(manufacturer, engine_code)
        engine_slug = self._generate_slug(engine_code)
        master_path = engine_dir / REQUIRED_FILES["master"].format(engine=engine_slug)

        if master_path.exists():
            with open(master_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def list_documented_engines(self, manufacturer: str) -> List[str]:
        """List all documented engines for a manufacturer."""
        manufacturer_path = self.base_path / manufacturer
        if not manufacturer_path.exists():
            return []

        engines = []
        for engine_dir in manufacturer_path.iterdir():
            if engine_dir.is_dir():
                # Check for master file
                for f in engine_dir.glob("*-master.json"):
                    engines.append(engine_dir.name)
                    break

        return engines

    def get_documentation_completeness(
        self,
        manufacturer: str,
        engine_code: str
    ) -> Dict[str, bool]:
        """Check which documentation files exist for an engine."""
        engine_dir = self._get_engine_directory(manufacturer, engine_code)
        engine_slug = self._generate_slug(engine_code)

        completeness = {}
        for name, pattern in REQUIRED_FILES.items():
            file_path = engine_dir / pattern.format(engine=engine_slug)
            completeness[name] = file_path.exists()

        for name, pattern in OPTIONAL_FILES.items():
            file_path = engine_dir / pattern.format(engine=engine_slug)
            completeness[name] = file_path.exists()

        return completeness
