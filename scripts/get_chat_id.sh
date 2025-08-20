#\!/bin/bash

BOT_TOKEN="7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ"

echo "🤖 Getting your Telegram Chat ID..."
echo ""
echo "1. Open Telegram and search for your bot"
echo "2. Send any message to the bot (e.g., /start or 'hello')"
echo "3. Run this script to get your Chat ID"
echo ""
echo "Checking for recent messages..."

curl -s "https://api.telegram.org/bot$BOT_TOKEN/getUpdates" | \
jq -r '.result[] | "Chat ID: " + (.message.chat.id | tostring) + " - " + .message.from.first_name'

echo ""
echo "Copy your Chat ID and update the CHAT_ID variable in /opt/monitoring/orangepi_monitor.sh"
