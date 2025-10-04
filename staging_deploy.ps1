# ============================================
# Capstone Hub - Staging Deployment Script
# Based on: FINAL_PRE_PRODUCTION_REVIEW.md
# ============================================
# This script:
# 1. Verifies Railway CLI login
# 2. Generates fresh SECRET_KEY
# 3. Sets staging environment variables
# 4. Deploys to Railway staging
# 5. Opens browser to staging URL
# 6. Auto-runs smoke test after 10 seconds
# ============================================

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Capstone Hub - Staging Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ============================================
# Step 1: Verify Railway CLI Login
# ============================================
Write-Host "[1/6] Verifying Railway CLI login..." -ForegroundColor Yellow

try {
    $railwayWhoami = railway whoami 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        throw "Not logged in"
    }
    Write-Host "✓ Railway CLI authenticated: $($railwayWhoami.Trim())" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Railway CLI not logged in" -ForegroundColor Red
    Write-Host "`nPlease run: railway login" -ForegroundColor Yellow
    Write-Host "Then re-run this script.`n" -ForegroundColor Yellow
    exit 1
}

# ============================================
# Step 2: Generate Fresh SECRET_KEY
# ============================================
Write-Host "`n[2/6] Generating fresh SECRET_KEY..." -ForegroundColor Yellow

# Generate 32-byte hex string (64 hex characters)
$secretKey = -join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Minimum 0 -Maximum 256) })

if ($secretKey.Length -ne 64) {
    Write-Host "✗ ERROR: Failed to generate valid SECRET_KEY" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Generated 32-byte SECRET_KEY (64 hex chars)" -ForegroundColor Green

# ============================================
# Step 3: Initial Deploy (Creates Service)
# ============================================
Write-Host "`n[3/6] Deploying to Railway (auto-creates service if needed)..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes. Please wait..." -ForegroundColor Gray

try {
    $deployOutput = railway up --detach 2>&1 | Out-String
    Write-Host $deployOutput -ForegroundColor Gray
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠ Initial deployment had issues, but continuing..." -ForegroundColor Yellow
    } else {
        Write-Host "✓ Initial deployment triggered" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Initial deployment warning: $_" -ForegroundColor Yellow
    Write-Host "Continuing with variable setup..." -ForegroundColor Gray
}

# Give Railway a moment to create the service
Start-Sleep -Seconds 3

# ============================================
# Step 4: Set Environment Variables
# ============================================
Write-Host "`n[4/6] Setting staging environment variables..." -ForegroundColor Yellow

try {
    # Use --set flag with railway variables (more reliable)
    railway variables --set "FLASK_ENV=production" --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ FLASK_ENV=production" -ForegroundColor Gray
    }

    railway variables --set "SECRET_KEY=$secretKey" --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ SECRET_KEY=<generated>" -ForegroundColor Gray
    }

    railway variables --set "PORT=5000" --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ PORT=5000" -ForegroundColor Gray
    }

    railway variables --set "ADMIN_PASSWORD=HLStearns2025!" --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ ADMIN_PASSWORD=HLStearns2025! (staging default)" -ForegroundColor Gray
    }

    Write-Host "✓ Environment variables configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ WARNING: Some variables may not be set" -ForegroundColor Yellow
    Write-Host "Details: $_" -ForegroundColor Yellow
    Write-Host "Continuing with deployment..." -ForegroundColor Gray
}

# ============================================
# Step 5: Deploy with New Variables
# ============================================
Write-Host "`n[5/6] Deploying with environment variables..." -ForegroundColor Yellow
Write-Host "This triggers a new build with your secrets. Please wait..." -ForegroundColor Gray

try {
    $deployOutput = railway up 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Deployment failed" -ForegroundColor Red
        Write-Host $deployOutput -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Deployment successful with secrets" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Deployment failed" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    exit 1
}

# ============================================
# Step 6: Get Staging URL and Save to File
# ============================================
Write-Host "`n[6/7] Retrieving staging URL..." -ForegroundColor Yellow

try {
    # Try to get URL from Railway status
    $statusJson = railway status --json 2>&1 | Out-String
    $statusObj = $statusJson | ConvertFrom-Json -ErrorAction SilentlyContinue
    $stagingUrl = $statusObj.deployments[0].staticUrl

    if (-not $stagingUrl) {
        # Fallback: try different JSON path
        $stagingUrl = $statusObj.url
    }

    if (-not $stagingUrl) {
        Write-Host "⚠ WARNING: Could not auto-detect staging URL" -ForegroundColor Yellow
        Write-Host "Please enter your staging URL manually:" -ForegroundColor Yellow
        $stagingUrl = Read-Host "Staging URL"
    }

    # Ensure URL starts with https://
    if ($stagingUrl -notmatch '^https?://') {
        $stagingUrl = "https://$stagingUrl"
    }

    # Save to file
    $stagingUrl | Out-File -FilePath ".staging_url" -Encoding UTF8 -NoNewline
    Write-Host "✓ Staging URL: $stagingUrl" -ForegroundColor Green
    Write-Host "✓ URL saved to .staging_url" -ForegroundColor Gray
} catch {
    Write-Host "✗ ERROR: Failed to retrieve staging URL" -ForegroundColor Red
    Write-Host "Run manually: railway status" -ForegroundColor Yellow
    exit 1
}

# ============================================
# Step 7: Open Browser and Run Smoke Test
# ============================================
Write-Host "`n[7/7] Opening staging URL in browser..." -ForegroundColor Yellow

try {
    Start-Process $stagingUrl
    Write-Host "✓ Browser opened" -ForegroundColor Green
} catch {
    Write-Host "⚠ Could not open browser automatically" -ForegroundColor Yellow
    Write-Host "Please open manually: $stagingUrl" -ForegroundColor Yellow
}

# Wait 10 seconds for app to fully start
Write-Host "`nWaiting 10 seconds for app to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 10

# Auto-run smoke test if Python is available
Write-Host "`nRunning smoke test..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    try {
        # Run smoke test and capture exit code
        python smoke_staging.py --url $stagingUrl
        $smokeExitCode = $LASTEXITCODE

        if ($smokeExitCode -eq 0) {
            Write-Host "`n========================================" -ForegroundColor Green
            Write-Host "✓ STAGING DEPLOYMENT SUCCESSFUL" -ForegroundColor Green
            Write-Host "✓ ALL SMOKE TESTS PASSED" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "`nStaging URL: $stagingUrl" -ForegroundColor Cyan
            Write-Host "Report: staging_smoke_report.txt" -ForegroundColor Cyan
            Write-Host "`nNEXT STEP:" -ForegroundColor Yellow
            Write-Host "  .\promote_to_prod.ps1" -ForegroundColor White
            Write-Host ""
            exit 0
        } else {
            Write-Host "`n========================================" -ForegroundColor Red
            Write-Host "✗ SMOKE TESTS FAILED" -ForegroundColor Red
            Write-Host "========================================" -ForegroundColor Red
            Write-Host "`nReview: staging_smoke_report.txt" -ForegroundColor Yellow
            Write-Host "Fix issues and re-run: .\staging_deploy.ps1" -ForegroundColor Yellow
            Write-Host ""
            exit 1
        }
    } catch {
        Write-Host "⚠ Could not run smoke test automatically" -ForegroundColor Yellow
        Write-Host "Run manually: python smoke_staging.py" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "⚠ Python not found in PATH" -ForegroundColor Yellow
    Write-Host "Run smoke test manually: python smoke_staging.py" -ForegroundColor Yellow
    Write-Host "`nStaging URL: $stagingUrl" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}
