"""
Universal BOM Taxonomy — Part Categories
=========================================
"Every part that exists, has existed, or will exist, has a place."

Hierarchical classification system covering all mechanical, electrical,
hydraulic, pneumatic, structural, and electronic parts globally.

Category codes follow the pattern: DOMAIN.GROUP.TYPE.SUBTYPE
  e.g., MECH.FAST.BOLT.HEX  = Mechanical > Fasteners > Bolt > Hex
        ELEC.CONN.TERM.RING  = Electrical > Connectors > Terminal > Ring
        HYDR.SEAL.ORING.STAT = Hydraulic > Seals > O-Ring > Static
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class PartCategory(str, Enum):
    """Top-level part domains."""
    MECHANICAL = "MECH"
    ELECTRICAL = "ELEC"
    HYDRAULIC = "HYDR"
    PNEUMATIC = "PNEU"
    STRUCTURAL = "STRC"
    THERMAL = "THRM"
    OPTICAL = "OPTC"
    ELECTRONIC = "ELCN"
    RAW_MATERIAL = "RAWM"
    TOOLING = "TOOL"
    CONSUMABLE = "CONS"


# ---------------------------------------------------------------------------
# The Universal Taxonomy Tree
# ---------------------------------------------------------------------------
# This is the master classification. Each entry:
#   code -> (display_name, description, required_specs[], optional_specs[])
#
# required_specs: fields that MUST be populated for a quality record
# optional_specs: fields that enhance the record
# ---------------------------------------------------------------------------

TAXONOMY_TREE: Dict[str, Dict] = {
    "MECH": {
        "name": "Mechanical Components",
        "children": {
            "FAST": {
                "name": "Fasteners",
                "children": {
                    "BOLT": {
                        "name": "Bolts",
                        "required_specs": ["thread_spec", "length", "material", "head_type", "grade"],
                        "children": {
                            "HEX": {"name": "Hex Bolts"},
                            "CARR": {"name": "Carriage Bolts"},
                            "EYE": {"name": "Eye Bolts"},
                            "UBLT": {"name": "U-Bolts"},
                            "FLNG": {"name": "Flange Bolts"},
                            "STRC": {"name": "Structural Bolts"},
                            "ANCH": {"name": "Anchor Bolts"},
                        },
                    },
                    "SCRW": {
                        "name": "Screws",
                        "required_specs": ["thread_spec", "length", "material", "head_type", "drive_type"],
                        "children": {
                            "SHCS": {"name": "Socket Head Cap Screws"},
                            "BHCS": {"name": "Button Head Cap Screws"},
                            "FHCS": {"name": "Flat Head Cap Screws"},
                            "MACH": {"name": "Machine Screws"},
                            "SSET": {"name": "Set Screws / Grub Screws"},
                            "SELF": {"name": "Self-Tapping Screws"},
                            "WOOD": {"name": "Wood Screws"},
                            "DRLL": {"name": "Self-Drilling Screws"},
                            "SHLD": {"name": "Shoulder Screws"},
                            "THUM": {"name": "Thumb Screws"},
                        },
                    },
                    "NUT": {
                        "name": "Nuts",
                        "required_specs": ["thread_spec", "material", "nut_type"],
                        "children": {
                            "HEX": {"name": "Hex Nuts"},
                            "LOCK": {"name": "Lock Nuts / Nyloc"},
                            "WING": {"name": "Wing Nuts"},
                            "CAGE": {"name": "Cage Nuts"},
                            "COUP": {"name": "Coupling Nuts"},
                            "CAST": {"name": "Castle Nuts"},
                            "WELD": {"name": "Weld Nuts"},
                            "RVET": {"name": "Rivet Nuts"},
                            "TEE": {"name": "T-Nuts"},
                            "FLNG": {"name": "Flange Nuts"},
                        },
                    },
                    "WASH": {
                        "name": "Washers",
                        "required_specs": ["inner_diameter", "outer_diameter", "thickness", "material"],
                        "children": {
                            "FLAT": {"name": "Flat Washers"},
                            "LOCK": {"name": "Lock Washers"},
                            "STAR": {"name": "Star / Tooth Washers"},
                            "BELL": {"name": "Belleville / Disc Springs"},
                            "SHIM": {"name": "Shim Washers"},
                            "FELT": {"name": "Felt Washers"},
                            "RBBR": {"name": "Rubber Washers"},
                            "WAVE": {"name": "Wave Washers"},
                        },
                    },
                    "STUD": {
                        "name": "Studs & Threaded Rod",
                        "required_specs": ["thread_spec", "length", "material"],
                        "children": {
                            "FULL": {"name": "Fully Threaded Studs"},
                            "DBND": {"name": "Double-End Studs"},
                            "ROD": {"name": "Threaded Rod / Allthread"},
                        },
                    },
                    "RIVT": {
                        "name": "Rivets",
                        "required_specs": ["diameter", "grip_range", "material", "rivet_type"],
                        "children": {
                            "BLND": {"name": "Blind / Pop Rivets"},
                            "SOLD": {"name": "Solid Rivets"},
                            "DRIV": {"name": "Drive Rivets"},
                            "TBUL": {"name": "Tubular Rivets"},
                        },
                    },
                    "PIN": {
                        "name": "Pins",
                        "required_specs": ["diameter", "length", "material", "pin_type"],
                        "children": {
                            "DOWL": {"name": "Dowel Pins"},
                            "COTR": {"name": "Cotter Pins / Split Pins"},
                            "ROLL": {"name": "Roll Pins / Spring Pins"},
                            "TAPR": {"name": "Taper Pins"},
                            "CLVS": {"name": "Clevis Pins"},
                            "LNCH": {"name": "Lynch Pins / Linch Pins"},
                            "QUIK": {"name": "Quick-Release Pins"},
                        },
                    },
                    "CLMP": {
                        "name": "Clamps & Clips",
                        "children": {
                            "HOSE": {"name": "Hose Clamps"},
                            "SPRN": {"name": "Spring Clips"},
                            "ECRP": {"name": "E-Clips / Circlips"},
                            "RETG": {"name": "Retaining Rings"},
                            "CBLE": {"name": "Cable Clamps"},
                            "PIPE": {"name": "Pipe Clamps"},
                        },
                    },
                    "ANCR": {
                        "name": "Anchors",
                        "children": {
                            "EXPN": {"name": "Expansion Anchors"},
                            "WEDG": {"name": "Wedge Anchors"},
                            "DROP": {"name": "Drop-In Anchors"},
                            "TOGL": {"name": "Toggle Bolts"},
                            "CHEM": {"name": "Chemical Anchors"},
                        },
                    },
                    "INST": {
                        "name": "Inserts",
                        "children": {
                            "HELI": {"name": "Helicoil / Thread Inserts"},
                            "HEAT": {"name": "Heat-Set Inserts"},
                            "PRSS": {"name": "Press-Fit Inserts"},
                            "KYLK": {"name": "Key-Locking Inserts"},
                        },
                    },
                },
            },
            "BEAR": {
                "name": "Bearings",
                "required_specs": ["bore_diameter", "outer_diameter", "width", "bearing_type", "load_rating"],
                "children": {
                    "BALL": {
                        "name": "Ball Bearings",
                        "children": {
                            "DEEP": {"name": "Deep Groove Ball Bearings"},
                            "ANGL": {"name": "Angular Contact Ball Bearings"},
                            "THRT": {"name": "Thrust Ball Bearings"},
                            "SELF": {"name": "Self-Aligning Ball Bearings"},
                            "MINI": {"name": "Miniature Ball Bearings"},
                        },
                    },
                    "ROLL": {
                        "name": "Roller Bearings",
                        "children": {
                            "CYLR": {"name": "Cylindrical Roller Bearings"},
                            "TAPR": {"name": "Tapered Roller Bearings"},
                            "SPHC": {"name": "Spherical Roller Bearings"},
                            "NEDL": {"name": "Needle Roller Bearings"},
                        },
                    },
                    "SLEV": {"name": "Sleeve / Bushings"},
                    "LINR": {"name": "Linear Bearings"},
                    "PLOW": {"name": "Pillow Block / Mounted Bearings"},
                    "MGNT": {"name": "Magnetic Bearings"},
                },
            },
            "GEAR": {
                "name": "Gears & Power Transmission",
                "required_specs": ["pitch", "num_teeth", "bore_diameter", "material", "pressure_angle"],
                "children": {
                    "SPUR": {"name": "Spur Gears"},
                    "HELC": {"name": "Helical Gears"},
                    "BEVL": {"name": "Bevel Gears"},
                    "WORM": {"name": "Worm Gears"},
                    "RACK": {"name": "Rack & Pinion"},
                    "INTL": {"name": "Internal Gears"},
                    "TMNG": {"name": "Timing Pulleys & Belts"},
                    "CHNS": {"name": "Sprockets & Chain"},
                    "VBLT": {"name": "V-Belt Pulleys"},
                },
            },
            "SEAL": {
                "name": "Seals & Gaskets",
                "required_specs": ["inner_diameter", "outer_diameter", "material", "seal_type"],
                "children": {
                    "ORNG": {
                        "name": "O-Rings",
                        "children": {
                            "STAT": {"name": "Static O-Rings"},
                            "DYNM": {"name": "Dynamic O-Rings"},
                            "FACE": {"name": "Face Seal O-Rings"},
                        },
                    },
                    "GSKT": {
                        "name": "Gaskets",
                        "children": {
                            "HEAD": {"name": "Head Gaskets"},
                            "FLNG": {"name": "Flange Gaskets"},
                            "SPRL": {"name": "Spiral Wound Gaskets"},
                            "RING": {"name": "Ring Joint Gaskets"},
                            "CORK": {"name": "Cork Gaskets"},
                            "SHEET": {"name": "Sheet Gaskets"},
                        },
                    },
                    "LIPS": {"name": "Lip Seals / Oil Seals"},
                    "MECH": {"name": "Mechanical Seals"},
                    "PACK": {"name": "Packing / Gland Packing"},
                    "VSTR": {"name": "V-Seals / Wiper Seals"},
                    "DUST": {"name": "Dust Seals / Boots"},
                },
            },
            "SPRG": {
                "name": "Springs",
                "required_specs": ["spring_type", "wire_diameter", "outer_diameter", "free_length", "spring_rate", "material"],
                "children": {
                    "COMP": {"name": "Compression Springs"},
                    "TENS": {"name": "Tension / Extension Springs"},
                    "TORS": {"name": "Torsion Springs"},
                    "WAVE": {"name": "Wave Springs"},
                    "DISC": {"name": "Disc / Belleville Springs"},
                    "CONS": {"name": "Constant Force Springs"},
                    "GAS": {"name": "Gas Springs"},
                    "LEAF": {"name": "Leaf Springs"},
                },
            },
            "SHFT": {
                "name": "Shafts & Couplings",
                "required_specs": ["diameter", "length", "material"],
                "children": {
                    "SHFT": {"name": "Shafts / Axles"},
                    "COUP": {"name": "Shaft Couplings"},
                    "UJNT": {"name": "Universal Joints"},
                    "CVJT": {"name": "CV Joints"},
                    "KEYY": {"name": "Keys & Keystock"},
                    "SPLN": {"name": "Splines"},
                    "COLL": {"name": "Shaft Collars"},
                },
            },
            "BELT": {
                "name": "Belts & Chains",
                "children": {
                    "VBLT": {"name": "V-Belts"},
                    "TMNG": {"name": "Timing Belts"},
                    "FLAT": {"name": "Flat Belts"},
                    "POLY": {"name": "Poly-V / Ribbed Belts"},
                    "ROLR": {"name": "Roller Chain"},
                    "SILR": {"name": "Silent / Inverted Tooth Chain"},
                },
            },
            "PIPE": {
                "name": "Pipe & Tube Fittings",
                "required_specs": ["nominal_size", "material", "connection_type", "pressure_rating"],
                "children": {
                    "PIPE": {"name": "Pipe"},
                    "TUBE": {"name": "Tubing"},
                    "ELBW": {"name": "Elbows"},
                    "TEE": {"name": "Tees"},
                    "REDX": {"name": "Reducers"},
                    "UNON": {"name": "Unions"},
                    "CPLN": {"name": "Couplings"},
                    "NPLE": {"name": "Nipples"},
                    "PLUG": {"name": "Plugs & Caps"},
                    "FLNG": {"name": "Flanges"},
                    "VALV": {"name": "Valves"},
                    "STRN": {"name": "Strainers / Filters"},
                    "QUIK": {"name": "Quick-Connect Fittings"},
                },
            },
            "LNMO": {
                "name": "Linear Motion",
                "children": {
                    "RAIL": {"name": "Linear Rails / Guides"},
                    "BSCW": {"name": "Ball Screws"},
                    "LDSCW": {"name": "Lead Screws"},
                    "ACTR": {"name": "Linear Actuators"},
                    "SLDE": {"name": "Linear Slides"},
                },
            },
        },
    },
    "ELEC": {
        "name": "Electrical Components",
        "children": {
            "CONN": {
                "name": "Connectors",
                "required_specs": ["connector_type", "pin_count", "voltage_rating", "current_rating"],
                "children": {
                    "TERM": {"name": "Terminals"},
                    "PLUG": {"name": "Plugs & Sockets"},
                    "CIRC": {"name": "Circular Connectors"},
                    "RECT": {"name": "Rectangular Connectors"},
                    "EDGE": {"name": "Edge / Card Connectors"},
                    "COAX": {"name": "Coaxial Connectors"},
                    "FIBR": {"name": "Fiber Optic Connectors"},
                    "AUTM": {"name": "Automotive Connectors"},
                },
            },
            "WIRE": {
                "name": "Wire & Cable",
                "required_specs": ["gauge_awg", "conductor_material", "insulation", "voltage_rating"],
                "children": {
                    "HOOK": {"name": "Hook-Up Wire"},
                    "POWR": {"name": "Power Cable"},
                    "COAX": {"name": "Coaxial Cable"},
                    "RBON": {"name": "Ribbon Cable"},
                    "SHLD": {"name": "Shielded Cable"},
                    "FLEX": {"name": "Flex Cable"},
                    "HARN": {"name": "Wire Harnesses"},
                },
            },
            "PROT": {
                "name": "Circuit Protection",
                "children": {
                    "FUSE": {"name": "Fuses"},
                    "BRKR": {"name": "Circuit Breakers"},
                    "SURG": {"name": "Surge Protectors"},
                    "THML": {"name": "Thermal Cutoffs"},
                },
            },
            "SWTC": {
                "name": "Switches & Relays",
                "children": {
                    "TOGL": {"name": "Toggle Switches"},
                    "PUSH": {"name": "Pushbutton Switches"},
                    "ROTQ": {"name": "Rotary Switches"},
                    "LMIT": {"name": "Limit Switches"},
                    "PROX": {"name": "Proximity Switches"},
                    "RELY": {"name": "Relays"},
                    "CNTR": {"name": "Contactors"},
                },
            },
            "MOTR": {
                "name": "Motors & Drives",
                "required_specs": ["motor_type", "voltage", "power_watts", "rpm", "frame_size"],
                "children": {
                    "DCMT": {"name": "DC Motors"},
                    "ACMT": {"name": "AC Motors"},
                    "STEP": {"name": "Stepper Motors"},
                    "SERV": {"name": "Servo Motors"},
                    "BLDC": {"name": "Brushless DC Motors"},
                    "GEAR": {"name": "Gear Motors"},
                    "DRVE": {"name": "Variable Frequency Drives"},
                },
            },
            "TRNS": {
                "name": "Transformers & Power Supply",
                "children": {
                    "XFMR": {"name": "Transformers"},
                    "PSUP": {"name": "Power Supplies"},
                    "CONV": {"name": "DC-DC Converters"},
                    "INVT": {"name": "Inverters"},
                    "BATT": {"name": "Batteries"},
                    "CHRG": {"name": "Chargers"},
                },
            },
        },
    },
    "HYDR": {
        "name": "Hydraulic Components",
        "children": {
            "PUMP": {
                "name": "Hydraulic Pumps",
                "required_specs": ["pump_type", "displacement_cc", "pressure_rating_bar", "rpm"],
                "children": {
                    "GEAR": {"name": "Gear Pumps"},
                    "VANE": {"name": "Vane Pumps"},
                    "PSTN": {"name": "Piston Pumps"},
                },
            },
            "CYLR": {
                "name": "Hydraulic Cylinders",
                "required_specs": ["bore_diameter", "rod_diameter", "stroke", "pressure_rating"],
                "children": {
                    "SNGL": {"name": "Single Acting"},
                    "DBLE": {"name": "Double Acting"},
                    "TLSC": {"name": "Telescopic"},
                },
            },
            "VALV": {
                "name": "Hydraulic Valves",
                "children": {
                    "DRCT": {"name": "Directional Control Valves"},
                    "PRSS": {"name": "Pressure Control Valves"},
                    "FLOW": {"name": "Flow Control Valves"},
                    "CHCK": {"name": "Check Valves"},
                    "PROP": {"name": "Proportional Valves"},
                    "SERV": {"name": "Servo Valves"},
                },
            },
            "FILT": {"name": "Hydraulic Filters"},
            "RSRV": {"name": "Reservoirs / Tanks"},
            "HOSE": {
                "name": "Hydraulic Hoses & Fittings",
                "children": {
                    "HOSE": {"name": "Hoses"},
                    "FTTG": {"name": "Fittings"},
                    "ADPT": {"name": "Adapters"},
                    "QUIK": {"name": "Quick Disconnects"},
                },
            },
            "SEAL": {"name": "Hydraulic Seals"},
            "ACUM": {"name": "Accumulators"},
        },
    },
    "PNEU": {
        "name": "Pneumatic Components",
        "children": {
            "CYLR": {
                "name": "Pneumatic Cylinders",
                "required_specs": ["bore_diameter", "stroke", "pressure_rating", "port_size"],
                "children": {
                    "SNGL": {"name": "Single Acting"},
                    "DBLE": {"name": "Double Acting"},
                    "RDLS": {"name": "Rodless Cylinders"},
                    "COMP": {"name": "Compact Cylinders"},
                    "GDRN": {"name": "Guided Cylinders"},
                },
            },
            "VALV": {
                "name": "Pneumatic Valves",
                "children": {
                    "SOLN": {"name": "Solenoid Valves"},
                    "MECH": {"name": "Mechanical Valves"},
                    "REGR": {"name": "Regulators"},
                    "FLTR": {"name": "Filter-Regulator-Lubricator (FRL)"},
                },
            },
            "FTTG": {
                "name": "Pneumatic Fittings & Tubing",
                "children": {
                    "PUSH": {"name": "Push-to-Connect Fittings"},
                    "BARB": {"name": "Barb Fittings"},
                    "TUBE": {"name": "Pneumatic Tubing"},
                    "MNFL": {"name": "Manifolds"},
                },
            },
            "COMP": {"name": "Compressors"},
            "DRYR": {"name": "Air Dryers"},
            "MUFL": {"name": "Mufflers / Silencers"},
            "VACU": {"name": "Vacuum Components"},
        },
    },
    "STRC": {
        "name": "Structural Components",
        "children": {
            "BEAM": {
                "name": "Structural Shapes",
                "required_specs": ["profile_type", "material", "dimensions"],
                "children": {
                    "IBEM": {"name": "I-Beams / W-Shapes"},
                    "CHNL": {"name": "Channels"},
                    "ANGL": {"name": "Angles"},
                    "SQTB": {"name": "Square Tubing"},
                    "RDTB": {"name": "Round Tubing"},
                    "RCTB": {"name": "Rectangular Tubing"},
                    "TBAR": {"name": "T-Bars"},
                    "FLAT": {"name": "Flat Bar"},
                    "RBAR": {"name": "Round Bar"},
                },
            },
            "PLAT": {
                "name": "Sheet & Plate",
                "required_specs": ["material", "thickness", "width", "length"],
                "children": {
                    "SHMT": {"name": "Sheet Metal"},
                    "PLTE": {"name": "Plate"},
                    "CHKR": {"name": "Checker / Diamond Plate"},
                    "PERF": {"name": "Perforated Sheet"},
                    "EXPN": {"name": "Expanded Metal"},
                    "MESH": {"name": "Wire Mesh"},
                },
            },
            "XTRN": {
                "name": "Extrusions",
                "children": {
                    "8020": {"name": "80/20 Style T-Slot"},
                    "CSTM": {"name": "Custom Extrusions"},
                    "RAIL": {"name": "Rail Extrusions"},
                },
            },
            "BRCKT": {
                "name": "Brackets & Mounting",
                "children": {
                    "ANGL": {"name": "Angle Brackets"},
                    "GUST": {"name": "Gussets"},
                    "MNTP": {"name": "Mounting Plates"},
                    "UBOT": {"name": "U-Brackets"},
                    "STND": {"name": "Standoffs"},
                },
            },
        },
    },
    "THRM": {
        "name": "Thermal Management",
        "children": {
            "HTEX": {
                "name": "Heat Exchangers",
                "children": {
                    "RDTR": {"name": "Radiators"},
                    "COOL": {"name": "Coolers / Intercoolers"},
                    "PLTE": {"name": "Plate Heat Exchangers"},
                    "SHEL": {"name": "Shell & Tube"},
                },
            },
            "HTSK": {"name": "Heat Sinks"},
            "FANS": {
                "name": "Fans & Blowers",
                "children": {
                    "AXLF": {"name": "Axial Fans"},
                    "CENT": {"name": "Centrifugal Blowers"},
                    "CRSS": {"name": "Cross-Flow Fans"},
                },
            },
            "INSL": {
                "name": "Thermal Insulation",
                "children": {
                    "WRAP": {"name": "Heat Wrap / Tape"},
                    "SLVE": {"name": "Thermal Sleeves"},
                    "BLNK": {"name": "Thermal Blankets"},
                    "PADS": {"name": "Thermal Pads"},
                },
            },
            "HTER": {"name": "Heaters & Heating Elements"},
            "TEPS": {"name": "Thermocouples & Temperature Sensors"},
        },
    },
    "ELCN": {
        "name": "Electronic Components",
        "children": {
            "PASS": {
                "name": "Passive Components",
                "children": {
                    "RSTR": {"name": "Resistors"},
                    "CAPR": {"name": "Capacitors"},
                    "INDR": {"name": "Inductors"},
                    "XTAL": {"name": "Crystals & Oscillators"},
                },
            },
            "SEMI": {
                "name": "Semiconductors",
                "children": {
                    "DIOD": {"name": "Diodes"},
                    "TRNS": {"name": "Transistors"},
                    "IC": {"name": "Integrated Circuits"},
                    "OPAM": {"name": "Op-Amps"},
                    "VREG": {"name": "Voltage Regulators"},
                    "MCU": {"name": "Microcontrollers"},
                    "FPGA": {"name": "FPGAs"},
                },
            },
            "SENS": {
                "name": "Sensors",
                "children": {
                    "TEMP": {"name": "Temperature Sensors"},
                    "PRES": {"name": "Pressure Sensors"},
                    "ACCL": {"name": "Accelerometers"},
                    "GYRO": {"name": "Gyroscopes"},
                    "PROX": {"name": "Proximity Sensors"},
                    "PHOT": {"name": "Photodetectors"},
                    "FORC": {"name": "Force / Load Cells"},
                    "FLOW": {"name": "Flow Sensors"},
                    "LEVL": {"name": "Level Sensors"},
                },
            },
            "DSPL": {
                "name": "Displays",
                "children": {
                    "LCD": {"name": "LCD Displays"},
                    "OLED": {"name": "OLED Displays"},
                    "LED": {"name": "LED Indicators"},
                    "SEGM": {"name": "7-Segment Displays"},
                },
            },
            "PCB": {
                "name": "PCB & Prototyping",
                "children": {
                    "BARE": {"name": "Bare PCBs"},
                    "PROT": {"name": "Prototyping Boards"},
                    "BRDG": {"name": "Breakout Boards"},
                },
            },
        },
    },
    "RAWM": {
        "name": "Raw Materials & Stock",
        "children": {
            "METL": {
                "name": "Metals",
                "required_specs": ["alloy", "form", "dimensions", "temper"],
                "children": {
                    "ALUM": {"name": "Aluminum"},
                    "STEL": {"name": "Steel"},
                    "STLS": {"name": "Stainless Steel"},
                    "BRAS": {"name": "Brass"},
                    "BRNZ": {"name": "Bronze"},
                    "COPR": {"name": "Copper"},
                    "TITN": {"name": "Titanium"},
                    "NCKL": {"name": "Nickel Alloys"},
                    "CAST": {"name": "Cast Iron"},
                },
            },
            "PLST": {
                "name": "Plastics & Polymers",
                "required_specs": ["polymer_type", "form", "dimensions"],
                "children": {
                    "ABS": {"name": "ABS"},
                    "NYLON": {"name": "Nylon / Polyamide"},
                    "PTFE": {"name": "PTFE / Teflon"},
                    "DELN": {"name": "Delrin / Acetal / POM"},
                    "PEEK": {"name": "PEEK"},
                    "POLY": {"name": "Polycarbonate"},
                    "UHMW": {"name": "UHMW-PE"},
                    "ACRL": {"name": "Acrylic"},
                    "PVC": {"name": "PVC"},
                },
            },
            "RUBR": {
                "name": "Rubber & Elastomers",
                "children": {
                    "NITR": {"name": "Nitrile / Buna-N"},
                    "VITN": {"name": "Viton / FKM"},
                    "EPDM": {"name": "EPDM"},
                    "SLCN": {"name": "Silicone"},
                    "NPRN": {"name": "Neoprene"},
                    "NATL": {"name": "Natural Rubber"},
                },
            },
            "COMP": {
                "name": "Composites",
                "children": {
                    "CFRP": {"name": "Carbon Fiber"},
                    "GFRP": {"name": "Fiberglass"},
                    "KVLR": {"name": "Kevlar / Aramid"},
                },
            },
            "CERM": {"name": "Ceramics & Glass"},
            "WOOD": {"name": "Wood & Lumber"},
            "FOAM": {"name": "Foam & Sponge"},
            "ADHV": {
                "name": "Adhesives & Sealants",
                "children": {
                    "EPXY": {"name": "Epoxy"},
                    "CYAN": {"name": "Cyanoacrylate / Super Glue"},
                    "THRD": {"name": "Thread Locker"},
                    "SLNT": {"name": "Silicone Sealant"},
                    "ANRB": {"name": "Anaerobic"},
                    "STRL": {"name": "Structural Adhesive"},
                },
            },
        },
    },
    "TOOL": {
        "name": "Tooling & Workholding",
        "children": {
            "CUTT": {
                "name": "Cutting Tools",
                "children": {
                    "DRLL": {"name": "Drill Bits"},
                    "EMILL": {"name": "End Mills"},
                    "TAPS": {"name": "Taps"},
                    "DIES": {"name": "Dies"},
                    "REAM": {"name": "Reamers"},
                    "INSRT": {"name": "Carbide Inserts"},
                    "SAWB": {"name": "Saw Blades"},
                    "BRRR": {"name": "Burrs / Deburring"},
                },
            },
            "HOLD": {
                "name": "Workholding",
                "children": {
                    "VISE": {"name": "Vises"},
                    "CHUK": {"name": "Chucks"},
                    "CLMP": {"name": "Clamps"},
                    "FIXT": {"name": "Fixtures"},
                    "COLR": {"name": "Collets"},
                    "ARBS": {"name": "Arbors & Mandrels"},
                },
            },
            "MSRG": {
                "name": "Measuring & Gauging",
                "children": {
                    "CALP": {"name": "Calipers"},
                    "MICR": {"name": "Micrometers"},
                    "GUGE": {"name": "Gauges"},
                    "INDQ": {"name": "Indicators"},
                    "LEVL": {"name": "Levels"},
                },
            },
            "ABRS": {
                "name": "Abrasives",
                "children": {
                    "GWHEEL": {"name": "Grinding Wheels"},
                    "SANDP": {"name": "Sandpaper / Sanding Discs"},
                    "FLAP": {"name": "Flap Discs"},
                    "BUFF": {"name": "Buffing Wheels"},
                },
            },
        },
    },
    "CONS": {
        "name": "Consumables & Supplies",
        "children": {
            "LUBR": {
                "name": "Lubricants",
                "children": {
                    "OIL": {"name": "Oils"},
                    "GRES": {"name": "Greases"},
                    "DRYL": {"name": "Dry Lubricants"},
                    "PNTR": {"name": "Penetrating Oil"},
                    "ANTI": {"name": "Anti-Seize"},
                },
            },
            "WELD": {
                "name": "Welding Supplies",
                "children": {
                    "WIRE": {"name": "Welding Wire"},
                    "ROD": {"name": "Welding Rod"},
                    "FLUX": {"name": "Flux"},
                    "GAS": {"name": "Shielding Gas"},
                    "TIPS": {"name": "Contact Tips & Nozzles"},
                },
            },
            "TAPE": {
                "name": "Tapes & Films",
                "children": {
                    "ELEC": {"name": "Electrical Tape"},
                    "MASK": {"name": "Masking Tape"},
                    "KPTN": {"name": "Kapton / Polyimide Tape"},
                    "SHRT": {"name": "Heat Shrink Tubing"},
                },
            },
            "SAFE": {
                "name": "Safety & PPE",
                "children": {
                    "GLOV": {"name": "Gloves"},
                    "EYEP": {"name": "Eye Protection"},
                    "RESP": {"name": "Respirators"},
                    "EARP": {"name": "Hearing Protection"},
                },
            },
        },
    },
    "OPTC": {
        "name": "Optical Components",
        "children": {
            "LENS": {"name": "Lenses"},
            "MIRR": {"name": "Mirrors"},
            "FLTR": {"name": "Optical Filters"},
            "FIBR": {"name": "Fiber Optics"},
            "LASR": {"name": "Laser Components"},
            "MNTS": {"name": "Optical Mounts"},
        },
    },
}


@dataclass
class TaxonomyNode:
    """A node in the taxonomy tree."""
    code: str
    name: str
    full_code: str  # e.g., "MECH.FAST.BOLT.HEX"
    depth: int
    parent_code: Optional[str] = None
    required_specs: List[str] = field(default_factory=list)
    children: Dict[str, "TaxonomyNode"] = field(default_factory=dict)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def path(self) -> List[str]:
        return self.full_code.split(".")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "full_code": self.full_code,
            "depth": self.depth,
            "parent_code": self.parent_code,
            "required_specs": self.required_specs,
            "is_leaf": self.is_leaf,
            "children": {k: v.to_dict() for k, v in self.children.items()},
        }


class PartTaxonomy:
    """
    The Universal Parts Taxonomy.

    Provides hierarchical classification, lookup, search, and
    validation for all part categories globally.
    """

    def __init__(self):
        self._root: Dict[str, TaxonomyNode] = {}
        self._flat_index: Dict[str, TaxonomyNode] = {}
        self._build_tree(TAXONOMY_TREE)

    def _build_tree(
        self,
        tree: Dict[str, Dict],
        parent_code: str = "",
        depth: int = 0,
        inherited_specs: Optional[List[str]] = None,
    ) -> None:
        """Recursively build taxonomy tree from definition."""
        for code, data in tree.items():
            full_code = f"{parent_code}.{code}" if parent_code else code
            specs = data.get("required_specs", inherited_specs or [])

            node = TaxonomyNode(
                code=code,
                name=data["name"],
                full_code=full_code,
                depth=depth,
                parent_code=parent_code or None,
                required_specs=specs,
            )

            # Register in flat index
            self._flat_index[full_code] = node

            # Add to parent or root
            if parent_code:
                parent = self._flat_index.get(parent_code)
                if parent:
                    parent.children[code] = node
            else:
                self._root[code] = node

            # Process children
            if "children" in data:
                self._build_tree(
                    data["children"],
                    parent_code=full_code,
                    depth=depth + 1,
                    inherited_specs=specs,
                )

    def get(self, code: str) -> Optional[TaxonomyNode]:
        """Get a taxonomy node by its full code (e.g., 'MECH.FAST.BOLT.HEX')."""
        return self._flat_index.get(code)

    def get_children(self, code: str) -> List[TaxonomyNode]:
        """Get all direct children of a node."""
        node = self._flat_index.get(code)
        if node:
            return list(node.children.values())
        return []

    def get_leaves(self, code: str = "") -> List[TaxonomyNode]:
        """Get all leaf nodes under a given code (or all if empty)."""
        leaves = []
        if code:
            node = self._flat_index.get(code)
            if not node:
                return []
            self._collect_leaves(node, leaves)
        else:
            for root_node in self._root.values():
                self._collect_leaves(root_node, leaves)
        return leaves

    def _collect_leaves(self, node: TaxonomyNode, leaves: List[TaxonomyNode]) -> None:
        if node.is_leaf:
            leaves.append(node)
        else:
            for child in node.children.values():
                self._collect_leaves(child, leaves)

    def search(self, query: str) -> List[TaxonomyNode]:
        """Search taxonomy by name or code (case-insensitive)."""
        query_lower = query.lower()
        results = []
        for full_code, node in self._flat_index.items():
            if (
                query_lower in node.name.lower()
                or query_lower in full_code.lower()
                or query_lower in node.code.lower()
            ):
                results.append(node)
        return results

    def classify(self, description: str) -> List[Tuple[TaxonomyNode, float]]:
        """
        Classify a part description into taxonomy categories.

        Returns list of (node, confidence) tuples sorted by confidence.
        """
        desc_lower = description.lower()
        scores: Dict[str, float] = {}

        # Keyword matching against taxonomy names
        for full_code, node in self._flat_index.items():
            name_words = set(node.name.lower().split())
            desc_words = set(desc_lower.split())

            # Calculate overlap
            overlap = name_words & desc_words
            if overlap:
                # Score based on overlap ratio and depth (prefer more specific)
                score = len(overlap) / len(name_words)
                # Boost deeper nodes (more specific classification)
                score *= (1 + node.depth * 0.2)
                scores[full_code] = score

        # Sort by score descending
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [
            (self._flat_index[code], score)
            for code, score in sorted_results[:10]
        ]

    def get_required_specs(self, code: str) -> List[str]:
        """Get the required specifications for a taxonomy code."""
        node = self._flat_index.get(code)
        if node:
            return node.required_specs
        return []

    def validate_classification(self, code: str) -> bool:
        """Check if a taxonomy code is valid."""
        return code in self._flat_index

    @property
    def domains(self) -> List[TaxonomyNode]:
        """Get all top-level domains."""
        return list(self._root.values())

    @property
    def total_categories(self) -> int:
        """Total number of categories in the taxonomy."""
        return len(self._flat_index)

    def stats(self) -> Dict[str, Any]:
        """Get taxonomy statistics."""
        domains = len(self._root)
        total = len(self._flat_index)
        leaves = len(self.get_leaves())
        max_depth = max((n.depth for n in self._flat_index.values()), default=0)

        return {
            "domains": domains,
            "total_categories": total,
            "leaf_categories": leaves,
            "max_depth": max_depth,
            "domain_breakdown": {
                code: {
                    "name": node.name,
                    "categories": sum(
                        1 for fc in self._flat_index
                        if fc.startswith(code)
                    ),
                }
                for code, node in self._root.items()
            },
        }

    def export_json(self, path: Optional[Path] = None) -> str:
        """Export taxonomy as JSON."""
        data = {
            "version": "1.0.0",
            "stats": self.stats(),
            "tree": {code: node.to_dict() for code, node in self._root.items()},
        }
        output = json.dumps(data, indent=2)
        if path:
            path.write_text(output)
        return output


# Singleton taxonomy instance
_taxonomy: Optional[PartTaxonomy] = None


def get_taxonomy() -> PartTaxonomy:
    """Get the global taxonomy instance."""
    global _taxonomy
    if _taxonomy is None:
        _taxonomy = PartTaxonomy()
    return _taxonomy
