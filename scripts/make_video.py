#!/usr/bin/env python3
"""make_video · ffmpeg视频合成 — 改SLIDES, IMG_DIR, AUDIO_DIR, OUTPUT_FINAL即可"""
import os, subprocess

# ═══ 每次改这里 ═══
SLIDES       = 12
IMG_DIR      = "/tmp/ppt_slides"
AUDIO_DIR    = "/tmp/ppt_audio"
OUTPUT_FINAL = "/tmp/event_radar_video.mp4"
# ═══════════════════

FFMPEG = os.path.expanduser("~/.local/lib/python3.12/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")

def get_duration(wav_path):
    r = subprocess.run([FFMPEG, "-i", wav_path, "-f", "null", "-"], capture_output=True, text=True)
    for line in r.stderr.split("\n"):
        if "time=" in line:
            hms = line.strip().split("time=")[-1].split()[0].split(":")
            return float(hms[0])*3600 + float(hms[1])*60 + float(hms[2])
    return 5.0

# Step 1: 获取每个slide的配音时长
durations = []
for i in range(1, SLIDES+1):
    d = get_duration(f"{AUDIO_DIR}/slide_{i:02d}.wav")
    durations.append(d)
    print(f"  Slide {i}: {d:.1f}s")
print(f"\n总时长: {sum(durations):.1f}s")

# Step 2: 逐页渲染（图片+配音+Ken Burns缩放）
lines = []
for i in range(1, SLIDES+1):
    img = f"{IMG_DIR}/slide_{i:02d}.png"
    wav = f"{AUDIO_DIR}/slide_{i:02d}.wav"
    out = f"/tmp/clip_{i:02d}.mp4"
    dur = durations[i-1]
    print(f"  Rendering slide {i} ({dur:.1f}s)...")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", img, "-i", wav,
        "-vf", f"scale=1920*1.008:1080*1.008,zoompan=z='min(zoom+0.008/{dur:.3f},1.008)':d={int(dur*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,fps=25",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",           # 🚨 必要！否则播放器黑屏
        "-c:a", "aac", "-b:a", "128k", "-shortest", out
    ], check=True, capture_output=True)
    lines.append(f"file '{out}'")

# Step 3: 拼接
concat = "/tmp/concat_video.txt"
with open(concat, "w") as f:
    f.write("\n".join(lines))
print("Concat...")
subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", "/tmp/raw_video.mp4"], check=True)

# Step 4: 最终压缩到720p
print("Final compression...")
subprocess.run([
    FFMPEG, "-y", "-i", "/tmp/raw_video.mp4",
    "-vf", "scale=1280:720",
    "-c:v", "libx264", "-preset", "medium", "-crf", "23",
    "-pix_fmt", "yuv420p",               # 🚨 必要！保证播放器兼容
    "-c:a", "aac", "-b:a", "96k",
    "-movflags", "+faststart", OUTPUT_FINAL
], check=True)

size = os.path.getsize(OUTPUT_FINAL) / 1024
print(f"\n✅ 完成: {OUTPUT_FINAL} ({size:.0f} KB / {size/1024:.1f} MB)")

# 清理
for i in range(1, SLIDES+1):
    os.remove(f"/tmp/clip_{i:02d}.mp4")
os.remove(concat)
