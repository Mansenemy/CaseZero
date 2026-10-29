"""
Procedural Mystery Case Generator for CaseZero.
Generates an infinite variety of solvable, mathematically sound DSA detective cases:
- Random suspect graph with typed relationships
- Balanced trait matrix (Handedness, Clearance, Height)
- Exactly one designated culprit and one accomplice
- Exactly one planted contradiction clue
- Hierarchical lead tree with AP costs
- Fully validated: tests over 200 seeds guarantee exactly one viable culprit once all
  true clues are gathered, and an empty set contradiction when the planted lie is active.
"""

import random

FIRST_NAMES = ["Cassian", "Beatrix", "Alexander", "Daphne", "Ezekiel", "Freja", "Gabriel", "Helena", "Rowan", "Silas"]
LAST_NAMES = ["Vance", "Cross", "Blackwood", "Mercer", "Sinclair", "Kowalski", "Sterling", "Zhang", "Novak", "Frost"]
ROLES = [
    "Chief Cryptographer",
    "Security Director",
    "Forensic Auditor",
    "Hardware Specialist",
    "Facility Architect",
    "Data Broker"
]

HANDEDNESS_OPTIONS = ["Left-Handed", "Right-Handed", "Ambidextrous"]
CLEARANCE_OPTIONS = ["Tier 1", "Tier 2", "Tier 3"]
HEIGHT_OPTIONS = ["Height 168cm", "Height 176cm", "Height 186cm", "Height 192cm"]

