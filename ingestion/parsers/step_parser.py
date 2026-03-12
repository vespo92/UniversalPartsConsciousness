"""
STEP / IGES File Parser
========================
"The Rosetta Stone of CAD — every system speaks STEP."

Parses ISO 10303 STEP (.stp/.step) and IGES (.igs/.iges) files
to extract geometry, dimensions, material properties, and BOM data.

This parser works at two levels:
  1. Header parsing (pure Python, no dependencies) — extracts metadata,
     file description, author, organization, schema
  2. Geometry parsing (requires OCP/cadquery) — extracts shapes, dimensions,
     bounding boxes, volumes, surface areas, and BOM structures

Level 1 always works. Level 2 requires optional dependencies.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("UPC.Ingestion.STEP")


class CADFormat(str, Enum):
    STEP = "STEP"
    IGES = "IGES"
    STL = "STL"


@dataclass
class BoundingBox:
    """Axis-aligned bounding box in mm."""
    x_min: float = 0.0
    x_max: float = 0.0
    y_min: float = 0.0
    y_max: float = 0.0
    z_min: float = 0.0
    z_max: float = 0.0

    @property
    def length(self) -> float:
        """Extent in X."""
        return abs(self.x_max - self.x_min)

    @property
    def width(self) -> float:
        """Extent in Y."""
        return abs(self.y_max - self.y_min)

    @property
    def height(self) -> float:
        """Extent in Z."""
        return abs(self.z_max - self.z_min)

    @property
    def diagonal(self) -> float:
        return math.sqrt(self.length**2 + self.width**2 + self.height**2)

    def to_dict(self) -> Dict[str, float]:
        return {
            "x_min": round(self.x_min, 4),
            "x_max": round(self.x_max, 4),
            "y_min": round(self.y_min, 4),
            "y_max": round(self.y_max, 4),
            "z_min": round(self.z_min, 4),
            "z_max": round(self.z_max, 4),
            "length_mm": round(self.length, 4),
            "width_mm": round(self.width, 4),
            "height_mm": round(self.height, 4),
        }


@dataclass
class STEPPartData:
    """Extracted part data from a STEP/IGES file."""
    # File info
    file_path: str
    file_format: CADFormat
    file_size_bytes: int = 0
    file_hash: str = ""  # SHA-256 of file content

    # Header metadata (always available from text parsing)
    description: str = ""
    author: str = ""
    organization: str = ""
    schema: str = ""  # AP203, AP214, AP242
    originating_system: str = ""  # "SolidWorks", "Fusion 360", etc.
    timestamp: Optional[str] = None

    # Geometry data (requires OCP)
    has_geometry: bool = False
    bounding_box: Optional[BoundingBox] = None
    volume_mm3: Optional[float] = None
    surface_area_mm2: Optional[float] = None
    center_of_mass: Optional[Tuple[float, float, float]] = None

    # Part structure
    part_count: int = 0
    part_names: List[str] = field(default_factory=list)
    is_assembly: bool = False

    # Detected features
    has_threads: bool = False
    has_holes: bool = False
    detected_hole_diameters_mm: List[float] = field(default_factory=list)
    symmetry: Optional[str] = None  # axial, bilateral, none

    # Material (from STEP material assignments if present)
    material_name: Optional[str] = None
    material_density: Optional[float] = None
    estimated_weight_kg: Optional[float] = None

    # Child parts (for assemblies)
    children: List["STEPPartData"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "file_format": self.file_format.value,
            "file_size_bytes": self.file_size_bytes,
            "file_hash": self.file_hash,
            "description": self.description,
            "author": self.author,
            "organization": self.organization,
            "schema": self.schema,
            "originating_system": self.originating_system,
            "timestamp": self.timestamp,
            "has_geometry": self.has_geometry,
            "bounding_box": self.bounding_box.to_dict() if self.bounding_box else None,
            "volume_mm3": round(self.volume_mm3, 4) if self.volume_mm3 else None,
            "surface_area_mm2": round(self.surface_area_mm2, 4) if self.surface_area_mm2 else None,
            "center_of_mass": self.center_of_mass,
            "part_count": self.part_count,
            "part_names": self.part_names,
            "is_assembly": self.is_assembly,
            "has_threads": self.has_threads,
            "has_holes": self.has_holes,
            "detected_hole_diameters_mm": self.detected_hole_diameters_mm,
            "material_name": self.material_name,
            "estimated_weight_kg": self.estimated_weight_kg,
            "children": [c.to_dict() for c in self.children],
        }

    def generate_upc_id(self) -> str:
        """Generate a deterministic UPC ID from geometry."""
        if self.bounding_box and self.volume_mm3:
            identity = (
                f"{self.bounding_box.length:.2f}|"
                f"{self.bounding_box.width:.2f}|"
                f"{self.bounding_box.height:.2f}|"
                f"{self.volume_mm3:.2f}"
            )
        else:
            identity = self.file_hash or self.file_path
        return f"UPC-CAD-{hashlib.sha256(identity.encode()).hexdigest()[:12].upper()}"


class STEPParser:
    """
    Parse STEP (ISO 10303) and IGES files for part data.

    Two operating modes:
    - Header-only (no deps): Extracts metadata from file text
    - Full geometry (OCP): Extracts shapes, dimensions, BOM structure

    Usage:
        parser = STEPParser()
        part_data = parser.parse("bracket.step")
        print(part_data.bounding_box)
        print(part_data.volume_mm3)
    """

    def __init__(self):
        self._ocp_available = self._check_ocp()

    @staticmethod
    def _check_ocp() -> bool:
        """Check if OpenCascade Python bindings are available."""
        try:
            import OCP  # noqa: F401
            return True
        except ImportError:
            pass
        try:
            from cadquery import importers  # noqa: F401
            return True
        except ImportError:
            pass
        return False

    def parse(self, file_path: str | Path) -> STEPPartData:
        """
        Parse a STEP or IGES file and extract all available data.

        Args:
            file_path: Path to the CAD file

        Returns:
            STEPPartData with extracted information
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"CAD file not found: {path}")

        # Determine format
        suffix = path.suffix.lower()
        if suffix in (".step", ".stp"):
            fmt = CADFormat.STEP
        elif suffix in (".iges", ".igs"):
            fmt = CADFormat.IGES
        elif suffix == ".stl":
            fmt = CADFormat.STL
        else:
            raise ValueError(f"Unsupported CAD format: {suffix}")

        # Read file
        content = path.read_bytes()
        file_hash = hashlib.sha256(content).hexdigest()

        part_data = STEPPartData(
            file_path=str(path.absolute()),
            file_format=fmt,
            file_size_bytes=len(content),
            file_hash=file_hash,
        )

        # Level 1: Header parsing (always works)
        if fmt == CADFormat.STEP:
            self._parse_step_header(content.decode("utf-8", errors="replace"), part_data)
        elif fmt == CADFormat.IGES:
            self._parse_iges_header(content.decode("utf-8", errors="replace"), part_data)

        # Level 2: Geometry parsing (requires OCP)
        if self._ocp_available and fmt in (CADFormat.STEP, CADFormat.IGES):
            self._parse_geometry(path, part_data)

        return part_data

    def parse_directory(self, dir_path: str | Path, recursive: bool = True) -> List[STEPPartData]:
        """Parse all CAD files in a directory."""
        path = Path(dir_path)
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        extensions = {".step", ".stp", ".iges", ".igs", ".stl"}
        results = []

        pattern = "**/*" if recursive else "*"
        for file_path in path.glob(pattern):
            if file_path.suffix.lower() in extensions and file_path.is_file():
                try:
                    result = self.parse(file_path)
                    results.append(result)
                    logger.info(f"Parsed: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to parse {file_path.name}: {e}")

        return results

    # ---------------------------------------------------------------
    # STEP Header Parsing (pure Python)
    # ---------------------------------------------------------------

    def _parse_step_header(self, content: str, data: STEPPartData) -> None:
        """Parse STEP file header section for metadata."""
        # Extract HEADER section
        header_match = re.search(
            r'HEADER;(.*?)ENDSEC;', content, re.DOTALL | re.IGNORECASE
        )
        if not header_match:
            return

        header = header_match.group(1)

        # FILE_DESCRIPTION
        desc_match = re.search(
            r"FILE_DESCRIPTION\s*\(\s*\(([^)]*)\)", header, re.IGNORECASE
        )
        if desc_match:
            data.description = self._clean_step_string(desc_match.group(1))

        # FILE_NAME - contains filename, timestamp, author, org, etc.
        name_match = re.search(
            r"FILE_NAME\s*\(\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*\(([^)]*)\)\s*,\s*\(([^)]*)\)\s*,\s*'([^']*)'\s*,\s*'([^']*)'",
            header, re.IGNORECASE
        )
        if name_match:
            data.timestamp = name_match.group(2)
            data.author = self._clean_step_string(name_match.group(3))
            data.organization = self._clean_step_string(name_match.group(4))
            preprocessor = name_match.group(5)
            data.originating_system = name_match.group(6)

            # Detect CAD system from preprocessor or originating system
            if not data.originating_system:
                data.originating_system = self._detect_cad_system(preprocessor)

        # FILE_SCHEMA
        schema_match = re.search(
            r"FILE_SCHEMA\s*\(\s*\(([^)]*)\)", header, re.IGNORECASE
        )
        if schema_match:
            data.schema = self._clean_step_string(schema_match.group(1))

        # Count entities to estimate part count
        entity_count = content.count("#")
        product_matches = re.findall(
            r"PRODUCT\s*\(\s*'([^']*)'", content, re.IGNORECASE
        )
        data.part_names = [self._clean_step_string(m) for m in product_matches]
        data.part_count = max(len(data.part_names), 1)
        data.is_assembly = data.part_count > 1

        # Detect threads from entity names
        thread_indicators = ["thread", "helix", "helical"]
        content_lower = content.lower()
        data.has_threads = any(t in content_lower for t in thread_indicators)

        # Look for material assignments
        mat_match = re.search(
            r"MATERIAL_DESIGNATION\s*\(\s*'([^']*)'", content, re.IGNORECASE
        )
        if mat_match:
            data.material_name = self._clean_step_string(mat_match.group(1))

        # Fallback: look for material in product names or descriptions
        if not data.material_name:
            for name in data.part_names + [data.description]:
                detected = self._detect_material(name)
                if detected:
                    data.material_name = detected
                    break

    def _parse_iges_header(self, content: str, data: STEPPartData) -> None:
        """Parse IGES file header for metadata."""
        lines = content.split("\n")

        # IGES has fixed-width records:
        # Columns 1-72: data, Column 73: section letter (S/G/D/P/T)
        start_lines = []
        global_lines = []

        for line in lines:
            if len(line) >= 73:
                section = line[72]
                if section == "S":
                    start_lines.append(line[:72].strip())
                elif section == "G":
                    global_lines.append(line[:72].strip())

        # Start section has description
        if start_lines:
            data.description = " ".join(start_lines)

        # Global section has parameters delimited by commas
        if global_lines:
            global_text = "".join(global_lines)
            params = global_text.split(",")
            if len(params) > 5:
                data.author = params[5].strip().strip("'\"H ")
            if len(params) > 6:
                data.organization = params[6].strip().strip("'\"H ")
            if len(params) > 9:
                data.originating_system = params[9].strip().strip("'\"H ")

        # Count entities
        d_count = sum(1 for line in lines if len(line) >= 73 and line[72] == "D")
        data.part_count = max(d_count // 2, 1)  # D lines come in pairs
        data.is_assembly = data.part_count > 5

    # ---------------------------------------------------------------
    # Geometry Parsing (requires OCP/CadQuery)
    # ---------------------------------------------------------------

    def _parse_geometry(self, file_path: Path, data: STEPPartData) -> None:
        """Parse full 3D geometry using OpenCascade."""
        try:
            self._parse_with_ocp(file_path, data)
        except ImportError:
            try:
                self._parse_with_cadquery(file_path, data)
            except ImportError:
                logger.info("No geometry engine available, skipping geometry parsing")
                return

    def _parse_with_ocp(self, file_path: Path, data: STEPPartData) -> None:
        """Parse geometry using raw OCP bindings."""
        from OCP.STEPControl import STEPControl_Reader
        from OCP.IGESControl import IGESControl_Reader
        from OCP.BRepBndLib import BRepBndLib
        from OCP.Bnd import Bnd_Box
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp
        from OCP.TopExp import TopExp_Explorer
        from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
        from OCP.BRep import BRep_Tool
        from OCP.Geom import Geom_CylindricalSurface

        # Read the file
        if data.file_format == CADFormat.STEP:
            reader = STEPControl_Reader()
            status = reader.ReadFile(str(file_path))
        else:
            reader = IGESControl_Reader()
            status = reader.ReadFile(str(file_path))

        if status != 1:  # IFSelect_RetDone
            logger.warning(f"Failed to read file: {file_path}")
            return

        reader.TransferRoots()
        shape = reader.OneShape()

        data.has_geometry = True

        # Bounding box
        bbox = Bnd_Box()
        BRepBndLib.Add_s(shape, bbox)
        x_min, y_min, z_min, x_max, y_max, z_max = bbox.Get()
        data.bounding_box = BoundingBox(
            x_min=x_min, x_max=x_max,
            y_min=y_min, y_max=y_max,
            z_min=z_min, z_max=z_max,
        )

        # Volume and surface area
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(shape, props)
        data.volume_mm3 = props.Mass()

        com = props.CentreOfMass()
        data.center_of_mass = (com.X(), com.Y(), com.Z())

        surface_props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(shape, surface_props)
        data.surface_area_mm2 = surface_props.Mass()

        # Estimate weight if material density is known
        if data.material_density and data.volume_mm3:
            volume_cm3 = data.volume_mm3 / 1000.0
            data.estimated_weight_kg = volume_cm3 * data.material_density / 1000.0

        # Detect cylindrical holes
        hole_diameters = set()
        explorer = TopExp_Explorer(shape, TopAbs_FACE)
        while explorer.More():
            face = explorer.Current()
            surface = BRep_Tool.Surface_s(face)
            if isinstance(surface, Geom_CylindricalSurface):
                radius = surface.Radius()
                diameter = radius * 2
                if diameter < 200:  # Likely a hole, not a large cylinder
                    hole_diameters.add(round(diameter, 2))
                    data.has_holes = True
            explorer.Next()

        data.detected_hole_diameters_mm = sorted(hole_diameters)

    def _parse_with_cadquery(self, file_path: Path, data: STEPPartData) -> None:
        """Parse geometry using CadQuery (higher-level API)."""
        import cadquery as cq

        if data.file_format == CADFormat.STEP:
            result = cq.importers.importStep(str(file_path))
        elif data.file_format == CADFormat.IGES:
            # CadQuery doesn't directly support IGES, try through OCP
            raise ImportError("CadQuery does not support IGES import directly")
        else:
            return

        data.has_geometry = True

        # Bounding box
        bb = result.val().BoundingBox()
        data.bounding_box = BoundingBox(
            x_min=bb.xmin, x_max=bb.xmax,
            y_min=bb.ymin, y_max=bb.ymax,
            z_min=bb.zmin, z_max=bb.zmax,
        )

        # Volume
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp

        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(result.val().wrapped, props)
        data.volume_mm3 = props.Mass()

        com = props.CentreOfMass()
        data.center_of_mass = (com.X(), com.Y(), com.Z())

        surface_props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(result.val().wrapped, surface_props)
        data.surface_area_mm2 = surface_props.Mass()

    # ---------------------------------------------------------------
    # Utility Methods
    # ---------------------------------------------------------------

    @staticmethod
    def _clean_step_string(s: str) -> str:
        """Clean STEP string values."""
        s = s.strip()
        # Remove surrounding quotes
        s = s.strip("'\"")
        # Remove STEP string delimiters
        s = re.sub(r"^'|'$", "", s)
        return s.strip()

    @staticmethod
    def _detect_cad_system(preprocessor_str: str) -> str:
        """Detect originating CAD system from preprocessor string."""
        p = preprocessor_str.lower()
        systems = {
            "solidworks": "SolidWorks",
            "catia": "CATIA",
            "creo": "Creo / Pro/ENGINEER",
            "pro/engineer": "Creo / Pro/ENGINEER",
            "nx": "Siemens NX",
            "inventor": "Autodesk Inventor",
            "fusion": "Autodesk Fusion 360",
            "freecad": "FreeCAD",
            "onshape": "Onshape",
            "rhino": "Rhino / Grasshopper",
            "autocad": "AutoCAD",
            "solid edge": "Solid Edge",
            "alibre": "Alibre Design",
            "spaceclaim": "SpaceClaim",
        }
        for key, name in systems.items():
            if key in p:
                return name
        return preprocessor_str

    @staticmethod
    def _detect_material(text: str) -> Optional[str]:
        """Try to detect material from text strings."""
        if not text:
            return None
        text_lower = text.lower()
        materials = {
            "aluminum": "Aluminum",
            "aluminium": "Aluminum",
            "6061": "Aluminum 6061",
            "7075": "Aluminum 7075",
            "steel": "Steel",
            "stainless": "Stainless Steel",
            "304": "304 Stainless Steel",
            "316": "316 Stainless Steel",
            "titanium": "Titanium",
            "ti-6al-4v": "Titanium Ti-6Al-4V",
            "brass": "Brass",
            "bronze": "Bronze",
            "copper": "Copper",
            "nylon": "Nylon",
            "delrin": "Delrin / Acetal",
            "abs": "ABS",
            "polycarbonate": "Polycarbonate",
            "peek": "PEEK",
            "ptfe": "PTFE",
            "cast iron": "Cast Iron",
            "carbon fiber": "Carbon Fiber",
        }
        for key, name in materials.items():
            if key in text_lower:
                return name
        return None

    @property
    def geometry_available(self) -> bool:
        """Whether full geometry parsing is available."""
        return self._ocp_available
