# -*- mode: python ; coding: utf-8 -*-
# this is a .spec file for PyInstaller used to create windows package

datas = [
    ('data', 'data'),
]

block_cipher = None

a = Analysis(['wopeditor\\wopeditor.py'],
             pathex=['C:\\Users\\yac\\source\\py\\wopeditor'],
             binaries=[],
             datas=datas,
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
          name='wopeditor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='wopeditor')
