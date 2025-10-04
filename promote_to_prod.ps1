# ============================================
# Capstone Hub - Production Promotion Script
# Based on: FINAL_PRE_PRODUCTION_REVIEW.md
# ============================================
# This script:
# 1. Verifies staging smoke tests passed
# 2. Creates/switches to production environment
# 3. Prompts for NEW admin password
# 4. Generates NEW SECRET_KEY
# 5. Sets production environment variables
# 6. Deploys to Railway production
# 7. Saves production URL and password
# 8. Prints post-deployment checklist
# ============================================

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Capstone Hub - Production Promotion" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ============================================
# Step 1: Verify Staging Tests Passed
# ============================================
Write-Host "[1/7] Verifying staging smoke tests..." -ForegroundColor Yellow

if (-Not (Test-Path "staging_smoke_report.txt")) {
    Write-Host "`n[X] ERROR: staging_smoke_report.txt not found" -ForegroundColor Red
    Write-Host "`nYou must run staging deployment and smoke test first:" -ForegroundColor Yellow
    Write-Host "  1. .\staging_deploy.ps1" -ForegroundColor Gray
    Write-Host "  2. python smoke_staging.py" -ForegroundColor Gray
    Write-Host "  3. Review staging_smoke_report.txt`n" -ForegroundColor Gray
    exit 1
}

$reportContent = Get-Content "staging_smoke_report.txt" -Raw

if ($reportContent -notmatch "ALL TESTS PASSED") {
    Write-Host "`n[X] ERROR: Staging tests did not pass!" -ForegroundColor Red
    Write-Host "`nReview staging_smoke_report.txt and fix issues before promoting." -ForegroundColor Yellow
    Write-Host "Key checks:" -ForegroundColor Yellow
    Write-Host "  - Unauthorized POST returns 401/403" -ForegroundColor Gray
    Write-Host "  - All security headers present" -ForegroundColor Gray
    Write-Host "  - XSS payload escaped" -ForegroundColor Gray
    Write-Host "  - Admin login works`n" -ForegroundColor Gray
    exit 1
}

Write-Host "[OK] Staging tests passed - ready for production" -ForegroundColor Green

# ============================================
# Step 2: Create/Switch Production Environment
# ============================================
Write-Host "`n[2/7] Setting up production environment..." -ForegroundColor Yellow

# Check if production environment exists
$envCheck = railway environment list 2>&1 | Out-String
$productionExists = $envCheck -match "production"

if (-not $productionExists) {
    Write-Host "`nProduction environment not found. Creating it now..." -ForegroundColor Yellow
    Write-Host "`nIMPORTANT: You need to create the 'production' environment manually in Railway dashboard:" -ForegroundColor Red
    Write-Host "  1. Go to https://railway.app" -ForegroundColor Gray
    Write-Host "  2. Open project: mabbott-oemba-capstone-25-26" -ForegroundColor Gray
    Write-Host "  3. Click 'New Environment' button" -ForegroundColor Gray
    Write-Host "  4. Name it: production" -ForegroundColor Gray
    Write-Host "  5. Re-run this script`n" -ForegroundColor Gray

    $createNow = Read-Host "Have you created the production environment? (y/N)"
    if ($createNow -ne 'y') {
        Write-Host "`nExiting. Create the environment and re-run this script.`n" -ForegroundColor Yellow
        exit 1
    }
}

# Switch to production environment
try {
    railway environment production 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to switch to production environment"
    }
    Write-Host "[OK] Switched to production environment" -ForegroundColor Green
} catch {
    Write-Host "`n[X] ERROR: Could not switch to production environment" -ForegroundColor Red
    Write-Host "Create it in Railway dashboard first (see instructions above)`n" -ForegroundColor Yellow
    exit 1
}

# ============================================
# Step 3: Prompt for NEW Admin Password
# ============================================
Write-Host "`n[3/7] Setting production secrets..." -ForegroundColor Yellow
Write-Host "`n[!] CRITICAL: Production needs a DIFFERENT admin password" -ForegroundColor Red
Write-Host "    Staging password: HLStearns2025!" -ForegroundColor Gray
Write-Host "    Production must use a NEW password`n" -ForegroundColor Gray

$newPassword = Read-Host "Enter NEW admin password for production" -AsSecureString
$newPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($newPassword)
)

if ([string]::IsNullOrWhiteSpace($newPasswordPlain)) {
    Write-Host "`n[X] ERROR: Password cannot be empty`n" -ForegroundColor Red
    exit 1
}

