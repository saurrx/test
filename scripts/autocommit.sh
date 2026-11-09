#!/usr/bin/env bash
# Commit + push background job outputs every 10 minutes so nothing is lost if the container is reclaimed.
cd "$(dirname "$0")/.."
while true; do
  if [ -n "$(git status --porcelain)" ]; then
    git add -A && git commit -qm "Auto-snapshot: background job outputs

Co-Authored-By: Claude <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Gy5RgGBibuvxR5H9sESUN3" && { git pull -q --rebase -X theirs origin claude/determined-cannon-c2c60l || git rebase --abort; git push -q origin claude/determined-cannon-c2c60l; }
  fi
  sleep 600
done
