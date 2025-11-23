"""
Agent_14: HEALER - Medical Device Parts Intelligence

The conscience of medical parts compatibility. Where mechanical fitness
meets patient safety, and every substitution decision carries the weight
of human well-being.

Domains:
- Medical imaging equipment (MRI, CT, X-ray)
- Patient monitoring systems
- Surgical instruments and implants
- Infusion and drug delivery systems
- Laboratory equipment

CRITICAL: This agent includes regulatory compliance checking.
          Parts may be mechanically compatible but NOT legally substitutable.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime


class ContactType(Enum):
    """ISO 10993 contact categorization"""
    SURFACE = "surface"              # Skin, mucous membrane
    EXTERNAL_COMMUNICATING = "external_communicating"  # Blood path, tissue/bone
    IMPLANT = "implant"              # Tissue, bone, blood


class ContactDuration(Enum):
    """ISO 10993 contact duration categorization"""
    LIMITED = "limited"              # < 24 hours
    PROLONGED = "prolonged"          # 24 hours to 30 days
    PERMANENT = "permanent"          # > 30 days


class DeviceClass(Enum):
    """FDA device classification"""
    CLASS_I = "I"                    # Low risk - general controls
    CLASS_II = "II"                  # Moderate risk - 510(k)
    CLASS_III = "III"                # High risk - PMA


class SterilizationMethod(Enum):
    """Common medical device sterilization methods"""
    AUTOCLAVE_121 = "autoclave_121c"       # Steam 121°C
    AUTOCLAVE_134 = "autoclave_134c"       # Steam 134°C
    ETO = "ethylene_oxide"                  # Ethylene oxide gas
    GAMMA = "gamma_radiation"               # Gamma irradiation
    EBEAM = "electron_beam"                 # E-beam irradiation
    H2O2_PLASMA = "hydrogen_peroxide_plasma"  # Low temp plasma
    DRY_HEAT = "dry_heat"                   # High temp dry


class USPClass(Enum):
    """USP Plastic Class for biological reactivity"""
    CLASS_I = "I"
    CLASS_II = "II"
    CLASS_III = "III"
    CLASS_IV = "IV"
    CLASS_V = "V"
    CLASS_VI = "VI"  # Most stringent - implant grade


@dataclass
class BiocompatibilityAssessment:
    """Assessment of material biocompatibility per ISO 10993"""
    material: str
    contact_type: ContactType
    duration: ContactDuration
    iso_10993_compliant: bool
    required_tests: List[str]
    completed_tests: List[str]
    material_standard: Optional[str]
    known_concerns: List[str]
    recommended_alternatives: List[str]
    usp_class: Optional[USPClass]
    fda_status: str


@dataclass
class MedicalGradeEquivalent:
    """A medical-grade equivalent for a commercial part"""
    part: str
    manufacturer: str
    compatibility_score: float  # 0-1
    certifications: List[str]
    biocompatibility: str
    sterilizable_methods: List[SterilizationMethod]
    price_vs_commercial: float  # Multiplier
    lead_time_weeks: int
    notes: str


@dataclass
class SterilizationCompatibility:
    """Sterilization method compatibility assessment"""
    part: str
    material: str
    method: SterilizationMethod
    compatible: bool
    reason: Optional[str]
    max_cycles: Optional[int]
    degradation_notes: str
    alternatives: List[Dict]
    alternative_methods: List[SterilizationMethod]


@dataclass
class RegulatoryAssessment:
    """Assessment of regulatory implications for part substitution"""
    original_device: str
    proposed_part: str
    device_class: DeviceClass
    is_critical_component: bool
    substitution_allowed: bool
    reason: str
    regulatory_path: str
    documentation_required: List[str]
    risk_level: str
    recommendation: str


@dataclass
class MedicalMaterial:
    """Medical-grade material specification"""
    designation: str
    common_name: str
    standard: str  # ASTM F138, etc.
    material_type: str  # metal, polymer, ceramic
    biocompatibility_tier: str
    usp_class: Optional[USPClass]
    contact_types: List[ContactType]
    max_contact_duration: ContactDuration
    sterilization_methods: List[SterilizationMethod]
    typical_applications: List[str]
    known_concerns: List[str]
    cost_factor: float


@dataclass
class MaterialCertification:
    """Material certification and traceability"""
    lot_number: str
    material: str
    manufacturer: str
    certification_date: datetime
    certifications: List[str]
    test_reports: List[str]
    expiry_date: Optional[datetime]
    traceability_chain: List[str]


class HealerAgent:
    """
    Agent_14: HEALER - Medical Device Parts Intelligence

    Core responsibilities:
    1. Biocompatibility assessment per ISO 10993
    2. Medical-grade equivalent finding
    3. Sterilization compatibility checking
    4. Regulatory pathway guidance
    5. Material traceability support
    """

    def __init__(self):
        self.biocompatibility_db = self._initialize_biocompatibility_db()
        self.materials_db = self._initialize_materials_db()
        self.sterilization_matrix = self._initialize_sterilization_matrix()
        self.device_classification = self._initialize_device_classification()

    def _initialize_biocompatibility_db(self) -> Dict:
        """Initialize ISO 10993 test requirements matrix"""
        return {
            # Contact type -> Duration -> Required tests
            (ContactType.SURFACE, ContactDuration.LIMITED): [
                "Cytotoxicity"
            ],
            (ContactType.SURFACE, ContactDuration.PROLONGED): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation"
            ],
            (ContactType.SURFACE, ContactDuration.PERMANENT): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Chronic Toxicity"
            ],
            (ContactType.EXTERNAL_COMMUNICATING, ContactDuration.LIMITED): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Hemocompatibility"
            ],
            (ContactType.EXTERNAL_COMMUNICATING, ContactDuration.PROLONGED): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Subchronic Toxicity",
                "Genotoxicity",
                "Hemocompatibility"
            ],
            (ContactType.EXTERNAL_COMMUNICATING, ContactDuration.PERMANENT): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Subchronic Toxicity",
                "Chronic Toxicity",
                "Genotoxicity",
                "Implantation",
                "Hemocompatibility"
            ],
            (ContactType.IMPLANT, ContactDuration.LIMITED): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Genotoxicity"
            ],
            (ContactType.IMPLANT, ContactDuration.PROLONGED): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Subchronic Toxicity",
                "Genotoxicity",
                "Implantation"
            ],
            (ContactType.IMPLANT, ContactDuration.PERMANENT): [
                "Cytotoxicity",
                "Sensitization",
                "Irritation",
                "Acute Systemic Toxicity",
                "Subchronic Toxicity",
                "Chronic Toxicity",
                "Genotoxicity",
                "Implantation",
                "Carcinogenicity"
            ],
        }

    def _initialize_materials_db(self) -> Dict[str, MedicalMaterial]:
        """Initialize medical-grade materials database"""
        return {
            "316L_surgical": MedicalMaterial(
                designation="316L Surgical Grade",
                common_name="Surgical Stainless Steel",
                standard="ASTM F138",
                material_type="metal",
                biocompatibility_tier="implant_grade",
                usp_class=None,  # Metals don't have USP class
                contact_types=[ContactType.SURFACE, ContactType.EXTERNAL_COMMUNICATING, ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_121, SterilizationMethod.AUTOCLAVE_134,
                                      SterilizationMethod.ETO, SterilizationMethod.GAMMA],
                typical_applications=["surgical instruments", "temporary implants", "bone plates"],
                known_concerns=["nickel sensitivity in some patients (~10-15%)", "not MRI safe at high field"],
                cost_factor=3.0
            ),
            "Ti6Al4V_ELI": MedicalMaterial(
                designation="Ti-6Al-4V ELI",
                common_name="Titanium Alloy Grade 23",
                standard="ASTM F136",
                material_type="metal",
                biocompatibility_tier="implant_grade",
                usp_class=None,
                contact_types=[ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_121, SterilizationMethod.AUTOCLAVE_134,
                                      SterilizationMethod.ETO, SterilizationMethod.GAMMA],
                typical_applications=["permanent implants", "orthopedic devices", "dental implants"],
                known_concerns=["higher cost", "difficult to machine"],
                cost_factor=15.0
            ),
            "PEEK_implant": MedicalMaterial(
                designation="PEEK Implant Grade",
                common_name="Polyether Ether Ketone",
                standard="ASTM F2026",
                material_type="polymer",
                biocompatibility_tier="implant_grade",
                usp_class=USPClass.CLASS_VI,
                contact_types=[ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                      SterilizationMethod.GAMMA],
                typical_applications=["spinal cages", "cranial implants", "dental abutments"],
                known_concerns=["radiolucent (invisible on X-ray)", "high cost"],
                cost_factor=20.0
            ),
            "UHMWPE_medical": MedicalMaterial(
                designation="UHMWPE Medical Grade",
                common_name="Ultra-High Molecular Weight Polyethylene",
                standard="ASTM F648",
                material_type="polymer",
                biocompatibility_tier="implant_grade",
                usp_class=USPClass.CLASS_VI,
                contact_types=[ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.ETO, SterilizationMethod.GAMMA],
                typical_applications=["joint replacement bearings", "acetabular cups", "tibial inserts"],
                known_concerns=["wear debris", "oxidation from gamma sterilization in air"],
                cost_factor=8.0
            ),
            "silicone_implant": MedicalMaterial(
                designation="Medical Grade Silicone",
                common_name="Implant Grade Silicone",
                standard="ASTM F2042",
                material_type="polymer",
                biocompatibility_tier="implant_grade",
                usp_class=USPClass.CLASS_VI,
                contact_types=[ContactType.SURFACE, ContactType.EXTERNAL_COMMUNICATING, ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_121, SterilizationMethod.ETO,
                                      SterilizationMethod.GAMMA],
                typical_applications=["catheters", "tubing", "soft tissue implants", "seals"],
                known_concerns=["limited strength", "possible sensitivity reactions"],
                cost_factor=5.0
            ),
            "PPSU": MedicalMaterial(
                designation="PPSU (Radel)",
                common_name="Polyphenylsulfone",
                standard="ISO 10993",
                material_type="polymer",
                biocompatibility_tier="medical_grade",
                usp_class=USPClass.CLASS_VI,
                contact_types=[ContactType.SURFACE, ContactType.EXTERNAL_COMMUNICATING],
                max_contact_duration=ContactDuration.PROLONGED,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                      SterilizationMethod.GAMMA, SterilizationMethod.H2O2_PLASMA],
                typical_applications=["surgical instrument handles", "sterilization trays", "housings"],
                known_concerns=["amber color may affect visibility", "expensive"],
                cost_factor=10.0
            ),
            "cobalt_chrome": MedicalMaterial(
                designation="CoCrMo Alloy",
                common_name="Cobalt Chrome",
                standard="ASTM F75/F1537",
                material_type="metal",
                biocompatibility_tier="implant_grade",
                usp_class=None,
                contact_types=[ContactType.IMPLANT],
                max_contact_duration=ContactDuration.PERMANENT,
                sterilization_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                      SterilizationMethod.GAMMA],
                typical_applications=["hip implants", "knee implants", "dental prosthetics"],
                known_concerns=["metal ion release", "cobalt sensitivity", "MRI conditional"],
                cost_factor=12.0
            ),
        }

    def _initialize_sterilization_matrix(self) -> Dict:
        """Initialize material-sterilization compatibility matrix"""
        return {
            # Material type -> Sterilization method -> (compatible, max_cycles, notes)
            ("ABS", SterilizationMethod.AUTOCLAVE_121): (False, 0, "HDT ~98°C, will deform"),
            ("ABS", SterilizationMethod.AUTOCLAVE_134): (False, 0, "HDT ~98°C, will deform"),
            ("ABS", SterilizationMethod.ETO): (True, 100, "Compatible"),
            ("ABS", SterilizationMethod.H2O2_PLASMA): (True, 100, "Compatible"),

            ("PPSU", SterilizationMethod.AUTOCLAVE_121): (True, 1000, "Excellent steam resistance"),
            ("PPSU", SterilizationMethod.AUTOCLAVE_134): (True, 1000, "Excellent steam resistance"),
            ("PPSU", SterilizationMethod.ETO): (True, 500, "Compatible"),
            ("PPSU", SterilizationMethod.GAMMA): (True, 5, "Limited cycles, may yellow"),

            ("PEEK", SterilizationMethod.AUTOCLAVE_134): (True, 3000, "Excellent resistance"),
            ("PEEK", SterilizationMethod.ETO): (True, 1000, "Compatible"),
            ("PEEK", SterilizationMethod.GAMMA): (True, 10, "May affect mechanical properties"),

            ("Polycarbonate", SterilizationMethod.AUTOCLAVE_121): (False, 0, "Will craze/crack"),
            ("Polycarbonate", SterilizationMethod.ETO): (True, 50, "Compatible"),
            ("Polycarbonate", SterilizationMethod.GAMMA): (True, 5, "Yellowing, embrittlement"),

            ("Silicone", SterilizationMethod.AUTOCLAVE_121): (True, 500, "Compatible"),
            ("Silicone", SterilizationMethod.AUTOCLAVE_134): (True, 500, "Compatible"),
            ("Silicone", SterilizationMethod.ETO): (True, 500, "Compatible"),
            ("Silicone", SterilizationMethod.GAMMA): (True, 100, "May affect properties over time"),

            ("316L_Stainless", SterilizationMethod.AUTOCLAVE_121): (True, 10000, "Excellent"),
            ("316L_Stainless", SterilizationMethod.AUTOCLAVE_134): (True, 10000, "Excellent"),
            ("316L_Stainless", SterilizationMethod.ETO): (True, 10000, "Excellent"),
            ("316L_Stainless", SterilizationMethod.GAMMA): (True, 10000, "Excellent"),

            ("Titanium", SterilizationMethod.AUTOCLAVE_121): (True, 10000, "Excellent"),
            ("Titanium", SterilizationMethod.AUTOCLAVE_134): (True, 10000, "Excellent"),
            ("Titanium", SterilizationMethod.ETO): (True, 10000, "Excellent"),
            ("Titanium", SterilizationMethod.GAMMA): (True, 10000, "Excellent"),

            ("UHMWPE", SterilizationMethod.AUTOCLAVE_121): (False, 0, "Low melting point"),
            ("UHMWPE", SterilizationMethod.ETO): (True, 100, "Preferred method"),
            ("UHMWPE", SterilizationMethod.GAMMA): (True, 1, "Single use - causes oxidation"),
        }

    def _initialize_device_classification(self) -> Dict:
        """Initialize FDA device classification examples"""
        return {
            "tongue_depressor": DeviceClass.CLASS_I,
            "bandage": DeviceClass.CLASS_I,
            "surgical_gloves": DeviceClass.CLASS_I,
            "infusion_pump": DeviceClass.CLASS_II,
            "surgical_drape": DeviceClass.CLASS_II,
            "powered_wheelchair": DeviceClass.CLASS_II,
            "ct_scanner": DeviceClass.CLASS_II,
            "pacemaker": DeviceClass.CLASS_III,
            "hip_implant": DeviceClass.CLASS_III,
            "heart_valve": DeviceClass.CLASS_III,
            "drug_eluting_stent": DeviceClass.CLASS_III,
        }

    def check_biocompatibility(
        self,
        material: str,
        contact_type: str,
        duration: str
    ) -> BiocompatibilityAssessment:
        """
        Check if a material is biocompatible for the intended use.

        Args:
            material: Material name (e.g., "316L Stainless Steel")
            contact_type: "surface", "external_communicating", "implant"
            duration: "limited", "prolonged", "permanent"

        Returns:
            BiocompatibilityAssessment with ISO 10993 compliance details
        """
        # Convert string inputs to enums
        contact = ContactType[contact_type.upper()]
        dur = ContactDuration[duration.upper()]

        # Get required tests for this contact/duration combination
        required_tests = self.biocompatibility_db.get((contact, dur), [])

        # Check if material is in our medical-grade database
        material_lower = material.lower().replace("-", "").replace("_", "").replace(" ", "")
        material_data = None

        # Material aliases for better matching
        material_aliases = {
            "316l": ["316l_surgical", "316lstainless", "surgicalstainless"],
            "316lstainless": ["316l_surgical"],
            "titanium": ["Ti6Al4V_ELI", "titaniumalloy"],
            "ti6al4v": ["Ti6Al4V_ELI"],
            "peek": ["PEEK_implant"],
            "uhmwpe": ["UHMWPE_medical"],
            "silicone": ["silicone_implant"],
            "ppsu": ["PPSU"],
            "radel": ["PPSU"],
            "cobaltchrome": ["cobalt_chrome"],
            "cocrmo": ["cobalt_chrome"],
        }

        for key, mat in self.materials_db.items():
            # Normalize both for comparison
            designation_norm = mat.designation.lower().replace("-", "").replace("_", "").replace(" ", "")
            common_norm = mat.common_name.lower().replace("-", "").replace("_", "").replace(" ", "")
            key_norm = key.lower().replace("_", "")

            # Check various matching patterns
            matched = False

            # Direct substring matching
            if (material_lower in designation_norm or
                designation_norm in material_lower or
                material_lower in common_norm or
                common_norm in material_lower):
                matched = True

            # Key-based matching (extract base material name)
            if not matched:
                # Check if any part of the material matches the key
                for alias_key, alias_values in material_aliases.items():
                    if alias_key in material_lower and key in alias_values:
                        matched = True
                        break

            # Partial key match (e.g., "316l" in "316lstainlesssteel")
            if not matched:
                key_base = key.lower().split("_")[0]
                if key_base in material_lower:
                    matched = True

            if matched:
                material_data = mat
                break

        # Build assessment
        if material_data:
            # Known medical-grade material
            is_compliant = (
                contact in material_data.contact_types and
                self._duration_compatible(dur, material_data.max_contact_duration)
            )
            return BiocompatibilityAssessment(
                material=material,
                contact_type=contact,
                duration=dur,
                iso_10993_compliant=is_compliant,
                required_tests=required_tests,
                completed_tests=required_tests if is_compliant else [],
                material_standard=material_data.standard,
                known_concerns=material_data.known_concerns,
                recommended_alternatives=self._get_alternatives(contact, dur),
                usp_class=material_data.usp_class,
                fda_status="Recognized" if is_compliant else "Requires testing"
            )
        else:
            # Unknown material - requires full testing
            return BiocompatibilityAssessment(
                material=material,
                contact_type=contact,
                duration=dur,
                iso_10993_compliant=False,
                required_tests=required_tests,
                completed_tests=[],
                material_standard=None,
                known_concerns=["Material not in medical-grade database", "Full ISO 10993 testing required"],
                recommended_alternatives=self._get_alternatives(contact, dur),
                usp_class=None,
                fda_status="Unknown - requires testing"
            )

    def _duration_compatible(self, requested: ContactDuration, max_allowed: ContactDuration) -> bool:
        """Check if requested duration is within material's capability"""
        duration_order = [ContactDuration.LIMITED, ContactDuration.PROLONGED, ContactDuration.PERMANENT]
        return duration_order.index(requested) <= duration_order.index(max_allowed)

    def _get_alternatives(self, contact: ContactType, duration: ContactDuration) -> List[str]:
        """Get alternative materials for given contact/duration"""
        alternatives = []
        for key, mat in self.materials_db.items():
            if contact in mat.contact_types and self._duration_compatible(duration, mat.max_contact_duration):
                alternatives.append(f"{mat.designation} ({mat.standard})")
        return alternatives[:5]  # Top 5

    def find_medical_grade_equivalent(
        self,
        commercial_part: str,
        medical_application: str
    ) -> List[MedicalGradeEquivalent]:
        """
        Find medical-grade equivalents for commercial parts.

        Args:
            commercial_part: Description of commercial part
            medical_application: Intended medical use

        Returns:
            List of MedicalGradeEquivalent options
        """
        equivalents = []
        part_lower = commercial_part.lower()
        app_lower = medical_application.lower()

        # Tubing equivalents
        if "tubing" in part_lower or "tube" in part_lower:
            equivalents.append(MedicalGradeEquivalent(
                part="Pumpsil Platinum-Cured Silicone Tubing",
                manufacturer="Saint-Gobain",
                compatibility_score=0.95,
                certifications=["USP Class VI", "FDA 21 CFR 177.2600", "ISO 10993"],
                biocompatibility="Full ISO 10993 compliant",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_121, SterilizationMethod.ETO,
                                     SterilizationMethod.GAMMA],
                price_vs_commercial=3.5,
                lead_time_weeks=2,
                notes="Platinum-cured, no peroxide residuals"
            ))
            equivalents.append(MedicalGradeEquivalent(
                part="C-Flex TPE Tubing",
                manufacturer="Saint-Gobain",
                compatibility_score=0.88,
                certifications=["USP Class VI", "FDA compliant"],
                biocompatibility="USP Class VI",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_121, SterilizationMethod.ETO,
                                     SterilizationMethod.GAMMA],
                price_vs_commercial=2.5,
                lead_time_weeks=2,
                notes="Good for peristaltic pumps, bonds easily"
            ))

        # Fastener equivalents
        if "fastener" in part_lower or "bolt" in part_lower or "screw" in part_lower:
            equivalents.append(MedicalGradeEquivalent(
                part="316L Surgical Grade Fastener",
                manufacturer="UC Components",
                compatibility_score=0.92,
                certifications=["ASTM F138", "ISO 10993 compliant"],
                biocompatibility="Surgical implant grade",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                     SterilizationMethod.GAMMA],
                price_vs_commercial=5.0,
                lead_time_weeks=3,
                notes="Full material certification available"
            ))
            equivalents.append(MedicalGradeEquivalent(
                part="Ti-6Al-4V ELI Fastener",
                manufacturer="Titanium Industries",
                compatibility_score=0.98,
                certifications=["ASTM F136", "ISO 5832-3"],
                biocompatibility="Permanent implant grade",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                     SterilizationMethod.GAMMA],
                price_vs_commercial=15.0,
                lead_time_weeks=4,
                notes="Best for nickel-sensitive patients"
            ))

        # Plastic parts
        if "plastic" in part_lower or "handle" in part_lower or "housing" in part_lower:
            equivalents.append(MedicalGradeEquivalent(
                part="PPSU (Radel R-5500)",
                manufacturer="Solvay",
                compatibility_score=0.90,
                certifications=["USP Class VI", "ISO 10993"],
                biocompatibility="Medical device grade",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                     SterilizationMethod.H2O2_PLASMA],
                price_vs_commercial=8.0,
                lead_time_weeks=3,
                notes="Excellent for reusable surgical instruments"
            ))
            equivalents.append(MedicalGradeEquivalent(
                part="PEEK-OPTIMA",
                manufacturer="Invibio",
                compatibility_score=0.95,
                certifications=["ASTM F2026", "USP Class VI", "ISO 10993"],
                biocompatibility="Implant grade polymer",
                sterilizable_methods=[SterilizationMethod.AUTOCLAVE_134, SterilizationMethod.ETO,
                                     SterilizationMethod.GAMMA],
                price_vs_commercial=20.0,
                lead_time_weeks=4,
                notes="Premium implant-grade polymer"
            ))

        # Default recommendation if no specific match
        if not equivalents:
            equivalents.append(MedicalGradeEquivalent(
                part="Contact for custom assessment",
                manufacturer="Consult medical materials supplier",
                compatibility_score=0.0,
                certifications=["Requires evaluation"],
                biocompatibility="Unknown",
                sterilizable_methods=[],
                price_vs_commercial=1.0,
                lead_time_weeks=8,
                notes="Part not in database - requires detailed evaluation"
            ))

        # Sort by compatibility score
        equivalents.sort(key=lambda x: x.compatibility_score, reverse=True)
        return equivalents

    def validate_sterilization_compatibility(
        self,
        part: str,
        material: str,
        sterilization_method: str
    ) -> SterilizationCompatibility:
        """
        Validate if a material can withstand a sterilization method.

        Args:
            part: Part description
            material: Material type (e.g., "ABS", "PPSU", "316L_Stainless")
            sterilization_method: Method name or enum

        Returns:
            SterilizationCompatibility assessment
        """
        # Convert method string to enum if needed
        if isinstance(sterilization_method, str):
            method_map = {
                "autoclave": SterilizationMethod.AUTOCLAVE_121,
                "autoclave_121": SterilizationMethod.AUTOCLAVE_121,
                "autoclave_134": SterilizationMethod.AUTOCLAVE_134,
                "autoclave 134c": SterilizationMethod.AUTOCLAVE_134,
                "eto": SterilizationMethod.ETO,
                "ethylene oxide": SterilizationMethod.ETO,
                "gamma": SterilizationMethod.GAMMA,
                "gamma radiation": SterilizationMethod.GAMMA,
                "h2o2": SterilizationMethod.H2O2_PLASMA,
                "plasma": SterilizationMethod.H2O2_PLASMA,
            }
            method = method_map.get(sterilization_method.lower(), SterilizationMethod.AUTOCLAVE_134)
        else:
            method = sterilization_method

        # Look up in matrix
        key = (material, method)
        if key in self.sterilization_matrix:
            compatible, max_cycles, notes = self.sterilization_matrix[key]
        else:
            # Unknown combination
            compatible = False
            max_cycles = 0
            notes = "Material-method combination not in database"

        # Find alternatives if not compatible
        alternatives = []
        alternative_methods = []

        if not compatible:
            # Find alternative materials that work with this method
            for (mat, meth), (compat, cycles, _) in self.sterilization_matrix.items():
                if meth == method and compat and cycles > 0:
                    alternatives.append({
                        "material": mat,
                        "max_cycles": cycles,
                        "compatible": True
                    })

            # Find alternative methods that work with this material
            for (mat, meth), (compat, cycles, _) in self.sterilization_matrix.items():
                if mat == material and compat and cycles > 0:
                    alternative_methods.append(meth)

        return SterilizationCompatibility(
            part=part,
            material=material,
            method=method,
            compatible=compatible,
            reason=notes if not compatible else None,
            max_cycles=max_cycles if compatible else None,
            degradation_notes=notes,
            alternatives=alternatives[:3],  # Top 3 alternatives
            alternative_methods=list(set(alternative_methods))[:3]
        )

    def check_regulatory_substitution(
        self,
        original_device: str,
        proposed_part: str
    ) -> RegulatoryAssessment:
        """
        Determine if part substitution requires regulatory action.

        Args:
            original_device: Original medical device description
            proposed_part: Proposed replacement part

        Returns:
            RegulatoryAssessment with pathway guidance
        """
        device_lower = original_device.lower()
        part_lower = proposed_part.lower()

        # Determine device class
        device_class = DeviceClass.CLASS_II  # Default
        for device_keyword, dev_class in self.device_classification.items():
            if device_keyword in device_lower:
                device_class = dev_class
                break

        # Determine if critical component
        critical_keywords = [
            "motor", "pump", "sensor", "battery", "software",
            "electrode", "catheter", "implant", "seal", "valve"
        ]
        is_critical = any(kw in part_lower for kw in critical_keywords)

        # Build assessment based on device class and criticality
        if device_class == DeviceClass.CLASS_I:
            if is_critical:
                return RegulatoryAssessment(
                    original_device=original_device,
                    proposed_part=proposed_part,
                    device_class=device_class,
                    is_critical_component=is_critical,
                    substitution_allowed=True,
                    reason="Class I device - critical component change",
                    regulatory_path="Document change in DHF, update risk analysis",
                    documentation_required=["Design History File update", "Risk analysis update"],
                    risk_level="LOW",
                    recommendation="Document change per 21 CFR 820"
                )
            else:
                return RegulatoryAssessment(
                    original_device=original_device,
                    proposed_part=proposed_part,
                    device_class=device_class,
                    is_critical_component=is_critical,
                    substitution_allowed=True,
                    reason="Class I device - non-critical component",
                    regulatory_path="Document in DHF",
                    documentation_required=["Design History File update"],
                    risk_level="MINIMAL",
                    recommendation="Standard change control documentation"
                )

        elif device_class == DeviceClass.CLASS_II:
            if is_critical:
                return RegulatoryAssessment(
                    original_device=original_device,
                    proposed_part=proposed_part,
                    device_class=device_class,
                    is_critical_component=is_critical,
                    substitution_allowed=False,
                    reason="Class II device - critical component may require new 510(k)",
                    regulatory_path="Assess per FDA guidance on 510(k) changes, likely Letter to File or new 510(k)",
                    documentation_required=[
                        "510(k) change assessment",
                        "Design verification testing",
                        "Risk analysis update",
                        "Biocompatibility assessment (if patient contact)"
                    ],
                    risk_level="MODERATE to HIGH",
                    recommendation="Consult regulatory affairs before substitution"
                )
            else:
                return RegulatoryAssessment(
                    original_device=original_device,
                    proposed_part=proposed_part,
                    device_class=device_class,
                    is_critical_component=is_critical,
                    substitution_allowed=True,
                    reason="Class II device - non-critical component",
                    regulatory_path="Letter to File or DHF update",
                    documentation_required=[
                        "Design History File update",
                        "Risk analysis review",
                        "Equivalence justification"
                    ],
                    risk_level="LOW to MODERATE",
                    recommendation="Document equivalent performance"
                )

        else:  # Class III
            return RegulatoryAssessment(
                original_device=original_device,
                proposed_part=proposed_part,
                device_class=device_class,
                is_critical_component=True,  # Assume all Class III components are critical
                substitution_allowed=False,
                reason="Class III device - all component changes require PMA supplement evaluation",
                regulatory_path="PMA supplement or 30-day notice required",
                documentation_required=[
                    "PMA supplement assessment",
                    "Full design verification",
                    "Clinical evaluation (if needed)",
                    "Biocompatibility testing",
                    "Risk analysis update"
                ],
                risk_level="HIGH",
                recommendation="DO NOT substitute without regulatory approval. Consult regulatory affairs."
            )

    def get_material_certification_requirements(
        self,
        material: str,
        application: str
    ) -> Dict:
        """
        Get certification requirements for a material in medical use.

        Args:
            material: Material type
            application: Intended medical application

        Returns:
            Dict with certification requirements
        """
        requirements = {
            "material": material,
            "application": application,
            "certifications_needed": [],
            "testing_required": [],
            "documentation_required": [],
            "estimated_cost_usd": 0,
            "estimated_time_months": 0
        }

        # Base certifications for any medical material
        requirements["certifications_needed"].extend([
            "Material Certificate of Analysis (CoA)",
            "Certificate of Conformance (CoC)",
            "Lot traceability documentation"
        ])

        # Application-specific requirements
        app_lower = application.lower()

        if "implant" in app_lower:
            requirements["certifications_needed"].extend([
                "ASTM/ISO material standard compliance",
                "Full ISO 10993 biocompatibility"
            ])
            requirements["testing_required"].extend([
                "Cytotoxicity (ISO 10993-5)",
                "Sensitization (ISO 10993-10)",
                "Implantation testing (ISO 10993-6)",
                "Systemic toxicity",
                "Genotoxicity",
                "Chronic toxicity (for permanent implants)"
            ])
            requirements["estimated_cost_usd"] = 75000
            requirements["estimated_time_months"] = 12

        elif "blood contact" in app_lower or "catheter" in app_lower:
            requirements["certifications_needed"].extend([
                "ISO 10993 biocompatibility",
                "Hemocompatibility testing"
            ])
            requirements["testing_required"].extend([
                "Cytotoxicity",
                "Sensitization",
                "Hemocompatibility (ISO 10993-4)",
                "Thrombogenicity",
                "Hemolysis"
            ])
            requirements["estimated_cost_usd"] = 45000
            requirements["estimated_time_months"] = 8

        elif "surface" in app_lower or "external" in app_lower:
            requirements["certifications_needed"].extend([
                "USP Class VI (for plastics)",
                "ISO 10993 basic testing"
            ])
            requirements["testing_required"].extend([
                "Cytotoxicity",
                "Sensitization",
                "Irritation"
            ])
            requirements["estimated_cost_usd"] = 15000
            requirements["estimated_time_months"] = 4

        else:
            requirements["certifications_needed"].append("ISO 10993 risk-based testing")
            requirements["testing_required"].extend([
                "Cytotoxicity",
                "Sensitization"
            ])
            requirements["estimated_cost_usd"] = 10000
            requirements["estimated_time_months"] = 3

        requirements["documentation_required"] = [
            "Material specification",
            "Manufacturing process validation",
            "Cleaning validation (if applicable)",
            "Sterilization validation",
            "Shelf life/aging studies",
            "Supplier quality agreement"
        ]

        return requirements


