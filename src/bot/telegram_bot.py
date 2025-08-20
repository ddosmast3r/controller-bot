import json
import requests
import subprocess
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.env_config import BOT_TOKEN, CHAT_ID
from src.utils.telegram_client import send_message, log, create_main_keyboard
from src.pc_control.pc_control import get_pc_status
LAST_UPDATE_ID = 0

def handle_message(message):
    text = message.get("text", "")
    log(f"Received message: {text}")
    
    if text == "📊 Get Report":
        send_message(f"📊 *System Report*\n\n🟢 OrangePi Online\n🖥️ All services running\n⏰ {time.strftime('%H:%M:%S')}")
    
    elif "PC" in text:
        pc_control_path = os.path.join(os.path.dirname(__file__), '..', 'pc_control', 'pc_control.py')
        subprocess.run(["python3", pc_control_path, "wake"])
        send_message("⚡ *Wake-on-LAN sent!*\n\nMagic packet sent to your PC.")
    
    elif text == "🔄 Reboot Server":
        send_message("🔄 *Reboot Confirmation*\n\nType: `confirm reboot` to restart OrangePi")
    
    elif text == "💀 Shutdown Server":
        send_message("🔴 *Shutdown Confirmation*\n\nType: `confirm shutdown` to power off OrangePi")
    
    elif "confirm reboot" in text.lower():
        send_message("🔄 Rebooting OrangePi... Bot will restart automatically.")
        subprocess.run(["sudo", "reboot"])
    
    elif "confirm shutdown" in text.lower():
        send_message("🔴 Shutting down OrangePi... Goodbye!")
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    
    elif text.startswith("/start") or text.lower() in ["hi", "hello", "help", "menu"]:
        pc_status = get_pc_status()
        send_message(
            "🍊 *OrangePi Control Bot*\n\n"
            "📊 *Get Report* - System status\n"
            f"{pc_status} *PC* - Wake up main PC\n"
            "🔄 *Reboot Server* - Restart OrangePi\n"
            "💀 *Shutdown Server* - Power off OrangePi",
            create_main_keyboard(pc_status)
        )

def get_updates():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "offset": LAST_UPDATE_ID + 1, 
        "timeout": 30,
        "allowed_updates": ["message"]
    }
    
    try:
        response = requests.get(url, params=params, timeout=35)
        data = response.json()
        
        if data.get("ok"):
            updates = data.get("result", [])
            if updates:
                log(f"Received {len(updates)} updates")
                
            for update in updates:
                LAST_UPDATE_ID = update["update_id"]
                
                if "message" in update:
                    message = update["message"]
                    if str(message["chat"]["id"]) == CHAT_ID:
                        handle_message(message)
        else:
            log(f"Error from Telegram API: {data}")
            
    except requests.exceptions.Timeout:
        pass
    except Exception as e:
        log(f"Error getting updates: {e}")
        time.sleep(5)

def main():
    log("🍊 OrangePi Control Bot started")
    
    while True:
        try:
            get_updates()
        except KeyboardInterrupt:
            log("🛑 Bot stopped by user")
            break
        except Exception as e:
            log(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
