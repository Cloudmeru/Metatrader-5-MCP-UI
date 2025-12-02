# Initialize Git repository for MT5 Trading Assistant
# Run this script: .\init-repo.ps1

Write-Host "🚀 Initializing MT5 Trading Assistant repository..." -ForegroundColor Cyan
Write-Host ""

# Initialize git if not already initialized
if (-not (Test-Path .git)) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already initialized" -ForegroundColor Yellow
}

# Add all files
Write-Host "📦 Adding files..." -ForegroundColor Cyan
git add .

# Initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Cyan
git commit -m @"
Initial commit: MT5 Trading Assistant v0.3.0

🤖 AI-powered trading assistant with MCP integration
- Gradio 6 UI with multi-provider LLM support
- MCP server integration (SSE + Streamable HTTP)
- 80+ technical indicators via mt5-mcp
- Prophet forecasting + XGBoost ML signals
- Production-ready for HuggingFace Spaces deployment

🏆 Built for MCP's 1st Birthday Hackathon
"@

Write-Host ""
Write-Host "✅ Initial commit created" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Create GitHub repository: https://github.com/new" -ForegroundColor White
Write-Host "  2. Add remote: git remote add origin https://github.com/Cloudmeru/mt5-mcp-ui.git" -ForegroundColor White
Write-Host "  3. Push code: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Repository ready for publication!" -ForegroundColor Green