# Demo usage
if __name__ == "__main__":
    agent = HealerAgent()

    print("=" * 60)
    print("Agent_14: HEALER - Medical Device Parts Intelligence")
    print("=" * 60)

    # Test biocompatibility check
    print("\n--- Biocompatibility Assessment ---")
    result = agent.check_biocompatibility(
        material="316L Stainless Steel",
        contact_type="implant",
        duration="permanent"
    )
    print(f"Material: {result.material}")
    print(f"ISO 10993 Compliant: {result.iso_10993_compliant}")
    print(f"Material Standard: {result.material_standard}")
    print(f"Required Tests: {len(result.required_tests)}")
    for test in result.required_tests[:3]:
        print(f"  - {test}")
    print(f"Known Concerns:")
    for concern in result.known_concerns:
        print(f"  - {concern}")

    # Test medical-grade equivalent finding
    print("\n--- Medical-Grade Equivalent Finding ---")
    equivalents = agent.find_medical_grade_equivalent(
        commercial_part="Generic silicone tubing 1/4 ID",
        medical_application="peristaltic pump, drug contact"
    )
    for eq in equivalents[:2]:
        print(f"\n{eq.part} ({eq.manufacturer}):")
        print(f"  Compatibility: {eq.compatibility_score:.0%}")
        print(f"  Certifications: {', '.join(eq.certifications[:2])}")
        print(f"  Price vs commercial: {eq.price_vs_commercial}x")

    # Test sterilization compatibility
    print("\n--- Sterilization Compatibility ---")
    compat = agent.validate_sterilization_compatibility(
        part="Plastic instrument handle",
        material="ABS",
        sterilization_method="autoclave_134"
    )
    print(f"Part: {compat.part}")
    print(f"Material: {compat.material}")
    print(f"Method: {compat.method.value}")
    print(f"Compatible: {compat.compatible}")
    print(f"Reason: {compat.reason}")
    if compat.alternatives:
        print("Alternative materials:")
        for alt in compat.alternatives:
            print(f"  - {alt['material']} (up to {alt['max_cycles']} cycles)")
    if compat.alternative_methods:
        print("Alternative sterilization methods:")
        for meth in compat.alternative_methods:
            print(f"  - {meth.value}")

    # Test regulatory substitution check
    print("\n--- Regulatory Substitution Assessment ---")
    reg = agent.check_regulatory_substitution(
        original_device="Infusion pump model XYZ",
        proposed_part="Generic motor"
    )
    print(f"Device: {reg.original_device}")
    print(f"Proposed Part: {reg.proposed_part}")
    print(f"Device Class: {reg.device_class.value}")
    print(f"Substitution Allowed: {reg.substitution_allowed}")
    print(f"Risk Level: {reg.risk_level}")
    print(f"Regulatory Path: {reg.regulatory_path}")
    print(f"Recommendation: {reg.recommendation}")
