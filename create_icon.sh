#!/bin/bash
"""
Script to create .icns icon file from a PNG image

Usage:
    ./create_icon.sh input.png

This will create icon.icns from input.png
The input PNG should be 1024x1024 pixels for best results.
"""

set -e  # Exit on error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <input.png>"
    echo ""
    echo "Example:"
    echo "  $0 icon.png"
    echo ""
    echo "Note: Input PNG should be 1024x1024 pixels"
    exit 1
fi

INPUT_PNG="$1"

if [ ! -f "${INPUT_PNG}" ]; then
    echo "Error: ${INPUT_PNG} not found!"
    exit 1
fi

echo "Creating icon.icns from ${INPUT_PNG}..."

# Create iconset directory
mkdir -p icon.iconset

# Generate all required icon sizes
echo "Generating icon sizes..."
sips -z 16 16     "${INPUT_PNG}" --out icon.iconset/icon_16x16.png
sips -z 32 32     "${INPUT_PNG}" --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     "${INPUT_PNG}" --out icon.iconset/icon_32x32.png
sips -z 64 64     "${INPUT_PNG}" --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   "${INPUT_PNG}" --out icon.iconset/icon_128x128.png
sips -z 256 256   "${INPUT_PNG}" --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   "${INPUT_PNG}" --out icon.iconset/icon_256x256.png
sips -z 512 512   "${INPUT_PNG}" --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   "${INPUT_PNG}" --out icon.iconset/icon_512x512.png
sips -z 1024 1024 "${INPUT_PNG}" --out icon.iconset/icon_512x512@2x.png

# Create .icns file
echo "Creating icon.icns..."
iconutil -c icns icon.iconset

# Clean up
rm -rf icon.iconset

echo ""
echo "✓ icon.icns created successfully!"
echo ""
echo "To use this icon:"
echo "  1. Update kivy-clock.spec: icon='icon.icns'"
echo "  2. Update setup.py: 'iconfile': 'icon.icns'"
echo "  3. Rebuild the application"
