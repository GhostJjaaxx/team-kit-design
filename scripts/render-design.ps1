# Name: QiuCheng Zhen
# Nickname: HuangXiaoYunMeiMei WoXiHuanNi
# ID: 2400012917

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('01-charcoal-amber', '02-cream-burgundy', '03-white-blue-code')]
    [string]$Design,

    [string]$OutputPath,
    [switch]$WithLogo,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($env:OS -ne 'Windows_NT') {
    throw 'This renderer requires Windows and PowerShell 5.1 or 7.'
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = [IO.Path]::GetFullPath((Join-Path $repoRoot "designs/$Design/source"))
$configPath = Join-Path $sourceDir 'composition.json'
if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Composition config not found: $configPath"
}

function Resolve-SourceImage {
    param($RelativePath)

    if ($RelativePath -isnot [string] -or [string]::IsNullOrWhiteSpace($RelativePath) -or
        [IO.Path]::IsPathRooted($RelativePath)) {
        throw 'Image paths in composition.json must be relative to its source directory.'
    }
    $resolved = [IO.Path]::GetFullPath((Join-Path $sourceDir $RelativePath))
    $prefix = $sourceDir.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Image path escapes the source directory: $RelativePath"
    }
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) {
        throw "Source image not found: $resolved"
    }
    return $resolved
}

function Read-Integer {
    param($Value, [string]$Name, [int]$Minimum)

    if ($null -eq $Value -or $Value -is [string] -or $Value -is [bool]) {
        throw "overlay.$Name must be an integer >= $Minimum."
    }
    try { $number = [double]$Value } catch {
        throw "overlay.$Name must be an integer >= $Minimum."
    }
    if ([double]::IsNaN($number) -or [double]::IsInfinity($number) -or
        $number -lt $Minimum -or $number -gt [int]::MaxValue -or
        [math]::Truncate($number) -ne $number) {
        throw "overlay.$Name must be an integer >= $Minimum."
    }
    return [int]$number
}

$config = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($null -eq $config -or $null -eq $config.PSObject.Properties['base'] -or
    $null -eq $config.PSObject.Properties['overlay'] -or $null -eq $config.overlay) {
    throw 'composition.json must contain base and overlay.'
}
foreach ($name in @('enabled', 'file', 'x', 'y', 'width', 'height')) {
    if ($null -eq $config.overlay.PSObject.Properties[$name]) {
        throw "Missing overlay.$name in composition.json."
    }
}
if ($config.overlay.enabled -isnot [bool]) {
    throw 'overlay.enabled must be a JSON boolean (true or false).'
}

$basePath = Resolve-SourceImage $config.base
$logoPath = Resolve-SourceImage $config.overlay.file
$x = Read-Integer $config.overlay.x 'x' 0
$y = Read-Integer $config.overlay.y 'y' 0
$width = Read-Integer $config.overlay.width 'width' 1
$height = Read-Integer $config.overlay.height 'height' 1
$useLogo = $WithLogo.IsPresent -or $config.overlay.enabled

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $repoRoot "generated/$Design/preview.png"
}
$destination = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$destination = [IO.Path]::GetFullPath($destination)
if ([IO.Path]::GetExtension($destination) -ine '.png') {
    throw 'OutputPath must end with .png.'
}
foreach ($inputPath in @($basePath, $logoPath)) {
    if ($destination.Equals($inputPath, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'OutputPath must not overwrite a source image, even with -Force.'
    }
}
if (Test-Path -LiteralPath $destination -PathType Container) {
    throw "OutputPath is a directory: $destination"
}
if ((Test-Path -LiteralPath $destination) -and -not $Force) {
    throw "Output already exists. Choose another OutputPath or use -Force: $destination"
}

Add-Type -AssemblyName System.Drawing
$baseImage = $null
$logoImage = $null
$scaledLogo = $null
$scaleGraphics = $null
$imageAttributes = $null
$canvas = $null
$canvasGraphics = $null
$outputStream = $null

try {
    $baseImage = [Drawing.Image]::FromFile($basePath)
    if ([long]$x + $width -gt $baseImage.Width -or [long]$y + $height -gt $baseImage.Height) {
        throw "The overlay rectangle exceeds the base image ($($baseImage.Width) x $($baseImage.Height))."
    }
    $outputDir = Split-Path -Parent $destination
    [void][IO.Directory]::CreateDirectory($outputDir)

    if (-not $useLogo) {
        if ($baseImage.RawFormat.Guid -ne [Drawing.Imaging.ImageFormat]::Png.Guid) {
            throw 'The base image must be PNG for unchanged, lossless copying.'
        }
        $baseImage.Dispose()
        $baseImage = $null
        [IO.File]::Copy($basePath, $destination, $Force.IsPresent)
    } else {
        $logoImage = [Drawing.Image]::FromFile($logoPath)
        $scaledLogo = [Drawing.Bitmap]::new($width, $height, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $scaleGraphics = [Drawing.Graphics]::FromImage($scaledLogo)
        $scaleGraphics.Clear([Drawing.Color]::Transparent)
        $scaleGraphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceCopy
        $scaleGraphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $scaleGraphics.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $imageAttributes = [Drawing.Imaging.ImageAttributes]::new()
        $imageAttributes.SetWrapMode([Drawing.Drawing2D.WrapMode]::TileFlipXY)
        $targetRect = [Drawing.Rectangle]::new(0, 0, $width, $height)
        $scaleGraphics.DrawImage($logoImage, $targetRect, 0, 0, $logoImage.Width, $logoImage.Height,
            [Drawing.GraphicsUnit]::Pixel, $imageAttributes)
        $scaleGraphics.Dispose()
        $scaleGraphics = $null

        $canvas = [Drawing.Bitmap]::new($baseImage.Width, $baseImage.Height, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $canvasGraphics = [Drawing.Graphics]::FromImage($canvas)
        $canvasGraphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceCopy
        $canvasGraphics.DrawImageUnscaled($baseImage, 0, 0)
        $canvasGraphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceOver
        $canvasGraphics.DrawImageUnscaled($scaledLogo, $x, $y)
        $canvasGraphics.Dispose()
        $canvasGraphics = $null

        $fileMode = [IO.FileMode]::CreateNew
        if ($Force) { $fileMode = [IO.FileMode]::Create }
        $outputStream = [IO.File]::Open($destination, $fileMode, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $canvas.Save($outputStream, [Drawing.Imaging.ImageFormat]::Png)
    }
} finally {
    foreach ($resource in @($outputStream, $canvasGraphics, $canvas, $imageAttributes,
            $scaleGraphics, $scaledLogo, $logoImage, $baseImage)) {
        if ($null -ne $resource) { $resource.Dispose() }
    }
}

Write-Output $destination
