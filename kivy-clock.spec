# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Kivy Clock application
This file defines how PyInstaller should bundle the application for macOS
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('clock.kv', '.'),
        ('settings.json', '.'),
        ('fonts/*.ttf', 'fonts'),
    ],
    hiddenimports=[
        'kivy.core.window.window_sdl2',
        'kivy.core.image.img_imageio',
        'kivy.core.audio.audio_sdl2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Kivy Clock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Kivy Clock',
)

app = BUNDLE(
    coll,
    name='Kivy Clock.app',
    icon=None,  # Add path to .icns file if available: icon='icon.icns'
    bundle_identifier='com.yourname.kivy-clock',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSPrincipalClass': 'NSApplication',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'CFBundleName': 'Kivy Clock',
        'CFBundleDisplayName': 'Kivy Clock',
    },
)
