#!/usr/bin/env bash
# Runs ON THE PC from remotion/: render one Reel props file from the prebuilt bundle, retry once, make a frame sheet.
P=$1; N=$2; MODE=$3
[ "$MODE" = draft ] && Q="--scale=0.5 --jpeg-quality=70 --crf=26" || Q="--crf=18"
R="npx remotion render ${BUILD:-build} Reel ../renders/$N.mp4 --props=../$P $Q --gl=swangle --concurrency=${RCONC:-4} --browser-executable=/usr/bin/chromium --chrome-mode=chrome-for-testing"
if $R >../renders/$N.log 2>&1 || $R >../renders/$N.log 2>&1; then
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ../renders/$N.mp4)
  ffmpeg -y -v error -i ../renders/$N.mp4 -vf "fps=20/$D,scale=180:-2,tile=10x2" -frames:v 1 ../renders/$N.sheet.jpg
  echo "OK $N"
else echo "FAIL $N"; tail -4 ../renders/$N.log; fi
