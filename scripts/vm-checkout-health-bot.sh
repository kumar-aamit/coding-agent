#!/usr/bin/env bash
# Run on the OpenClaw VM (dcloud) to fetch the health-bot scaffold branch.
set -euo pipefail

REPO="${REPO:-/home/dcloud/openclaw/workspace/coding-agent}"
BRANCH="${BRANCH:-health-bot}"

cd "$REPO"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

echo "Branch: $(git branch --show-current)"
echo "Commit: $(git log -1 --oneline)"
echo
ls -la database.py models.py schemas.py llm_client.py main.py HEALTH_APP.md opencode.json
