#!/usr/bin/env python3
"""Test script to verify FFmpeg merge logic"""

import subprocess
import tempfile
from pathlib import Path
import sys

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_ffmpeg_available():
    """Test if FFmpeg is available"""
    try:
        import imageio_ffmpeg as ffmpeg
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
        print(f"✓ FFmpeg found: {ffmpeg_exe}")
        
        # Test FFmpeg version
        result = subprocess.run(
            [ffmpeg_exe, "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg version: {version_line}")
            return True
        else:
            print(f"✗ FFmpeg execution failed: {result.stderr}")
            return False
    except ImportError:
        print("✗ imageio-ffmpeg not installed")
        return False
    except Exception as e:
        print(f"✗ Error testing FFmpeg: {e}")
        return False


def test_imports():
    """Test all required imports"""
    try:
        from yuload.core.downloader import Downloader
        from yuload.core.youtube_handler import YouTubeHandler
        from yuload.utils.config import Config
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


def test_config():
    """Test Config settings"""
    try:
        from yuload.utils.config import Config
        
        print(f"✓ Config.TEMP_DIR: {Config.TEMP_DIR}")
        print(f"✓ Config.SYSTEM_PLATFORM: {Config.SYSTEM_PLATFORM}")
        print(f"✓ Config.IS_WINDOWS: {Config.IS_WINDOWS}")
        print(f"✓ Config.IS_LINUX: {Config.IS_LINUX}")
        print(f"✓ Config.USE_FFMPEG_MERGE: {Config.USE_FFMPEG_MERGE}")
        print(f"✓ Config.FFMPEG_PRESET: {Config.FFMPEG_PRESET}")
        
        # Ensure temp dir exists
        Config.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✓ TEMP_DIR exists/created: {Config.TEMP_DIR}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Yuload FFmpeg Integration Tests")
    print("=" * 60)
    
    tests = [
        ("FFmpeg Availability", test_ffmpeg_available),
        ("Module Imports", test_imports),
        ("Config Settings", test_config),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r for _, r in results)
    print("\n" + ("✓ All tests passed!" if all_passed else "✗ Some tests failed"))
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
