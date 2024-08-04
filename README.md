# YT video dowload scripts
## install

1. Install [Python 3.9 or higher](https://www.python.org/downloads/)
2. Install the [ffmpeg tool](https://www.ffmpeg.org/download.html) for your platform
3. Install requirements:
```
pip install -r requirements.txt
``` 
3. Copy the scripts to the folder you want to download files to
   
## yt.py

Will request the video URL. You can use the URL in the browser input field, or any or the ones provided by YT like when pressing YT, or when right clicking on the video and using one of the "Copy URL" options.

It will also ask if you want only the audio, in which case only an mp3 will be provided, at the highest available bit rate.

The video stream of highest resolution will be downloaded. Sometimes that video is not in progressive video format and the resulting MP4 will not contain an audio stream. In that case the scritp will also download the audio in an MP3, resulting in two files being downloaded, one with the video and one with the audio. In those cases use the  `merge.ps1` script to produce a complete file with video and audio.

If the video description conforms to the following format:

```
<start> - <end> - <title>
```

For example:

```
1:00 - 1:30 - Billie Jean - Michael Jackson
```
    *Start and end must be time expressed in `HH:MM:SS.000` format, the hours and miliseconds being optional. In the example above, the time period expressed is that between one minute and one minute and thirty seconds.*

An aditional file containing the information of the first three fields in CSV format will be produced. **Notice** that each line can contain other elements after the third one using the `-` as delimiter. Those extra columns will be ignored.If the video's description does not follow the format, the chapter information can be also created manually in a CSV format with a header line `start,end,song` with any text editor, and naming it with the same base name of the MP4 file and `.csv`extension will be directly used by the `split_video.ps1` script as explained in the next chapter.

## merge.ps1

To merge video and audio run the `merge.ps1` script from a Windows PowerShell command line witht the `-file` parameter indicating the `.mp4` file name. This only needs to be done for non-progressive videos, if the `yt.py` script produced separate `.mp4` and `.mp3` files.

```
./merge.ps1 -file yt-video-test.mp4
```
## split_video.ps1

This is a PowerShell script that has to be run from a Windows PowerShell command line. It will take a MP4 file and CSV file by the same base name, and split the video in separate files, one for each chapter declared in the CSV file. Each file will be named by the value of the third field, replacing spaces by dashes. In the example used in a previous chapter, an MP4 file named `Billie_Jean.mp4` would be produced, discarding all the other footage of the video except that between 1:00 and 1:30 time.
