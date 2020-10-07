# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['H:\\Park_doc\\python\\wh_support\\main.py'],
             pathex=['H:\\Park_doc\\python\\wh_support'],
             binaries=[],
             datas=[('./exec', './exec'), ('./setting', './setting')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='H:\\Park_doc\\python\\wh_support\\icon\\Plug_in_Script.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
