from pytube import YouTube
from re import sub
import ffmpeg
import sys
import subprocess
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ytytyt.py [arguments]")
        sys.exit(1)
        

def slugify_filename(name):
    name = name.lower().strip()
    name = sub(r'[^\w\s-]', '', name)
    name = sub(r'[\s_-]+', '-', name)
    name = sub(r'^-+|-+$', '', name)
    if not name:
        name = 'untitled'

    return name 


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

args = sys.argv[1:]
url = args[0]
print(url)

yt = YouTube(url)
title = slugify_filename(yt.streams[0].title)

video_folder = "/Users/simonclynes/Documents/ytytyt/vids/"
clip_folder = "/Users/simonclynes/Documents/ytytyt/vids/clips/"

yt.streams.filter(progressive=True,file_extension='mp4').first().download(filename=video_folder+title+'.mp4')
optimize_video_for_twitter(video_folder+title+'.mp4', video_folder+title+'_x.mp4')
os.remove(video_folder+title+'.mp4')

if len(sys.argv) > 3:
    start = str(sys.argv[2])
    end = str(sys.argv[3])
    ffmpeg.input(video_folder+title+'_x.mp4', ss=start, to=end).output(clip_folder+title+'_clip.mp4').run()
    #optimize_video_for_twitter(clip_folder+title+'_clip.mp4', clip_folder+title+'_clipx.mp4')
    os.remove(clip_folder+title+'_clip.mp4')

os.system(f'open "{video_folder}"')