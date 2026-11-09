#!/usr/bin/env bash
# Runs ON THE PC. Metadata-only pass (caption, counts, cover image) for every reel, slowest-priority reels first so it
# does not duplicate what pc_worker.sh is about to fetch. One request every ~20 s; stops for 30 min after 4 failures in a row.
cd "$(dirname "$0")/.."
YT=../.venv/bin/yt-dlp; fails=0
while IFS=$'\t' read -r h s <&3; do
  d="data/reels/$h"; mkdir -p "$d"
  [ -s "$d/$s.info.json" ] && continue
  if $YT -q --no-warnings --skip-download --write-info-json --write-thumbnail --convert-thumbnails jpg -o "$d/%(id)s.%(ext)s" "https://www.instagram.com/p/$s/" </dev/null 2>>data/reels/_meta_errors.log; then fails=0
  else fails=$((fails + 1)); [ $fails -ge 4 ] && { sleep 1800; fails=0; }; fi
  sleep $((17 + RANDOM % 7))
done 3< <(tac data/reels_priority.tsv)
