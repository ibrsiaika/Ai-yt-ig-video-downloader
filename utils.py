"""
Utility functions for the bot
Bot के लिए utility functions

This file contains helper functions used throughout the bot.
यह file bot में use होने वाले helper functions contain करती है।
"""

import os
import re
import logging
from typing import Optional
import config

logger = logging.getLogger(__name__)


def is_youtube_url(url: str) -> bool:
    """
    Check if the URL is a valid YouTube URL
    Check करें कि URL valid YouTube URL है या नहीं
    
    Args:
        url: URL string to check / check करने के लिए URL string
        
    Returns:
        True if valid YouTube URL, False otherwise
        True अगर valid YouTube URL है, नहीं तो False
    """
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/',
        r'youtube\.com/watch\?v=',
        r'youtu\.be/',
        r'youtube\.com/shorts/',
        r'youtube\.com/embed/'
    ]
    
    for pattern in youtube_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def is_instagram_url(url: str) -> bool:
    """
    Check if the URL is a valid Instagram URL
    Check करें कि URL valid Instagram URL है या नहीं
    
    Args:
        url: URL string to check / check करने के लिए URL string
        
    Returns:
        True if valid Instagram URL, False otherwise
        True अगर valid Instagram URL है, नहीं तो False
    """
    instagram_patterns = [
        r'(https?://)?(www\.)?instagram\.com/(p|reel|tv|stories)/',
        r'(https?://)?(www\.)?instagram\.com/[a-zA-Z0-9._]+/?$'
    ]
    
    for pattern in instagram_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    Bytes को human-readable format में convert करें
    
    Args:
        size_bytes: Size in bytes / bytes में size
        
    Returns:
        Formatted string like "10.5 MB" / "10.5 MB" जैसी formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_file_size(filepath: str) -> Optional[int]:
    """
    Get the size of a file in bytes
    File का size bytes में प्राप्त करें
    
    Args:
        filepath: Path to the file / file का path
        
    Returns:
        File size in bytes or None if file doesn't exist
        File size bytes में या None अगर file exist नहीं करती
    """
    try:
        if os.path.exists(filepath):
            return os.path.getsize(filepath)
        return None
    except Exception as e:
        logger.error(f"Error getting file size for {filepath}: {str(e)}")
        return None


def cleanup_temp_files(file_paths: list = None) -> None:
    """
    Clean up temporary downloaded files
    Temporary download की गई files को clean करें
    
    Args:
        file_paths: List of file paths to delete, or None to clean all in temp dir
                    Delete करने के लिए file paths की list, या temp dir में सभी को clean करने के लिए None
    """
    try:
        if file_paths:
            # Delete specific files / Specific files delete करें
            for filepath in file_paths:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Deleted file: {filepath}")
        else:
            # Clean entire temp directory / पूरी temp directory clean करें
            temp_dir = config.TEMP_DOWNLOAD_DIR
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    filepath = os.path.join(temp_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        logger.info(f"Deleted file: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    Invalid characters को remove करके filename को sanitize करें
    
    Args:
        filename: Original filename / Original filename
        
    Returns:
        Sanitized filename / Sanitized filename
    """
    # Remove invalid characters for most filesystems
    # Most filesystems के लिए invalid characters remove करें
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length / Filename की length limit करें
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename


def extract_video_id_youtube(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL
    YouTube URL से video ID extract करें
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID or None if not found / Video ID या None अगर नहीं मिली
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_shortcode_instagram(url: str) -> Optional[str]:
    """
    Extract shortcode from Instagram URL
    Instagram URL से shortcode extract करें
    
    Args:
        url: Instagram URL
        
    Returns:
        Shortcode or None if not found / Shortcode या None अगर नहीं मिला
    """
    pattern = r'/(p|reel|tv)/([A-Za-z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(2)
    return None
