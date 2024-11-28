param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$name = $mp4_file.Basename

$mp3 = "{0}.mp3" -f $name

if (-Not (Test-Path $mp3)) {
  $mp3 = "{0}.m4a" -f $name
}

if(-Not (Test-Path $mp3)){
  Write-Host "Audio file not found for {0}" -f $name
  exit 1
}

$mp4 = "{0}.mp4" -f $name 
$out = "{0}_mix.mp4" -f $name 

ffmpeg -v quiet -stats -i $mp3 -i $mp4 -c:v copy -c:a aac $out

