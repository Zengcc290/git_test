[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Url,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [Parameter(Mandatory = $true)]
    [long]$ExpectedBytes,

    [long]$SegmentBytes = 268435456
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($SegmentBytes -le 0) {
    throw "SegmentBytes must be greater than zero."
}

$parent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$parent = (Resolve-Path -LiteralPath $parent).Path
$leaf = Split-Path -Leaf $OutputPath
$output = Join-Path $parent $leaf
$part = "$output.part"

if (Test-Path -LiteralPath $output -PathType Leaf) {
    $existing = (Get-Item -LiteralPath $output).Length
    if ($existing -eq $ExpectedBytes) {
        Write-Output "Already complete: $output ($existing bytes)"
        exit 0
    }
    throw "Output already exists with an unexpected size: $output ($existing bytes)."
}

$partLength = 0L
if (Test-Path -LiteralPath $part -PathType Leaf) {
    $partLength = (Get-Item -LiteralPath $part).Length
    if (($partLength -gt $ExpectedBytes) -or (($partLength % $SegmentBytes) -ne 0)) {
        throw "Partial file is not aligned to a completed segment: $part ($partLength bytes)."
    }
}

$segmentNumber = [long]($partLength / $SegmentBytes)
while ($partLength -lt $ExpectedBytes) {
    $start = $partLength
    $end = [Math]::Min($ExpectedBytes - 1L, $start + $SegmentBytes - 1L)
    $expectedSegmentBytes = $end - $start + 1L
    $segmentPath = "$part.$segmentNumber"

    if (Test-Path -LiteralPath $segmentPath -PathType Leaf) {
        [System.IO.File]::Delete($segmentPath)
    }

    Write-Output ("Downloading segment {0}: bytes {1}-{2}" -f $segmentNumber, $start, $end)
    $curlArgs = @(
        "-L", "--fail", "--retry", "6", "--retry-all-errors", "--retry-delay", "5",
        "--connect-timeout", "30", "--range", "$start-$end", "--output", $segmentPath, $Url
    )
    $process = Start-Process -FilePath "curl.exe" -ArgumentList $curlArgs -NoNewWindow -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        throw "curl failed for segment $segmentNumber with exit code $($process.ExitCode)."
    }

    $actualSegmentBytes = (Get-Item -LiteralPath $segmentPath).Length
    if ($actualSegmentBytes -ne $expectedSegmentBytes) {
        throw "Segment $segmentNumber has $actualSegmentBytes bytes; expected $expectedSegmentBytes."
    }

    $inputStream = [System.IO.File]::OpenRead($segmentPath)
    try {
        $outputStream = [System.IO.File]::Open($part, [System.IO.FileMode]::Append, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
        try {
            $inputStream.CopyTo($outputStream, 1048576)
        }
        finally {
            $outputStream.Dispose()
        }
    }
    finally {
        $inputStream.Dispose()
    }
    [System.IO.File]::Delete($segmentPath)

    $partLength += $actualSegmentBytes
    $segmentNumber++
    Write-Output ("Completed: {0:N2}% ({1}/{2} bytes)" -f (($partLength / $ExpectedBytes) * 100), $partLength, $ExpectedBytes)
}

$finalLength = (Get-Item -LiteralPath $part).Length
if ($finalLength -ne $ExpectedBytes) {
    throw "Final partial file has $finalLength bytes; expected $ExpectedBytes."
}

[System.IO.File]::Move($part, $output)
Write-Output "Complete: $output ($ExpectedBytes bytes)"
