"""
YouTube download handler using yt-dlp
yt-dlp का उपयोग करके YouTube download handler

This file handles all YouTube video and audio downloads.
यह file सभी YouTube video और audio downloads को handle करती है।
"""

import os
import logging
import asyncio
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import yt_dlp
import config
from utils import format_file_size, get_file_size, cleanup_temp_files, sanitize_filename, extract_video_id_youtube

logger = logging.getLogger(__name__)


async def show_youtube_options(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, message) -> None:
    """
    Show format selection options for YouTube video
    YouTube video के लिए format selection options दिखाएं
    
    Args:
        update: Telegram update object
        context: Telegram context object
        url: YouTube video URL
        message: Message object to edit
    """
    # Store URL in user data for callback / callback के लिए user data में URL store करें
    context.user_data['current_url'] = url
    
    # Create inline keyboard / Inline keyboard बनाएं
    keyboard = [
        [
            InlineKeyboardButton("🎥 Video (MP4)", callback_data='yt_mp4'),
            InlineKeyboardButton("🎵 Audio (MP3)", callback_data='yt_mp3')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "📹 **YouTube Video Detected!**\n\n"
        "Kya download karna hai? Select karo:\n"
        "• MP4 - Video with audio\n"
        "• MP3 - Audio only",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def download_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, 
                          message, format: str = None) -> None:
    """
    Download YouTube video or audio
    YouTube video या audio download करें
    
    Args:
        update: Telegram update object
        context: Telegram context object
        url: YouTube video URL
        message: Message object to edit
        format: 'mp4' for video, 'mp3' for audio, None to show options
    """
    try:
        # If no format specified, show options / अगर कोई format specify नहीं है, तो options दिखाएं
        if format is None:
            await show_youtube_options(update, context, url, message)
            return
        
        # Update status / Status update करें
        await message.edit_text(f"📥 Downloading {'video' if format == 'mp4' else 'audio'}... Please wait!\n"
                               f"⏳ Thoda time lag sakta hai...")
        
        # Extract video info first / पहले video info extract करें
        video_info = await get_youtube_info(url)
        if not video_info:
            await message.edit_text("❌ Video information nahi mil payi. URL check karo!")
            return
        
        # Check video duration / Video duration check करें
        duration = video_info.get('duration', 0)
        if duration > 3600:  # More than 1 hour / 1 घंटे से ज्यादा
            await message.edit_text(
                "⚠️ Video bahut lambi hai (1 hour+).\n"
                "Download mein time lag sakta hai ya fail ho sakta hai.\n"
                "Koshish kar rahe hain..."
            )
        
        # Generate filename / Filename generate करें
        video_id = extract_video_id_youtube(url)
        title = sanitize_filename(video_info.get('title', 'video'))
        
        if format == 'mp4':
            output_filename = f"{title}_{video_id}.mp4"
        else:  # mp3
            output_filename = f"{title}_{video_id}.mp3"
        
        output_path = os.path.join(config.TEMP_DOWNLOAD_DIR, output_filename)
        
        # Download the file / File download करें
        success = await download_youtube_file(url, output_path, format)
        
        if not success or not os.path.exists(output_path):
            await message.edit_text("❌ Download failed! Network issue ya video unavailable ho sakta hai.")
            return
        
        # Check file size / File size check करें
        file_size = get_file_size(output_path)
        if file_size is None:
            await message.edit_text("❌ Downloaded file access nahi ho pa rahi!")
            cleanup_temp_files([output_path])
            return
        
        # If file is too large / अगर file bahut badi hai
        if file_size > config.MAX_TELEGRAM_FILE_SIZE:
            file_size_str = format_file_size(file_size)
            await message.edit_text(
                f"⚠️ File bahut badi hai ({file_size_str})!\n\n"
                f"Telegram limit 50MB hai.\n"
                f"File saved hai lekin upload nahi ho sakti.\n\n"
                f"💡 **Solution:** Cloud storage use karo ya video quality kam karo."
            )
            cleanup_temp_files([output_path])
            return
        
        # Upload to Telegram / Telegram par upload करें
        await message.edit_text(f"📤 Uploading {format_file_size(file_size)}... Almost done!")
        
        # Get the actual Update object for sending files
        # Files भेजने के लिए actual Update object प्राप्त करें
        chat_id = update.effective_chat.id
        
        try:
            if format == 'mp4':
                # Send as video / Video के रूप में भेजें
                with open(output_path, 'rb') as video_file:
                    await context.bot.send_video(
                        chat_id=chat_id,
                        video=video_file,
                        caption=f"🎬 {title}\n\n📦 Size: {format_file_size(file_size)}",
                        supports_streaming=True,
                        read_timeout=60,
                        write_timeout=60
                    )
            else:  # mp3
                # Send as audio / Audio के रूप में भेजें
                with open(output_path, 'rb') as audio_file:
                    await context.bot.send_audio(
                        chat_id=chat_id,
                        audio=audio_file,
                        caption=f"🎵 {title}\n\n📦 Size: {format_file_size(file_size)}",
                        title=title,
                        read_timeout=60,
                        write_timeout=60
                    )
            
            # Delete the status message / Status message delete करें
            await message.delete()
            
            logger.info(f"Successfully sent {format} to user {chat_id}")
            
        except Exception as upload_error:
            logger.error(f"Upload error: {str(upload_error)}")
            await message.edit_text(
                f"❌ Upload failed!\n\n"
                f"Possible reasons:\n"
                f"• Network issue\n"
                f"• Telegram server busy\n"
                f"• File size: {format_file_size(file_size)}\n\n"
                f"Please try again!"
            )
        
        # Cleanup / Cleanup करें
        cleanup_temp_files([output_path])
        
    except Exception as e:
        logger.error(f"YouTube download error: {str(e)}")
        await message.edit_text(f"❌ Error: {str(e)[:200]}")


async def get_youtube_info(url: str) -> Optional[dict]:
    """
    Get YouTube video information without downloading
    Download किए बिना YouTube video की information प्राप्त करें
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video info dict or None if failed
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
        logger.error(f"Error getting YouTube info: {str(e)}")
        return None


async def download_youtube_file(url: str, output_path: str, format: str) -> bool:
    """
    Download YouTube video or audio file
    YouTube video या audio file download करें
    
    Args:
        url: YouTube video URL
        output_path: Output file path
        format: 'mp4' or 'mp3'
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if format == 'mp4':
            # Download video / Video download करें
            ydl_opts = {
                'format': config.YOUTUBE_VIDEO_FORMAT,
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
                'extract_audio': False,
                'merge_output_format': 'mp4',
            }
        else:  # mp3
            # Download and convert to audio / Download करें और audio में convert करें
            ydl_opts = {
                'format': config.YOUTUBE_AUDIO_FORMAT,
                'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        
        # Download with timeout / Timeout के साथ download करें
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.wait_for(
                asyncio.to_thread(ydl.download, [url]),
                timeout=config.DOWNLOAD_TIMEOUT
            )
        
        return True
        
    except asyncio.TimeoutError:
        logger.error(f"YouTube download timeout for {url}")
        return False
    except Exception as e:
        logger.error(f"YouTube download error: {str(e)}")
        return False
