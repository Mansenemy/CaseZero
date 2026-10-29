"""
Handcrafted Case Files for CaseZero:
- Case 01: The Phantom Key (CyberDyne Systems)
- Case 02: The Midnight Heist (Obsidian Manor)

All clue text is under 20 words.
Each clue records allowed suspects, the lead that reveals it, its image path, and whether it is forged.
"""

CASE_01 = {
    "id": "case_1",
    "title": "The Phantom Key",
    "location": "CyberDyne Systems - Sector 7 Vault",
    "difficulty": "Standard",
    "briefing": "At 23:45, the Quantum Master Key was stolen from the air-gapped vault. Inside conspirators tampered with logs.",
    "scene_image": "assets/img/scenes/vault_scene.svg",
    "culprit_id": "S4",
    "accomplice_id": "S2",
    "forged_clue_id": "C3",
    "contradicting_clue_id": "C5",
    "suspects": [
        {
            "id": "S1",
            "name": "Dr. Aris Thorne",
            "role": "Chief AI Architect",
            "image": "assets/img/suspects/S1.svg",
            "traits": ["Left-Handed", "Tier 3 Clearance", "Height 188cm", "Male"],
            "alibi": "Claims he was asleep in on-call room after long compile.",
            "motive": "Disputed ownership rights over quantum core algorithms.",
            "notes": "Elena manages his security access. Viktor recently blackmailed him."
        },
        {
            "id": "S2",
            "name": "Elena Vance",
            "role": "Security Systems Admin",
            "image": "assets/img/suspects/S2.svg",
            "traits": ["Right-Handed", "Tier 3 Clearance", "Height 168cm", "Female"],
            "alibi": "Claims she monitored server room diagnostics with Dr. Maya Lin.",
            "motive": "Huge unexplained offshore cryptocurrency transfers.",
            "notes": "Accomplice who granted override privileges and forged initial guard log."
        },
        {
            "id": "S3",
            "name": "Marcus Cole",
            "role": "Senior Hardware Engineer",
            "image": "assets/img/suspects/S3.svg",
            "traits": ["Left-Handed", "Tier 2 Clearance", "Height 186cm", "Male"],
            "alibi": "Recalibrating cooling lines in Sub-level 1.",
            "motive": "Heavy underground gambling debts owed to broker Jax Ramos.",
            "notes": "Sold physical maintenance bypass card to Viktor Drake."
        },
        {
            "id": "S4",
            "name": "Viktor Drake",
            "role": "Corporate Diplomat",
            "image": "assets/img/suspects/S4.svg",
            "traits": ["Ambidextrous", "Override Badge", "Height 189cm", "Male"],
            "alibi": "Claims he left building at 21:00 for diplomatic dinner.",
            "motive": "Offered 10M bounty by competitor syndicate for master key.",
            "notes": "True culprit. Stole quantum key using bypass card and Elena's credentials."
        },
        {
            "id": "S5",
            "name": "Dr. Maya Lin",
            "role": "Quantum Physicist",
            "image": "assets/img/suspects/S5.svg",
            "traits": ["Right-Handed", "Tier 3 Clearance", "Height 165cm", "Female"],
            "alibi": "Digitally signed grant proposal in Conference Room B at 23:45.",
            "motive": "Pure academic devotion. No financial motive detected.",
            "notes": "Firmly denies Elena's claim that they were together during breach."
        },
        {
            "id": "S6",
            "name": "Jax 'Cipher' Ramos",
            "role": "Black-Market Data Broker",
            "image": "assets/img/suspects/S6.svg",
            "traits": ["Left-Handed", "Offsite Access", "Height 175cm", "Male"],
            "alibi": "Operated off-site through remote proxy servers.",
            "motive": "Fencing stolen quantum keys on encrypted darknet.",
            "notes": "Financial handler for Marcus Cole and extraction contact for Viktor."
        }
    ],
    "connections": [
        {"u": "S1", "v": "S2", "type": "COLLEAGUE", "desc": "Elena manages Aris's security access credentials."},
        {"u": "S1", "v": "S4", "type": "BLACKMAIL", "desc": "Viktor threatened Aris over unauthorized private research."},
        {"u": "S2", "v": "S5", "type": "CONSPIRACY", "desc": "Elena fabricated false joint alibi with Maya."},
        {"u": "S2", "v": "S4", "type": "CONSPIRACY", "desc": "Elena provided Viktor with active vault override permissions."},
        {"u": "S3", "v": "S6", "type": "DEBT", "desc": "Marcus owes Jax 250,000 credits in underground debts."},
        {"u": "S3", "v": "S4", "type": "EQUIPMENT", "desc": "Marcus supplied Viktor with physical bypass hardware."},
        {"u": "S4", "v": "S6", "type": "CONSPIRACY", "desc": "Encrypted telemetry channel to fence stolen key."}
    ],
    "clues": [
        {
            "id": "C1",
            "title": "Biometric Keypad Powder",
            "desc": "Keypad powder residue confirms intruder entered the 8-digit PIN using left hand or is ambidextrous.",
            "allowed": ["S1", "S3", "S4", "S6"],
            "lead_id": "L1",
            "image": "assets/img/evidence/keypad.svg",
            "is_forged": False
        },
        {
            "id": "C2",
            "title": "Airlock Firmware Filter",
            "desc": "Door lock controller shows entry permitted only to Level 3 clearance or active Security Override badge.",
            "allowed": ["S1", "S2", "S4", "S5"],
            "lead_id": "L2",
            "image": "assets/img/evidence/vault_door.svg",
            "is_forged": False
        },
        {
            "id": "C3",
            "title": "Tampered Guard Incident Log",
            "desc": "Altered log claims: 'Intruder was a petite female operative fleeing toward stairwell at 23:46.'",
            "allowed": ["S2", "S5"],
            "lead_id": "L3",
            "image": "assets/img/evidence/evidence_bag.svg",
            "is_forged": True,
            "contradicts": ["C5"]
        },
        {
            "id": "C4",
            "title": "Darknet Relay Capture",
            "desc": "Switch capture proves intruder actively relayed data packets directly to broker Jax 'Cipher' Ramos.",
            "allowed": ["S3", "S4"],
            "lead_id": "L5",
            "image": "assets/img/evidence/laptop_code.svg",
            "is_forged": False
        },
        {
            "id": "C5",
            "title": "Corridor Thermal Silhouette",
            "desc": "Thermal camera captured athletic male silhouette between 185cm and 192cm fleeing sector at 23:46.",
            "allowed": ["S1", "S3", "S4"],
            "lead_id": "L4",
            "image": "assets/img/evidence/thermal_camera.svg",
            "is_forged": False,
            "contradicts": ["C3"]
        },
        {
            "id": "C6",
            "title": "Decrypted Extraction Wire",
            "desc": "Decrypted packet payload: 'Key secured from vault. Meeting extraction driver at emergency bay. - V.D.'",
            "allowed": ["S4"],
            "lead_id": "L6",
            "image": "assets/img/evidence/fingerprint.svg",
            "is_forged": False
        }
    ],
    "tree": {
        "id": "ROOT",
        "title": "Quantum Vault Ground Zero",
        "category": "SCENE",
        "description": "Perimeter inspection outside breached air-gapped vault door.",
        "ap_cost": 0,
        "clues": [],
        "prerequisites": [],
        "children": [
            {
                "id": "L1",
                "title": "Dust Biometric Keypad",
                "category": "FORENSICS",
                "description": "Analyze chemical dusting and latent finger smudges on terminal.",
                "ap_cost": 1,
                "clues": ["C1"],
                "prerequisites": ["ROOT"],
                "children": [
                    {
                        "id": "L2",
                        "title": "Dump Airlock Firmware",
                        "category": "CYBER",
                        "description": "Extract badge reader authorization hashes from memory buffer.",
                        "ap_cost": 1,
                        "clues": ["C2"],
                        "prerequisites": ["L1"],
                        "children": []
                    }
                ]
            },
            {
                "id": "L3",
                "title": "Review Guard Incident Desk",
                "category": "INTERROGATION",
                "description": "Examine physical paper log signed right after siren.",
                "ap_cost": 1,
                "clues": ["C3"],
                "prerequisites": ["ROOT"],
                "children": [
                    {
                        "id": "L4",
                        "title": "Enhance Thermal Optics",
                        "category": "FORENSICS",
                        "description": "Calibrate high-speed thermal corridor cameras at 23:46.",
                        "ap_cost": 1,
                        "clues": ["C5"],
                        "prerequisites": ["L3"],
                        "children": []
                    }
                ]
            },
            {
                "id": "L5",
                "title": "Tap Fiber-Optic Switch",
                "category": "CYBER",
                "description": "Mirror outbound traffic from Server Rack B.",
                "ap_cost": 1,
                "clues": ["C4"],
                "prerequisites": ["ROOT"],
                "children": [
                    {
                        "id": "L6",
                        "title": "Decrypt Darknet Packet",
                        "category": "CYBER",
                        "description": "Run brute-force quantum decryption on outbound wire.",
                        "ap_cost": 2,
                        "clues": ["C6"],
                        "prerequisites": ["L5"],
                        "children": []
                    }
                ]
            }
        ]
    },
    "security_logs": [
        {"time": "19:40", "suspect_id": "S4", "event": "Badge tap at lobby reception", "location": "Lobby"},
        {"time": "20:15", "suspect_id": "S1", "event": "Workstation login for compile", "location": "AI Lab"},
        {"time": "21:00", "suspect_id": "S4", "event": "Security badge departure registered", "location": "Lobby Gate"},
        {"time": "21:30", "suspect_id": "S3", "event": "Hardware diagnostic sweep", "location": "Sub-level 1"},
        {"time": "22:15", "suspect_id": "S2", "event": "Console override updated", "location": "Security Hub"},
        {"time": "23:10", "suspect_id": "S6", "event": "Darknet tunnel ping received", "location": "Proxy Node"},
        {"time": "23:40", "suspect_id": "S4", "event": "Maintenance hatch unlocked", "location": "Ventilation Shaft"},
        {"time": "23:45", "suspect_id": "S5", "event": "ALIBI VERIFIED: Grant proposal signed", "location": "Conference B"},
        {"time": "23:45", "suspect_id": "S4", "event": "CRIME TIME: Vault pressure seal bypassed", "location": "Quantum Vault"},
        {"time": "23:48", "suspect_id": "S2", "event": "Manual alarm delay tripped 180s", "location": "Security Hub"},
        {"time": "00:05", "suspect_id": "S4", "event": "Emergency exit pushed from inside", "location": "Loading Bay"}
    ]
}


