$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot
$url = "http://127.0.0.1:4000/"
$config = "_config.yml,_config.dev.yml"

Write-Host "ZLinkTek local preview" -ForegroundColor Cyan
Write-Host "Site directory: $PSScriptRoot"
Write-Host "Preview URL: $url"
Write-Host ""

$listener = Get-NetTCPConnection -LocalPort 4000 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($listener) {
    Write-Host "Port 4000 is already in use. Checking the existing preview server." -ForegroundColor Yellow
    Write-Host "Owning process id: $($listener.OwningProcess)"
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
        if ($response.StatusCode -ne 200) {
            throw "HTTP status $($response.StatusCode)"
        }
        Start-Process $url
    }
    catch {
        Write-Host "The process on port 4000 is not a working website: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Stop process $($listener.OwningProcess), then run this script again."
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host ""
    Write-Host "If the page is stale, close the old preview window/process and run this script again."
    Read-Host "Press Enter to exit"
    exit 0
}

if (-not (Get-Command bundle -ErrorAction SilentlyContinue)) {
    Write-Host "Ruby Bundler command 'bundle' was not found." -ForegroundColor Red
    Write-Host "Please install Ruby/Bundler or run this script in the same environment where Jekyll can build the site."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting Jekyll. Keep this window open while previewing." -ForegroundColor Green
Write-Host "After editing Markdown files, Jekyll will rebuild automatically."
Write-Host "Press Ctrl+C in this window to stop the preview server."
Write-Host ""

# Build once before starting the server. This prevents Jekyll from serving a
# missing or stale _site directory when the initial build is skipped.
bundle exec jekyll build --config $config
if ($LASTEXITCODE -ne 0) {
    Write-Host "Jekyll build failed. Review the error above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit $LASTEXITCODE
}

Start-Process powershell -WindowStyle Hidden -ArgumentList @(
    "-NoProfile",
    "-Command",
    "for (`$i = 0; `$i -lt 30; `$i++) { try { Invoke-WebRequest -UseBasicParsing -Uri '$url' -TimeoutSec 1 | Out-Null; Start-Process '$url'; exit } catch { Start-Sleep -Milliseconds 500 } }"
)

bundle exec jekyll serve --config $config --host 127.0.0.1 --port 4000 --watch
