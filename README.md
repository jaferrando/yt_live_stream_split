# PITUBEFIX TEMPORARY BUG WORK AROUND

The library we use to download from YT (pytubefix) is experiencing a bug that makes downloads fail with an error saying the video is unavailable. This happens for example for videos that where produced from a Live Stream. In this particular case of Live Stream videos and until pytubefix fixes the bug, use the following workaround:

Run this command to locate where pytubefix is installed:

```
pip list -v
```
Find pytubefix in the list:
```
Package            Version  Location                                                                        Installer
------------------ -------- ------------------------------------------------------------------------------- ---------
pytubefix          7.1rc1   C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Lib\site-packages pip
```

Go to the route and to the `pytubefix` directory in it. Then open the `__main__.py` file with a text editor:
Find the text `LIVE_STREAM` on line 372, then remove or comment line 373 and add in it place the command `pass` resulting in this section of code:

```
            elif status == 'LIVE_STREAM':
                pass
                # raise exceptions.LiveStreamError(video_id=self.video_id)
```

This solves the issue at least for Live Stream videos

# YT video dowload and split scripts
## install

1. Install [Python 3.9 or higher](https://www.python.org/downloads/)
2. (ONLY to download videos, if only MP3 is wanted skip this) Install the [ffmpeg tool](https://www.ffmpeg.org/download.html) for your platform
3. Install requirements:
```
pip install -r requirements.txt
``` 
3. Copy the scripts to the folder you want to download files to
   
## yt.py

Will request the video URL. You can use the URL in the browser input field, or any or the ones provided by YT like when pressing YT, or when right clicking on the video and using one of the "Copy URL" options.

It will also ask if you want only the audio, in which case only an mp3 will be provided, at the highest available bit rate.

The video stream of highest resolution will be downloaded. Sometimes that video is not in progressive video format and the resulting MP4 will not contain an audio stream. In that case the script will also download the audio in an MP3, resulting in two files being downloaded, one with the video and one with the audio. Then the script will try to run the `merge.ps1` Microsoft Powershell script to merge both into a single video file that will have the `_mix` suffix.

If the video description in YT contains lines that conform to the following format, they will be takes as the video index. Other lines that do not have this format are ignored, so thre can be anything written before, after or in between the index lines:

```
<start> - <end> - <title>
```

For example:

```
1:00 - 1:30 - Billie Jean - Michael Jackson
```

*Start and end must be time expressed in `HH:MM:SS.000` format, the hours and miliseconds being optional. In the example above, the time period expressed is that between one minute and one minute and thirty seconds. The time format is quite permissive and will understand `1:30` as minute 1 and 30 seconds, and also `1:3:1` as hour one, minute three and one second.*

An aditional file containing the information of the first three fields in CSV format will be produced. **Notice** that each line can contain other elements after the third one using the `-` as delimiter. Those extra columns will be ignored.If the video's description does not follow the format, the chapter information can be also created manually in a CSV format with a header line `start,end,song` with any text editor, and naming it with the same base name of the MP4 file and `.csv`extension will be directly used by the `split_video.ps1` script as explained in the next chapter.

The output will include the description of the file as found in YT, and progress indication of each download and of the video-audio merging process if required.

Sample execution:

```
PS C:\Users\jaferrando\jam> python .\yt.py
Video URL: https://www.youtube.com/watch?v=qyltRTowCBY
Audio Only [yes/no] (no):
Title: Jam Oviedo 2.0 31-7-2024 Javi Queen Highest Resolution:720p Progressive=False
1:44    - 4:40    - Caperucita Feroz                 - Orquesta Mondragón
6:22    - 9:50    - I Want To Break Free             - Queen
11:34   - 16:06   - I Just Want To Make Love To You  - Etta James
18:36   - 21:00   - A Little Less Conversation       - Elvis Presley
24:09   - 27:36   - Bien Por Ti                      - Viva Suecia
29:30   - 33:05   - Who Can It Be Now                - Men At Work
35:45   - 41:00   - Just a Gigolo                    - David Lee Roth
45:36   - 50:10   - Zombie                           - The Cranberries
52:49   - 59:10   - Edge Of Seventeen                - Stevie Nicks
1:01:03 - 1:06:10 - Reinas De La Noche               - Burning
1:08:00 - 1:12:45 - Losing My Religion               - REM
1:15:18 - 1:20:50 - So Lonely                        - The Police
1:23:15 - 1:27:35 - Everlong                         - Foofigters
1:30:15 - 1:35:30 - I Drink Alone                    - George T&TD
1:37:48 - 1:42:30 - Dont Stop Believin               - Journey
1:45:19 - 1:49:30 - Greased Lightning                - BSO Grease
1:50:38 - 1:57:30 - Confortably Numb                 - Pink Floyd
1:59:15 - 2:03:15 - Can I Play With Madness          - Iron Maiden
2:05:00 - 2:09:15 - Pain                             - Marcus King
2:11:00 - 2:14:55 - Misery Business                  - Paramore
2:17:54 - 2:23:00 - Hammer To Fall                   - Queen
2:27:20 - 2:36:40 - Hot Stuff                        - Donna Summers
2:38:49 - 2:43:30 - Whats Next To The Moon           - AC/DC
2:45:45 - 2:50:50 - Ghost Riders In The Sky          - Blues Brothers
2:52:19 - 2:59:20 - Smoke On The Water               - Deep Purple
2:59:46 - 3:01:30 - Cumpleaños Feliz Claudia                     - .
3:01:36 - 3:05:25 - Breaking The Law                 - Judas Priest
Stream is not progressive, downloading the audio separatedly...
Merging video and audio file into output:jam-oviedo-20-31-7-2024-javi-queen_mix.mp4
This may take some time. Do not interrupt the process...
File 'jam-oviedo-20-31-7-2024-javi-queen_mix.mp4' already exists. Overwrite? [y/N] y
size= 3111005KiB time=03:05:53.63 bitrate=2284.9kbits/s speed=28.2x
```

## merge.ps1

To merge video and audio run the `merge.ps1` script from a Windows PowerShell command line witht the `-file` parameter indicating the `.mp4` file name. This only needs to be done for non-progressive videos, if the `yt.py` script produced separate `.mp4` and `.mp3` files it will try to run this script automatically.

```
./merge.ps1 -file yt-video-test.mp4
```

The script will produce a new file with the  `_mix` suffix in the name (f.e. `yt-video-test_mix.mp4`)

## split_video.ps1

This is a PowerShell script that has to be run from a Windows PowerShell command line. It will take a MP4 file and CSV file by the same base name, and split the video in separate files, one for each chapter declared in the CSV file. Each file will be named by the value of the third field, replacing spaces by dashes. In the example used in a previous chapter, an MP4 file named `Billie_Jean.mp4` would be produced, discarding all the other footage of the video except that between 1:00 and 1:30 time.

You can provide a file with the `_mix` suffix if that is what the `yt.py` script produced as result of merging video and audio, and it will use the CSV of the file without the `_mix` as produced by the `yt.py` script.

```
./split_video.ps1 -file jam-oviedo-20-31-7-2024-javi-queen_mix.mp4
```

