#!/usr/bin/env bash
# Commit + push background job outputs every 10 minutes so nothing is lost if the container is reclaimed.
# data/reels/*/ is gitignored so in-progress downloads don't show as untracked; the metadata is force-added here.
cd "$(dirname "$0")/.."
B=claude/determined-cannon-c2c60l
while true; do
  git add -A
  find data/reels -name '*.info.json' -print0 2>/dev/null | xargs -0 -r git add -f
  if ! git diff --cached --quiet; then
    git commit -qm "Auto-snapshot: background job outputs

Co-Authored-By: Claude <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Gy5RgGBibuvxR5H9sESUN3" && { git pull -q --rebase -X theirs origin "$B" || git rebase --abort; git push -q origin "$B"; }
  fi
  sleep 600
done
