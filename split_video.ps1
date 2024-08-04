param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$name = $mp4_file.Basename

$mp3_name = "{0}.mp3" -f $name
$chapters_name = "{0}.csv" -f $name

$chapters = Import-Csv -Path $chapters_name | Select-Object -Skip 1 | Foreach-Object {
  $start = $_.start
  $end = $_.end
  $song = ("{0}.mp4" -f $_.song)
  Write-Host "ffmpeg -y -i $output_name -avoid_negative_ts make_zero -fflags +genpts -ss $start -to $end -c:a aac $song"
}


