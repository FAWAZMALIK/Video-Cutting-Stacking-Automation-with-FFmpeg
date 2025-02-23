import os
import subprocess

# Define folder paths
folder_A = "A"  # First set of clips
folder_B = "B"  # Second set of clips (from cut videos)
folder_C = "C"  # Output folder

os.makedirs(folder_C, exist_ok=True)

videos_A = sorted([f for f in os.listdir(folder_A) if f.endswith(('.mp4', '.mov', '.avi'))])
videos_B = sorted([f for f in os.listdir(folder_B) if f.endswith(('.mp4', '.mov', '.avi'))])

for i, video_a in enumerate(videos_A):
    if i >= len(videos_B):
        print("⚠️ No more matching clips in Folder B. Stopping.")
        break
    
    video_b = videos_B[i]

    input_A = os.path.join(folder_A, video_a)
    input_B = os.path.join(folder_B, video_b)
    temp_A = os.path.join(folder_C, f"temp_A_{i+1}.mp4")
    temp_B = os.path.join(folder_C, f"temp_B_{i+1}.mp4")
    output_C = os.path.join(folder_C, f"stacked_{i+1}.mp4")

    # Step 1: Re-encode both clips to ensure compatibility
    for input_file, temp_file in [(input_A, temp_A), (input_B, temp_B)]:
        ffmpeg_reencode_cmd = [
            "ffmpeg", "-i", input_file, 
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25", "-crf", "21", "-preset", "fast",
            "-vsync", "1", "-start_at_zero",  
            "-c:a", "aac", "-b:a", "128k", "-y", temp_file
        ]
        subprocess.run(ffmpeg_reencode_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step 2: Stack the re-encoded videos
    ffmpeg_stack_cmd = [
        "ffmpeg", "-i", temp_A, "-i", temp_B,
        "-filter_complex",
        "[0:v]scale=1080:960,format=yuv420p,setpts=PTS-STARTPTS[v0];"
        "[1:v]scale=1080:960,format=yuv420p,setpts=PTS-STARTPTS[v1];"
        "[v0][v1]vstack[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "21", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-y", output_C
    ]

    subprocess.run(ffmpeg_stack_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Processed: {video_a} + {video_b} → {output_C}")

print("✅ All videos stacked successfully!")
