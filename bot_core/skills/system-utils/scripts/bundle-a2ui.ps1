$ErrorActionPreference = "Stop"

function On-Error {
    Write-Error "A2UI bundling failed. Re-run with: pnpm canvas:a2ui:bundle"
    Write-Error "If this persists, verify pnpm deps and try again."
    exit 1
}

trap { On-Error }

$RootDir = Resolve-Path "$PSScriptRoot\.."
$HashFile = Join-Path $RootDir "src\canvas-host\a2ui\.bundle.hash"
$OutputFile = Join-Path $RootDir "src\canvas-host\a2ui\a2ui.bundle.js"
$A2UiRendererDir = Join-Path $RootDir "vendor\a2ui\renderers\lit"
$A2UiAppDir = Join-Path $RootDir "apps\shared\OpenClawKit\Tools\CanvasA2UI"

if (-not (Test-Path $A2UiRendererDir) -or -not (Test-Path $A2UiAppDir)) {
    Write-Host "A2UI sources missing; keeping prebuilt bundle."
    exit 0
}

$InputPaths = @(
    (Join-Path $RootDir "package.json"),
    (Join-Path $RootDir "pnpm-lock.yaml"),
    $A2UiRendererDir,
    $A2UiAppDir
)

# Compute hash using the extracted Node.js script
$Env:ROOT_DIR = $RootDir
$ComputeScript = Join-Path $PSScriptRoot "compute-a2ui-hash.mjs"
$CurrentHash = node $ComputeScript $InputPaths

if (Test-Path $HashFile) {
    $PreviousHash = Get-Content $HashFile -Raw
    if ($PreviousHash -eq $CurrentHash -and (Test-Path $OutputFile)) {
        Write-Host "A2UI bundle up to date; skipping."
        exit 0
    }
}

Write-Host "Building A2UI..."
pnpm exec tsc -p (Join-Path $A2UiRendererDir "tsconfig.json")
# rolldown might need explicit calling on Windows if not in PATH correctly, but pnpm exec usually handles it.
# We call rolldown directly assuming it is in node_modules/.bin
& (Join-Path $RootDir "node_modules\.bin\rolldown.cmd") -c (Join-Path $A2UiAppDir "rolldown.config.mjs")

Set-Content -Path $HashFile -Value $CurrentHash -NoNewline
Write-Host "A2UI bundle built successfully."
