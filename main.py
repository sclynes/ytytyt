from pytube import YouTube
import ffmpeg
import sys
import subprocess
import os

def optimize_video_for_twitter(input_file, output_file):
    try:
        command = [
            "ffmpeg",
            "-i", input_file,
            "-vf", "scale=w=1920:h=trunc(ow/a/2)*2",
            "-r", "30",
            "-b:v", "5M",
            "-maxrate", "5M",
            "-bufsize", "10M",
            "-vcodec", "libx264",
            "-preset", "slow",
            "-profile:v", "high",
            "-level", "4.0",
            "-acodec", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            output_file
        ]

        subprocess.run(command, check=True)
        print(f"Video successfully optimized and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during video processing: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure it is installed and in your PATH.")

if len(sys.argv) < 2:
    print("Please provide a url")
    sys.exit(1)

url = str(sys.argv[1])

yt = YouTube(url)
title = yt.streams[0].title

yt.streams.filter(progressive=True,file_extension='mp4').first().download(filename=title+'.mp4')
optimize_video_for_twitter(title+'.mp4', title+'_x.mp4')

if len(sys.argv) > 3:
    start = str(sys.argv[2])
    end = str(sys.argv[3])
    ffmpeg.input(title+'.mp4', ss=start, to=end).output(title+'_clip.mp4').run()
    optimize_video_for_twitter(title+'_clip.mp4', title+'_clipx.mp4')

os.remove(title+'.mp4')
os.remove(title+'_clip.mp4')