"""
Configuration Management
إدارة الإعدادات والمتغيرات البيئية
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# API Keys and Credentials
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE", "")

# Google Drive
GOOGLE_DRIVE_CREDENTIALS = os.getenv("GOOGLE_DRIVE_CREDENTIALS", "")

# Language Settings
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ar")  # ar, en, ru
SUPPORTED_LANGUAGES = ["ar", "en", "ru"]

# Storage Paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
LOCAL_DB_DIR = os.path.join(DATA_DIR, "db")

# Telegram Channels
TELEGRAM_CHANNELS = {
    "images": os.getenv("TELEGRAM_IMAGES_CHANNEL", ""),
    "audio": os.getenv("TELEGRAM_AUDIO_CHANNEL", ""),
    "videos": os.getenv("TELEGRAM_VIDEOS_CHANNEL", ""),
    "system_logs": os.getenv("TELEGRAM_LOGS_CHANNEL", ""),
    "knowledge": os.getenv("TELEGRAM_KNOWLEDGE_CHANNEL", ""),
}

# System Settings
SYSTEM_NAME = "Honda"
OWNER_PHONE = "+201068309448"
AUTO_BACKUP_INTERVAL = 3600  # 1 hour in seconds
MAX_CACHE_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB

# Create necessary directories
for directory in [DATA_DIR, LOGS_DIR, CACHE_DIR, LOCAL_DB_DIR]:
    os.makedirs(directory, exist_ok=True)
