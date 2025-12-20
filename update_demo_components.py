#!/usr/bin/env python3
"""Update App.jsx for each quantum demo with the correct component"""

from pathlib import Path

BASE_DIR = Path("/Users/yoshikondo/ddsp-piano")
DEMOS_DIR = BASE_DIR / "quantum-demos"
QUANTUM_DEMO_DIR = BASE_DIR / "quantum-demo"

# Read component files
entanglement_component = (QUANTUM_DEMO_DIR / "src/components/Entanglement.jsx").read_text()
grover_component = (QUANTUM_DEMO_DIR / "src/components/GroverSearch.jsx").read_text()
random_component = (QUANTUM_DEMO_DIR / "src/components/QuantumRandom.jsx").read_text()

# Template for App.jsx
def create_app_jsx(component_name, component_import, component_usage, title, description, icon="⚛️"):
    header_comment = "{/* Header */}"
    demo_comment = "{/* Main Demo */}"
    footer_comment = "{/* Footer */}"
    return f'''import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
{component_import}

function App() {{
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-8">
      <div className="max-w-6xl mx-auto">
        {header_comment}
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-2xl">{icon}</span>
            </div>
            <h1 className="text-4xl font-bold text-gray-800">{title}</h1>
          </div>
          <p className="text-lg text-gray-600">
            {description}
          </p>
        </header>

        {demo_comment}
        {component_usage}

        {footer_comment}
        <footer className="text-center mt-8 text-gray-600 text-sm">
          <p>Made with ⚛️ for curious minds | Part of the Quantum Computing Demos series</p>
        </footer>
      </div>
    </div>
  );
}}

export default App;
'''

# Update each demo
demos_config = {
    "quantum-twins-demo": {
        "import": "import Entanglement from './components/Entanglement';",
        "usage": "<Entanglement />",
        "title": "Quantum Twins Demo",
        "description": "Experience quantum entanglement - instant correlation across any distance!",
    },
    "grover-search-demo": {
        "import": "import GroverSearch from './components/GroverSearch';",
        "usage": "<GroverSearch />",
        "title": "Grover Search Demo",
        "description": "See how quantum search is faster than classical search!",
    },
    "quantum-randomness-demo": {
        "import": "import QuantumRandomDemo from './components/QuantumRandom';",
        "usage": "<QuantumRandomDemo />",
        "title": "Quantum Randomness Demo",
        "description": "Generate true randomness from quantum measurements!",
    },
}

# Copy component files first
components_to_copy = {
    "quantum-twins-demo": ("Entanglement.jsx", "Entanglement"),
    "grover-search-demo": ("GroverSearch.jsx", "GroverSearch"),
    "quantum-randomness-demo": ("QuantumRandom.jsx", "QuantumRandomDemo"),
}

for demo_name, (src_file, component_name) in components_to_copy.items():
    src = QUANTUM_DEMO_DIR / "src/components" / src_file
    dst = DEMOS_DIR / demo_name / "src/components" / src_file
    if src.exists():
        content = src.read_text()
        # Update import paths
        content = content.replace("from '../utils/quantumSimulator'", "from '../utils/quantumSimulator'")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content)
        print(f"✅ Copied {src_file} to {demo_name}")

# Create App.jsx for each
for demo_name, config in demos_config.items():
    app_jsx = create_app_jsx(
        component_name=config["usage"].replace("<", "").replace(" />", ""),
        component_import=config["import"],
        component_usage=config["usage"],
        title=config["title"],
        description=config["description"],
    )
    app_file = DEMOS_DIR / demo_name / "src/App.jsx"
    app_file.write_text(app_jsx)
    print(f"✅ Updated App.jsx for {demo_name}")

# For demos that need new components, create placeholder App.jsx
for demo_name in ["quantum-teleportation-demo", "quantum-noise-demo", "quantum-art-generator"]:
    app_file = DEMOS_DIR / demo_name / "src/App.jsx"
    if not app_file.exists() or "Quantum Coin" in app_file.read_text():
        placeholder = create_app_jsx(
            component_name="Demo",
            component_import="// Component coming soon",
            component_usage="<div className='bg-white rounded-xl shadow-lg p-8 text-center'><h2 className='text-2xl font-bold mb-4'>Demo Coming Soon</h2><p className='text-gray-600'>This demo is under development.</p></div>",
            title=demo_name.replace("-", " ").title(),
            description="Interactive quantum computing demonstration",
        )
        app_file.write_text(placeholder)
        print(f"✅ Created placeholder App.jsx for {demo_name}")

print("\n✅ All components updated!")

