#\!/bin/bash

echo "🎯 Final Bot Test"
echo ""

echo "📋 Bot Status:"
systemctl is-active orangepi-bot && echo "✅ Bot: RUNNING" || echo "❌ Bot: STOPPED"

echo ""
echo "📡 Testing Telegram Connection:"
# Test getUpdates with callback_query support
curl -s "https://api.telegram.org/bot7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ/getUpdates?allowed_updates=%5B%22message%22,%22callback_query%22%5D&limit=1" | jq -r '.result | length'

echo ""
echo "🔄 Bot Process:"
ps aux | grep telegram_bot | grep -v grep | awk '{print "PID: " $2 ", Running for: " $9}'

echo ""
echo "📝 Recent Logs:"
journalctl -u orangepi-bot --since '2 minutes ago' --no-pager | tail -3

echo ""
echo "✅ Test the buttons in Telegram now\!"
echo "• Click '📊 Get Report' button"
echo "• You should see callback logs appear"
echo "• Report should be sent automatically"
