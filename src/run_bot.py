#!/usr/bin/env python3
"""
Launcher script for CogniBot.
Checks configuration and dependencies before starting the bot.

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "telegram", "openai", "python-dotenv", 
        "pydantic", "rich", "loguru", "aiohttp"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_configuration():
    """Check if configuration is properly set."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("Copy env_template.txt to .env and fill in your credentials")
        return False
    
    # Load and check required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY", "TELEGRAM_CHANNEL_ID"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var).startswith("your_"):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing configuration: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    
    print("✅ Configuration looks good")
    return True

def main():
    """Main launcher function."""
    print("🚀 CogniBot Launcher")
    print("=" * 50)
    
    # Run checks
    checks = [
        check_python_version(),
        check_dependencies(),
        check_configuration()
    ]
    
    if not all(checks):
        print("\n❌ Pre-flight checks failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting CogniBot...")
    print("=" * 50)
    
    # Import and run the bot
    try:
        from cognibot import main as bot_main
        import asyncio
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 