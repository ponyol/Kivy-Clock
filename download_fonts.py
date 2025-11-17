#!/usr/bin/env python3
"""
Font downloader script for Kivy Clock application.
Downloads free fonts from Google Fonts and other sources.
"""

import os
import requests
from pathlib import Path


FONTS_DIR = Path(__file__).parent / "fonts"
FONTS_DIR.mkdir(exist_ok=True)


# Font sources (direct download URLs for .ttf files)
FONT_URLS = {
    "Roboto-Thin.ttf": "https://github.com/google/roboto/raw/main/src/hinted/Roboto-Thin.ttf",
    "UbuntuMono-Regular.ttf": "https://github.com/google/fonts/raw/main/ufl/ubuntumono/UbuntuMono-Regular.ttf",
    "DejaVuSansMono.ttf": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSansMono.ttf",
    "SourceCodePro-Regular.ttf": "https://github.com/adobe-fonts/source-code-pro/raw/release/TTF/SourceCodePro-Regular.ttf",
    "FiraMono-Regular.ttf": "https://github.com/mozilla/Fira/raw/master/ttf/FiraMono-Regular.ttf",
    "DSEG7Classic-Regular.ttf": "https://github.com/keshikan/DSEG/raw/master/fonts/DSEG7-Classic/DSEG7Classic-Regular.ttf",
}


def download_font(name: str, url: str) -> bool:
    """
    Downloads a font file from the given URL.

    Args:
        name: The filename to save the font as
        url: The URL to download from

    Returns:
        True if successful, False otherwise
    """
    file_path = FONTS_DIR / name

    # Skip if already exists
    if file_path.exists():
        print(f"✓ {name} already exists, skipping")
        return True

    try:
        print(f"Downloading {name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        file_path.write_bytes(response.content)
        print(f"✓ {name} downloaded successfully")
        return True

    except Exception as e:
        print(f"✗ Failed to download {name}: {e}")
        return False


def main():
    """Download all fonts."""
    print(f"Downloading fonts to {FONTS_DIR}...\n")

    success_count = 0
    total_count = len(FONT_URLS)

    for font_name, font_url in FONT_URLS.items():
        if download_font(font_name, font_url):
            success_count += 1

    print(f"\n{success_count}/{total_count} fonts downloaded successfully")

    if success_count < total_count:
        print("\nWARNING: Some fonts failed to download.")
        print("The application will still work but those fonts won't be available.")


if __name__ == "__main__":
    main()
