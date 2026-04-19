# TarDAL-Poss: build PyInstaller backend EXE (same behavior as build_backend_exe.bat).
# Usage:  .\scripts\Build-BackendExe.ps1
# Optional: $env:FORCE_NPM = '1' to rebuild frontend even when frontend\dist exists.

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

Write-Host '========================================'
Write-Host '  TarDAL-Poss: build backend EXE'
Write-Host '========================================'
Write-Host "Root: $root"
Write-Host ''

$w1 = Join-Path $root 'weights\v1\tardal-dt.pth'
$w2 = Join-Path $root 'weights\v1\mask-u2.pth'
if (-not (Test-Path -LiteralPath $w1)) {
    Write-Error "Missing fuse weight: $w1 — place tardal-dt.pth here for offline judge bundle."
}
if (-not (Test-Path -LiteralPath $w2)) {
    Write-Error "Missing saliency weight: $w2 — place mask-u2.pth here for offline judge bundle."
}

$forceNpm = ($env:FORCE_NPM -eq '1')
$distIndex = Join-Path $root 'frontend\dist\index.html'
$runNpm = $forceNpm -or -not (Test-Path -LiteralPath $distIndex)

if (-not $runNpm) {
    Write-Host 'SKIP npm: frontend\dist already present. Set $env:FORCE_NPM=1 to rebuild.'
} else {
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        Write-Error 'npm not found. Install Node.js LTS, or build frontend elsewhere and copy frontend\dist here.'
    }
    $nm = Join-Path $root 'frontend\node_modules'
    if (-not (Test-Path -LiteralPath $nm)) {
        Write-Host '[npm] npm install ...'
        Push-Location (Join-Path $root 'frontend')
        try {
            npm install
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        } finally {
            Pop-Location
        }
    }
    Write-Host '[npm] npm run build ...'
    Push-Location (Join-Path $root 'frontend')
    try {
        npm run build
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } finally {
        Pop-Location
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $root 'frontend\dist\index.html'))) {
    Write-Error 'frontend\dist\index.html not found.'
}

& python -c 'import flask' 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host '[pip] pip install -r requirements.txt ...'
    pip install -r (Join-Path $root 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& pip show pyinstaller 2>$null
if ($LASTEXITCODE -ne 0) {
    pip install 'pyinstaller>=6.0'
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host ''
Write-Host 'Running PyInstaller - this may take a long time.'
Set-Location $root
& pyinstaller --clean --noconfirm (Join-Path $root 'tardal_backend.spec')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$distBackend = Join-Path $root 'dist\TarDAL-Poss-Backend'
& (Join-Path $PSScriptRoot 'Copy-PictureExampleToDist.ps1') -DistBackendRoot $distBackend

Write-Host ''
Write-Host "Done. Output: $distBackend"
Write-Host 'Run offline demo: dist\TarDAL-Poss-Backend\TarDAL-Poss-Backend.exe or RUN.bat'
Write-Host ''
