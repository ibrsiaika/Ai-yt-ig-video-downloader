# 🚀 Deployment Guide / डिप्लॉयमेंट गाइड

This guide explains how to deploy your Telegram bot on various hosting platforms.
यह guide बताती है कि अपने Telegram bot को विभिन्न hosting platforms पर कैसे deploy करें।

## Table of Contents / विषय सूची

1. [Render](#render-deployment)
2. [Heroku](#heroku-deployment)
3. [Railway](#railway-deployment)
4. [VPS (Ubuntu/Debian)](#vps-deployment)
5. [Docker (Optional)](#docker-deployment)

---

## 🌐 Render Deployment

Render एक modern cloud platform है जो free tier provide करता है।

### Steps / कदम:

1. **Account बनाएं**
   - [Render.com](https://render.com) पर जाएं
   - Sign up करें (GitHub account से भी sign up कर सकते हैं)

2. **New Web Service बनाएं**
   - Dashboard में "New +" button click करें
   - "Web Service" select करें
   - अपनी GitHub repository connect करें

3. **Configuration**
   ```
   Name: telegram-bot-downloader
   Environment: Python 3
   Build Command: pip install -r requirements.txt && apt-get update && apt-get install -y ffmpeg
   Start Command: python main.py
   ```

4. **Environment Variables**
   - "Environment" tab में जाएं
   - Add करें:
     - Key: `TELEGRAM_BOT_TOKEN`
     - Value: आपका bot token

5. **Deploy**
   - "Create Web Service" button click करें
   - Bot automatically deploy हो जाएगा

**Note:** Render का free tier web services के लिए है। Background workers के लिए paid plan चाहिए, लेकिन आप web service के रूप में भी bot run कर सकते हैं।

---

## 🔴 Heroku Deployment

Heroku एक popular PaaS platform है (paid plans से migration के बाद)।

### Steps / कदम:

1. **Heroku CLI Install करें**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download installer from heroku.com
```

2. **Login करें**
```bash
heroku login
```

3. **Project को prepare करें**

Create `Procfile`:
```
worker: python main.py
```

Create `runtime.txt`:
```
python-3.11.7
```

Create `Aptfile` (ffmpeg के लिए):
```
ffmpeg
```

4. **App बनाएं और deploy करें**
```bash
# Git repository initialize करें (अगर नहीं है तो)
git init
git add .
git commit -m "Initial commit"

# Heroku app create करें
heroku create your-bot-name

# Buildpacks add करें
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python

# Environment variable set करें
heroku config:set TELEGRAM_BOT_TOKEN=your_token_here

# Deploy करें
git push heroku main

# Worker dyno enable करें
heroku ps:scale worker=1

# Logs देखें
heroku logs --tail
```

**Cost:** Heroku अब free tier नहीं देता। Minimum $5/month से plans start होते हैं।

---

## 🚂 Railway Deployment

Railway एक modern deployment platform है जो GitHub integration provide करता है।

### Steps / कदम:

1. **Account बनाएं**
   - [Railway.app](https://railway.app) पर जाएं
   - GitHub account से sign up करें

2. **New Project बनाएं**
   - "New Project" click करें
   - "Deploy from GitHub repo" select करें
   - अपनी repository select करें

3. **Configuration**
   - Railway automatically Python project detect करेगा
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

4. **Environment Variables**
   - Variables tab में जाएं
   - Add करें:
     - `TELEGRAM_BOT_TOKEN`: आपका token

5. **Add ffmpeg**

Railway पर ffmpeg install करने के लिए `nixpacks.toml` file बनाएं:
```toml
[phases.setup]
aptPkgs = ["ffmpeg"]
```

6. **Deploy**
   - Changes commit और push करें
   - Railway automatically redeploy करेगा

**Free Tier:** Railway $5 credit हर महीने free देता है, जो small bots के लिए enough है।

---

## 🖥️ VPS Deployment

अपने खुद के VPS (Ubuntu/Debian) पर deployment।

### Prerequisites / पूर्व आवश्यकताएं:
- Ubuntu 20.04+ या Debian 11+ server
- Root या sudo access
- Domain name (optional)

### Steps / कदम:

1. **Server को update करें**
```bash
sudo apt update
sudo apt upgrade -y
```

2. **Python और dependencies install करें**
```bash
sudo apt install python3 python3-pip python3-venv ffmpeg git -y
```

3. **Project को clone करें**
```bash
cd /home/your-username
git clone https://github.com/ibrsiaika/Ai-yt-ig-video-downloader.git
cd Ai-yt-ig-video-downloader
```

4. **Virtual environment setup करें**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Environment variables configure करें**
```bash
cp .env.example .env
nano .env  # अपना token add करें
```

6. **Systemd service बनाएं**

`/etc/systemd/system/telegram-bot.service` file बनाएं:
```ini
[Unit]
Description=Telegram Video Downloader Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/Ai-yt-ig-video-downloader
Environment="PATH=/home/your-username/Ai-yt-ig-video-downloader/venv/bin"
ExecStart=/home/your-username/Ai-yt-ig-video-downloader/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

7. **Service enable और start करें**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

8. **Logs देखें**
```bash
sudo journalctl -u telegram-bot -f
```

### Optional: Nginx Reverse Proxy

अगर आप webhooks use करना चाहते हैं (optional):
```bash
sudo apt install nginx -y
```

Nginx configuration `/etc/nginx/sites-available/bot`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐳 Docker Deployment (Optional)

Docker container में bot run करने के लिए।

### Dockerfile बनाएं:

```dockerfile
FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create downloads directory
RUN mkdir -p downloads

# Run the bot
CMD ["python", "main.py"]
```

### docker-compose.yml बनाएं:

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: telegram-video-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - LOG_LEVEL=INFO
    volumes:
      - ./downloads:/app/downloads
```

### Run करें:

```bash
# Build और run
docker-compose up -d

# Logs देखें
docker-compose logs -f

# Stop करें
docker-compose down
```

---

## 📊 Monitoring & Maintenance / निगरानी और रखरखाव

### Logs Check करना:

**Render/Railway/Heroku:**
- Dashboard में logs section देखें

**VPS:**
```bash
sudo journalctl -u telegram-bot -f
```

**Docker:**
```bash
docker-compose logs -f
```

### Bot Update करना:

**Git-based deployments:**
```bash
git pull origin main
# Restart service/container
```

**VPS:**
```bash
cd /home/your-username/Ai-yt-ig-video-downloader
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
```

**Docker:**
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🔒 Security Best Practices / सुरक्षा सर्वोत्तम प्रथाएं

1. **Environment Variables:** कभी भी tokens को code में hardcode न करें
2. **Firewall:** VPS पर firewall configure करें (UFW)
3. **Updates:** Regular updates install करें
4. **Backups:** Important data का backup लें
5. **Monitoring:** Error notifications setup करें

### UFW Firewall Setup (VPS):
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 💡 Tips / सुझाव

1. **Resource Monitoring:** CPU और memory usage monitor करें
2. **Rate Limiting:** Telegram API rate limits का ध्यान रखें
3. **Error Handling:** Proper error logging setup करें
4. **Cleanup:** Regular cleanup scripts चलाएं temporary files के लिए
5. **Testing:** Production में deploy करने से पहले test करें

---

## 🆘 Common Issues / सामान्य समस्याएं

### Bot offline हो जाता है:
- Service/container restart करें
- Logs check करें errors के लिए
- Token verify करें

### ffmpeg not found error:
- Ensure ffmpeg properly installed है
- PATH में add है verify करें

### Download failures:
- Network connectivity check करें
- yt-dlp update करें: `pip install -U yt-dlp`

### Memory issues:
- Server resources upgrade करें
- Cleanup script add करें

---

## 📞 Support / सहायता

अगर deployment में कोई problem है तो:
- GitHub issues में report करें
- Documentation फिर से पढ़ें
- Community forums में help लें

---

**Happy Deploying! 🎉**

यदि यह guide helpful लगी तो star ⭐ करना न भूलें!
