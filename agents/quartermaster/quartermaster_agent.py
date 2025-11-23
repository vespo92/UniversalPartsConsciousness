"""
Agent_19: QUARTERMASTER - Supply Chain & Sourcing Intelligence

The answer to "where can I get this part?"
Tracks inventory across distributors, detects counterfeits,
predicts lead times, and optimizes sourcing decisions.

Domains:
- Distributor inventory (McMaster, Fastenal, Grainger, DigiKey)
- Direct manufacturer sourcing
- Counterfeit detection
- Lead time tracking
- Cost optimization
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime, date
from decimal import Decimal


class SupplierTier(Enum):
    """Supplier classification by reliability and authorization"""
    MANUFACTURER = "manufacturer"        # Direct from OEM
    AUTHORIZED = "authorized"            # Authorized distributor
    FRANCHISE = "franchise"              # National distributor
    INDEPENDENT = "independent"          # Independent distributor
    BROKER = "broker"                    # Parts broker
    MARKETPLACE = "marketplace"          # eBay, AliExpress, etc.
    UNKNOWN = "unknown"


class CounterfeitRisk(Enum):
    """Risk level for counterfeit parts"""
    MINIMAL = "minimal"     # Authorized source, traceable
    LOW = "low"             # Reputable distributor
    MEDIUM = "medium"       # Independent, some verification
    HIGH = "high"           # Marketplace, price anomalies
    CRITICAL = "critical"   # Multiple red flags


@dataclass
class SupplierProfile:
    """Profile of a parts supplier"""
    name: str
    tier: SupplierTier
    website: str
    locations: List[str]
    specializations: List[str]  # ["fasteners", "bearings", "electronics"]

    # Ratings
    reliability_rating: float   # 0-1 based on historical data
    quality_rating: float       # 0-1 based on returns/complaints
    delivery_rating: float      # 0-1 based on on-time delivery

    # Capabilities
    minimum_order: Optional[Decimal]
    ships_international: bool
    same_day_shipping: bool
    accepts_credit_card: bool

    # Certifications
    certifications: List[str]   # ["ISO 9001", "AS9120", "ITAR"]
    authorized_for: List[str]   # Brands they're authorized for


@dataclass
class InventoryResult:
    """Result of an inventory search"""
    supplier: str
    supplier_tier: SupplierTier
    part_number: str
    description: str
    stock_quantity: int
    unit_price: Decimal
    price_breaks: Dict[int, Decimal]  # {qty: price_per_unit}
    lead_time_days: int
    shipping_estimate: Decimal
    last_updated: datetime

    @property
    def total_for_qty(self) -> Decimal:
        """Calculate total cost for quantity of 1"""
        return self.unit_price + self.shipping_estimate


@dataclass
class CounterfeitAssessment:
    """Assessment of counterfeit risk for a part/supplier"""
    part_number: str
    supplier: str
    risk_level: CounterfeitRisk
    risk_score: float  # 0-1
    red_flags: List[str]
    green_flags: List[str]
    genuine_price_range: Tuple[Decimal, Decimal]
    offered_price: Decimal
    recommended_sources: List[str]
    verification_steps: List[str]


@dataclass
class LeadTimePrediction:
    """Predicted lead time for a part"""
    part_type: str
    estimated_days_min: int
    estimated_days_max: int
    confidence: float
    factors: List[str]  # Factors affecting lead time
    rush_available: bool
    rush_premium_percent: Optional[int]
    rush_lead_days: Optional[int]
    recommended_suppliers: List[str]


@dataclass
class SourcingOptimization:
    """Optimized sourcing strategy for a BOM"""
    strategy: str
    total_cost: Decimal
    total_lead_days: int
    supplier_allocation: List[Dict]
    alternative_strategies: List[Dict]
    warnings: List[str]


class QuartermasterAgent:
    """
    Agent_19: QUARTERMASTER - Supply Chain & Sourcing Intelligence

    Core responsibilities:
    1. Multi-distributor inventory search
    2. Counterfeit risk assessment
    3. Lead time prediction
    4. Sourcing optimization
    5. Supplier qualification
    """

    def __init__(self):
        self.suppliers = self._initialize_suppliers()
        self.counterfeit_indicators = self._initialize_counterfeit_db()
        self.price_history = {}  # Part -> historical prices

    def _initialize_suppliers(self) -> Dict[str, SupplierProfile]:
        """Initialize known supplier database"""
        return {
            "mcmaster": SupplierProfile(
                name="McMaster-Carr",
                tier=SupplierTier.FRANCHISE,
                website="mcmaster.com",
                locations=["USA"],
                specializations=["fasteners", "raw_materials", "tools", "hardware"],
                reliability_rating=0.99,
                quality_rating=0.98,
                delivery_rating=0.99,
                minimum_order=None,
                ships_international=True,
                same_day_shipping=True,
                accepts_credit_card=True,
                certifications=["ISO 9001"],
                authorized_for=[]
            ),
            "fastenal": SupplierProfile(
                name="Fastenal",
                tier=SupplierTier.FRANCHISE,
                website="fastenal.com",
                locations=["USA", "Canada", "Mexico", "Europe"],
                specializations=["fasteners", "safety", "tools"],
                reliability_rating=0.95,
                quality_rating=0.94,
                delivery_rating=0.92,
                minimum_order=Decimal("0"),
                ships_international=True,
                same_day_shipping=True,
                accepts_credit_card=True,
                certifications=["ISO 9001", "AS9120"],
                authorized_for=[]
            ),
            "digikey": SupplierProfile(
                name="DigiKey",
                tier=SupplierTier.AUTHORIZED,
                website="digikey.com",
                locations=["USA"],
                specializations=["electronics", "semiconductors", "passives"],
                reliability_rating=0.98,
                quality_rating=0.99,
                delivery_rating=0.97,
                minimum_order=None,
                ships_international=True,
                same_day_shipping=True,
                accepts_credit_card=True,
                certifications=["ISO 9001", "AS9120", "ITAR"],
                authorized_for=["TI", "Analog Devices", "Microchip", "STM"]
            ),
            "motion_industries": SupplierProfile(
                name="Motion Industries",
                tier=SupplierTier.AUTHORIZED,
                website="motionindustries.com",
                locations=["USA", "Canada"],
                specializations=["bearings", "power_transmission", "hydraulics"],
                reliability_rating=0.96,
                quality_rating=0.97,
                delivery_rating=0.93,
                minimum_order=Decimal("25"),
                ships_international=False,
                same_day_shipping=True,
                accepts_credit_card=True,
                certifications=["ISO 9001"],
                authorized_for=["SKF", "NSK", "Timken", "FAG"]
            ),
            "grainger": SupplierProfile(
                name="Grainger",
                tier=SupplierTier.FRANCHISE,
                website="grainger.com",
                locations=["USA", "Canada", "Mexico"],
                specializations=["MRO", "safety", "tools", "electrical"],
                reliability_rating=0.94,
                quality_rating=0.93,
                delivery_rating=0.91,
                minimum_order=None,
                ships_international=False,
                same_day_shipping=True,
                accepts_credit_card=True,
                certifications=["ISO 9001"],
                authorized_for=[]
            ),
        }

    def _initialize_counterfeit_db(self) -> Dict:
        """Initialize counterfeit detection patterns"""
        return {
            "high_risk_categories": [
                "bearings",
                "semiconductors",
                "aviation_fasteners",
                "automotive_sensors",
                "safety_equipment"
            ],
            "price_deviation_threshold": 0.40,  # 40% below market = suspicious
            "red_flag_phrases": [
                "oem quality",
                "same as original",
                "factory direct",
                "bulk lot",
            ],
            "trusted_sources": {
                "bearings": ["Motion Industries", "Applied Industrial", "Kaman"],
                "semiconductors": ["DigiKey", "Mouser", "Arrow", "Avnet"],
                "fasteners": ["McMaster-Carr", "Fastenal", "MSC Industrial"],
            }
        }

    def search_inventory(
        self,
        part_spec: str,
        quantity: int,
        location: str,
        max_lead_days: int = 5
    ) -> List[InventoryResult]:
        """
        Search multiple distributors for part availability.

        Args:
            part_spec: Part specification (e.g., "M8x1.25-10.9 SHCS x 30mm")
            quantity: Required quantity
            location: Shipping destination
            max_lead_days: Maximum acceptable lead time

        Returns:
            List of InventoryResult sorted by best match
        """
        # In production, this would query actual distributor APIs
        # Demo implementation with mock data
        results = []

        # Simulate McMaster result
        results.append(InventoryResult(
            supplier="McMaster-Carr",
            supplier_tier=SupplierTier.FRANCHISE,
            part_number="91290A428",
            description=f"{part_spec}",
            stock_quantity=5000,
            unit_price=Decimal("0.45"),
            price_breaks={
                1: Decimal("0.55"),
                50: Decimal("0.48"),
                100: Decimal("0.45"),
                500: Decimal("0.38")
            },
            lead_time_days=1,
            shipping_estimate=Decimal("8.50"),
            last_updated=datetime.now()
        ))

        # Simulate Fastenal result
        results.append(InventoryResult(
            supplier="Fastenal",
            supplier_tier=SupplierTier.FRANCHISE,
            part_number="11120748",
            description=f"{part_spec}",
            stock_quantity=2000,
            unit_price=Decimal("0.38"),
            price_breaks={
                1: Decimal("0.45"),
                100: Decimal("0.38"),
                1000: Decimal("0.32")
            },
            lead_time_days=2,
            shipping_estimate=Decimal("12.00"),
            last_updated=datetime.now()
        ))

        # Filter by lead time and sort by total cost
        results = [r for r in results if r.lead_time_days <= max_lead_days]
        results.sort(key=lambda x: x.total_for_qty)

        return results

    def assess_counterfeit_risk(
        self,
        part: str,
        supplier: str,
        offered_price: Decimal
    ) -> CounterfeitAssessment:
        """
        Assess counterfeit risk for a part from a specific supplier.

        Args:
            part: Part number or description
            supplier: Supplier name
            offered_price: Price being offered

        Returns:
            CounterfeitAssessment with risk evaluation
        """
        red_flags = []
        green_flags = []

        # Check if supplier is known
        supplier_key = supplier.lower().replace(" ", "_").replace("-", "_")
        known_supplier = self.suppliers.get(supplier_key)

        if known_supplier:
            green_flags.append(f"Known supplier: {known_supplier.tier.value}")
            if known_supplier.tier in [SupplierTier.MANUFACTURER, SupplierTier.AUTHORIZED]:
                green_flags.append("Authorized/manufacturer tier")
        else:
            red_flags.append("Unknown supplier - not in verified database")

        # Estimate genuine price range (simplified)
        # In production, this would query price history
        genuine_min = offered_price * Decimal("1.2")
        genuine_max = offered_price * Decimal("2.5")

        # Check price deviation
        if offered_price < genuine_min * Decimal("0.6"):
            red_flags.append(f"Price {offered_price} is suspiciously low")

        # Check for high-risk category
        part_lower = part.lower()
        for category in self.counterfeit_indicators["high_risk_categories"]:
            if category in part_lower:
                red_flags.append(f"Part category '{category}' is high-risk for counterfeits")
                break

        # Calculate risk score
        risk_score = len(red_flags) * 0.25 - len(green_flags) * 0.1
        risk_score = max(0, min(1, risk_score + 0.3))  # Baseline 0.3

        # Determine risk level
        if risk_score < 0.2:
            risk_level = CounterfeitRisk.MINIMAL
        elif risk_score < 0.4:
            risk_level = CounterfeitRisk.LOW
        elif risk_score < 0.6:
            risk_level = CounterfeitRisk.MEDIUM
        elif risk_score < 0.8:
            risk_level = CounterfeitRisk.HIGH
        else:
            risk_level = CounterfeitRisk.CRITICAL

        # Get recommended sources
        recommended = []
        for category, sources in self.counterfeit_indicators["trusted_sources"].items():
            if category in part_lower:
                recommended.extend(sources)
                break
        if not recommended:
            recommended = ["McMaster-Carr", "Fastenal", "Grainger"]

        return CounterfeitAssessment(
            part_number=part,
            supplier=supplier,
            risk_level=risk_level,
            risk_score=risk_score,
            red_flags=red_flags,
            green_flags=green_flags,
            genuine_price_range=(genuine_min, genuine_max),
            offered_price=offered_price,
            recommended_sources=recommended,
            verification_steps=[
                "Verify supplier authorization with manufacturer",
                "Request certificate of conformance",
                "Check part markings match OEM specifications",
                "Compare weight and finish to known genuine parts"
            ]
        )

    def predict_lead_time(
        self,
        part_type: str,
        quantity: int,
        customization: Optional[str] = None
    ) -> LeadTimePrediction:
        """
        Predict lead time for a part, especially custom items.

        Args:
            part_type: Type of part (e.g., "CNC machined bracket")
            quantity: Quantity needed
            customization: Description of custom requirements

        Returns:
            LeadTimePrediction with estimates and factors
        """
        # Base lead times by part type
        base_times = {
            "fastener_standard": (1, 3),
            "fastener_special": (5, 14),
            "bearing": (1, 5),
            "cnc_machined": (7, 21),
            "casting": (21, 42),
            "forging": (28, 56),
            "injection_molded": (14, 35),
            "sheet_metal": (5, 14),
            "pcb": (5, 14),
            "cable_assembly": (7, 21),
        }

        # Determine base time
        part_lower = part_type.lower()
        base = (7, 14)  # Default
        for key, times in base_times.items():
            if key.replace("_", " ") in part_lower or key.replace("_", "") in part_lower:
                base = times
                break

        # Adjust for quantity
        qty_factor = 1.0
        if quantity > 1000:
            qty_factor = 1.5
        elif quantity > 100:
            qty_factor = 1.2

        # Adjust for customization
        custom_factor = 1.0
        factors = []
        if customization:
            factors.append("Custom work required")
            if "anodized" in customization.lower() or "plated" in customization.lower():
                custom_factor += 0.3
                factors.append("Surface treatment adds 3-5 days")
            if "tight tolerance" in customization.lower():
                custom_factor += 0.2
                factors.append("Tight tolerances require slower machining")

        min_days = int(base[0] * qty_factor * custom_factor)
        max_days = int(base[1] * qty_factor * custom_factor)

        return LeadTimePrediction(
            part_type=part_type,
            estimated_days_min=min_days,
            estimated_days_max=max_days,
            confidence=0.8,
            factors=factors or ["Standard production time"],
            rush_available=True,
            rush_premium_percent=50,
            rush_lead_days=max(3, min_days // 2),
            recommended_suppliers=["Xometry", "Protolabs", "Fictiv"]
        )

    def optimize_sourcing(
        self,
        bom: List[Dict],
        priorities: Dict
    ) -> SourcingOptimization:
        """
        Optimize sourcing across a bill of materials.

        Args:
            bom: List of {"part": str, "qty": int, "spec": str}
            priorities: {"cost": 0-1, "speed": 0-1, "quality": 0-1}

        Returns:
            SourcingOptimization with recommended strategy
        """
        # Normalize priorities
        total = sum(priorities.values())
        cost_weight = priorities.get("cost", 0.33) / total
        speed_weight = priorities.get("speed", 0.33) / total
        quality_weight = priorities.get("quality", 0.34) / total

        allocations = []
        total_cost = Decimal("0")
        max_lead = 0
        warnings = []

        for item in bom:
            # Search for each item
            results = self.search_inventory(
                item.get("spec", item["part"]),
                item["qty"],
                "USA",
                max_lead_days=30
            )

            if results:
                # Score each result
                scored = []
                for r in results:
                    cost_score = 1 - (float(r.unit_price) / 2)  # Normalize
                    speed_score = 1 - (r.lead_time_days / 30)
                    quality_score = self.suppliers.get(
                        r.supplier.lower().replace("-", "_").replace(" ", "_"),
                        SupplierProfile("", SupplierTier.UNKNOWN, "", [], [], 0.5, 0.5, 0.5, None, False, False, False, [], [])
                    ).quality_rating

                    total_score = (
                        cost_score * cost_weight +
                        speed_score * speed_weight +
                        quality_score * quality_weight
                    )
                    scored.append((total_score, r))

                # Pick best
                scored.sort(reverse=True)
                best = scored[0][1]

                allocations.append({
                    "part": item["part"],
                    "qty": item["qty"],
                    "supplier": best.supplier,
                    "unit_price": float(best.unit_price),
                    "lead_days": best.lead_time_days
                })

                total_cost += best.unit_price * item["qty"]
                max_lead = max(max_lead, best.lead_time_days)
            else:
                warnings.append(f"No source found for {item['part']}")

        return SourcingOptimization(
            strategy="Multi-supplier optimization" if len(set(a["supplier"] for a in allocations)) > 1 else "Single supplier",
            total_cost=total_cost,
            total_lead_days=max_lead,
            supplier_allocation=allocations,
            alternative_strategies=[
                {
                    "name": "Single supplier (McMaster)",
                    "pros": "Single shipment, simpler receiving",
                    "cons": "May not have all items, potentially higher cost"
                }
            ],
            warnings=warnings
        )


# Demo usage
if __name__ == "__main__":
    agent = QuartermasterAgent()

    print("=" * 60)
    print("Agent_19: QUARTERMASTER - Supply Chain Intelligence")
    print("=" * 60)

    # Test inventory search
    print("\n--- Inventory Search ---")
    results = agent.search_inventory(
        "M8x1.25-10.9 Socket Head Cap Screw x 30mm",
        quantity=100,
        location="California",
        max_lead_days=3
    )
    for r in results:
        print(f"\n{r.supplier}:")
        print(f"  Part#: {r.part_number}")
        print(f"  Stock: {r.stock_quantity}")
        print(f"  Price: ${r.unit_price}/ea")
        print(f"  Lead time: {r.lead_time_days} day(s)")

    # Test counterfeit assessment
    print("\n--- Counterfeit Risk Assessment ---")
    assessment = agent.assess_counterfeit_risk(
        "SKF 6205-2RS bearing",
        "AliExpress seller best_bearings_888",
        Decimal("2.50")
    )
    print(f"Part: {assessment.part_number}")
    print(f"Supplier: {assessment.supplier}")
    print(f"Risk Level: {assessment.risk_level.value}")
    print(f"Risk Score: {assessment.risk_score:.0%}")
    print("Red flags:")
    for flag in assessment.red_flags:
        print(f"  - {flag}")
    print(f"Recommended sources: {', '.join(assessment.recommended_sources)}")

    # Test lead time prediction
    print("\n--- Lead Time Prediction ---")
    prediction = agent.predict_lead_time(
        "CNC machined aluminum bracket",
        quantity=50,
        customization="Custom design, 6061-T6, anodized black"
    )
    print(f"Part type: {prediction.part_type}")
    print(f"Estimated lead time: {prediction.estimated_days_min}-{prediction.estimated_days_max} days")
    print(f"Rush available: {prediction.rush_lead_days} days (+{prediction.rush_premium_percent}%)")
    print("Factors:")
    for factor in prediction.factors:
        print(f"  - {factor}")
