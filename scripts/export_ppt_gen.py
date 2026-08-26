#!/usr/bin/env python3
"""export_ppt.ps1 — 通过PowerShell COM调用PPT导出PNG"""
CONTENT = """# Export PPT slides as PNG (1920x1080) via PowerPoint COM
$pptPath = "C:\Users\Lenovo\AppData\Local\Temp\\radar_pptv.pptx"
$outDir  = "C:\Users\Lenovo\AppData\Local\Temp\\ppt_slides"

if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force }

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptPath, 1, 0, 0)
$total = $pres.Slides.Count
Write-Host "PPT opened: $total slides"

for ($i = 1; $i -le $total; $i++) {
    $imgPath = Join-Path $outDir ("slide_{0:D2}.png" -f $i)
    $slide = $pres.Slides($i)
    $slide.Export($imgPath, "png", 1920, 1080)
    Write-Host "  Exported slide $i"
}

$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "DONE! $total slides exported"
"""
print(CONTENT)
