# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for iTerm2 Tabs
"""
import os
import sys

block_cipher = None

# Get the project root directory
spec_root = os.path.dirname(SPEC)

# Collect all source files
src_dir = os.path.join(spec_root, 'src', 'iterm2_tabs')

a = Analysis(
    [os.path.join(src_dir, '__main__.py')],
    pathex=[spec_root],
    binaries=[],
    datas=[
        # Add any data files here if needed
        # (source, destination),
    ],
    hiddenimports=[
        'iterm2',
        'websockets',
        'websockets.legacy',
        'websockets.legacy.client',
        'websockets.datastructures',
        'google.protobuf',
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
    name='iTerm2 Tabs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hide console window for GUI app
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
    name='iTerm2 Tabs',
)

app = BUNDLE(
    exe,
    coll,
    name='iTerm2 Tabs.app',
    icon=None,
    bundle_identifier='com.iterm2-tabs.app',
    info_plist={
        'CFBundleName': 'iTerm2 Tabs',
        'CFBundleDisplayName': 'iTerm2 Tabs',
        'CFBundleIdentifier': 'com.iterm2-tabs.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
        'LSBackgroundOnly': False,
        'LSForegroundOnly': True,
        'NSSupportsAutomaticTermination': False,
        'NSSupportsSuddenTermination': False,
    },
)