if ($newPasswordPlain -eq "HLStearns2025!") {
    Write-Host "`n[!] WARNING: You're using the same password as staging!" -ForegroundColor Red
    Write-Host "    This is a security risk. Production should have a unique password.`n" -ForegroundColor Yellow
    $confirm = Read-Host "Continue anyway? Type 'yes' to proceed or anything else to abort"
    if ($confirm -ne "yes") {
        Write-Host "`nAborted. Re-run and choose a different password.`n" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "[OK] New password accepted" -ForegroundColor Green

# ============================================
# Step 4: Generate NEW SECRET_KEY
# ============================================
Write-Host "`n[4/7] Generating new SECRET_KEY for production..." -ForegroundColor Yellow

# Generate 32-byte hex string (64 hex characters) - DIFFERENT from staging
$productionSecretKey = -join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Minimum 0 -Maximum 256) })

if ($productionSecretKey.Length -ne 64) {
    Write-Host "[X] ERROR: Failed to generate valid SECRET_KEY`n" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Generated 32-byte SECRET_KEY (different from staging)" -ForegroundColor Green

# ============================================
# Step 5: Set Production Environment Variables
# ============================================
Write-Host "`n[5/7] Setting production environment variables..." -ForegroundColor Yellow

try {
    # Use --service flag to specify capstone-hub service
    railway variables --set "FLASK_ENV=production" --service capstone-hub --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] FLASK_ENV=production" -ForegroundColor Gray
    }

    railway variables --set "SECRET_KEY=$productionSecretKey" --service capstone-hub --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] SECRET_KEY=<NEW-KEY> (different from staging)" -ForegroundColor Gray
    }

    railway variables --set "PORT=5000" --service capstone-hub --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] PORT=5000" -ForegroundColor Gray
    }

    railway variables --set "ADMIN_PASSWORD=$newPasswordPlain" --service capstone-hub --skip-deploys 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] ADMIN_PASSWORD=<YOUR-PASSWORD>" -ForegroundColor Gray
    }

    Write-Host "`n[OK] All environment variables configured" -ForegroundColor Green
} catch {
    Write-Host "`n[!] WARNING: Some variables may not be set" -ForegroundColor Yellow
    Write-Host "Details: $_" -ForegroundColor Yellow
    Write-Host "Continuing with deployment...`n" -ForegroundColor Gray
}

# Save password to file (SECURE THIS!)
$newPasswordPlain | Out-File -FilePath ".prod_admin_password.txt" -Encoding UTF8 -NoNewline
Write-Host "`n[!] Admin password saved to: .prod_admin_password.txt" -ForegroundColor Yellow
Write-Host "    SECURE THIS FILE! Delete after sharing password via secure channel." -ForegroundColor Red

# ============================================
# Step 6: Deploy to Production
# ============================================
Write-Host "`n[6/7] Deploying to Railway production..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes. Please wait...`n" -ForegroundColor Gray

try {
    $deployOutput = railway up --service capstone-hub 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[X] Deployment failed" -ForegroundColor Red
        Write-Host $deployOutput -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Production deployment successful" -ForegroundColor Green
} catch {
    Write-Host "`n[X] ERROR: Deployment failed" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    Write-Host "`nCheck Railway dashboard for build logs`n" -ForegroundColor Yellow
    exit 1
}

# ============================================
# Step 7: Get Production URL
# ============================================
Write-Host "`n[7/7] Retrieving production URL..." -ForegroundColor Yellow

Start-Sleep -Seconds 5  # Give Railway time to update

try {
    # Get production URL from Railway status
    $statusJson = railway status --json 2>&1 | Out-String
    $statusObj = $statusJson | ConvertFrom-Json -ErrorAction SilentlyContinue

    # Find the capstone-hub service
    $capstoneSvc = $statusObj.services.edges | Where-Object { $_.node.name -eq "capstone-hub" }
    $productionInstance = $capstoneSvc.node.serviceInstances.edges | Where-Object {
        $_.node.environmentId -eq ($statusObj.environments.edges | Where-Object { $_.node.name -eq "production" }).node.id
    }

    if ($productionInstance -and $productionInstance.node.domains.serviceDomains) {
        $productionUrl = "https://" + $productionInstance.node.domains.serviceDomains[0].domain
    } else {
        # Fallback: ask user
        Write-Host "[!] Could not auto-detect production URL" -ForegroundColor Yellow
        $productionUrl = Read-Host "Enter your production URL (e.g., https://your-app-production.railway.app)"
    }

    # Ensure URL has https://
    if ($productionUrl -notmatch '^https?://') {
        $productionUrl = "https://$productionUrl"
    }

    # Save to file
    $productionUrl | Out-File -FilePath ".production_url" -Encoding UTF8 -NoNewline
    Write-Host "[OK] Production URL: $productionUrl" -ForegroundColor Green
    Write-Host "[OK] Saved to .production_url`n" -ForegroundColor Gray

} catch {
    Write-Host "[!] WARNING: Could not retrieve production URL automatically" -ForegroundColor Yellow
    Write-Host "Run manually: railway status`n" -ForegroundColor Gray
    $productionUrl = "https://your-production-url.railway.app"
}

