#!/bin/sh
set -eu
# PATH 首位寫死正確 launcher：cron 子行程繼承 gateway 環境時，
# PATH 首位可能是 node-v24/bin 下的舊版 OpenClaw 2026.9.4（schema 17），
# 會因 DB 已被新版升到 schema 18 而拒絕啟動。
# /home/openclaw/.openclaw/bin/openclaw 是 2026.9.6 的正式 launcher。
PATH="/home/openclaw/.openclaw/bin:$PATH"
export PATH
TOKEN="$(openclaw secrets store get GITHUB_TOKEN --scope team --plain)"
export GITHUB_TOKEN="$TOKEN"
unset TOKEN
exec python3 /mnt/d/Workspace/03_Dev_Projects/wiki/publish_shared_brain_to_github.py
