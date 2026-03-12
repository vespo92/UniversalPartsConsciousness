"""
CSV / JSON / Excel Part Importer
==================================
"The simplest path to consciousness — a spreadsheet."

Imports parts from structured data files (CSV, JSON, JSONL, Excel)
with automatic column mapping, unit detection, and taxonomy classification.

Supports:
  - CSV with header detection and column mapping
  - JSON (array of objects or nested BOM)
  - JSONL (one object per line)
  - Excel (.xlsx) with multi-sheet support
"""

from __future__ import annotations

import csv
import io
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("UPC.Ingestion.CSV")


# Column name mappings — maps common header names to our standard fields
COLUMN_MAPPINGS: Dict[str, str] = {
    # Part number
    "part_number": "part_number",
    "part number": "part_number",
    "part #": "part_number",
    "part#": "part_number",
    "p/n": "part_number",
    "pn": "part_number",
    "item number": "part_number",
    "item #": "part_number",
    "item_number": "part_number",
    "sku": "part_number",
    "catalog number": "part_number",
    "catalog #": "part_number",
    "catalog_number": "part_number",
    "mpn": "part_number",

    # Name / Description
    "name": "name",
    "part name": "name",
    "part_name": "name",
    "description": "description",
    "desc": "description",
    "title": "name",
    "item": "name",
    "item_description": "description",
    "product_name": "name",

    # Manufacturer
    "manufacturer": "manufacturer",
    "mfr": "manufacturer",
    "mfg": "manufacturer",
    "brand": "brand",
    "vendor": "manufacturer",
    "supplier": "data_source",
    "make": "manufacturer",

    # Category
    "category": "taxonomy_code",
    "type": "taxonomy_code",
    "part_type": "taxonomy_code",
    "part type": "taxonomy_code",
    "subcategory": "subcategory",
    "class": "taxonomy_code",

    # Material
    "material": "material",
    "material_grade": "material_grade",
    "material grade": "material_grade",
    "alloy": "material",
    "finish": "finish",
    "coating": "coating",

    # Thread spec
    "thread": "thread_spec",
    "thread_spec": "thread_spec",
    "thread spec": "thread_spec",
    "thread size": "thread_spec",
    "thread_size": "thread_spec",

    # Dimensions
    "length": "length_mm",
    "length_mm": "length_mm",
    "length (mm)": "length_mm",
    "length_in": "length_in",
    "length (in)": "length_in",
    "width": "width_mm",
    "width_mm": "width_mm",
    "height": "height_mm",
    "height_mm": "height_mm",
    "diameter": "diameter_mm",
    "diameter_mm": "diameter_mm",
    "od": "outer_diameter_mm",
    "outer_diameter": "outer_diameter_mm",
    "id": "inner_diameter_mm",
    "inner_diameter": "inner_diameter_mm",
    "bore": "bore_diameter_mm",
    "thickness": "thickness_mm",

    # Mechanical properties
    "tensile_strength": "tensile_strength_mpa",
    "tensile strength": "tensile_strength_mpa",
    "tensile strength (mpa)": "tensile_strength_mpa",
    "yield_strength": "yield_strength_mpa",
    "yield strength": "yield_strength_mpa",
    "hardness": "hardness",
    "grade": "grade",

    # Fastener-specific
    "head_type": "head_type",
    "head type": "head_type",
    "drive_type": "drive_type",
    "drive type": "drive_type",
    "drive_size": "drive_size",
    "drive size": "drive_size",

    # Pricing
    "price": "price_usd",
    "unit_price": "price_usd",
    "unit price": "price_usd",
    "cost": "price_usd",
    "price_usd": "price_usd",

    # Quantity (for BOM imports)
    "quantity": "quantity",
    "qty": "quantity",
    "count": "quantity",

    # Weight
    "weight": "weight_kg",
    "weight_kg": "weight_kg",
    "weight (kg)": "weight_kg",
    "weight_lb": "weight_lb",
    "weight (lb)": "weight_lb",
    "mass": "weight_kg",

    # Standard
    "standard": "standard_designation",
    "standard_designation": "standard_designation",
    "din": "standard_designation",
    "iso": "standard_designation",

    # Reference designator (for BOM)
    "reference": "reference_designator",
    "ref": "reference_designator",
    "ref_des": "reference_designator",
    "designator": "reference_designator",

    # Notes
    "notes": "notes",
    "remarks": "notes",
    "comment": "notes",
    "comments": "notes",
}


