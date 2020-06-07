# -*- mode: python ; coding: utf-8 -*-
import sys
site_packages = [path for path in sys.path if path.rstrip("/\\").endswith('site-packages')]

from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(['/Users/vonkuptschino/Desktop/derdiedas/main.py'],
             pathex=['/Users/vonkuptschino/Desktop/derdiedas'],
             binaries=[],
             datas=[(site_packages_, ".") for site_packages_ in site_packages],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='derdiedas',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('/Users/vonkuptschino/Desktop/derdiedas/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='derdiedas')
app = BUNDLE(coll,
             name='derdiedas.app',
             icon='icon.icns',
             bundle_identifier=None)
