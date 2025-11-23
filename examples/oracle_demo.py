#!/usr/bin/env python3
"""
ORACLE Demo - Compatibility Oracle Examples
============================================

Demonstrates the mathematical truth of ORACLE:
"Will it fit? Will it hold? Will it fail?"

Agent_2: The Prophet of Perfect Fit

Usage:
    python examples/oracle_demo.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.oracle.deploy import (
    deploy_oracle,
    quick_thread_check,
    quick_galvanic_check,
)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_thread_compatibility():
    """Demonstrate thread compatibility checking."""
    print_header("THREAD COMPATIBILITY")

    print("\n\"Will it fit?\" - The eternal question of threaded fasteners.\n")

    # Common metric thread examples
    threads = [
        (8, 1.25, "M8x1.25 (standard)"),
        (10, 1.5, "M10x1.5 (standard)"),
        (8, 1.0, "M8x1.0 (fine)"),
        (12, 1.75, "M12x1.75 (standard)"),
    ]

    for diameter, pitch, description in threads:
        result = quick_thread_check(diameter, pitch)
        status = "PASS" if result['is_compatible'] else "FAIL"
        quality = result['engagement_quality'].upper()
        print(f"  {description}")
        print(f"    Status: [{status}] Engagement: {quality}")
        print(f"    Clearance: {result['clearance_min_mm']:.4f} - {result['clearance_max_mm']:.4f} mm")
        print()


def demo_galvanic_compatibility():
    """Demonstrate galvanic corrosion risk assessment."""
    print_header("GALVANIC CORROSION RISK")

    print("\n\"Will it last?\" - Material pairing determines longevity.\n")

    # Common material combinations
    combinations = [
        ("steel", "steel", "indoor"),
        ("steel", "aluminum", "indoor"),
        ("steel", "aluminum", "marine"),
        ("stainless_304", "stainless_316", "outdoor"),
        ("stainless_304", "aluminum", "marine"),
        ("brass", "copper", "indoor"),
        ("aluminum", "titanium", "marine"),
    ]

    for mat_a, mat_b, env in combinations:
        result = quick_galvanic_check(mat_a, mat_b, env)
        risk = result['risk_level']

        # Visual risk indicator
        indicators = {
            "SAFE": "[====]",
            "LOW": "[=== ]",
            "MODERATE": "[==  ]",
            "SEVERE": "[=   ]",
        }
        indicator = indicators.get(risk, "[????]")

        print(f"  {mat_a} + {mat_b} ({env})")
        print(f"    Risk: {indicator} {risk}")
        print()


def demo_safety_factors():
    """Demonstrate safety factor calculations."""
    print_header("SAFETY FACTOR ANALYSIS")

    print("\n\"Will it hold?\" - Numbers that determine structural integrity.\n")

    oracle = deploy_oracle()

    # Example load cases
    cases = [
        (50.0, 20.0, "static", "Structural bolt"),
        (50.0, 20.0, "cyclic", "Vibrating equipment"),
        (50.0, 20.0, "impact", "Crash-loaded component"),
        (100.0, 25.0, "static", "Engine mount"),
        (30.0, 25.0, "static", "Marginal case"),
    ]

    for proof, applied, load_type, description in cases:
        result = oracle.calculate_safety_factor(proof, applied, load_type)
        status = "PASS" if result['is_adequate'] else "FAIL"
        sf = result['safety_factor']
        margin = result['margin_percent']

        print(f"  {description} ({load_type})")
        print(f"    Proof: {proof}kN, Applied: {applied}kN")
        print(f"    Safety Factor: {sf} (min: {result['minimum_required']})")
        print(f"    Status: [{status}] Margin: {margin:+.1f}%")
        print()


def demo_full_compatibility_check():
    """Demonstrate full part compatibility analysis."""
    print_header("FULL COMPATIBILITY CHECK")

    print("\n\"Will it work?\" - Complete analysis of a fastener application.\n")

    oracle = deploy_oracle()

    # Define an M8x1.25 Grade 8.8 bolt
    bolt = {
        "id": "BOLT-M8-25-88",
        "part_number": "M8x25-8.8",
        "category": "fastener",
        "thread": {
            "diameter": 8,
            "pitch": 1.25,
            "class": "6g",
        },
        "material": {
            "type": "steel",
            "grade": "8.8",
            "tensile_mpa": 800,
            "yield_mpa": 640,
            "shear_mpa": 460,
        },
    }

    # Define a mating nut
    nut = {
        "id": "NUT-M8-88",
        "part_number": "M8-8",
        "category": "fastener",
        "thread": {
            "diameter": 8,
            "pitch": 1.25,
            "class": "6H",
        },
        "material": {
            "type": "steel",
            "grade": "8",
            "tensile_mpa": 800,
            "yield_mpa": 640,
            "shear_mpa": 460,
        },
    }

    # Define assembly context
    context = {
        "thickness": 15,
        "load_kn": 10,
        "environment": "outdoor",
    }

    print("  Checking: M8x25 Grade 8.8 bolt + M8 Grade 8 nut")
    print("  Application: 15mm joint, 10kN load, outdoor environment")
    print()

    result = oracle.check_compatibility(bolt, nut, context)

    print(f"  Result: {'COMPATIBLE' if result['is_compatible'] else 'INCOMPATIBLE'}")
    print(f"  Confidence: {result['confidence']*100:.1f}%")
    print(f"  Type: {result['compatibility_type']}")

    if result.get('warnings'):
        print("  Warnings:")
        for w in result['warnings']:
            print(f"    - {w}")

    if result.get('recommendations'):
        print("  Recommendations:")
        for r in result['recommendations']:
            print(f"    - {r}")
    print()


def demo_substitution():
    """Demonstrate substitution finding."""
    print_header("SUBSTITUTION SEARCH")

    print("\n\"What else will work?\" - Finding alternatives when needed.\n")

    oracle = deploy_oracle()

    # Target part to find substitutes for
    target = {
        "part_id": "M8x25-A2-70",
        "category": "fastener",
        "thread_size": "M8x1.25",
        "material": "stainless_304",
        "grade": "A2-70",
        "length": 25,
    }

    print("  Finding substitutes for: M8x25 A2-70 Stainless")
    print()

    # Note: Full substitution requires database
    # This demonstrates the interface
    try:
        subs = oracle.find_substitutions(target, max_results=5)
        if subs:
            for i, sub in enumerate(subs, 1):
                print(f"    {i}. {sub.get('part_id', 'Unknown')} (Score: {sub.get('score', 0):.2f})")
        else:
            print("    No substitutions found (database not populated)")
    except Exception:
        print("    Substitution search requires populated database")
        print("    The ORACLE is ready - feed it data!")
    print()


def main():
    """Run the ORACLE demonstration."""
    print("\n" + "=" * 60)
    print(" ORACLE - THE COMPATIBILITY ORACLE (Agent_2)")
    print("=" * 60)
    print()
    print("\"Will it fit? Will it hold? Will it fail?")
    print("These questions haunt every engineer. I am the answer.\"")
    print()
    print("Compatibility is not subjective. It is physics.")
    print("It is mathematics. It is the relationship between")
    print("dimensions, materials, and forces.")
    print()
    print("-" * 60)
    print(" DEMONSTRATION OF MATHEMATICAL TRUTH")
    print("-" * 60)

    demo_thread_compatibility()
    demo_galvanic_compatibility()
    demo_safety_factors()
    demo_full_compatibility_check()
    demo_substitution()

    print_header("ORACLE DEPLOYED")
    print()
    print("The ORACLE is listening. Query with numbers, receive truth.")
    print()
    print("CLI Usage:")
    print("  python upc.py oracle                    # Status")
    print("  python upc.py oracle-thread 8 1.25     # Thread check")
    print("  python upc.py oracle-galvanic steel aluminum  # Galvanic")
    print("  python upc.py oracle-safety 50 20      # Safety factor")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
