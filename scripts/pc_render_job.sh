#!/usr/bin/env bash
# Runs ON THE PC as a detached systemd unit, so a restart of the cloud session cannot kill a render.
#   pc_render_job.sh <job> <draft|final> <props> <name> [<props> <name> ...]   -> renders/<name>.mp4, renders/_job_<job>.done
cd "$(dirname "$0")/../remotion"; JOB=$1; MODE=$2; shift 2
export BUILD=build_$JOB; rm -f ../renders/_job_$JOB.done; mkdir -p ../renders
rm -rf $BUILD && npx remotion bundle src/index.ts --out-dir $BUILD > ../renders/_job_$JOB.log 2>&1 || { echo BUNDLE_FAILED > ../renders/_job_$JOB.done; exit 1; }
n=0; while [ $# -ge 2 ]; do bash ../scripts/pc_render_one.sh "$1" "$2" $MODE >> ../renders/_job_$JOB.log 2>&1 & shift 2; n=$((n + 1)); [ $((n % 3)) = 0 ] && wait; done; wait
if [ "$MODE" = final ]; then for f in "$@"; do :; done; fi
rm -rf $BUILD; grep -E "^(OK|FAIL)" ../renders/_job_$JOB.log > ../renders/_job_$JOB.done; echo END >> ../renders/_job_$JOB.done
