# Product Management Application - Start Script
# This script starts the Angular development server

Write-Host "🚀 Starting Product Management Application..." -ForegroundColor Cyan
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path ".\product-management-app\node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    Set-Location .\product-management-app
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Set-Location ..
}

# Check if backend is running
Write-Host "🔍 Checking backend connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost/products" -Method GET -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Backend is running!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Backend may not be running at http://localhost" -ForegroundColor Yellow
    Write-Host "   Please start the FastAPI backend first:" -ForegroundColor Yellow
    Write-Host "   cd ..\03_python_fastapi_project" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "🌐 Starting Angular development server..." -ForegroundColor Cyan
Write-Host "   The application will open at http://localhost:4200" -ForegroundColor Gray
Write-Host ""

Set-Location .\product-management-app
npm start
