# -*- mode: python ; coding: utf-8 -*-
EXCLUDE = {
        "MSVCP140.dll",
        "ucrtbase.dll",
}

goes2pf_a = Analysis(
    ['goes2pf.py'],
    pathex=[],
    datas=[
        ( "README.md", '.' ),
        ( "ACKNOWLEDGMENTS.md", "." ),
    ],
    hiddenimports=['packaging', 'pyproj'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# exclude binaries
toKeep = []

for (dest, source, kind) in goes2pf_a.binaries:
    filename = os.path.split(dest)[1]
    if filename.startswith("api-ms-win-")  or \
       filename.startswith("VCRUNTIME140") or \
       filename in EXCLUDE                    :
        continue

    toKeep.append((dest, source, kind))

goes2pf_a.binaries = toKeep

goes2pf_pyz = PYZ(goes2pf_a.pure)

goes2pf_exe = EXE(
    goes2pf_pyz,
    goes2pf_a.scripts,
    [],
    exclude_binaries=True,
    name='goes2pf',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    #icon=[
    #    "icon\\icon16.ico",
    #    "icon\\icon32.ico",
    #    "icon\\icon512.ico"
    #    ],
)

coll = COLLECT(
    geos2pf_exe,
    geos2pf_a.binaries,
    geos2pf_a.datas,
    geos2pf_ui_exe,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='geos2pf',
)
