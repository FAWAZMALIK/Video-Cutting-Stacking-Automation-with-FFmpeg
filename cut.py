import os
import subprocess
import re

def get_video_duration(input_video):
    """Get the total duration of the video in seconds using FFmpeg."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", input_video], stderr=subprocess.PIPE, text=True
        )
        match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
        if match:
            h, m, s = map(float, match.groups())
            return int(h * 3600 + m * 60 + s)
    except Exception as e:
        print(f"❌ Error getting video duration: {e}")
    return 0

def ensure_directory(directory):
    """Ensure output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_and_encode_video(input_video, output_folder, clip_duration=60):
    """Splits a video into clips and ensures proper encoding."""
    ensure_directory(output_folder)
    
    total_duration = get_video_duration(input_video)
    if total_duration == 0:
        print("❌ Error: Unable to determine video duration.")
        return

    print(f"📌 Video duration: {total_duration} seconds. Checking for existing clips...")

    existing_clips = {f for f in os.listdir(output_folder) if f.startswith("clip_") and f.endswith(".mp4")}
    
    for start_time in range(0, total_duration, clip_duration):
        clip_num = start_time // clip_duration + 1
        output_file = os.path.join(output_folder, f"clip_{clip_num}.mp4")

        if f"clip_{clip_num}.mp4" in existing_clips:
            print(f"⏩ Skipping existing clip: {output_file}")
            continue

        ffmpeg_cmd = [
            "ffmpeg", "-i", input_video, "-ss", str(start_time), "-t", str(clip_duration),
            "-vf", "scale=1080:960,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "30", "-r", "25",  
            "-vsync", "1", "-start_at_zero", 
            "-crf", "21", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-y", output_file
        ]

        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Created clip: {output_file}")

# === USAGE ===
input_video_path = "VideoName.mp4"  # Change this to your video file
output_folder = "output"  # Output folder for clips

split_and_encode_video(input_video_path, output_folder)
