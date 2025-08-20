#\!/bin/bash

echo "🔍 Bot Debug Information"
echo ""

echo "📋 Service Status:"
systemctl is-active orangepi-bot && echo "✅ Bot service: ACTIVE" || echo "❌ Bot service: INACTIVE"

echo ""
echo "🔄 Process Info:"
ps aux | grep telegram_bot | grep -v grep | awk '{print "PID: " $2 ", CPU: " $3 "%, Memory: " $4 "%"}'

echo ""
echo "📝 Recent Bot Activity (last 10 lines):"
journalctl -u orangepi-bot --since '5 minutes ago' --no-pager | tail -10

echo ""
echo "🌐 Network Test:"
curl -s --max-time 5 "https://api.telegram.org/bot7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ/getMe" | jq .

echo ""
echo "✅ If buttons don't work, try:"
echo "• Click 'Test Report' button in Telegram"
echo "• Check if you get callback response"
echo "• Bot should respond within 2-3 seconds"
