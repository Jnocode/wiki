#!/bin/sh
set -eu
TOKEN="$(openclaw secrets store get GITHUB_TOKEN --scope team --plain)"
export GITHUB_TOKEN="$TOKEN"
unset TOKEN
exec python3 /mnt/d/Workspace/03_Dev_Projects/wiki/publish_shared_brain_to_github.py
