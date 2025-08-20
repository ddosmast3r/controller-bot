#\!/bin/bash

echo "📊 What CPU line SHOULD show:"
echo ""

# Get CPU cores
CORES=$(nproc)
echo "🔢 CPU Cores: $CORES"

# Test CPU usage calculation
echo "💻 Testing CPU usage methods:"

# Method 1: Using top
CPU_TOP=$(top -bn1 | grep Cpu | head -1 | awk '{print 100 - $8}' 2>/dev/null || echo "Failed")
echo "   Method 1 (top): $CPU_TOP%"

# Method 2: Using vmstat
CPU_VMSTAT=$(vmstat 1 2 | tail -1 | awk '{print 100 - $15}' 2>/dev/null || echo "Failed")
echo "   Method 2 (vmstat): $CPU_VMSTAT%"

# Test top processes
echo ""
echo "🔥 Top CPU processes:"
ps aux --sort=-%cpu | head -4 | tail -3 | awk '{printf "   %s: %.1f%%\n", $11, $3}'

echo ""
echo "✅ EXPECTED CPU LINE:"
echo "🟢 CPU (4 cores)"
echo "💻 Usage: 5.2%"
echo "🔥 Top: node(8.1%) systemd(2.3%) sshd(1.8%)"
echo ""
echo "❌ CURRENT PROBLEM: Shows N/A instead of real values"
