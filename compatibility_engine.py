"""
Universal Parts Consciousness - Technical Compatibility Engine
Precise mathematical validation of part compatibility
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
import math

@dataclass
class ThreadSpec:
    """Complete thread specification"""
    nominal_diameter: Decimal
    pitch: Decimal
    thread_class: str
    major_dia_min: Decimal
    major_dia_max: Decimal
    pitch_dia_min: Decimal
    pitch_dia_max: Decimal
    minor_dia_min: Decimal
    minor_dia_max: Decimal
    thread_angle: Decimal = Decimal('60')  # degrees

@dataclass
class PartSpec:
    """Complete part specification"""
    part_id: str
    thread: ThreadSpec
    length: Decimal
    length_tolerance_plus: Decimal
    length_tolerance_minus: Decimal
    material_grade: str
    tensile_strength: Decimal  # MPa
    proof_load: Decimal  # kN
    head_height: Optional[Decimal] = None
    thread_length: Optional[Decimal] = None  # None = fully threaded

class TechnicalCompatibilityEngine:
    """
    Engine for precise technical compatibility checking
    No consciousness, just mathematics and specifications
    """
    
    def __init__(self, database_connection):
        self.db = database_connection
        self.material_factors = self._load_material_factors()
        
    def check_thread_compatibility(self, 
                                 external: ThreadSpec, 
                                 internal: ThreadSpec) -> Dict:
        """
        Mathematically verify thread compatibility
        """
        # Basic compatibility checks
        if external.nominal_diameter != internal.nominal_diameter:
            return {
                'compatible': False,
                'reason': f'Diameter mismatch: {external.nominal_diameter} vs {internal.nominal_diameter}'
            }
            
        if external.pitch != internal.pitch:
            return {
                'compatible': False,
                'reason': f'Pitch mismatch: {external.pitch} vs {internal.pitch}'
            }
        
        # Tolerance stack-up analysis
        # External thread pitch diameter should be smaller than internal
        clearance_min = internal.pitch_dia_min - external.pitch_dia_max
        clearance_max = internal.pitch_dia_max - external.pitch_dia_min
        
        # ISO 965-1 allowances
        if clearance_min < 0:
            return {
                'compatible': False,
                'reason': 'Interference fit - threads will not assemble',
                'clearance_min': float(clearance_min)
            }
        
        # Check engagement parameters
        engagement_quality = self._calculate_engagement_quality(external, internal)
        
        return {
            'compatible': True,
            'clearance_min': float(clearance_min),
            'clearance_max': float(clearance_max),
            'engagement_quality': engagement_quality,
            'tolerance_class_match': self._check_tolerance_class_match(
                external.thread_class, 
                internal.thread_class
            )
        }
    
    def check_length_compatibility(self,
                                 screw: PartSpec,
                                 material_thickness: Decimal,
                                 nut_height: Optional[Decimal] = None) -> Dict:
        """
        Verify length compatibility for application
        """
        # Calculate actual length range with tolerances
        min_length = screw.length + screw.length_tolerance_minus
        max_length = screw.length + screw.length_tolerance_plus
        
        # Grip length (unthreaded portion under head)
        if screw.thread_length:
            grip_length = screw.length - screw.thread_length
        else:
            grip_length = Decimal('0')  # Fully threaded
        
        # Calculate engagement
        if nut_height:
            # Through-bolt with nut
            engagement = nut_height
            protrusion_min = min_length - material_thickness
            protrusion_max = max_length - material_thickness
            
            # Need at least 1 thread showing past nut (ISO 898-2)
            min_protrusion_required = screw.thread.pitch
            
            length_ok = protrusion_min >= (nut_height + min_protrusion_required)
            
        else:
            # Blind hole threading
            available_depth = material_thickness
            engagement = min(max_length, available_depth)
            protrusion_min = max(Decimal('0'), min_length - material_thickness)
            protrusion_max = max(Decimal('0'), max_length - material_thickness)
            length_ok = True  # Will check engagement ratio instead
        
        # Engagement ratio (thread engagement / diameter)
        engagement_ratio = engagement / screw.thread.nominal_diameter
        
        # Minimum engagement per ISO 898-1
        min_engagement_ratio = self._get_min_engagement_ratio(
            screw.material_grade,
            'steel'  # Assume steel nut/tapped hole
        )
        
        sufficient_engagement = engagement_ratio >= min_engagement_ratio
        
        return {
            'length_compatible': length_ok and sufficient_engagement,
            'engagement_length': float(engagement),
            'engagement_ratio': float(engagement_ratio),
            'min_engagement_ratio': float(min_engagement_ratio),
            'sufficient_engagement': sufficient_engagement,
            'protrusion_min': float(protrusion_min),
            'protrusion_max': float(protrusion_max),
            'grip_length': float(grip_length),
            'recommendations': self._get_length_recommendations(
                engagement_ratio, 
                min_engagement_ratio,
                protrusion_max
            )
        }
    
    def calculate_joint_strength(self,
                               screw: PartSpec,
                               engagement_length: Decimal,
                               base_material: str,
                               safety_factor: Decimal = Decimal('2.5')) -> Dict:
        """
        Calculate actual joint strength with given parameters
        """
        # Thread shear area per ISO 898-1
        thread_shear_area = self._calculate_thread_shear_area(
            screw.thread,
            engagement_length
        )
        
        # Material strength factors
        screw_material_factor = self._get_material_strength_factor(screw.material_grade)
        base_material_factor = self._get_material_strength_factor(base_material)
        
        # Failure modes
        # 1. Screw tensile failure
        screw_tensile_strength = screw.proof_load
        
        # 2. Thread stripping - external (screw)
        external_strip_strength = (
            thread_shear_area * 
            screw.tensile_strength * 
            Decimal('0.577')  # Shear = 0.577 * tensile
        ) / 1000  # Convert to kN
        
        # 3. Thread stripping - internal (base material)
        base_material_tensile = self._get_base_material_tensile(base_material)
        internal_strip_strength = (
            thread_shear_area * 
            base_material_tensile * 
            Decimal('0.577') *
            Decimal('1.25')  # Internal threads are 25% stronger
        ) / 1000  # Convert to kN
        
        # Limiting failure mode
        limiting_strength = min(
            screw_tensile_strength,
            external_strip_strength,
            internal_strip_strength
        )
        
        limiting_mode = 'screw_tensile'
        if limiting_strength == external_strip_strength:
            limiting_mode = 'external_thread_strip'
        elif limiting_strength == internal_strip_strength:
            limiting_mode = 'internal_thread_strip'
        
        # Apply safety factor
        allowable_load = limiting_strength / safety_factor
        
        return {
            'thread_shear_area_mm2': float(thread_shear_area),
            'screw_tensile_strength_kN': float(screw_tensile_strength),
            'external_strip_strength_kN': float(external_strip_strength),
            'internal_strip_strength_kN': float(internal_strip_strength),
            'limiting_strength_kN': float(limiting_strength),
            'limiting_failure_mode': limiting_mode,
            'safety_factor': float(safety_factor),
            'allowable_load_kN': float(allowable_load),
            'allowable_load_N': float(allowable_load * 1000)
        }
    
    def find_compatible_parts(self,
                            requirements: Dict,
                            inventory: List[str] = None) -> List[Dict]:
        """
        Find all parts meeting technical requirements
        """
        query = """
        SELECT p.*, t.*, fh.*
        FROM parts p
        JOIN thread_specifications t ON p.thread_id = t.thread_id
        LEFT JOIN fastener_heads fh ON p.part_id = fh.part_id
        WHERE 1=1
        """
        
        params = []
        
        # Thread requirements
        if 'thread_diameter' in requirements:
            query += " AND t.nominal_diameter = %s"
            params.append(requirements['thread_diameter'])
            
        if 'thread_pitch' in requirements:
            query += " AND t.pitch = %s"
            params.append(requirements['thread_pitch'])
        
        # Length requirements
        if 'min_length' in requirements:
            query += " AND p.length >= %s"
            params.append(requirements['min_length'])
            
        if 'max_length' in requirements:
            query += " AND p.length <= %s"
            params.append(requirements['max_length'])
        
        # Strength requirements
        if 'min_proof_load' in requirements:
            query += " AND p.proof_load >= %s"
            params.append(requirements['min_proof_load'])
        
        # Drive type
        if 'drive_type' in requirements:
            query += " AND fh.drive_type = %s"
            params.append(requirements['drive_type'])
        
        # Inventory filter
        if inventory:
            query += " AND p.part_id IN %s"
            params.append(tuple(inventory))
        
        results = self.db.execute(query, params)
        
        # Post-process for exact compatibility
        compatible_parts = []
        for part in results:
            # Run full compatibility check
            if self._meets_all_requirements(part, requirements):
                compatible_parts.append({
                    'part': part,
                    'compatibility_score': self._calculate_compatibility_score(
                        part, 
                        requirements
                    )
                })
        
        # Sort by compatibility score
        compatible_parts.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return compatible_parts
    
    def _calculate_thread_shear_area(self, 
                                   thread: ThreadSpec, 
                                   engagement: Decimal) -> Decimal:
        """
        Calculate thread shear area per ISO 898-1
        """
        # Number of engaged threads
        n_threads = engagement / thread.pitch
        
        # Shear area for external threads
        # As = 0.5 * π * d * Le * (0.5 + 0.577 * (d - d2))
        d = thread.nominal_diameter
        d2 = (thread.pitch_dia_min + thread.pitch_dia_max) / 2
        
        shear_area = (
            Decimal('0.5') * 
            Decimal(str(math.pi)) * 
            d * 
            engagement * 
            (Decimal('0.5') + Decimal('0.577') * (d - d2) / thread.pitch)
        )
        
        return shear_area
    
    def _get_min_engagement_ratio(self, 
                                screw_grade: str, 
                                base_material: str) -> Decimal:
        """
        Get minimum engagement ratio for reliable joint
        """
        # ISO 898-1 recommendations
        min_ratios = {
            ('8.8', 'steel'): Decimal('1.0'),
            ('10.9', 'steel'): Decimal('1.25'),
            ('12.9', 'steel'): Decimal('1.5'),
            ('8.8', 'aluminum'): Decimal('2.0'),
            ('10.9', 'aluminum'): Decimal('2.5'),
            ('A2-70', 'steel'): Decimal('1.5'),
            ('A2-70', 'aluminum'): Decimal('2.5'),
        }
        
        return min_ratios.get((screw_grade, base_material), Decimal('2.0'))
    
    def _check_tolerance_class_match(self, 
                                   external_class: str, 
                                   internal_class: str) -> str:
        """
        Check if tolerance classes are compatible
        """
        # ISO 965-1 preferred fits
        preferred_fits = {
            ('6g', '6H'): 'medium',
            ('6g', '6G'): 'medium',
            ('4g6g', '5H'): 'close',
            ('8g', '7H'): 'loose',
        }
        
        return preferred_fits.get((external_class, internal_class), 'non-standard')


# Example usage for precise technical checking
if __name__ == "__main__":
    # Define a screw
    m5_screw = PartSpec(
        part_id="DIN912-M5x16-8.8",
        thread=ThreadSpec(
            nominal_diameter=Decimal('5.0'),
            pitch=Decimal('0.8'),
            thread_class='6g',
            major_dia_min=Decimal('4.826'),
            major_dia_max=Decimal('4.976'),
            pitch_dia_min=Decimal('4.456'),
            pitch_dia_max=Decimal('4.556'),
            minor_dia_min=Decimal('4.134'),
            minor_dia_max=Decimal('4.334')
        ),
        length=Decimal('16'),
        length_tolerance_plus=Decimal('0'),
        length_tolerance_minus=Decimal('-0.5'),
        material_grade='8.8',
        tensile_strength=Decimal('800'),
        proof_load=Decimal('8.14')  # kN for M5
    )
    
    # Check compatibility with 10mm thick aluminum plate
    engine = TechnicalCompatibilityEngine(None)
    
    # Length check
    length_result = engine.check_length_compatibility(
        m5_screw,
        material_thickness=Decimal('10'),
        nut_height=Decimal('4')  # M5 nut
    )
    
    print(f"Length compatible: {length_result['length_compatible']}")
    print(f"Engagement: {length_result['engagement_length']}mm")
    print(f"Protrusion: {length_result['protrusion_min']}-{length_result['protrusion_max']}mm")
    
    # Strength check
    strength_result = engine.calculate_joint_strength(
        m5_screw,
        engagement_length=Decimal('10'),
        base_material='aluminum_6061'
    )
    
    print(f"\nAllowable load: {strength_result['allowable_load_N']}N")
    print(f"Limiting mode: {strength_result['limiting_failure_mode']}")