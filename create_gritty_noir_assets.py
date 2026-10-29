"""
Gritty Hand-Drawn Noir Asset Generator for CaseZero.
Creates highly detailed, hand-drawn / sketched neo-noir vector SVGs:
- Suspect mugshot portraits with realistic sketching, hatching, and crimson rim lights
- Hand-drawn crime scenes (Vault breach, Manor gallery, Detective desk)
- Hand-drawn forensic evidence illustrations with chalk markers and textures
- Stylized logo with magnifying glass, fingerprint whorls, and ink splatter
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "web" / "assets" / "img"
SUSPECTS_DIR = IMG_DIR / "suspects"
EVIDENCE_DIR = IMG_DIR / "evidence"
SCENES_DIR = IMG_DIR / "scenes"

def ensure_dirs():
    SUSPECTS_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    SCENES_DIR.mkdir(parents=True, exist_ok=True)

def generate_logo():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <defs>
    <radialGradient id="logoGlow" cx="45%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#ff1e2d" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#8b0000" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#050505" stop-opacity="0"/>
    </radialGradient>
    <filter id="inkRoughness">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.5"/>
    </filter>
  </defs>
  <!-- Background badge -->
  <rect width="120" height="120" rx="12" fill="#050505" stroke="#1f1f1f" stroke-width="2"/>
  <circle cx="52" cy="50" r="44" fill="url(#logoGlow)"/>

  <!-- Blood splatter droplets -->
  <circle cx="96" cy="22" r="3.5" fill="#ff1e2d" opacity="0.85"/>
  <circle cx="102" cy="28" r="1.8" fill="#e11d2a" opacity="0.7"/>
  <circle cx="92" cy="30" r="1.2" fill="#b3121b" opacity="0.6"/>
  <path d="M 88 24 Q 92 20 96 22 Q 94 28 88 24 Z" fill="#ff1e2d" opacity="0.8"/>

  <!-- Hand-drawn fingerprint ridges -->
  <g fill="none" stroke="#666666" stroke-width="2.2" stroke-linecap="round" opacity="0.55" filter="url(#inkRoughness)">
    <path d="M 42 62 A 12 14 0 0 1 64 60"/>
    <path d="M 36 66 A 18 20 0 0 1 70 56"/>
    <path d="M 30 70 A 24 26 0 0 1 76 52"/>
    <path d="M 26 74 A 30 32 0 0 1 82 48"/>
    <path d="M 38 46 A 14 16 0 0 1 68 44"/>
    <path d="M 44 36 A 20 22 0 0 1 74 38"/>
  </g>

  <!-- Magnifying Glass with metal reflections -->
  <circle cx="52" cy="48" r="32" fill="none" stroke="#ff1e2d" stroke-width="5.5"/>
  <circle cx="52" cy="48" r="32" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.4" stroke-dasharray="16 80"/>
  <circle cx="52" cy="48" r="28" fill="#ff1e2d" fill-opacity="0.1"/>

  <!-- Glass lens reflection glare -->
  <path d="M 32 34 A 26 26 0 0 1 68 26" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>

  <!-- Handle with textured grip -->
  <line x1="75" y1="71" x2="104" y2="100" stroke="#ff1e2d" stroke-width="9" stroke-linecap="round"/>
  <line x1="75" y1="71" x2="104" y2="100" stroke="#050505" stroke-width="3" stroke-linecap="round"/>
  <line x1="82" y1="78" x2="86" y2="82" stroke="#ffffff" stroke-width="2" opacity="0.5"/>
</svg>'''
    (IMG_DIR / "logo.svg").write_text(svg, encoding="utf-8")

def generate_handdrawn_suspect(path: Path, name: str, code: str, gender: str = "m",
                               style: str = "formal", glasses: bool = False, beard: bool = False,
                               accessories: str = "none"):
    """Generates gritty hand-drawn crosshatch noir mugshots."""
    hair_path = ""
    collar_path = ""
    acc_path = ""

    if style == "formal":
        collar_path = '''
        <!-- Suit Collar & Tie -->
        <path d="M 170 340 L 256 460 L 342 340" fill="#0a0a0a" stroke="#222" stroke-width="2"/>
        <path d="M 238 340 L 256 400 L 274 340 Z" fill="#ff1e2d" opacity="0.85"/>
        <line x1="256" y1="400" x2="256" y2="480" stroke="#e11d2a" stroke-width="3"/>
        '''
    elif style == "tech":
        collar_path = '''
        <!-- High Tech Jacket & Cables -->
        <path d="M 160 340 C 200 320 312 320 352 340 L 380 480 L 132 480 Z" fill="#0d0d0d" stroke="#ff1e2d" stroke-width="1.5"/>
        <path d="M 180 370 L 220 480" stroke="#ff1e2d" stroke-width="2" stroke-dasharray="6 3"/>
        <circle cx="210" cy="340" r="5" fill="#ff1e2d"/>
        '''
    elif style == "academic":
        collar_path = '''
        <!-- Lab Coat & Cardigan -->
        <path d="M 160 340 L 256 390 L 352 340 L 380 480 L 132 480 Z" fill="#181818" stroke="#333" stroke-width="2"/>
        <path d="M 200 340 L 256 480 L 312 340" fill="#0a0a0a"/>
        '''
    else:  # street / casual
        collar_path = '''
        <!-- Hooded Coat / Street Leather -->
        <path d="M 140 330 C 180 300 332 300 372 330 L 400 480 L 112 480 Z" fill="#080808" stroke="#2b2b2b" stroke-width="2"/>
        <path d="M 190 320 Q 256 360 322 320" fill="none" stroke="#ff1e2d" stroke-width="1.5" opacity="0.7"/>
        '''

    if gender == "f":
        hair_path = '''
        <!-- Hand-drawn sketched Bob / Curls -->
        <path d="M 170 200 C 160 110 240 90 256 90 C 272 90 352 110 342 200 C 356 260 330 290 320 290 C 310 250 330 190 320 150 C 300 110 212 110 192 150 C 182 190 202 250 192 290 C 182 290 156 260 170 200 Z" fill="#0a0a0a" stroke="#1c1c1c" stroke-width="3"/>
        <!-- Sketched hair strands -->
        <g stroke="#ff1e2d" stroke-width="1" opacity="0.35">
          <path d="M 180 140 Q 230 120 256 120"/>
          <path d="M 175 160 Q 210 150 240 150"/>
          <path d="M 332 140 Q 282 120 256 120"/>
        </g>
        '''
    else:
        hair_path = '''
        <!-- Hand-drawn textured fade / slicked hair -->
        <path d="M 175 180 C 170 110 230 95 256 95 C 282 95 342 110 337 180 C 325 130 187 130 175 180 Z" fill="#080808" stroke="#222" stroke-width="2"/>
        <g stroke="#ff1e2d" stroke-width="1.2" opacity="0.3">
          <line x1="200" y1="110" x2="220" y2="135"/>
          <line x1="230" y1="105" x2="250" y2="130"/>
          <line x1="260" y1="105" x2="280" y2="130"/>
          <line x1="290" y1="110" x2="310" y2="135"/>
        </g>
        '''

    glasses_svg = ""
    if glasses:
        glasses_svg = '''
        <!-- Wireframe Glasses with red rim highlight -->
        <g stroke="#ff1e2d" stroke-width="2.5" fill="none">
          <rect x="206" y="195" width="42" height="28" rx="4"/>
          <rect x="264" y="195" width="42" height="28" rx="4"/>
          <line x1="248" y1="208" x2="264" y2="208"/>
          <!-- Lens glint -->
          <line x1="210" y1="202" x2="222" y2="202" stroke="#ffffff" stroke-width="1.5" opacity="0.7"/>
          <line x1="268" y1="202" x2="280" y2="202" stroke="#ffffff" stroke-width="1.5" opacity="0.7"/>
        </g>
        '''

    beard_svg = ""
    if beard:
        beard_svg = '''
        <!-- Stubble and Beard Hatching -->
        <path d="M 215 250 C 225 300 287 300 297 250 C 290 290 222 290 215 250 Z" fill="#080808" stroke="#ff1e2d" stroke-width="1" opacity="0.4"/>
        <g stroke="#333333" stroke-width="1.2" opacity="0.7">
          <line x1="230" y1="260" x2="235" y2="270"/>
          <line x1="240" y1="262" x2="245" y2="274"/>
          <line x1="255" y1="265" x2="255" y2="278"/>
          <line x1="265" y1="262" x2="270" y2="274"/>
          <line x1="275" y1="260" x2="280" y2="270"/>
        </g>
        '''

    if accessories == "headset":
        acc_path = '''
        <path d="M 180 190 Q 256 140 332 190" fill="none" stroke="#ff1e2d" stroke-width="3"/>
        <circle cx="180" cy="205" r="8" fill="#111" stroke="#ff1e2d" stroke-width="2"/>
        <line x1="180" y1="210" x2="215" y2="240" stroke="#ff1e2d" stroke-width="2"/>
        '''
    elif accessories == "monocle":
        acc_path = '''
        <circle cx="285" cy="208" r="16" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>
        <line x1="285" y1="224" x2="285" y2="280" stroke="#ff1e2d" stroke-width="1.5" stroke-dasharray="3 3"/>
        '''
    elif accessories == "implant":
        acc_path = '''
        <g stroke="#ff1e2d" stroke-width="1.5">
          <circle cx="282" cy="208" r="7" fill="#ff1e2d" opacity="0.8"/>
          <circle cx="282" cy="208" r="11" fill="none"/>
          <line x1="293" y1="208" x2="315" y2="200"/>
          <line x1="282" y1="219" x2="295" y2="235"/>
        </g>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Dark deep charcoal background with blood red spotlight -->
    <radialGradient id="portraitBg" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#141414"/>
      <stop offset="60%" stop-color="#070707"/>
      <stop offset="100%" stop-color="#020202"/>
    </radialGradient>
    <linearGradient id="rimRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff1e2d" stop-opacity="0.9"/>
      <stop offset="40%" stop-color="#8b0000" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>
    <pattern id="crosshatch" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M 0 0 L 8 8 M 8 0 L 0 8" stroke="#181818" stroke-width="0.75"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="512" height="512" fill="url(#portraitBg)"/>
  <rect width="512" height="512" fill="url(#crosshatch)" opacity="0.5"/>

  <!-- Police Stature Height Chart -->
  <g stroke="#1a1a1a" stroke-width="1.5">
    <line x1="40" y1="90" x2="472" y2="90"/><text x="476" y="94" fill="#333" font-family="monospace" font-size="11">195</text>
    <line x1="40" y1="130" x2="472" y2="130"/><text x="476" y="134" fill="#333" font-family="monospace" font-size="11">185</text>
    <line x1="40" y1="170" x2="472" y2="170"/><text x="476" y="174" fill="#333" font-family="monospace" font-size="11">175</text>
    <line x1="40" y1="210" x2="472" y2="210"/><text x="476" y="214" fill="#333" font-family="monospace" font-size="11">165</text>
    <line x1="40" y1="250" x2="472" y2="250"/><text x="476" y="254" fill="#333" font-family="monospace" font-size="11">155</text>
  </g>

  <!-- Shoulder / Torso base -->
  <path d="M 110 490 C 130 350 200 320 256 320 C 312 320 382 350 402 490 Z" fill="#0a0a0a" stroke="#222222" stroke-width="2"/>

  {collar_path}

  <!-- Neck -->
  <rect x="228" y="250" width="56" height="85" fill="#1a1a1a"/>
  <!-- Neck shadow line -->
  <path d="M 228 275 Q 256 295 284 275" fill="none" stroke="#000" stroke-width="4"/>

  <!-- Head Base -->
  <ellipse cx="256" cy="205" rx="74" ry="92" fill="#1e1e1e" stroke="#262626" stroke-width="2"/>
  <!-- Dramatic Red Rim Light -->
  <ellipse cx="256" cy="205" rx="74" ry="92" fill="url(#rimRed)"/>

  {hair_path}

  <!-- Facial Features (Sketched Eyes, Nose, Lips) -->
  <g fill="#080808">
    <!-- Left Eye -->
    <ellipse cx="228" cy="205" rx="13" ry="7" fill="#080808" stroke="#111" stroke-width="1.5"/>
    <circle cx="228" cy="205" r="3" fill="#ffffff" opacity="0.9"/>
    <path d="M 212 195 Q 228 190 244 195" fill="none" stroke="#222" stroke-width="2.5"/>

    <!-- Right Eye -->
    <ellipse cx="284" cy="205" rx="13" ry="7" fill="#080808" stroke="#111" stroke-width="1.5"/>
    <circle cx="284" cy="205" r="3" fill="#ffffff" opacity="0.9"/>
    <path d="M 268 195 Q 284 190 300 195" fill="none" stroke="#222" stroke-width="2.5"/>

    <!-- Nose -->
    <path d="M 256 200 L 250 236 L 262 238" fill="none" stroke="#141414" stroke-width="3"/>

    <!-- Mouth -->
    <path d="M 238 262 Q 256 266 274 262" fill="none" stroke="#141414" stroke-width="3.5"/>
  </g>

  <!-- Sketched Crosshatch Shadows on Cheek -->
  <g stroke="#0f0f0f" stroke-width="1" opacity="0.7">
    <line x1="200" y1="210" x2="215" y2="235"/>
    <line x1="205" y1="210" x2="220" y2="235"/>
    <line x1="295" y1="210" x2="310" y2="235"/>
    <line x1="290" y1="210" x2="305" y2="235"/>
  </g>

  {glasses_svg}
  {beard_svg}
  {acc_path}

  <!-- Chalk Fingerprint / Evidence Number Tag -->
  <rect x="34" y="34" width="36" height="36" fill="#0a0a0a" stroke="#ff1e2d" stroke-width="1.5"/>
  <text x="52" y="58" fill="#ff1e2d" font-family="monospace" font-size="14" font-weight="bold" text-anchor="middle">{code.split('-')[0]}</text>

  <!-- Bottom Forensic Dossier Placard (Typewriter Style) -->
  <rect x="110" y="420" width="292" height="70" fill="#050505" stroke="#ff1e2d" stroke-width="2" rx="3"/>
  <rect x="116" y="426" width="280" height="58" fill="#0d0d0d" stroke="#222" stroke-width="1"/>
  <text x="256" y="452" fill="#ffffff" font-family="'Courier New', monospace" font-size="15" font-weight="bold" text-anchor="middle" letter-spacing="2">{code} // {name[:16].upper()}</text>
  <text x="256" y="472" fill="#888888" font-family="'Courier New', monospace" font-size="10" text-anchor="middle" letter-spacing="1">FORENSIC DIVISION // SUSPECT DOSSIER</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")

def generate_handdrawn_scene(path: Path, title: str, subtitle: str, scene_type: str = "vault"):
    """Generates atmospheric neo-noir crime scene artworks with deep blacks and vibrant red accents."""
    scene_elements = ""

    if scene_type == "vault":
        scene_elements = '''
        <!-- Heavy Breached Vault Circular Blast Door -->
        <circle cx="400" cy="225" r="130" fill="#080808" stroke="#222" stroke-width="6"/>
        <circle cx="400" cy="225" r="105" fill="#030303" stroke="#ff1e2d" stroke-width="3" stroke-dasharray="12 6"/>
        <circle cx="400" cy="225" r="45" fill="#141414" stroke="#ff1e2d" stroke-width="4"/>

        <!-- Blast lock bolts (severed) -->
        <line x1="400" y1="160" x2="400" y2="290" stroke="#ff1e2d" stroke-width="6" stroke-linecap="round"/>
        <line x1="335" y1="225" x2="465" y2="225" stroke="#ff1e2d" stroke-width="6" stroke-linecap="round"/>

        <!-- Sparks / Laser Grid cuts -->
        <path d="M 240 180 L 290 260 L 260 280" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>
        <circle cx="290" cy="260" r="3" fill="#ffffff"/>

        <!-- Police Chalk Evidence Marker & Body Outline -->
        <g stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4 4" fill="none" opacity="0.65">
          <ellipse cx="200" cy="360" rx="30" ry="12"/>
          <path d="M 180 370 L 140 400 L 120 380"/>
          <path d="M 220 370 L 260 410"/>
        </g>
        <polygon points="110,340 130,340 135,365 105,365" fill="#ff1e2d"/>
        <text x="120" y="358" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">A</text>
        '''
    elif scene_type == "manor":
        scene_elements = '''
        <!-- Victorian Gothic Gallery with Spotlight -->
        <ellipse cx="400" cy="380" rx="220" ry="60" fill="#141414" opacity="0.8"/>
        <!-- Shattered Velvet Display Vitrine Pedestal -->
        <rect x="340" y="240" width="120" height="150" fill="#0d0d0d" stroke="#333" stroke-width="2"/>
        <path d="M 330 240 L 400 200 L 470 240 Z" fill="#181818" stroke="#ff1e2d" stroke-width="2"/>

        <!-- Shattered Glass Shards -->
        <polygon points="320,230 350,180 360,240" fill="#222" stroke="#ff1e2d" stroke-width="1.5"/>
        <polygon points="440,220 480,190 460,250" fill="#1a1a1a" stroke="#ffffff" stroke-width="1" opacity="0.8"/>
        <polygon points="380,160 410,210 395,215" fill="#2b2b2b" stroke="#ffffff" stroke-width="1"/>

        <!-- Masquerade Mask Left Behind -->
        <path d="M 370 225 Q 400 210 430 225 Q 415 245 400 235 Q 385 245 370 225 Z" fill="#ff1e2d" stroke="#ffffff" stroke-width="1.5"/>
        <circle cx="385" cy="225" r="4" fill="#050505"/>
        <circle cx="415" cy="225" r="4" fill="#050505"/>

        <!-- Broken Red Laser Beam -->
        <line x1="120" y1="210" x2="350" y2="210" stroke="#ff1e2d" stroke-width="2.5" stroke-dasharray="8 4"/>
        <line x1="450" y1="210" x2="680" y2="210" stroke="#ff1e2d" stroke-width="2.5" stroke-dasharray="8 4"/>
        '''
    else:  # title_bg / detective room
        scene_elements = '''
        <!-- Detective Office Window with Venetian Blinds -->
        <g stroke="#000000" stroke-width="14" opacity="0.7">
          <line x1="0" y1="60" x2="800" y2="60"/>
          <line x1="0" y1="110" x2="800" y2="110"/>
          <line x1="0" y1="160" x2="800" y2="160"/>
          <line x1="0" y1="210" x2="800" y2="210"/>
          <line x1="0" y1="260" x2="800" y2="260"/>
          <line x1="0" y1="310" x2="800" y2="310"/>
        </g>
        <!-- Detective Corkboard with Red Strings in background -->
        <rect x="460" y="70" width="280" height="220" fill="#0a0a0a" stroke="#222" stroke-width="2"/>
        <circle cx="510" cy="120" r="14" fill="#141414" stroke="#ff1e2d" stroke-width="2"/>
        <circle cx="680" cy="140" r="14" fill="#141414" stroke="#ff1e2d" stroke-width="2"/>
        <circle cx="600" cy="230" r="14" fill="#141414" stroke="#ff1e2d" stroke-width="2"/>
        <line x1="510" y1="120" x2="680" y2="140" stroke="#ff1e2d" stroke-width="2.5"/>
        <line x1="680" y1="140" x2="600" y2="230" stroke="#ff1e2d" stroke-width="2.5"/>
        <line x1="510" y1="120" x2="600" y2="230" stroke="#ff1e2d" stroke-width="2.5"/>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450">
  <defs>
    <radialGradient id="sceneSpot" cx="50%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#1c070a"/>
      <stop offset="50%" stop-color="#080808"/>
      <stop offset="100%" stop-color="#020202"/>
    </radialGradient>
    <pattern id="sceneGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#0f0f0f" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Deep pitch black base -->
  <rect width="800" height="450" fill="#020202"/>
  <rect width="800" height="450" fill="url(#sceneSpot)"/>
  <rect width="800" height="450" fill="url(#sceneGrid)" opacity="0.6"/>

  {scene_elements}

  <!-- Crime scene tape banner at bottom -->
  <g>
    <rect x="0" y="416" width="800" height="34" fill="#050505"/>
    <line x1="0" y1="416" x2="800" y2="416" stroke="#ff1e2d" stroke-width="2.5"/>
    <text x="30" y="438" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="12" font-weight="bold" letter-spacing="3">
      METRO CRIME DIVISION // CASEZERO PROTOCOL // SECURE FORENSIC EVIDENCE
    </text>
  </g>

  <!-- Headline Header (Neo-Noir tracked style) -->
  <text x="40" y="72" fill="#ffffff" font-family="Georgia, serif" font-size="28" font-weight="bold" letter-spacing="3">{title}</text>
  <line x1="40" y1="84" x2="320" y2="84" stroke="#ff1e2d" stroke-width="3.5"/>
  <text x="40" y="108" fill="#888888" font-family="'Courier New', monospace" font-size="12" letter-spacing="2">{subtitle}</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")

def generate_handdrawn_evidence(path: Path, title: str, ev_type: str):
    """Generates gritty hand-drawn evidence artifacts."""
    content = ""

    if ev_type == "keypad":
        content = '''
        <!-- Keypad with fluorescent latent fingerprint powder -->
        <rect x="130" y="45" width="140" height="195" rx="6" fill="#0a0a0a" stroke="#ff1e2d" stroke-width="2.5"/>
        <rect x="145" y="60" width="110" height="34" fill="#030303" stroke="#222" stroke-width="1.5"/>
        <text x="200" y="82" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="15" text-anchor="middle" font-weight="bold" letter-spacing="4">****23:45</text>

        <!-- Push Buttons with Smudge Highlights on 2, 4, 7, 8 -->
        <g fill="#141414" stroke="#2b2b2b" stroke-width="1.5">
          <rect x="145" y="105" width="28" height="26" rx="3"/>
          <rect x="186" y="105" width="28" height="26" rx="3" fill="#220508" stroke="#ff1e2d"/>
          <rect x="227" y="105" width="28" height="26" rx="3"/>

          <rect x="145" y="138" width="28" height="26" rx="3" fill="#220508" stroke="#ff1e2d"/>
          <rect x="186" y="138" width="28" height="26" rx="3"/>
          <rect x="227" y="138" width="28" height="26" rx="3"/>

          <rect x="145" y="171" width="28" height="26" rx="3" fill="#220508" stroke="#ff1e2d"/>
          <rect x="186" y="171" width="28" height="26" rx="3" fill="#220508" stroke="#ff1e2d"/>
          <rect x="227" y="171" width="28" height="26" rx="3"/>
        </g>
        <!-- Fluorescent Powder Dusting Smears -->
        <ellipse cx="192" cy="118" rx="8" ry="6" fill="#ff1e2d" opacity="0.6"/>
        <ellipse cx="152" cy="151" rx="9" ry="7" fill="#ff1e2d" opacity="0.6"/>
        <ellipse cx="192" cy="184" rx="10" ry="7" fill="#ff1e2d" opacity="0.7"/>
        '''
    elif ev_type == "thermal":
        content = '''
        <!-- Thermal Camera Silhouette Analysis -->
        <rect x="100" y="45" width="200" height="195" fill="#030303" stroke="#ff1e2d" stroke-width="2"/>
        <line x1="100" y1="80" x2="300" y2="80" stroke="#222" stroke-width="1"/>
        <line x1="100" y1="130" x2="300" y2="130" stroke="#222" stroke-width="1"/>
        <line x1="100" y1="180" x2="300" y2="180" stroke="#222" stroke-width="1"/>

        <!-- Heat signature body -->
        <ellipse cx="200" cy="100" rx="26" ry="32" fill="#ff1e2d" opacity="0.9"/>
        <path d="M 155 210 C 160 140 240 140 245 210 Z" fill="#ff1e2d" opacity="0.8"/>
        <!-- White hot core -->
        <ellipse cx="200" cy="102" rx="14" ry="18" fill="#ffffff" opacity="0.85"/>
        <path d="M 175 210 C 180 160 220 160 225 210 Z" fill="#ffffff" opacity="0.75"/>

        <!-- Crosshair and stats -->
        <text x="110" y="65" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="11" font-weight="bold">TARGET STATURE: 188 CM</text>
        <text x="110" y="228" fill="#888888" font-family="'Courier New', monospace" font-size="10">TEMP CORE: 37.8°C // MALE</text>
        '''
    elif ev_type == "fingerprint":
        content = '''
        <!-- Forensic Latent Fingerprint with Minutiae Markers -->
        <g fill="none" stroke="#ff1e2d" stroke-width="2.4" opacity="0.9">
          <ellipse cx="200" cy="140" rx="14" ry="18"/>
          <ellipse cx="200" cy="140" rx="26" ry="32"/>
          <ellipse cx="200" cy="140" rx="38" ry="46"/>
          <ellipse cx="200" cy="140" rx="50" ry="60"/>
          <ellipse cx="200" cy="140" rx="62" ry="74"/>
        </g>
        <!-- Red Minutiae Verification Markers -->
        <circle cx="186" cy="120" r="3" fill="#ffffff"/>
        <line x1="186" y1="120" x2="160" y2="105" stroke="#ffffff" stroke-width="1.2"/>
        <text x="125" y="105" fill="#ffffff" font-family="monospace" font-size="9">WHORL-04</text>

        <circle cx="218" cy="155" r="3" fill="#ffffff"/>
        <line x1="218" y1="155" x2="250" y2="170" stroke="#ffffff" stroke-width="1.2"/>
        <text x="255" y="174" fill="#ffffff" font-family="monospace" font-size="9">BIFURCATION</text>
        '''
    elif ev_type == "vault":
        content = '''
        <!-- Heavy Vault Door Airlock -->
        <circle cx="200" cy="140" r="85" fill="#080808" stroke="#333" stroke-width="5"/>
        <circle cx="200" cy="140" r="70" fill="#040404" stroke="#ff1e2d" stroke-width="2.5" stroke-dasharray="8 4"/>
        <circle cx="200" cy="140" r="28" fill="#141414" stroke="#ff1e2d" stroke-width="3"/>
        <line x1="200" y1="95" x2="200" y2="185" stroke="#ff1e2d" stroke-width="5" stroke-linecap="round"/>
        <line x1="155" y1="140" x2="245" y2="140" stroke="#ff1e2d" stroke-width="5" stroke-linecap="round"/>
        '''
    elif ev_type == "gem":
        content = '''
        <!-- Gem Case with Faceted Replica -->
        <path d="M 200 65 L 260 110 L 235 190 L 165 190 L 140 110 Z" fill="#111" stroke="#ff1e2d" stroke-width="3"/>
        <polygon points="200,65 170,110 230,110" fill="#242424" stroke="#ff1e2d" stroke-width="1.5"/>
        <polygon points="170,110 200,190 230,110" fill="#1a1a1a" stroke="#8b0000" stroke-width="1.5"/>
        <circle cx="200" cy="110" r="4" fill="#ffffff"/>
        '''
    elif ev_type == "laptop":
        content = '''
        <!-- Decrypted Hacker Laptop Matrix -->
        <rect x="110" y="60" width="180" height="120" rx="4" fill="#0a0a0a" stroke="#ff1e2d" stroke-width="2"/>
        <polygon points="90,180 310,180 325,205 75,205" fill="#181818" stroke="#333" stroke-width="1.5"/>
        <text x="125" y="85" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="11">&gt; bypass_vault()</text>
        <text x="125" y="105" fill="#ffffff" font-family="'Courier New', monospace" font-size="11">&gt; packet_to: CIPHER</text>
        <text x="125" y="125" fill="#888888" font-family="'Courier New', monospace" font-size="11">&gt; key: 0x9AF4 [OK]</text>
        '''
    elif ev_type == "cctv":
        content = '''
        <!-- CCTV Frame with CRT Lines -->
        <rect x="70" y="50" width="260" height="180" fill="#050505" stroke="#ff1e2d" stroke-width="2"/>
        <circle cx="90" cy="72" r="5" fill="#ff1e2d"/>
        <text x="105" y="76" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="11" font-weight="bold">CAM-04 // 23:45:18</text>
        <!-- Fleeing silhouette box -->
        <rect x="160" y="90" width="80" height="120" fill="none" stroke="#ff1e2d" stroke-width="1.5" stroke-dasharray="4 2"/>
        <circle cx="200" cy="115" r="14" fill="#222"/>
        <path d="M 180 180 L 200 135 L 220 180" stroke="#444" stroke-width="4"/>
        '''
    else:  # evidence_bag
        content = '''
        <!-- Sealed Forensic Evidence Bag with Red Tamper Tape -->
        <rect x="120" y="45" width="160" height="195" rx="4" fill="#0d0d0d" stroke="#555" stroke-width="2" stroke-dasharray="6 3"/>
        <rect x="135" y="60" width="130" height="32" fill="#8b0000" stroke="#ff1e2d" stroke-width="1.5"/>
        <text x="200" y="81" fill="#ffffff" font-family="'Courier New', monospace" font-size="12" font-weight="bold" text-anchor="middle">TAMPER EVIDENCE</text>
        <line x1="140" y1="120" x2="260" y2="120" stroke="#333" stroke-width="1.5"/>
        <line x1="140" y1="145" x2="260" y2="145" stroke="#333" stroke-width="1.5"/>
        <text x="145" y="138" fill="#ff1e2d" font-family="'Courier New', monospace" font-size="11">PLANTED WITNESS LOG</text>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <rect width="400" height="300" fill="#080808" stroke="#1f1f1f" stroke-width="2" rx="6"/>
  <!-- Corner Forensic Crop Marks -->
  <path d="M 14 32 L 14 14 L 32 14" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>
  <path d="M 386 32 L 386 14 L 368 14" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>
  <path d="M 14 268 L 14 286 L 32 286" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>
  <path d="M 386 268 L 386 286 L 368 286" fill="none" stroke="#ff1e2d" stroke-width="2.5"/>

  {content}

  <!-- Forensic Tag Footer -->
  <rect x="16" y="252" width="368" height="32" fill="#030303" stroke="#ff1e2d" stroke-width="1"/>
  <text x="30" y="273" fill="#ffffff" font-family="'Courier New', monospace" font-size="11" font-weight="bold" letter-spacing="1">
    EXHIBIT // {title.upper()}
  </text>
</svg>'''
    path.write_text(svg, encoding="utf-8")

def main():
    ensure_dirs()
    generate_logo()

    # Case 1 suspects
    generate_handdrawn_suspect(SUSPECTS_DIR / "S1.svg", "Dr. Aris Thorne", "S1-ARCH", "m", style="academic", glasses=True, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "S2.svg", "Elena Vance", "S2-ADMIN", "f", style="tech", glasses=False, beard=False, accessories="headset")
    generate_handdrawn_suspect(SUSPECTS_DIR / "S3.svg", "Marcus Cole", "S3-ENGR", "m", style="street", glasses=False, beard=True)
    generate_handdrawn_suspect(SUSPECTS_DIR / "S4.svg", "Viktor Drake", "S4-DIPL", "m", style="formal", glasses=False, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "S5.svg", "Dr. Maya Lin", "S5-PHYS", "f", style="academic", glasses=True, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "S6.svg", "Cipher Ramos", "S6-BROK", "m", style="street", glasses=False, beard=True, accessories="implant")

    # Case 2 suspects
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM1.svg", "Lord Reginald", "OM1-LORD", "m", style="formal", glasses=False, beard=True)
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM2.svg", "Dr. Finch", "OM2-CURA", "m", style="academic", glasses=True, beard=False, accessories="monocle")
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM3.svg", "Julian Vance", "OM3-APPR", "m", style="formal", glasses=False, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM4.svg", "Baroness Helga", "OM4-INDU", "f", style="formal", glasses=False, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM5.svg", "Lady Genevieve", "OM5-ARCH", "f", style="tech", glasses=False, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM6.svg", "Felix Moreau", "OM6-CATB", "m", style="street", glasses=False, beard=False)
    generate_handdrawn_suspect(SUSPECTS_DIR / "OM7.svg", "Mme Vivienne", "OM7-FENC", "f", style="formal", glasses=False, beard=False)

    # Procedural suspects
    for i in range(1, 7):
        generate_handdrawn_suspect(
            SUSPECTS_DIR / f"PS_{i}.svg",
            f"Subject {i}",
            f"PS-{i:02d}",
            "m" if i % 2 == 1 else "f",
            style=["formal", "tech", "academic", "street"][i % 4],
            glasses=(i % 3 == 0),
            beard=(i % 2 == 0)
        )

    generate_handdrawn_suspect(SUSPECTS_DIR / "placeholder.svg", "Unknown Subject", "UN-00", "m")

    # Evidence SVGs
    generate_handdrawn_evidence(EVIDENCE_DIR / "keypad.svg", "Keypad Latent Smear", "keypad")
    generate_handdrawn_evidence(EVIDENCE_DIR / "vault_door.svg", "Vault Airlock Seal", "vault")
    generate_handdrawn_evidence(EVIDENCE_DIR / "thermal_camera.svg", "Thermal Stature Scan", "thermal")
    generate_handdrawn_evidence(EVIDENCE_DIR / "gem_case.svg", "Display Pedestal Shards", "gem")
    generate_handdrawn_evidence(EVIDENCE_DIR / "cctv_frame.svg", "CCTV Optical Still", "cctv")
    generate_handdrawn_evidence(EVIDENCE_DIR / "laptop_code.svg", "Server Telemetry Decrypt", "laptop")
    generate_handdrawn_evidence(EVIDENCE_DIR / "fingerprint.svg", "Fingerprint Ridge Match", "fingerprint")
    generate_handdrawn_evidence(EVIDENCE_DIR / "evidence_bag.svg", "Tampered Deposition Log", "evidence_bag")

    # Scene Background SVGs
    generate_handdrawn_scene(SCENES_DIR / "vault_scene.svg", "CYBERDYNE QUANTUM VAULT", "SECTOR 7 AIR-GAPPED CHAMBER", "vault")
    generate_handdrawn_scene(SCENES_DIR / "manor_scene.svg", "OBSIDIAN MANOR", "PRIVATE MASQUERADE GALLERY", "manor")
    generate_handdrawn_scene(SCENES_DIR / "title_bg.svg", "CASEZERO FORENSICS", "ALGORITHMIC INVESTIGATION DIVISION", "detective")

    print("[SUCCESS] All gritty hand-drawn noir vector assets created!")

if __name__ == "__main__":
    main()
