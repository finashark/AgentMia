"""
Configuration file for API keys and settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

# HeyGen API Configuration
HEYGEN_BASE_URL = "https://api.heygen.com"
HEYGEN_HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
}

# Google Gemini Configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"

# File Configuration
SCRIPT_FOLDER = "Script Folder"
SUPPORTED_FILE_FORMATS = [".docx", ".txt"]

# Video Configuration
VIDEO_POLL_INTERVAL = 10  # seconds
