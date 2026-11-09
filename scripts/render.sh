#!/usr/bin/env bash
# Render a Reel props JSON on the owner's PC and bring back the mp4 plus a frame sheet.
#   scripts/render.sh <props.json> <name> [draft|final]     -> renders/<name>.mp4, renders/<name>.sheet.jpg
# draft = 540x960 (fast), final = 1080x1920. Several props files can be rendered in one call: pass pairs "props name".
cd "$(dirname "$0")/.."
MODE=draft; ARGS=()
for a in "$@"; do case "$a" in draft|final) MODE=$a ;; *) ARGS+=("$a") ;; esac; done
scripts/pc_sync.sh push >/dev/null
SSH='ssh -o BatchMode=yes -o ConnectTimeout=20 -o ProxyCommand="tailscale nc %h %p"'
rsync -az -e "$SSH" makes bench gamer@arch:reels-loop/repo/ --exclude '*.mp4'
CMD='cd ~/reels-loop/repo/remotion && mkdir -p ../renders && rm -rf build && npx remotion bundle src/index.ts --out-dir build >/dev/null 2>&1 || { echo BUNDLE_FAILED; npx remotion bundle src/index.ts --out-dir build 2>&1 | tail -15; exit 1; }; '
i=0; while [ $i -lt ${#ARGS[@]} ]; do P=${ARGS[$i]}; N=${ARGS[$((i+1))]}; i=$((i+2))
  CMD+="bash ../scripts/pc_render_one.sh $P $N $MODE & "
  [ $((i % 8)) = 0 ] && CMD+="wait; "
done
CMD+="wait"
PC_TIMEOUT=${PC_TIMEOUT:-900} scripts/pc "$CMD"
rsync -az -e "$SSH" --include '*.mp4' --include '*.jpg' --exclude '*' gamer@arch:reels-loop/repo/renders/ renders/
