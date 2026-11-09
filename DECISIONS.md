# Decisions log

## 2026-11-09 — Bootstrap
- Session already runs in **auto** permission mode, so no settings.json permission changes were needed.
- Added CLAUDE.md so every future session (including scheduled ones) inherits "don't ask, decide and log".
- State lives in committed files (TASKS.md / DECISIONS.md) because containers are ephemeral.

## 2026-11-09 — Runner setup (session_01Gy5RgGBibuvxR5H9sESUN3)
- **Treg balance check:** $0.581 (team shifuventures). The `mcp__Treg__*` allow rule in settings.json doesn't match this connector's real server id (a UUID), but auto mode let the call through with no prompt. Spend: 1 call, $0 (balance is free).
- **Remotion:** hand-written minimal scaffold in `remotion/` pinned to remotion@4.0.242 / react@18.3.1, instead of `create-video`, which is interactive and pulls a template. Remotion's own headless-shell download worked here, so the `/opt/pw-browsers/chromium` fallback wasn't needed. Smoke render: 60 frames, 1080x1920, 2.05 s, h264+aac.
- **Second runner on the branch:** session_01Gy5RgDkmrkJXPDhauesKmA (idle, waiting on the owner's "go") pushed to this branch at 19:02 UTC. Its download log ends in Instagram 429s and then `Terminated`. Risk: two runners pushing to the branch, or two downloaders doubling the Instagram request rate. Mitigation: `autocommit.sh` now pulls and rebases before pushing. Recommend the owner only says "go" in one of the two sessions.
- **My mistake (fixed):** I started `download_reels.sh` before pip had finished installing yt-dlp, which produced "command not found" failures. I killed it, deleted `_failed.txt`, and will restart it once yt-dlp is installed.
