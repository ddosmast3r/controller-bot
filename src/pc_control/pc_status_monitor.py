import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.telegram_client import send_message, delete_message, create_main_keyboard
from src.pc_control.pc_control import get_pc_status


def update_keyboard_silently():
    """Update keyboard without sending message"""
    pc_emoji = get_pc_status()
    keyboard = create_main_keyboard(pc_emoji)
    
    # Send a minimal update message
    response = send_message(".", keyboard, parse_mode=None)
    
    # Immediately delete the message to keep chat clean
    if response and "result" in response:
        message_id = response["result"]["message_id"]
        delete_message(message_id)
    
    print(f"[{time.strftime('%H:%M:%S')}] PC: {pc_emoji} - Updated silently")
    return response is not None

if __name__ == "__main__":
    update_keyboard_silently()
