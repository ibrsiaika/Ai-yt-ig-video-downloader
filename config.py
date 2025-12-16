"""
Configuration settings for the Telegram Bot
Bot के लिए configuration settings

This file contains all constants and configuration used by the bot.
यह file bot द्वारा use की जाने वाली सभी constants और configuration contain करती है।
"""

import os
from dotenv import load_dotenv

# Load environment variables / Environment variables load करें
load_dotenv()

# Telegram Bot Configuration / Telegram Bot की Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# File size limits (in bytes) / File size की limits (bytes में)
MAX_TELEGRAM_FILE_SIZE = 50 * 1024 * 1024  # 50MB - Telegram's limit for bots
MAX_DOWNLOAD_SIZE = 500 * 1024 * 1024  # 500MB - Maximum file size to attempt downloading

# Download settings / Download की settings
DOWNLOAD_TIMEOUT = 300  # 5 minutes timeout for downloads / downloads के लिए 5 minute का timeout
TEMP_DOWNLOAD_DIR = 'downloads'  # Temporary directory for downloads / downloads के लिए temporary directory

# YouTube settings / YouTube की settings
YOUTUBE_VIDEO_FORMAT = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
YOUTUBE_AUDIO_FORMAT = 'bestaudio[ext=m4a]/bestaudio'

# Instagram settings / Instagram की settings
INSTAGRAM_SESSION_FILE = None  # Set if you want to use a session file for private posts

# Logging settings / Logging की settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Create temp directory if it doesn't exist / Temp directory बनाएं अगर exist नहीं करती
os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)
