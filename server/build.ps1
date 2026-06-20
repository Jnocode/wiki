# Build script: copies wiki .md into VitePress project and builds static site
# Output: dist/

param (
    [string]$WikiRoot = "D:\Personal_Website\wiki",
    [string]$FrontendRoot = "D:\Personal_Website\wiki\server\frontend"
)

# Clean old
$targets = @("entities", "concepts", "comparisons")
foreach ($t in $targets) {
    $p = Join-Path $FrontendRoot $t
    if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}

# Copy .md files
foreach ($t in $targets) {
    $src = Join-Path $WikiRoot $t
    $dst = Join-Path $FrontendRoot $t
    if (Test-Path $src) {
        Copy-Item -Recurse -Path $src -Destination $dst
    }
}

# Copy SCHEMA.md and other root .md files (skip index.md since VitePress has its own)
Get-ChildItem -Path $WikiRoot -Filter "*.md" -File | Where-Object {
    $_.Name -ne "index.md" -and $_.Name -ne "log.md"
} | ForEach-Object {
    Copy-Item $_.FullName -Destination (Join-Path $FrontendRoot $_.Name) -Force
}

Write-Host "✅ Wiki files copied. Building VitePress..." -ForegroundColor Green

# Build
Set-Location $FrontendRoot
npx vitepress build

Write-Host "✅ Build complete! Output: dist/" -ForegroundColor Green
