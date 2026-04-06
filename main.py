"""
Yuload - YouTube Video Downloader Application Entry Point
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from yuload.utils.config import Config
from yuload.utils.logger import setup_logger
from yuload.ui.main_window import MainWindow

logger = setup_logger(__name__)


def main():
    """Start the Yuload application"""
    try:
        logger.info("Starting Yuload application...")
        
        # Initialize configuration
        Config.init_directories()
        
        # Create and run main window
        app = MainWindow()
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
