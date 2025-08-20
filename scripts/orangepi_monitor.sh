#\!/bin/bash

# Telegram Bot Configuration
BOT_TOKEN="7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ"
CHAT_ID="138754523"

# Get system information
HOSTNAME=$(hostname)
UPTIME=$(uptime -p)
LOAD=$(uptime | cut -d: -f4-)

# CPU Usage (simplified)
CPU_USAGE=$(top -bn1 | grep "^%Cpu" | awk '{printf "%.1f", 100 - $8}' || echo "N/A")
CPU_CORES=$(nproc)

# Memory and disk
MEMORY=$(free -h | awk '/^Mem:/ {printf "%.1f%% (%s/%s)", $3/$2 * 100, $3, $2}')
DISK=$(df -h / | awk 'NR==2 {printf "%s (%s free)", $5, $4}')
TEMP=$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1 | awk '{printf "%.1f°C", $1/1000}' || echo "N/A")

# Check services
NGINX_STATUS=$(systemctl is-active nginx 2>/dev/null || echo "inactive")
WEBSITE_STATUS=$(systemctl is-active odissey-website 2>/dev/null || echo "inactive")
BOT_STATUS=$(systemctl is-active orangepi-bot 2>/dev/null || echo "inactive")
WEBSITE_PORT=$(netstat -tlnp | grep :3001 | wc -l)

# Website response check
WEBSITE_RESPONSE=$(timeout 10 curl -s -o /dev/null -w "%{http_code}" http://localhost:3001 || echo "timeout")

# Get network info
LOCAL_IP=$(ip route get 8.8.8.8 2>/dev/null | awk '{print $7}' | head -1)
EXTERNAL_IP=$(timeout 10 curl -s ifconfig.me || echo "N/A")

# Security check
SUSPICIOUS=$(ps aux | grep -E '(bizy|odin|miner|crypto)' | grep -v grep | wc -l)

# Top CPU processes
TOP_PROCESSES=$(ps aux --sort=-%cpu | head -4 | tail -3 | awk '{printf "%s(%.1f%%) ", $11, $3}' | head -c 50)

# Create status icons
if [ "$NGINX_STATUS" = "active" ]; then
    NGINX_ICON="🟢"
else
    NGINX_ICON="🔴"
fi

if [ "$WEBSITE_STATUS" = "active" ] && [ "$WEBSITE_PORT" -gt 0 ] && [ "$WEBSITE_RESPONSE" = "200" ]; then
    WEBSITE_ICON="🟢"
elif [ "$WEBSITE_STATUS" = "active" ] && [ "$WEBSITE_PORT" -gt 0 ]; then
    WEBSITE_ICON="🟡"
else
    WEBSITE_ICON="🔴"
fi

if [ "$BOT_STATUS" = "active" ]; then
    BOT_ICON="🟢"
else
    BOT_ICON="🔴"
fi

if [ "$SUSPICIOUS" -gt 0 ]; then
    SECURITY_ICON="⚠️"
else
    SECURITY_ICON="🔒"
fi

# CPU Load icon
if [ "$CPU_USAGE" \!= "N/A" ]; then
    CPU_NUM=$(echo $CPU_USAGE | cut -d. -f1)
    if [ "$CPU_NUM" -gt 80 ]; then
        CPU_ICON="🔴"
    elif [ "$CPU_NUM" -gt 50 ]; then
        CPU_ICON="🟡"
    else
        CPU_ICON="🟢"
    fi
else
    CPU_ICON="⚪"
fi

# Current time
CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

# Format message
MESSAGE="🍊 *OrangePi System Report*

📊 *System Status*
🖥️ Host: \`$HOSTNAME\`
⏰ Uptime: $UPTIME
📈 Load:$LOAD

$CPU_ICON *CPU ($CPU_CORES cores)*
💻 Usage: $CPU_USAGE%
🔥 Top: $TOP_PROCESSES

🧠 *Memory & Storage*
🧠 Memory: $MEMORY
💾 Disk: $DISK
🌡️ Temperature: $TEMP

🌐 *Network*
🏠 Local IP: $LOCAL_IP
🌍 External IP: $EXTERNAL_IP

🔧 *Services Status*
$NGINX_ICON Nginx: $NGINX_STATUS
$WEBSITE_ICON Website: $WEBSITE_STATUS (Response: $WEBSITE_RESPONSE)
$BOT_ICON Bot: $BOT_STATUS

$SECURITY_ICON *Security*
Suspicious processes: $SUSPICIOUS

📅 $CURRENT_TIME"

# Create inline keyboard
KEYBOARD='{"inline_keyboard":[[{"text":"📊 Get Report","callback_data":"report"},{"text":"🔄 Reboot","callback_data":"reboot"}],[{"text":"⚡ Shutdown","callback_data":"shutdown"}]]}'

# Send message to Telegram
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d chat_id="$CHAT_ID" \
     -d text="$MESSAGE" \
     -d parse_mode="Markdown" \
     -d reply_markup="$KEYBOARD" > /dev/null 2>&1

# Log the report
echo "$CURRENT_TIME: Monitoring report sent" >> /var/log/orangepi-monitor.log

# Return success
exit 0
