param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$name = $mp4_file.Basename
if ($name -like "*_mix") {
  $orig_name = $name -replace "_mix"
  Write-Host $orig_name
  $mp3_name = "{0}.mp3" -f $orig_name
  Write-Host $mp3_name
  $chapters_name = "{0}.csv" -f $orig_name
  Write-Host $chapters_name
} else {
  $mp3_name = "{0}.mp3" -f $name
  $chapters_name = "{0}.csv" -f $name
}

$chapters = Import-Csv -Path $chapters_name | Select-Object -Skip 1 | Foreach-Object {
  $start = $_.start
  $end = $_.end
  $song = ("{0}.mp4" -f $_.song)
  if (!(Test-Path $song -PathType Leaf)) {
    ffmpeg -v quiet -stats -y -i $file -avoid_negative_ts make_zero -fflags +genpts -ss $start -to $end -c:a aac $song
  }
}


