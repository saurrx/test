#!/usr/bin/env bash
# render_get.sh <job> [wait]  -> RUNNING, or the job's OK/FAIL lines; pulls mp4 + sheets when done. With "wait", blocks (max 25 min).
cd "$(dirname "$0")/.."; JOB=$1
SSH='ssh -o BatchMode=yes -o ConnectTimeout=20 -o ProxyCommand="tailscale nc %h %p"'
for i in $(seq 1 100); do
  R=$(scripts/pc "cat ~/reels-loop/repo/renders/_job_$JOB.done 2>/dev/null")
  [ -n "$R" ] && break; [ "$2" = wait ] || { echo RUNNING; exit 0; }; sleep 15
done
echo "$R"; rsync -az -T /tmp -e "$SSH" --exclude '*_final.mp4' --exclude '*_1080.mp4' --include '*.mp4' --include '*.jpg' --exclude '*' --max-size=40m gamer@arch:reels-loop/repo/renders/ renders/
