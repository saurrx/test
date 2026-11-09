#!/usr/bin/env bash
# Bring the cloud side back after a worker restart: Tailscale (saved state, no new login) and the autocommit loop.
cd "$(dirname "$0")/.."
pgrep -x tailscaled >/dev/null || { nohup tailscaled --tun=userspace-networking --socks5-server=localhost:1055 --state=/var/lib/tailscale/tailscaled.state > /var/log/tailscaled.log 2>&1 & sleep 5; }
pgrep -f scripts/autocommit.sh >/dev/null || { nohup scripts/autocommit.sh > /dev/null 2>&1 & }
[ -x /usr/local/bin/pc ] || cp scripts/pc /usr/local/bin/pc
tailscale status 2>&1 | grep -q arch && echo "tailscale ok" || { echo "TAILSCALE DOWN"; tailscale up --hostname=claude-cloud-reels --shields-up=true 2>&1 | head -4; }
