#!/usr/bin/env bash
# Download every reel listed in data/all_reels.tsv (handle<TAB>shortcode), skipping ones already present.
# Gentle on Instagram: 2 parallel workers, small sleep between requests, retries on failure.
cd "$(dirname "$0")/.."
dl() {
  h="$1"; s="$2"; d="data/reels/$h"; mkdir -p "$d"
  [ -s "$d/$s.mp4" ] && return 0
  for i in 1 2 3; do
    yt-dlp -q --no-warnings -f "b[height<=1280]/b" -o "$d/%(id)s.%(ext)s" --write-info-json \
      "https://www.instagram.com/p/$s/" && return 0
    sleep $((i*60))
  done
  echo "FAIL $h $s" >> data/reels/_failed.txt
}
export -f dl
awk -F'\t' '{print $1" "$2}' data/all_reels.tsv | xargs -P 1 -n 2 bash -c 'dl "$0" "$1"; sleep 6'
echo DONE
