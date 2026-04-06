#!/usr/bin/env python3
"""Test FFmpeg merge with actual video/audio files"""

import subprocess
import tempfile
from pathlib import Path
import sys

def create_test_video(ffmpeg_exe, filepath, duration=1):
    """Create a test video file using FFmpeg"""
    cmd = [
        ffmpeg_exe,
        "-f", "lavfi",
        "-i", f"color=c=blue:s=320x240:d={duration}",
        "-f", "lavfi",
        "-i", f"sine=f=1000:d={duration}",
        "-pix_fmt", "yuv420p",
        str(filepath),
        "-y"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.returncode == 0

def create_test_audio(ffmpeg_exe, filepath, duration=1):
    """Create a test audio file using FFmpeg"""
    cmd = [
        ffmpeg_exe,
        "-f", "lavfi",
        "-i", f"sine=f=1000:d={duration}",
        str(filepath),
        "-y"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.returncode == 0

def test_ffmpeg_merge():
    """Test FFmpeg merge of video and audio"""
    try:
        import imageio_ffmpeg as ffmpeg
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
        print(f"Using FFmpeg: {ffmpeg_exe}\n")
    except Exception as e:
        print(f"✗ Failed to get FFmpeg: {e}")
        return False
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        video_file = tmpdir / "test_video.mp4"
        audio_file = tmpdir / "test_audio.mp4"
        output_file = tmpdir / "test_merged.mp4"
        
        print("Creating test files...")
        
        # Create test video
        print(f"  Creating test video: {video_file.name}")
        if not create_test_video(ffmpeg_exe, video_file, duration=2):
            print("✗ Failed to create test video")
            return False
        
        # Create test audio
        print(f"  Creating test audio: {audio_file.name}")
        if not create_test_audio(ffmpeg_exe, audio_file, duration=2):
            print("✗ Failed to create test audio")
            return False
        
        print(f"\nVideo file: {video_file} ({video_file.stat().st_size} bytes)")
        print(f"Audio file: {audio_file} ({audio_file.stat().st_size} bytes)\n")
        
        # Test FFmpeg merge
        print("Testing FFmpeg merge with '-c copy'...")
        cmd = [
            ffmpeg_exe,
            "-i", str(video_file),
            "-i", str(audio_file),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_file),
            "-y"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✓ Merge successful!")
            print(f"  Output file: {output_file.name}")
            print(f"  Output size: {output_file.stat().st_size} bytes")
            
            # Verify output has both video and audio
            print("\nVerifying output has video and audio streams...")
            probe_cmd = [
                ffmpeg_exe,
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0",
                str(output_file)
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if "video" in probe_result.stdout:
                print("✓ Output has video stream")
            
            probe_cmd[4] = "a:0"
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if "audio" in probe_result.stdout:
                print("✓ Output has audio stream")
            
            return True
        else:
            print(f"✗ Merge failed!")
            print(f"Error output:\n{result.stderr}")
            return False

def main():
    print("=" * 60)
    print("FFmpeg Merge Test")
    print("=" * 60)
    print()
    
    success = test_ffmpeg_merge()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ FFmpeg merge test PASSED")
        return 0
    else:
        print("✗ FFmpeg merge test FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