@dataclass
class ImportResult:
    """Result of a file import operation."""
    success: bool
    file_path: str
    total_rows: int = 0
    imported_rows: int = 0
    skipped_rows: int = 0
    error_rows: int = 0
    column_mapping: Dict[str, str] = field(default_factory=dict)
    unmapped_columns: List[str] = field(default_factory=list)
    parts: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"Import: {self.file_path}",
            f"  Total rows: {self.total_rows}",
            f"  Imported: {self.imported_rows}",
            f"  Skipped: {self.skipped_rows}",
            f"  Errors: {self.error_rows}",
        ]
        if self.unmapped_columns:
            lines.append(f"  Unmapped columns: {', '.join(self.unmapped_columns)}")
        if self.warnings:
            lines.append(f"  Warnings: {len(self.warnings)}")
        return "\n".join(lines)


class CSVPartImporter:
    """
    Import parts from CSV, JSON, JSONL, and Excel files.

    Usage:
        importer = CSVPartImporter()
        result = importer.import_file("parts.csv")
        for part in result.parts:
            print(part["name"], part.get("part_number"))

        # Custom column mapping
        result = importer.import_file("parts.csv", column_map={
            "my_weird_column": "part_number",
            "size": "thread_spec",
        })
    """

    def __init__(self, custom_mappings: Optional[Dict[str, str]] = None):
        self.column_map = {**COLUMN_MAPPINGS}
        if custom_mappings:
            self.column_map.update({k.lower(): v for k, v in custom_mappings.items()})

    def import_file(
        self,
        file_path: str | Path,
        column_map: Optional[Dict[str, str]] = None,
        sheet_name: Optional[str] = None,
        encoding: str = "utf-8",
        delimiter: str = ",",
    ) -> ImportResult:
        """
        Import parts from a file.

        Automatically detects format by extension.
        """
        path = Path(file_path)
        if not path.exists():
            return ImportResult(success=False, file_path=str(path),
                                errors=[{"error": f"File not found: {path}"}])

        # Merge custom column map
        effective_map = {**self.column_map}
        if column_map:
            effective_map.update({k.lower(): v for k, v in column_map.items()})

        suffix = path.suffix.lower()

        if suffix == ".csv":
            return self._import_csv(path, effective_map, encoding, delimiter)
        elif suffix == ".tsv":
            return self._import_csv(path, effective_map, encoding, "\t")
        elif suffix == ".json":
            return self._import_json(path, effective_map, encoding)
        elif suffix == ".jsonl":
            return self._import_jsonl(path, effective_map, encoding)
        elif suffix in (".xlsx", ".xls"):
            return self._import_excel(path, effective_map, sheet_name)
        else:
            return ImportResult(
                success=False, file_path=str(path),
                errors=[{"error": f"Unsupported file format: {suffix}"}],
            )

    def _import_csv(
        self,
        path: Path,
        col_map: Dict[str, str],
        encoding: str,
        delimiter: str,
    ) -> ImportResult:
        """Import from CSV/TSV."""
        result = ImportResult(success=True, file_path=str(path))

        try:
            with open(path, "r", encoding=encoding, errors="replace") as f:
                # Detect dialect
                sample = f.read(8192)
                f.seek(0)

                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
                except csv.Error:
                    dialect = None

                reader = csv.DictReader(
                    f,
                    delimiter=delimiter if dialect is None else dialect.delimiter,
                )

                if not reader.fieldnames:
                    result.success = False
                    result.errors.append({"error": "No headers found in CSV"})
                    return result

                # Map columns
                mapping, unmapped = self._map_columns(reader.fieldnames, col_map)
                result.column_mapping = mapping
                result.unmapped_columns = unmapped

                for row_num, row in enumerate(reader, start=2):
                    result.total_rows += 1
                    try:
                        part = self._transform_row(row, mapping)
                        if part.get("name") or part.get("part_number"):
                            result.parts.append(part)
                            result.imported_rows += 1
                        else:
                            result.skipped_rows += 1
                    except Exception as e:
                        result.error_rows += 1
                        result.errors.append({"row": row_num, "error": str(e)})

        except Exception as e:
            result.success = False
            result.errors.append({"error": str(e)})

        return result

    def _import_json(
        self,
        path: Path,
        col_map: Dict[str, str],
        encoding: str,
    ) -> ImportResult:
        """Import from JSON (array of objects or nested BOM)."""
        result = ImportResult(success=True, file_path=str(path))

        try:
            with open(path, "r", encoding=encoding) as f:
                data = json.load(f)

            # Handle different JSON structures
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Look for common array keys
                for key in ["parts", "items", "data", "records", "bom", "components"]:
                    if key in data and isinstance(data[key], list):
                        items = data[key]
                        break
                else:
                    items = [data]
            else:
                result.success = False
                result.errors.append({"error": "Unexpected JSON structure"})
                return result

            for idx, item in enumerate(items):
                result.total_rows += 1
                if not isinstance(item, dict):
                    result.skipped_rows += 1
                    continue

                try:
                    # Map keys
                    keys = list(item.keys())
                    if idx == 0:
                        mapping, unmapped = self._map_columns(keys, col_map)
                        result.column_mapping = mapping
                        result.unmapped_columns = unmapped

                    part = self._transform_row(item, result.column_mapping)

                    # For JSON, also preserve any extra fields as specs
                    extra_specs = {}
                    for key, value in item.items():
                        if key.lower() not in col_map and value is not None:
                            extra_specs[key] = value
                    if extra_specs:
                        part.setdefault("specifications", {}).update(extra_specs)

                    if part.get("name") or part.get("part_number"):
                        result.parts.append(part)
                        result.imported_rows += 1
                    else:
                        result.skipped_rows += 1

                except Exception as e:
                    result.error_rows += 1
                    result.errors.append({"index": idx, "error": str(e)})

        except json.JSONDecodeError as e:
            result.success = False
            result.errors.append({"error": f"Invalid JSON: {e}"})
        except Exception as e:
            result.success = False
            result.errors.append({"error": str(e)})

        return result

    def _import_jsonl(
        self,
        path: Path,
        col_map: Dict[str, str],
        encoding: str,
    ) -> ImportResult:
        """Import from JSONL (one JSON object per line)."""
        result = ImportResult(success=True, file_path=str(path))

        try:
            with open(path, "r", encoding=encoding) as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue

                    result.total_rows += 1
                    try:
                        item = json.loads(line)
                        if not isinstance(item, dict):
                            result.skipped_rows += 1
                            continue

                        if line_num == 1:
                            mapping, unmapped = self._map_columns(
                                list(item.keys()), col_map
                            )
                            result.column_mapping = mapping
                            result.unmapped_columns = unmapped

                        part = self._transform_row(item, result.column_mapping)
                        if part.get("name") or part.get("part_number"):
                            result.parts.append(part)
                            result.imported_rows += 1
                        else:
                            result.skipped_rows += 1

                    except json.JSONDecodeError as e:
                        result.error_rows += 1
                        result.errors.append({"line": line_num, "error": str(e)})
                    except Exception as e:
                        result.error_rows += 1
                        result.errors.append({"line": line_num, "error": str(e)})

        except Exception as e:
            result.success = False
            result.errors.append({"error": str(e)})

        return result

    def _import_excel(
        self,
        path: Path,
        col_map: Dict[str, str],
        sheet_name: Optional[str],
    ) -> ImportResult:
        """Import from Excel (.xlsx)."""
        result = ImportResult(success=True, file_path=str(path))

        try:
            import openpyxl
        except ImportError:
            result.success = False
            result.errors.append({
                "error": "openpyxl required for Excel import: pip install openpyxl"
            })
            return result

        try:
            wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
            sheet = wb[sheet_name] if sheet_name else wb.active

            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                result.success = False
                result.errors.append({"error": "Empty spreadsheet"})
                return result

            # First row is headers
            headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(rows[0])]
            mapping, unmapped = self._map_columns(headers, col_map)
            result.column_mapping = mapping
            result.unmapped_columns = unmapped

            for row_num, row in enumerate(rows[1:], start=2):
                result.total_rows += 1
                try:
                    row_dict = {}
                    for i, (header, value) in enumerate(zip(headers, row)):
                        if value is not None:
                            row_dict[header] = value

                    part = self._transform_row(row_dict, mapping)
                    if part.get("name") or part.get("part_number"):
                        result.parts.append(part)
                        result.imported_rows += 1
                    else:
                        result.skipped_rows += 1

                except Exception as e:
                    result.error_rows += 1
                    result.errors.append({"row": row_num, "error": str(e)})

            wb.close()

        except Exception as e:
            result.success = False
            result.errors.append({"error": str(e)})

        return result

    def _map_columns(
        self,
        headers: List[str],
        col_map: Dict[str, str],
    ) -> Tuple[Dict[str, str], List[str]]:
        """Map source column names to standard field names."""
        mapping = {}
        unmapped = []

        for header in headers:
            if not header:
                continue
            header_lower = header.lower().strip()
            if header_lower in col_map:
                mapping[header] = col_map[header_lower]
            else:
                # Try fuzzy matching
                matched = False
                for pattern, target in col_map.items():
                    if pattern in header_lower or header_lower in pattern:
                        mapping[header] = target
                        matched = True
                        break
                if not matched:
                    unmapped.append(header)

        return mapping, unmapped

    def _transform_row(
        self,
        row: Dict[str, Any],
        mapping: Dict[str, str],
    ) -> Dict[str, Any]:
        """Transform a row using column mapping, with unit conversion."""
        part: Dict[str, Any] = {"specifications": {}}

        for source_col, target_field in mapping.items():
            value = row.get(source_col)
            if value is None or (isinstance(value, str) and not value.strip()):
                continue

            # Convert value types
            value = self._convert_value(target_field, value)

            if target_field in (
                "part_number", "name", "description", "manufacturer", "brand",
                "material", "material_grade", "taxonomy_code", "subcategory",
                "standard_designation", "thread_spec", "head_type", "drive_type",
                "drive_size", "hardness", "grade", "finish", "coating",
                "reference_designator", "notes", "data_source",
            ):
                part[target_field] = str(value).strip()
            elif target_field in (
                "length_mm", "width_mm", "height_mm", "diameter_mm",
                "outer_diameter_mm", "inner_diameter_mm", "bore_diameter_mm",
                "thickness_mm", "tensile_strength_mpa", "yield_strength_mpa",
                "price_usd", "weight_kg", "quantity",
            ):
                try:
                    part[target_field] = float(value)
                except (ValueError, TypeError):
                    pass
            else:
                # Put unknown fields in specifications
                part["specifications"][target_field] = value

        # Handle imperial conversions
        if "length_in" in {mapping.get(k) for k in row}:
            length_in = row.get(
                next((k for k, v in mapping.items() if v == "length_in"), ""), None
            )
            if length_in:
                try:
                    part["length_mm"] = float(length_in) * 25.4
                except (ValueError, TypeError):
                    pass

        if "weight_lb" in {mapping.get(k) for k in row}:
            weight_lb = row.get(
                next((k for k, v in mapping.items() if v == "weight_lb"), ""), None
            )
            if weight_lb:
                try:
                    part["weight_kg"] = float(weight_lb) * 0.453592
                except (ValueError, TypeError):
                    pass

        return part

    @staticmethod
    def _convert_value(field_name: str, value: Any) -> Any:
        """Convert values, stripping units if present."""
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            value = value.strip()
            # Strip common unit suffixes for numeric fields
            if field_name.endswith(("_mm", "_mpa", "_usd", "_kg")):
                # Remove unit text like "25.4 mm" -> "25.4"
                cleaned = re.sub(r'\s*(mm|in|mpa|psi|usd|\$|kg|lb|g)\s*$', '', value, flags=re.IGNORECASE)
                cleaned = cleaned.replace(",", "")
                try:
                    return float(cleaned)
                except ValueError:
                    return value
        return value

    @staticmethod
    def generate_template(format: str = "csv") -> str:
        """Generate a template file content for part import."""
        headers = [
            "part_number", "name", "description", "manufacturer",
            "category", "material", "thread_spec",
            "length_mm", "diameter_mm", "weight_kg",
            "tensile_strength_mpa", "hardness", "grade",
            "head_type", "drive_type", "price_usd",
            "standard", "notes",
        ]

        if format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            # Example row
            writer.writerow([
                "91290A113", "M3x0.5 Socket Head Cap Screw, 10mm",
                "Alloy steel socket head cap screw", "Generic",
                "MECH.FAST.SCRW.SHCS", "Alloy Steel", "M3x0.5",
                "10", "3", "0.002",
                "1220", "HRC 38-43", "12.9",
                "Socket Head", "Hex Socket", "0.15",
                "DIN 912", "",
            ])
            return output.getvalue()

        elif format == "json":
            template = {
                "parts": [
                    {
                        "part_number": "91290A113",
                        "name": "M3x0.5 Socket Head Cap Screw, 10mm",
                        "description": "Alloy steel socket head cap screw",
                        "manufacturer": "Generic",
                        "category": "MECH.FAST.SCRW.SHCS",
                        "material": "Alloy Steel",
                        "thread_spec": "M3x0.5",
                        "length_mm": 10,
                        "diameter_mm": 3,
                        "weight_kg": 0.002,
                        "tensile_strength_mpa": 1220,
                        "hardness": "HRC 38-43",
                        "grade": "12.9",
                        "head_type": "Socket Head",
                        "drive_type": "Hex Socket",
                        "price_usd": 0.15,
                        "standard": "DIN 912",
                    }
                ]
            }
            return json.dumps(template, indent=2)

        else:
            raise ValueError(f"Unsupported template format: {format}")
