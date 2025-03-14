from pytubefix import YouTube
from pytubefix import exceptions
from pytubefix.cli import on_progress
import unicodedata
import re
import csv
import subprocess

def parse_description(description):
  print(description)
  data = []
  try:
    for l in description.split('\n'):
      if re.match('\s*[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}.*$', l):
        cols = l.split('-')
        start_val = cols[0].strip()
        end_val = cols[1].strip()
        song_val = cols[2].strip().replace(' ','_')
        item = [start_val,end_val,song_val]
        data.append(item)
    return data
  except Exception as err:
    print("Video description does not comply with format. No chapters data is being produced for split.")
    print(str(err))
    return None

def run_ps(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], stdout=subprocess.PIPE)
    return completed

def main():
  url = input("Video URL: ")
  mp3_only = input("Audio Only [yes/no] (no): ").lower()
  progressive = True

  yt = YouTube(url, on_progress_callback = on_progress, use_po_token=True)

  if mp3_only != "yes":
    try:
      ys = yt.streams
    except exceptions.UnknownVideoError as ex:
      if ex.reason == 'This live event has ended.':
        print('Video is not available yet. Live stream videos take hours to be available')
        exit()
      else:
        raise ex
    ys = [ x for x in ys if x.type == "video" ]
    ys.sort(key=lambda x: int(x.resolution[:-1]), reverse=True)
    ys = ys[0]

    progressive = ys.is_progressive == "True"
  
    filename = ys.default_filename
    print(f"Title: {ys.title} Highest Resolution:{ys.resolution} Progressive={ys.is_progressive}")

    filename= unicodedata.normalize('NFKD', filename).encode('utf8', 'ignore').decode('utf8')
    filename= re.sub(r'[^\w\s\.-]', '', filename.lower())
    filename= re.sub(r'[-\s]+', '-', filename).strip('-_')

    ys.download(filename = filename)

    description = yt.description
    data = parse_description(description)
    if data:
      with open(filename.replace('.mp4','.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["start","end","song"]
        writer.writerow(field)
        for l in data:
          writer.writerow(l)

  if not progressive or mp3_only:
    print("Stream is not progressive, downloading the audio separatedly...")
    ya = yt.streams.get_audio_only()
    audio_filename = ya.default_filename
    audio_filename = unicodedata.normalize('NFKD', audio_filename).encode('ascii', 'ignore').decode('ascii')
    audio_filename= re.sub(r'[^\w\s\.-]', '', audio_filename.lower())
    audio_filename= re.sub(r'[-\s]+', '-', audio_filename).strip('-_')
    audio_filename = audio_filename.replace('.mp4', '')

    ya.download(filename = audio_filename) #,mp3=True)

  if not progressive:
    print("Merging video and audio file into output:"+filename.replace(".mp4","_mix.mp4"))
    print("This may take some time. Do not interrupt the process...")
    run_ps(cmd = f'./merge.ps1 -file {filename}')

if __name__ == '__main__':
  main()