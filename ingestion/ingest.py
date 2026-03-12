"""
Universal Part Ingestor
========================
"One gateway. All parts. Every format."

The UniversalIngestor is the single entry point for getting data
into the Universal Parts Consciousness. It orchestrates:

  1. Source detection (file type, API, or manual)
  2. Parsing / fetching
  3. Taxonomy classification
  4. Normalization & validation
  5. Quality scoring
  6. Storage (JSON output, database, or stream)

Usage:
    # CLI
    python -m ingestion.ingest file parts.csv
    python -m ingestion.ingest file bracket.step
    python -m ingestion.ingest search --source digikey "10k resistor"
    python -m ingestion.ingest import --source iso_standards --category threads

    # Python API
    ingestor = UniversalIngestor()
    results = await ingestor.ingest_file("parts.csv")
    results = await ingestor.search_and_ingest("digikey", "M8 socket head cap screw")
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .parsers.step_parser import STEPParser, STEPPartData
from .parsers.csv_parser import CSVPartImporter, ImportResult
from .parsers.assembly_parser import AssemblyParser, AssemblyIngestResult
from .connectors.base import ConnectorRegistry, DataSourceConnector, FetchedPart, SourceConfig

logger = logging.getLogger("UPC.Ingestor")

# Lazy import taxonomy to avoid circular imports
_taxonomy = None


def _get_taxonomy():
    global _taxonomy
    if _taxonomy is None:
        from taxonomy import get_taxonomy
        _taxonomy = get_taxonomy()
    return _taxonomy


@dataclass
class IngestResult:
    """Result of an ingestion operation."""
    success: bool
    source: str
    operation: str  # "file", "search", "category", "part"

    parts_processed: int = 0
    parts_accepted: int = 0
    parts_rejected: int = 0

    output_file: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # The actual ingested data
    parts: List[Dict[str, Any]] = field(default_factory=list)

    duration_seconds: float = 0.0

    def summary(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        lines = [
            f"[{status}] Ingestion from {self.source} ({self.operation})",
            f"  Processed: {self.parts_processed}",
            f"  Accepted:  {self.parts_accepted}",
            f"  Rejected:  {self.parts_rejected}",
            f"  Duration:  {self.duration_seconds:.1f}s",
        ]
        if self.output_file:
            lines.append(f"  Output:    {self.output_file}")
        if self.errors:
            lines.append(f"  Errors:    {len(self.errors)}")
        if self.warnings:
            lines.append(f"  Warnings:  {len(self.warnings)}")
        return "\n".join(lines)


class UniversalIngestor:
    """
    Unified ingestion orchestrator.

    Handles all data sources and formats through a single interface.
    """

    def __init__(self, output_dir: str | Path = "./data/ingested"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.step_parser = STEPParser()
        self.csv_importer = CSVPartImporter()

    async def ingest_file(
        self,
        file_path: str | Path,
        column_map: Optional[Dict[str, str]] = None,
        output: Optional[str] = None,
    ) -> IngestResult:
        """
        Ingest parts from a file.

        Supports: CSV, JSON, JSONL, Excel, STEP, IGES, STL
        """
        start = datetime.utcnow()
        path = Path(file_path)

        if not path.exists():
            return IngestResult(
                success=False, source=str(path), operation="file",
                errors=[f"File not found: {path}"],
            )

        suffix = path.suffix.lower()

        # CAD files
        if suffix in (".step", ".stp", ".iges", ".igs", ".stl"):
            return self._ingest_cad_file(path, output, start)

        # Tabular data files
        if suffix in (".csv", ".tsv", ".json", ".jsonl", ".xlsx", ".xls"):
            return self._ingest_tabular_file(path, column_map, output, start)

        return IngestResult(
            success=False, source=str(path), operation="file",
            errors=[f"Unsupported file type: {suffix}"],
        )

    def _ingest_cad_file(
        self,
        path: Path,
        output: Optional[str],
        start: datetime,
    ) -> IngestResult:
        """Ingest a CAD file (STEP/IGES/STL)."""
        result = IngestResult(
            success=True, source=str(path), operation="file",
        )

        try:
            part_data = self.step_parser.parse(path)
            part_dict = self._cad_to_universal(part_data)

            result.parts = [part_dict]
            result.parts_processed = 1
            result.parts_accepted = 1

            # Also process child parts in assemblies
            for child in part_data.children:
                child_dict = self._cad_to_universal(child)
                result.parts.append(child_dict)
                result.parts_processed += 1
                result.parts_accepted += 1

            # Save output
            output_path = self._save_output(result.parts, output or path.stem)
            result.output_file = str(output_path)

            if not self.step_parser.geometry_available:
                result.warnings.append(
                    "Geometry parsing unavailable (install cadquery or OCP). "
                    "Only header metadata was extracted."
                )

        except Exception as e:
            result.success = False
            result.errors.append(str(e))

        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    def _ingest_tabular_file(
        self,
        path: Path,
        column_map: Optional[Dict[str, str]],
        output: Optional[str],
        start: datetime,
    ) -> IngestResult:
        """Ingest a CSV/JSON/Excel file."""
        result = IngestResult(
            success=True, source=str(path), operation="file",
        )

        try:
            import_result = self.csv_importer.import_file(path, column_map=column_map)

            if not import_result.success:
                result.success = False
                result.errors = [e.get("error", str(e)) for e in import_result.errors]
                return result

            result.parts_processed = import_result.total_rows
            result.parts_rejected = import_result.skipped_rows + import_result.error_rows

            # Enhance each part with UPC fields
            for part in import_result.parts:
                enhanced = self._enhance_part(part)
                result.parts.append(enhanced)
                result.parts_accepted += 1

            if import_result.unmapped_columns:
                result.warnings.append(
                    f"Unmapped columns: {', '.join(import_result.unmapped_columns)}"
                )

            # Save output
            output_path = self._save_output(result.parts, output or path.stem)
            result.output_file = str(output_path)

        except Exception as e:
            result.success = False
            result.errors.append(str(e))

        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    async def search_and_ingest(
        self,
        source_id: str,
        query: str,
        category: Optional[str] = None,
        max_results: int = 100,
        output: Optional[str] = None,
    ) -> IngestResult:
        """
        Search a data source and ingest results.

        Args:
            source_id: Connector ID (e.g., "digikey", "grabcad", "iso_standards")
            query: Search query
            category: Optional category filter
            max_results: Maximum results to fetch
            output: Optional output filename
        """
        start = datetime.utcnow()
        result = IngestResult(
            success=True, source=source_id, operation="search",
        )

        try:
            connector = self._get_connector(source_id)
            fetched_count = 0

            async for fetched_part in connector.fetch_all(
                query=query, category=category, max_items=max_results,
            ):
                result.parts_processed += 1
                try:
                    part_dict = self._fetched_to_universal(fetched_part)
                    result.parts.append(part_dict)
                    result.parts_accepted += 1
                    fetched_count += 1
                except Exception as e:
                    result.parts_rejected += 1
                    result.errors.append(f"Transform error: {e}")

            # Save output
            output_name = output or f"{source_id}_{query.replace(' ', '_')[:30]}"
            output_path = self._save_output(result.parts, output_name)
            result.output_file = str(output_path)

        except Exception as e:
            result.success = False
            result.errors.append(str(e))

        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    async def ingest_category(
        self,
        source_id: str,
        category: str,
        max_results: int = 500,
        output: Optional[str] = None,
    ) -> IngestResult:
        """Ingest all parts from a specific category of a data source."""
        return await self.search_and_ingest(
            source_id=source_id,
            query="",
            category=category,
            max_results=max_results,
            output=output,
        )

    def ingest_directory(
        self,
        dir_path: str | Path,
        recursive: bool = True,
        output: Optional[str] = None,
    ) -> IngestResult:
        """Ingest all supported files from a directory."""
        start = datetime.utcnow()
        path = Path(dir_path)
        result = IngestResult(
            success=True, source=str(path), operation="directory",
        )

        if not path.is_dir():
            result.success = False
            result.errors.append(f"Not a directory: {path}")
            return result

        # Find all supported files
        extensions = {
            ".csv", ".tsv", ".json", ".jsonl", ".xlsx",
            ".step", ".stp", ".iges", ".igs", ".stl",
        }

        pattern = "**/*" if recursive else "*"
        files = [f for f in path.glob(pattern)
                 if f.is_file() and f.suffix.lower() in extensions]

        logger.info(f"Found {len(files)} files to ingest from {path}")

        for file_path in files:
            sub_result = asyncio.get_event_loop().run_until_complete(
                self.ingest_file(file_path)
            )
            result.parts.extend(sub_result.parts)
            result.parts_processed += sub_result.parts_processed
            result.parts_accepted += sub_result.parts_accepted
            result.parts_rejected += sub_result.parts_rejected
            result.errors.extend(sub_result.errors)
            result.warnings.extend(sub_result.warnings)

        # Save combined output
        output_name = output or f"directory_{path.name}"
        output_path = self._save_output(result.parts, output_name)
        result.output_file = str(output_path)

        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    # ---------------------------------------------------------------
    # Transformation helpers
    # ---------------------------------------------------------------

    def _cad_to_universal(self, cad_data: STEPPartData) -> Dict[str, Any]:
        """Transform CAD part data to universal format."""
        part = {
            "name": cad_data.part_names[0] if cad_data.part_names else Path(cad_data.file_path).stem,
            "description": cad_data.description,
            "data_source": f"cad_file:{cad_data.file_format.value}",
            "source_file": cad_data.file_path,
            "file_hash": cad_data.file_hash,
            "material": cad_data.material_name,
            "originating_system": cad_data.originating_system,
            "specifications": {
                "cad_format": cad_data.file_format.value,
                "cad_schema": cad_data.schema,
                "is_assembly": cad_data.is_assembly,
                "part_count": cad_data.part_count,
                "has_threads": cad_data.has_threads,
                "has_holes": cad_data.has_holes,
            },
        }

        if cad_data.bounding_box:
            bb = cad_data.bounding_box
            part["dimension_x_mm"] = round(bb.length, 4)
            part["dimension_y_mm"] = round(bb.width, 4)
            part["dimension_z_mm"] = round(bb.height, 4)
            part["specifications"]["bounding_box"] = bb.to_dict()

        if cad_data.volume_mm3:
            part["specifications"]["volume_mm3"] = round(cad_data.volume_mm3, 4)
        if cad_data.surface_area_mm2:
            part["specifications"]["surface_area_mm2"] = round(cad_data.surface_area_mm2, 4)
        if cad_data.estimated_weight_kg:
            part["weight_kg"] = round(cad_data.estimated_weight_kg, 6)
        if cad_data.detected_hole_diameters_mm:
            part["specifications"]["hole_diameters_mm"] = cad_data.detected_hole_diameters_mm
        if cad_data.center_of_mass:
            part["specifications"]["center_of_mass"] = [
                round(v, 4) for v in cad_data.center_of_mass
            ]

        return self._enhance_part(part)

    def _fetched_to_universal(self, fetched: FetchedPart) -> Dict[str, Any]:
        """Transform a FetchedPart to universal format."""
        part = {
            "name": fetched.name or "",
            "part_number": fetched.part_number,
            "manufacturer": fetched.manufacturer,
            "description": fetched.description,
            "material": fetched.material,
            "data_source": fetched.source_name,
            "source_part_id": fetched.source_id,
            "price_usd": fetched.price,
            "currency": fetched.currency,
            "image_urls": [fetched.image_url] if fetched.image_url else [],
            "datasheet_url": fetched.datasheet_url,
            "cad_models": fetched.cad_models,
            "specifications": fetched.specifications,
        }

        if fetched.category:
            part["source_category"] = fetched.category

        return self._enhance_part(part)

    def _enhance_part(self, part: Dict[str, Any]) -> Dict[str, Any]:
        """Add UPC metadata to a part record."""
        # Generate UPC ID
        identity = "|".join(str(part.get(f, "")) for f in [
            "name", "part_number", "manufacturer", "material",
        ])
        part["upc_id"] = f"UPC-{hashlib.sha256(identity.encode()).hexdigest()[:12].upper()}"

        # Auto-classify using taxonomy
        try:
            taxonomy = _get_taxonomy()
            name = part.get("name", "")
            desc = part.get("description", "")
            text = f"{name} {desc}"

            if text.strip():
                matches = taxonomy.classify(text)
                if matches:
                    best_match, confidence = matches[0]
                    if confidence > 0.3:
                        part["taxonomy_code"] = best_match.full_code
                        part["taxonomy_name"] = best_match.name
                        part["taxonomy_confidence"] = round(confidence, 3)
        except Exception:
            pass  # Taxonomy classification is optional

        # Set quality/consciousness defaults
        part.setdefault("quality_score", 0.0)
        part.setdefault("consciousness_level", "DORMANT")
        part.setdefault("ingested_at", datetime.utcnow().isoformat())
        part.setdefault("version", 1)

        # Calculate completeness
        required_fields = [
            "name", "part_number", "manufacturer", "material",
            "description", "data_source",
        ]
        filled = sum(1 for f in required_fields if part.get(f))
        part["completeness_score"] = round(filled / len(required_fields), 2)

        return part

    def _save_output(
        self, parts: List[Dict[str, Any]], name: str
    ) -> Path:
        """Save ingested parts to JSON."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        output_path = self.output_dir / filename

        output_data = {
            "ingested_at": datetime.utcnow().isoformat(),
            "total_parts": len(parts),
            "parts": parts,
        }

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2, default=str)

        logger.info(f"Saved {len(parts)} parts to {output_path}")
        return output_path

    def _get_connector(self, source_id: str) -> DataSourceConnector:
        """Get or create a connector by source ID."""
        return ConnectorRegistry.create(source_id, SourceConfig(
            source_id=source_id,
            name=source_id,
            source_type=ConnectorRegistry.get_class(source_id).__name__
            if ConnectorRegistry.get_class(source_id)
            else "unknown",
            tier=1,
        ))

    def ingest_assembly(
        self,
        dir_path: str | Path,
        output: Optional[str] = None,
    ) -> IngestResult:
        """
        Ingest an assembly (engine, vehicle, etc.) from a directory
        of structured JSON files.

        This handles deeply nested data like:
          - Engine master specs with variants
          - Parts catalogs with system → component hierarchies
          - Interchangeability matrices
          - Aftermarket ecosystems
          - Tools & service data

        Args:
            dir_path: Path to assembly directory (e.g., Ford-FE-V8/)
            output: Optional output filename
        """
        start = datetime.utcnow()
        path = Path(dir_path)

        result = IngestResult(
            success=True, source=str(path), operation="assembly",
        )

        try:
            parser = AssemblyParser()
            assembly_result = parser.parse_engine_directory(path)

            # Convert assembly parts to universal format
            for part in assembly_result.parts:
                part_dict = part.to_dict()
                part_dict["data_source"] = f"assembly:{assembly_result.assembly_id}"
                enhanced = self._enhance_part(part_dict)
                result.parts.append(enhanced)
                result.parts_accepted += 1

            result.parts_processed = len(assembly_result.parts)

            # Build complete output with all assembly data
            output_data = assembly_result.to_dict()
            output_data["enhanced_parts"] = result.parts

            # Save output
            output_name = output or assembly_result.assembly_id
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"assembly_{output_name}_{timestamp}.json"
            output_path = self.output_dir / filename

            with open(output_path, "w") as f:
                json.dump(output_data, f, indent=2, default=str)

            result.output_file = str(output_path)

            logger.info(
                f"Assembly ingested: {assembly_result.assembly_name} — "
                f"{assembly_result.total_parts} parts, "
                f"{assembly_result.total_relationships} relationships, "
                f"{assembly_result.total_systems} systems, "
                f"{assembly_result.total_variants} variants"
            )

        except Exception as e:
            result.success = False
            result.errors.append(str(e))

        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    def ingest_all_assemblies(
        self,
        manufacturers_dir: str | Path,
        output: Optional[str] = None,
    ) -> IngestResult:
        """
        Ingest ALL engine assemblies under a manufacturers directory.

        Args:
            manufacturers_dir: Root path (e.g., Automotive/Engines/Manufacturers/)
        """
        start = datetime.utcnow()
        path = Path(manufacturers_dir)

        result = IngestResult(
            success=True, source=str(path), operation="all_assemblies",
        )

        parser = AssemblyParser()
        all_results = parser.parse_all_engines(path)

        for assembly_result in all_results:
            for part in assembly_result.parts:
                part_dict = part.to_dict()
                part_dict["data_source"] = f"assembly:{assembly_result.assembly_id}"
                result.parts.append(part_dict)
                result.parts_accepted += 1
            result.parts_processed += len(assembly_result.parts)

        # Save combined output
        output_name = output or "all_engines"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"all_assemblies_{output_name}_{timestamp}.json"
        output_path = self.output_dir / filename

        combined = {
            "ingested_at": datetime.utcnow().isoformat(),
            "total_assemblies": len(all_results),
            "total_parts": result.parts_accepted,
            "assemblies": [r.to_dict() for r in all_results],
        }

        with open(output_path, "w") as f:
            json.dump(combined, f, indent=2, default=str)

        result.output_file = str(output_path)
        result.duration_seconds = (datetime.utcnow() - start).total_seconds()
        return result

    @staticmethod
    def list_sources() -> List[str]:
        """List all available data sources."""
        return ConnectorRegistry.list_sources()

    @staticmethod
    def generate_template(format: str = "csv") -> str:
        """Generate an import template."""
        return CSVPartImporter.generate_template(format)


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    """CLI for the Universal Parts Ingestor."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Universal Parts Consciousness — Data Ingestor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from CSV/JSON/Excel
  python -m ingestion.ingest file parts.csv
  python -m ingestion.ingest file bom.json
  python -m ingestion.ingest file inventory.xlsx

  # Import CAD files
  python -m ingestion.ingest file bracket.step
  python -m ingestion.ingest dir ./cad-models/

  # Ingest engine assemblies (deeply nested BOM data)
  python -m ingestion.ingest assembly Automotive/Engines/Manufacturers/Ford/Ford-FE-V8/
  python -m ingestion.ingest assembly-all Automotive/Engines/Manufacturers/

  # Search supplier APIs
  python -m ingestion.ingest search --source digikey "10k 0805 resistor"
  python -m ingestion.ingest search --source iso_standards "M8"
  python -m ingestion.ingest search --source grabcad "gearbox"

  # Import by category
  python -m ingestion.ingest category --source iso_standards threads

  # Generate import template
  python -m ingestion.ingest template --format csv > template.csv
  python -m ingestion.ingest template --format json > template.json

  # List available sources
  python -m ingestion.ingest sources
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # File import
    file_parser = subparsers.add_parser("file", help="Import from file")
    file_parser.add_argument("path", help="Path to file")
    file_parser.add_argument("-o", "--output", help="Output filename")
    file_parser.add_argument("--column-map", help="JSON column mapping")

    # Directory import
    dir_parser = subparsers.add_parser("dir", help="Import from directory")
    dir_parser.add_argument("path", help="Path to directory")
    dir_parser.add_argument("-o", "--output", help="Output filename")
    dir_parser.add_argument("--no-recursive", action="store_true")

    # Search
    search_parser = subparsers.add_parser("search", help="Search a data source")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--source", required=True, help="Data source ID")
    search_parser.add_argument("--category", help="Category filter")
    search_parser.add_argument("--max", type=int, default=100, help="Max results")
    search_parser.add_argument("-o", "--output", help="Output filename")

    # Category import
    cat_parser = subparsers.add_parser("category", help="Import by category")
    cat_parser.add_argument("category", help="Category ID or name")
    cat_parser.add_argument("--source", required=True, help="Data source ID")
    cat_parser.add_argument("--max", type=int, default=500, help="Max results")
    cat_parser.add_argument("-o", "--output", help="Output filename")

    # Template generation
    tmpl_parser = subparsers.add_parser("template", help="Generate import template")
    tmpl_parser.add_argument("--format", choices=["csv", "json"], default="csv")

    # List sources
    subparsers.add_parser("sources", help="List available data sources")

    # Assembly import (engine directories with nested BOM data)
    asm_parser = subparsers.add_parser("assembly", help="Ingest engine/assembly directory")
    asm_parser.add_argument("path", help="Path to assembly directory")
    asm_parser.add_argument("-o", "--output", help="Output filename")

    # All assemblies import
    asm_all_parser = subparsers.add_parser("assembly-all", help="Ingest all engine assemblies")
    asm_all_parser.add_argument("path", help="Path to manufacturers root directory")
    asm_all_parser.add_argument("-o", "--output", help="Output filename")

    # Taxonomy info
    tax_parser = subparsers.add_parser("taxonomy", help="Show taxonomy info")
    tax_parser.add_argument("--search", help="Search taxonomy")
    tax_parser.add_argument("--code", help="Show specific code")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    ingestor = UniversalIngestor()

    if args.command == "file":
        column_map = json.loads(args.column_map) if args.column_map else None
        result = asyncio.run(
            ingestor.ingest_file(args.path, column_map=column_map, output=args.output)
        )
        print(result.summary())

    elif args.command == "dir":
        result = ingestor.ingest_directory(
            args.path,
            recursive=not args.no_recursive,
            output=args.output,
        )
        print(result.summary())

    elif args.command == "search":
        result = asyncio.run(ingestor.search_and_ingest(
            source_id=args.source,
            query=args.query,
            category=args.category,
            max_results=args.max,
            output=args.output,
        ))
        print(result.summary())

    elif args.command == "category":
        result = asyncio.run(ingestor.ingest_category(
            source_id=args.source,
            category=args.category,
            max_results=args.max,
            output=args.output,
        ))
        print(result.summary())

    elif args.command == "template":
        print(ingestor.generate_template(args.format))

    elif args.command == "sources":
        sources = ingestor.list_sources()
        print("Available data sources:")
        for source in sources:
            print(f"  - {source}")

    elif args.command == "assembly":
        result = ingestor.ingest_assembly(args.path, output=args.output)
        print(result.summary())

    elif args.command == "assembly-all":
        result = ingestor.ingest_all_assemblies(args.path, output=args.output)
        print(result.summary())

    elif args.command == "taxonomy":
        taxonomy = _get_taxonomy()
        if args.search:
            results = taxonomy.search(args.search)
            for node in results:
                print(f"  {node.full_code:40s} {node.name}")
        elif args.code:
            node = taxonomy.get(args.code)
            if node:
                print(f"Code: {node.full_code}")
                print(f"Name: {node.name}")
                print(f"Depth: {node.depth}")
                print(f"Leaf: {node.is_leaf}")
                if node.required_specs:
                    print(f"Required specs: {', '.join(node.required_specs)}")
                if node.children:
                    print(f"Children:")
                    for child in node.children.values():
                        print(f"  {child.full_code:40s} {child.name}")
            else:
                print(f"Unknown taxonomy code: {args.code}")
        else:
            stats = taxonomy.stats()
            print(f"Universal Parts Taxonomy")
            print(f"  Total categories: {stats['total_categories']}")
            print(f"  Leaf categories:  {stats['leaf_categories']}")
            print(f"  Max depth:        {stats['max_depth']}")
            print(f"  Domains:")
            for code, info in stats["domain_breakdown"].items():
                print(f"    {code:6s} {info['name']:40s} ({info['categories']} categories)")


if __name__ == "__main__":
    main()
