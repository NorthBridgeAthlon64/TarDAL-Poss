# TarDAL-Poss: remove build caches and runtime artifacts (before source delivery).
# Usage:  .\scripts\clean_cache.ps1
#         .\scripts\clean_cache.ps1 -Full    # also removes frontend/node_modules
#Requires -Version 5.1
param(
    [switch]$Full
)

$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

Write-Host '========================================'
Write-Host '  TarDAL-Poss: clean cache'
Write-Host '========================================'
Write-Host "Root: $root"
if ($Full) {
    Write-Host 'Mode: FULL (will remove frontend\node_modules)'
} else {
    Write-Host 'Mode: default (keeps frontend\node_modules). Use -Full for minimal size.'
}
Write-Host ''

# Python __pycache__ (skip paths under node_modules)
Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__' -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '[\\/]node_modules[\\/]' } |
    ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }

function Remove-DirIfExists([string]$rel) {
    $p = Join-Path $root $rel
    if (Test-Path -LiteralPath $p) {
        Write-Host "Removing $rel ..."
        Remove-Item -LiteralPath $p -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function Clear-DirContents([string]$rel) {
    $p = Join-Path $root $rel
    if (-not (Test-Path -LiteralPath $p)) { return }
    Write-Host "Clearing $rel ..."
    Get-ChildItem -LiteralPath $p -Force -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

Remove-DirIfExists 'build'
Remove-DirIfExists 'dist'
Remove-DirIfExists 'frontend\dist'
Remove-DirIfExists 'frontend\node_modules\.vite'
Clear-DirContents 'backend\results'
Clear-DirContents 'backend\uploads'
Clear-DirContents 'runs'
Remove-DirIfExists 'wandb'

Get-ChildItem -LiteralPath $root -Filter '*.spec.bak' -File -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }

foreach ($name in @('.pytest_cache', '.mypy_cache', '.ruff_cache')) {
    Remove-DirIfExists $name
}

if ($Full -and (Test-Path -LiteralPath (Join-Path $root 'frontend\node_modules'))) {
    Write-Host 'Removing frontend\node_modules - may take a while ...'
    Remove-Item -LiteralPath (Join-Path $root 'frontend\node_modules') -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ''
Write-Host 'Done. Next: scripts\build_backend_exe.bat'
Write-Host 'If node_modules was removed, the build script will run npm install then npm run build.'
Write-Host ''
