#\!/bin/bash

echo "🧪 Testing Enhanced CPU Monitoring"
echo ""

# Test CPU monitoring components
echo "📊 CPU Information:"
echo "CPU Cores: $(nproc)"

# Get CPU usage
CPU_USAGE=$(top -bn2 -d1 | grep "^%Cpu" | tail -1 | awk '{print $2}' | sed 's/%us,//')
CPU_IDLE=$(top -bn2 -d1 | grep "^%Cpu" | tail -1 | awk '{print $8}' | sed 's/%id,//')
echo "CPU Usage: $CPU_USAGE%"
echo "CPU Idle: $CPU_IDLE%"

# Top processes
echo ""
echo "🔥 Top CPU processes:"
ps aux --sort=-%cpu | head -4 | tail -3 | awk '{printf "%s: %.1f%%\n", $11, $3}'

echo ""
echo "🌡️ Temperature: $(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1 | awk '{printf "%.1f°C", $1/1000}' || echo "N/A")"

echo ""
echo "📈 Load Average: $(uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//')"

echo ""
echo "✅ Enhanced monitoring ready\!"
echo "Click 'Get Report' button in Telegram to see detailed CPU info."
