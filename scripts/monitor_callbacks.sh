#\!/bin/bash

echo "👀 Monitoring Bot Callbacks (Press Ctrl+C to stop)"
echo ""
echo "📱 Now click buttons in Telegram..."
echo ""

# Monitor logs in real time
journalctl -u orangepi-bot -f --since now
