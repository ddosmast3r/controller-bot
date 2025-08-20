#\!/usr/bin/env python3
import subprocess
import time

def test_cpu_methods():
    print("🧪 Testing CPU monitoring methods")
    
    # Method 1: /proc/stat
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        cpu_times = [int(x) for x in line.split()[1:]]
        idle_time = cpu_times[3]
        total_time = sum(cpu_times)
        
        time.sleep(1)
        
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        cpu_times2 = [int(x) for x in line.split()[1:]]
        idle_time2 = cpu_times2[3]
        total_time2 = sum(cpu_times2)
        
        idle_delta = idle_time2 - idle_time
        total_delta = total_time2 - total_time
        
        if total_delta > 0:
            cpu_usage = 100.0 * (1.0 - idle_delta / total_delta)
            print(f"✅ /proc/stat method: {cpu_usage:.1f}%")
        else:
            print("❌ /proc/stat method failed")
    except Exception as e:
        print(f"❌ /proc/stat method error: {e}")
    
    # Method 2: ps command
    try:
        result = subprocess.check_output(['ps', 'aux'], text=True)
        lines = result.strip().split('\n')[1:4]  # Top 3 processes
        processes = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                cpu_pct = parts[2]
                cmd = parts[10].split('/')[-1]
                processes.append(f"{cmd}({cpu_pct}%)")
        print(f"✅ Top processes: {' '.join(processes)}")
    except Exception as e:
        print(f"❌ ps command error: {e}")

if __name__ == "__main__":
    test_cpu_methods()
