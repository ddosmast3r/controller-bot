import json
import requests
import subprocess
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.env_config import BOT_TOKEN, CHAT_ID
LAST_UPDATE_ID = 0

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def send_message(text, keyboard=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
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

def create_main_keyboard():
    return {
        "keyboard": [
            ["📊 Get Report", "🔴 PC"],
            ["🔄 Reboot Server", "🔴 Shutdown Server"]
        ],
        "resize_keyboard": True,
        "persistent": True
    }

def handle_message(message):
    text = message.get("text", "")
    log(f"Received message: {text}")
    
    if text == "📊 Get Report":
        send_message("📊 *System Report*\n\n🟢 OrangePi Online\n🖥️ All services running\n⏰ " + time.strftime("%H:%M:%S"))
    
    elif "PC" in text:
        subprocess.run(["python3", "/opt/monitoring/pc_control.py", "wake"])
        send_message("⚡ *Wake-on-LAN sent!*\n\nMagic packet sent to your PC.")
    
    elif text == "🔄 Reboot Server":
        send_message("🔄 *Reboot Confirmation*\n\nType:  to restart OrangePi")
    
    elif text == "🔴 Shutdown Server":
        send_message("🔴 *Shutdown Confirmation*\n\nType:  to power off OrangePi")
    
    elif "confirm reboot" in text.lower():
        send_message("🔄 Rebooting OrangePi... Bot will restart automatically.")
        subprocess.run(["sudo", "reboot"])
    
    elif "confirm shutdown" in text.lower():
        send_message("🔴 Shutting down OrangePi... Goodbye!")
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    
    elif text.startswith("/start") or text.lower() in ["hi", "hello", "help", "menu"]:
        send_message(
            "🍊 *OrangePi Control Bot*\n\n" +
            "📊 *Get Report* - System status\n" +
            "🔴 *PC* - Wake up main PC\n" +
            "🔄 *Reboot Server* - Restart OrangePi\n" +
            "🔴 *Shutdown Server* - Power off OrangePi",
            create_main_keyboard()
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
