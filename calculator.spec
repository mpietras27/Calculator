# Calculator.spec — FINAL working PyInstaller spec for PySide6 (2025)

from PyInstaller.utils.hooks import collect_all, collect_submodules
import PySide6

# Collect all PySide6 resources (DLLs, plugins, qml, etc.)
datas, binaries, hiddenimports = collect_all('PySide6')

# Force inclusion of all QtTools and widget modules
hiddenimports += collect_submodules("PySide6.QtCore")
hiddenimports += collect_submodules("PySide6.QtGui")
hiddenimports += collect_submodules("PySide6.QtWidgets")
hiddenimports += collect_submodules("PySide6.QtQml")
hiddenimports += collect_submodules("PySide6.QtQuick")
hiddenimports += collect_submodules("PySide6.QtNetwork")

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='Calculator'
)
