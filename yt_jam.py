from pytubefix import YouTube
from pytubefix.cli import on_progress
import unicodedata
import re
import csv

url = input("Video URL: ")
 
yt = YouTube(url, on_progress_callback = on_progress)

ys = yt.streams.get_highest_resolution(progressive=False)

filename = ys.default_filename
print(ys.title)
filename= unicodedata.normalize('NFKD', filename).encode('utf8', 'ignore').decode('utf8')
filename= re.sub(r'[^\w\s\.-]', '', filename.lower())
filename= re.sub(r'[-\s]+', '-', filename).strip('-_')

description = yt.description
with open(filename.replace('.mp4','.csv'), 'w', newline='') as file:
  writer = csv.writer(file)
  field = ["start","end","song"]
  writer.writerow(field)
  for l in description.split('\n'):
    cols = l.split('-')
    start = cols[0].strip()
    end = cols[1].strip()
    song = cols[2].strip().replace(' ','_')
    band = cols[3].strip()
    writer.writerow([start,end,song])

ys.download(filename = filename)

ya = yt.streams.get_audio_only()
filename = ya.default_filename
filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
filename= re.sub(r'[^\w\s\.-]', '', filename.lower())
filename= re.sub(r'[-\s]+', '-', filename).strip('-_')
filename = filename.replace('.mp4', '')

ya.download(filename = filename,mp3=True)