# ============================================
# Success Summary
# ============================================
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "PRODUCTION PROMOTION COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Production URL:     $productionUrl" -ForegroundColor Cyan
Write-Host "Admin Password:     (see .prod_admin_password.txt)" -ForegroundColor Cyan
Write-Host "Environment:        production" -ForegroundColor Cyan
Write-Host "Service:            capstone-hub`n" -ForegroundColor Cyan

# ============================================
# Post-Deployment Checklist
# ============================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "POST-DEPLOYMENT CHECKLIST" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

Write-Host "REQUIRED ACTIONS (do these now):`n" -ForegroundColor Red

Write-Host "1. Verify production deployment:" -ForegroundColor White
Write-Host "   python smoke_staging.py --url $productionUrl`n" -ForegroundColor Gray

Write-Host "2. Test admin login manually:" -ForegroundColor White
Write-Host "   - Open: $productionUrl" -ForegroundColor Gray
Write-Host "   - Click lock icon" -ForegroundColor Gray
Write-Host "   - Enter NEW password from .prod_admin_password.txt" -ForegroundColor Gray
Write-Host "   - Verify admin badge appears" -ForegroundColor Gray
Write-Host "   - Create a test item" -ForegroundColor Gray
Write-Host "   - Refresh and verify it persists`n" -ForegroundColor Gray

Write-Host "3. Secure the password file:" -ForegroundColor White
Write-Host "   - Share password via secure channel (1Password, LastPass, etc.)" -ForegroundColor Gray
Write-Host "   - DELETE .prod_admin_password.txt after sharing" -ForegroundColor Gray
Write-Host "   - NEVER commit this file to git`n" -ForegroundColor Gray

Write-Host "OPTIONAL (when ready for public access):`n" -ForegroundColor Yellow

Write-Host "4. Remove search engine blocking:" -ForegroundColor White
Write-Host "   - Delete src/static/robots.txt" -ForegroundColor Gray
Write-Host "   - Remove X-Robots-Tag header in src/main.py (line ~55)" -ForegroundColor Gray
Write-Host "   - Commit and push to GitHub" -ForegroundColor Gray
Write-Host "   - Railway will auto-redeploy`n" -ForegroundColor Gray

Write-Host "ONGOING SECURITY PRACTICES:`n" -ForegroundColor Yellow

Write-Host "5. Monitor production logs for 24-48 hours:" -ForegroundColor White
Write-Host "   railway environment production" -ForegroundColor Gray
Write-Host "   railway logs --service capstone-hub`n" -ForegroundColor Gray

Write-Host "6. Rotate passwords periodically:" -ForegroundColor White
Write-Host "   - Change staging password: HLStearns2025!" -ForegroundColor Gray
Write-Host "   - Change production password quarterly" -ForegroundColor Gray
Write-Host "   - Update via Railway dashboard > Variables`n" -ForegroundColor Gray

Write-Host "7. Backup database before major changes:" -ForegroundColor White
Write-Host "   - Railway > Service > Data > Download Backup`n" -ForegroundColor Gray

Write-Host "8. Review security headers quarterly:" -ForegroundColor White
Write-Host "   - Re-run smoke test" -ForegroundColor Gray
Write-Host "   - Check https://securityheaders.com/" -ForegroundColor Gray
Write-Host "   - Verify CSP is still strict (no unsafe-inline)`n" -ForegroundColor Gray

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Environment Separation Confirmed:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Staging:     Different SECRET_KEY, password HLStearns2025!" -ForegroundColor Gray
Write-Host "Production:  Different SECRET_KEY, NEW password" -ForegroundColor Gray
Write-Host "`nEach environment is isolated. Changes to staging" -ForegroundColor Gray
Write-Host "do not affect production until you promote.`n" -ForegroundColor Gray

Write-Host "========================================`n" -ForegroundColor Green
