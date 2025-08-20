#!/usr/bin/env python3
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.telegram_client import send_message

def send_test_message():
    keyboard = {
        "inline_keyboard": [
            [{"text": "🧪 Test Report", "callback_data": "report"},
             {"text": "🔄 Test Reboot", "callback_data": "reboot"}],
            [{"text": "⚡ Test Shutdown", "callback_data": "shutdown"}]
        ]
    }
    
    text = (
        "🧪 *Button Test Message*\n\n"
        "Click any button to test functionality:\n\n"
        "📊 **Enhanced CPU Monitoring Now Available:**\n"
        "• 4 CPU cores monitored\n"
        "• Real-time usage: 0.9%\n"
        "• Temperature: 67.5°C\n"
        "• Top processes tracked\n\n"
        "Buttons should work now!"
    )
    
    response = send_message(text, keyboard)
    if response:
        print(f"Test message sent: 200")
        print(f"Response: {response}")
    else:
        print("Failed to send test message")

if __name__ == "__main__":
    send_test_message()
