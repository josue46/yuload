"""Main Window for Yuload Application"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from pathlib import Path
import threading

from ..utils.config import Config
from ..utils.validators import validate_youtube_url
from ..utils.logger import setup_logger
from ..core.youtube_handler import YouTubeHandler
from ..core.downloader import Downloader
from .styles import Colors, StyleManager
from .widgets import (
    ModernButton, AnimatedProgressBar, VideoInfoFrame, 
    QualitySelector, SubtitleSelector, StatusBar
)

logger = setup_logger(__name__)


class MainWindow(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        # Configure window
        self.title("Yuload - YouTube Video Downloader")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.minsize(Config.MIN_WINDOW_WIDTH, Config.MIN_WINDOW_HEIGHT)
        self.configure(bg=Colors.PRIMARY)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize components
        Config.init_directories()
        self.youtube_handler = YouTubeHandler()
        self.downloader = Downloader(self.youtube_handler)
        
        self.current_video_info = None
        self.is_loading = False
        self.selected_quality = None
        
        # Create UI
        self._create_widgets()
        self._setup_styles()
        
        # Set icon if available
        self._set_icon()
        
        logger.info("Application started")
    
    def _create_widgets(self):
        """Create all widgets"""
        # Main container
        main_container = tk.Frame(self, bg=Colors.PRIMARY)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_rowconfigure(5, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Title
        title = tk.Label(
            main_container,
            text="Yuload",
            font=StyleManager.default_font(24, bold=True),
            bg=Colors.PRIMARY,
            fg=Colors.ACCENT
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # URL Input Section
        self._create_url_section(main_container)
        
        # Video Info Section
        self.video_info_frame = VideoInfoFrame(
            main_container,
            relief="flat",
            height=100
        )
        self.video_info_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        # Quality Selection Section
        self.quality_selector = QualitySelector(
            main_container,
            on_select=self._on_quality_selected
        )
        self.quality_selector.grid(row=3, column=0, sticky="ew", pady=10)
        
        # Subtitle Selection Section
        self.subtitle_selector = SubtitleSelector(main_container)
        self.subtitle_selector.grid(row=4, column=0, sticky="ew", pady=10)
        
        # Download Section
        self._create_download_section(main_container)
        
        # Status Bar
        self.status_bar = StatusBar(main_container)
        self.status_bar.grid(row=7, column=0, sticky="ew", pady=(20, 0))
    
    def _create_url_section(self, parent):
        """Create URL input section"""
        url_frame = tk.Frame(parent, bg=Colors.PRIMARY)
        url_frame.grid(row=1, column=0, sticky="ew", pady=10)
        url_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        label = tk.Label(
            url_frame,
            text="YouTube URL:",
            font=StyleManager.default_font(10),
            bg=Colors.PRIMARY,
            fg=Colors.TEXT_PRIMARY
        )
        label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Champ de texte pour l'URL (utilise tk.Text au lieu de tk.Entry pour supporter height)
        self.url_entry = tk.Text(
            url_frame,
            font=StyleManager.default_font(10),
            bg=Colors.SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.ACCENT,
            relief="flat",
            bd=0,
            height=2,
            wrap="word"
        )
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=10)
        self.url_entry.bind("<Return>", lambda e: self._on_load_click())
        
        # Charger le bouton
        self.load_button = ModernButton(
            url_frame,
            text="Load Video",
            command=self._on_load_click,
            width=120,
            height=35
        )
        self.load_button.grid(row=0, column=2, padx=10)
    
    def _create_download_section(self, parent):
        """Create download section"""
        download_frame = tk.Frame(parent, bg=Colors.PRIMARY)
        download_frame.grid(row=6, column=0, sticky="ew", pady=15)
        download_frame.grid_columnconfigure(0, weight=1)
        
        # Progress Bar
        self.progress_bar = AnimatedProgressBar(
            download_frame,
            width=600,
            height=8
        )
        self.progress_bar.pack(pady=10, fill="x")
        
        # Progress Label
        self.progress_label = tk.Label(
            download_frame,
            text="0%",
            font=StyleManager.default_font(9),
            bg=Colors.PRIMARY,
            fg=Colors.TEXT_SECONDARY
        )
        self.progress_label.pack(pady=5)
        
        # Buttons Frame
        buttons_frame = tk.Frame(download_frame, bg=Colors.PRIMARY)
        buttons_frame.pack(pady=15, fill="x")
        
        # Download Button
        self.download_button = ModernButton(
            buttons_frame,
            text="Download Video",
            command=self._on_download_click,
            width=200,
            height=45,
            bg_color=Colors.SUCCESS,
            hover_color="#5ed9b8"
        )
        self.download_button.pack(side="left", padx=10)
        
        # Cancel Button (hidden initially)
        self.cancel_button = ModernButton(
            buttons_frame,
            text="Cancel",
            command=self._on_cancel_click,
            width=200,
            height=45,
            bg_color=Colors.ERROR,
            hover_color="#ff5555"
        )
        # Don't pack yet
        
        # Browse Folder Button
        self.folder_button = ModernButton(
            buttons_frame,
            text="📁 Open Folder",
            command=self._on_browse_folder,
            width=150,
            height=45,
            bg_color=Colors.TERTIARY,
            hover_color="#4d4d4d"
        )
        self.folder_button.pack(side="left", padx=5)
    
    def _setup_styles(self):
        """Setup ttk styles"""
        StyleManager.configure_styles(self)
    
    def _set_icon(self):
        """Set window icon if available"""
        try:
            # Try to create a simple icon using PIL if available
            from PIL import Image, ImageDraw
            from io import BytesIO
            
            img = Image.new('RGB', (256, 256), color=Config.ACCENT_COLOR[1:])
            draw = ImageDraw.Draw(img)
            draw.text((50, 100), "Y", fill='white')
            
            photo = tk.PhotoImage(file="/dev/null")
            self.iconphoto(False, photo)
        except Exception:
            pass
    
    def _on_load_click(self):
        """Gère le clic sur le bouton Charger"""
        # Récupérer l'URL depuis Text widget (utiliser "1.0" "end-1c" pour éviter le newline final)
        url = self.url_entry.get("1.0", "end-1c").strip()
        
        if not url:
            self.status_bar.show_message("Veuillez entrer une URL YouTube", "warning")
            return
        
        if not validate_youtube_url(url):
            self.status_bar.show_message("URL YouTube invalide", "error")
            return
        
        self.is_loading = True
        self.load_button.config(state="disabled")
        self.status_bar.show_message("Chargement des informations vidéo...", "info")
        
        # Charger la vidéo dans un thread séparé pour ne pas bloquer l'interface
        threading.Thread(target=self._load_video_thread, args=(url,), daemon=True).start()
    
    def _load_video_thread(self, url: str):
        """Charge la vidéo dans un thread séparé"""
        try:
            video_info = self.youtube_handler.get_video_info(url)
            
            if not video_info:
                self.status_bar.show_message("Failed to load video. Check URL or internet connection.", "error")
                self.is_loading = False
                self.load_button.config(state="normal")
                return
            
            self.current_video_info = video_info
            
            # Update UI
            self.video_info_frame.set_info(video_info)
            self.status_bar.show_message(f"Loaded: {video_info['title']}", "success")
            
            # Get available streams
            streams = self.youtube_handler.get_available_streams()
            if streams:
                self.quality_selector.set_streams(streams)
            
            # Get captions
            captions = self.youtube_handler.get_captions()
            if captions:
                self.subtitle_selector.set_captions(captions)
            
            # Select first quality by default
            if streams:
                first_quality = streams[0]['quality']
                self.quality_selector._select_quality(first_quality)
            
        except Exception as e:
            logger.error(f"Error loading video: {e}")
            self.status_bar.show_message(f"Error: {str(e)}", "error")
        
        finally:
            self.is_loading = False
            self.load_button.config(state="normal")
    
    def _on_quality_selected(self, quality: str):
        """Handle quality selection"""
        self.selected_quality = quality
        logger.info(f"Quality selected: {quality}")
    
    def _on_download_click(self):
        """Handle download button click"""
        if not self.current_video_info:
            self.status_bar.show_message("Please load a video first", "warning")
            return
        
        if not self.selected_quality:
            self.status_bar.show_message("Please select a quality", "warning")
            return
        
        # Ask for output folder
        output_folder = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=str(Config.DOWNLOAD_DIR)
        )
        
        if not output_folder:
            return
        
        # Prepare download parameters
        include_subtitle = self.subtitle_selector.should_include()
        subtitle_code = self.subtitle_selector.get_selected_code() if include_subtitle else None
        
        # Update UI for download
        self.download_button.pack_forget()
        self.cancel_button.pack(side="left", padx=10)
        self.load_button.config(state="disabled")
        self.url_entry.config(state="disabled")
        self.quality_selector.config(state="disabled")
        
        self.status_bar.show_message("Downloading...", "info")
        self.progress_bar.set_progress(0)
        
        # Start download
        self.downloader.download_video(
            quality=self.selected_quality,
            output_path=output_folder,
            include_subtitle=include_subtitle,
            subtitle_code=subtitle_code,
            progress_callback=self._on_progress,
            completion_callback=self._on_download_complete,
            error_callback=self._on_download_error
        )
    
    def _on_cancel_click(self):
        """Handle cancel button click"""
        self.downloader.cancel_download()
        self.status_bar.show_message("Download cancelled", "warning")
        self._reset_download_ui()
    
    def _on_progress(self, current: int, total: int):
        """Handle progress update"""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar.set_progress(progress)
            
            # Update progress label
            self.progress_label.config(
                text=f"{int(progress)}% • {current/1024/1024:.1f}MB / {total/1024/1024:.1f}MB"
            )
            
            # Animate progress bar
            self.progress_bar.draw_progress()
    
    def _on_download_complete(self, filepath: str):
        """Handle download completion"""
        self.progress_bar.set_progress(100)
        self.progress_label.config(text="100% • Download Complete!")
        self.status_bar.show_message(f"Download completed: {Path(filepath).name}", "success")
        
        # Reset UI after 2 seconds
        self.after(2000, self._reset_download_ui)
        
        # Ask if user wants to open folder
        if messagebox.askyesno("Success", "Download completed! Open folder?"):
            self._on_browse_folder()
    
    def _on_download_error(self, error_message: str):
        """Handle download error"""
        self.status_bar.show_message(error_message, "error")
        self._reset_download_ui()
        messagebox.showerror("Download Error", error_message)
    
    def _reset_download_ui(self):
        """Reset download UI to initial state"""
        self.cancel_button.pack_forget()
        self.download_button.pack(side="left", padx=10)
        self.load_button.config(state="normal")
        self.url_entry.config(state="normal")
        self.quality_selector.config(state="normal")
        self.progress_bar.set_progress(0)
        self.progress_label.config(text="0%")
        self.status_bar.show_message("Ready", "info")
    
    def _on_browse_folder(self):
        """Open downloads folder"""
        folder = str(Config.DOWNLOAD_DIR)
        try:
            import subprocess
            import sys
            
            if sys.platform == 'win32':
                subprocess.Popen(f'explorer "{folder}"')
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', folder])
            else:
                subprocess.Popen(['xdg-open', folder])
        except Exception as e:
            logger.error(f"Error opening folder: {e}")
            self.status_bar.show_message("Could not open folder", "error")
