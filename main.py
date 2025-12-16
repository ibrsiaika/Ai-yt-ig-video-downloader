import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import config
from youtube_handler import download_youtube
from instagram_handler import download_instagram
from utils import is_youtube_url, is_instagram_url, cleanup_temp_files

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get token from environment
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome_message = """
🎬 **YouTube aur Instagram Video Downloader Bot**

Mujhe YouTube ya Instagram link bhejo, main download kar dunga!

**Features:**
✅ YouTube videos (MP4) aur audio (MP3)
✅ Instagram videos, reels, stories
✅ High quality downloads
✅ Large files ke liye direct links

**Bas link bhejo aur enjoy karo!** 📱
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
📖 **Help Guide**

1. YouTube link bhejo → Option select karo (MP4/MP3)
2. Instagram link bhejo → Video download ho jayegi

**Supported Links:**
• YouTube: https://www.youtube.com/watch?v=...
• Instagram: https://www.instagram.com/p/... , https://www.instagram.com/reel/...

**Tips:**
• Large files (50MB+) ke liye download link milega
• Public posts ke liye best results
• Network stable hona chahiye

Kya problem hai? /support bhejo!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    about_text = """
ℹ️ **About Bot**

Ye bot aapko YouTube aur Instagram se videos download karne mein madad karta hai.

**Developer:** @ibrsiaika
**Version:** 1.0.0
**Library:** python-telegram-bot

Agar koi suggestion hai to contact karo! 💬
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming URLs from user"""
    try:
        user_message = update.message.text.strip()
        user_id = update.message.from_user.id
        
        logger.info(f"User {user_id} sent: {user_message}")
        
        # Show processing message
        processing_msg = await update.message.reply_text("🔄 Processing... Please wait!")
        
        # Check if it's a YouTube URL
        if is_youtube_url(user_message):
            logger.info(f"YouTube URL detected: {user_message}")
            await processing_msg.edit_text("📥 Downloading YouTube video... Thoda intezaar karo!")
            await download_youtube(update, context, user_message, processing_msg)
        
        # Check if it's an Instagram URL
        elif is_instagram_url(user_message):
            logger.info(f"Instagram URL detected: {user_message}")
            await processing_msg.edit_text("📥 Downloading Instagram media... Thoda intezaar karo!")
            await download_instagram(update, context, user_message, processing_msg)
        
        else:
            await processing_msg.edit_text("❌ Galat URL! YouTube ya Instagram link bhejo.")
            logger.warning(f"Invalid URL from {user_id}: {user_message}")
    
    except Exception as e:
        logger.error(f"Error handling URL: {str(e)}")
        await update.message.reply_text(f"❌ Kuch error hua: {str(e)[:100]}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button clicks"""
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        logger.info(f"Button pressed: {data}")
        
        # Extract URL from context
        url = context.user_data.get('current_url')
        if not url:
            await query.edit_message_text("❌ URL nahi mila! Link dobara bhejo.")
            return
        
        if data == 'yt_mp4':
            await query.edit_message_text("📥 MP4 download ho raha hai...")
            await download_youtube(update, context, url, query.message, format='mp4')
        
        elif data == 'yt_mp3':
            await query.edit_message_text("🎵 MP3 download ho raha hai...")
            await download_youtube(update, context, url, query.message, format='mp3')
        
        elif data == 'ig_video':
            await query.edit_message_text("📥 Video download ho raha hai...")
            await download_instagram(update, context, url, query.message)
    
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")
        await query.edit_message_text(f"❌ Error: {str(e)[:100]}")

def main():
    """Start the bot"""
    # Create the Application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    
    # Add message handler for URLs
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Add callback query handler for buttons
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    logger.info("🤖 Bot started successfully!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
