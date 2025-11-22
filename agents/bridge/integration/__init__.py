"""External integration layer - connects UPC to the world's systems."""

from .supplier_gateway import SupplierGateway
from .cad_bridge import CADBridge
from .erp_connector import ERPConnector
from .iot_protocol import IoTProtocol

__all__ = ['SupplierGateway', 'CADBridge', 'ERPConnector', 'IoTProtocol']
