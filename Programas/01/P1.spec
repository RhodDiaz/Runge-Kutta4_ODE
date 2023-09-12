# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['ventanita2.py'],
             pathex=[''],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='R-K-Tere',
          debug=False,
          bootloader_ignore_signals=False,
	  	strip=False,
          upx=True,
          upx_exclude=[],
          upx_include=[],
          runtime_tmpdir=None,
          console=False , # si deseas una ventana de consola
          icon='icono.ico', # si deseas agregar un icono
          version='1.0', # versión del programa
          description='Resuelve EDO por los métodos RungeKutta',
          author='Díaz, Eduardo, Correa',
		onefile=True)

