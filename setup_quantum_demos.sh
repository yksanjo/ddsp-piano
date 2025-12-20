#!/bin/bash

# Script to create standalone projects for each quantum demo
# Extracts each demo from the main quantum-demo project

set -e

BASE_DIR="/Users/yoshikondo/ddsp-piano"
QUANTUM_DEMO_DIR="$BASE_DIR/quantum-demo"
DEMOS_DIR="$BASE_DIR/quantum-demos"

echo "🚀 Setting up standalone quantum demo projects..."
echo ""

# Create demos directory
mkdir -p "$DEMOS_DIR"

# Function to create a standalone demo project
create_demo_project() {
    local demo_name=$1
    local demo_dir="$DEMOS_DIR/$demo_name"
    
    echo "📦 Creating: $demo_name"
    mkdir -p "$demo_dir"
    
    # Copy base files
    cp "$QUANTUM_DEMO_DIR/package.json" "$demo_dir/"
    cp "$QUANTUM_DEMO_DIR/vite.config.js" "$demo_dir/"
    cp "$QUANTUM_DEMO_DIR/tailwind.config.js" "$demo_dir/"
    cp "$QUANTUM_DEMO_DIR/postcss.config.js" "$demo_dir/"
    cp "$QUANTUM_DEMO_DIR/.gitignore" "$demo_dir/"
    cp "$QUANTUM_DEMO_DIR/.npmrc" "$demo_dir/"
    
    # Create index.html
    cat > "$demo_dir/index.html" <<EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>$demo_name - Quantum Computing Demo</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF

    # Create src directory structure
    mkdir -p "$demo_dir/src/components"
    mkdir -p "$demo_dir/src/utils"
    
    # Copy CSS
    cp "$QUANTUM_DEMO_DIR/src/index.css" "$demo_dir/src/"
    
    # Copy quantum simulator (needed for all demos)
    cp "$QUANTUM_DEMO_DIR/src/utils/quantumSimulator.js" "$demo_dir/src/utils/"
    
    echo "  ✅ Project structure created"
}

# Create all demo projects
create_demo_project "quantum-coin-demo"
create_demo_project "quantum-twins-demo"
create_demo_project "grover-search-demo"
create_demo_project "quantum-randomness-demo"
create_demo_project "quantum-teleportation-demo"
create_demo_project "quantum-noise-demo"
create_demo_project "quantum-art-generator"

echo ""
echo "✅ All demo project structures created!"
echo ""
echo "📋 Next: Add demo-specific components to each project"
echo "   Run: ./populate_quantum_demos.sh"



