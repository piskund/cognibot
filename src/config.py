"""
Configuration Management for CogniBot

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Telegram settings
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_channel_id: str = Field(..., env="TELEGRAM_CHANNEL_ID")
    
    # OpenAI settings
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    
    # Bot behavior settings
    analysis_threshold: float = Field(default=0.7, env="ANALYSIS_THRESHOLD")
    max_message_length: int = Field(default=4000, env="MAX_MESSAGE_LENGTH")
    response_delay: int = Field(default=2, env="RESPONSE_DELAY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 