import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    CHAT_MODEL = "mistral-tiny"  # You can change this to other models like "mistral-small" or "mistral-medium" 