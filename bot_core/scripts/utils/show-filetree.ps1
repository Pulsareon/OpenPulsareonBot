# Generate file tree for PulsareonThinker

function Get-FileTree {
    param(
        [string]$Path,
        [int]$Depth = 0,
        [int]$MaxDepth = 6
    )

    if ($Depth -gt $MaxDepth) {
        return
    }

    $indent = "  " * $Depth

    # Get items
    $items = Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Sort-Object { $_.PSIsContainer }, Name

    foreach ($item in $items) {
        # Skip hidden and system files
        if ($item.Attributes -match "Hidden|System") {
            continue
        }

        # Skip .git and .DS_Store
        if ($item.Name -eq ".git" -or $item.Name -eq ".DS_Store" -or $item.Name -eq "node_modules") {
            continue
        }

        if ($item.PSIsContainer) {
            Write-Host "$indent├─ $($item.Name)/" -ForegroundColor Cyan
            Get-FileTree -Path $item.FullName -Depth ($Depth + 1) -MaxDepth $MaxDepth
        } else {
            $sizeInfo = if ($item.Length -gt 0) { " ($([math]::Round($item.Length / 1KB, 1))KB)" } else { "" }
            $ext = $item.Extension
            $color = switch ($ext) {
                ".md" { "Green" }
                ".ps1" { "Yellow" }
                ".log" { "Gray" }
                ".json" { "Blue" }
                default { "White" }
            }
            Write-Host "$indent├─ $($item.Name)$sizeInfo" -ForegroundColor $color
        }
    }
}

Write-Host "`n=== PulsareonThinker New Home ===" -ForegroundColor Magenta
Write-Host "E:\PulsareonThinker`n"

Get-FileTree -Path "E:\PulsareonThinker" -Depth 0 -MaxDepth 4

Write-Host "`n=== End of Tree ===" -ForegroundColor Magenta
