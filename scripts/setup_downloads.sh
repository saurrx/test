#!/usr/bin/env bash
# Seed reels first (21, needed for analysis), then the full list. One Instagram client at a time.
cd "$(dirname "$0")/.."
yt-dlp -q --no-warnings --sleep-requests 3 --sleep-interval 6 -f "b[height<=1280]/b" \
  -o "data/seed/%(channel)s__%(id)s.%(ext)s" -a data/seed/urls.txt > data/seed/_download.log 2>&1
echo "SEED DONE $(ls data/seed/*.mp4 2>/dev/null | wc -l)" >> data/seed/_download.log
nohup python3 scripts/analyze_reel.py data/seed/*.mp4 > analysis/_seed_run.log 2>&1 &
scripts/download_reels.sh > data/reels/_download.log 2>&1
