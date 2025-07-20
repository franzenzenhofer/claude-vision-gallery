#!/bin/bash
# Generate all art pieces for the Claude Vision Gallery

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLIC_DIR="$(dirname "$SCRIPT_DIR")/public"

echo "Creating public directory..."
mkdir -p "$PUBLIC_DIR"

echo "Generating Neural Network visualization..."
blender --background --python "$SCRIPT_DIR/generate_neural_network.py"

echo "Generating Data Flow visualization..."
blender --background --python "$SCRIPT_DIR/generate_data_flow.py"

echo "Generating Algorithm Crystal visualization..."
blender --background --python "$SCRIPT_DIR/generate_algorithm_crystal.py"

echo "Generating System Architecture visualization..."
blender --background --python "$SCRIPT_DIR/generate_system_architecture.py"

echo "Generating Code Universe visualization..."
blender --background --python "$SCRIPT_DIR/generate_code_universe.py"

echo "All art pieces generated successfully!"
echo "Images saved in: $PUBLIC_DIR"
ls -la "$PUBLIC_DIR"/*.png