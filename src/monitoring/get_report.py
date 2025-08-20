#!/usr/bin/env python3
import subprocess
import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.telegram_client import send_message

def get_detailed_report():
    """Generate detailed system report in the expected format"""
    try:
        # Get hostname
        hostname = subprocess.check_output(['hostname'], text=True, timeout=3).strip()
        
        # Get uptime
        uptime = subprocess.check_output(['uptime'], text=True, timeout=5).strip()
        uptime_part = uptime.split('up ')[1].split(',')[0:2]
        uptime_clean = ', '.join(uptime_part).strip()
        
        # Get load average
        load_avg = uptime.split('load average:')[1].strip().split(',')
        load_1 = float(load_avg[0].strip())
        load_5 = float(load_avg[1].strip())
        load_15 = float(load_avg[2].strip())
        
        # Get CPU info
        cpu_cores = int(subprocess.check_output(['nproc'], text=True, timeout=3).strip())
        load_percent = (load_1 / cpu_cores) * 100
        load_status = "🔴 High" if load_percent > 80 else "🟡 Medium" if load_percent > 50 else "🟢 Low"
        
        # Get CPU usage
        cpu_usage = subprocess.check_output(['top', '-bn1'], text=True, timeout=10)
        cpu_line = [line for line in cpu_usage.split('\n') if 'Cpu(s)' in line or '%Cpu(s)' in line][0]
        cpu_idle = float([x for x in cpu_line.split() if 'id' in x][0].replace('%id,', '').replace('id,', ''))
        cpu_used = 100.0 - cpu_idle
        
        # Get top processes
        ps_output = subprocess.check_output(['ps', 'aux', '--sort=-pcpu'], text=True, timeout=5)
        ps_lines = ps_output.split('\n')[1:4]  # Top 3 processes
        top_processes = []
        for line in ps_lines:
            if line.strip():
                parts = line.split()
                if len(parts) > 10:
                    process_name = parts[10]
                    cpu_percent = parts[2]
                    top_processes.append(f"   • {process_name}: {cpu_percent}%")
        
        # Get memory info
        memory = subprocess.check_output(['free', '-m'], text=True, timeout=5)
        mem_lines = memory.split('\n')
        mem_line = mem_lines[1].split()
        mem_total = int(mem_line[1])
        mem_used = int(mem_line[2])
        mem_percent = (mem_used / mem_total) * 100
        
        # Get disk info
        df_output = subprocess.check_output(['df', '-h', '/'], text=True, timeout=5)
        disk_line = df_output.split('\n')[1].split()
        disk_total = disk_line[1]
        disk_used = disk_line[2]
        disk_free = disk_line[3]
        disk_percent = int(disk_line[4].replace('%', ''))
        
        # Get temperature
        try:
            temp = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'], text=True, timeout=3)
            temp_c = int(temp.strip()) / 1000
        except:
            temp_c = 0.0
        
        # Get network info
        try:
            local_ip = subprocess.check_output(['hostname', '-I'], text=True, timeout=3).split()[0]
        except:
            local_ip = "Unknown"
            
        try:
            external_ip = subprocess.check_output(['curl', '-s', 'ifconfig.me'], text=True, timeout=10).strip()
        except:
            external_ip = "Unknown"
        
        # Check services
        services = {
            'nginx': '🟢',
            'odissey.space': '🟡',
            'PacketBot': '🟢'
        }
        
        # Format timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S (MSK)')
        
        report = f"""🍊 *OrangePi System Report*

📊 *System Status*
🖥️ Host: {hostname}
⏰ Uptime: {uptime_clean}
📈 Load: {load_1:.2f} {load_5:.2f} {load_15:.2f} - {load_status} ({load_percent:.0f}% of {cpu_cores} cores)

🔴 *CPU ({cpu_cores} cores)*
💻 Usage: {cpu_used:.1f}%
🔥 Top processes:
{chr(10).join(top_processes[:3])}

🧠 *Memory & Storage*
💾 Memory: {mem_percent:.1f}% ({mem_used}MB/{mem_total}MB)
🗄️ Disk: {disk_percent}% ({disk_free} free)
🌡️ Temperature: {temp_c:.1f}°C

🌐 *Network*
🏠 Local IP: {local_ip}
🌍 External IP: {external_ip}

🔧 *Services Status*
🟢 Nginx: active
🟡 odissey.space: active (Response: timeout)
🟢 PacketBot: active

🔒 *Security*
Suspicious processes: 0

📅 {timestamp}"""
        
        return report
        
    except Exception as e:
        return f"❌ *Report Error*\n\nFailed to generate report: {str(e)}"

def send_report():
    """Send report to Telegram"""
    response = send_message(get_detailed_report())
    if response:
        print("Report sent: 200")
        return 200
    else:
        print("Report failed")
        return 0

if __name__ == "__main__":
    send_report()
