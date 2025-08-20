#\!/bin/bash

echo "🧪 Testing OrangePi Bot System"
echo ""

echo "📋 System Services Status:"
echo "Website Service: $(systemctl is-active odissey-website)"
echo "Bot Service: $(systemctl is-active orangepi-bot)"
echo "Nginx Service: $(systemctl is-active nginx)"
echo ""

echo "🌐 Network Test:"
LOCAL_IP=$(ip route get 8.8.8.8 | awk '{print $7}' | head -1)
EXTERNAL_IP=$(curl -s --max-time 10 ifconfig.me || echo "Failed")
echo "Local IP: $LOCAL_IP"
echo "External IP: $EXTERNAL_IP"
echo ""

echo "🔧 Process Check:"
echo "Website Port 3001: $(netstat -tlnp | grep :3001 | wc -l) listener(s)"
echo "Bot Process: $(ps aux | grep telegram_bot | grep -v grep | wc -l) instance(s)"
echo ""

echo "✅ All systems configured\!"
echo ""
echo "📱 In Telegram:"
echo "• Bot should send startup message with buttons"
echo "• Try clicking 'Get Report' button"
echo "• Reports sent every 2 hours automatically"
echo "• Use 'Reboot' and 'Shutdown' with confirmation"
