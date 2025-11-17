#!/bin/bash
"""
Script to create a DMG installer for Kivy Clock application

This script packages the .app bundle into a DMG file suitable for distribution.
It creates a temporary directory with the app and a link to Applications folder,
then creates a compressed DMG image.
"""

set -e  # Exit on error

APP_NAME="Kivy Clock"
DMG_NAME="Kivy-Clock-1.0.0"
APP_PATH="dist/${APP_NAME}.app"
DMG_DIR="dmg_temp"

echo "Creating DMG installer for ${APP_NAME}..."

# Check if app exists
if [ ! -d "${APP_PATH}" ]; then
    echo "Error: ${APP_PATH} not found!"
    echo "Please build the application first using PyInstaller or py2app"
    exit 1
fi

# Create temporary directory
echo "Creating temporary directory..."
mkdir -p "${DMG_DIR}"

# Copy application
echo "Copying application..."
cp -r "${APP_PATH}" "${DMG_DIR}/"

# Create symbolic link to Applications
echo "Creating Applications symlink..."
ln -s /Applications "${DMG_DIR}/Applications"

# Create DMG
echo "Creating DMG image..."
hdiutil create -volname "${APP_NAME}" \
  -srcfolder "${DMG_DIR}" \
  -ov -format UDZO \
  "${DMG_NAME}.dmg"

# Clean up
echo "Cleaning up..."
rm -rf "${DMG_DIR}"

echo ""
echo "✓ DMG created successfully: ${DMG_NAME}.dmg"
echo ""
echo "To test the DMG:"
echo "  open ${DMG_NAME}.dmg"
echo ""
echo "To sign the DMG (optional):"
echo "  codesign --force --sign \"Developer ID\" ${DMG_NAME}.dmg"