CASE_02 = {
    "id": "case_2",
    "title": "The Midnight Heist",
    "location": "Obsidian Manor - Private Gallery",
    "difficulty": "Advanced",
    "briefing": "During a midnight masquerade gala, the 'Heart of Chronos' gem was replaced with a synthetic replica.",
    "scene_image": "assets/img/scenes/manor_scene.svg",
    "culprit_id": "OM3",
    "accomplice_id": "OM5",
    "forged_clue_id": "OM_C2",
    "contradicting_clue_id": "OM_C4",
    "suspects": [
        {
            "id": "OM1",
            "name": "Lord Reginald Sterling",
            "role": "Host & Collector",
            "image": "assets/img/suspects/OM1.svg",
            "traits": ["Right-Handed", "Master Keyholder", "Height 180cm"],
            "alibi": "Delivering midnight toast on grand ballroom balcony.",
            "motive": "Massive insurance policy on the gemstone.",
            "notes": "Hired Genevieve to design the acoustic grid."
        },
        {
            "id": "OM2",
            "name": "Dr. Alistair Finch",
            "role": "Museum Curator",
            "image": "assets/img/suspects/OM2.svg",
            "traits": ["Left-Handed", "Acoustic Specialist", "Height 172cm"],
            "alibi": "In wine cellar selecting rare vintage bottles.",
            "motive": "Bitter rivalry regarding authenticity of the Chronos stone.",
            "notes": "Possesses acoustic tuning expertise."
        },
        {
            "id": "OM3",
            "name": "Julian Vance",
            "role": "Master Gem Appraiser",
            "image": "assets/img/suspects/OM3.svg",
            "traits": ["Right-Handed", "Diamond Cutter", "Acoustic Specialist", "Height 185cm"],
            "alibi": "Claims he was smoking cigars in private conservatory.",
            "motive": "Black-market buyer arranged by Madame Vivienne.",
            "notes": "True culprit. Precision cut synthetic replica and bypassed laser grid."
        },
        {
            "id": "OM4",
            "name": "Baroness Helga Strauss",
            "role": "Industrialist",
            "image": "assets/img/suspects/OM4.svg",
            "traits": ["Ambidextrous", "Diamond Cutter", "Height 168cm"],
            "alibi": "Dancing with foreign trade ambassador in ballroom.",
            "motive": "Retaining Felix Moreau for industrial espionage.",
            "notes": "Experienced lapidary and synthetic gem cutter."
        },
        {
            "id": "OM5",
            "name": "Lady Genevieve",
            "role": "Security Architect",
            "image": "assets/img/suspects/OM5.svg",
            "traits": ["Right-Handed", "Master Keyholder", "Height 175cm"],
            "alibi": "In security booth monitoring laser grid frequency.",
            "motive": "Secret financial alliance and affair with Julian Vance.",
            "notes": "Accomplice who muted acoustic alarm and planted false monocle."
        },
        {
            "id": "OM6",
            "name": "Felix 'Ghost' Moreau",
            "role": "Cat Burglar",
            "image": "assets/img/suspects/OM6.svg",
            "traits": ["Left-Handed", "Acrobat", "Height 182cm"],
            "alibi": "Posing as ice sculptor in outdoor garden pavilion.",
            "motive": "Freelance thief with contract history under Baroness.",
            "notes": "Targeted by Genevieve's planted left-handed clue."
        },
        {
            "id": "OM7",
            "name": "Madame Vivienne",
            "role": "Art Broker",
            "image": "assets/img/suspects/OM7.svg",
            "traits": ["Right-Handed", "Black Market Fencer", "Height 165cm"],
            "alibi": "In card parlor with Lord Sterling's brother.",
            "motive": "Brokering high-value smuggled stones to overseas collectors.",
            "notes": "Julian contracted Vivienne to move uncut stones."
        }
    ],
    "connections": [
        {"u": "OM1", "v": "OM5", "type": "COLLEAGUE", "desc": "Reginald commissioned Genevieve to secure gallery."},
        {"u": "OM3", "v": "OM5", "type": "CONSPIRACY", "desc": "Julian and Genevieve shared secret financial accounts."},
        {"u": "OM3", "v": "OM7", "type": "CONSPIRACY", "desc": "Julian contracted Vivienne to fence uncut gems."},
        {"u": "OM2", "v": "OM3", "type": "BLACKMAIL", "desc": "Rivalry over gem certification credentials."},
        {"u": "OM4", "v": "OM6", "type": "DEBT", "desc": "Baroness retained Felix for previous heist operations."}
    ],
    "clues": [
        {
            "id": "OM_C1",
            "title": "Acoustic Bypass Frequency",
            "desc": "Laser sensors muted using a 432Hz harmonic pitch. Culprit is an Acoustic Specialist.",
            "allowed": ["OM2", "OM3"],
            "lead_id": "OM_L1",
            "image": "assets/img/evidence/keypad.svg",
            "is_forged": False
        },
        {
            "id": "OM_C2",
            "title": "Planted Left-Eye Monocle",
            "desc": "Planted vintage reading monocle found beside pedestal, pointing to an older left-handed scholar.",
            "allowed": ["OM2", "OM6"],
            "lead_id": "OM_L3",
            "image": "assets/img/evidence/evidence_bag.svg",
            "is_forged": True,
            "contradicts": ["OM_C4"]
        },
        {
            "id": "OM_C3",
            "title": "Gem Facet Cutting Precision",
            "desc": "Synthetic replica required master diamond cutting skill to match the antique titanium mount.",
            "allowed": ["OM3", "OM4"],
            "lead_id": "OM_L2",
            "image": "assets/img/evidence/gem_case.svg",
            "is_forged": False
        },
        {
            "id": "OM_C4",
            "title": "Mirror Reflection Analysis",
            "desc": "Champagne mirror reflection shows perpetrator holding acoustic fork in their right hand.",
            "allowed": ["OM1", "OM3", "OM5", "OM7"],
            "lead_id": "OM_L4",
            "image": "assets/img/evidence/cctv_frame.svg",
            "is_forged": False,
            "contradicts": ["OM_C2"]
        },
        {
            "id": "OM_C5",
            "title": "Telegram Fencing Note",
            "desc": "Encrypted telegram found in coats: 'Synthetic gem placed. Delivery ready for London courier. J.V.'",
            "allowed": ["OM3"],
            "lead_id": "OM_L5",
            "image": "assets/img/evidence/fingerprint.svg",
            "is_forged": False
        }
    ],
    "tree": {
        "id": "OM_ROOT",
        "title": "Obsidian Gallery Pedestal",
        "category": "SCENE",
        "description": "Inspection of glass display case and severed laser grid.",
        "ap_cost": 0,
        "clues": [],
        "prerequisites": [],
        "children": [
            {
                "id": "OM_L1",
                "title": "Analyze Laser Relays",
                "category": "CYBER",
                "description": "Inspect harmonic frequency resonance in acoustic sensor.",
                "ap_cost": 1,
                "clues": ["OM_C1"],
                "prerequisites": ["OM_ROOT"],
                "children": [
                    {
                        "id": "OM_L2",
                        "title": "Spectrometry on Fake Gem",
                        "category": "FORENSICS",
                        "description": "Inspect microscopic lapidary facets on the replica.",
                        "ap_cost": 1,
                        "clues": ["OM_C3"],
                        "prerequisites": ["OM_L1"],
                        "children": [
                            {
                                "id": "OM_L5",
                                "title": "Intercept Courier Wire",
                                "category": "INTERROGATION",
                                "description": "Inspect telegraph messages sent from ballroom.",
                                "ap_cost": 2,
                                "clues": ["OM_C5"],
                                "prerequisites": ["OM_L2"],
                                "children": []
                            }
                        ]
                    }
                ]
            },
            {
                "id": "OM_L3",
                "title": "Search Display Carpet",
                "category": "FORENSICS",
                "description": "Collect physical debris and dropped objects by velvet base.",
                "ap_cost": 1,
                "clues": ["OM_C2"],
                "prerequisites": ["OM_ROOT"],
                "children": [
                    {
                        "id": "OM_L4",
                        "title": "Enhance Chandelier Reflection",
                        "category": "FORENSICS",
                        "description": "Analyze mirror reflection in champagne tower glass.",
                        "ap_cost": 1,
                        "clues": ["OM_C4"],
                        "prerequisites": ["OM_L3"],
                        "children": []
                    }
                ]
            }
        ]
    },
    "security_logs": [
        {"time": "22:00", "suspect_id": "OM1", "event": "Ballroom welcoming address", "location": "Ballroom"},
        {"time": "23:15", "suspect_id": "OM2", "event": "Descended to private cellar", "location": "Cellar"},
        {"time": "23:40", "suspect_id": "OM5", "event": "Control console: laser muted", "location": "Security Annex"},
        {"time": "23:55", "suspect_id": "OM3", "event": "Conservatory motion sensor silent", "location": "Conservatory"},
        {"time": "23:58", "suspect_id": "OM3", "event": "CRIME TIME: Gem replaced with weighted replica", "location": "Gallery"},
        {"time": "00:02", "suspect_id": "OM6", "event": "Security checkpoint pass in garden", "location": "Garden Pavilion"}
    ]
}

CASES = {
    "case_1": CASE_01,
    "case_2": CASE_02
}
