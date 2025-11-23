"""
CNC Retrofit Engine - Find retrofit solutions for aging CNC equipment

Handles:
- Monitor/CRT replacements
- Control system retrofits
- Spindle drive upgrades
- Communication interface updates
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class RetrofitComplexity(Enum):
    """Complexity levels for retrofit installations"""
    SIMPLE = "simple"          # <4 hours, minimal wiring
    MODERATE = "moderate"      # 4-16 hours, some wiring changes
    COMPLEX = "complex"        # 16-40 hours, significant modifications
    MAJOR = "major"            # >40 hours, complete overhaul


class ControlGeneration(Enum):
    """CNC control generations"""
    LEGACY_NC = "legacy_nc"      # Pre-1980, tape-based
    EARLY_CNC = "early_cnc"      # 1980-1990, basic CNC
    MATURE_CNC = "mature_cnc"    # 1990-2005, established platforms
    MODERN_CNC = "modern_cnc"    # 2005+, PC-based, networking


@dataclass
class RetrofitVendor:
    """Retrofit solution vendor information"""
    name: str
    website: str
    phone: Optional[str]
    specialties: List[str]
    brands_supported: List[str]
    years_in_business: int
    warranty_months: int
    installation_support: bool
    remote_support: bool


@dataclass
class MonitorRetrofitSpec:
    """Specification for CRT-to-LCD monitor retrofit"""
    original_crt_size: str           # "9-inch", "12-inch", "14-inch"
    original_signal_type: str        # "Composite", "RGB", "VGA"
    replacement_lcd_size: str
    resolution: str
    mounting_type: str               # "Direct", "Adapter plate", "Custom"
    video_converter_needed: bool
    power_requirements: str
    brightness_cd_m2: int
    viewing_angle_degrees: int
    compatible_controls: List[str]


@dataclass
class ControlRetrofitSpec:
    """Specification for complete CNC control retrofit"""
    retrofit_control: str
    manufacturer: str
    axes_supported: int
    spindle_channels: int
    display_size_inches: float
    touchscreen: bool
    usb_support: bool
    ethernet_support: bool
    cad_import: List[str]            # ["DXF", "DWG", "STEP", etc.]
    conversational_programming: bool
    macro_support: bool
    probing_support: bool
    tool_changer_support: bool
    rigid_tapping: bool
    includes_drives: bool
    includes_motors: bool
    servo_drive_options: List[str]


class CNCRetrofitEngine:
    """
    Engine for finding CNC retrofit solutions

    Covers:
    - Fanuc (0, 6, 10, 11, 15, 16, 18, 21 series)
    - Siemens (Sinumerik 3, 810, 820, 840, 880)
    - Mazak (Mazatrol T, M, T-Plus, M-Plus)
    - Haas (Classic, NGC)
    - Okuma (OSP-U, OSP-P)
    - Mitsubishi (Meldas, M60, M64, M70)
    """

    def __init__(self):
        self.vendors = self._initialize_vendors()
        self.monitor_retrofits = self._initialize_monitor_retrofits()
        self.control_retrofits = self._initialize_control_retrofits()

    def _initialize_vendors(self) -> Dict[str, RetrofitVendor]:
        """Initialize retrofit vendor database"""
        return {
            "cncmonitors": RetrofitVendor(
                name="CNC Monitors",
                website="https://www.cncmonitors.com",
                phone="1-800-CNC-PARTS",
                specialties=["Monitor replacement", "Video converters"],
                brands_supported=["Fanuc", "Mazak", "Siemens", "Okuma", "Haas"],
                years_in_business=25,
                warranty_months=24,
                installation_support=False,
                remote_support=True
            ),
            "centroid": RetrofitVendor(
                name="Centroid CNC",
                website="https://www.centroidcnc.com",
                phone="1-814-353-9256",
                specialties=["Complete control retrofits", "DIY kits"],
                brands_supported=["Universal - any machine"],
                years_in_business=40,
                warranty_months=12,
                installation_support=True,
                remote_support=True
            ),
            "siemens": RetrofitVendor(
                name="Siemens CNC",
                website="https://www.siemens.com/cnc",
                phone=None,
                specialties=["OEM upgrades", "Sinumerik modernization"],
                brands_supported=["Siemens"],
                years_in_business=50,
                warranty_months=12,
                installation_support=True,
                remote_support=True
            ),
            "fanuc_america": RetrofitVendor(
                name="FANUC America",
                website="https://www.fanucamerica.com",
                phone="1-888-326-8287",
                specialties=["OEM parts", "Control upgrades"],
                brands_supported=["Fanuc"],
                years_in_business=40,
                warranty_months=12,
                installation_support=True,
                remote_support=True
            ),
            "mesa_electronics": RetrofitVendor(
                name="Mesa Electronics",
                website="https://www.mesanet.com",
                phone="1-510-223-9272",
                specialties=["Motion control cards", "FPGA solutions"],
                brands_supported=["Universal - LinuxCNC/Mach"],
                years_in_business=30,
                warranty_months=12,
                installation_support=False,
                remote_support=False
            ),
        }

    def _initialize_monitor_retrofits(self) -> Dict[str, List[MonitorRetrofitSpec]]:
        """Initialize monitor retrofit solutions"""
        return {
            "fanuc_9inch": [
                MonitorRetrofitSpec(
                    original_crt_size="9-inch",
                    original_signal_type="Composite",
                    replacement_lcd_size="10.4-inch",
                    resolution="800x600",
                    mounting_type="Direct",
                    video_converter_needed=False,
                    power_requirements="5V/12V from original supply",
                    brightness_cd_m2=400,
                    viewing_angle_degrees=160,
                    compatible_controls=["Fanuc 0", "Fanuc 6", "Fanuc 10", "Fanuc 11"]
                ),
            ],
            "fanuc_12inch": [
                MonitorRetrofitSpec(
                    original_crt_size="12-inch",
                    original_signal_type="RGB",
                    replacement_lcd_size="12.1-inch",
                    resolution="1024x768",
                    mounting_type="Adapter plate",
                    video_converter_needed=True,
                    power_requirements="12V DC",
                    brightness_cd_m2=500,
                    viewing_angle_degrees=170,
                    compatible_controls=["Fanuc 15", "Fanuc 16", "Fanuc 18", "Fanuc 21"]
                ),
            ],
            "siemens_crt": [
                MonitorRetrofitSpec(
                    original_crt_size="14-inch",
                    original_signal_type="RGB TTL",
                    replacement_lcd_size="15-inch",
                    resolution="1024x768",
                    mounting_type="Custom frame",
                    video_converter_needed=True,
                    power_requirements="24V DC",
                    brightness_cd_m2=450,
                    viewing_angle_degrees=160,
                    compatible_controls=["Sinumerik 810", "Sinumerik 820", "Sinumerik 850"]
                ),
            ],
            "mazak_crt": [
                MonitorRetrofitSpec(
                    original_crt_size="14-inch",
                    original_signal_type="VGA",
                    replacement_lcd_size="15-inch",
                    resolution="1024x768",
                    mounting_type="Direct",
                    video_converter_needed=False,
                    power_requirements="12V DC",
                    brightness_cd_m2=500,
                    viewing_angle_degrees=170,
                    compatible_controls=["Mazatrol T-Plus", "Mazatrol M-Plus", "Mazatrol T32"]
                ),
            ],
        }

    def _initialize_control_retrofits(self) -> Dict[str, ControlRetrofitSpec]:
        """Initialize complete control retrofit solutions"""
        return {
            "centroid_acorn": ControlRetrofitSpec(
                retrofit_control="Centroid Acorn",
                manufacturer="Centroid",
                axes_supported=4,
                spindle_channels=1,
                display_size_inches=15.6,
                touchscreen=True,
                usb_support=True,
                ethernet_support=True,
                cad_import=["DXF"],
                conversational_programming=True,
                macro_support=True,
                probing_support=True,
                tool_changer_support=True,
                rigid_tapping=True,
                includes_drives=False,
                includes_motors=False,
                servo_drive_options=["Use existing", "DMM Tech", "Clearpath"]
            ),
            "centroid_m400": ControlRetrofitSpec(
                retrofit_control="Centroid M400",
                manufacturer="Centroid",
                axes_supported=6,
                spindle_channels=2,
                display_size_inches=15.6,
                touchscreen=True,
                usb_support=True,
                ethernet_support=True,
                cad_import=["DXF", "G-code"],
                conversational_programming=True,
                macro_support=True,
                probing_support=True,
                tool_changer_support=True,
                rigid_tapping=True,
                includes_drives=True,
                includes_motors=False,
                servo_drive_options=["Centroid MPU11"]
            ),
            "mach4_industrial": ControlRetrofitSpec(
                retrofit_control="Mach4 Industrial",
                manufacturer="Newfangled Solutions",
                axes_supported=6,
                spindle_channels=2,
                display_size_inches=21.5,
                touchscreen=True,
                usb_support=True,
                ethernet_support=True,
                cad_import=["DXF", "G-code"],
                conversational_programming=False,
                macro_support=True,
                probing_support=True,
                tool_changer_support=True,
                rigid_tapping=True,
                includes_drives=False,
                includes_motors=False,
                servo_drive_options=["Mesa/Ethernet", "Galil", "PMDX"]
            ),
            "linuxcnc": ControlRetrofitSpec(
                retrofit_control="LinuxCNC",
                manufacturer="Open Source",
                axes_supported=9,
                spindle_channels=4,
                display_size_inches=21.5,
                touchscreen=True,
                usb_support=True,
                ethernet_support=True,
                cad_import=["DXF", "G-code", "STEP (via CAM)"],
                conversational_programming=False,
                macro_support=True,
                probing_support=True,
                tool_changer_support=True,
                rigid_tapping=True,
                includes_drives=False,
                includes_motors=False,
                servo_drive_options=["Mesa 7i96", "Mesa 7i92", "Parallel port"]
            ),
        }

    def find_monitor_retrofit(
        self,
        control_brand: str,
        control_model: str,
        crt_size: Optional[str] = None
    ) -> List[MonitorRetrofitSpec]:
        """
        Find LCD monitor retrofit for CRT-based CNC control.

        Args:
            control_brand: Fanuc, Siemens, Mazak, etc.
            control_model: Specific model number
            crt_size: Original CRT size if known

        Returns:
            List of compatible monitor retrofits
        """
        results = []
        brand_lower = control_brand.lower()
        model_lower = control_model.lower()

        # Fanuc
        if "fanuc" in brand_lower:
            # Early Fanuc (0, 6, 10, 11) use 9-inch
            if any(m in model_lower for m in ["0m", "0t", "6m", "6t", "10m", "10t", "11m", "11t"]):
                results.extend(self.monitor_retrofits.get("fanuc_9inch", []))
            # Later Fanuc (15, 16, 18, 21) use 12-inch
            elif any(m in model_lower for m in ["15", "16", "18", "21"]):
                results.extend(self.monitor_retrofits.get("fanuc_12inch", []))

        # Siemens
        elif "siemens" in brand_lower or "sinumerik" in brand_lower:
            results.extend(self.monitor_retrofits.get("siemens_crt", []))

        # Mazak
        elif "mazak" in brand_lower or "mazatrol" in brand_lower:
            results.extend(self.monitor_retrofits.get("mazak_crt", []))

        return results

    def find_control_retrofit(
        self,
        machine_type: str,
        axes_needed: int,
        budget_usd: Optional[float] = None,
        keep_existing_drives: bool = True
    ) -> List[Tuple[ControlRetrofitSpec, float]]:
        """
        Find complete control retrofit solutions.

        Args:
            machine_type: "mill", "lathe", "router"
            axes_needed: Number of axes required
            budget_usd: Maximum budget
            keep_existing_drives: Whether to reuse existing servo drives

        Returns:
            List of (retrofit_spec, estimated_cost) tuples
        """
        results = []

        for key, spec in self.control_retrofits.items():
            if spec.axes_supported >= axes_needed:
                # Estimate cost based on options
                if "acorn" in key:
                    base_cost = 4000
                elif "m400" in key:
                    base_cost = 8500
                elif "mach4" in key:
                    base_cost = 5000
                elif "linuxcnc" in key:
                    base_cost = 2000  # Open source + hardware
                else:
                    base_cost = 10000

                # Add drive costs if not included and not keeping existing
                if not spec.includes_drives and not keep_existing_drives:
                    base_cost += axes_needed * 1500  # ~$1500/axis for new drives

                # Budget filter
                if budget_usd and base_cost > budget_usd:
                    continue

                results.append((spec, base_cost))

        # Sort by cost
        results.sort(key=lambda x: x[1])
        return results

    def estimate_retrofit_time(
        self,
        retrofit_type: str,
        machine_complexity: str = "standard"
    ) -> Dict[str, float]:
        """
        Estimate installation time for different retrofit types.

        Returns dict with hours for each phase.
        """
        # Base times in hours
        base_times = {
            "monitor_only": {
                "removal": 1,
                "mounting": 2,
                "wiring": 1,
                "testing": 1,
                "total": 5
            },
            "control_reuse_drives": {
                "removal": 8,
                "mounting": 8,
                "wiring": 16,
                "configuration": 8,
                "testing": 8,
                "total": 48
            },
            "control_new_drives": {
                "removal": 8,
                "mounting": 16,
                "wiring": 24,
                "configuration": 16,
                "testing": 16,
                "total": 80
            },
            "complete_rebuild": {
                "removal": 16,
                "mounting": 24,
                "wiring": 40,
                "configuration": 24,
                "testing": 24,
                "commissioning": 16,
                "total": 144
            }
        }

        times = base_times.get(retrofit_type, base_times["control_reuse_drives"]).copy()

        # Complexity multiplier
        multipliers = {
            "simple": 0.75,
            "standard": 1.0,
            "complex": 1.5,
            "very_complex": 2.0
        }
        mult = multipliers.get(machine_complexity, 1.0)

        return {k: v * mult for k, v in times.items()}

    def get_vendor_for_brand(self, cnc_brand: str) -> List[RetrofitVendor]:
        """Get recommended vendors for a CNC brand"""
        results = []
        brand_lower = cnc_brand.lower()

        for vendor_id, vendor in self.vendors.items():
            if brand_lower in [b.lower() for b in vendor.brands_supported]:
                results.append(vendor)
            elif "universal" in " ".join(vendor.brands_supported).lower():
                results.append(vendor)

        return results
