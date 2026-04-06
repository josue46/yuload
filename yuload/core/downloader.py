"""Downloader Module - Handles actual video downloads"""

import os
from pathlib import Path
from typing import Callable, Optional
from concurrent.futures import ThreadPoolExecutor
import threading
from ..utils.logger import setup_logger
from ..utils.config import Config
from .youtube_handler import YouTubeHandler

logger = setup_logger(__name__)


class Downloader:
    """Handle video and subtitle downloads"""
    
    def __init__(self, youtube_handler: YouTubeHandler):
        """
        Initialize downloader
        
        Args:
            youtube_handler: YouTubeHandler instance
        """
        self.handler = youtube_handler
        self.is_downloading = False
        self.current_thread: Optional[threading.Thread] = None
    
    def download_video(
        self,
        quality: str,
        output_path: str,
        include_subtitle: bool = False,
        subtitle_code: Optional[str] = None,
        progress_callback: Optional[Callable] = None,
        completion_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
    ) -> bool:
        """
        Download video in separate thread
        
        Args:
            quality: Video quality (e.g., "720p")
            output_path: Output directory path
            include_subtitle: Whether to download subtitles
            subtitle_code: Language code for subtitles
            progress_callback: Callback function(current, total) for progress
            completion_callback: Callback when download completes
            error_callback: Callback function(error_message) for errors
            
        Returns:
            True if download started successfully
        """
        if self.is_downloading:
            error_msg = "Download already in progress"
            logger.warning(error_msg)
            if error_callback:
                error_callback(error_msg)
            return False
        
        # Start download in separate thread
        self.is_downloading = True
        self.current_thread = threading.Thread(
            target=self._download_video_thread,
            args=(
                quality,
                output_path,
                include_subtitle,
                subtitle_code,
                progress_callback,
                completion_callback,
                error_callback,
            ),
            daemon=True
        )
        self.current_thread.start()
        return True
    
    def _download_video_thread(
        self,
        quality: str,
        output_path: str,
        include_subtitle: bool,
        subtitle_code: Optional[str],
        progress_callback: Optional[Callable],
        completion_callback: Optional[Callable],
        error_callback: Optional[Callable],
    ):
        """Internal method to download video in thread"""
        try:
            # Validate output path
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Get video and audio streams
            video_stream = self.handler.get_stream_by_quality(quality)
            audio_stream = self.handler.get_audio_stream()
            
            if not video_stream or not audio_stream:
                raise ValueError(f"Cannot find streams for quality {quality}")
            
            # Get video info for filename
            video_info = self.handler.current_video
            safe_title = self._make_safe_filename(video_info.title)
            
            # Download video
            logger.info(f"Starting video download: {quality}")
            video_file = self._download_stream(
                video_stream,
                output_dir,
                f"{safe_title}_video.mp4",
                progress_callback
            )
            
            if not video_file:
                raise Exception("Video download failed")
            
            # Download audio
            logger.info("Starting audio download")
            audio_file = self._download_stream(
                audio_stream,
                output_dir,
                f"{safe_title}_audio.mp4",
                progress_callback
            )
            
            if not audio_file:
                raise Exception("Audio download failed")
            
            # Merge video and audio
            logger.info("Merging video and audio")
            final_file = self._merge_streams(
                video_file,
                audio_file,
                output_dir,
                safe_title
            )
            
            # Download subtitles if requested
            if include_subtitle and subtitle_code:
                logger.info(f"Downloading subtitles: {subtitle_code}")
                self._download_subtitle(
                    subtitle_code,
                    output_dir,
                    safe_title
                )
            
            logger.info(f"Download completed: {final_file}")
            if completion_callback:
                completion_callback(final_file)
            
        except Exception as e:
            error_msg = f"Download error: {str(e)}"
            logger.error(error_msg)
            if error_callback:
                error_callback(error_msg)
        
        finally:
            self.is_downloading = False
    
    def _download_stream(
        self,
        stream,
        output_dir: Path,
        filename: str,
        progress_callback: Optional[Callable]
    ) -> Optional[str]:
        """
        Download a single stream
        
        Args:
            stream: Stream object to download
            output_dir: Output directory
            filename: Output filename
            progress_callback: Progress callback
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            filepath = output_dir / filename
            stream.download(output_path=str(output_dir), filename=filename)
            return str(filepath)
        except Exception as e:
            logger.error(f"Error downloading stream: {e}")
            return None
    
    def _merge_streams(
        self,
        video_path: str,
        audio_path: str,
        output_dir: Path,
        title: str
    ) -> str:
        """
        Merge video and audio streams
        (Uses moviepy for merging - requires ffmpeg)
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_dir: Output directory
            title: Video title for output filename
            
        Returns:
            Path to merged file
        """
        output_file = output_dir / f"{title}.mp4"
        
        try:
            # Try using moviepy if available
            try:
                from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
                
                video = VideoFileClip(video_path)
                audio = AudioFileClip(audio_path)
                
                final = video.set_audio(audio)
                final.write_videofile(str(output_file), verbose=False, logger=None)
                
                video.close()
                audio.close()
                
            except ImportError:
                logger.warning("moviepy not installed, skipping merge. Using video stream only.")
                # Fall back to using video file directly
                import shutil
                shutil.copy(video_path, output_file)
            
            # Clean up temporary files
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error merging streams: {e}")
            # Return video file even if merge failed
            return video_path
    
    def _download_subtitle(
        self,
        subtitle_code: str,
        output_dir: Path,
        title: str
    ) -> bool:
        """
        Download subtitles
        
        Args:
            subtitle_code: Language code for subtitles
            output_dir: Output directory
            title: Video title for filename
            
        Returns:
            True if successful
        """
        try:
            caption = self.handler.get_caption_by_code(subtitle_code)
            if not caption:
                logger.warning(f"Caption not found for code {subtitle_code}")
                return False
            
            subtitle_file = output_dir / f"{title}_{subtitle_code}.vtt"
            caption.save(str(subtitle_file))
            logger.info(f"Subtitles downloaded: {subtitle_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading subtitles: {e}")
            return False
    
    @staticmethod
    def _make_safe_filename(filename: str) -> str:
        """Make filename safe for file systems"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:200]  # Limit filename length
    
    def cancel_download(self):
        """Cancel current download"""
        self.is_downloading = False
        logger.info("Download cancellation requested")
