# Force Railway redeploy
cd "C:\Users\HP\OneDrive\Desktop\voice ai agent\frontend"

# Option 1: Try using Railway CLI
Write-Host "Attempting Railway redeploy..."
railway redeploy --service voice-ai-frontend --yes 2>$null

# Option 2: If that fails, push an empty commit
if ($LASTEXITCODE -ne 0) {
    Write-Host "Railway CLI failed, using git push method..."
    cd ..
    git commit --allow-empty -m "chore: force redeploy $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main
    Write-Host "Empty commit pushed. Railway should auto-deploy in 1-2 minutes."
}
