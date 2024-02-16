# -*- mode: python ; coding: utf-8 -*-

import os, sys
import shutil


def copy_files_to_dist(datas, current_dir):
    # Diretório de destino, que é a pasta 'dist'
    dist_dir = os.path.join(current_dir, "dist")
    for origem_arquivo, destino_arquivo in datas:
        origem_completa = os.path.join(current_dir, origem_arquivo)
        destino_completo = os.path.join(dist_dir, destino_arquivo)

        if os.path.exists(origem_completa):
            # Cria os diretórios de destino, se necessário
            os.makedirs(os.path.dirname(destino_completo), exist_ok=True)

            # Copia o arquivo
            shutil.copy(origem_completa, destino_completo)


current_path = os.path.dirname(os.path.abspath(sys.argv[0]))

data = [
    (
        os.path.join("src", "images", "logo.png"),
        os.path.join("src", "images", "logo.png"),
    ),
    (
        os.path.join("src", "images", "logo.ico"),
        os.path.join("src", "images", "logo.ico"),
    ),
    (
        os.path.join("src", "cache.json"),
        os.path.join("src", "cache.json"),
    ),
    # (
    #     os.path.join("src", "logs_xml_sieg_downloader.log"),
    #     os.path.join("src", "logs_xml_sieg_downloader.log"),
    # )

    
]

copy_files_to_dist(data, current_path)

file_name = "SIEG_DOWNLOADER.py"

print(file_name)
a = Analysis(
    [file_name],
    pathex=[current_path],
    binaries=[],
    datas=data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name=file_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["src\\images\\logo.ico"],
)
