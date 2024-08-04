from pytubefix import YouTube
from pytubefix.cli import on_progress
import unicodedata
import re
import csv

url = input("Video URL: ")
mp3_only = input("Audio Only [yes/no] (no): ").lower()
progressive = True

yt = YouTube(url, on_progress_callback = on_progress)

if mp3_only != "yes":
  ys = yt.streams
  ys = [ x for x in ys if x.type == "video" ]
  ys.sort(key=lambda x: x.resolution, reverse=True)
  ys = ys[0]

  progressive = ys.is_progressive == "True"

  filename = ys.default_filename
  print(f"Title: {ys.title} Highest Resolution:{ys.resolution} Progressive={ys.is_progressive}")

  filename= unicodedata.normalize('NFKD', filename).encode('utf8', 'ignore').decode('utf8')
  filename= re.sub(r'[^\w\s\.-]', '', filename.lower())
  filename= re.sub(r'[-\s]+', '-', filename).strip('-_')

  ys.download(filename = filename)

if not progressive or mp3_only:
  print("Stream is not progressive, downloading the audio separatedly...")
  ya = yt.streams.get_audio_only()
  filename = ya.default_filename
  filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
  filename= re.sub(r'[^\w\s\.-]', '', filename.lower())
  filename= re.sub(r'[-\s]+', '-', filename).strip('-_')
  filename = filename.replace('.mp4', '')

  ya.download(filename = filename,mp3=True)