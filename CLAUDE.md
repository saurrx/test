# Operating rules for Claude in this repo

This is an experimental sandbox repo with no real data. The owner wants Claude to run autonomously.

- Do not stop to ask for decisions. Pick the most sensible option, act, and record it.
- Log every non-obvious choice (what, why, alternatives skipped) as a dated entry in `DECISIONS.md`.
- Keep a running `TASKS.md`: what is in progress, what is done, what comes next. Pick up from it at the start of each session, since cloud containers are ephemeral and only what is committed survives.
- Commit and push after each meaningful step so work is never lost when a container is reclaimed.
- Only stop for things that actually need the owner: a missing credential, an external account action, or spending real money.
