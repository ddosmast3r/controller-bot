#\!/usr/bin/env python3
import subprocess
import json
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.env_config import BOT_TOKEN, CHAT_ID, PC_IP

def check_pc_status():
    """Check PC status and return emoji"""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', PC_IP], 
                              capture_output=True, timeout=5)
        return '🟢' if result.returncode == 0 else '🔴'
    except:
        return '❓'

def update_keyboard_silent():
    """Update keyboard without sending notification message"""
    pc_emoji = check_pc_status()
    
    keyboard = {
        "keyboard": [
            ["📊 Get Report", f"{pc_emoji} PC"],
            ["🔄 Reboot Server", "🔴 Shutdown Server"]
        ],
        "resize_keyboard": True,
        "persistent": True
    }
    
    # Just return the keyboard, don't send notification
    status_text = "Online" if pc_emoji == '🟢' else "Offline" if pc_emoji == '🔴' else "Unknown"
    print(f"PC status checked: {status_text} (no notification sent)")
    return keyboard

def send_updated_keyboard():
    """Send message with updated PC status in keyboard - DEPRECATED"""
    # This function is kept for backward compatibility but should not be used
    # Use update_keyboard_silent() instead
    print("Warning: send_updated_keyboard() is deprecated. PC status notifications are disabled.")
    return update_keyboard_silent()

if __name__ == "__main__":
    send_updated_keyboard()
