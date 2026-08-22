# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

panda_datas, panda_bins, panda_hidden = collect_all('panda3d')
direct_datas, direct_bins, direct_hidden = collect_all('direct')
ursina_datas, ursina_bins, ursina_hidden = collect_all('ursina')
gltf_datas, gltf_bins, gltf_hidden = collect_all('panda3d_gltf')

datas = []
binaries = []
hiddenimports = []

datas += panda_datas + direct_datas + ursina_datas + gltf_datas
binaries += panda_bins + direct_bins + ursina_bins + gltf_bins
hiddenimports += panda_hidden + direct_hidden + ursina_hidden + gltf_hidden

datas += [('python/models-tx', 'models-tx')]
datas += [('python/html', 'html')]

a = Analysis(
    ['python/main.py'],
    pathex=['python'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MUNDI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon='python/Earth.ico'
)

