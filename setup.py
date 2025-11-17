"""
Setup script for creating macOS .app bundle using py2app

Usage:
    python setup.py py2app -A     # Development mode (alias mode)
    python setup.py py2app         # Production mode (full bundle)
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('', ['clock.kv', 'settings.json']),
    ('fonts', [
        'fonts/Roboto-Thin.ttf',
        'fonts/DSEG7Classic-Regular.ttf',
        'fonts/UbuntuMono-Regular.ttf',
        'fonts/DejaVuSansMono.ttf',
        'fonts/SourceCodePro-Regular.ttf',
        'fonts/FiraMono-Regular.ttf',
    ]),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Specify path to .icns if available: 'icon.icns'
    'plist': {
        'CFBundleName': 'Kivy Clock',
        'CFBundleDisplayName': 'Kivy Clock',
        'CFBundleIdentifier': 'com.yourname.kivy-clock',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
    'packages': ['kivy'],
    'frameworks': [],
    'includes': [
        'kivy.core.window.window_sdl2',
        'kivy.core.image.img_imageio',
    ],
}

setup(
    name='Kivy Clock',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
