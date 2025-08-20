#\!/usr/bin/env python3
import subprocess
import json
import requests
import time

BOT_TOKEN = "7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ"
CHAT_ID = "138754523"

def check_pc_status():
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', '192.168.0.100'], 
                              capture_output=True, timeout=5)
        return '🟢' if result.returncode == 0 else '🔴'
    except:
        return '❓'

def update_keyboard_silently():
    """Update keyboard without sending message"""
    pc_emoji = check_pc_status()
    keyboard = {
        "keyboard": [
            ["📊 Get Report", f"{pc_emoji} PC"],
            ["🔄 Reboot Server", "🔴 Shutdown Server"]
        ],
        "resize_keyboard": True,
        "persistent": True
    }
    
    # Send a minimal update message
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": ".",  # Minimal message
        "reply_markup": json.dumps(keyboard)
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        # Immediately delete the message to keep chat clean
        if response.status_code == 200:
            message_data = response.json()
            if "result" in message_data:
                message_id = message_data["result"]["message_id"]
                delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
                delete_data = {"chat_id": CHAT_ID, "message_id": message_id}
                requests.post(delete_url, data=delete_data, timeout=5)
        
        print(f"[{time.strftime('%H:%M:%S')}] PC: {pc_emoji} - Updated silently")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    update_keyboard_silently()
