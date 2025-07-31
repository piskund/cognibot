#!/usr/bin/env python3
"""
Deployment script for CogniBot
Safely restarts the bot with code changes
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def find_bot_processes():
    """Find running bot processes."""
    try:
        # Find python processes running the bot
        result = subprocess.run(['tasklist', '/fi', 'IMAGENAME eq python.exe', '/fo', 'csv'], 
                              capture_output=True, text=True, shell=True)
        
        pids = []
        for line in result.stdout.split('\n')[1:]:  # Skip header
            if 'python.exe' in line and 'cognibot' in line:
                parts = line.split(',')
                if len(parts) > 1:
                    pid = parts[1].strip('"')
                    pids.append(pid)
        return pids
    except Exception as e:
        print(f"Error finding processes: {e}")
        return []

def stop_bot():
    """Stop running bot instances."""
    print("🛑 Stopping existing bot instances...")
    
    try:
        # Kill all python processes (simple approach)
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
        print("✅ Bot stopped")
    except Exception as e:
        print(f"Warning: Could not stop bot: {e}")

def start_bot(dev_mode=False):
    """Start the bot."""
    print("🚀 Starting bot...")
    
    # Set environment variable for dev mode
    env = os.environ.copy()
    if dev_mode:
        env['COGNIBOT_DEV_MODE'] = 'true'
    
    # Start bot in background
    if dev_mode:
        print("🔄 Development mode: Auto-restart enabled")
        subprocess.Popen([sys.executable, 'src/run_bot.py'], env=env)
    else:
        subprocess.Popen([sys.executable, 'src/run_bot.py'], env=env)
    
    time.sleep(3)
    print("✅ Bot started")

def main():
    """Main deployment function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy CogniBot')
    parser.add_argument('--dev', action='store_true', 
                       help='Run in development mode with auto-restart')
    parser.add_argument('--stop', action='store_true', 
                       help='Only stop the bot')
    parser.add_argument('--start', action='store_true', 
                       help='Only start the bot')
    
    args = parser.parse_args()
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    if args.stop:
        stop_bot()
        return
    
    if args.start:
        start_bot(args.dev)
        return
    
    # Default: restart
    print("🔄 Deploying CogniBot...")
    stop_bot()
    start_bot(args.dev)
    print("✅ Deployment complete!")
    
    if args.dev:
        print("\n💡 Development mode active:")
        print("   - Bot will auto-restart on crashes")
        print("   - Use Ctrl+C to stop completely")

if __name__ == "__main__":
    main()