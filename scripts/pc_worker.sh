#!/usr/bin/env bash
# Runs ON THE PC (from ~/reels-loop/repo). Downloads reels in priority order and analyses each one right after,
# so results arrive steadily. One Instagram request stream, polite pacing, back-off on errors.
# Cookies are OFF by default; set COOKIES_BROWSER=firefox only if anonymous access gets blocked.
cd "$(dirname "$0")/.."
PY=../.venv/bin/python; YT=../.venv/bin/yt-dlp
LIST=data/reels_priority.tsv; [ -s "$LIST" ] || LIST=data/all_reels.tsv
mkdir -p data/reels analysis
fails=0
while IFS=$'\t' read -r h s; do
  d="data/reels/$h"; mkdir -p "$d"
  if [ ! -s "$d/$s.mp4" ]; then
    ok=0
    for i in 1 2 3; do
      $YT -q --no-warnings ${COOKIES_BROWSER:+--cookies-from-browser $COOKIES_BROWSER} -f "b[height<=1280]/b" \
        -o "$d/%(id)s.%(ext)s" --write-info-json "https://www.instagram.com/p/$s/" 2>>data/reels/_errors.log && { ok=1; break; }
      sleep $((i * 90))
    done
    if [ $ok = 1 ]; then fails=0; else
      echo "FAIL $h $s" >> data/reels/_failed.txt; fails=$((fails + 1))
      [ $fails -ge 5 ] && { echo "$(date -u +%FT%TZ) 5 failures in a row, sleeping 30 min" >> data/reels/_progress.txt; sleep 1800; fails=0; }
      continue
    fi
    sleep $((5 + RANDOM % 6))
  fi
  nice -n 10 $PY scripts/analyze_reel.py "$d/$s.mp4" >> analysis/_pc_run.log 2>&1
  echo "$(date -u +%FT%TZ) $(find data/reels -name '*.mp4' | wc -l) downloaded, $(ls analysis | grep -c __) analysed" > data/reels/_progress.txt
done < "$LIST"
echo "$(date -u +%FT%TZ) DONE" >> data/reels/_progress.txt
