#!/usr/bin/env bash
# Sync with the owner's PC (gamer@arch over Tailscale). The PC does Instagram downloads, transcription and heavy renders.
#   pc_sync.sh push   -> send scripts/, remotion/ (no node_modules), data lists to the PC
#   pc_sync.sh pull   -> bring back analysis/ (no raw frames), reel metadata, renders
cd "$(dirname "$0")/.."
SSH='ssh -o StrictHostKeyChecking=accept-new -o BatchMode=yes -o ConnectTimeout=20 -o ProxyCommand="tailscale nc %h %p"'
R=gamer@arch:reels-loop/repo
case "$1" in
  push) rsync -az -e "$SSH" --exclude node_modules --exclude out --exclude '*.mp4' --exclude .git \
          scripts remotion data/all_reels.tsv data/reels_priority.tsv data/creators data/seed/urls.txt "$R/" --relative ;;
  pull) rsync -az -e "$SSH" --exclude 'frames/' --exclude 'frames_2s/' "$R/analysis/" analysis/
        rsync -az -e "$SSH" --include '*/' --include '*.info.json' --include '_failed.txt' --include '_progress.txt' --exclude '*' "$R/data/reels/" data/reels/
        rsync -az -e "$SSH" "$R/renders/" renders/ 2>/dev/null || true ;;
  *) echo "usage: $0 push|pull"; exit 1 ;;
esac
