import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PC_MAC = os.getenv('PC_MAC')
PC_IP = os.getenv('PC_IP')

if not all([BOT_TOKEN, CHAT_ID, PC_MAC, PC_IP]):
    raise ValueError("Missing required environment variables. Check .env file.")