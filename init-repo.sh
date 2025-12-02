#!/bin/bash
# Initialize Git repository for MT5 Trading Assistant

echo "🚀 Initializing MT5 Trading Assistant repository..."

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: MT5 Trading Assistant v0.3.0

🤖 AI-powered trading assistant with MCP integration
- Gradio 6 UI with multi-provider LLM support
- MCP server integration (SSE + Streamable HTTP)
- 80+ technical indicators via mt5-mcp
- Prophet forecasting + XGBoost ML signals
- Production-ready for HuggingFace Spaces deployment

🏆 Built for MCP's 1st Birthday Hackathon
"

echo "✅ Initial commit created"
echo ""
echo "📋 Next steps:"
echo "  1. Create GitHub repository: https://github.com/new"
echo "  2. Add remote: git remote add origin https://github.com/Cloudmeru/mt5-mcp-ui.git"
echo "  3. Push code: git push -u origin main"
echo ""
echo "🎉 Repository ready for publication!"
