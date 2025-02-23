# 🎥 Video Cutting & Stacking Automation with FFmpeg 🚀

✨ **Automate your video editing workflow like a pro!** ✨  
This project is designed to **cut long videos into 60-second clips**, **stack videos from two folders (A and B) vertically**, and **retain only the audio from the second video**—all while ensuring flawless encoding to avoid pesky black screen issues. Built with **Python** and powered by **FFmpeg**, it’s your go-to tool for efficient, high-quality video processing. 🎬

---
## 🛠 Installation & Setup

### 1️⃣ **Install FFmpeg**
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system `PATH`.  
- **macOS**: Run `brew install ffmpeg`.  
- **Linux**: Run `sudo apt install ffmpeg`.  

### 2️⃣ **Install Python Dependencies**
Run the following command to install the required Python package:

    pip install ffmpeg-python
---

### **🚀 How to Use**

### 1️⃣ Cutting Videos into 60-Second Clips
Run the cut_videos.py script to process an input video and generate 60-second clips

✅ The clips will be saved in the B folder.
### 2️⃣ Stacking Videos from Folder A & B
Run the stack_videos.py script to combine matching clips from A and B.

✅ The stacked videos will be saved in the C folder.

---

### *⚙️ How It Works*

#### 🎬 Cutting Script
- Splits the input video into 60-second clips.

- Ensures correct encoding (yuv420p, 25 FPS, keyframes).

- Avoids black screen issues by fixing timestamps.

#### 🎥 Stacking Script
- Matches videos from A and B.

- Rescales them to 1080x960 and stacks them vertically.

- Retains only the audio from B.

- Ensures proper encoding to prevent playback issues.

---

#### 📜 License
This project is open-source under the MIT License. Feel free to use, modify, and share! 🎬
