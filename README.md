# 🎬 Yuload - YouTube Video Downloader

A modern, professional YouTube video downloader with a sleek GUI built with Tkinter. Download videos in multiple qualities, with optional subtitle support, all from an elegant interface.

## ✨ Features

- 🎥 **Download YouTube Videos** - Download any public YouTube video with a simple URL paste
- 🎯 **Multiple Quality Options** - Choose from all available video qualities (1080p, 720p, 480p, 360p, 144p, etc.)
- 🔊 **Audio Integration** - Automatic video and audio merging for complete download
- 📝 **Subtitle Support** - Download and include video subtitles in multiple languages
- 📊 **Progress Tracking** - Animated progress bar with real-time download statistics
- 🎨 **Modern UI** - Professional, modern interface with dark theme and smooth animations
- 🛡️ **Error Handling** - Comprehensive error handling with user-friendly messages
- 📁 **Easy Access** - Quick access to downloaded files from the application

## 🏗️ Architecture

The application follows a modular, scalable architecture:

```
yuload/
├── core/                      # Business logic
│   ├── youtube_handler.py    # YouTube API interactions
│   └── downloader.py         # Download management
├── ui/                        # User Interface
│   ├── main_window.py        # Main application window
│   ├── widgets.py            # Custom UI components
│   └── styles.py             # Theme and styling
└── utils/                     # Utilities
    ├── config.py             # Configuration management
    ├── logger.py             # Logging setup
    └── validators.py         # Input validation
```

## 📋 Requirements

- Python 3.9+ (required by pytubefix)
- Tkinter (usually included with Python)
- FFmpeg (for audio merging - optional, falls back to video-only if not available)

## 🚀 Installation

### 1. Clone or Download the Project
```bash
cd /path/to/yuload
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or with poetry:
```bash
poetry install
```

### 4. Install FFmpeg (Optional but Recommended)

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## 🎯 Usage

### Start the Application
```bash
python main.py
```

### How to Use
1. **Paste YouTube URL** - Copy any YouTube video URL and paste it in the URL field
2. **Load Video** - Click "Load Video" to fetch video information and available qualities
3. **Select Quality** - Choose your preferred video quality
4. **Subtitle Options** - Optionally select subtitles if available
5. **Download** - Click "Download Video" and select your preferred folder
6. **Access Downloads** - Click "📁 Open Folder" to quickly access downloaded files

## ⚙️ Configuration

Configuration can be modified in `yuload/utils/config.py`:

- **Default Download Location**: `~/.yuload/downloads`
- **Window Size**: `900x700` (minimum `600x400`)
- **Theme Colors**: Modern dark theme with accent colors
- **Maximum Retries**: 3
- **Chunk Size**: 1MB

## 🏆 Key Components

### YouTubeHandler
Manages all interactions with YouTube:
- Video information retrieval
- Stream availability checking
- Subtitle/caption management

### Downloader
Handles the download process:
- Multi-threaded downloads
- Progress tracking
- Video/audio merging
- Subtitle downloading

### Main UI
Professional interface featuring:
- URL input with validation
- Video information display
- Quality selector with file size info
- Subtitle selector
- Animated progress bar
- Status messages
- Real-time feedback

## 🎨 Design Features

- **Modern Dark Theme** - Easy on the eyes with professional colors
- **Smooth Animations** - Animated progress bar and hover effects
- **Responsive Layout** - Adapts to window resizing
- **Professional Buttons** - Custom modern buttons with hover states
- **Clear Information** - Video metadata clearly displayed
- **Intuitive Controls** - Logical workflow and clear visual hierarchy

## 🐛 Troubleshooting

### "Invalid YouTube URL"
- Ensure you're using a valid YouTube URL
- URLs should start with `youtube.com` or `youtu.be`

### "Cannot find streams"
- Video might be age-restricted or unavailable
- Check your internet connection
- Try a different video

### "Download fails at merge"
- FFmpeg is not installed (optional - app falls back to video-only)
- Install FFmpeg for full functionality

### Progress bar not updating
- Normal for large files - progress is updated in 1MB chunks
- Download is still in progress in the background

## 📊 Logging

Logs are saved to `~/.yuload/logs/` with:
- Daily log files
- 10MB file rotation
- Detailed error information
- Debug information for troubleshooting

## 🔧 Development

### Code Structure
- **Modular Design**: Each component has a single responsibility
- **Error Handling**: Comprehensive try-catch with proper logging
- **Type Hints**: Full type annotations for better IDE support
- **Documentation**: Detailed docstrings for all functions

### Running in Development Mode
```bash
source .venv/bin/activate
python main.py
```

### Extending the Application
- Add new quality filters in `youtube_handler.py`
- Create new UI widgets by extending `widgets.py`
- Add configuration options in `config.py`

## 📄 License

This project is provided as-is for personal use.

## ⚠️ Disclaimer

Yuload is designed for downloading videos you have permission to download. Respect copyright laws and YouTube's Terms of Service. The authors are not responsible for misuse of this tool.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Optimize code

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `~/.yuload/logs/`
3. Verify FFmpeg installation
4. Check your internet connection

---

**Enjoy downloading videos with Yuload!** 🎉