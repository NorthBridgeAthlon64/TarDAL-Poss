# After PyInstaller: complete dist\TarDAL-Poss-Backend next to the exe (no separate zip step).
# - readme.txt: project root install + usage
# - packaging\judge: RUN.bat, 评委说明.txt
# - Picture-Example: merged from repo root and packaging\judge (sample images)
param(
    [Parameter(Mandatory = $true)]
    [string]$DistBackendRoot
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$dest = Join-Path $DistBackendRoot 'Picture-Example'

if (-not (Test-Path -LiteralPath $DistBackendRoot)) {
    Write-Error "Dist folder not found: $DistBackendRoot"
}

$readmeSrc = Join-Path $root 'readme.txt'
if (Test-Path -LiteralPath $readmeSrc) {
    Copy-Item -LiteralPath $readmeSrc -Destination (Join-Path $DistBackendRoot 'readme.txt') -Force
    Write-Host "[readme.txt] installation and usage doc -> $DistBackendRoot\readme.txt"
} else {
    Write-Warning "Missing: $readmeSrc — not copied to dist."
}

$runBat = Join-Path $root 'packaging\judge\RUN.bat'
if (Test-Path -LiteralPath $runBat) {
    Copy-Item -LiteralPath $runBat -Destination (Join-Path $DistBackendRoot 'RUN.bat') -Force
    Write-Host "[RUN.bat] -> $DistBackendRoot\RUN.bat"
}
$judgeTxt = Join-Path $root 'packaging\judge\评委说明.txt'
if (Test-Path -LiteralPath $judgeTxt) {
    Copy-Item -LiteralPath $judgeTxt -Destination (Join-Path $DistBackendRoot '评委说明.txt') -Force
    Write-Host "[评委说明.txt] -> $DistBackendRoot\评委说明.txt"
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null

$src1 = Join-Path $root 'Picture-Example'
$src2 = Join-Path $root 'packaging\judge\Picture-Example'

foreach ($src in @($src1, $src2)) {
    if (-not (Test-Path -LiteralPath $src)) { continue }
    Get-ChildItem -LiteralPath $src -Force -ErrorAction SilentlyContinue | ForEach-Object {
        $target = Join-Path $dest $_.Name
        Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    }
    Write-Host "[Picture-Example] merged: $src -> $dest"
}
