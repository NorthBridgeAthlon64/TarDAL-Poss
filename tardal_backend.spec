# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 规格文件：将 backend/app.py 打成 Windows 可执行程序（文件夹模式 onedir）。
# 用法（在项目根目录）： pip install pyinstaller && pyinstaller tardal_backend.spec
# 输出：dist/TarDAL-Poss-Backend/TarDAL-Poss-Backend.exe

block_cipher = None

from pathlib import Path

try:
    from PyInstaller.utils.hooks import collect_all, collect_data_files
except ImportError:
    collect_all = None
    collect_data_files = None

ROOT = Path(SPECPATH).resolve()

datas = [
    (str(ROOT / 'config'), 'config'),
    (str(ROOT / 'module'), 'module'),
    (str(ROOT / 'pipeline'), 'pipeline'),
    (str(ROOT / 'functions'), 'functions'),
    (str(ROOT / 'loader'), 'loader'),
    # 打包前须先执行: cd frontend && npm run build
    (str(ROOT / 'frontend' / 'dist'), 'frontend/dist'),
]

# 离线评委包：融合与显著性权重必须打入 _MEIPASS，运行时不访问外网下载
_wv1 = ROOT / 'weights' / 'v1'
for _req in ('tardal-dt.pth', 'mask-u2.pth'):
    _p = _wv1 / _req
    if not _p.is_file():
        raise SystemExit(
            '[tardal_backend.spec] 缺少 %s — 请从 TarDAL 官方 Release 下载后放入 weights/v1/ 再执行打包。' % (_p,)
        )
datas.append((str(_wv1), 'weights/v1'))

binaries = []
hiddenimports = []

if collect_all:
    for pkg in ('torch', 'torchvision', 'kornia'):
        try:
            d, b, h = collect_all(pkg)
            datas += d
            binaries += b
            hiddenimports += h
        except Exception as exc:
            print(f'[tardal_backend.spec] collect_all({pkg!r}) 跳过: {exc}')

if collect_data_files:
    for pkg in ('cv2',):
        try:
            datas += collect_data_files(pkg)
        except Exception as exc:
            print(f'[tardal_backend.spec] collect_data_files({pkg!r}) 跳过: {exc}')

a = Analysis(
    [str(ROOT / 'backend' / 'app.py')],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='TarDAL-Poss-Backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
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
    upx=False,
    upx_exclude=[],
    name='TarDAL-Poss-Backend',
)
