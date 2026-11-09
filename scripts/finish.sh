#!/usr/bin/env bash
# Finish a final render ON THE PC and pull it: loudness -14 LUFS / -1.5 dBTP, capped bitrate (film grain inflates files), faststart.
#   finish.sh <render name on PC, no .mp4> <output name>   -> renders/best/<output>.mp4
cd "$(dirname "$0")/.."
scripts/pc "cd ~/reels-loop/repo/renders && ffmpeg -y -v error -i $1.mp4 -af loudnorm=I=-14:TP=-2.5:LRA=11,alimiter=limit=0.79:level=false -ar 48000 -c:a aac -b:a 192k -c:v libx264 -preset slow -crf 25 -maxrate 3500k -bufsize 7M -pix_fmt yuv420p -movflags +faststart $2.mp4 && ls -la $2.mp4 | awk '{print \$5}'"
rsync -az -e 'ssh -o BatchMode=yes -o ProxyCommand="tailscale nc %h %p"' gamer@arch:reels-loop/repo/renders/$2.mp4 renders/best/
