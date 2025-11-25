"""
Configuration file for API keys and settings
"""
import os

# Try to load from Streamlit secrets first (for Streamlit Cloud)
# Fall back to environment variables (for local development)
try:
    import streamlit as st
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    HEYGEN_API_KEY = st.secrets.get("HEYGEN_API_KEY", os.getenv("HEYGEN_API_KEY"))
except Exception:
    # Fallback to dotenv for local development
    from dotenv import load_dotenv
    load_dotenv()
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
