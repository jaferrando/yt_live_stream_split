param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$name = $mp4_file.Basename

$mp3 = "{0}.mp3" -f $name 
$mp4 = "{0}.mp4" -f $name 
$out = "{0}_mix.mp4" -f $name 

ffmpeg -v quiet -stats -i $mp3 -i $mp4 -c:v copy -c:a aac $out

