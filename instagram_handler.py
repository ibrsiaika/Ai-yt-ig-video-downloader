"""
Instagram download handler using yt-dlp and instaloader
yt-dlp और instaloader का उपयोग करके Instagram download handler

This file handles all Instagram media downloads (videos, reels, stories, carousels).
यह file सभी Instagram media downloads (videos, reels, stories, carousels) को handle करती है।
"""

import os
import logging
import asyncio
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
import yt_dlp
import config
from utils import format_file_size, get_file_size, cleanup_temp_files, sanitize_filename, extract_shortcode_instagram

logger = logging.getLogger(__name__)


async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, message) -> None:
    """
    Download Instagram video/reel/story
    Instagram video/reel/story download करें
    
    Args:
        update: Telegram update object
        context: Telegram context object
        url: Instagram media URL
        message: Message object to edit
    """
    try:
        # Update status / Status update करें
        await message.edit_text(
            "📥 Instagram se download ho raha hai...\n"
            "⏳ Please wait, thoda time lag sakta hai!"
        )
        
        # Extract shortcode / Shortcode extract करें
        shortcode = extract_shortcode_instagram(url)
        if not shortcode:
            # Try to get info anyway / फिर भी info लेने की कोशिश करें
            shortcode = "instagram_media"
        
        # Generate output filename / Output filename generate करें
        output_filename = f"instagram_{shortcode}.mp4"
        output_path = os.path.join(config.TEMP_DOWNLOAD_DIR, output_filename)
        
        # Try downloading with yt-dlp first (works for most public posts)
        # पहले yt-dlp से download करने की कोशिश करें (most public posts के लिए काम करता है)
        success = await download_instagram_ytdlp(url, output_path)
        
        if not success:
            # If yt-dlp fails, inform user / अगर yt-dlp fail होता है, तो user को inform करें
            await message.edit_text(
                "❌ Download failed!\n\n"
                "**Possible reasons:**\n"
                "• Private account (login required)\n"
                "• Story expired\n"
                "• Invalid link\n"
                "• Network issue\n\n"
                "💡 **Tip:** Make sure the post is public!"
            )
            return
        
        # Check if file exists / Check करें कि file exist करती है
        if not os.path.exists(output_path):
            await message.edit_text(
                "❌ File download nahi hui!\n"
                "Link check karo ya baad mein try karo."
            )
            return
        
        # Check file size / File size check करें
        file_size = get_file_size(output_path)
        if file_size is None or file_size == 0:
            await message.edit_text("❌ Downloaded file corrupt hai ya empty hai!")
            cleanup_temp_files([output_path])
            return
        
        # If file is too large / अगर file bahut badi hai
        if file_size > config.MAX_TELEGRAM_FILE_SIZE:
            file_size_str = format_file_size(file_size)
            await message.edit_text(
                f"⚠️ File bahut badi hai ({file_size_str})!\n\n"
                f"Telegram limit 50MB hai.\n"
                f"💡 **Solution:** File manually download karo ya compress karo."
            )
            cleanup_temp_files([output_path])
            return
        
        # Upload to Telegram / Telegram par upload करें
        await message.edit_text(f"📤 Uploading {format_file_size(file_size)}... Almost there!")
        
        # Get chat ID / Chat ID प्राप्त करें
        chat_id = update.effective_chat.id
        
        try:
            # Send as video / Video के रूप में भेजें
            with open(output_path, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption=f"📸 Instagram Video\n\n📦 Size: {format_file_size(file_size)}",
                    supports_streaming=True,
                    read_timeout=60,
                    write_timeout=60
                )
            
            # Delete the status message / Status message delete करें
            await message.delete()
            
            logger.info(f"Successfully sent Instagram video to user {chat_id}")
            
        except Exception as upload_error:
            logger.error(f"Upload error: {str(upload_error)}")
            await message.edit_text(
                f"❌ Upload failed!\n\n"
                f"File size: {format_file_size(file_size)}\n"
                f"Network issue ho sakta hai. Please retry!"
            )
        
        # Cleanup / Cleanup करें
        cleanup_temp_files([output_path])
        
    except Exception as e:
        logger.error(f"Instagram download error: {str(e)}")
        await message.edit_text(f"❌ Error: {str(e)[:200]}")


async def download_instagram_ytdlp(url: str, output_path: str) -> bool:
    """
    Download Instagram media using yt-dlp
    yt-dlp का उपयोग करके Instagram media download करें
    
    Args:
        url: Instagram media URL
        output_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Instagram specific options / Instagram specific options
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
        }
        
        # Download with timeout / Timeout के साथ download करें
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.wait_for(
                asyncio.to_thread(ydl.download, [url]),
                timeout=config.DOWNLOAD_TIMEOUT
            )
        
        return True
        
    except asyncio.TimeoutError:
        logger.error(f"Instagram download timeout for {url}")
        return False
    except Exception as e:
        logger.error(f"Instagram yt-dlp download error: {str(e)}")
        return False


async def download_instagram_instaloader(url: str, output_path: str) -> bool:
    """
    Download Instagram media using instaloader (fallback method)
    instaloader का उपयोग करके Instagram media download करें (fallback method)
    
    This is a fallback method if yt-dlp doesn't work.
    यह fallback method है अगर yt-dlp काम नहीं करता।
    
    Args:
        url: Instagram media URL
        output_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Import instaloader / instaloader import करें
        import instaloader
        
        # Create instaloader instance / Instaloader instance बनाएं
        L = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True
        )
        
        # Extract shortcode from URL / URL से shortcode extract करें
        shortcode = extract_shortcode_instagram(url)
        if not shortcode:
            return False
        
        # Get post / Post प्राप्त करें
        post = await asyncio.to_thread(instaloader.Post.from_shortcode, L.context, shortcode)
        
        # Download video / Video download करें
        if post.is_video:
            video_url = post.video_url
            # Download the video file / Video file download करें
            await asyncio.to_thread(L.download_pic, 
                                   filename=output_path.replace('.mp4', ''),
                                   url=video_url,
                                   mtime=post.date_local)
            return True
        else:
            logger.warning("Post is not a video")
            return False
            
    except Exception as e:
        logger.error(f"Instagram instaloader download error: {str(e)}")
        return False


async def get_instagram_info(url: str) -> Optional[dict]:
    """
    Get Instagram media information without downloading
    Download किए बिना Instagram media की information प्राप्त करें
    
    Args:
        url: Instagram media URL
        
    Returns:
        Media info dict or None if failed
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            return info
    except Exception as e:
        logger.error(f"Error getting Instagram info: {str(e)}")
        return None
