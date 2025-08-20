#\!/usr/bin/env python3
import requests
import json
import time

BOT_TOKEN = "7964664704:AAFFik_PyRFt1OogdZ7n0bzl8NZ1jv2KpIQ"
CHAT_ID = "138754523"

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🧪 Test Report", "callback_data": "report"},
             {"text": "🔄 Test Reboot", "callback_data": "reboot"}],
            [{"text": "⚡ Test Shutdown", "callback_data": "shutdown"}]
        ]
    }
    
    data = {
        "chat_id": CHAT_ID,
        "text": "🧪 *Button Test Message*\n\nClick any button to test functionality:\n\n📊 **Enhanced CPU Monitoring Now Available:**\n• 4 CPU cores monitored\n• Real-time usage: 0.9%\n• Temperature: 67.5°C\n• Top processes tracked\n\nButtons should work now!",
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    response = requests.post(url, data=data)
    print(f"Test message sent: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    send_test_message()
