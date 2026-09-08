#!/usr/bin/env python3
"""Publish the canonical shared-brain projection to GitHub Pages.

Designed for OpenClaw's WSL cron. It never stages unrelated files and fails closed
when push or public read-back fails.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

REPO = Path(__file__).resolve().parent
SYNC = REPO / "sync_shared_brain_to_github.py"
COMPILER = REPO / "compile_hot_cache.py"
ASKPASS = REPO / "git_askpass_env.sh"
TARGETS = [
    "index.html",
    "hot.md",
    "concepts/agent-collaboration-contract.md",
    "concepts/codex-context-management.md",
    "concepts/data-source-integrity-and-fallback.md",
    "concepts/discord-ai-digest-presentation.md",
    "concepts/podcast-current-production-contract.md",
    "concepts/runtime-environment-map.md",
    "concepts/workspace-architecture.md",
]
PROBE = "https://jnocode.github.io/wiki/concepts/codex-context-management.md"
MARKER = "Codex 上下文管理與跨 Agent 帳本"


def run(*args: str, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO, text=True, capture_output=True, check=check, env=env)


def main() -> int:
    compiled = run(sys.executable, str(COMPILER), check=False)
    if compiled.returncode != 0:
        print("PUBLISH_BLOCKED hot_cache_compile_failed=true", file=sys.stderr)
        return 1
    sync = run(sys.executable, str(SYNC))
    changed = [line.removeprefix("UPDATED ") for line in sync.stdout.splitlines() if line.startswith("UPDATED ")]

    # Always stage only the allow-listed projection. This also recovers a staged
    # change left behind by a previous failed commit.
    run("git", "add", *TARGETS)
    staged = [x for x in run("git", "diff", "--cached", "--name-only").stdout.splitlines() if x]
    if any(x not in TARGETS for x in staged):
        print("PUBLISH_BLOCKED staged_scope_violation=true", file=sys.stderr)
        return 2

    pending = run("git", "rev-list", "--count", "origin/main..HEAD").stdout.strip()
    if not staged and pending == "0":
        print("PUBLISH_NOOP shared_brain_unchanged=true")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if staged:
        commit = run(
            "git", "-c", "user.name=jnocode", "-c",
            "user.email=78481666+Jnocode@users.noreply.github.com",
            "commit", "-m", f"docs: sync shared brain to GitHub Pages ({stamp})", check=False,
        )
        if commit.returncode != 0:
            print("PUBLISH_BLOCKED commit_failed=true", file=sys.stderr)
            return 3
    push_env = os.environ.copy()
    if os.name != "nt":
        if not push_env.get("GITHUB_TOKEN"):
            print("PUBLISH_BLOCKED github_token_missing=true", file=sys.stderr)
            return 4
        push_env.update({
            "GIT_ASKPASS": str(ASKPASS),
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "credential.helper",
            "GIT_CONFIG_VALUE_0": "",
        })
    push = run("git", "push", "origin", "main", check=False, env=push_env)
    if push.returncode != 0:
        print("PUBLISH_BLOCKED push_failed=true", file=sys.stderr)
        return 4

    with urlopen(PROBE + "?sync=" + stamp, timeout=30) as response:
        body = response.read().decode("utf-8", "replace")
        status = response.status
    if status != 200 or MARKER not in body:
        print("PUBLISH_BLOCKED public_readback_failed=true", file=sys.stderr)
        return 5
    print(f"PUBLISH_OK changed={len(changed)} committed={len(staged)} public_readback=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
