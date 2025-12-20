#!/usr/bin/env python3
"""Update all quantum demo projects with correct components and READMEs"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/yoshikondo/ddsp-piano")
QUANTUM_DEMO_DIR = BASE_DIR / "quantum-demo"
DEMOS_DIR = BASE_DIR / "quantum-demos"

# Copy full quantum simulator to all demos
def copy_simulator():
    src = QUANTUM_DEMO_DIR / "src/utils/quantumSimulator.js"
    for demo_dir in DEMOS_DIR.iterdir():
        if demo_dir.is_dir():
            dst = demo_dir / "src/utils/quantumSimulator.js"
            shutil.copy2(src, dst)
            print(f"✅ Updated simulator in {demo_dir.name}")

# Update package.json for each demo
def update_package_json(demo_name, description):
    pkg_file = DEMOS_DIR / demo_name / "package.json"
    if pkg_file.exists():
        content = pkg_file.read_text()
        content = content.replace('"name": "quantum-coin-demo"', f'"name": "{demo_name}"')
        content = content.replace('Interactive superposition demonstration', description)
        pkg_file.write_text(content)
        print(f"✅ Updated package.json for {demo_name}")

# Update index.html title
def update_index_html(demo_name, title):
    html_file = DEMOS_DIR / demo_name / "index.html"
    if html_file.exists():
        content = html_file.read_text()
        content = content.replace("Quantum Coin Demo - Superposition Demonstration", title)
        html_file.write_text(content)
        print(f"✅ Updated index.html for {demo_name}")

if __name__ == "__main__":
    print("🔄 Updating all quantum demo projects...")
    
    # Copy full simulator to all
    copy_simulator()
    
    # Update package.json and index.html for each
    demos = {
        "quantum-coin-demo": ("Interactive superposition demonstration - heads AND tails simultaneously", "Quantum Coin Demo - Superposition Demonstration"),
        "quantum-twins-demo": ("Entanglement visualization - instant correlation across any distance", "Quantum Twins Demo - Entanglement Visualization"),
        "grover-search-demo": ("Quantum search algorithm - faster than classical search", "Grover Search Demo - Quantum Search Algorithm"),
        "quantum-randomness-demo": ("True randomness generation for security applications", "Quantum Randomness Demo - True Randomness Generation"),
        "quantum-teleportation-demo": ("Teleport quantum information without physical transfer", "Quantum Teleportation Demo - Information Teleportation"),
        "quantum-noise-demo": ("Compare perfect simulator vs noisy real quantum hardware", "Quantum Noise Demo - Simulator vs Real Hardware"),
        "quantum-art-generator": ("Generate unique art and music from quantum measurements", "Quantum Art Generator - Art & Music from Quantum"),
    }
    
    for demo_name, (desc, title) in demos.items():
        update_package_json(demo_name, desc)
        update_index_html(demo_name, title)
    
    print("\n✅ All demos updated!")


