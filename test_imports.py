#!/usr/bin/env python3
"""Test script to verify Yuload installation and imports"""

import sys
from pathlib import Path

def test_imports():
    """Test all module imports"""
    print("Testing Yuload module imports...\n")
    
    tests = [
        ("Config", "from yuload.utils.config import Config"),
        ("Logger", "from yuload.utils.logger import setup_logger"),
        ("Validators", "from yuload.utils.validators import validate_youtube_url"),
        ("YouTubeHandler", "from yuload.core.youtube_handler import YouTubeHandler"),
        ("Downloader", "from yuload.core.downloader import Downloader"),
        ("Styles", "from yuload.ui.styles import StyleManager"),
        ("Widgets", "from yuload.ui.widgets import ModernButton"),
        ("MainWindow", "from yuload.ui.main_window import MainWindow"),
    ]
    
    failed = []
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"✓ {name:20s} - OK")
        except Exception as e:
            print(f"✗ {name:20s} - FAILED: {str(e)}")
            failed.append((name, str(e)))
    
    print("\n" + "="*50)
    
    if failed:
        print(f"\n❌ {len(failed)} imports failed:\n")
        for name, error in failed:
            print(f"  {name}: {error}")
        return False
    else:
        print("\n✅ All imports successful!")
        print("\nYuload is ready to run!")
        print("Start the application with:")
        print("  python3 main.py")
        return True

def check_environment():
    """Check Python environment"""
    print("Python Environment Check")
    print("="*50)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    print()

if __name__ == "__main__":
    check_environment()
    success = test_imports()
    sys.exit(0 if success else 1)
