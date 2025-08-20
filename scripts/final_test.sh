#\!/bin/bash

echo "✅ FINAL SYSTEM TEST"
echo ""

echo "📋 All Services Status:"
echo "• Website: $(systemctl is-active odissey-website) ($(netstat -tlnp | grep :3001 | wc -l) listeners)"
echo "• Nginx: $(systemctl is-active nginx)"
echo "• Bot: $(systemctl is-active orangepi-bot)"
echo ""

echo "🧪 Monitoring Script Test:"
echo "Running monitoring script..."
/opt/monitoring/orangepi_monitor.sh
if [ $? -eq 0 ]; then
    echo "✅ Monitoring script: SUCCESS"
else
    echo "❌ Monitoring script: FAILED"
fi
echo ""

echo "🔗 Network Test:"
LOCAL_IP=$(ip route get 8.8.8.8 2>/dev/null | awk '{print $7}' | head -1)
EXTERNAL_IP=$(timeout 5 curl -s ifconfig.me || echo "N/A")
echo "• Local IP: $LOCAL_IP"
echo "• External IP: $EXTERNAL_IP"
echo ""

echo "💻 CPU Info:"
echo "• Cores: $(nproc)"
echo "• Usage: $(top -bn1 | grep '^%Cpu' | awk '{printf "%.1f%%", 100 - $8}' || echo "N/A")"
echo "• Temperature: $(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1 | awk '{printf "%.1f°C", $1/1000}' || echo "N/A")"
echo ""

echo "📱 Bot Status:"
echo "• Process: $(ps aux | grep telegram_bot | grep -v grep | wc -l) running"
echo "• Recent activity: $(journalctl -u orangepi-bot --since '1 minute ago' --no-pager | wc -l) log entries"
echo ""

echo "🎯 READY FOR TESTING\!"
echo ""
echo "📲 In Telegram:"
echo "1. You should see: 'OrangePi Bot Online (FULLY FIXED)'"
echo "2. Click '📊 Get Report' button"
echo "3. You should get detailed system report"
echo "4. Then see: '✅ System report sent\!'"
echo ""
echo "🔧 If issues persist, check logs:"
echo "   journalctl -u orangepi-bot -f"
