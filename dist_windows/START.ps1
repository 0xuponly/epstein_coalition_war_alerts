Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Telegram channel forwarder (Windows)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Set-Location $PSScriptRoot
python windows_launcher.py
Write-Host ""
Write-Host "Closed." -ForegroundColor Yellow
Read-Host "Press Enter to continue"
