param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$name = $mp4_file.Basename
if ($name -like "*_mix") {
  $orig_name = $name -replace "_mix"
  Write-Host $orig_name
  $m4a_name = "{0}.m4a" -f $orig_name
  Write-Host $mp3_name
  $chapters_name = "{0}.csv" -f $orig_name
  Write-Host $chapters_name
} else {
  $m4a_name = "{0}.m4a" -f $name
  $chapters_name = "{0}.csv" -f $name
}
Write-Host $chapters_name
$chapters = Import-Csv -Path $chapters_name | Foreach-Object {
  $start = $_.start
  $end = $_.end
  $song = ("{0}.mp4" -f $_.song)
  Write-Host $song
  if (!(Test-Path $song -PathType Leaf)) {
    ffmpeg -v quiet -stats -y -i $file -avoid_negative_ts make_zero -fflags +genpts -ss $start -to $end -c:a aac $song
  }
}
