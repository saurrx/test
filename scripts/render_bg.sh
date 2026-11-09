#!/usr/bin/env bash
# Start a render job on the PC that survives cloud restarts.   render_bg.sh <job> <draft|final> <props> <name> [...]
# Check / collect with:  scripts/render_get.sh <job>     (prints the job's OK/FAIL lines once finished and pulls the files)
cd "$(dirname "$0")/.."; JOB=$1; MODE=$2; shift 2
SSH='ssh -o BatchMode=yes -o ConnectTimeout=20 -o ProxyCommand="tailscale nc %h %p"'
scripts/pc_sync.sh push >/dev/null && rsync -az -e "$SSH" makes bench gamer@arch:reels-loop/repo/ --exclude '*.mp4' --exclude '*.wav'
scripts/pc "systemctl --user reset-failed render-$JOB 2>/dev/null; systemd-run --user --unit=render-$JOB --setenv=RCONC=${RCONC:-5} --working-directory=\$HOME/reels-loop/repo bash scripts/pc_render_job.sh $JOB $MODE $* 2>&1 | tail -1"
