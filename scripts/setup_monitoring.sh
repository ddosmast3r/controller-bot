#\!/bin/bash

echo "📱 Setting up OrangePi Telegram Monitoring"
echo ""

# Check if Chat ID is configured
if grep -q "YOUR_CHAT_ID" /opt/monitoring/orangepi_monitor.sh; then
    echo "❌ Please configure your Chat ID first:"
    echo ""
    echo "1. Run: /opt/monitoring/get_chat_id.sh"
    echo "2. Send a message to your Telegram bot"
    echo "3. Get your Chat ID from the output"
    echo "4. Edit /opt/monitoring/orangepi_monitor.sh and replace YOUR_CHAT_ID"
    echo ""
    exit 1
fi

# Setup cron job for every 2 hours
CRON_JOB="0 */2 * * * /opt/monitoring/orangepi_monitor.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "orangepi_monitor.sh"; then
    echo "✅ Monitoring cron job already exists"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Added monitoring cron job (every 2 hours)"
fi

# Create log file
touch /var/log/orangepi-monitor.log
chmod 644 /var/log/orangepi-monitor.log

echo ""
echo "🎉 Monitoring setup complete\!"
echo ""
echo "📋 What happens now:"
echo "• Reports sent every 2 hours to Telegram"
echo "• Logs saved to /var/log/orangepi-monitor.log"
echo "• Manual test: /opt/monitoring/orangepi_monitor.sh"
echo ""
echo "🔧 Useful commands:"
echo "• View cron jobs: crontab -l"
echo "• Remove monitoring: crontab -e"
echo "• View logs: tail -f /var/log/orangepi-monitor.log"
