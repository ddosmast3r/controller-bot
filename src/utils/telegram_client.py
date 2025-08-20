#!/usr/bin/env python3
import json
import requests
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.env_config import BOT_TOKEN, CHAT_ID

def log(message):
    """Log message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def send_message(text, keyboard=None, parse_mode="Markdown"):
    """Send message to Telegram chat"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, data=data, timeout=10)
        log(f"Message sent: {response.status_code}")
        return response.json()
    except Exception as e:
        log(f"Error sending message: {e}")
        return None

def delete_message(message_id):
    """Delete message from Telegram chat"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    data = {
        "chat_id": CHAT_ID,
        "message_id": message_id
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        log(f"Error deleting message: {e}")
        return False

def create_main_keyboard(pc_status="🔴"):
    """Create main keyboard with PC status"""
    return {
        "keyboard": [
            ["📊 Get Report", f"{pc_status} PC"],
            ["🔄 Reboot Server", "💀 Shutdown Server"]
        ],
        "resize_keyboard": True,
        "persistent": True
    }