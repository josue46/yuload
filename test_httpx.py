#!/usr/bin/env python3
"""Test httpx and dependencies"""

try:
    import httpx
    print("✓ httpx imported successfully")
except ImportError as e:
    print(f"✗ Failed to import httpx: {e}")
    exit(1)

try:
    from yuload.utils.http import HTTPClient, get_http_client
    print("✓ HTTPClient module loaded")
except ImportError as e:
    print(f"✗ Failed to import HTTPClient: {e}")
    exit(1)

try:
    from yuload.utils.config import Config
    from yuload.core.youtube_handler import YouTubeHandler
    from yuload.ui.main_window import MainWindow
    print("✓ All Yuload modules imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Yuload modules: {e}")
    exit(1)

print("\n✓ Dependencies configured for uv successfully!")
print("✓ Ready to run: python3 main.py")
