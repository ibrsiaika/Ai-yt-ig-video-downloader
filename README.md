# 🎬 AI YouTube & Instagram Video Downloader Bot

A powerful Telegram bot that downloads videos and audio from YouTube and Instagram with high quality and user-friendly interface.

Ek powerful Telegram bot jo YouTube aur Instagram se videos aur audio high quality mein download karta hai.

## ✨ Features / विशेषताएं

### YouTube Support
- 🎥 Download videos in MP4 format (high quality)
- 🎵 Download audio in MP3 format
- ⚡ Quality selection via inline buttons
- 🚀 Fast downloads using yt-dlp

### Instagram Support
- 📸 Download videos, reels, and stories
- 🎭 Support for carousels
- 🔓 Works with public posts
- 💫 Handles private accounts gracefully

### Bot Features
- 🤖 Easy-to-use interface
- 📊 Progress/status messages
- 🛡️ Comprehensive error handling
- 🧹 Automatic cleanup of temporary files
- 📝 Bilingual support (Hindi/English)
- 🔒 Secure token management

## 🚀 Quick Start / शुरू करें

### Prerequisites / पूर्व आवश्यकताएं

- Python 3.8 या उससे ऊपर
- Telegram Bot Token (@BotFather से प्राप्त करें)
- ffmpeg (audio conversion के लिए)

### Installation / स्थापना

1. **Clone the repository / Repository को clone करें**
```bash
git clone https://github.com/ibrsiaika/Ai-yt-ig-video-downloader.git
cd Ai-yt-ig-video-downloader
```

2. **Install ffmpeg / ffmpeg install करें**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

3. **Create virtual environment / Virtual environment बनाएं**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# या Windows के लिए: venv\Scripts\activate
```

4. **Install dependencies / Dependencies install करें**
```bash
pip install -r requirements.txt
```

5. **Setup environment variables / Environment variables setup करें**
```bash
cp .env.example .env
```

Edit `.env` file और अपना Telegram Bot Token डालें:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

6. **Run the bot / Bot को चलाएं**
```bash
python main.py
```

## 📱 Usage / उपयोग

1. **Start the bot / Bot को start करें**
   - Telegram में अपने bot को खोलें
   - `/start` command भेजें

2. **Send a link / Link भेजें**
   - YouTube या Instagram का कोई भी public link भेजें
   - Bot automatically detect करेगा कि कौन सा platform है

3. **Select format (YouTube only) / Format select करें (सिर्फ YouTube के लिए)**
   - MP4 (Video) या MP3 (Audio) select करें
   - Bot download करके भेज देगा

## 🎯 Commands / कमांड्स

- `/start` - Bot को शुरू करें और welcome message देखें
- `/help` - Help guide देखें
- `/about` - Bot के बारे में जानकारी

## 📂 Project Structure / प्रोजेक्ट की संरचना

```
├── main.py                  # Main bot entry point / मुख्य bot entry point
├── config.py                # Configuration settings / Configuration की settings
├── youtube_handler.py       # YouTube download logic / YouTube download की logic
├── instagram_handler.py     # Instagram download logic / Instagram download की logic
├── utils.py                 # Helper functions / Helper functions
├── requirements.txt         # Python dependencies / Python की dependencies
├── .env.example            # Environment template / Environment की template
├── .gitignore              # Git ignore file
├── README.md               # This file / यह file
└── deployment_guide.md     # Hosting instructions / Hosting की instructions
```

## 🔧 Configuration / कॉन्फ़िगरेशन

Bot की settings `config.py` में modify कर सकते हैं:

- `MAX_TELEGRAM_FILE_SIZE`: Maximum file size for Telegram upload (default: 50MB)
- `MAX_DOWNLOAD_SIZE`: Maximum file size to attempt downloading (default: 500MB)
- `DOWNLOAD_TIMEOUT`: Timeout for downloads (default: 300 seconds)

## ⚠️ Limitations / सीमाएं

- Telegram bot API की limit 50MB है files के लिए
- बहुत बड़ी files के लिए download link generate होगा
- Private Instagram accounts के लिए login required है
- Network speed पर depend करता है

## 🐛 Troubleshooting / समस्या निवारण

### Bot start नहीं हो रहा?
- Check करें कि `.env` file में सही token है
- Virtual environment activate है या नहीं
- सभी dependencies install हैं या नहीं

### Download fail हो रहा है?
- Internet connection check करें
- Link public है या नहीं verify करें
- Video available है या delete नहीं हुआ

### ffmpeg error आ रहा है?
- ffmpeg properly install है या नहीं check करें
- PATH में add है या नहीं verify करें

## 🚀 Deployment / डिप्लॉयमेंट

Detailed deployment instructions के लिए `deployment_guide.md` देखें।

**Supported Platforms:**
- Render
- Heroku
- Railway
- VPS (Ubuntu/Debian)

## 🤝 Contributing / योगदान

Contributions welcome हैं! Please feel free to submit a Pull Request.

## 📄 License / लाइसेंस

This project is open source and available under the MIT License.

## 👨‍💻 Developer / डेवलपर

**GitHub:** [@ibrsiaika](https://github.com/ibrsiaika)

## 🙏 Acknowledgments / आभार

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [instaloader](https://github.com/instaloader/instaloader)

## 📞 Support / सहायता

Issues या questions के लिए GitHub issues का use करें।

---

**Note:** यह bot सिर्फ educational purposes के लिए है। Content download करते समय copyright laws का ध्यान रखें।
