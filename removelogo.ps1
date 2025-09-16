param (
   [Parameter(Mandatory=$true)][string]$file
)

$mp4_file = Get-Item $file
$basename = $mp4_file.Basename
$mixname = "{0}_mix.mp4" -f $basename

ffmpeg -i .\$file -vf "delogo=x=1440:y=980:w=460:h=80" -c:a copy .\$mixname