#!/usr/bin/env python3
import subprocess
import sys
import os
from wakeonlan import send_magic_packet

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.env_config import PC_MAC, PC_IP

def check_pc():
    """Check PC status with detailed output"""
    status = get_pc_status()
    if status == '🟢':
        print('🟢 Online')
    elif status == '🔴':
        print('🔴 Offline')
    else:
        print('❓ Unknown')

def get_pc_status():
    """Get PC status as emoji - for use by other modules"""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', PC_IP], 
                              capture_output=True, timeout=5)
        return '🟢' if result.returncode == 0 else '🔴'
    except subprocess.TimeoutExpired:
        return '❓'
    except Exception:
        return '❓'

def wake_pc():
    try:
        send_magic_packet(PC_MAC)
        print(f'⚡ Wake-on-LAN sent to {PC_MAC}')
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'status':
            check_pc()
        elif sys.argv[1] == 'wake':
            wake_pc()
    else:
        print('Usage: python3 pc_control.py [status|wake]')
