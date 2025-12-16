#!/usr/bin/env python3
"""
Setup verification script
Setup verify करने के लिए script

This script checks if your environment is properly set up to run the bot.
यह script check करती है कि आपका environment bot चलाने के लिए properly set up है या नहीं।
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    print("\n🎬 Checking ffmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            # Get first line which contains version
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {version_line}")
            return True
    except FileNotFoundError:
        print("   ❌ ffmpeg not found")
        print("   💡 Install: sudo apt install ffmpeg (Linux)")
        print("   💡 Install: brew install ffmpeg (macOS)")
        return False
    except Exception as e:
        print(f"   ❌ Error checking ffmpeg: {e}")
        return False
    return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔐 Checking environment file...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ❌ .env file not found")
        print("   💡 Copy .env.example to .env and add your token")
        return False
    
    print("   ✅ .env file exists")
    
    # Check if token is set
    with open(env_path, 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN=' in content:
            if 'your_telegram_bot_token_here' in content or 'your_token_here' in content:
                print("   ⚠️  .env file exists but token not set")
                print("   💡 Add your actual bot token from @BotFather")
                return False
            else:
                print("   ✅ Token appears to be set")
                return True
        else:
            print("   ❌ TELEGRAM_BOT_TOKEN not found in .env")
            return False

def check_required_files():
    """Check if all required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'main.py',
        'config.py',
        'utils.py',
        'youtube_handler.py',
        'instagram_handler.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - Missing!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if Python dependencies are installed"""
    print("\n📦 Checking Python dependencies...")
    
    required_packages = {
        'telegram': 'python-telegram-bot',
        'yt_dlp': 'yt-dlp',
        'instaloader': 'instaloader',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
    }
    
    all_installed = True
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   💡 Install dependencies: pip install -r requirements.txt")
    
    return all_installed

def check_downloads_directory():
    """Check if downloads directory will be created"""
    print("\n📂 Checking downloads directory...")
    
    downloads_dir = Path('downloads')
    if downloads_dir.exists():
        print(f"   ✅ downloads/ directory exists")
    else:
        print(f"   ℹ️  downloads/ will be created automatically")
    
    return True

def main():
    """Main verification function"""
    print_header("🤖 Telegram Bot Setup Verification")
    print("Checking if your environment is ready to run the bot...")
    print("Bot चलाने के लिए आपका environment ready है या नहीं check कर रहे हैं...")
    
    results = {}
    
    # Run all checks
    results['Python Version'] = check_python_version()
    results['ffmpeg'] = check_ffmpeg()
    results['Environment File'] = check_env_file()
    results['Required Files'] = check_required_files()
    results['Python Dependencies'] = check_dependencies()
    results['Downloads Directory'] = check_downloads_directory()
    
    # Summary
    print_header("📊 Verification Summary")
    
    all_passed = True
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("\n🎉 Great! Everything is set up correctly!")
        print("🚀 You can now run the bot with: python main.py")
        print("\n🎉 बढ़िया! सब कुछ सही से set up है!")
        print("🚀 अब bot को चलाएं: python main.py")
        return 0
    else:
        print("\n⚠️  Some issues found. Please fix them before running the bot.")
        print("⚠️  कुछ issues मिले हैं। Bot चलाने से पहले उन्हें fix करें।")
        return 1

if __name__ == '__main__':
    sys.exit(main())
