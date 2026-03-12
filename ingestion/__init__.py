"""
Universal Parts Ingestion System
=================================
"Every part enters through these gates."

The ingestion layer handles all data input into the Universal Parts
Consciousness — from CAD files to supplier APIs to manual CSV imports.
"""

from .parsers.step_parser import STEPParser, STEPPartData
from .parsers.csv_parser import CSVPartImporter
from .parsers.assembly_parser import AssemblyParser, AssemblyIngestResult
from .connectors.base import DataSourceConnector, ConnectorRegistry
from .ingest import UniversalIngestor

__all__ = [
    "STEPParser",
    "STEPPartData",
    "CSVPartImporter",
    "AssemblyParser",
    "AssemblyIngestResult",
    "DataSourceConnector",
    "ConnectorRegistry",
    "UniversalIngestor",
]
