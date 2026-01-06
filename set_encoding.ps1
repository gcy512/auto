# PowerShell脚本：设置终端编码为UTF-8
# 在运行测试前执行此脚本，或在PowerShell中执行：chcp 65001

# 设置控制台代码页为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 设置环境变量
$env:PYTHONIOENCODING = "utf-8"

Write-Host "编码已设置为UTF-8" -ForegroundColor Green
Write-Host "PYTHONIOENCODING = $env:PYTHONIOENCODING" -ForegroundColor Green

