# 读取所有配置文件

$files = Get-ChildItem "E:\PulsareonThinker\config" -Filter "*.md"

foreach ($file in $files) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "文件: $($file.Name)" -ForegroundColor Yellow
    Write-Host "大小: $($file.Length) bytes" -ForegroundColor Gray
    Write-Host "========================================`n" -ForegroundColor Cyan

    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    # 使用Write-Host输出原始内容
    $content
}