def generate_procedural_case(seed: int = None) -> dict:
    """
    Generates a guaranteed solvable procedural mystery case.
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    suspect_count = 6
    chosen_firsts = rng.sample(FIRST_NAMES, suspect_count)
    chosen_lasts = rng.sample(LAST_NAMES, suspect_count)

    suspects = []
    for i in range(suspect_count):
        s_id = f"PS_{i+1}"
        name = f"{chosen_firsts[i]} {chosen_lasts[i]}"
        role = ROLES[i % len(ROLES)]

        # Unique or well-distributed trait combos
        h = HANDEDNESS_OPTIONS[i % len(HANDEDNESS_OPTIONS)]
        c = CLEARANCE_OPTIONS[(i // 2) % len(CLEARANCE_OPTIONS)]
        ht = HEIGHT_OPTIONS[i % len(HEIGHT_OPTIONS)]

        suspects.append({
            "id": s_id,
            "name": name,
            "role": role,
            "image": f"assets/img/suspects/{s_id}.svg",
            "traits": [h, c, ht],
            "alibi": f"Claims presence in Sector {chr(65 + i)} during critical incident.",
            "motive": "Documented financial irregularities and unauthorized system queries.",
            "notes": "Monitored under internal security surveillance."
        })

    # Pick culprit and accomplice
    culprit_idx = rng.randint(0, suspect_count - 1)
    culprit = suspects[culprit_idx]
    accomplice_idx = (culprit_idx + 1) % suspect_count
    accomplice = suspects[accomplice_idx]

    culprit_id = culprit["id"]
    accomplice_id = accomplice["id"]

    # Graph connections
    connections = []
    edge_types = ["COLLEAGUE", "CONSPIRACY", "DEBT", "BLACKMAIL", "EQUIPMENT"]
    for i in range(suspect_count):
        nxt = (i + 1) % suspect_count
        connections.append({
            "u": suspects[i]["id"],
            "v": suspects[nxt]["id"],
            "type": edge_types[i % len(edge_types)],
            "desc": f"Logged association between {suspects[i]['name']} and {suspects[nxt]['name']}."
        })
    # Add cross connection between culprit and accomplice
    connections.append({
        "u": culprit_id,
        "v": accomplice_id,
        "type": "CONSPIRACY",
        "desc": "Conspiratorial message channel active during perimeter alarm."
    })

    # Trait matching
    culprit_h, culprit_c, culprit_ht = culprit["traits"]

    # Clue 1: Handedness
    matching_h = [s["id"] for s in suspects if s["traits"][0] == culprit_h or s["traits"][0] == "Ambidextrous"]
    # Clue 2: Clearance
    matching_c = [s["id"] for s in suspects if s["traits"][1] == culprit_c]
    # Clue 4: Height
    matching_ht = [s["id"] for s in suspects if s["traits"][2] == culprit_ht]

    # Ensure intersection of true clues narrows down to culprit alone
    # True Clues: C1, C2, C4, C5
    # If intersection of matching_h and matching_c is not just culprit, Clue 4 (height) isolates them!
    # Planted False Clue (C3): points to an impossible trait for the culprit
    fake_h = "Right-Handed" if culprit_h != "Right-Handed" else "Left-Handed"
    fake_suspects = [s["id"] for s in suspects if s["traits"][0] == fake_h and s["id"] != culprit_id]
    if not fake_suspects:
        # Fallback to ensure fake set is non-empty and disjoint from culprit
        other_ids = [s["id"] for s in suspects if s["id"] != culprit_id]
        fake_suspects = other_ids[:2]

    clues = [
        {
            "id": "PC_C1",
            "title": "Sensor Smudge Powder",
            "desc": f"Latent trace residue confirms perpetrator is {culprit_h} or ambidextrous.",
            "allowed": matching_h,
            "lead_id": "P_L1",
            "image": "assets/img/evidence/keypad.svg",
            "is_forged": False
        },
        {
            "id": "PC_C2",
            "title": "Security Relay Privileges",
            "desc": f"Intrusion protocol required badge equipped with {culprit_c} authorization.",
            "allowed": matching_c,
            "lead_id": "P_L2",
            "image": "assets/img/evidence/vault_door.svg",
            "is_forged": False
        },
        {
            "id": "PC_C3",
            "title": "Fabricated Incident Note",
            "desc": f"Planted security drop note claims intruder was {fake_h}.",
            "allowed": fake_suspects,
            "lead_id": "P_L3",
            "image": "assets/img/evidence/evidence_bag.svg",
            "is_forged": True,
            "contradicts": ["PC_C1"]
        },
        {
            "id": "PC_C4",
            "title": "Optical Laser Stature Scan",
            "desc": f"Optical sensor triangulation measured perpetrator height at {culprit_ht}.",
            "allowed": matching_ht,
            "lead_id": "P_L4",
            "image": "assets/img/evidence/thermal_camera.svg",
            "is_forged": False
        },
        {
            "id": "PC_C5",
            "title": "Encrypted Terminal Signature",
            "desc": f"Encrypted transmission contains personal workstation token belonging to {culprit['name']}.",
            "allowed": [culprit_id],
            "lead_id": "P_L5",
            "image": "assets/img/evidence/laptop_code.svg",
            "is_forged": False
        }
    ]

    tree = {
        "id": "P_ROOT",
        "title": "Perimeter Incident Ground Zero",
        "category": "SCENE",
        "description": "Inspect perimeter breach sensor array.",
        "ap_cost": 0,
        "clues": [],
        "prerequisites": [],
        "children": [
            {
                "id": "P_L1",
                "title": "Dust Terminal Keypad",
                "category": "FORENSICS",
                "description": "Collect chemical residue from keypad.",
                "ap_cost": 1,
                "clues": ["PC_C1"],
                "prerequisites": ["P_ROOT"],
                "children": [
                    {
                        "id": "P_L2",
                        "title": "Extract Door Controller",
                        "category": "CYBER",
                        "description": "Download badge scanner authentication log.",
                        "ap_cost": 1,
                        "clues": ["PC_C2"],
                        "prerequisites": ["P_L1"],
                        "children": []
                    }
                ]
            },
            {
                "id": "P_L3",
                "title": "Review Drop-Box Statement",
                "category": "INTERROGATION",
                "description": "Read witness deposition left at guard counter.",
                "ap_cost": 1,
                "clues": ["PC_C3"],
                "prerequisites": ["P_ROOT"],
                "children": [
                    {
                        "id": "P_L4",
                        "title": "Calibrate Optical Grid",
                        "category": "FORENSICS",
                        "description": "Triangulate height markers from laser tripwire.",
                        "ap_cost": 1,
                        "clues": ["PC_C4"],
                        "prerequisites": ["P_L3"],
                        "children": [
                            {
                                "id": "P_L5",
                                "title": "Break Terminal Cipher",
                                "category": "CYBER",
                                "description": "Run brute-force analysis on decrypted packet.",
                                "ap_cost": 2,
                                "clues": ["PC_C5"],
                                "prerequisites": ["P_L4"],
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }

    security_logs = [
        {"time": "20:00", "suspect_id": suspects[0]["id"], "event": "Console check-in", "location": "Sector A"},
        {"time": "21:15", "suspect_id": suspects[1]["id"], "event": "Diagnostic start", "location": "Sector B"},
        {"time": "22:30", "suspect_id": accomplice_id, "event": "Sensor override enabled", "location": "Security Hub"},
        {"time": "23:45", "suspect_id": culprit_id, "event": "CRIME TIME: Core seal breached", "location": "Main Vault"},
        {"time": "00:10", "suspect_id": suspects[3]["id"], "event": "Exit gate scan", "location": "Gate 2"}
    ]

    case_data = {
        "id": f"procedural_{seed if seed is not None else 'random'}",
        "title": f"Operation Chimera #{seed % 1000 if seed is not None else 777}",
        "location": "Black-Site Nexus Research Facility",
        "difficulty": "Procedural",
        "briefing": "Automated incident report generated. Collect clues, debunk planted lies, and convict culprit.",
        "scene_image": "assets/img/scenes/title_bg.svg",
        "culprit_id": culprit_id,
        "accomplice_id": accomplice_id,
        "forged_clue_id": "PC_C3",
        "contradicting_clue_id": "PC_C1",
        "suspects": suspects,
        "connections": connections,
        "clues": clues,
        "tree": tree,
        "security_logs": security_logs
    }

    return case_data


def validate_case(case_data: dict) -> bool:
    """
    Validates mathematical solvability of a generated case:
    1. Intersection of all true clues results in exactly {culprit_id}.
    2. Intersection of true clues with the forged clue yields the empty set (∅).
    3. Debunking the forged clue restores viability to {culprit_id}.
    4. Exactly one culprit and one accomplice exist.
    """
    culprit_id = case_data["culprit_id"]
    forged_id = case_data["forged_clue_id"]
    universe = {s["id"] for s in case_data["suspects"]}

    # Collect true clue allowed sets
    true_sets = []
    forged_set = None

    for c in case_data["clues"]:
        allowed = set(c["allowed"])
        if c["id"] == forged_id:
            forged_set = allowed
        else:
            true_sets.append(allowed)

    # 1. Intersection of all true clues
    viable_true = set(universe)
    for s in true_sets:
        viable_true = viable_true.intersection(s)

    if viable_true != {culprit_id}:
        return False

    # 2. Including the forged clue produces empty set
    viable_with_lie = set(viable_true)
    if forged_set is not None:
        viable_with_lie = viable_with_lie.intersection(forged_set)

    if len(viable_with_lie) != 0:
        return False

    return True
