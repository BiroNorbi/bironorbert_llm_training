#!/bin/bash
# Production mode with HTTPS - Uvicorn + Nginx

set -e  # Exit on error

PROJECT_DIR="/mnt/c/ai_training/bironorbert_llm_training/03_python_fastapi_project"
cd $PROJECT_DIR

echo "🚀 Starting FastAPI in production mode with HTTPS..."

# Check if SSL certificates exist
if [ ! -f "ssl/localhost.crt" ] || [ ! -f "ssl/localhost.key" ]; then
    echo "❌ SSL certificates not found!"
    echo "Run: ./scripts/generate-ssl-cert.sh"
    exit 1
fi

# Step 1: Start Uvicorn on localhost (not exposed to internet)
echo "📦 Starting Uvicorn on localhost:8000..."
uvicorn main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --proxy-headers &

UVICORN_PID=$!
echo "✅ Uvicorn started with PID: $UVICORN_PID"

# Wait a moment for Uvicorn to start
sleep 2

# Step 2: Configure Nginx with HTTPS
echo "🔒 Configuring Nginx with HTTPS..."
# sudo cp /etc/nginx/sites-available/03_python_fastapi_project /etc/nginx/sites-enabled/03_python_fastapi_project
sudo ln -sf /etc/nginx/sites-available/03_python_fastapi_project /etc/nginx/sites-enabled/03_python_fastapi_project

# Remove default site if exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    sudo systemctl restart nginx
    echo "✅ Nginx restarted successfully"
else
    echo "❌ Nginx configuration error!"
    kill $UVICORN_PID
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Production setup complete with HTTPS!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access your API at:"
echo "   HTTPS: https://localhost"
echo "   HTTP:  http://localhost (redirects to HTTPS)"
echo ""
echo "📚 API Documentation:"
echo "   Swagger UI: https://localhost/docs"
echo "   ReDoc:      https://localhost/redoc"
echo ""
echo "⚠️  Your browser will show a security warning"
echo "    because the certificate is self-signed."
echo "    Click 'Advanced' → 'Proceed to localhost'"
echo ""
echo "🛑 To stop:"
echo "   sudo systemctl stop nginx && kill $UVICORN_PID"
echo ""
echo "📊 Check logs:"
echo "   Uvicorn: ps aux | grep uvicorn"
echo "   Nginx:   sudo tail -f /var/log/nginx/error.log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
 