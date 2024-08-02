python yt.py

$mp4_files = Get-ChildItem -Filter *.mp4
$mp4_name = $mp4_files[0].Name

$mp3_files = Get-ChildItem -Filter *.mp3
$mp3_name = $mp3_files[0].Name

$csv_files = Get-ChildItem -Filter *.csv
$chapters_name = $csv_files[0].Name

$output_name = $mp4_name.replace('.mp4','_aud.mp4')

Write-Host "ffmpeg -i $mp3_name -i $mp4_name -c:v copy -c:a aac $output_name"

$chapters = Import-Csv -Path $chapters_name | Select-Object -Skip 1 | Foreach-Object {
  $start = $_.start
  $end = $_.end
  $song = ("{0}.mp4" -f $_.song)
  Write-Host "ffmpeg -y -i $output_name -avoid_negative_ts make_zero -fflags +genpts -ss $start -to $end -c:a aac $song"
}


