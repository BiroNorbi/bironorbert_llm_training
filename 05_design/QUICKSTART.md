# Product Management Application - Quick Start Guide

## 🚀 Quick Start

### Option 1: PowerShell Script (Recommended)
```powershell
.\start-app.ps1
```

### Option 2: Manual Start

1. **Start Backend** (in terminal 1):
```powershell
cd ..\03_python_fastapi_project
# Make sure nginx is configured and running
# Or start the FastAPI server directly
```

2. **Start Frontend** (in terminal 2):
```powershell
cd product-management-app
npm start
```

3. Open your browser to `http://localhost:4200`

## 📋 Pre-flight Checklist

- [ ] Node.js installed (v18+)
- [ ] Angular CLI installed globally
- [ ] Dependencies installed (`npm install`)
- [ ] FastAPI backend running on `http://localhost`
- [ ] Nginx configured (if using reverse proxy)

## 🎯 First Time Setup

```powershell
# Install dependencies
npm install

# Verify Angular CLI is installed
ng version

# Start the app
npm start
```

## 🔧 Troubleshooting

### Backend Connection Issues
- Ensure FastAPI is running on `http://localhost`
- Check nginx configuration in `03_python_fastapi_project`
- Verify CORS settings are properly configured

### Port Already in Use
```powershell
# Use a different port
ng serve --port 4300
```

### Module Not Found Errors
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install
```

## 📝 API Testing

You can test the backend API using the Bruno collection in `AITraning-FastAPI/` folder.

## 🎨 Features Overview

### Product List (`/products`)
- View all products in a grid
- Search and filter
- Quick edit/delete actions
- Click to view details

### Product Detail (`/products/:id`)
- Full product information
- Stock status visualization
- Inventory value calculation
- Edit/Delete options

### Create/Edit Product (`/products/new`, `/products/edit/:id`)
- Form validation
- Real-time error feedback
- Stock management
- Price formatting

## 🛠️ Development

```powershell
# Development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Watch mode
npm run watch
```

## 📦 Project Info

- **Framework**: Angular 20.3
- **Language**: TypeScript 5.9
- **Styling**: SCSS
- **State Management**: Signals
- **HTTP Client**: HttpClient with Fetch API
- **Change Detection**: Zoneless
